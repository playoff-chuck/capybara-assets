# V698 (Martin 13.11. 12:13): Cuddle Zombie nur in W57, 77, 97, 117, 137 – dort sind die ersten 5 Monster nur sie,
# danach (falls die Welle weitergeht) die normalen Monster. In allen anderen Wellen kommt sie nicht. Test-Link zeigt genau das.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep('GAME_VER = "V697"', 'GAME_VER = "V698"')
rep('const cuF = G.cuddleFrom || 57, cuddles = w >= cuF ? 1 + Math.floor((w - cuF) / 20) : 0;   /* V697 */',
    'const cuF = G.cuddleFrom || 57, cuddleW = !S.nuts && w >= cuF && (w - cuF) % 20 === 0;   /* V698: W57/77/97/117/137 */')
rep('if (w >= G.kieferFrom && S.totalSpawned % 30 === 0) kind = "kiefer";',
    'if (cuddleW && idx < 5) kind = "cuddle";   /* V698: erste 5 Monster dieser Welle sind Cuddle Zombies */\n  else if (w >= G.kieferFrom && S.totalSpawned % 30 === 0) kind = "kiefer";')
rep('''else if ((S.testCuddle && idx % 3 === 1) || [...Array(cuddles)].some((_, k) => slot(k, cuddles) + 3 === idx)) kind = "cuddle";   /* V697: Cuddle Zombie */
  ''', '')
rep('TEST · CUDDLE ZOMBIE in wave 57 · 99 lives · build towers right next to the path', 'TEST · wave 57 starts with 5 CUDDLE ZOMBIES · 99 lives · build towers right next to the path')
open(dst, "w", encoding="utf8").write(s)
print("ok V698")
