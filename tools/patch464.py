#!/usr/bin/env python3
"""V464 – Blue-Sprechblase verschwindet wieder (Vergleich über Zähler statt übersetztem Text).
Nuts-Disco: Spots 50 % durchsichtiger, Discokugel entfernt.
Nutzung: python3 tools/patch464.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V463";', 'const GAME_VER = "V464";')
rep('const mine = el.querySelector(".say").innerHTML; bT = setTimeout(() => { if (el.querySelector(".say").innerHTML === mine) el.classList.remove("on"); }, 2800); }',
    'const mine = String((+el.dataset.bn || 0) + 1); el.dataset.bn = mine; bT = setTimeout(() => { if (el.dataset.bn === mine) el.classList.remove("on"); }, 2800); }   /* V464: übersetzter Text bricht den Vergleich nicht mehr */')
rep('rgba(255,40,70,.55),rgba(255,40,70,.16) 70%', 'rgba(255,40,70,.28),rgba(255,40,70,.08) 70%')
rep('rgba(255,60,200,.5),rgba(255,60,200,.14) 70%', 'rgba(255,60,200,.25),rgba(255,60,200,.07) 70%')
rep('rgba(255,20,20,.5),rgba(255,20,20,.14) 70%', 'rgba(255,20,20,.25),rgba(255,20,20,.07) 70%')
rep('rgba(255,50,110,.55),rgba(255,50,110,0) 70%', 'rgba(255,50,110,.28),rgba(255,50,110,0) 70%')
rep('<div class="nzHalo"></div><div class="nzBall"></div>', '<div class="nzHalo"></div>')
open(dst, "w", encoding="utf-8").write(s)
print("ok V464")
