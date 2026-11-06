"""V352 (Martin 07.11. 00:35): Easter Egg gibt 1000 Gold statt 5000 Punkte (Anzeige «+1000 GOLD»)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V351";', 'const GAME_VER = "V352";')
rep('<span>+5000</span>', '<span>+1000 GOLD</span>')
rep('S.eggBonus = (S.eggBonus || 0) + 5000;', 'S.gold += 1000; snd("sell");')
rep('toast("EASTER EGG · +5000 points", "HQ", 1800);', 'toast("EASTER EGG · +1000 gold", "HQ", 1800);')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
