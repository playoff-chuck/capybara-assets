#!/usr/bin/env python3
"""V504: LASER SHOW in 5 weiteren ruhigen Wellen (Martin 09.11. 15:11): 10, 26, 74, 109, 134 (+ 44).
Geprüft: keine Sonderwelle, kein Boss-Hack, kein Signalverlust/Magnet/Unkraut/Dieb, kein Elite/Ei/Wild-Card, keine neue Waffe/kein neues Monster, kein Kontinent-Anlauf.
Test: ?test=laser10 / laser26 / laser74 / laser109 / laser134. Aufruf: python3 tools/patch504.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V503";', 'const GAME_VER = "V504";')
rep('const LASER_WAVES = { 44: 1 };', 'const LASER_WAVES = { 10: 1, 26: 1, 44: 1, 74: 1, 109: 1, 134: 1 };')
rep('const map = { laser: 44,', 'const map = { laser: 44, laser10: 10, laser26: 26, laser74: 74, laser109: 109, laser134: 134,')
open(p, "w", encoding="utf-8").write(s); print("ok V504")
