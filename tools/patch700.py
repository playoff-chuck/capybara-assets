# V700 (Martin 13.11. 12:40): in W58/78/98/118/138 ist jedes 5. Monster Натааа (statt der ersten 5).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep('GAME_VER = "V699"', 'GAME_VER = "V700"')
rep('if (cuddleW && idx < 5) kind = "cuddle";   /* V698: erste 5 Monster dieser Welle sind Cuddle Zombies */',
    'if (cuddleW && idx % 5 === 4) kind = "cuddle";   /* V700: jedes 5. Monster dieser Welle ist ein Cuddle Zombie */')
rep('TEST · wave 58 starts with 5 CUDDLE ZOMBIES', 'TEST · wave 58 · every 5th monster is a CUDDLE ZOMBIE')
open(dst, "w", encoding="utf8").write(s)
print("ok V700")
