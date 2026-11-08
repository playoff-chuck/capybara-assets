#!/usr/bin/env python3
"""V488: Tutorial Schritt 5 «HOLD THE RING» schließt nach 10 s von selbst (Martin 09.11. 01:15: «sollte nach 10 Sekunden
verschwinden, bleibt aber»). «Got it» schließt weiterhin sofort. Spiel läuft dabei weiter (V483).
Aufruf: python3 tools/patch488.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V487";', 'const GAME_VER = "V488";')
rep('at: "board", done: () => false },   /* V367: endet mit «Got it» · V483: Spiel läuft dabei weiter */',
    'at: "board", done: () => TUT.t >= 10 },   /* V367: «Got it» · V483: Spiel läuft dabei weiter · V488: nach 10 s von selbst zu (Martin 09.11.) */')
open(p, "w", encoding="utf-8").write(s); print("ok V488")
