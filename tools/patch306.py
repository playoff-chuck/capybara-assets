"""V306: Boss-Hack-Fenster am Handy unten abgeschnitten (Martin, Screenshot 06.11. 01:12).
Ursache: #ovHack liegt im Spielfeld (#board). Wackelt/bebt das Spielfeld (transform/translate-Animation), wird das
Spielfeld zum Bezugsrahmen für position:fixed – das Fenster schrumpft auf Spielfeldgröße und wird unten abgeschnitten.
1) #ovHack beim Laden direkt an <body> hängen (immer bildschirmfüllend).
2) Während des Hacks keine Wackel-Animation am Spielfeld.
3) Karte nie höher als der Bildschirm: Bild wird bei kleiner Höhe flacher, sonst scrollt die Karte."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V305";', 'const GAME_VER = "V306";')

JS = r'''
  /* V306: Boss-Hack-Fenster nie an das (wackelnde) Spielfeld binden */
  try { const ov = document.getElementById("ovHack"); if (ov && ov.parentElement !== document.body) document.body.appendChild(ov); } catch (e) {}
'''
end = '})();\n</script>'
i = s.rindex(end)
s = s[:i] + JS + s[i:]

CSS = '''<style id="v306hack">
body.duelOn .board,body.duelOn #board,body.duelOn #boardWrap,body.duelOn .boardWrap,body.duelOn #app,body.duelOn .app{animation:none!important;transform:none!important;translate:none!important;rotate:none!important;scale:none!important}
body.duelOn #ovHack{overflow-y:auto!important;align-items:center}
#ovHack .hackBet,#ovHack .hackRes{max-height:100%;overflow-y:auto!important;flex:0 1 auto;min-height:0}
#ovHack .hackBet{gap:6px}
@media (max-height:760px){#ovHack .hackBet .hkBetPic{aspect-ratio:auto!important;height:clamp(80px,calc(100vh - 470px),200px);background-position:center 35%!important}}
@media (max-height:600px){#ovHack .hackBet p{font-size:13px;margin:0}#ovHack .hkStake b{font-size:32px!important}}
</style>
'''
i = s.rindex('</body>')
s = s[:i] + CSS + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
