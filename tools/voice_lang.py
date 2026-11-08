#!/usr/bin/env python3
"""Sprachclips für eine Sprache mit HeyGen (geklonte Stimme) erzeugen → site/lang/voice_<lang>.json {t:{key:text}, v:{key:base64 mp3}}.
Aufruf (auf dem Server, im Repo): python3 tools/voice_lang.py <lang> <voice_id> [nur_zaehlen]
Texte: VOICE_TEXT aus site/index.html, übersetzt über site/lang/<lang>.json (exakt, dann #-Muster). Fehlende bleiben weg (englischer Clip bleibt).
Kosten: 0,000333 $/s (Starfish TTS); am Ende wird die Summe ausgegeben. Clips: Stille abschneiden, −17 LUFS, 10 ms Ein-/25 ms Ausblende (Klick-Schutz V433)."""
import json, re, sys, os, subprocess, base64, urllib.request, tempfile
lang, V = sys.argv[1], sys.argv[2]; count_only = len(sys.argv) > 3
s = open("site/index.html", encoding="utf-8").read()
vt = json.loads(re.search(r"const VOICE_TEXT = (\{.*?\});\n", s, re.S).group(1))
D = json.load(open(f"site/lang/{lang}.json", encoding="utf-8"))
NUM = re.compile(r"[-−]?\d[\d.,:/]*\d|[-−]?\d")
lines = {}
for k, t in vt.items():
    v = D.get(t) or D.get(NUM.sub("#", t))
    if v: lines[k] = v
print(lang, len(lines), "von", len(vt), "Zeilen übersetzt")
if count_only: sys.exit(0)
out_p = f"site/lang/voice_{lang}.json"
out = json.load(open(out_p, encoding="utf-8")) if os.path.exists(out_p) else {"t": {}, "v": {}}
K = open("/etc/splatsquad/heygen.key").read().strip(); tot = 0; n = 0
for k, txt in lines.items():
    if out["v"].get(k) and out["t"].get(k) == txt: continue
    req = urllib.request.Request("https://api.heygen.com/v3/voices/speech", data=json.dumps({"text": txt, "voice_id": V}).encode(), headers={"X-API-KEY": K, "Content-Type": "application/json"})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=60))["data"]; tot += d.get("duration", 0)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f: wav = f.name
        urllib.request.urlretrieve(d["audio_url"], wav); mp3 = wav[:-4] + ".mp3"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-17:TP=-1.5:LRA=11,afade=t=in:d=0.01,areverse,afade=t=in:d=0.025,areverse", "-ar", "44100", "-b:a", "64k", mp3], check=True)
        out["v"][k] = base64.b64encode(open(mp3, "rb").read()).decode(); out["t"][k] = txt; n += 1
        os.remove(wav); os.remove(mp3)
        if n % 10 == 0: json.dump(out, open(out_p, "w", encoding="utf-8"), ensure_ascii=False)
        print("ok", k, round(d.get("duration", 0), 2), flush=True)
    except Exception as e: print("ERR", k, e, flush=True)
json.dump(out, open(out_p, "w", encoding="utf-8"), ensure_ascii=False)
print("neu", n, "total_s", round(tot, 1), "cost_usd", round(tot * 0.000333, 4), "→", out_p, os.path.getsize(out_p) // 1024, "KB")
