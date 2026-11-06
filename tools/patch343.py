"""V343 (Martin 07.11. 00:02): Test-Wellen (?test=… / Dev-Liste) laufen 5 Minuten statt 3 – genug Zeit, das Unkraut ganz wachsen zu sehen."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V342";', 'const GAME_VER = "V343";')
rep('S.testLongUntil = performance.now() + 180000;', 'S.testLongUntil = performance.now() + 300000;')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
