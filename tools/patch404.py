"""V404: Nordamerika + Miami Vice Loop (80er, Martin 07.11.) → 6 Stücke, je Ort 3 im Wechsel.
Aufruf: python3 tools/patch404.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
rep('''midtown: ["Midtown Shuffle", 120] };''', '''midtown: ["Midtown Shuffle", 120], miami: ["Miami Nights", 118] };''')
rep('''midtown: "na_midtown" };''', '''midtown: "na_midtown", miami: "na_miami" };''')
rep('''TRK_NA = ["dorian", "midtown", "oddphased", "gameloop", "cartoon"]''', '''TRK_NA = ["dorian", "midtown", "oddphased", "miami", "gameloop", "cartoon"]''')
rep('''TRK_NA[(p + i) % 5]''', '''TRK_NA[(p + i) % 6]''')
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
