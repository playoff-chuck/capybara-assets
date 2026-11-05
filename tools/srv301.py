"""V301 Server: anonymes Fehler-/Ereignis-Log in capy-api (/api/events, /api/events/summary) + Datenschutztext."""
p='server/api/app.py'; s=open(p).read()
def rep(a,b):
    global s; assert s.count(a)==1,a[:60]; s=s.replace(a,b)
rep('"""Capybara Squad API - high scores, nuts board, anonymous round stats.',
    '"""Capybara Squad API - high scores, nuts board, anonymous round stats, anonymous error/event log.')
rep('VERSION = "1.0"', '''VERSION = "1.1"
EVENT_RETENTION_DAYS = 90
EVENT_MAX_BODY = 8192
EVENTS_PER_MIN = 20
EVENT_KINDS = ("start", "error", "leave", "back", "wave")''')
rep('CREATE INDEX IF NOT EXISTS runs_t ON runs(t);\n', '''CREATE INDEX IF NOT EXISTS runs_t ON runs(t);
CREATE TABLE IF NOT EXISTS events(
  id INTEGER PRIMARY KEY, t INTEGER NOT NULL, ver TEXT, sess TEXT, kind TEXT NOT NULL, wave INTEGER, scr TEXT,
  msg TEXT, src TEXT, mins REAL, dev INTEGER, plat TEXT, br TEXT, sw INTEGER, sh INTEGER, mem REAL);
CREATE INDEX IF NOT EXISTS events_t ON events(t);
CREATE INDEX IF NOT EXISTS events_kind ON events(kind, t);
''')
rep('''def purge_old_runs():
    cutoff = int(time.time() * 1000) - RUN_RETENTION_DAYS * 86400 * 1000
    with db() as c:
        c.execute("DELETE FROM runs WHERE t < ?", (cutoff,))''', '''def purge_old_runs():
    cutoff = int(time.time() * 1000) - RUN_RETENTION_DAYS * 86400 * 1000
    ecut = int(time.time() * 1000) - EVENT_RETENTION_DAYS * 86400 * 1000
    with db() as c:
        c.execute("DELETE FROM runs WHERE t < ?", (cutoff,))
        c.execute("DELETE FROM events WHERE t < ?", (ecut,))

_URLQ = re.compile(r"(https?://[^\\s?#]*)[?#]\\S*")
def clean_text(v, maxlen):
    """Fehlertext ohne URL-Parameter, ohne Steuerzeichen, gekürzt."""
    if not isinstance(v, str):
        return ""
    v = _URLQ.sub(r"\\1", v)
    v = re.sub(r"[\\x00-\\x1f\\x7f]+", " ", v).strip()
    return v[:maxlen]''')
rep('''    def parse_json(self, raw, n):
        if n > MAX_BODY:''', '''    def parse_json(self, raw, n, limit=MAX_BODY):
        if n > limit:''')
rep('''            if p == "/runs/summary":
                return self.send_json(200, self.summary(qs))''', '''            if p == "/runs/summary":
                return self.send_json(200, self.summary(qs))
            if p == "/events/summary":
                return self.send_json(200, self.event_summary(qs))''')
rep('''    def do_POST(self):
        try:
            raw, n = self.read_body()
            if raw is None:
                return self.send_json(413, {"error": "body too large"})
            if not rate_ok(self.client_ip(), "p", POST_PER_MIN):''', '''    def event_summary(self, qs):
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
            if not rate_ok(self.client_ip(), "p", POST_PER_MIN):''')
open(p,'w').write(s)

p='server/privacy/index.html'; s=open(p).read()
rep('<li>We collect anonymous round statistics (for example wave reached, cause of game over, gold) to balance the game. They contain no personal data.</li>',
    '<li>We collect anonymous round statistics (for example wave reached, cause of game over, gold) and an anonymous error log to balance the game and fix bugs. They contain no personal data.</li>')
rep('<h2>Server, IP address, cookies</h2>\n<p>Our server', '''<h2>Anonymous error and usage log</h2>
<p>To find and fix bugs, the game sends short technical notes to our server: error messages of the game, the wave and screen where you left or came back, the game version, a rough device description (operating system and browser version, screen size, memory class) and a random session number that is created anew every time the game starts and is never stored on your device. No call sign, no player ID, no advertising ID and no other identifier is sent. We use the log only in aggregated form. Entries are deleted after 90 days at the latest.</p>
<h2>Server, IP address, cookies</h2>
<p>Our server''')
rep('<li>Wir erfassen anonyme Rundenstatistiken (z. B. erreichte Welle, Grund für das Spielende, Gold), um das Spiel auszubalancieren. Sie enthalten keine personenbezogenen Daten.</li>',
    '<li>Wir erfassen anonyme Rundenstatistiken (z. B. erreichte Welle, Grund für das Spielende, Gold) und ein anonymes Fehlerprotokoll, um das Spiel auszubalancieren und Fehler zu beheben. Sie enthalten keine personenbezogenen Daten.</li>')
rep('<h2>Server, IP-Adresse, Cookies</h2>\n<p>Unser Server', '''<h2>Anonymes Fehler- und Nutzungsprotokoll</h2>
<p>Um Fehler zu finden und zu beheben, sendet das Spiel kurze technische Hinweise an unseren Server: Fehlermeldungen des Spiels, Welle und Bildschirm, an dem du das Spiel verlässt oder zurückkehrst, die Spielversion, eine grobe Gerätebeschreibung (Betriebssystem- und Browserversion, Bildschirmgröße, Speicherklasse) und eine Zufallsnummer der Sitzung, die bei jedem Spielstart neu entsteht und nicht auf deinem Gerät gespeichert wird. Es werden kein Rufzeichen, keine Spieler-ID, keine Werbe-ID und keine sonstige Kennung übertragen. Wir werten das Protokoll nur zusammengefasst aus. Einträge werden spätestens nach 90 Tagen gelöscht.</p>
<h2>Server, IP-Adresse, Cookies</h2>
<p>Unser Server''')
open(p,'w').write(s)
print("ok")
