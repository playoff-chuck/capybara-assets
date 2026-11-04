"""V216: Ebenen oben: Buchhalter-Bericht ganz oben, darunter Boss-Signal (bleibt länger), darunter Wellen-Nummer."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('const GAME_VER = "V215";') == 1
s = s.replace('const GAME_VER = "V215";', 'const GAME_VER = "V216";')
css = '''<style id="v216">
#waveNum{z-index:43!important}
#hackPill{z-index:940!important}
#book,.book{z-index:960!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
