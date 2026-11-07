"""V403: weitere Suno-Musik (Martin, 07.11.): Antarktis + Frozen Retro Groove, Glide on the Ice (jetzt 4 Stücke, je Ort 3 im Wechsel);
Nordamerika + Midtown Shuffle (80er Disco, jetzt 5 Stücke). Odd-Phased kam doppelt – nicht nochmal eingebaut.
Aufruf: python3 tools/patch403.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
rep('''icea: ["Polar Night", 90], iceb: ["Ice Shelf", 90] };''', '''icea: ["Polar Night", 90], iceb: ["Ice Shelf", 90], frozenretro: ["Frozen Retro Groove", 116], glide: ["Glide on the Ice", 112], midtown: ["Midtown Shuffle", 120] };''')
rep('''icea: "an_ice_a", iceb: "an_ice_b" };''', '''icea: "an_ice_a", iceb: "an_ice_b", frozenretro: "an_frozen_retro", glide: "an_glide", midtown: "na_midtown" };''')
rep('''TRK_NA = ["dorian", "oddphased", "gameloop", "cartoon"], TRK_AN = ["icea", "iceb"];''', '''TRK_NA = ["dorian", "midtown", "oddphased", "gameloop", "cartoon"], TRK_AN = ["icea", "frozenretro", "iceb", "glide"];''')
rep('''if (wave >= 91 && wave <= 120) return [0, 1, 2].map(i => TRK_NA[(p + i) % 4]); if (wave >= 121) return TRK_AN.slice();''',
    '''if (wave >= 91 && wave <= 120) return [0, 1, 2].map(i => TRK_NA[(p + i) %% 5]); if (wave >= 121) return [0, 1, 2].map(i => TRK_AN[(p + i) %% 4]);   /* V%d */''' % NEW)
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
