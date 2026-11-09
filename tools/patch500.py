#!/usr/bin/env python3
"""V500: Elite-Turm-Laser (MAX) 60 s → 3 min (Martin 09.11. 14:42). Aufruf: python3 tools/patch500.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V499";', 'const GAME_VER = "V500";')
rep('t.eliteT = 60;', 't.eliteT = 180;')
rep('brings the Elite tower · 2× fire rate for 60 s`', 'brings the Elite tower · 2× fire rate for 180 s`')
rep('Not for sale · your partner parachutes in with it. 60 s pink laser', 'Not for sale · your partner parachutes in with it. 180 s pink laser')
open(p, "w", encoding="utf-8").write(s); print("ok V500")
