#!/usr/bin/env python3
"""Capybara Squad – Google-Test-Lab-Lauf mit der selbstspielenden Test-App (Game-Loop).
Aufruf: testlab_daily.py daily   → 1 Gerät je Kategorie (5), Gerät rotiert täglich
        testlab_daily.py all     → alle 15 Geräte (3 je Kategorie)
Ergebnis: /root/tlw/daily/<datum>-<modus>.md/.json, Kurzbericht per /root/capy_tg.py send (falls eingerichtet).
"""
import sys, json, time, re, os, datetime, urllib.request, urllib.parse, subprocess
sys.path.insert(0, '/root'); import gtok
P = "capybara-514506-d7d2e"; B = "capy-testlab-514506"
APK = '/srv/testapp/app/build/outputs/apk/debug/app-debug.apk'
CATS = [
    ("Alt-klein",   [("a03su", "33"), ("RMX3231", "30"), ("TECNO-BF6", "31")]),
    ("Schmal-lang", [("a06", "35"), ("RE58C2", "35"), ("TECNO-BG6", "33")]),
    ("Standard",    [("a16", "35"), ("a15", "34"), ("a26x", "36")]),
    ("Neu-schnell", [("a56x", "35"), ("houji", "35"), ("pa1q", "36")]),
    ("Tablet",      [("gta9pwifi", "34"), ("gta8wifi", "34"), ("TB330FU", "35")]),
]
NAMES = {"a03su": "Galaxy A03s", "RMX3231": "realme C11", "TECNO-BF6": "Tecno Pop 7", "a06": "Galaxy A06", "RE58C2": "realme C53",
         "TECNO-BG6": "Tecno Spark Go 2024", "a16": "Galaxy A16", "a15": "Galaxy A15", "a26x": "Galaxy A26", "a56x": "Galaxy A56",
         "houji": "Xiaomi 14", "pa1q": "Galaxy S25", "gta9pwifi": "Galaxy Tab A9+", "gta8wifi": "Galaxy Tab A8", "TB330FU": "Lenovo Tab M11"}
OUT = '/root/tlw/daily'; os.makedirs(OUT, exist_ok=True)

def gcs_get(name):
    r = urllib.request.Request(f"https://storage.googleapis.com/storage/v1/b/{B}/o/{urllib.parse.quote(name, safe='')}?alt=media",
                               headers={'Authorization': 'Bearer ' + gtok.TOK, 'x-goog-user-project': P})
    return urllib.request.urlopen(r, timeout=120).read()

def gcs_list(prefix):
    s, b = gtok.call('GET', f"https://storage.googleapis.com/storage/v1/b/{B}/o?prefix={urllib.parse.quote(prefix)}", None, qp=P)
    return [i['name'] for i in json.loads(b).get('items', [])]

def analyse(txt):
    L = txt.split('\n')
    waves = [int(m.group(1)) for l in L for m in [re.search(r'CAPYAUTO w=(\d+)', l)] if m]
    err = [l for l in L if 'CapyJS' in l and 'ERROR' in l and not any(x in l for x in ('ResizeObserver', "hasn't tapped", 'vibrate'))]   # harmlose Browser-Hinweise (kein Tippen im Test) ignorieren
    F = [(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))) for l in L for m in [re.search(r'fps=(\d+) min=(\d+) jank=(\d+) lite=(\d)', l)] if m]
    F = F[1:] or F   # erste 10 s (Laden) weglassen
    perf = {"fps": round(sum(f[0] for f in F) / len(F)) if F else None, "fps_min": min(f[1] for f in F) if F else None,
            "ruckler": sum(f[2] for f in F), "leicht": any(f[3] for f in F)}
    return {**perf, "geladen": any('CAPYAUTO inject' in l for l in L), "gestartet": any('CAPYAUTO start' in l for l in L),
            "welle": max(waves) if waves else 0, "js_fehler": len(err), "fehler_bsp": [e[-160:] for e in err[:3]],
            "absturz": any('FATAL EXCEPTION' in l and 'webtest' in txt for l in L), "anr": any('ANR in com.playcapybarasquad' in l for l in L)}

def main(mode):
    day = datetime.date.today()
    if mode == 'all':
        devs = [(c, m, v) for c, lst in CATS for m, v in lst]
    elif mode.startswith('nur:'):   # z. B. nur:a03su,a06 – gezielter Extra-Lauf
        want = mode[4:].split(',')
        devs = [(c, m, v) for c, lst in CATS for m, v in lst if m in want]
    else:
        k = day.toordinal() % 3
        devs = [(c, lst[k][0], lst[k][1]) for c, lst in CATS]
    ts = time.strftime('%m%d%H%M'); name = f"app/capy-webtest-daily-{ts}.apk"
    req = urllib.request.Request(f"https://storage.googleapis.com/upload/storage/v1/b/{B}/o?uploadType=media&name={name}", data=open(APK, 'rb').read(),
                                 headers={'Authorization': 'Bearer ' + gtok.TOK, 'Content-Type': 'application/vnd.android.package-archive', 'x-goog-user-project': P}, method="POST")
    urllib.request.urlopen(req, timeout=120)
    gcs = f"results/daily-{ts}/"
    body = {"projectId": P, "testSpecification": {"testTimeout": "320s", "androidTestLoop": {"appApk": {"gcsPath": f"gs://{B}/{name}"}}},
            "environmentMatrix": {"androidDeviceList": {"androidDevices": [{"androidModelId": m, "androidVersionId": v, "locale": "ru", "orientation": "portrait"} for _, m, v in devs]}},
            "resultStorage": {"googleCloudStorage": {"gcsPath": f"gs://{B}/{gcs}"}, "toolResultsHistory": {"projectId": P}}, "flakyTestAttempts": 0}
    s, b = gtok.call("POST", f"https://testing.googleapis.com/v1/projects/{P}/testMatrices", body, qp=P)
    mx = json.loads(b).get('testMatrixId'); print('matrix', s, mx, flush=True)
    if not mx: raise SystemExit(b[:500])
    t0 = time.time(); d = {}
    while time.time() - t0 < 75 * 60:
        time.sleep(60)
        if int(time.time() - t0) // 60 % 20 == 0: gtok.TOK = gtok.token()
        s, b = gtok.call('GET', f'https://testing.googleapis.com/v1/projects/{P}/testMatrices/{mx}', None, qp=P); d = json.loads(b)
        if d.get('state') in ('FINISHED', 'ERROR', 'INVALID'): break
    gtok.TOK = gtok.token()
    rows = []
    items = gcs_list(gcs)
    for ex in d.get('testExecutions', []):
        m = ex['environment']['androidDevice']['androidModelId']; v = ex['environment']['androidDevice']['androidVersionId']
        cat = next(c for c, mm, vv in devs if mm == m)
        r = {"kategorie": cat, "geraet": NAMES.get(m, m), "modell": m, "android": v, "status": ex.get('state'), "info": (ex.get('testDetails') or {}).get('errorMessage', '')}
        lc = [i for i in items if i.startswith(f"{gcs}{m}-{v}-") and i.endswith('/logcat')]
        if lc:
            try: r.update(analyse(gcs_get(lc[0]).decode('utf8', 'replace')))
            except Exception as e: r["info"] += f" logcat: {e}"
        vid = [i for i in items if i.startswith(f"{gcs}{m}-{v}-") and i.endswith('video.mp4')]
        if vid: r["video"] = vid[0]
        rows.append(r)
    res = {"datum": str(day), "modus": mode, "matrix": mx, "zustand": d.get('state'), "ergebnis": d.get('outcomeSummary'), "geraete": rows}
    base = f"{OUT}/{day}-{mode.replace(':', '-').replace(',', '_')}"; json.dump(res, open(base + '.json', 'w'), ensure_ascii=False, indent=1)
    lines = [f"📱 Google-Handytest {day} ({'15 Geräte' if mode == 'all' else ('Extra-Lauf ' + mode[4:] if mode.startswith('nur:') else 'täglich, 5 Geräte')}) – {d.get('outcomeSummary') or d.get('state')}"]
    for r in rows:
        ok = r.get('gestartet') and not r.get('absturz') and not r.get('anr') and not r.get('js_fehler')
        lines.append(f"{'✅' if ok else ('⚪' if not r.get('geladen') else '❌')} {r['kategorie']}: {r['geraet']} (A{r['android']}) – " +
                     (f"läuft, Welle {r.get('welle', 0)}" + (f", {r['fps']} FPS (tiefster {r['fps_min']}), Ruckler {r['ruckler']}" + (", Sparmodus" if r.get('leicht') else "") if r.get('fps') is not None else "") + "" + (f", {r['js_fehler']} Spielfehler" if r.get('js_fehler') else ", keine Fehler") + (", ABSTURZ" if r.get('absturz') else "") + (", HÄNGER" if r.get('anr') else "")
                      if r.get('geladen') else "Google-Gerät nicht verfügbar (kein Fehler im Spiel)"))
    open(base + '.md', 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))
    if os.path.exists('/root/capy_tg.py'):
        subprocess.run(['python3', '/root/capy_tg.py', 'send', '\n'.join(lines)], timeout=60)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'daily')
