"""V396: Pause-Capybara auf niedrigen Bildschirmen nicht mehr oben abgeschnitten (Martin-Screenshot 07.11.).
Bei max-height 780px saß das Bild 92 px über der Karte und ragte aus dem Bild; jetzt 30 px über der Karte.
Aufruf: python3 tools/patch396.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
rep('''#ovPause .pCapy{position:absolute;left:50%;top:-58px;width:110px;height:110px;margin-left:-55px;object-fit:contain;filter:drop-shadow(0 4px 4px rgba(0,0,0,.35));pointer-events:none}''',
    '''#ovPause .pCapy{position:absolute;left:50%%;top:-58px;width:110px;height:110px;margin-left:-55px;object-fit:contain;filter:drop-shadow(0 4px 4px rgba(0,0,0,.35));pointer-events:none}
@media (max-height:780px){#ovPause .pCapy{top:-30px!important;margin-top:0!important;height:58px!important;width:58px!important;margin-left:-29px!important}#ovPause .pCard{padding-top:34px!important}}   /* V%d */''' % NEW)
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
