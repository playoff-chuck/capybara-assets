#!/usr/bin/env python3
"""Fügt tools/lang_src/<lang>_*.json zu site/lang/<lang>.json zusammen und prüft gegen site/lang/en.json.
Aufruf: python3 tools/i18n_merge.py <lang>
- Schlüssel, die in en.json fehlen, werden trotzdem übernommen (zusätzliche Muster).
- Zahl-Varianten (Schlüssel mit Ziffern), deren #-Muster übersetzt ist, gelten als gedeckt.
- Namen/Identitäten (Rosie, Blue, BPM …) fehlen bewusst – Rückfall ist der englische Text."""
import sys, json, glob, re, os
lang = sys.argv[1]
NUM = re.compile(r"\d[\d.,:/]*\d|\d")
en = json.load(open("site/lang/en.json", encoding="utf-8"))
out = {}
for f in sorted(glob.glob(f"tools/lang_src/{lang}_*.json")):
    if f.endswith("_missing.json"): continue
    d = json.load(open(f, encoding="utf-8"))
    for k, v in d.items():
        if k in out and out[k] != v: print("doppelt (anders):", k[:60])
        out[k] = v
# Platzhalter prüfen
bad = [k for k, v in out.items() if k.count("#") != v.count("#") or k.count("@") != v.count("@")]
if bad: print("Platzhalter-Fehler:", len(bad)); [print("  ", k[:70], "→", out[k][:70]) for k in bad[:20]]
missing = []
for k in en:
    if k in out: continue
    p = NUM.sub("#", k)
    if p != k and p in out: continue
    missing.append(k)
json.dump(out, open(f"site/lang/{lang}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
# neue Schlüssel auch in en.json (Identität) aufnehmen
add = [k for k in out if k not in en]
if add:
    for k in add: en[k] = k
    json.dump(dict(sorted(en.items())), open("site/lang/en.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0); print("en.json +", len(add))
json.dump(missing, open(f"tools/lang_src/{lang}_missing.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(lang, "Einträge", len(out), "fehlend (von en.json)", len(missing))
