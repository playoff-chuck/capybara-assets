"""V243: Schriften selbst gehostet (site/fonts, SIL Open Font License) statt live von Google Fonts – kein Abruf bei Google
mehr (Datenschutz DE/AT). Sonderwelle «Deep Desert» heißt im Spiel nur noch «Sandstorm» (Band + Dev-Menü)."""
import sys, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V242";', 'const GAME_VER = "V243";')
css = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts.css'), encoding='utf-8').read().strip()
assert css.count('@font-face') == 12 and 'gstatic' not in css
rep('''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bangers&family=Baloo+2:wght@500;700;800&family=Saira+Stencil+One&family=Barlow+Condensed:wght@500;600;700&display=swap" rel="stylesheet">
''', '''<link rel="preload" href="fonts/bangers-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/baloo2-var-latin.woff2" as="font" type="font/woff2" crossorigin>
<style id="fonts">
/* V243: Schriften liegen auf dem eigenen Server (SIL Open Font License) */
''' + css + '''
</style>
''')
assert 'fonts.googleapis.com' not in s and 'fonts.gstatic.com' not in s
rep('<span>DEEP DESERT</span><i>SANDSTORM · 52°C</i><span>DEEP DESERT</span>', '<span>SANDSTORM</span><i>NO SIGHT · 52°C</i><span>SANDSTORM</span>')
rep('["Deep Desert", "WAVE 47 · SANDSTORM", 47]', '["Sandstorm", "WAVE 47", 47]')
rep('["Deep Desert II", "WAVE 65 · RADIO SILENCE", 65]', '["Sandstorm II", "WAVE 65 · RADIO SILENCE", 65]')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
