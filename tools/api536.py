#!/usr/bin/env python3
"""V536 (Martin 09.11. 21:17): Admin-Übersicht der Spieler.
- Tabelle players(uid, first, last, n, data): jedes Gerät meldet sein Spielprofil (capy-uid, Rufzeichen, Gerät,
  Fortschritt, Spielzeit, Tode …) über POST /api/player. Keine IP, kein Klarname außer dem selbst gewählten Rufzeichen.
- POST /api/admin/claim {uid}: einmalig für Martins Gerät (uid M2HL-KCQH) – erzeugt den Admin-Schlüssel,
  speichert nur seinen Hash (kv admin:hash), danach gesperrt (kv admin:claimed). Zurücksetzen: beide kv-Zeilen löschen.
- POST /api/admin/players {token}: Liste aller Spieler mit laufender Nummer (Reihenfolge erster Kontakt).
Aufruf: python3 tools/api536.py /srv/capy-api/app.py"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)

rep('CREATE TABLE IF NOT EXISTS kv(k TEXT PRIMARY KEY, v TEXT NOT NULL);\n',
    'CREATE TABLE IF NOT EXISTS kv(k TEXT PRIMARY KEY, v TEXT NOT NULL);\n'
    'CREATE TABLE IF NOT EXISTS players(uid TEXT PRIMARY KEY, first INTEGER NOT NULL, last INTEGER NOT NULL, n INTEGER NOT NULL DEFAULT 0, data TEXT NOT NULL);\n'
    'CREATE INDEX IF NOT EXISTS players_first ON players(first);\n')

rep('EVENT_KINDS = ("start", "error", "leave", "back", "wave")\n',
    'EVENT_KINDS = ("start", "error", "leave", "back", "wave")\n'
    'UID_RE = re.compile(r"[A-Z0-9]{4}-[A-Z0-9]{4}")\n'
    'ADMIN_UID = "M2HL-KCQH"\n'
    'PLAYER_PER_MIN = 8\n'
    'PLAYER_MAX_BODY = 6000\n'
    'PLAYER_RETENTION_DAYS = 730\n'
    'import hmac\n'
    'def clean_profile(v, depth=0):\n'
    '    """Nur einfache Werte: Zahlen, kurze Texte, kleine Listen/Objekte (max. 2 Ebenen)."""\n'
    '    if isinstance(v, bool): return v\n'
    '    if isinstance(v, (int, float)):\n'
    '        return max(-1e12, min(1e12, v)) if v == v else 0\n'
    '    if isinstance(v, str): return clean_text(v, 120)\n'
    '    if depth >= 2: return None\n'
    '    if isinstance(v, list): return [clean_profile(x, depth + 1) for x in v[:12]]\n'
    '    if isinstance(v, dict):\n'
    '        out = {}\n'
    '        for k, x in list(v.items())[:40]:\n'
    '            if isinstance(k, str) and re.fullmatch(r"[A-Za-z0-9_]{1,16}", k): out[k] = clean_profile(x, depth + 1)\n'
    '        return out\n'
    '    return None\n')

rep('''            if self.route()[0] == "/events":''',
    '''            if self.route()[0] == "/player":   # V536: Spielprofil je Gerät
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
            if self.route()[0] == "/admin/claim":   # V536: einmalig für Martins Gerät
                if not rate_ok(self.client_ip(), "ad", 6):
                    return self.send_json(429, {"error": "too many requests"})
                d = self.parse_json(raw, n)
                if d.get("uid") != ADMIN_UID:
                    return self.send_json(403, {"error": "forbidden"})
                with db() as c:
                    if c.execute("SELECT 1 FROM kv WHERE k='admin:claimed'").fetchone():
                        return self.send_json(403, {"error": "already claimed"})
                    tok = secrets.token_urlsafe(32)
                    c.execute("INSERT OR REPLACE INTO kv(k,v) VALUES('admin:hash',?)", (hashlib.sha256(tok.encode()).hexdigest(),))
                    c.execute("INSERT OR REPLACE INTO kv(k,v) VALUES('admin:claimed',?)", (str(now_ms()),))
                return self.send_json(200, {"ok": True, "token": tok})
            if self.route()[0] == "/admin/players":   # V536: Spielerliste nur mit Admin-Schlüssel
                if not rate_ok(self.client_ip(), "ad", 30):
                    return self.send_json(429, {"error": "too many requests"})
                d = self.parse_json(raw, n)
                tok = d.get("token")
                with db() as c:
                    r = c.execute("SELECT v FROM kv WHERE k='admin:hash'").fetchone()
                    if not (r and isinstance(tok, str) and hmac.compare_digest(r["v"], hashlib.sha256(tok.encode()).hexdigest())):
                        return self.send_json(403, {"error": "forbidden"})
                    rows = c.execute("SELECT uid, first, last, n, data FROM players ORDER BY first, uid").fetchall()
                lst = []
                for i, x in enumerate(rows):
                    try: dd = json.loads(x["data"])
                    except Exception: dd = {}
                    lst.append({"no": i + 1, "uid": x["uid"], "first": x["first"], "last": x["last"], "n": x["n"], "d": dd})
                return self.send_json(200, {"ok": True, "now": now_ms(), "list": lst})
            if self.route()[0] == "/events":''')

rep('''        c.execute("DELETE FROM nuts WHERE t < ?", (cutoff,))\n''',
    '''        c.execute("DELETE FROM nuts WHERE t < ?", (cutoff,))\n        c.execute("DELETE FROM players WHERE last < ?", (int(time.time() * 1000) - PLAYER_RETENTION_DAYS * 86400 * 1000,))\n''')
open(p, "w", encoding="utf-8").write(s); print("ok api536")
