#!/usr/bin/env python3
"""V531 (Martin 09.11. 20:24/20:25): Hall of Fame-Titel wie im Squad-Screen (fett, font-weight 700);
Name + «LVL … · …» unten links im Startmenü linksbündig.
Aufruf: python3 tools/patch531.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V530";', 'const GAME_VER = "V531";')
rep('.sqLvl:empty{display:none}', '.sqLvl:empty{display:none}\n#sqLvl,.sqLvl{text-align:left!important}\n#ovHs .hsBox h2{font-weight:700!important}')
open(p, "w", encoding="utf-8").write(s); print("ok V531")
