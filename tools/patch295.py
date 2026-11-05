"""V295 (Martin 18:14): Shop – Kachel «Field tower» (Basis für Waffen) leichter zu finden: gleiche Größe, aber warmes Gold-Gelb
als Hintergrund und dicker dunkler Rahmen."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V294";', 'const GAME_VER = "V295";')
css = r'''
<style id="v295tower">
#sheet .shopItem:has(button[data-shop="tower"]){background:linear-gradient(180deg,#ffe9a6,#ffd36a)!important;border:3.5px solid #3a2414!important;box-shadow:0 3px 0 #3a2414!important}
#sheet .shopItem:has(button[data-shop="tower"]) .shopTxt b{color:#3a2414!important}
#sheet .shopItem:has(button[data-shop="tower"]) .shopTxt span{color:#5a3d1a!important}
#sheet .shopItem.dis:has(button[data-shop="tower"]){filter:saturate(.75)}
</style>
'''
i = s.rindex('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
