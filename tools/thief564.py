#!/usr/bin/env python3
# V564: Dieb bekommt eine eigene tiefe Stimme (Martin 10.11. 17:31) – die Dieb-Clips in lang/voice_*.json
# werden um ~5,7 Halbtöne tiefer gesetzt (asetrate 0,72), etwas langsamer, mit mehr Bass. Nur einmal ausführen.
# Aufruf: python3 tools/thief564.py site
import sys, json, base64, subprocess, tempfile, os
site = sys.argv[1]
for l in ["ru", "es", "pt", "de"]:
    p = os.path.join(site, "lang", f"voice_{l}.json"); d = json.load(open(p, encoding="utf-8"))
    for k in ["thief_hello", "thief_laugh"]:
        if k not in d["v"]: continue
        with tempfile.TemporaryDirectory() as t:
            a, b = os.path.join(t, "a.mp3"), os.path.join(t, "b.mp3")
            open(a, "wb").write(base64.b64decode(d["v"][k]))
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a, "-af", "asetrate=44100*0.72,aresample=44100,atempo=1.2,bass=g=4:f=140,equalizer=f=2500:t=q:w=1:g=-3,volume=1.4,alimiter=limit=0.95", "-ac", "1", "-b:a", "64k", b], check=True)
            d["v"][k] = base64.b64encode(open(b, "rb").read()).decode()
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False)
    print(l, "ok")
