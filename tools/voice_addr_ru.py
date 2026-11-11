#!/usr/bin/env python3
"""V640: RU-Anrede-Varianten der Sprachclips (Martin 11.11.): Schlüssel <k>__dr («дружище», ab W31) und <k>__dg («друг», ab W61).
Quelle: site/lang/voice_ru.json t[k] mit «, напарник». HeyGen-TTS (Stimme «Martin 4min»), gleiche Nachbearbeitung wie voice_lang.py.
Aufruf (im Repo): python3 tools/voice_addr_ru.py <voice_id>"""
import json, re, sys, os, subprocess, base64, urllib.request, tempfile
V = sys.argv[1]; p = "site/lang/voice_ru.json"; out = json.load(open(p, encoding="utf-8"))
RX = re.compile(r", напарник(?=[\s.,!?–—])")
todo = {}
for k, t in list(out["t"].items()):
    if "__" in k or not RX.search(t): continue
    todo[k + "__dr"] = RX.sub(", дружище", t); todo[k + "__dg"] = RX.sub(", друг", t)
K = open("/etc/splatsquad/heygen.key").read().strip(); tot = 0; n = 0
for k, txt in todo.items():
    if out["v"].get(k) and out["t"].get(k) == txt: continue
    req = urllib.request.Request("https://api.heygen.com/v3/voices/speech", data=json.dumps({"text": txt, "voice_id": V}).encode(), headers={"X-API-KEY": K, "Content-Type": "application/json"})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=60))["data"]; tot += d.get("duration", 0)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f: wav = f.name
        urllib.request.urlretrieve(d["audio_url"], wav); mp3 = wav[:-4] + ".mp3"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-17:TP=-1.5:LRA=11,afade=t=in:d=0.01,areverse,afade=t=in:d=0.025,areverse", "-ar", "44100", "-b:a", "64k", mp3], check=True)
        out["v"][k] = base64.b64encode(open(mp3, "rb").read()).decode(); out["t"][k] = txt; n += 1
        os.remove(wav); os.remove(mp3)
        print("ok", k, round(d.get("duration", 0), 2), txt, flush=True)
    except Exception as e: print("ERR", k, e, flush=True)
json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False)
print("neu", n, "von", len(todo), "total_s", round(tot, 1), "cost_usd", round(tot * 0.000333, 4))
