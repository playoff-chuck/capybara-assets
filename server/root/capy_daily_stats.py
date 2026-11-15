#!/usr/bin/env python3
"""Capybara Squad – Tagesstatistik (gestriger Tag, Moskauer Zeit) für Martins Telegram-Kanal.
  capy_daily_stats.py local [JJJJ-MM-TT]  → JSON dieses Servers
  capy_daily_stats.py send  [JJJJ-MM-TT]  → .com + .ru zusammen, Text in den Kanal (/root/capy_tg.py)
Zählt nur echte Spieler (team=0, dev=0)."""
import sys, json, sqlite3, datetime, subprocess, collections

def day_bounds(d):
    t0 = datetime.datetime(d.year, d.month, d.day) - datetime.timedelta(hours=3)   # MSK → UTC
    e = int(t0.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000)
    return e, e + 86400000

import re
def is_bot(x):
    """Test- und Robotergeräte (geprüft 14.11.2026 an den Daten vom 12.11.): Google-Play-Vorabtests, Emulatoren,
    Google-Test-Lab (Sprache ru + Zeitzone Los Angeles), Server-/Headless-Browser, Link-Vorschau-Roboter."""
    os_, app, scr, tz, loc = (str(x.get(k) or '') for k in ('os', 'app', 'scr', 'tz', 'loc'))
    if 'sdk_gphone' in os_ or 'OnePlus8Pro' in os_: return True                     # Play-Vorabbericht / Emulator
    if tz == 'America/Los_Angeles' and 'Android' in os_: return True                  # Google Test Lab (alle Geräte in LA-Zeit)
    if tz == 'Indian/Maldives': return True                                          # Martins/Familien-Testgeräte
    if os_.startswith('Linux'): return True                                          # Server, Headless, Crawler
    if 'Edge 12' in app or tz in ('Etc/Unknown', '+00:00'): return True               # Roboter
    m = re.match(r'(\d+)×(\d+) @1x', scr)
    if m and ('iPhone' in os_ or 'Android' in os_): return True                       # Handy mit Desktop-Bildschirm = gefälscht
    if os_.startswith('Windows') and scr.startswith(('800×600', '1024×1024', '1080×600')): return True   # Headless-Fenster
    return False

def local(d):
    c = sqlite3.connect('/srv/capy-api/data.db'); a, b = day_bounds(d); pa, _ = day_bounds(d - datetime.timedelta(days=1))
    q = "SELECT t,sess,kind,wave,mins,plat,uid,ch,data FROM events WHERE t>=? AND t<? AND uid IS NOT NULL AND dev=0 AND COALESCE(team,0)=0"
    bots = set()   # Google-Testgeräte (Sprache ru + Zeitzone Los Angeles) und Server-Browser (Linux) nicht mitzählen
    for u, dj in c.execute("SELECT uid, data FROM players"):
        try: x = json.loads(dj)
        except Exception: continue
        if is_bot(x): bots.add(u)
    bots |= {r[0] for r in c.execute("SELECT DISTINCT uid FROM events WHERE plat='Linux'")}
    bots |= {r[0] for r in c.execute("SELECT DISTINCT uid FROM events WHERE uid NOT IN (SELECT uid FROM players) OR sh>=5000 OR (sw=400 AND sh=400)")}   # ohne Profil = Crawler/Vorschau-Roboter
    ev = [r for r in c.execute(q, (a, b)).fetchall() if r[6] not in bots]
    uids = {r[6] for r in ev}
    first = dict(c.execute("SELECT uid, MIN(t) FROM events WHERE uid IS NOT NULL AND dev=0 AND COALESCE(team,0)=0 GROUP BY uid").fetchall())
    first = {u: t for u, t in first.items() if u not in bots}
    new = {u for u in uids if first.get(u, 0) >= a}
    prev_new = {u for u, t in first.items() if pa <= t < a}
    sm = collections.defaultdict(float); su = {}
    for r in ev:
        if r[1]: sm[r[1]] = max(sm[r[1]], r[4] or 0); su[r[1]] = r[6]
    mins_u = collections.defaultdict(float)
    for s, m in sm.items(): mins_u[su[s]] += m
    plat = collections.Counter(); ch = collections.Counter(); seen = set()
    for r in ev:
        if r[6] in seen: continue
        seen.add(r[6]); p = (r[5] or '').lower()
        plat['Android' if 'android' in p else 'iPhone/iPad' if 'ios' in p else 'PC/andere'] += 1
        ch['App' if r[7] == 'app' else 'Browser'] += 1
    k = collections.Counter(r[2] for r in ev)
    best = max([r[3] or 0 for r in ev if r[2] in ('wend', 'wave')] or [0])
    try: testers = c.execute("SELECT COUNT(*) FROM testers WHERE t>=? AND t<?", (a, b)).fetchone()[0]
    except Exception: testers = 0
    tot_players = len(first)
    return {"aktiv": len(uids), "neu": len(new), "rueck": len(uids - new), "sitzungen": len(sm), "minuten": round(sum(sm.values()), 1),
            "min_neu": round(sum(mins_u[u] for u in new), 1), "d1_basis": len(prev_new), "d1": len(prev_new & uids),
            "wellen": k.get('wend', 0), "beste": best, "kaeufe": k.get('buy', 0), "werbung": k.get('ad', 0), "boss_hack": k.get('hack', 0),
            "plat": dict(plat), "kanal": dict(ch), "tester": testers, "gesamt": tot_players,
            "spieler_min": sorted([round(v, 1) for v in mins_u.values()], reverse=True)}

def fmt(d, S):
    def s(k): return sum(x.get(k, 0) for x in S.values())
    def cnt(k):
        c = collections.Counter()
        for x in S.values(): c.update(x.get(k, {}))
        return ', '.join(f"{a} {b}" for a, b in c.most_common()) or '–'
    allm = sorted(sum((x.get('spieler_min', []) for x in S.values()), []), reverse=True)
    med = allm[len(allm) // 2] if allm else 0
    akt = s('aktiv'); d1b = s('d1_basis')
    L = [f"📊 Capybara Squad – {d:%d.%m.%Y} (MSK)",
         f"👤 Neue Spieler: {s('neu')}  (COM {S.get('com', {}).get('neu', 0)} · RU {S.get('ru', {}).get('neu', 0)})",
         f"🔁 Aktive Spieler: {akt}  (davon zurückgekehrt {s('rueck')})",
         f"⏱ Spielzeit: {s('minuten'):.0f} min gesamt · Ø {s('minuten') / akt:.1f} min/Spieler · Median {med:.1f} min" if akt else "⏱ Spielzeit: –",
         f"🆕 Spielzeit der Neuen: {s('min_neu'):.0f} min" + (f" (Ø {s('min_neu') / s('neu'):.1f})" if s('neu') else ""),
         f"📅 Wiederkehr Tag 1: {s('d1')} von {d1b} Neuen von vorgestern" + (f" ({100 * s('d1') / d1b:.0f} %)" if d1b else ""),
         f"🎮 Sitzungen {s('sitzungen')} · Wellen geschafft {s('wellen')} · beste Welle {max([x.get('beste', 0) for x in S.values()] or [0])}",
         f"🛒 Käufe im Laden {s('kaeufe')} · Werbung angesehen {s('werbung')} · Boss-Hacks {s('boss_hack')}",
         f"📱 Geräte: {cnt('plat')} · Zugang: {cnt('kanal')}",
         f"🧪 Tester-Anmeldungen: {s('tester')}",
         f"Σ Spieler bisher: {s('gesamt')}"]
    if len(S) < 2: L.append("⚠️ Nur Daten von: " + ', '.join(S))
    return '\n'.join(L)

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'local'
    d = datetime.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).date() - datetime.timedelta(days=1)
    if mode == 'local':
        print(json.dumps(local(d)))
    else:
        S = {"com": local(d)}
        try:
            subprocess.run(["scp", "-q", "-i", "/root/.ssh/ru_server", __file__, "root@177.177.219.65:/root/capy_daily_stats.py"], timeout=40)
            out = subprocess.run(["ssh", "-i", "/root/.ssh/ru_server", "-o", "ConnectTimeout=10", "root@177.177.219.65", "python3", "/root/capy_daily_stats.py", "local", str(d)],
                                 capture_output=True, text=True, timeout=60).stdout.strip()
            if out: S["ru"] = json.loads(out)
        except Exception as e: print("ru", e)
        txt = fmt(d, S); print(txt)
        if mode == 'send': subprocess.run(["python3", "/root/capy_tg.py", "send", txt], timeout=60)
