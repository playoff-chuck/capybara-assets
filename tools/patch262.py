"""V262 (Martin 05.11. 14:11–14:15):
- Doppeldecker: Propeller dreht sich (Blatt rotiert + Unschärfe-Scheibe), Capybara im Cockpit wackelt leicht im Wind
  (Bild in Rumpf- und Capybara-Ebene geteilt: img/biplane_body.webp, img/biplane_cap.webp).
- Shop/Turm-Menü: Knöpfe unten etwas höher, damit der schwarze Schatten ganz zu sehen ist.
- Lucky Supply: Fenster kompakter – leerer Rand unter dem Automaten weg (img/bandit_cab3.webp), Ergebnis-Zeile liegt jetzt
  auf dem Automaten, SPIN-Knopf direkt darunter.
- Hänger-Schutz Neuheiten-Fenster/Anzeigen: GOT IT schließt das Fenster immer; bleibt das Spiel ohne sichtbares Fenster
  im Intro-Zustand hängen, löst es sich nach 3 s selbst."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V261";', 'const GAME_VER = "V262";')
rep('function closeIntro() { clearTimeout(introT); if (!S.intro || S.joinOpen) return;',
    'function closeIntro() { clearTimeout(introT); if (S.joinOpen) return; if (!S.intro) { $("ovIntro").hidden = true; document.body.classList.remove("introWin"); return; }')
rep('class="mapPlane"><img class="biPlane" src="img/biplane.webp" alt=""></div>',
    'class="mapPlane"><div class="biPlane"><img class="bpCap" src="img/biplane_cap.webp" alt=""><img class="bpBody" src="img/biplane_body.webp" alt=""><i class="bpDisc"></i><i class="bpProp"></i><i class="bpHub"></i></div></div>')
# Bandit
rep('<img class="bdCabImg" src="img/bandit_cab2.webp"', '<img class="bdCabImg" src="img/bandit_cab3.webp"')
n = s.count('top:43.5%;width:19.2%;height:17.4%'); assert n == 3, n
s = s.replace('top:43.5%;width:19.2%;height:17.4%', 'top:47.9%;width:19.2%;height:19.16%')
rep('.bdCab{aspect-ratio:600/881!important;width:min(100%,calc((100vh - 270px) * .681))!important}', '.bdCab{aspect-ratio:600/800!important;width:min(100%,calc((100vh - 230px) * .75))!important}')
rep('.bdCab .bdLever{left:82%!important;top:36%!important;width:18%!important;height:42%!important}', '.bdCab .bdLever{left:82%!important;top:39.6%!important;width:18%!important;height:46.3%!important}')
css = r'''
<style id="v262">
.biPlane{position:relative;width:86px!important;height:59.5px!important}
.biPlane img{position:absolute;display:block}
.biPlane .bpBody{left:0;top:0;width:100%;height:100%}
.biPlane .bpCap{left:43.08%;top:6.67%;width:28.46%;height:38.89%;transform-origin:50% 95%;animation:bpCap 1.1s ease-in-out infinite alternate}
.biPlane .bpDisc{position:absolute;left:6.2%;top:55.6%;width:7px;height:64%;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(ellipse at center,rgba(236,214,170,.55),rgba(236,214,170,.18) 60%,rgba(236,214,170,0) 72%)}
.biPlane .bpProp{position:absolute;left:6.2%;top:55.6%;width:5px;height:64%;margin:-19px 0 0 -2.5px;border-radius:3px;background:linear-gradient(180deg,#a7804c,#f0d9a6 20%,#c49b5d 48%,#c49b5d 52%,#f0d9a6 80%,#a7804c);animation:bpSpin .11s linear infinite}
.biPlane .bpHub{position:absolute;left:6.2%;top:55.6%;width:6px;height:8px;margin:-4px 0 0 -3px;border-radius:50% 40% 40% 50%;background:radial-gradient(circle at 35% 35%,#f6e3b8,#b08550 70%);box-shadow:0 0 0 1px rgba(80,55,25,.35)}
@keyframes bpSpin{0%{transform:scaleY(1)}25%{transform:scaleY(.12)}50%{transform:scaleY(-1)}75%{transform:scaleY(-.12)}100%{transform:scaleY(1)}}
@keyframes bpCap{0%{transform:rotate(-4deg) translateY(0)}50%{transform:rotate(1deg) translateY(-.6px)}100%{transform:rotate(4deg) translateY(.3px)}}
@media (prefers-reduced-motion:reduce){.biPlane .bpCap{animation:none}.biPlane .bpProp{animation-duration:.4s}}
#sheetIn .sheetFoot{padding-bottom:calc(12px + env(safe-area-inset-bottom,0px))!important}
#ovBandit .bdRes{position:absolute;left:12%;right:12%;bottom:31%;height:auto;min-height:0;margin:0!important;padding:6px 8px;border-radius:14px;z-index:4;pointer-events:none}
#ovBandit.win .bdRes{background:rgba(255,246,230,.94);box-shadow:0 0 0 3px #3a2a1a,0 6px 14px rgba(0,0,0,.3)}
#ovBandit #bdGo{margin-top:8px}
</style>
'''
js = r'''
  /* V262: Ergebnis-Zeile auf den Automaten; Intro-Hänger-Schutz */
  try { const res = document.querySelector("#ovBandit .bdRes"), cab = document.getElementById("bdCab"); if (res && cab) cab.appendChild(res); } catch (e) {}
  try { let stuck = 0; setInterval(() => { try {
      if (!S || !S.intro || S.joinOpen || S.signOpen || S.banditOpen || S.over) { stuck = 0; return; }
      const oi = document.getElementById("ovIntro"), oa = document.getElementById("ovAd");
      const vis = el => el && !el.hidden && getComputedStyle(el).display !== "none";
      if (vis(oi) || document.body.classList.contains("introWin") || vis(oa)) { stuck = 0; return; }
      if (++stuck >= 6) { stuck = 0; S.intro = false; S.adOpen = false; console.warn("intro unstuck"); }
    } catch (e) {} }, 500); } catch (e) {}
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
