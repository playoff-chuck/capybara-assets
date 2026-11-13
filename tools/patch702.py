# V702 (Martin 13.11. 13:00): Konfetti im Hack-Ergebnis stand im Leicht-Modus/ohne Animation als Punktreihe oben fest -> dann ausblenden.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep('GAME_VER = "V701"', 'GAME_VER = "V702"')
rep('@media (prefers-reduced-motion: reduce){.hackRes .hkArt svg,.hkConf i,.hkArt .smoke,.hkArt .coinfly{animation:none}}',
    '@media (prefers-reduced-motion: reduce){.hackRes .hkArt svg,.hkConf i,.hkArt .smoke,.hkArt .coinfly{animation:none}.hkConf{display:none!important}}\nbody.lite .hkConf{display:none!important}   /* V702: stehendes Konfetti = Punktreihe oben, deshalb weg */')
open(dst, "w", encoding="utf8").write(s)
print("ok V702")
