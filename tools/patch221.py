"""V221: Münze neben dem Boss-Monster entfernt."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V220";', 'const GAME_VER = "V221";')
rep('<img src="${src}" alt=""><span class="hkCoin">$</span></div>', '<img src="${src}" alt=""></div>')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
