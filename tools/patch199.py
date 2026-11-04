"""V199: Herz zwischen Blue und Rosie auf dem Boss-Hack-Ergebnis entfernt."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V198";', 'const GAME_VER = "V199";')
rep('<span class="hrt">♥</span>', '')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
