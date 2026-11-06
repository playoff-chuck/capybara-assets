"""V346 (Martin 07.11. 00:07): Dieb-Clips («Hello… I'm just looking.» und «thank you!») mit 0,3 s Pause davor, damit der Anfang nicht abgeschnitten wird."""
import sys, re, base64, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V345";', 'const GAME_VER = "V346";')
VD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'voice')
for key, f in (("thief_hello", "thief_hello.mp3"), ("thief_laugh", "thief_thanks.mp3")):
    b = base64.b64encode(open(os.path.join(VD, f), 'rb').read()).decode()
    s, n = re.subn(r'"' + key + r'":"[A-Za-z0-9+/=]+"', '"' + key + '":"' + b + '"', s); assert n == 1, (key, n)
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
