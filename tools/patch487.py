#!/usr/bin/env python3
"""V487: Grizzly HP ×4 → ×3 (Martin 09.11. «3 ok»). Kontroll-Simulation V485: Grizzly W96–101 war Hauptkiller
des schwächeren Spielers (74 % der Monster-Tode). Fell −2 je Treffer bleibt. Codex-Zeile und en.json-Schlüssel angepasst.
Aufruf: python3 tools/patch487.py site/index.html site/lang/en.json"""
import sys
p, pl = sys.argv[1], sys.argv[2]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V486";', 'const GAME_VER = "V487";')
rep('tiger: 2.2, bear: 4.0, norm: 1 }[kind]);', 'tiger: 2.2, bear: 3.0, norm: 1 }[kind]);   /* V487: Grizzly ×4 → ×3 */')
rep('["HP ×4", "Speed ×0.7", "Fur −2"]', '["HP ×3", "Speed ×0.7", "Fur −2"]')
open(p, "w", encoding="utf-8").write(s)
s = open(pl, encoding="utf-8").read()
rep('"HP ×4": "HP ×4",', '"HP ×3": "HP ×3",')
open(pl, "w", encoding="utf-8").write(s); print("ok V487")
