"""V227: Neues Hauptlogo A2 (Capybara mit Kanone auf hellem Camo-T-Stein) – Startbildschirm, Kopfzeile, Guide, Hall of Fame."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V226";', 'const GAME_VER = "V227";')
rep('const MAIN_LOGO = "img/logo_main.webp?v=218";', 'const MAIN_LOGO = "img/logo_main.webp?v=227";')
rep('<link rel="preload" as="image" href="img/logo_main.webp?v=218">', '<link rel="preload" as="image" href="img/logo_main.webp?v=227">')
css = '''<style id="v227">
#stLogo{width:126px!important;height:106px!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
