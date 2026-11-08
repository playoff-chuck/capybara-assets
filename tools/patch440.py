#!/usr/bin/env python3
"""V440: Elite-Wow – nur der Partner (nicht der eigene Held) springt ab und bringt den Elite-Turm (Martin 08.11. 11:47).
Nutzung: python3 tools/patch440.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('GAME_VER = "V439"', 'GAME_VER = "V440"')
rep('ch(h, 1.0, 0, "") + ch(b, 1.25, 26, " b2")', 'ch(b, 1.0, 0, "")   /* V440: nur der Partner springt */')
rep('announce("ELITE TOWER", "Rosie & Blue on board · 2× fire rate for 60 s", "SQUAD", 2400)',
    'announce("ELITE TOWER", `${b === "rosie" ? "Rosie" : "Blue"} brings the Elite tower · 2× fire rate for 60 s`, "SQUAD", 2400)')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
