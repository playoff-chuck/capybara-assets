# V699 (Martin 13.11. 12:32): Cuddle Zombie nicht in W57 (Sonderwelle «Doppelsicht» – man sieht schlecht).
# Neu: W58, dann alle 20 Wellen (78, 98, 118, 138) – alle ohne Sonderwelle/Störung. Erste 5 Monster sind sie.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep('GAME_VER = "V698"', 'GAME_VER = "V699"')
rep('G.cuddleFrom || 57', 'G.cuddleFrom || 58', 2)
rep('cuddle: 57,', 'cuddle: 58,')
rep('/* V698: W57/77/97/117/137 */', '/* V699: W58/78/98/118/138 */')
rep('TEST · wave 57 starts with 5 CUDDLE ZOMBIES', 'TEST · wave 58 starts with 5 CUDDLE ZOMBIES')
open(dst, "w", encoding="utf8").write(s)
print("ok V699")
