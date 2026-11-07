"""V389: Wow-Momente fest an Wellen gebunden (Martin ok, 07.11.):
- Squad Incoming (Gratis-Ten-ton) bleibt W1.
- Erster Dreifach-Splat ab W2 (bis W6 als Nachhol-Fenster), beim ersten Treffer; Nachbar-Monster aus dem ganzen Feld statt nur < 7 Felder.
- Elite-Turm in W6, 10 s nach Wellenstart (bis W9, falls noch kein Turm mit Waffe) statt nach 150 s Spielzeit.
Aufruf: python3 tools/patch389.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
rep('''!S.testRun && S.wave >= 1 && S.wave <= 6 && performance.now() - WOW.tonT > 6000 && hit.size >= 3) {''',
    '''!S.testRun && S.wave >= 2 && S.wave <= 6 && performance.now() - WOW.tonT > 6000 && hit.size >= 3) {   /* V%d: fest ab W2 */''' % NEW)
rep('''more = alive.filter(m => !inHit(m) && Math.hypot(m.x - f.x, m.y - f.y) < 7).sort(''',
    '''more = alive.filter(m => !inHit(m)).sort(''')
rep('''function wowOk() { return S.started && !S.over && !S.nuts && !S.testRun && !(TUT && TUT.on) && !frozen() && (S.wave || 0) >= 1 && S.wave <= 6; }''',
    '''function wowOk(maxW = 6) { return S.started && !S.over && !S.nuts && !S.testRun && !(TUT && TUT.on) && !frozen() && (S.wave || 0) >= 1 && S.wave <= maxW; }''')
rep('''if (!wowDone("elite") && WOW.pt > 150 && wowOk() && S.inWave && performance.now() - WOW.tonT > 8000) {''',
    '''if (!wowDone("elite") && S.wave >= 6 && WOW.wt > 10 && wowOk(9) && S.inWave && performance.now() - WOW.tonT > 8000) {   /* V%d: fest W6, 10 s nach Start */''' % NEW)
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
