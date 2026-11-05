#!/usr/bin/env python3
"""Capybara Squad API - high scores, nuts board, anonymous round stats, anonymous error/event log.
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
VERSION = "1.1"
EVENT_RETENTION_DAYS = 90
EVENT_MAX_BODY = 8192
EVENTS_PER_MIN = 20
EVENT_KINDS = ("start", "error", "leave", "back", "wave")

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
"""

def db():
    c = sqlite3.connect(DB, timeout=10)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with db() as c:
        c.executescript(SCHEMA)

def purge_old_runs():
    cutoff = int(time.time() * 1000) - RUN_RETENTION_DAYS * 86400 * 1000
    ecut = int(time.time() * 1000) - EVENT_RETENTION_DAYS * 86400 * 1000
    with db() as c:
        c.execute("DELETE FROM runs WHERE t < ?", (cutoff,))
        c.execute("DELETE FROM events WHERE t < ?", (ecut,))

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
        t, rows = now_ms(), []
        for e in ev[:12]:
            if not isinstance(e, dict):
                continue
            k = e.get("k")
            if k not in EVENT_KINDS:
                continue
            m = e.get("m")
            mins = max(0.0, min(10000.0, float(m))) if isinstance(m, (int, float)) and not isinstance(m, bool) else None
            rows.append((t, base[0], base[1], k, integer(e.get("w"), "w", 0, MAX_WAVE, 0), clean_text(e.get("scr"), 16),
                         clean_text(e.get("msg"), 200), clean_text(e.get("src"), 80), mins) + base[2:])
        if rows:
            with db() as c:
                c.executemany("INSERT INTO events(t,ver,sess,kind,wave,scr,msg,src,mins,dev,plat,br,sw,sh,mem) "
                              "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
        return self.send_json(200, {"ok": True, "n": len(rows)})

    def do_POST(self):
        try:
            raw, n = self.read_body()
            if raw is None:
                return self.send_json(413, {"error": "body too large"})
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


def purge_old_entries():
    cutoff = int(time.time() * 1000) - 730 * 86400 * 1000   # 24 Monate ohne neues Ergebnis
    with db() as c:
        c.execute("DELETE FROM scores WHERE t < ?", (cutoff,))
        c.execute("DELETE FROM nuts WHERE t < ?", (cutoff,))

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
    srv = ThreadingHTTPServer((HOST, PORT), H)
    srv.daemon_threads = True
    srv.serve_forever()
