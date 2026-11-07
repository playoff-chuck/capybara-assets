"""V399: Wolf heult sicher bei USE und beim Antippen des Diebs (Martin, 07.11.):
großzügige Trefferzone (±40 px) um den Dieb gilt jetzt, sobald ein Wolf in der Tasche ist; Heulen lauter.
Aufruf: python3 tools/patch399.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
rep('''|| true) return;   /* V394: Sniper/Tesla nicht mehr gegen den Dieb */''', '''|| !(S.wolves > 0)) return;   /* V%d: Trefferzone für den Wolf */''' % NEW)
rep('''const a = new Audio("sfx/wolf.mp3"); a.volume = Math.min(1, 3.6 * Math.pow(SFX.vol || 0.3, 2)) * (SFX.ch ? SFX.ch("f") : 1);''',
    '''const a = new Audio("sfx/wolf.mp3"); a.volume = Math.min(1, Math.max(0.6, 8 * Math.pow(SFX.vol || 0.3, 2)));''')
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
