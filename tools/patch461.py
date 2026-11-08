#!/usr/bin/env python3
"""V461 – Portugiesisch (Brasilien) live: lang/pt.json. Kurze Tages-Chip-Namen («10 Ton», «Sniper») in es/pt.
Nutzung: python3 tools/patch461.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V460";', 'const GAME_VER = "V461";')
open(dst, "w", encoding="utf-8").write(s)
print("ok V461")
