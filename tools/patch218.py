"""V218: Startscreen-Logo = kleiner Turm (Capybara schaut nach rechts), oben links in der Ecke, feste Größe."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('const GAME_VER = "V217";') == 1
s = s.replace('const GAME_VER = "V217";', 'const GAME_VER = "V218";')
s = s.replace('im.src = "img/logo_main.webp"', 'im.src = "img/logo_main.webp?v=218"')
s = s.replace('href="img/logo_main.webp"', 'href="img/logo_main.webp?v=218"')
css = '''<style id="v218">
#stLogo{left:calc(env(safe-area-inset-left,0px) + 6px)!important;margin-left:0!important;top:calc(env(safe-area-inset-top,0px) + 4px)!important;width:112px!important;height:102px!important;object-position:left top!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
