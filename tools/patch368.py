"""V368 (Martin 07.11. 08:17): Pokal im Hauptmenü – das Fenster stimmte nicht.
Hall of fame blendete das ganze Hauptmenü aus (Logo und Ton-Knopf sprangen, Symbolleiste weg, anderer Hintergrund).
Jetzt öffnet es wie Settings als Karte über dem stehenden Menü – nichts verschiebt sich; lange Listen scrollen in der Karte."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V367";', 'const GAME_VER = "V368";')
i = s.index('<div class="overlay win" id="ovHs" hidden>'); j = s.index('</div>', s.index('id="hsNuts"')) + len('</div>')
old = s[i:j]; k = old.index('<button class="xBtn" id="btnHsClose"'); btn = old[k:old.index('</button>', k) + len('</button>')]
assert old.count('<h2>HALL OF FAME</h2>') == 1
rep(old, '<div class="overlay joinOv" id="ovHs" hidden><div class="joinBox hsBox">\n        ' + btn +
    '\n        <div class="alHead"><span class="alTag">HALL OF FAME</span><span></span></div>\n        <div class="hs" id="hsList"></div><div class="hs" id="hsNuts"></div>\n      </div>')
rep('#ovSettings{z-index:65}', '#ovSettings{z-index:65}#ovHs{z-index:65}#ovHs .hsBox{max-height:min(64vh,540px);overflow-y:auto}#ovHs .hs{width:100%}')
rep('$("ovStart").hidden = true; $("ovHs").hidden = false;', '$("ovHs").hidden = false;   /* V368: Menü bleibt stehen, Hall of fame als Karte darüber */')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
