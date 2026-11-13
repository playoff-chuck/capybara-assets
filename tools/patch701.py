# V701 (Martin 13.11. 12:47): in W58/78/98/118/138 kommen nur Натааа (Cuddle Zombies), in derselben Menge wie sonst alle Monster.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep('GAME_VER = "V700"', 'GAME_VER = "V701"')
rep('if (cuddleW && idx % 5 === 4) kind = "cuddle";   /* V700: jedes 5. Monster dieser Welle ist ein Cuddle Zombie */',
    'if (cuddleW) kind = "cuddle";   /* V701: in dieser Welle kommen nur Cuddle Zombies, gleiche Anzahl wie sonst */')
rep('TEST · wave 58 · every 5th monster is a CUDDLE ZOMBIE', 'TEST · wave 58 · only CUDDLE ZOMBIES this wave')
open(dst, "w", encoding="utf8").write(s)
print("ok V701")
