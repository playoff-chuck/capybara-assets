#!/usr/bin/env python3
"""V439: ?test=elite – springt direkt in Welle 6 und setzt den Elite-Wow zurück (Martin 08.11. 11:43).
Nutzung: python3 tools/patch439.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('GAME_VER = "V438"', 'GAME_VER = "V439"')
rep('weed5: 131, thief: 100', 'weed5: 131, elite: 6, thief: 100')
rep('devJump(map[q], q.replace(/\\d$/, ""));',
    'devJump(map[q], q.replace(/\\d$/, "")); if (q === "elite") { try { LS.del("capy-wow-elite"); } catch (e) {} S.testRun = false; S.gold += 200; }   /* V439: Elite-Wow direkt in W6 testen */')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
