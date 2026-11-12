# V692 (Martin 12.11. 22:43): Boss-Hack-Niederlage als Bild – der Boss liegt mit Sonnenbrille und Karottensaft unter dem
# Sonnenschirm, Blue wäscht ihm die Füße, Rosie macht die Maniküre (img/hk_lose.webp, Nano Banana Pro). Gleiche Karte wie der Sieg.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
rep('''$("hkArt").classList.toggle("scn", win); res.classList.add("hkNew");''', '''$("hkArt").classList.add("scn"); res.classList.add("hkNew");   /* V692: auch die Niederlage als Bild */''')
rep('''    $("hkArt").innerHTML = src ? `<div class="hkWinMon"><img src="${src}" alt=""></div>` : HK_ART_LOSE; }''',
    '''    $("hkArt").innerHTML = `<div class="hkScn lose"><img class="bg" src="img/hk_lose.webp" alt=""></div>`; void src; }   /* V692: Boss lässt sich verwöhnen */''')
rep('#hkArt .hkScn .glow{', '#hkArt .hkScn.lose img.bg{object-position:50% 40%}\n#hkArt .hkScn .glow{')
rep('const GAME_VER = "V691"', 'const GAME_VER = "V692"')
open(dst, "w", encoding="utf8").write(s); print("ok", len(s))
