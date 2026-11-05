"""V267 (Martin 05.11. 15:16): Boss-Hack-Angebot ohne Ausnahme unter der Abstandsregel (45 s / max. 1 Angebot je 2,5 min).
Haben sich mehrere vorgemerkt, wird nur eins gezeigt (das jüngste) – nie mehrere hintereinander."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V266";', 'const GAME_VER = "V267";')
rep('window.__offerOK(S.wave >= S.hackPending + 2))', 'window.__offerOK())')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
