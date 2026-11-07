"""V390: Boss-Hack und Gratis-Shop tauschen (Martin, 07.11.):
- Erster Boss-Hack nach W4 → erscheint in W5 (HK_WAVES 8 → 4).
- Ten-ton wird erst in W8 freigeschaltet (statt W5); seine Gratis-Vorstellung fällt mit dem Air Drop W8 zusammen,
  in W5 gibt es keinen Gratis-Shop mehr.
Aufruf: python3 tools/patch390.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
rep('const HK_WAVES = new Set([8, 12, 18,', 'const HK_WAVES = new Set([4, 12, 18,')
n = s.count('"ton": 5, "chomp"'); assert n >= 1, n
s = s.replace('"ton": 5, "chomp"', '"ton": 8, "chomp"'); print("unlock-Stellen", n)
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
