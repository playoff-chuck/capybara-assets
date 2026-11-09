#!/usr/bin/env python3
"""V506: Weltkarte – Abstand Nuts-Punkt ↔ Nuts-Schild gleich wie Orts-Punkt ↔ Orts-Schild (~6 px), Martin 09.11. 15:41.
Aufruf: python3 tools/patch506.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V505";', 'const GAME_VER = "V506";')
rep('.mNuts .nzTag{position:absolute;left:0;top:54px;', '.mNuts .nzTag{position:absolute;left:0;top:50px;')
open(p, "w", encoding="utf-8").write(s); print("ok V506")
