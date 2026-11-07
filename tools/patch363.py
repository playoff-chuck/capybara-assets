"""V363 (Martin 07.11. 08:13): Lucky Supply bis Welle 60 um 30 % seltener
(Abstand bis zum nächsten Lucky 7–10 statt 5–7 Wellen, Ø 8,5 statt 6 → Häufigkeit ×0,71). Ab Welle 60 unverändert."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V362";', 'const GAME_VER = "V363";')
rep('S.banditNext = (S.wave || 1) + 5 + Math.floor(Math.random() * 3);',
    'S.banditNext = (S.wave || 1) + ((S.wave || 1) < 60 ? 7 + Math.floor(Math.random() * 4) : 5 + Math.floor(Math.random() * 3));   /* V363: bis Welle 60 30 % seltener */')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
