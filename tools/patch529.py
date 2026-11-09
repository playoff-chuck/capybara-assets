#!/usr/bin/env python3
"""V529 (Martin 09.11. 20:21): Zahnrad-Menü (und andere Fenster dieser Art) überdeckt den Lautstärke-Knopf/Logo oben –
solange so ein Fenster offen ist, werden Lautstärke-Knopf und Startlogo ausgeblendet (das ✕ des Fensters ist frei).
Aufruf: python3 tools/patch529.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V528";', 'const GAME_VER = "V529";')
rep('#ovStart[hidden] #stLogo,#ovStart:not(.artReady) #stLogo{display:none!important}',
    '#ovStart[hidden] #stLogo,#ovStart:not(.artReady) #stLogo{display:none!important}\nbody:has(.overlay.joinOv:not([hidden])) #stMute,body:has(.overlay.joinOv:not([hidden])) #stLogo,body:has(#ovDaily:not([hidden])) #stMute{display:none!important}')
open(p, "w", encoding="utf-8").write(s); print("ok V529")
