#!/usr/bin/env python3
"""Capybara Squad – Meldungen in Martins Telegram-Kanal.
  capy_tg.py status        → Bot/Kanal eingerichtet?
  capy_tg.py find          → Kanal aus getUpdates erkennen (Bot muss als Admin im Kanal sein, eine Nachricht im Kanal posten)
  capy_tg.py send <text>   → Text in den Kanal
  capy_tg.py testers       → neue Tester-Anmeldungen (.com und .ru) melden (läuft alle 2 min per Timer)
Token liegt nur in /srv/capy-api/secret/tg.json (0600), nie in Logs/Chat.
"""
import sys, json, os, sqlite3, subprocess, urllib.request, urllib.parse, datetime
SEC = '/srv/capy-api/secret/tg.json'; ST = '/root/capy_tg_state.json'

def cfg():
    return json.load(open(SEC)) if os.path.exists(SEC) else {}

def state():
    return json.load(open(ST)) if os.path.exists(ST) else {"com": 0, "ru": 0, "upd": 0}

def save_state(s):
    json.dump(s, open(ST, 'w'))

def api(method, **kw):
    c = cfg()
    if not c.get("bot"): raise SystemExit("kein Bot-Token")
    d = urllib.parse.urlencode(kw).encode()
    return json.loads(urllib.request.urlopen(f"https://api.telegram.org/bot{c['bot']}/{method}", d, timeout=20).read().decode())

def send(text):
    s = state()
    if not s.get("chat"): print("kein Kanal"); return False
    for i in range(0, len(text), 3900):
        api("sendMessage", chat_id=s["chat"], text=text[i:i + 3900], disable_web_page_preview="true")
    return True

def find():
    s = state(); r = api("getUpdates", offset=-20, timeout=0, allowed_updates=json.dumps(["channel_post", "my_chat_member", "message"]))
    for u in r.get("result", []):
        s["upd"] = u["update_id"] + 1
        for k in ("channel_post", "my_chat_member", "message"):
            x = u.get(k) or {}; ch = x.get("chat")
            if not ch or ch.get("type") not in ("channel", "supergroup", "group"): continue
            if k == "my_chat_member" and (x.get("new_chat_member") or {}).get("status") not in ("administrator", "member"): continue
            s["chat"] = ch["id"]; s["title"] = ch.get("title")
    save_state(s); print("Kanal:", s.get("title"), "gefunden" if s.get("chat") else "noch nicht gefunden")
    return s.get("chat")

def rows_com(last):
    c = sqlite3.connect('/srv/capy-api/data.db')
    return c.execute("SELECT id,t,name,email,tg,msg,lang,site FROM testers WHERE id>? ORDER BY id", (last,)).fetchall()

def rows_ru(last):
    q = f"import sqlite3,json;print(json.dumps(sqlite3.connect('/srv/capy-api/data.db').execute('SELECT id,t,name,email,tg,msg,lang,site FROM testers WHERE id>{int(last)} ORDER BY id').fetchall()))"
    out = subprocess.run(["ssh", "-i", "/root/.ssh/ru_server", "-o", "ConnectTimeout=10", "root@177.177.219.65", "python3", "-c", json.dumps(q)],
                         capture_output=True, text=True, timeout=40).stdout.strip()
    return json.loads(out) if out else []

def testers():
    s = state()
    if not s.get("chat"):
        if cfg().get("bot"): find()
        s = state()
        if not s.get("chat"): return
    for key, fn in (("com", rows_com), ("ru", rows_ru)):
        try: rows = fn(s.get(key, 0))
        except Exception as e: print(key, "Fehler", e); continue
        for (i, t, name, em, tg, msg, lang, site) in rows:
            tm = datetime.datetime.utcfromtimestamp(t / 1000) + datetime.timedelta(hours=3)
            txt = (f"🧪 Neuer Tester ({'RU' if key == 'ru' else 'COM'}, {lang or '?'}) – {tm:%d.%m. %H:%M} MSK\n"
                   f"Name: {name or '–'}\nE-Mail: {em}\nTelegram: {tg or '–'}" + (f"\nNachricht: {msg}" if msg else ""))
            send(txt); s[key] = i; save_state(s)

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'
    if cmd == 'status':
        c = cfg(); s = state(); print("Bot:", c.get("user") or "fehlt", "| Kanal:", s.get("title") or "fehlt")
    elif cmd == 'find': find()
    elif cmd == 'send': send(' '.join(sys.argv[2:]))
    elif cmd == 'testers': testers()
