"""V289 (Martin 17:16 / 17:21 / 17:26):
- Nuts-Endscreen: Bild oben (img/nuts_chase.webp – Rosie und Blue fliehen vor verrückten Monstern), nur noch zwei Schriften
  (Bangers für Titel/Zahl, «Baloo 2» für alles andere), Kopfzeile «NUTS DETOUR · FIRST TRY» schwarz auf dem Hintergrund statt roter Kasten.
- Boss-Hack-Einsatz: Bild oben (img/hk_bet.webp – Blue schiebt Goldchips zum Boss).
- Ankunftsbild (Welttour-Start und Kontinente) wächst aus dem Landepunkt und schrumpft am Ende wieder in den Punkt hinein."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V288";', 'const GAME_VER = "V289";')
rep('ovRes.innerHTML = `<div class="nutsResBox"><span class="alTag" id="nrTag">', 'ovRes.innerHTML = `<div class="nutsResBox"><div class="nrPic"></div><span class="alTag" id="nrTag">')
rep('''        <div class="hackBet" id="hackBet">
          <span class="alTag hackTag">BOSS SIGNAL</span>''', '''        <div class="hackBet" id="hackBet"><div class="hkBetPic"></div>
          <span class="alTag hackTag">BOSS SIGNAL</span>''')
rep('      at(12600, hide); }', '      at(11000, () => { try { arrC && arrC.classList.remove("on"); } catch (e) {} });\n      at(12600, hide); }')
rep('      at(10600, hide); }', '      at(9000, () => { try { arr && arr.classList.remove("on"); } catch (e) {} });\n      at(10600, hide); }')
css = r'''
<style id="v289">
/* Nuts-Endscreen: Bild, zwei Schriften */
.nutsResBox{padding:0 0 16px!important;overflow:auto;font-family:"Baloo 2",system-ui,sans-serif!important}
.nutsResBox .nrPic{aspect-ratio:960/536;max-width:100%;background:url(img/nuts_chase.webp) center/cover;border-bottom:3px solid #3a1d10;border-radius:13px 13px 0 0;margin-bottom:10px}
.nutsResBox>*:not(.nrPic){margin-left:14px!important;margin-right:14px!important}
.nutsResBox>button{width:calc(100% - 28px)!important}
.nutsResBox .alTag{display:block;background:none!important;color:#3a1d10!important;font:400 15px/1 Bangers,var(--f-display),sans-serif!important;letter-spacing:.14em!important;padding:0!important;border:0!important;box-shadow:none!important}
.nutsResBox h2{font-size:38px!important;line-height:1!important;color:#e0453a!important;-webkit-text-stroke:1.2px #3a1d10;margin:6px 14px 0!important;letter-spacing:.02em}
.nutsResBox .big{font-size:52px!important;color:#3a1d10;margin:2px 14px!important}
.nutsResBox p,.nutsResBox .hs,.nutsResBox .hs *{font-family:"Baloo 2",system-ui,sans-serif!important}
.nutsResBox p{font-size:14px!important;font-weight:600}
.nutsResBox .bonus{font-weight:800!important;font-size:14px!important;border-radius:12px!important}
.nutsResBox .hs h4{font:400 17px/1 Bangers,var(--f-display),sans-serif!important;letter-spacing:.06em;margin:4px 0 6px!important;color:#3a1d10}
.nutsResBox .hs .row{font-size:14px;font-weight:700}
/* Boss-Hack-Einsatz: Bild */
.hackBet{padding-top:0!important;overflow:hidden}
.hackBet .hkBetPic{align-self:stretch;aspect-ratio:960/536;max-width:calc(100% + 28px);margin:0 -14px 2px;background:url(img/hk_bet.webp) center/cover;border-bottom:3px solid var(--ink,#3a1d10)}
</style>
'''
i = s.rindex('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
