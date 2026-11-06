"""V342 (Martin 07.11. 00:00): Dieb braucht nach dem Diebstahl 20 s (statt 10 s) bis zum rechten Bildschirmrand – mehr Zeit zum Abschießen."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V341";', 'const GAME_VER = "V342";')
rep('if (T.t >= 20) { if (T.stolen) toast(`THIEF GOT AWAY', 'if (T.t >= 30) { if (T.stolen) toast(`THIEF GOT AWAY')
rep('gx + (innerWidth + SZ - gx) * Math.min(1, (T.t - 10) / 10)', 'gx + (innerWidth + SZ - gx) * Math.min(1, (T.t - 10) / 20)')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
