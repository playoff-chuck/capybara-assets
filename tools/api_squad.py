#!/usr/bin/env python3
# t14 Teil 2 (Martin 07.11. 18:20): kleiner Zähler-Endpunkt für «Freunde einladen» in capy-api.
# POST /squad {} → {code}   · POST /squad/join {code} → {ok}   · GET /squad?code=X → {n}
# Gespeichert nur: Code, Anlegezeit, Zähler, letzte Einladung. Keine IP, keine Kennung.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)

rep('CREATE INDEX IF NOT EXISTS saves_k ON saves(k, t DESC);\n',
    'CREATE INDEX IF NOT EXISTS saves_k ON saves(k, t DESC);\nCREATE TABLE IF NOT EXISTS squads(\n  code TEXT PRIMARY KEY, t INTEGER NOT NULL, n INTEGER NOT NULL DEFAULT 0, last INTEGER);\n')
rep('SAVE_READS_PER_MIN = 10\n',
    'SAVE_READS_PER_MIN = 10\nSQUAD_ABC = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"\nSQUAD_RE = re.compile(r"[ABCDEFGHJKMNPQRSTUVWXYZ23456789]{6}")\nSQUAD_MAX_N = 100000\n')
rep('''def purge_old_entries():''', '''def squad_code(v):
    if not isinstance(v, str):
        raise Bad("bad code")
    c = v.strip().upper()
    if not SQUAD_RE.fullmatch(c):
        raise Bad("bad code")
    return c

def purge_old_entries():''')
# GET /squad?code=
rep('''            if p == "/save":
                if not rate_ok(self.client_ip(), "r", SAVE_READS_PER_MIN):''',
    '''            if p == "/squad":
                c0 = squad_code(qs.get("code", [""])[0])
                with db() as c:
                    r = c.execute("SELECT n FROM squads WHERE code=?", (c0,)).fetchone()
                if not r:
                    return self.send_json(404, {"error": "unknown code"})
                return self.send_json(200, {"ok": True, "n": r["n"]})
            if p == "/save":
                if not rate_ok(self.client_ip(), "r", SAVE_READS_PER_MIN):''')
# POST /squad, /squad/join
rep('''            if p == "/nuts":
                return self.post_nuts(d)
            return self.send_json(404, {"error": "not found"})''',
    '''            if p == "/nuts":
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
                with db() as c:
                    cur = c.execute("UPDATE squads SET n=MIN(n+1,?), last=? WHERE code=?", (SQUAD_MAX_N, now_ms(), code))
                    if cur.rowcount != 1:
                        return self.send_json(404, {"error": "unknown code"})
                return self.send_json(200, {"ok": True})
            return self.send_json(404, {"error": "not found"})''')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
