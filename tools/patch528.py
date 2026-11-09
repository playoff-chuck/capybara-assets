#!/usr/bin/env python3
"""V528 (Martin 09.11. 20:05): Abreißgeräusch 70 % leiser (sfx/tear.mp3 ×0,3) – Cache-Bust ?v=528.
Aufruf: python3 tools/patch528.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V527";', 'const GAME_VER = "V528";')
rep('.mp3?v=527"', '.mp3?v=528"', 2)
open(p, "w", encoding="utf-8").write(s); print("ok V528")
