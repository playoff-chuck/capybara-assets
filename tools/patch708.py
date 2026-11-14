import sys
# V708: Vibration standardmäßig AUS (Martin 14.11.2026 15:33); einschalten im Pause-Menü «Vibration: on».
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V707";', 'const GAME_VER = "V708";')
rep('let on = LS.get("tarnturm-vib") !== "0";', 'let on = LS.get("tarnturm-vib") === "1";   /* V708: standardmäßig aus */')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
