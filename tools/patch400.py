"""V400: Suno-Musik für Nordamerika (W91–120) und Antarktis (W121–150) von Martin (07.11.):
NA: Dorian Dust, Odd-Phased, Game Loop, Cartoon Loop (je Ort 3 von 4, rotierend) · Antarktis: Ice A, Ice B.
Vorher liefen dort die Synth-Klänge.
Außerdem (Martin): höchstens ein Lob alle 15 s (vorher 1,5 s). Dateien music/na_*.mp4, music/an_*.mp4 (AAC 96k, −20 LUFS wie die anderen).
Aufruf: python3 tools/patch400.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
rep('''iceport: ["Ice Port Disco", 110], icepalace: ["Ice Palace", 120] };''', '''iceport: ["Ice Port Disco", 110], icepalace: ["Ice Palace", 120], dorian: ["Dorian Dust", 84], oddphased: ["Odd-Phased", 96], gameloop: ["Prairie Loop", 100], cartoon: ["Cartoon Trail", 110], icea: ["Polar Night", 90], iceb: ["Ice Shelf", 90] };''')
rep('''iceport: "as_iceport", icepalace: "as_icepalace" };''', '''iceport: "as_iceport", icepalace: "as_icepalace", dorian: "na_dorian_dust", oddphased: "na_odd_phased", gameloop: "na_game_loop", cartoon: "na_cartoon_loop", icea: "an_ice_a", iceb: "an_ice_b" };''')
rep('''const TRK_AF = ["oasis", "savanna", "dune", "dune2", "pyramid"], TRK_AS = ["taiga", "frozen", "steppe", "iceport", "icepalace"];''',
    '''const TRK_AF = ["oasis", "savanna", "dune", "dune2", "pyramid"], TRK_AS = ["taiga", "frozen", "steppe", "iceport", "icepalace"], TRK_NA = ["dorian", "oddphased", "gameloop", "cartoon"], TRK_AN = ["icea", "iceb"];   /* V%d */''' % NEW)
rep('''if (wave >= 61 && wave <= 90) return [0, 1, 2].map(i => TRK_AS[(p + i) % 5]);''', '''if (wave >= 61 && wave <= 90) return [0, 1, 2].map(i => TRK_AS[(p + i) % 5]);
  if (wave >= 91 && wave <= 120) return [0, 1, 2].map(i => TRK_NA[(p + i) % 4]); if (wave >= 121) return TRK_AN.slice();''')
rep('''const useTrk = w => w === 0 || (w >= 1 && w <= 90);''', '''const useTrk = w => w === 0 || (w >= 1 && w <= 150);''')
rep("if (now - lastPraise < 1500 || SFX.voiceBusy) return;", "if (now - lastPraise < 15000 || SFX.voiceBusy) return;   /* V%d: max. ein Lob je 15 s */" % NEW)
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
