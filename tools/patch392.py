"""V392: Boss-Hack nie im Kontinent-Schlusswelle (Regelwerk: «nie mit Orts-/Kontinentwechsel»).
Meldungs-Analyse: überfälliger Hack aus W28 erschien in W30 ~28 s vor «CONTINENT CLEARED» / Wegweiser.
Jetzt: während Welle 30/60/90/120/150 läuft, wartet der Boss-Hack; er kommt nach dem Wechsel (W31 usw., mit 30 s Ruhe).
Aufruf: python3 tools/patch392.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
rep('!S.ordDue && !hkSignFirst() && ', '!S.ordDue && !hkSignFirst() && !(S.inWave && (S.wave || 0) % 30 === 0) && ')
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
