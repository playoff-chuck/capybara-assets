"""V245: Guide-Texte an den Ablauf angepasst: Wild Cards kommen alle 20 Wellen (nicht alle 10), das Boss-Signal alle paar
Wellen (nicht jede 5.)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V244";', 'const GAME_VER = "V245";')
rep('"Every 10th wave: pick one wild card with an upside and a downside."', '"Every 20th wave: pick one wild card with an upside and a downside."')
rep('"Every 5th wave: hack the boss for gold. Win = stake ×2."', '"Every few waves: hack the boss for gold. Win = stake ×2."')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
