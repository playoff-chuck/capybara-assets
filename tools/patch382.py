"""V382 (Martin 07.11. 14:15): Lucky-Supply-Schild (Gewinn, z. B. «SNIPER STRIKE») verdeckte die Walzen. Jetzt unten auf dem Tarnband des Automaten."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V381";', 'const GAME_VER = "V382";')
rep('#ovBandit .bdRes{position:absolute;left:12%;right:12%;bottom:31%;',
    '#ovBandit .bdRes{position:absolute;left:12%;right:12%;bottom:3%;')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
