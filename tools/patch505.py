#!/usr/bin/env python3
"""V505: Weltkarte – Nuts-Schild mit Abstand unter dem Punkt (wie bei den Orts-Schildern), Martin 09.11. 15:23.
Aufruf: python3 tools/patch505.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V504";', 'const GAME_VER = "V505";')
rep('.mNuts .nzTag{position:absolute;left:0;top:42px;', '.mNuts .nzTag{position:absolute;left:0;top:54px;')
open(p, "w", encoding="utf-8").write(s); print("ok V505")
