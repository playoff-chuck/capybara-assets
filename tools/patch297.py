"""V297 (Martin 18:58): Hagelsturm-Einzelblöcke nochmals 100 % schneller (Fall-Intervall ÷ 3 statt ÷ 1,5)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V296";', 'const GAME_VER = "V297";')
rep('if (hailOn()) return g / 1.5;   /* V292: Hagel 50 % schneller */', 'if (hailOn()) return g / 3;   /* V292/V297: Hagel ×3 schneller als normal */')
open(dst, 'w', encoding='utf-8').write(s)
