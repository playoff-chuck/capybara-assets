#!/usr/bin/env python3
# V593 (Tutorial-Bot, 10 Durchgänge): auf schmalen Handys (360/362 breit) zeigte der gelbe Pfeil auf Blöcke am Rand
# ZWISCHEN zwei Spalten – er wurde 34 px vom Rand weg geschoben. Jetzt zeigt die Spitze genau auf die Mitte des Blocks
# (höchstens 6 px Randabstand; der Pfeil darf dafür etwas über den Rand ragen). Das ist Martins Screenshot von 01:59.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V592";', 'const GAME_VER = "V593";')
rep('      if (!r.side) x = Math.max(34, Math.min(innerWidth - 34, x));',
    '      if (!r.side) x = Math.max(6, Math.min(innerWidth - 6, x));   /* V593: Spitze genau auf die Blockmitte, auch am Rand */')
open(dst, "w", encoding="utf-8").write(s)
print("ok V593")
