#!/usr/bin/env python3
"""V467 – Deutsch live (lang/de.json); «PLACE» im Shop als Verb (SETZEN/COLOCAR).
Nutzung: python3 tools/patch467.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
a, b = 'const GAME_VER = "V466";', 'const GAME_VER = "V467";'
assert s.count(a) == 1; s = s.replace(a, b)
open(dst, "w", encoding="utf-8").write(s); print("ok V467")
