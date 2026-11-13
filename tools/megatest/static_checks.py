#!/usr/bin/env python3
"""Megatest – einmalige Prüfungen ohne Browser: A1 (Knacken in Dateien), A6 (Abtastrate), A13 (doppelte Wörter),
A14 (Sprachclips je Sprache), C7 (Schlüssel in es/pt, unübersetzte Werte), C12 (Glyphen latin), C14 (Marken), B16 (Bildpfade)."""
import json, os, re, subprocess, sys, glob
import numpy as np
SITE = sys.argv[1]; OUT = sys.argv[2]; F = []
def add(cat, key, msg, sev="M"): F.append({"cat": cat, "key": key, "msg": msg[:240], "sev": sev})
idx = open(os.path.join(SITE, "index.html"), encoding="utf8").read()
# A1 + A6: Audio-Dateien
aud = [p for p in glob.glob(SITE + "/**/*", recursive=True) if p.lower().endswith((".mp3", ".m4a", ".ogg", ".wav", ".opus", ".mp4"))]
for p in sorted(aud):
    rel = os.path.relpath(p, SITE)
    try:
        sr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=sample_rate", "-of", "csv=p=0", p], capture_output=True, text=True, timeout=30).stdout.strip()
        if sr and int(sr) > 48000: add("A6", rel, f"{rel}: {sr} Hz (Android spielt > 48 kHz teils nicht)", "K")
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", "44100", "-f", "f32le", "-"], capture_output=True, timeout=120).stdout
        x = np.frombuffer(raw, dtype=np.float32)
        if not len(x): add("A1", rel, f"{rel}: nicht dekodierbar", "K"); continue
        clip = int((np.abs(x) >= 0.999).sum())
        d2 = np.abs(np.diff(x, 2)); music = ('music/' in rel) or ('anthem' in rel) or len(x) > 44100 * 20; thr = 0.5 if music else 0.25; fac = 25 if music else 6
        # Knacken = einzelner Sprung, der deutlich über dem Umfeld liegt (Musik mit vielen Transienten nicht doppelt zählen)
        idxs = np.where(d2 > thr)[0]
        loc = 0
        for i in idxs[:5000]:
            a, b = max(0, i - 220), min(len(d2), i + 220)
            if d2[i] > fac * (np.median(d2[a:b]) + 1e-4): loc += 1
        if clip > 50: add("A1", rel + ":clip", f"{rel}: {clip} Samples bei 0 dBFS (Übersteuerung)", "K")
        if loc > 3: add("A1", rel + ":click", f"{rel}: {loc} Knackstellen (Sprung 2. Ableitung > {thr})", "K")
    except Exception as e:
        add("A1", rel, f"{rel}: Prüfung fehlgeschlagen {e}", "N")
# Sprachclips: VOICE / VOICE_TEXT aus index.html
def jsobj(name):
    m = re.search(r"const " + name + r" = (\{.*?\});\n", idx, re.S)
    if not m: return {}
    try: return json.loads(m.group(1))
    except Exception: return {}
VT = jsobj("VOICE_TEXT"); VK = set(jsobj("VOICE").keys()) or set(VT.keys())
dup = re.compile(r"\b(\w{2,})[\s,]+\1\b", re.I | re.U)
for k, t in VT.items():
    if isinstance(t, str) and dup.search(t): add("A13", k, f"EN-Clip {k}: doppeltes Wort «{dup.search(t).group(0)}»", "N")
for l in ["es", "pt", "ru"]:
    p = os.path.join(SITE, "lang", f"voice_{l}.json")
    if not os.path.exists(p): add("A14", l, f"voice_{l}.json fehlt", "K"); continue
    v = json.load(open(p, encoding="utf8")); miss = sorted(VK - set((v.get("v") or {}).keys()))
    if miss: add("A14", l, f"{l.upper()}: {len(miss)} Sprachclips fehlen: {', '.join(miss[:12])}", "M")
    for k, t in (v.get("t") or {}).items():
        if isinstance(t, str) and dup.search(t): add("A13", l + ":" + k, f"{l.upper()}-Clip {k}: doppeltes Wort «{dup.search(t).group(0)}»", "N")
# C7 statisch
L = {l: json.load(open(os.path.join(SITE, "lang", f"{l}.json"), encoding="utf8")) for l in ["ru", "es", "pt"] if os.path.exists(os.path.join(SITE, "lang", f"{l}.json"))}
for l in ["es", "pt"]:
    if l not in L: continue
    miss = sorted(set(L["ru"]) - set(L[l]))
    if miss: add("C7", l + ":keys", f"{l.upper()}: {len(miss)} Schlüssel aus ru.json fehlen, z. B. {' | '.join(m[:30] for m in miss[:8])}", "M")
    same = [k for k, v in L[l].items() if v == k and re.search(r"[a-z]{4}", k) and len(k) > 6]
    if same: add("C7", l + ":same", f"{l.upper()}: {len(same)} Werte = englischer Text, z. B. {' | '.join(s[:30] for s in same[:8])}", "N")
# C12: Glyphen der latin-Schriften für es/pt
try:
    from fontTools.ttLib import TTFont
    chars = set("".join(str(v) for l in ("es", "pt") if l in L for v in L[l].values()))
    for fp in glob.glob(SITE + "/fonts/*latin.woff2"):
        f = TTFont(fp); cm = set()
        for t in f["cmap"].tables: cm |= set(t.cmap.keys())
        ext = fp.replace("latin.woff2", "latin-ext.woff2")
        if os.path.exists(ext):
            for t in TTFont(ext)["cmap"].tables: cm |= set(t.cmap.keys())
        miss = sorted(c for c in chars if c.isalpha() and ord(c) > 127 and ord(c) not in cm and ord(c) < 0x400)
        if miss: add("C12", os.path.basename(fp), f"{os.path.basename(fp)}: Zeichen fehlen {''.join(miss[:30])}", "M")
except Exception as e:
    add("C12", "fonttools", f"Glyphenprüfung nicht möglich: {e}", "N")
# C14: Marken / verbotene Begriffe in sichtbaren Texten
for l, d in [("en", {k: k for k in L.get("ru", {})})] + list(L.items()):
    for k, v in d.items():
        if re.search(r"tetris|tetromino|plants vs|pac-?man", str(v), re.I): add("C14", l + ":" + k[:30], f"{l.upper()}: Marke im Text «{str(v)[:60]}»", "K")
# B16: Bildpfade
for m in sorted(set(re.findall(r"""["'(]((?:img|bg|sign|pro|fin)/[\w./-]+\.(?:webp|png|jpg|svg))""", idx))):
    if not os.path.exists(os.path.join(SITE, m.split("?")[0])): add("B16", m, f"Bild fehlt auf dem Server: {m}", "K")
json.dump(F, open(OUT, "w"), ensure_ascii=False, indent=0); print("static", len(F), "Funde,", len(aud), "Audiodateien")
