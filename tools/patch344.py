"""V344 (Martin 07.11. 00:05): Dieb sagt nach dem Diebstahl nur «thank you!» (aus Lach-Variante 4, tiefer + leiser) statt «Heh heh heh»."""
import sys, re, base64, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V343";', 'const GAME_VER = "V344";')
VD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'voice')
b = base64.b64encode(open(os.path.join(VD, 'thief_thanks.mp3'), 'rb').read()).decode()
s, n = re.subn(r'"thief_laugh":"[A-Za-z0-9+/=]+"', '"thief_laugh":"' + b + '"', s); assert n == 1, n
rep('"thief_laugh": "Heh heh heh heh...", ', '"thief_laugh": "Thank you!", ')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
