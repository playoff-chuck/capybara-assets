"""V341 (Martin 06.11. 23:54): Bildausfall-Rauschen nochmal −30 % (0,0245 → 0,017)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V340";', 'const GAME_VER = "V341";')
rep('noiseLevel(inside ? 0.0245 : 0);', 'noiseLevel(inside ? 0.017 : 0);')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
