"""Auswertung Meldungs-Analyse (To-do 10): liest meld30-JSONs, zählt gleichzeitige Kanäle und Medaillen-Takt.
Aufruf: python3 tools/meld_auswertung.py out.json lauf1.json [lauf2.json ...]"""
import json, sys, itertools
from collections import Counter, defaultdict
out, files = sys.argv[1], sys.argv[2:]
VOICE_MS = 2200   # Sprachclip gilt ~2,2 s als «läuft»
WIN = {"intro", "ad", "bandit", "hackAd", "duel", "join", "sign", "orders", "drop", "give", "map", "tip"}
runs = []
for f in files:
    try: r = json.load(open(f)); (runs.append(r) if not r.get("end", {}).get("stall") else None)   # hängengebliebene Läufe nicht mitzählen
    except Exception: pass
pairs, multi, perK, perWave, medW, medMin, dur = Counter(), Counter(), Counter(), defaultdict(Counter), [], [], []
for R in runs:
    iv = []   # (start, end, kanal, welle)
    openAt = {}
    for e in R.get("ch", []):
        if e["k"] == "voice": iv.append((e["t"], e["t"] + VOICE_MS, "voice", e["wave"])); continue
        if e["e"] == "on": openAt[e["k"]] = (e["t"], e["wave"])
        elif e["k"] in openAt: t0, w = openAt.pop(e["k"]); iv.append((t0, e["t"], e["k"], w))
    op = {}
    for e in R.get("ev", []):   # Fenster
        if e["k"] not in WIN: continue
        if e["e"] == "open": op[e["k"]] = (e["t"], e["wave"])
        elif e["e"] == "close" and e["k"] in op: t0, w = op.pop(e["k"]); iv.append((t0, e["t"], "win:" + e["k"], w))
    for a in iv: perK[a[2].split(":")[0]] += 1; perWave[a[3]][a[2].split(":")[0]] += 1
    # Überlappungen im 250-ms-Raster
    if iv:
        t0, t1 = min(a[0] for a in iv), max(a[1] for a in iv); t = t0; prevSet = frozenset()
        while t < t1:
            on = frozenset(a[2].split(":")[0] for a in iv if a[0] <= t < a[1])
            if len(on) >= 2 and on != prevSet:
                multi[len(on)] += 1
                for p in itertools.combinations(sorted(on), 2): pairs[p] += 1
            prevSet = on; t += 250
    meds = R.get("med", []) or [e for e in R.get("ch", []) if e.get("k") == "alert" and e.get("e") == "on" and "\U0001f396" in e.get("txt", "")]   # Medaillen aus Funk-Texten, falls S.medGot fehlt
    for m in meds: medW.append(m["wave"]); medMin.append(round(m["t"] / 60000, 1))
    dur.append(R.get("end", {}).get("t", 0) / 60000)
n = max(1, len(runs))
res = dict(runs=len(runs), minutesAvg=round(sum(dur) / n, 1),
           perRunByChannel={k: round(v / n, 1) for k, v in perK.most_common()},
           overlapPerRun={f"{k} gleichzeitig": round(v / n, 1) for k, v in sorted(multi.items())},
           topPairsPerRun=[(f"{a} + {b}", round(v / n, 1)) for (a, b), v in pairs.most_common(12)],
           perWave={w: dict(perWave[w]) for w in sorted(perWave)},
           medalsPerRun=round(len(medW) / n, 1), medalWaves=Counter(medW).most_common(), medalMinutes=sorted(medMin)[:200])
json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ("perWave", "medalMinutes")}, ensure_ascii=False, indent=1)[:2500])
