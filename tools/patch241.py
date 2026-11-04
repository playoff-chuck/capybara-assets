"""V241: Neues Schlussbild «World tour complete» (fin/finale2.webp, breit 16:9): Rosie & Blue jubeln auf dem
Camo-Turm, Eisfestung, Globus mit Reiseroute, Feuerwerk, rosa Wasserflugzeug. Bild wird nicht mehr beschnitten."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V240";', 'const GAME_VER = "V241";')
n = s.count('fin/finale.webp'); assert n >= 1; s = s.replace('fin/finale.webp', 'fin/finale2.webp')
css = '''<style id="v241">
.finImg{aspect-ratio:16/9;height:auto!important;max-height:26vh;object-fit:cover;object-position:50% 45%!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok', n)
