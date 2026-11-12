# V683 (Martin 12.11. 19:29): Admin-Knopf «Check news» entfernt (zeigte alle Neuheiten-Fenster nacheinander; mitten im Lauf
# gespeichert blieben die «schon gesehen»-Merker leer, die Fenster kamen dann im normalen Spiel wieder).
# Der zugehörige Code bleibt stehen und tut ohne Knopf nichts (if (!btn) return).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
rep('<button id="devFresh">Street player</button><button id="devNews">Check news</button></div>', '<button id="devFresh">Street player</button></div>')
rep('const GAME_VER = "V682"', 'const GAME_VER = "V683"')
open(dst, "w", encoding="utf8").write(s); print("ok", len(s))
