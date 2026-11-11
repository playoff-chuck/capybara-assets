#!/usr/bin/env python3
"""V641: Hänger-Suche – welches Ereignis wartet länger als 2 Wellen? Aufruf: python3 tools/pend_auswertung.py out.json [...]"""
import json, sys
for f in sys.argv[1:]:
    d = json.load(open(f)); P = d.get("pend", []); since = {}; bad = []
    for e in P:
        for k in ("hack", "ad", "lucky", "join", "ord", "nuts", "intro"):
            v = e.get(k)
            if v in (0, "", None): since.pop(k, None); continue
            if k not in since or since[k][1] != v: since[k] = (e["w"], v)
            elif e["w"] - since[k][0] > 2: bad.append((k, v, since[k][0], e["w"])); since[k] = (e["w"], v)
    print(f, "Einträge", len(P), "bis Welle", P[-1]["w"] if P else "-")
    for b in bad: print("  WARTET >2 Wellen:", b[0], "=", b[1], "seit W", b[2], "noch in W", b[3])
    if not bad: print("  keine Hänger > 2 Wellen")
