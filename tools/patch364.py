"""V364 (Martin 07.11. 08:20): Standard-Lautstärken für neue Spieler: Musik 80 %, Stimme 60 %, Effekte 50 %
(vorher je 100 %). Gespeicherte Regler-Einstellungen (tarnturm-ch) bleiben unverändert."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V363";', 'const GAME_VER = "V364";')
rep('CH = { f: 1, v: 1, m: 1 };', 'CH = { f: 0.5, v: 0.6, m: 0.8 };   /* V364: Standard Musik 80 %, Stimme 60 %, Effekte 50 % */')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
