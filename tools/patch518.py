#!/usr/bin/env python3
"""V518: Betonmischer – Beton fließt über eine niedrigere Wand nach außen und füllt dort alles bis zur Höhe der höchsten Wand (Martin 09.11. 16:46).
Aufruf: python3 tools/patch518.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V517";', 'const GAME_VER = "V518";')
rep('for (const [dx, dy] of DIRS) { const nx = cx + dx, ny = cy + dy; if (nx < x0 || nx > x1 || ny < level || ny >= GH || !free(nx, ny)) continue;',
    'for (const [dx, dy] of DIRS) { const nx = cx + dx, ny = cy + dy; if (nx < 0 || nx >= GW || ny < level || ny >= GH || !free(nx, ny)) continue;   /* V518: läuft über niedrige Wände nach außen */')
open(p, "w", encoding="utf-8").write(s); print("ok V518")
