#!/usr/bin/env python3
# V549: Gold-Tipp-Titel «BUILD A TOWER TO SPLAT MONSTERS!» statt «SPEND YOUR GOLD!» (Martin 10.11. 12:05)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V548";', 'const GAME_VER = "V549";')
rep('t: "SPEND YOUR GOLD!",', 't: "BUILD A TOWER TO SPLAT MONSTERS!",')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
