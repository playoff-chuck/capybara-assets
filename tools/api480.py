#!/usr/bin/env python3
"""capy-api V480: /squad/join zählt einen Freund je Code höchstens 1× pro Minute und je Gerät/Netz (Hash aus Salt+Code+IP, keine IP gespeichert) 1× je 24 h.
Nutzung: python3 api480.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('''CREATE TABLE IF NOT EXISTS squads(
  code TEXT PRIMARY KEY, t INTEGER NOT NULL, n INTEGER NOT NULL DEFAULT 0, last INTEGER);''',
'''CREATE TABLE IF NOT EXISTS squads(
  code TEXT PRIMARY KEY, t INTEGER NOT NULL, n INTEGER NOT NULL DEFAULT 0, last INTEGER);
CREATE TABLE IF NOT EXISTS squad_joins(h TEXT PRIMARY KEY, t INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS kv(k TEXT PRIMARY KEY, v TEXT NOT NULL);''')
rep('''            if p == "/squad/join":
                code = squad_code(d.get("code"))
                with db() as c:
                    cur = c.execute("UPDATE squads SET n=MIN(n+1,?), last=? WHERE code=?", (SQUAD_MAX_N, now_ms(), code))
                    if cur.rowcount != 1:
                        return self.send_json(404, {"error": "unknown code"})
                return self.send_json(200, {"ok": True})''',
'''            if p == "/squad/join":
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
                return self.send_json(200, {"ok": True, "counted": True})''')
open(dst, "w", encoding="utf-8").write(s); print("ok")
