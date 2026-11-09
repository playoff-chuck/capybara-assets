#!/usr/bin/env python3
"""V495: Einladungs-Bild – Logo 50 % kleiner, oben links (Martin 09.11. 10:35). Aufruf: python3 tools/patch495.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V494";', 'const GAME_VER = "V495";')
rep('if (logo) { const lw = 560, lh = logo.naturalHeight * lw / logo.naturalWidth; g.drawImage(logo, (W - lw) / 2, 20, lw, Math.min(lh, 340)); }',
    'if (logo) { const lw = 280, lh = logo.naturalHeight * lw / logo.naturalWidth; g.drawImage(logo, 36, 30, lw, Math.min(lh, 170)); }')
open(p, "w", encoding="utf-8").write(s); print("ok V495")
