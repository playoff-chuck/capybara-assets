#!/usr/bin/env python3
"""Capybara Squad API - high scores, nuts board, anonymous round stats, anonymous error/event log, cloud save by restore code.
Stdlib only (http.server + sqlite3). Listens on 127.0.0.1:8770 behind Caddy (/api/*).
Privacy: no cookies, no IPs stored. Rate limiting uses an in-memory hash of
(IP + random daily salt) that is never written to disk and is forgotten daily.
"""
import hashlib, json, os, re, secrets, sqlite3, threading, time
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import csfilter
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

DB = os.environ.get("CAPY_DB", "/srv/capy-api/data.db")
HOST, PORT = "127.0.0.1", int(os.environ.get("CAPY_PORT", "8770"))
MAX_BODY = 4096
POST_PER_MIN = 10
GET_PER_MIN = 120
MODES = ("chill", "pro", "nuts")
MAX_SCORE = 100_000_000
MAX_WAVE = 500
MAX_LEVEL = 1000
RUN_RETENTION_DAYS = 365
VERSION = "1.2"
SAVE_MAX_BODY = 60000
SAVE_MAX_DATA = 48000
SAVE_KEEP = 5
SAVE_RETENTION_DAYS = 730
SAVES_PER_MIN = 20
SAVE_READS_PER_MIN = 10
SQUAD_ABC = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
SQUAD_RE = re.compile(r"[ABCDEFGHJKMNPQRSTUVWXYZ23456789]{6}")
SQUAD_MAX_N = 100000
CODE_RE = re.compile(r"[0-9A-HJKMNP-TV-Z]{10}")
SAVE_KEY_RE = re.compile(r"(tarnturm|capy)-[a-z0-9_-]{1,40}")
EVENT_RETENTION_DAYS = 90
EVENT_MAX_BODY = 8192
EVENTS_PER_MIN = 20
EVENT_KINDS = ("thief", "start", "error", "leave", "back", "wave", "tut", "tutskip", "cert", "hack", "set", "buy", "spec", "cancel", "ad", "death", "restart", "perf", "wend", "near", "idle", "quit", "sess", "tip", "poll", "rate", "rescue", "audio")   # V594, V647, V678
UID_RE = re.compile(r"[A-Z0-9]{4}-[A-Z0-9]{4}")
ADMIN_UIDS = ("M2HL-KCQH", "BEEM-MGDC", "5478-BQ27", "R47V-R8F3", "69JD-AFLF")   # + 69JD-AFLF (Martins Handy nach «Street player», 11.11. 01:10)   # + R47V-R8F3 (Martins Handy nach Datenverlust, 11.11.)   # Martins Geräte (neu nach Reset 09.11.)
PLAYER_PER_MIN = 8
PLAYER_MAX_BODY = 6000
PLAYER_RETENTION_DAYS = 730
import hmac
def clean_profile(v, depth=0):
    """Nur einfache Werte: Zahlen, kurze Texte, kleine Listen/Objekte (max. 2 Ebenen)."""
    if isinstance(v, bool): return v
    if isinstance(v, (int, float)):
        return max(-1e12, min(1e12, v)) if v == v else 0
    if isinstance(v, str): return clean_text(v, 120)
    if depth >= 2: return None
    if isinstance(v, list): return [clean_profile(x, depth + 1) for x in v[:12]]
    if isinstance(v, dict):
        out = {}
        for k, x in list(v.items())[:40]:
            if isinstance(k, str) and re.fullmatch(r"[A-Za-z0-9_]{1,16}", k): out[k] = clean_profile(x, depth + 1)
        return out
    return None

# ---------- database ----------
SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS scores(
  id INTEGER PRIMARY KEY, mode TEXT NOT NULL, pid TEXT, callsign TEXT NOT NULL,
  score INTEGER NOT NULL, wave INTEGER NOT NULL, lines INTEGER, kills INTEGER, t INTEGER NOT NULL);
CREATE INDEX IF NOT EXISTS scores_mode_score ON scores(mode, score DESC, wave DESC);
CREATE UNIQUE INDEX IF NOT EXISTS scores_mode_pid ON scores(mode, pid) WHERE pid IS NOT NULL;
CREATE TABLE IF NOT EXISTS nuts(
  id INTEGER PRIMARY KEY, pid TEXT, callsign TEXT NOT NULL, continent INTEGER NOT NULL,
  level INTEGER NOT NULL, t INTEGER NOT NULL);
CREATE INDEX IF NOT EXISTS nuts_cont ON nuts(continent, level DESC);
CREATE UNIQUE INDEX IF NOT EXISTS nuts_cont_pid ON nuts(continent, pid) WHERE pid IS NOT NULL;
CREATE TABLE IF NOT EXISTS runs(
  id INTEGER PRIMARY KEY, t INTEGER NOT NULL, ver TEXT, mode TEXT, wave INTEGER, why TEXT,
  gold INTEGER, lines INTEGER, splats INTEGER, score INTEGER, medals INTEGER,
  max_speed INTEGER, mins REAL, hero TEXT, dev INTEGER);
CREATE INDEX IF NOT EXISTS runs_t ON runs(t);
CREATE TABLE IF NOT EXISTS events(
  id INTEGER PRIMARY KEY, t INTEGER NOT NULL, ver TEXT, sess TEXT, kind TEXT NOT NULL, wave INTEGER, scr TEXT,
  msg TEXT, src TEXT, mins REAL, dev INTEGER, plat TEXT, br TEXT, sw INTEGER, sh INTEGER, mem REAL);
CREATE INDEX IF NOT EXISTS events_t ON events(t);
CREATE INDEX IF NOT EXISTS events_kind ON events(kind, t);
CREATE TABLE IF NOT EXISTS saves(
  id INTEGER PRIMARY KEY, k TEXT NOT NULL, t INTEGER NOT NULL, ver TEXT, wave INTEGER, size INTEGER, data TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS saves_k ON saves(k, t DESC);
CREATE TABLE IF NOT EXISTS squads(
  code TEXT PRIMARY KEY, t INTEGER NOT NULL, n INTEGER NOT NULL DEFAULT 0, last INTEGER);
CREATE TABLE IF NOT EXISTS squad_joins(h TEXT PRIMARY KEY, t INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS kv(k TEXT PRIMARY KEY, v TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS testers(id INTEGER PRIMARY KEY, t INTEGER NOT NULL, name TEXT, email TEXT NOT NULL, tg TEXT, msg TEXT, lang TEXT, site TEXT);
CREATE TABLE IF NOT EXISTS players(uid TEXT PRIMARY KEY, first INTEGER NOT NULL, last INTEGER NOT NULL, n INTEGER NOT NULL DEFAULT 0, data TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS players_first ON players(first);
CREATE TABLE IF NOT EXISTS plays(sess TEXT PRIMARY KEY, uid TEXT, first INTEGER NOT NULL, last INTEGER NOT NULL, n INTEGER NOT NULL DEFAULT 0, secs INTEGER NOT NULL DEFAULT 0, maxw INTEGER NOT NULL DEFAULT 0, ver TEXT, ch TEXT, os TEXT, osv TEXT, model TEXT, br TEXT, sw INTEGER, sh INTEGER, tz TEXT, off INTEGER, lang TEXT, team INTEGER NOT NULL DEFAULT 0, dev INTEGER NOT NULL DEFAULT 0);
CREATE INDEX IF NOT EXISTS plays_uid ON plays(uid, first);
CREATE INDEX IF NOT EXISTS plays_first ON plays(first);
CREATE TABLE IF NOT EXISTS feedback(id INTEGER PRIMARY KEY, t INTEGER NOT NULL, uid TEXT, ver TEXT, ch TEXT, lang TEXT, src TEXT, wave INTEGER, stars INTEGER, msg TEXT, plat TEXT);
CREATE INDEX IF NOT EXISTS feedback_t ON feedback(t);
"""

class _DB:
    # sqlite3's own "with conn" only commits/rolls back and never closes:
    # every request leaked a file handle until the 1024 limit was hit.
    def __enter__(self):
        self.c = sqlite3.connect(DB, timeout=10)
        self.c.row_factory = sqlite3.Row
        return self.c
    def __exit__(self, et, ev, tb):
        try:
            if et is None:
                self.c.commit()
            else:
                self.c.rollback()
        finally:
            self.c.close()
        return False

def db():
    return _DB()

def init_db():
    with db() as c:
        c.executescript(SCHEMA)
        cols = {r[1] for r in c.execute("PRAGMA table_info(events)")}   # V594: Metrik-Spalten, alte Zeilen bleiben
        for col, typ in (("uid", "TEXT"), ("ch", "TEXT"), ("team", "INTEGER DEFAULT 0"), ("data", "TEXT")):
            if col not in cols:
                c.execute(f"ALTER TABLE events ADD COLUMN {col} {typ}")
        c.execute("CREATE INDEX IF NOT EXISTS events_uid ON events(uid, t)")

def purge_old_runs():
    cutoff = int(time.time() * 1000) - RUN_RETENTION_DAYS * 86400 * 1000
    ecut = int(time.time() * 1000) - EVENT_RETENTION_DAYS * 86400 * 1000
    with db() as c:
        c.execute("DELETE FROM runs WHERE t < ?", (cutoff,))
        c.execute("DELETE FROM events WHERE t < ?", (ecut,))
        scut = int(time.time() * 1000) - SAVE_RETENTION_DAYS * 86400 * 1000
        c.execute("DELETE FROM saves WHERE k IN (SELECT k FROM saves GROUP BY k HAVING MAX(t) < ?)", (scut,))

def is_bot_profile(x):
    """Google-Play-Vorabtest, Emulator, Google Test Lab, Server-/Headless-Browser, Roboter, Familien-Testgeräte (Malediven)."""
    if not isinstance(x, dict): return False
    os_, app, scr, tz, loc = (str(x.get(k) or "") for k in ("os", "app", "scr", "tz", "loc"))
    if "sdk_gphone" in os_ or "OnePlus8Pro" in os_: return True
    if tz == "America/Los_Angeles" and "Android" in os_: return True
    if tz == "Indian/Maldives": return True
    if os_.startswith("Linux"): return True
    if "Edge 12" in app or tz in ("Etc/Unknown", "+00:00"): return True
    if re.match(r"\d+×\d+ @1x", scr) and ("iPhone" in os_ or "Android" in os_): return True
    if os_.startswith("Windows") and scr.startswith(("800×600", "1024×1024", "1080×600")): return True
    return False

def admin_stats(c, days):
    """V594: Trichter, Ausstiege, Boss-Hack, Musik aus, Wiederkehr – nur echte Spieler (ohne team/dev/bot)."""
    now = now_ms(); since = now - days * 86400 * 1000
    bad = set(ADMIN_UIDS)
    for r in c.execute("SELECT uid, data FROM players"):
        try: dd = json.loads(r["data"])
        except Exception: dd = {}
        if dd.get("team") or dd.get("dev") or dd.get("bot") or is_bot_profile(dd): bad.add(r["uid"])
    ev = [r for r in c.execute("SELECT t, sess, kind, wave, scr, uid, ch, data FROM events WHERE t >= ? AND uid IS NOT NULL AND dev=0 AND COALESCE(team,0)=0 ORDER BY t", (since,)) if r["uid"] not in bad]
    def dj(r):
        try: return json.loads(r["data"]) if r["data"] else {}
        except Exception: return {}
    U = {}
    sess_last = {}
    hack, deaths, perf, loads, chans, spec, buys, ads, sets = {}, {}, [], [], {}, {}, {}, {}, {}
    for r in ev:
        u = U.setdefault(r["uid"], {"first": r["t"], "last": r["t"], "tut": 0, "cert": 0, "w": 0, "mu": None, "skip": 0, "start": 0, "ch": r["ch"] or "?"})
        u["last"] = r["t"]; k = r["kind"]; x = dj(r)
        sess_last[r["sess"]] = (r["t"], r["scr"] or "?", r["wave"] or 0, k)
        if k in ("wave", "death") or (r["wave"] or 0) > 0: u["w"] = max(u["w"], r["wave"] or 0)
        if k == "start":
            if "mu" in x: u["mu"] = x.get("mu")
            if isinstance(x.get("ld"), (int, float)) and 0 < x["ld"] < 120000: loads.append(x["ld"])
        if k == "tut": u["tut"] = max(u["tut"], int(x.get("n") or 0)); u["start"] = 1
        if k == "wave" and (r["wave"] or 0) >= 1: u["start"] = 1
        if k == "tutskip": u["skip"] = max(u["skip"], int(x.get("n") or 1)); u["start"] = 1
        if k == "cert": u["cert"] = 1
        if k == "hack": hack[str(x.get("r") or "?")] = hack.get(str(x.get("r") or "?"), 0) + 1
        if k == "death": deaths[r["wave"] or 0] = deaths.get(r["wave"] or 0, 0) + 1
        if k == "perf" and isinstance(x.get("fps"), (int, float)): perf.append(x["fps"])
        if k == "spec": spec[str(x.get("k") or "?")] = spec.get(str(x.get("k") or "?"), 0) + 1
        if k == "buy": buys[str(x.get("k") or "?")] = buys.get(str(x.get("k") or "?"), 0) + 1
        if k == "ad": ads[str(x.get("a") or "?")] = ads.get(str(x.get("a") or "?"), 0) + 1
        if k == "set":
            for kk in ("music", "mute", "lang"):
                if kk in x: sets[f"{kk}={x[kk]}"] = sets.get(f"{kk}={x[kk]}", 0) + 1
                if kk == "music" and kk in x: u["mu"] = x[kk]
    for u in U.values(): chans[u["ch"]] = chans.get(u["ch"], 0) + 1
    n = len(U)
    steps = [("geöffnet", n), ("gestartet", sum(1 for u in U.values() if u["start"] or u["w"] > 0))]
    for i in range(1, 11): steps.append((f"Lektion {i}", sum(1 for u in U.values() if u["tut"] >= i)))
    steps += [("Urkunde", sum(1 for u in U.values() if u["cert"])), ("Welle 5", sum(1 for u in U.values() if u["w"] >= 5)),
              ("Welle 10", sum(1 for u in U.values() if u["w"] >= 10)), ("Welle 30", sum(1 for u in U.values() if u["w"] >= 30))]
    funnel = [{"step": a, "n": b, "pct": round(100 * b / n, 1) if n else 0} for a, b in steps]
    ex = {}
    for t, scr, w, k in sess_last.values():
        if now - t > 30 * 60 * 1000:
            key = f"{scr} · W{w}"; ex[key] = ex.get(key, 0) + 1
    exits = sorted(({"where": k, "n": v} for k, v in ex.items()), key=lambda x: -x["n"])[:15]
    mu_known = [u for u in U.values() if u["mu"] is not None]
    old1 = [u for u in U.values() if now - u["first"] > 86400000]; old7 = [u for u in U.values() if now - u["first"] > 7 * 86400000]
    ret1 = sum(1 for u in old1 if u["last"] - u["first"] > 20 * 3600000); ret7 = sum(1 for u in old7 if u["last"] - u["first"] > 7 * 86400000 - 4 * 3600000)
    loads.sort()
    extra = {}
    try:   # V647: Erleben je Welle, Frust-Signale, Umfrage, Bewertungen
        wb, near, idle, quits, sessl, poll, tips = {}, {}, {}, {}, [], {}, {}
        seq = {}
        thf = {}   # V652
        for r in ev:
            k = r["kind"]; x = dj(r); w = r["wave"] or 0
            seq.setdefault(r["sess"], []).append((r["t"], k, w))
            if k == "wend" and not x.get("nz"):
                b = wb.setdefault(w, [0, 0, 0, 0, 0])   # n, sekunden, leben verloren, wellen mit verlust, max stapel
                b[0] += 1; b[1] += int(x.get("s") or 0); lv = int(x.get("lv") or 0); b[2] += lv; b[3] += 1 if lv else 0; b[4] += int(x.get("mx") or 0)
            elif k == "near": near[w] = near.get(w, 0) + 1
            elif k == "idle": idle[w] = idle.get(w, 0) + 1
            elif k == "quit": kk = str(x.get("a") or "menu"); quits[kk] = quits.get(kk, 0) + 1
            elif k == "sess" and isinstance(x.get("s"), (int, float)) and 0 < x["s"] < 86400: sessl.append(int(x["s"]))
            elif k == "poll": kk = f"W{x.get('at') or w}"; pv = poll.setdefault(kk, {"up": 0, "mid": 0, "down": 0, "skip": 0}); vv = {1: "up", 0: "mid", -1: "down"}.get(x.get("v"), "skip"); pv[vv] += 1
            elif k == "tip": kk = f"{x.get('k') or '?'}:{x.get('a') or 'shown'}"; tips[kk] = tips.get(kk, 0) + 1
            elif k == "thief":   # V652
                ta = str(x.get("a") or "?"); thf[ta] = thf.get(ta, 0) + 1; g = int(x.get("g") or 0)
                if ta == "steal": thf["gs"] = thf.get("gs", 0) + g
                elif ta == "wolf": thf["gb"] = thf.get("gb", 0) + g
                elif ta == "gone": thf["gl"] = thf.get("gl", 0) + g
        rage = 0; quickrestart = 0
        for L in seq.values():
            for i, (t, k, w) in enumerate(L):
                if k != "death": continue
                for t2, k2, w2 in L[i + 1:i + 6]:
                    if t2 - t > 20000: break
                    if k2 == "leave": rage += 1; break
                    if k2 == "restart" and t2 - t < 8000: quickrestart += 1; break
        waves = []
        for w in sorted(wb):
            b = wb[w]
            if w < 1 or w > 150: continue
            waves.append({"w": w, "n": b[0], "sec": round(b[1] / b[0]), "lives": round(b[2] / b[0], 2), "lossPct": round(100 * b[3] / b[0]), "stack": round(b[4] / b[0], 1)})
        sessl.sort()
        fb = c.execute("SELECT t, uid, ver, ch, lang, src, wave, stars, msg, plat FROM feedback WHERE t >= ? ORDER BY t DESC LIMIT 60", (since,)).fetchall()
        st = [x["stars"] for x in fb if x["stars"]]
        extra = {"waves": waves, "near": near, "idle": idle, "quits": quits, "rage": rage, "quickRestart": quickrestart,
                 "thief": thf, "sessMedian": sessl[len(sessl) // 2] if sessl else None, "sessN": len(sessl), "poll": poll, "tips": tips,
                 "rating": {"n": len(st), "avg": round(sum(st) / len(st), 2) if st else None, "dist": {str(i): st.count(i) for i in range(1, 6)}},
                 "feedback": [{"t": x["t"], "uid": x["uid"], "team": x["uid"] in bad, "ver": x["ver"], "ch": x["ch"], "lang": x["lang"], "src": x["src"], "w": x["wave"], "stars": x["stars"], "msg": x["msg"], "plat": x["plat"]} for x in fb]}
        try:   # V650
            mods, oss, hrs, wds, nP, tot = {}, {}, [0] * 24, [0] * 7, 0, 0
            for y in c.execute("SELECT uid, first, secs, os, osv, model, off FROM plays WHERE first >= ? AND dev=0 AND team=0", (since,)):
                if not y["uid"] or y["uid"] in bad: continue
                nP += 1; tot += y["secs"] or 0
                m = y["model"] or "?"; mods[m] = mods.get(m, 0) + 1
                o = ((y["os"] or "?") + " " + (y["osv"] or "")).strip(); oss[o] = oss.get(o, 0) + 1
                if y["off"] is not None:
                    lt = time.gmtime((y["first"] + y["off"] * 60000) / 1000); hrs[lt.tm_hour] += 1; wds[lt.tm_wday] += 1
            extra["plays"] = {"n": nP, "mins": round(tot / 60), "models": mods, "os": oss, "hours": hrs, "wd": wds}
        except Exception as e2:
            extra["plays"] = {"err": str(e2)[:120]}
    except Exception as e:
        extra = {"err": str(e)[:120]}
    return {"ok": True, "x": extra, "days": days, "players": n, "events": len(ev), "funnel": funnel, "exits": exits,
            "skipAt": {str(i): sum(1 for u in U.values() if u["skip"] == i) for i in range(1, 11) if any(u["skip"] == i for u in U.values())},
            "hack": hack, "deathsByWave": sorted(([w, c2] for w, c2 in deaths.items()), key=lambda x: -x[1])[:12],
            "musicOff": {"off": sum(1 for u in mu_known if not u["mu"]), "of": len(mu_known)},
            "return": {"d1": ret1, "d1of": len(old1), "d7": ret7, "d7of": len(old7)},
            "perf": {"n": len(perf), "avgFps": round(sum(perf) / len(perf), 1) if perf else None},
            "loadMs": {"n": len(loads), "median": loads[len(loads) // 2] if loads else None},
            "channels": chans, "spec": spec, "buy": buys, "ad": ads, "set": sets}

def save_key(code):
    """Der Code selbst wird nie gespeichert, nur sein Hash."""
    if not isinstance(code, str):
        raise Bad("bad code")
    c = code.upper().replace("-", "").replace(" ", "").replace("O", "0").replace("I", "1").replace("L", "1")
    if c.startswith("CAPY"):
        c = c[4:]
    if not CODE_RE.fullmatch(c):
        raise Bad("bad code")
    return hashlib.sha256(("capy-save:" + c).encode()).hexdigest()

_URLQ = re.compile(r"(https?://[^\s?#]*)[?#]\S*")
def clean_text(v, maxlen):
    """Fehlertext ohne URL-Parameter, ohne Steuerzeichen, gekürzt."""
    if not isinstance(v, str):
        return ""
    v = _URLQ.sub(r"\1", v)
    v = re.sub(r"[\x00-\x1f\x7f]+", " ", v).strip()
    return v[:maxlen]

# ---------- validation ----------
class Bad(Exception):
    pass

def callsign(v):
    if not isinstance(v, str):
        raise Bad("callsign must be a string")
    s = re.sub(r"\s+", " ", v).strip()
    if not 2 <= len(s) <= 16:
        raise Bad("callsign must be 2-16 characters")
    for ch in s:
        if not (ch.isalpha() or ch in "0123456789 -_"):
            raise Bad("callsign may contain letters, digits, space, - and _ only")
    why = csfilter.check(s)
    if why:
        raise Bad("callsign_rejected:" + why)
    return s

PID_RE = re.compile(r"^[A-Za-z0-9_-]{8,64}$")
def pid(v):
    if v is None or v == "":
        return None
    if not isinstance(v, str) or not PID_RE.match(v):
        raise Bad("pid must be 8-64 chars [A-Za-z0-9_-]")
    return v

def integer(v, name, lo, hi, default=None):
    if v is None:
        if default is not None:
            return default
        raise Bad(f"{name} is required")
    if isinstance(v, bool) or not isinstance(v, (int, float)) or v != v:
        raise Bad(f"{name} must be a number")
    v = int(v)
    if not lo <= v <= hi:
        raise Bad(f"{name} must be between {lo} and {hi}")
    return v

def short_str(v, name, allowed=None, maxlen=24, default=None):
    if v is None:
        return default
    if not isinstance(v, str):
        raise Bad(f"{name} must be a string")
    v = v.strip()[:maxlen]
    if allowed is not None and v not in allowed:
        raise Bad(f"{name} must be one of {', '.join(allowed)}")
    if allowed is None and not re.match(r"^[A-Za-z0-9._ -]*$", v):
        raise Bad(f"{name} has invalid characters")
    return v

def clamp_limit(qs, default=50, hi=100):
    try:
        return max(1, min(hi, int(qs.get("limit", [default])[0])))
    except ValueError:
        return default

# ---------- rate limit (memory only) ----------
_rl_lock = threading.Lock()
_rl = {}  # key -> list of timestamps
_salt = {"day": None, "salt": b""}

def rl_key(ip, kind):
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    with _rl_lock:
        if _salt["day"] != day:
            _salt["day"], _salt["salt"] = day, secrets.token_bytes(32)
            _rl.clear()
        return kind + hashlib.sha256(_salt["salt"] + ip.encode()).hexdigest()[:32]

def rate_ok(ip, kind, limit):
    k = rl_key(ip, kind)
    now = time.monotonic()
    with _rl_lock:
        ts = [t for t in _rl.get(k, []) if now - t < 60]
        if len(ts) >= limit:
            _rl[k] = ts
            return False
        ts.append(now)
        _rl[k] = ts
        if len(_rl) > 50000:  # crude memory cap
            _rl.clear()
        return True

# ---------- queries ----------
def top_scores(c, mode, limit):
    rows = c.execute("SELECT callsign, score, wave, t FROM scores WHERE mode=? "
                     "ORDER BY score DESC, wave DESC, t ASC LIMIT ?", (mode, limit)).fetchall()
    return [{"name": r["callsign"], "score": r["score"], "wave": r["wave"], "t": r["t"]} for r in rows]

def top_nuts(c, cont, limit):
    rows = c.execute("SELECT callsign, level, t FROM nuts WHERE continent=? "
                     "ORDER BY level DESC, t ASC LIMIT ?", (cont, limit)).fetchall()
    return [{"name": r["callsign"], "level": r["level"], "t": r["t"]} for r in rows]

def now_ms():
    return int(time.time() * 1000)

# ---------- handler ----------
class H(BaseHTTPRequestHandler):
    server_version = "capy-api"
    sys_version = ""
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # no IPs in logs
        pass

    def client_ip(self):
        xff = self.headers.get("X-Forwarded-For", "")
        return (xff.split(",")[-1].strip() if xff else self.client_address[0]) or "?"

    def send_json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Max-Age", "86400")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_json(200, {})

    def route(self):
        u = urlparse(self.path)
        p = u.path.rstrip("/")
        if p.startswith("/api"):
            p = p[4:] or "/"
        return p, parse_qs(u.query)

    def read_body(self):
        """Always consume the body (keeps the keep-alive connection with Caddy clean)."""
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            n = -1
        if n < 0 or n > 65536:
            self.close_connection = True
            return None, n
        return (self.rfile.read(n) if n else b""), n

    def parse_json(self, raw, n, limit=MAX_BODY):
        if n > limit:
            raise OverflowError
        if not raw:
            raise Bad("JSON body required")
        ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        if ctype not in ("application/json", "text/plain", ""):
            raise Bad("Content-Type must be application/json")
        try:
            d = json.loads(raw.decode("utf-8"))
        except Exception:
            raise Bad("invalid JSON")
        if not isinstance(d, dict):
            raise Bad("JSON object expected")
        return d

    def do_GET(self):
        try:
            if not rate_ok(self.client_ip(), "g", GET_PER_MIN):
                return self.send_json(429, {"error": "too many requests"})
            p, qs = self.route()
            if p == "/health":
                return self.send_json(200, {"ok": True, "service": "capy-api", "version": VERSION, "time": now_ms()})
            if p == "/scores":
                mode = short_str(qs.get("mode", ["pro"])[0], "mode", MODES)
                with db() as c:
                    return self.send_json(200, {"mode": mode, "list": top_scores(c, mode, clamp_limit(qs))})
            if p == "/nuts":
                lim = clamp_limit(qs)
                with db() as c:
                    if "continent" in qs:
                        cont = integer(int(qs["continent"][0]) if qs["continent"][0].isdigit() else -1, "continent", 1, 4)
                        return self.send_json(200, {"continent": cont, "list": top_nuts(c, cont, lim)})
                    return self.send_json(200, {"continents": {str(k): top_nuts(c, k, lim) for k in (1, 2, 3, 4)}})
            if p == "/callsign":
                try:
                    callsign(qs.get("name", [""])[0]); return self.send_json(200, {"ok": True})
                except Bad as e:
                    return self.send_json(200, {"ok": False, "why": str(e).replace("callsign_rejected:", "")})
            if p == "/runs/summary":
                return self.send_json(200, self.summary(qs))
            if p == "/events/summary":
                return self.send_json(200, self.event_summary(qs))
            if p == "/squad":
                c0 = squad_code(qs.get("code", [""])[0])
                with db() as c:
                    r = c.execute("SELECT n FROM squads WHERE code=?", (c0,)).fetchone()
                if not r:
                    return self.send_json(404, {"error": "unknown code"})
                return self.send_json(200, {"ok": True, "n": r["n"]})
            if p == "/pin":   # einmalig von HQ hinterlegter Spielstand (Reparatur), wird nach Abruf gelöscht
                if not rate_ok(self.client_ip(), "r", SAVE_READS_PER_MIN):
                    return self.send_json(429, {"error": "too many requests"})
                k = save_key(qs.get("code", [""])[0])
                with db() as c:
                    r = c.execute("SELECT v FROM kv WHERE k=?", ("pin:" + k,)).fetchone()
                    if r: c.execute("DELETE FROM kv WHERE k=?", ("pin:" + k,))
                if not r:
                    return self.send_json(404, {"error": "none"})
                return self.send_json(200, {"ok": True, "data": json.loads(r["v"])})
            if p == "/save":
                if not rate_ok(self.client_ip(), "r", SAVE_READS_PER_MIN):
                    return self.send_json(429, {"error": "too many requests"})
                k = save_key(qs.get("code", [""])[0])
                with db() as c:
                    r = c.execute("SELECT t, ver, wave, data FROM saves WHERE k=? ORDER BY t DESC, id DESC LIMIT 1", (k,)).fetchone()
                if not r:
                    return self.send_json(404, {"error": "unknown code"})
                return self.send_json(200, {"ok": True, "t": r["t"], "ver": r["ver"], "wave": r["wave"], "data": json.loads(r["data"])})
            return self.send_json(404, {"error": "not found"})
        except Bad as e:
            return self.send_json(400, {"error": str(e)})
        except Exception:
            return self.send_json(500, {"error": "server error"})

    def summary(self, qs):
        where, args = ("WHERE 1=1" if qs.get("dev", ["0"])[0] == "1" else "WHERE dev=0"), []
        if "mode" in qs:
            where += " AND mode=?"
            args.append(short_str(qs["mode"][0], "mode", MODES))
        with db() as c:
            total = c.execute(f"SELECT COUNT(*) n, AVG(wave) w, AVG(gold) g, AVG(mins) m FROM runs {where}", args).fetchone()
            by_wave = {str(r["wave"]): r["n"] for r in c.execute(
                f"SELECT wave, COUNT(*) n FROM runs {where} GROUP BY wave ORDER BY wave", args)}
            by_why = {r["why"] or "?": r["n"] for r in c.execute(
                f"SELECT why, COUNT(*) n FROM runs {where} GROUP BY why", args)}
            by_mode = {r["mode"] or "?": r["n"] for r in c.execute(
                f"SELECT mode, COUNT(*) n FROM runs {where} GROUP BY mode", args)}
            by_wave_why = {}
            for r in c.execute(f"SELECT wave, why, COUNT(*) n, AVG(gold) g FROM runs {where} GROUP BY wave, why", args):
                by_wave_why.setdefault(str(r["wave"]), {})[r["why"] or "?"] = {"n": r["n"], "avgGold": round(r["g"] or 0)}
        return {"runs": total["n"], "avgWave": round(total["w"] or 0, 2), "avgGold": round(total["g"] or 0),
                "avgMins": round(total["m"] or 0, 2), "byWave": by_wave, "byDeathCause": by_why,
                "byMode": by_mode, "byWaveAndCause": by_wave_why}

    def event_summary(self, qs):
        try:
            days = max(1, min(EVENT_RETENTION_DAYS, int(qs.get("days", ["7"])[0])))
        except ValueError:
            days = 7
        where, args = "WHERE t >= ?", [now_ms() - days * 86400 * 1000]
        if qs.get("dev", ["0"])[0] != "1":
            where += " AND dev=0"
        if "ver" in qs:
            where += " AND ver=?"; args.append(short_str(qs["ver"][0], "ver", None, 24))
        with db() as c:
            kinds = {r["kind"]: r["n"] for r in c.execute(f"SELECT kind, COUNT(*) n FROM events {where} GROUP BY kind", args)}
            sess = c.execute(f"SELECT COUNT(DISTINCT sess) n FROM events {where}", args).fetchone()["n"]
            errs = [{"msg": r["msg"], "src": r["src"], "n": r["n"], "sessions": r["s"], "lastVer": r["v"], "maxWave": r["w"], "last": r["lt"]}
                    for r in c.execute(f"SELECT msg, src, COUNT(*) n, COUNT(DISTINCT sess) s, MAX(ver) v, MAX(wave) w, MAX(t) lt FROM events {where} AND kind='error' "
                                       "GROUP BY msg, src ORDER BY s DESC, n DESC LIMIT 40", args)]
            leaves = {}
            for r in c.execute(f"SELECT wave, scr, COUNT(*) n FROM events {where} AND kind='leave' GROUP BY wave, scr ORDER BY wave", args):
                leaves.setdefault(str(r["wave"]), {})[r["scr"] or "?"] = r["n"]
            devices = [{"plat": r["plat"], "br": r["br"], "sessions": r["n"], "errors": r["e"]}
                       for r in c.execute(f"SELECT plat, br, COUNT(DISTINCT sess) n, SUM(kind='error') e FROM events {where} GROUP BY plat, br ORDER BY n DESC LIMIT 30", args)]
        return {"days": days, "sessions": sess, "byKind": kinds, "topErrors": errs, "leaveByWaveAndScreen": leaves, "devices": devices}

    def post_events(self, d):
        ev = d.get("ev")
        if not isinstance(ev, list) or not ev:
            raise Bad("ev list required")
        sess = d.get("sess")
        if not (isinstance(sess, str) and re.fullmatch(r"[0-9a-f]{8,16}", sess)):
            raise Bad("bad sess")
        base = (short_str(d.get("ver"), "ver", None, 24, ""), sess,
                1 if d.get("dev") is True else 0,
                clean_text(d.get("plat"), 24), clean_text(d.get("br"), 24),
                integer(d.get("sw"), "sw", 0, 10000, 0), integer(d.get("sh"), "sh", 0, 10000, 0),
                max(0.0, min(64.0, float(d.get("mem")))) if isinstance(d.get("mem"), (int, float)) and not isinstance(d.get("mem"), bool) else None)
        uid = d.get("uid") if isinstance(d.get("uid"), str) and UID_RE.fullmatch(d.get("uid")) else None   # V594
        ext = (uid, clean_text(d.get("ch"), 12) or None, 1 if d.get("team") is True or d.get("team") == 1 else 0)
        t, rows = now_ms(), []
        for e in ev[:12]:
            if not isinstance(e, dict):
                continue
            k = e.get("k")
            if k not in EVENT_KINDS:
                continue
            m = e.get("m")
            mins = max(0.0, min(10000.0, float(m))) if isinstance(m, (int, float)) and not isinstance(m, bool) else None
            dd = clean_profile(e.get("d")) if isinstance(e.get("d"), dict) else None
            dj = json.dumps(dd, separators=(",", ":"))[:400] if dd else None
            rows.append((t, base[0], base[1], k, integer(e.get("w"), "w", 0, MAX_WAVE, 0), clean_text(e.get("scr"), 16),
                         clean_text(e.get("msg"), 200), clean_text(e.get("src"), 80), mins) + base[2:] + ext + (dj,))
        if rows:
            with db() as c:
                c.executemany("INSERT INTO events(t,ver,sess,kind,wave,scr,msg,src,mins,dev,plat,br,sw,sh,mem,uid,ch,team,data) "
                              "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
                try:   # V650: Sitzung mit Gerät und Spielzeit
                    dv = d.get("dv") if isinstance(d.get("dv"), dict) else {}
                    off = dv.get("off"); off = int(off) if isinstance(off, (int, float)) and not isinstance(off, bool) and -900 <= off <= 900 else None
                    secs = 0
                    for e in ev[:12]:
                        if isinstance(e, dict) and e.get("k") == "sess" and isinstance(e.get("d"), dict) and isinstance(e["d"].get("s"), (int, float)):
                            secs = max(secs, min(86400, int(e["d"]["s"])))
                    mw = max([r[4] for r in rows] + [0])
                    c.execute("INSERT INTO plays(sess,uid,first,last,n,secs,maxw,ver,ch,os,osv,model,br,sw,sh,tz,off,lang,team,dev) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
                              "ON CONFLICT(sess) DO UPDATE SET last=excluded.last, n=plays.n+excluded.n, secs=MAX(plays.secs, excluded.secs), maxw=MAX(plays.maxw, excluded.maxw), ver=excluded.ver, "
                              "uid=COALESCE(excluded.uid, plays.uid), os=COALESCE(NULLIF(excluded.os,''), plays.os), osv=COALESCE(NULLIF(excluded.osv,''), plays.osv), "
                              "model=COALESCE(NULLIF(excluded.model,''), plays.model), tz=COALESCE(NULLIF(excluded.tz,''), plays.tz), off=COALESCE(excluded.off, plays.off), "
                              "lang=COALESCE(NULLIF(excluded.lang,''), plays.lang), team=MAX(plays.team, excluded.team), dev=MAX(plays.dev, excluded.dev)",
                              (sess, uid, t, t, len(rows), secs, mw, base[0], ext[1], clean_text(dv.get("os"), 24), clean_text(dv.get("osv"), 24), clean_text(dv.get("model"), 40),
                               base[4], base[5], base[6], clean_text(dv.get("tz"), 40), off, clean_text(dv.get("lang"), 8), ext[2], base[2]))
                except Exception:
                    pass
        return self.send_json(200, {"ok": True, "n": len(rows)})

    def post_save(self, d):
        k = save_key(d.get("code"))
        data = d.get("data")
        if not isinstance(data, dict) or not data or len(data) > 200:
            raise Bad("data object required")
        clean = {}
        for key, val in data.items():
            if not (isinstance(key, str) and SAVE_KEY_RE.fullmatch(key) and isinstance(val, str)):
                raise Bad("bad data entry")
            clean[key] = val
        blob = json.dumps(clean, ensure_ascii=False, separators=(",", ":"))
        if len(blob) > SAVE_MAX_DATA:
            raise Bad("save too large")
        t = now_ms()
        with db() as c:
            c.execute("INSERT INTO saves(k,t,ver,wave,size,data) VALUES(?,?,?,?,?,?)",
                      (k, t, short_str(d.get("ver"), "ver", None, 24, ""), integer(d.get("wave"), "wave", 0, MAX_WAVE, 0), len(blob), blob))
            c.execute("DELETE FROM saves WHERE k=? AND id NOT IN (SELECT id FROM saves WHERE k=? ORDER BY t DESC, id DESC LIMIT ?)", (k, k, SAVE_KEEP))
        return self.send_json(200, {"ok": True, "t": t})

    def do_POST(self):
        try:
            raw, n = self.read_body()
            if raw is None:
                return self.send_json(413, {"error": "body too large"})
            if self.route()[0] == "/save":
                if not rate_ok(self.client_ip(), "s", SAVES_PER_MIN):
                    return self.send_json(429, {"error": "too many requests"})
                return self.post_save(self.parse_json(raw, n, SAVE_MAX_BODY))
            if self.route()[0] == "/player":   # V536: Spielprofil je Gerät
                if not rate_ok(self.client_ip(), "pl", PLAYER_PER_MIN):
                    return self.send_json(429, {"error": "too many requests"})
                d = self.parse_json(raw, n, PLAYER_MAX_BODY)
                uid = d.get("uid")
                if not (isinstance(uid, str) and UID_RE.fullmatch(uid)):
                    raise Bad("bad uid")
                prof = clean_profile({k: v for k, v in d.items() if k not in ("uid", "start")})
                blob = json.dumps(prof, ensure_ascii=False, separators=(",", ":"))
                if len(blob) > PLAYER_MAX_BODY:
                    raise Bad("profile too large")
                t = now_ms(); inc = 1 if d.get("start") is True else 0
                with db() as c:
                    if c.execute("SELECT 1 FROM players WHERE uid=?", (uid,)).fetchone():
                        c.execute("UPDATE players SET last=?, n=n+?, data=? WHERE uid=?", (t, inc, blob, uid))
                    else:
                        c.execute("INSERT INTO players(uid,first,last,n,data) VALUES(?,?,?,?,?)", (uid, t, t, max(1, inc), blob))
                return self.send_json(200, {"ok": True})
            if self.route()[0] == "/tester":   # V707b: Tester-Anmeldung (Trailer-Seite)
                if not rate_ok(self.client_ip(), "te", 3):
                    return self.send_json(429, {"error": "too many requests"})
                d = self.parse_json(raw, n)
                if d.get("web"):   # Honigtopf gegen Bots
                    return self.send_json(200, {"ok": True})
                em = clean_text(d.get("email"), 120).strip()
                if not re.fullmatch(r"[^@\s]{1,64}@[^@\s]{1,80}\.[A-Za-z]{2,24}", em):
                    raise Bad("bad email")
                tg = clean_text(d.get("tg"), 40).strip()
                if tg and not re.fullmatch(r"@?[A-Za-z0-9_]{3,40}|\+?[0-9 ]{6,20}", tg):
                    raise Bad("bad telegram")
                row = (now_ms(), clean_text(d.get("name"), 60), em, tg, clean_text(d.get("msg"), 600),
                       short_str(d.get("lang"), "lang", ("ru", "en"), 4, ""), clean_text(d.get("site"), 40))
                with db() as c:
                    c.execute("INSERT INTO testers(t,name,email,tg,msg,lang,site) VALUES(?,?,?,?,?,?,?)", row)
                return self.send_json(200, {"ok": True})
            if self.route()[0] == "/admin/claim":   # V536: einmalig für Martins Gerät
                if not rate_ok(self.client_ip(), "ad", 6):
                    return self.send_json(429, {"error": "too many requests"})
                d = self.parse_json(raw, n)
                if d.get("uid") not in ADMIN_UIDS:
                    return self.send_json(403, {"error": "forbidden"})
                with db() as c:
                    tok = secrets.token_urlsafe(32)   # V576: je Admin-Gerät ein eigener Schlüssel, jederzeit neu holbar
                    c.execute("INSERT OR REPLACE INTO kv(k,v) VALUES(?,?)", ("admin:hash:" + d.get("uid"), hashlib.sha256(tok.encode()).hexdigest()))
                    c.execute("INSERT OR REPLACE INTO kv(k,v) VALUES('admin:claimed',?)", (str(now_ms()),))
                return self.send_json(200, {"ok": True, "token": tok})
            if self.route()[0] == "/admin/players":   # V536: Spielerliste nur mit Admin-Schlüssel
                if not rate_ok(self.client_ip(), "ad", 30):
                    return self.send_json(429, {"error": "too many requests"})
                d = self.parse_json(raw, n)
                tok = d.get("token")
                with db() as c:
                    hs = [x["v"] for x in c.execute("SELECT v FROM kv WHERE k='admin:hash' OR k LIKE 'admin:hash:%'").fetchall()]
                    th = hashlib.sha256(tok.encode()).hexdigest() if isinstance(tok, str) else ""
                    if not (th and any(hmac.compare_digest(h, th) for h in hs)):
                        return self.send_json(403, {"error": "forbidden"})
                    rows = c.execute("SELECT uid, first, last, n, data FROM players ORDER BY first, uid").fetchall()
                    PL = {}   # V650
                    for y in c.execute("SELECT uid, first, last, secs, maxw, ver, ch, os, osv, model, br, tz, off FROM plays WHERE uid IS NOT NULL ORDER BY first DESC LIMIT 6000"):
                        L = PL.setdefault(y["uid"], [])
                        if len(L) < 40: L.append({k: y[k] for k in y.keys() if k != "uid"})
                lst = []
                for i, x in enumerate(rows):
                    try: dd = json.loads(x["data"])
                    except Exception: dd = {}
                    lst.append({"no": i + 1, "uid": x["uid"], "first": x["first"], "last": x["last"], "n": x["n"], "d": dd, "plays": PL.get(x["uid"], [])})
                return self.send_json(200, {"ok": True, "now": now_ms(), "list": lst})
            if self.route()[0] == "/admin/tgtoken":   # V707c: Telegram-Bot-Token
                if not rate_ok(self.client_ip(), "ad", 10):
                    return self.send_json(429, {"error": "too many requests"})
                d = self.parse_json(raw, n)
                with db() as c:
                    if not admin_ok(c, d.get("token")):
                        return self.send_json(403, {"error": "forbidden"})
                bt = d.get("bot")
                if not (isinstance(bt, str) and re.fullmatch(r"[0-9]{5,15}:[A-Za-z0-9_-]{30,60}", bt.strip())):
                    return self.send_json(400, {"error": "Das sieht nicht wie ein Bot-Token aus."})
                bt = bt.strip()
                try:
                    import urllib.request as _u
                    me = json.loads(_u.urlopen("https://api.telegram.org/bot" + bt + "/getMe", timeout=15).read().decode())
                except Exception:
                    return self.send_json(400, {"error": "Telegram kennt diesen Token nicht."})
                if not me.get("ok"):
                    return self.send_json(400, {"error": "Telegram kennt diesen Token nicht."})
                sd = os.path.join(os.path.dirname(DB), "secret"); os.makedirs(sd, exist_ok=True); os.chmod(sd, 0o700)
                fp = os.path.join(sd, "tg.json"); fd = os.open(fp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
                with os.fdopen(fd, "w") as f: json.dump({"bot": bt, "user": me["result"].get("username")}, f)
                return self.send_json(200, {"ok": True, "user": me["result"].get("username")})
            if self.route()[0] == "/admin/secret":   # V656: Play-Dienstschlüssel speichern
                if not rate_ok(self.client_ip(), "ad", 10):
                    return self.send_json(429, {"error": "too many requests"})
                d = self.parse_json(raw, n, 16000)
                with db() as c:
                    if not admin_ok(c, d.get("token")):
                        return self.send_json(403, {"error": "forbidden"})
                k = d.get("key")
                if not (isinstance(k, dict) and k.get("type") == "service_account" and isinstance(k.get("client_email"), str) and "PRIVATE KEY" in str(k.get("private_key"))):
                    return self.send_json(400, {"error": "Das ist kein Dienstkonto-Schlüssel (JSON)."})
                sd = os.path.join(os.path.dirname(DB), "secret"); os.makedirs(sd, exist_ok=True); os.chmod(sd, 0o700)
                fp = os.path.join(sd, "play-sa.json"); fd = os.open(fp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
                with os.fdopen(fd, "w") as f: json.dump(k, f)
                return self.send_json(200, {"ok": True, "email": k["client_email"], "project": k.get("project_id")})
            if self.route()[0] == "/admin/report":   # V653: Tabelle jetzt bauen / Drive-Auftrag / herunterladen
                if not rate_ok(self.client_ip(), "ad", 30):
                    return self.send_json(429, {"error": "too many requests"})
                d = self.parse_json(raw, n)
                with db() as c:
                    if not admin_ok(c, d.get("token")):
                        return self.send_json(403, {"error": "forbidden"})
                act = d.get("act")
                if act == "refresh":
                    m = build_report(); return self.send_json(200, {"ok": True, "meta": m, "st": report_status()})
                if act == "drive":
                    m = build_report(); os.makedirs(REPORT_DIR, exist_ok=True)
                    json.dump({"req": now_ms(), "msk": _msk(now_ms()), "week": m["week"], "done": None}, open(os.path.join(REPORT_DIR, "drive.json"), "w"))
                    return self.send_json(200, {"ok": True, "meta": m, "st": report_status()})
                if act == "get":
                    wk = d.get("week") if isinstance(d.get("week"), str) and re.fullmatch(r"\d{4}-KW\d{2}", d.get("week") or "") else _week(now_ms())[0]
                    f = "sitzungen.csv" if d.get("f") == "sitzungen" else "spieler.csv"
                    try: txt = open(os.path.join(REPORT_DIR, wk, f), encoding="utf-8-sig").read()
                    except Exception: txt = ""
                    return self.send_json(200, {"ok": True, "week": wk, "file": f, "csv": txt})
                return self.send_json(200, {"ok": True, "st": report_status()})
            if self.route()[0] == "/admin/stats":   # V594: Analyse (nur echte Spieler)
                if not rate_ok(self.client_ip(), "ad", 30):
                    return self.send_json(429, {"error": "too many requests"})
                d = self.parse_json(raw, n)
                tok = d.get("token")
                with db() as c:
                    hs = [x["v"] for x in c.execute("SELECT v FROM kv WHERE k='admin:hash' OR k LIKE 'admin:hash:%'").fetchall()]
                    th = hashlib.sha256(tok.encode()).hexdigest() if isinstance(tok, str) else ""
                    if not (th and any(hmac.compare_digest(h, th) for h in hs)):
                        return self.send_json(403, {"error": "forbidden"})
                    try: days = max(1, min(EVENT_RETENTION_DAYS, int(d.get("days") or 30)))
                    except Exception: days = 30
                    return self.send_json(200, admin_stats(c, days))
            if self.route()[0] == "/feedback":   # V647: Bewertung 1–5 Sterne + Nachricht
                if not rate_ok(self.client_ip(), "fb", 6):
                    return self.send_json(429, {"error": "too many requests"})
                d = self.parse_json(raw, n, 8000)
                stars = d.get("stars")
                stars = stars if isinstance(stars, int) and not isinstance(stars, bool) and 1 <= stars <= 5 else None
                msg = d.get("msg") if isinstance(d.get("msg"), str) else ""
                msg = _URLQ.sub(r"\1", msg); msg = re.sub(r"[\x00-\x09\x0b-\x1f\x7f]+", " ", msg).strip()[:1000]
                if not stars and not msg:
                    raise Bad("empty")
                uid = d.get("uid") if isinstance(d.get("uid"), str) and UID_RE.fullmatch(d.get("uid")) else None
                with db() as c:
                    c.execute("INSERT INTO feedback(t,uid,ver,ch,lang,src,wave,stars,msg,plat) VALUES(?,?,?,?,?,?,?,?,?,?)",
                              (now_ms(), uid, short_str(d.get("ver"), "ver", None, 24, ""), clean_text(d.get("ch"), 12) or None,
                               clean_text(d.get("lang"), 5) or None, clean_text(d.get("src"), 12) or None,
                               integer(d.get("w"), "w", 0, MAX_WAVE, 0), stars, msg or None, clean_text(d.get("plat"), 24) or None))
                return self.send_json(200, {"ok": True})
            if self.route()[0] == "/events":
                if not rate_ok(self.client_ip(), "e", EVENTS_PER_MIN):
                    return self.send_json(429, {"error": "too many requests"})
                return self.post_events(self.parse_json(raw, n, EVENT_MAX_BODY))
            if not rate_ok(self.client_ip(), "p", POST_PER_MIN):
                return self.send_json(429, {"error": "too many requests, max %d per minute" % POST_PER_MIN})
            p, _ = self.route()
            d = self.parse_json(raw, n)
            if p == "/scores":
                return self.post_score(d)
            if p == "/runs":
                return self.post_run(d)
            if p == "/nuts":
                return self.post_nuts(d)
            if p == "/squad":
                with db() as c:
                    for _ in range(8):
                        code = "".join(secrets.choice(SQUAD_ABC) for _ in range(6))
                        if not c.execute("SELECT 1 FROM squads WHERE code=?", (code,)).fetchone():
                            c.execute("INSERT INTO squads(code,t,n) VALUES(?,?,0)", (code, now_ms()))
                            return self.send_json(200, {"ok": True, "code": code})
                return self.send_json(500, {"error": "server error"})
            if p == "/squad/join":
                code = squad_code(d.get("code"))
                ip = self.client_ip()
                with db() as c:
                    row = c.execute("SELECT n, last FROM squads WHERE code=?", (code,)).fetchone()
                    if not row:
                        return self.send_json(404, {"error": "unknown code"})
                    now = now_ms()
                    sr = c.execute("SELECT v FROM kv WHERE k='squad_salt'").fetchone()
                    if sr:
                        salt = sr["v"]
                    else:
                        salt = secrets.token_hex(32)
                        c.execute("INSERT OR IGNORE INTO kv(k, v) VALUES('squad_salt', ?)", (salt,))
                    h = hashlib.sha256((salt + code + ip).encode()).hexdigest()
                    j = c.execute("SELECT t FROM squad_joins WHERE h=?", (h,)).fetchone()
                    if j and now - j["t"] < 86400000:
                        return self.send_json(200, {"ok": True, "counted": False})
                    if row["last"] and now - row["last"] < 60000:
                        return self.send_json(200, {"ok": True, "counted": False})
                    c.execute("INSERT OR REPLACE INTO squad_joins(h, t) VALUES(?, ?)", (h, now))
                    c.execute("DELETE FROM squad_joins WHERE t < ?", (now - 3 * 86400000,))
                    c.execute("UPDATE squads SET n=MIN(n+1,?), last=? WHERE code=?", (SQUAD_MAX_N, now, code))
                return self.send_json(200, {"ok": True, "counted": True})
            return self.send_json(404, {"error": "not found"})
        except OverflowError:
            return self.send_json(413, {"error": "body too large"})
        except Bad as e:
            return self.send_json(400, {"error": str(e)})
        except Exception:
            return self.send_json(500, {"error": "server error"})

    def post_score(self, d):
        mode = short_str(d.get("mode", "pro"), "mode", MODES)
        name = callsign(d.get("callsign", d.get("name")))
        score = integer(d.get("score"), "score", 0, MAX_SCORE)
        wave = integer(d.get("wave"), "wave", 0, MAX_WAVE)
        lines = integer(d.get("lines"), "lines", 0, 10_000_000, 0)
        kills = integer(d.get("kills"), "kills", 0, 10_000_000, 0)
        if score > (wave + 1) * 2_000_000:
            raise Bad("score not plausible for this wave")
        pl = pid(d.get("pid"))
        t = now_ms()
        with db() as c:
            if pl:
                cur = c.execute("SELECT id, score, t FROM scores WHERE mode=? AND pid=?", (mode, pl)).fetchone()
                if cur and cur["score"] >= score:
                    c.execute("UPDATE scores SET callsign=? WHERE id=?", (name, cur["id"]))
                    t, improved = cur["t"], False
                elif cur:
                    c.execute("UPDATE scores SET callsign=?, score=?, wave=?, lines=?, kills=?, t=? WHERE id=?",
                              (name, score, wave, lines, kills, t, cur["id"]))
                    improved = True
                else:
                    c.execute("INSERT INTO scores(mode,pid,callsign,score,wave,lines,kills,t) VALUES(?,?,?,?,?,?,?,?)",
                              (mode, pl, name, score, wave, lines, kills, t))
                    improved = True
            else:
                c.execute("INSERT INTO scores(mode,pid,callsign,score,wave,lines,kills,t) VALUES(?,?,?,?,?,?,?,?)",
                          (mode, None, name, score, wave, lines, kills, t))
                improved = True
            best = c.execute("SELECT score, wave FROM scores WHERE mode=? AND t=? AND callsign=? LIMIT 1",
                             (mode, t, name)).fetchone()
            bs, bw = (best["score"], best["wave"]) if best else (score, wave)
            rank = c.execute("SELECT COUNT(*) FROM scores WHERE mode=? AND (score>? OR (score=? AND wave>?))",
                             (mode, bs, bs, bw)).fetchone()[0] + 1
            lst = top_scores(c, mode, 50)
        return self.send_json(200, {"ok": True, "mode": mode, "improved": improved, "rank": rank, "t": t, "list": lst})

    def post_run(self, d):
        row = (
            now_ms(),
            short_str(d.get("ver"), "ver", None, 24, ""),
            short_str(d.get("mode", "pro"), "mode", MODES),
            integer(d.get("wave"), "wave", 0, MAX_WAVE),
            short_str(d.get("why", "?"), "why", ("monsters", "blocks", "quit", "win", "?")),
            integer(d.get("gold"), "gold", 0, 100_000_000, 0),
            integer(d.get("lines"), "lines", 0, 10_000_000, 0),
            integer(d.get("splats"), "splats", 0, 10_000_000, 0),
            integer(d.get("score"), "score", 0, MAX_SCORE, 0),
            integer(d.get("medals"), "medals", 0, 100_000, 0),
            integer(d.get("maxSpeed"), "maxSpeed", 0, 16, 1),
            max(0.0, min(10000.0, float(d.get("mins") or 0))) if isinstance(d.get("mins"), (int, float, type(None))) and not isinstance(d.get("mins"), bool) else 0.0,
            short_str(d.get("hero"), "hero", None, 16, ""),
            1 if d.get("dev") is True else 0,
        )
        with db() as c:
            c.execute("INSERT INTO runs(t,ver,mode,wave,why,gold,lines,splats,score,medals,max_speed,mins,hero,dev) "
                      "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row)
        return self.send_json(200, {"ok": True})

    def post_nuts(self, d):
        name = callsign(d.get("callsign", d.get("name")))
        cont = integer(d.get("continent"), "continent", 1, 4)
        level = integer(d.get("level"), "level", 1, MAX_LEVEL)
        pl = pid(d.get("pid"))
        t = now_ms()
        with db() as c:
            cur = c.execute("SELECT id, level, t FROM nuts WHERE continent=? AND pid=?", (cont, pl)).fetchone() if pl else None
            if cur and cur["level"] >= level:
                c.execute("UPDATE nuts SET callsign=? WHERE id=?", (name, cur["id"]))
                level, t, improved = cur["level"], cur["t"], False
            elif cur:
                c.execute("UPDATE nuts SET callsign=?, level=?, t=? WHERE id=?", (name, level, t, cur["id"]))
                improved = True
            else:
                c.execute("INSERT INTO nuts(pid,callsign,continent,level,t) VALUES(?,?,?,?,?)", (pl, name, cont, level, t))
                improved = True
            rank = c.execute("SELECT COUNT(*) FROM nuts WHERE continent=? AND level>?", (cont, level)).fetchone()[0] + 1
            lst = top_nuts(c, cont, 50)
        return self.send_json(200, {"ok": True, "continent": cont, "improved": improved, "rank": rank, "t": t, "list": lst})


def squad_code(v):
    if not isinstance(v, str):
        raise Bad("bad code")
    c = v.strip().upper()
    if not SQUAD_RE.fullmatch(c):
        raise Bad("bad code")
    return c

def purge_old_entries():
    cutoff = int(time.time() * 1000) - 730 * 86400 * 1000   # 24 Monate ohne neues Ergebnis
    with db() as c:
        c.execute("DELETE FROM scores WHERE t < ?", (cutoff,))
        c.execute("DELETE FROM nuts WHERE t < ?", (cutoff,))
        c.execute("DELETE FROM players WHERE last < ?", (int(time.time() * 1000) - PLAYER_RETENTION_DAYS * 86400 * 1000,))
        c.execute("DELETE FROM plays WHERE last < ?", (int(time.time() * 1000) - PLAYER_RETENTION_DAYS * 86400 * 1000,))

# ---------- V653: Spieler-Tabelle je Woche ----------
import csv, io
REPORT_DIR = os.environ.get("CAPY_REPORTS", os.path.join(os.path.dirname(DB), "reports"))
MSK = 3 * 3600 * 1000
_rep_lock = threading.Lock()

def _msk(t):
    return time.strftime("%d.%m.%Y %H:%M", time.gmtime((t + MSK) / 1000)) if t else ""

def _week(now):
    d = datetime.fromtimestamp((now + MSK) / 1000, tz=timezone.utc)
    y, w, wd = d.isocalendar()
    start = int(datetime(d.year, d.month, d.day, tzinfo=timezone.utc).timestamp() * 1000) - (wd - 1) * 86400000 - MSK
    return f"{y}-KW{w:02d}", start

def build_report():
    with _rep_lock:
        now = now_ms(); wk, ws = _week(now)
        out = os.path.join(REPORT_DIR, wk); os.makedirs(out, exist_ok=True)
        with db() as c:
            P = c.execute("SELECT uid, first, last, n, data FROM players ORDER BY first, uid").fetchall()
            plays = c.execute("SELECT * FROM plays WHERE first >= ? ORDER BY first", (ws,)).fetchall()
            ev = c.execute("SELECT uid, kind, wave, data FROM events WHERE t >= ? AND uid IS NOT NULL", (ws,)).fetchall()
            fb = c.execute("SELECT t, uid, stars, msg FROM feedback WHERE t >= ? ORDER BY t", (ws,)).fetchall()
            ALLS = {r[0]: r[1] or 0 for r in c.execute("SELECT uid, SUM(COALESCE(secs, (last - first) / 1000)) FROM plays WHERE uid IS NOT NULL GROUP BY uid")}   # V724: Spielzeit gesamt aus allen Sitzungen
            TUTN = {}
            for r in c.execute("SELECT uid, data FROM events WHERE kind = 'tut' AND uid IS NOT NULL"):
                try: TUTN[r[0]] = max(TUTN.get(r[0], 0), int(json.loads(r[1] or "{}").get("n") or 0))
                except Exception: pass
        W = {}
        for r in plays:
            if not r["uid"]: continue
            a = W.setdefault(r["uid"], {"s": 0, "sec": 0, "mw": 0, "dev": ""})
            a["s"] += 1; a["sec"] += r["secs"] or max(0, (r["last"] - r["first"]) // 1000); a["mw"] = max(a["mw"], r["maxw"] or 0)
            a["dev"] = " ".join(x for x in (r["os"], r["osv"], r["model"]) if x) or a["dev"]; a["ch"] = r["ch"] or a.get("ch", "")
        E = {}
        for r in ev:
            k = r["kind"]; a = E.setdefault(r["uid"], {})
            try: x = json.loads(r["data"]) if r["data"] else {}
            except Exception: x = {}
            key = k
            if k == "thief": key = "thief_" + str(x.get("a") or "?")
            if k == "poll": key = "poll_" + {1: "up", 0: "mid", -1: "down"}.get(x.get("v"), "skip")
            a[key] = a.get(key, 0) + 1
            if k == "thief" and x.get("a") == "steal": a["thief_gold"] = a.get("thief_gold", 0) + int(x.get("g") or 0)
        F = {}
        for r in fb: F[r["uid"]] = r
        cols = ["Nr", "Spieler-Nr", "Name", "Team/Test", "Kanal", "Sprache", "Gerät (letzte Woche)", "System (Profil)", "App/Browser", "Bildschirm", "Zeitzone", "Version",
                "Erster Kontakt (MSK)", "Zuletzt (MSK)", "App-Starts gesamt", "Sitzungen Woche", "Spielzeit Woche (min)", "Spielzeit gesamt (min)", "Beste Welle", "Gerade",
                "Checkpoint", "Tutorial", "Tode gesamt", "Todesursachen", "Wellen gespielt Woche", "Tode Woche", "Knapp am Ende Woche", "Untätig 45s Woche", "Verlassen Woche",
                "Käufe Woche", "Werbung Woche", "Boss-Hack Woche", "Fehler Woche", "Umfrage 👍/😐/👎", "Dieb kam/stahl/Wolf/entkommen", "Dieb Gold gestohlen Woche",
                "Sterne-Bewertung", "Nachricht"]
        bad = set(ADMIN_UIDS)
        robots = set()
        for r in P:
            try:
                if is_bot_profile(json.loads(r["data"])): robots.add(r["uid"])
            except Exception: pass
        P = [r for r in P if r["uid"] not in robots]   # V708b: Roboter/Testgeräte nicht in der Tabelle
        plays = [r for r in plays if r["uid"] not in robots]
        buf = io.StringIO(); w = csv.writer(buf); w.writerow(cols)
        for i, r in enumerate(P):
            try: d = json.loads(r["data"])
            except Exception: d = {}
            uid = r["uid"]; a = W.get(uid, {}); e = E.get(uid, {}); f = F.get(uid)
            team = "ja" if (uid in bad or d.get("team") or d.get("dev")) else ""
            cur = d.get("cur") or {}
            cur_s = (f"Nuts {cur.get('c')} L{cur.get('lv')}" if cur.get("nz") else f"Welle {cur.get('w')}") if cur else ""
            by = d.get("dby") or {}
            w.writerow([i + 1, uid, d.get("nm") or "", team, a.get("ch", ""), d.get("lang") or "", a.get("dev", ""), d.get("os") or "", d.get("app") or "", d.get("scr") or "", d.get("tz") or "", d.get("ver") or "",
                        _msk(r["first"]), _msk(r["last"]), r["n"], a.get("s", 0), round(a.get("sec", 0) / 60), round(max(d.get("t") or 0, ALLS.get(uid, 0)) / 60), d.get("bw") or 0, cur_s,
                        d.get("cp") or 0, "ja" if d.get("tut") else (f"nein (bis Schritt {TUTN[uid]}/10)" if TUTN.get(uid) else "nein"), d.get("d") or 0, " ".join(f"{k}:{v}" for k, v in by.items()), e.get("wend", 0), e.get("death", 0), e.get("near", 0), e.get("idle", 0), e.get("quit", 0),
                        e.get("buy", 0), e.get("ad", 0), e.get("hack", 0), e.get("error", 0), f"{e.get('poll_up', 0)}/{e.get('poll_mid', 0)}/{e.get('poll_down', 0)}",
                        f"{e.get('thief_come', 0)}/{e.get('thief_steal', 0)}/{e.get('thief_wolf', 0)}/{e.get('thief_gone', 0)}", e.get("thief_gold", 0),
                        (f["stars"] or "") if f else "", (f["msg"] or "") if f else ""])
        open(os.path.join(out, "spieler.csv"), "w", encoding="utf-8-sig", newline="").write(buf.getvalue())
        buf = io.StringIO(); w = csv.writer(buf)
        w.writerow(["Start (MSK)", "Ende (MSK)", "Ortszeit Start", "Spieler-Nr", "Minuten", "bis Welle", "System", "Version System", "Modell", "Browser/App", "Bildschirm", "Zeitzone", "Kanal", "Spiel-Version", "Team/Test"])
        for r in plays:
            lt = time.strftime("%a %d.%m. %H:%M", time.gmtime((r["first"] + (r["off"] or 0) * 60000) / 1000)) if r["off"] is not None else ""
            w.writerow([_msk(r["first"]), _msk(r["last"]), lt, r["uid"] or "", round((r["secs"] or max(0, (r["last"] - r["first"]) // 1000)) / 60, 1), r["maxw"], r["os"] or "", r["osv"] or "", r["model"] or "",
                        r["br"] or "", f"{r['sw']}×{r['sh']}" if r["sw"] else "", r["tz"] or "", r["ch"] or "", r["ver"] or "", "ja" if (r["team"] or r["dev"] or r["uid"] in bad) else ""])
        open(os.path.join(out, "sitzungen.csv"), "w", encoding="utf-8-sig", newline="").write(buf.getvalue())
        meta = {"t": now, "msk": _msk(now), "week": wk, "players": len(P), "plays": len(plays)}
        json.dump(meta, open(os.path.join(REPORT_DIR, "last.json"), "w"))
        return meta

def report_status():
    st = {}
    try: st["last"] = json.load(open(os.path.join(REPORT_DIR, "last.json")))
    except Exception: st["last"] = None
    try: st["drive"] = json.load(open(os.path.join(REPORT_DIR, "drive.json")))
    except Exception: st["drive"] = None
    try: st["weeks"] = sorted([x for x in os.listdir(REPORT_DIR) if "-KW" in x], reverse=True)[:20]
    except Exception: st["weeks"] = []
    return st

def reporter():
    time.sleep(60)
    while True:
        try: build_report()
        except Exception as e:
            try: open(os.path.join(REPORT_DIR, "error.txt"), "w").write(str(e))
            except Exception: pass
        time.sleep(3600)

def admin_ok(c, tok):
    hs = [x["v"] for x in c.execute("SELECT v FROM kv WHERE k='admin:hash' OR k LIKE 'admin:hash:%'").fetchall()]
    th = hashlib.sha256(tok.encode()).hexdigest() if isinstance(tok, str) else ""
    return bool(th and any(hmac.compare_digest(h, th) for h in hs))

def janitor():
    while True:
        try:
            purge_old_runs()
            purge_old_entries()
        except Exception:
            pass
        time.sleep(6 * 3600)


if __name__ == "__main__":
    init_db()
    threading.Thread(target=janitor, daemon=True).start()
    threading.Thread(target=reporter, daemon=True).start()   # V653
    srv = ThreadingHTTPServer((HOST, PORT), H)
    srv.daemon_threads = True
    srv.serve_forever()
