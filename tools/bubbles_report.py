#!/usr/bin/env python3
"""Sprechblasen-Statistik aus autotest60 (BUBBLES=1): wie oft pro Spielminute Blue/Rosie, General, Buchhalter, DJ
und sonstige Fenster auftauchen – gesamt, je Welle und je Ort (5 Wellen).
Aufruf: python3 tools/bubbles_report.py <autotest.json> [<ausgabe.md>]"""
import json, sys
res = json.load(open(sys.argv[1]))
B = res.get("bubbles", [])
GROUP = {"buddy": "Blue/Rosie", "general": "General", "book": "Buchhalter", "dj": "DJ", "coach": "Coach-Karte",
         "ovIntro": "Fenster", "ovAd": "Fenster", "ovBandit": "Fenster", "ovOrders": "Fenster", "ovJoin": "Fenster",
         "ovCoachAd": "Fenster", "ovSign": "Fenster", "hackPill": "Boss-Hack-Knopf"}
COLS = ["Blue/Rosie", "General", "Buchhalter", "DJ", "Coach-Karte", "Fenster", "Boss-Hack-Knopf"]
if not B:
    print("keine Sprechblasen-Daten"); sys.exit(1)
t_end = max(b["t"] for b in B); t0 = min(b["t"] for b in B)
mins = max(0.1, (t_end - t0) / 60)
waves = {}
for b in B:
    waves.setdefault(b["w"], {"t0": b["t"], "t1": b["t"], "n": {}})
    x = waves[b["w"]]; x["t0"] = min(x["t0"], b["t"]); x["t1"] = max(x["t1"], b["t"])
    g = GROUP.get(b["k"], b["k"]); x["n"][g] = x["n"].get(g, 0) + 1
tot = {c: sum(1 for b in B if GROUP.get(b["k"], b["k"]) == c) for c in COLS}
out = [f"Spielzeit {mins:.1f} min · {len(B)} Auftritte · Wellen {min(waves)}–{max(waves)}", "",
       "## Gesamt (pro Spielminute)", "", "| Sprecher | Anzahl | pro Minute |", "|---|---|---|"]
out += [f"| {c} | {tot[c]} | {tot[c] / mins:.2f} |" for c in COLS]
out += ["", "## Je Ort (5 Wellen)", "", "| Ort (Wellen) | " + " | ".join(COLS) + " | Summe/min |", "|" + "---|" * (len(COLS) + 2)]
ws = sorted(waves)
for o in range(0, max(ws) // 5 + 1):
    grp = [w for w in ws if (max(w, 1) - 1) // 5 == o]
    if not grp: continue
    n = {c: sum(waves[w]["n"].get(c, 0) for w in grp) for c in COLS}
    dur = max(0.1, (max(waves[w]["t1"] for w in grp) - min(waves[w]["t0"] for w in grp)) / 60)
    out.append(f"| W{o * 5 + 1}–{o * 5 + 5} | " + " | ".join(str(n[c]) for c in COLS) + f" | {sum(n.values()) / dur:.1f} |")
out += ["", "## Je Welle", "", "| Welle | " + " | ".join(COLS) + " |", "|" + "---|" * (len(COLS) + 1)]
for w in ws:
    out.append(f"| {w} | " + " | ".join(str(waves[w]["n"].get(c, 0)) for c in COLS) + " |")
gen = {}
for b in B:
    if b["k"] == "general": gen[b.get("tag", "")] = gen.get(b.get("tag", ""), 0) + 1
out += ["", "## General-Meldungen nach Art", "", "| Art | Anzahl |", "|---|---|"] + [f"| {k or '–'} | {v} |" for k, v in sorted(gen.items(), key=lambda x: -x[1])]
txt = "\n".join(out)
print(txt)
if len(sys.argv) > 2: open(sys.argv[2], "w").write(txt + "\n")
