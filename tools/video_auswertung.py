#!/usr/bin/env python3
"""Auswertung videotest: hängende Elemente (zu lange sichtbar) und Überdeckungen (zwei Overlays überlappen sich).
Aufruf: python3 tools/video_auswertung.py <ausgabe_ordner>   (Ordner aus tools/videotest.py mit frames.json)"""
import json, sys, re
from collections import defaultdict
D = sys.argv[1]; J = json.load(open(f"{D}/frames.json")); F = J["frames"]; STEP = 2.5
# dauerhaft erlaubte HUD-Elemente (immer da)
PERSIST = re.compile(r"^\|?(genAv|djSong|buddy|sky|bPauseTop|awBar|coach|nutsBadge|hkMiss|btnMap|btnOffline|comicArrow|thiefCv|scorePop|score|cell|barSnake|grp|djBox|waveNum|bWave|hud|lever|pad|ctl)(\||#|$)", re.I)
LIMITS = [  # (regex auf key, maximale Sichtdauer in s)
    (re.compile(r"toast|stamp|praise|pop", re.I), 12), (re.compile(r"ann|banner|wowBan", re.I), 25), (re.compile(r"bubble|say|rb", re.I), 25),
    (re.compile(r"wowPlane|wowCoins", re.I), 8), (re.compile(r"crate|drop", re.I), 40), (re.compile(r"tip|hint", re.I), 20), (re.compile(r"book|ledger", re.I), 20)]
LIMIT_DEFAULT = 90   # Fenster, die der Bot schließt: >90 s ist verdächtig
# Sichtbarkeits-Spannen je Schlüssel (key+text)
runs = defaultdict(list)   # key -> [(start_i, end_i, text, rect)]
prev = {}
for f in F:
    cur = {}
    for e in f["el"]:
        if PERSIST.match(e["k"]): continue
        k = e["k"] + "#" + e["t"][:25]; cur[k] = e
        if k in prev: prev[k]["end"] = f["i"]
        else: prev[k] = {"start": f["i"], "end": f["i"], "e": e, "wave": f["wave"]}
    for k in list(prev):
        if k not in cur: runs[k].append(prev.pop(k))
for k, v in prev.items(): runs[k].append(v)
stuck = []
for k, L in runs.items():
    for r in L:
        dur = (r["end"] - r["start"] + 1) * STEP
        lim = LIMIT_DEFAULT
        for rx, l in LIMITS:
            if rx.search(k): lim = l; break
        if dur > lim: stuck.append((dur, k, r["start"], r["end"], r["wave"]))
stuck.sort(reverse=True)
# Überdeckungen: zwei transiente Elemente im selben Frame, deren Rechtecke sich überschneiden (>25 % des kleineren)
def inter(a, b):
    x = max(0, min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])); y = max(0, min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])); return x * y
ov = defaultdict(list)
for f in F:
    els = [e for e in f["el"] if not PERSIST.match(e["k"])]
    for i in range(len(els)):
        for j in range(i + 1, len(els)):
            a, b = els[i], els[j]; ar = inter(a["r"], b["r"]); sm = min(a["r"][2] * a["r"][3], b["r"][2] * b["r"][3])
            if sm and ar / sm > 0.25:
                pair = tuple(sorted([a["k"].split("|")[0] or a["k"], b["k"].split("|")[0] or b["k"]])); ov[pair].append((f["i"], f["wave"], a["t"][:30], b["t"][:30]))
print("Frames:", len(F), "bis Welle", F[-1]["wave"], "| Konsole-Fehler:", len(J["console"]))
for c in J["console"][:10]: print("  ERR", c[:150])
print("\n== Hängende Elemente (zu lange sichtbar) ==")
for d, k, s, e, w in stuck[:40]: print(f"  {d:6.0f}s  W{w:<3} f{s}-f{e}  {k[:90]}")
print("\n== Überdeckungen (Paare, Anzahl Frames) ==")
for pair, L in sorted(ov.items(), key=lambda x: -len(x[1]))[:40]:
    print(f"  {len(L):4d}  {pair[0][:40]} × {pair[1][:40]}   z.B. f{L[0][0]} W{L[0][1]}  «{L[0][2]}» / «{L[0][3]}»")
