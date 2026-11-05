"""V302 Server: Cloud-Speicherstand (/api/save) mit Wiederherstellungscode, je Code die letzten 5 Stände + Datenschutztext."""
p='server/api/app.py'; s=open(p).read()
def rep(a,b):
    global s; assert s.count(a)==1,a[:60]; s=s.replace(a,b)
rep('anonymous round stats, anonymous error/event log.', 'anonymous round stats, anonymous error/event log, cloud save by restore code.')
rep('VERSION = "1.1"', '''VERSION = "1.2"
SAVE_MAX_BODY = 60000
SAVE_MAX_DATA = 48000
SAVE_KEEP = 5
SAVE_RETENTION_DAYS = 730
SAVES_PER_MIN = 20
SAVE_READS_PER_MIN = 10
CODE_RE = re.compile(r"[0-9A-HJKMNP-TV-Z]{10}")
SAVE_KEY_RE = re.compile(r"(tarnturm|capy)-[a-z0-9_-]{1,40}")''')
rep('CREATE INDEX IF NOT EXISTS events_kind ON events(kind, t);\n', '''CREATE INDEX IF NOT EXISTS events_kind ON events(kind, t);
CREATE TABLE IF NOT EXISTS saves(
  id INTEGER PRIMARY KEY, k TEXT NOT NULL, t INTEGER NOT NULL, ver TEXT, wave INTEGER, size INTEGER, data TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS saves_k ON saves(k, t DESC);
''')
rep('''        c.execute("DELETE FROM events WHERE t < ?", (ecut,))''', '''        c.execute("DELETE FROM events WHERE t < ?", (ecut,))
        scut = int(time.time() * 1000) - SAVE_RETENTION_DAYS * 86400 * 1000
        c.execute("DELETE FROM saves WHERE k IN (SELECT k FROM saves GROUP BY k HAVING MAX(t) < ?)", (scut,))

def save_key(code):
    """Der Code selbst wird nie gespeichert, nur sein Hash."""
    if not isinstance(code, str):
        raise Bad("bad code")
    c = code.upper().replace("-", "").replace(" ", "").replace("O", "0").replace("I", "1").replace("L", "1")
    if c.startswith("CAPY"):
        c = c[4:]
    if not CODE_RE.fullmatch(c):
        raise Bad("bad code")
    return hashlib.sha256(("capy-save:" + c).encode()).hexdigest()''')
rep('''            if p == "/events/summary":
                return self.send_json(200, self.event_summary(qs))''', '''            if p == "/events/summary":
                return self.send_json(200, self.event_summary(qs))
            if p == "/save":
                if not rate_ok(self.client_ip(), "r", SAVE_READS_PER_MIN):
                    return self.send_json(429, {"error": "too many requests"})
                k = save_key(qs.get("code", [""])[0])
                with db() as c:
                    r = c.execute("SELECT t, ver, wave, data FROM saves WHERE k=? ORDER BY t DESC, id DESC LIMIT 1", (k,)).fetchone()
                if not r:
                    return self.send_json(404, {"error": "unknown code"})
                return self.send_json(200, {"ok": True, "t": r["t"], "ver": r["ver"], "wave": r["wave"], "data": json.loads(r["data"])})''')
rep('''            if self.route()[0] == "/events":''', '''            if self.route()[0] == "/save":
                if not rate_ok(self.client_ip(), "s", SAVES_PER_MIN):
                    return self.send_json(429, {"error": "too many requests"})
                return self.post_save(self.parse_json(raw, n, SAVE_MAX_BODY))
            if self.route()[0] == "/events":''')
rep('''    def do_POST(self):''', '''    def post_save(self, d):
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

    def do_POST(self):''')
open(p,'w').write(s)

p='server/privacy/index.html'; s=open(p).read()
rep('<li>Your game progress stays on your device.</li>', '<li>Your game progress is stored on your device and, as a backup, on our server under a random restore code – without your name.</li>')
rep('<h2>Anonymous error and usage log</h2>', '''<h2>Cloud backup of your progress</h2>
<p>So that your progress is never lost (for example after changing your phone), the game backs up your local game data on our server: progress, best results, medals, settings and your made-up call sign. The backup is filed under a random restore code that only you see in the game (☁ Cloud save). We store only a fingerprint (hash) of the code, never the code itself, and no name, e-mail or device ID. With the code you can restore your progress on any device. We keep the last five backups per code; backups are deleted 24 months after the last update, or earlier if you ask us and send the code.</p>
<h2>Anonymous error and usage log</h2>''')
rep('<li>Dein Spielstand bleibt auf deinem Gerät.</li>', '<li>Dein Spielstand liegt auf deinem Gerät und als Sicherung unter einem zufälligen Wiederherstellungscode auf unserem Server – ohne deinen Namen.</li>')
rep('<h2>Anonymes Fehler- und Nutzungsprotokoll</h2>', '''<h2>Cloud-Sicherung deines Spielstands</h2>
<p>Damit dein Spielstand nie verloren geht (z. B. bei einem Handywechsel), sichert das Spiel deine lokalen Spieldaten auf unserem Server: Fortschritt, Bestwerte, Medaillen, Einstellungen und dein ausgedachtes Rufzeichen. Die Sicherung liegt unter einem zufälligen Wiederherstellungscode, den nur du im Spiel siehst (☁ Cloud save). Wir speichern nur einen Fingerabdruck (Hash) des Codes, nie den Code selbst, und keinen Namen, keine E-Mail und keine Geräte-ID. Mit dem Code kannst du deinen Spielstand auf jedem Gerät wiederherstellen. Wir behalten die letzten fünf Sicherungen je Code; sie werden 24 Monate nach der letzten Aktualisierung gelöscht oder früher, wenn du uns darum bittest und den Code nennst.</p>
<h2>Anonymes Fehler- und Nutzungsprotokoll</h2>''')
open(p,'w').write(s)
print("ok")
