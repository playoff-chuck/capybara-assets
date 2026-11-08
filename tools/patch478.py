#!/usr/bin/env python3
"""V478 – Höhlen-Hintergrundbilder für alle vier Nuts-Territorien (t140, Martin 08.11. 22:36 «die Höhle in Südamerika passt, dann … für die anderen Kontinente»):
bg/nuts_africa.webp (gold), bg/nuts_asia.webp (eisblau), bg/nuts_namerica.webp (canyon-rot), Nano Banana Pro mit Südamerika-Bild als Stilvorlage (3 × 0,14 $).
Nutzung: python3 tools/patch478.py src dst"""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

m = re.search(r'const GAME_VER = "V(\d+)";', s); v = int(m.group(1))
rep(m.group(0), f'const GAME_VER = "V{v + 1}";')
rep('const NUTS_BG = ["bg/nuts_samerica.webp", null, null, null];   /* V473: echtes Höhlenbild je Nuts-Territorium (null = alter Look) */',
    'const NUTS_BG = ["bg/nuts_samerica.webp", "bg/nuts_africa.webp", "bg/nuts_asia.webp", "bg/nuts_namerica.webp"];   /* V473/V478: echtes Höhlenbild je Nuts-Territorium (null = alter Look) */')
open(dst, "w", encoding="utf-8").write(s); print("ok", v + 1)
