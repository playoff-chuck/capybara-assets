"""V203: «GOT IT» im Neuheiten-Fenster nicht mehr in der Sprechblase, sondern kleiner rechts unten im Bild."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('const GAME_VER = "V202";') == 1
s = s.replace('const GAME_VER = "V202";', 'const GAME_VER = "V203";')
js = '''
  /* V203: GOT IT rechts unten im Bildfenster */
  try { const ov = document.getElementById("ovIntro"), ok = document.getElementById("inOk");
    const place = () => { if (ov.hidden) return; const w = ov.querySelector(".inWin"), box = ov.querySelector(".introBox"); const inWin = w && box && w.contains(box) && document.body.classList.contains("introWin");
      if (inWin) { if (ok.parentElement !== w) w.appendChild(ok); ok.classList.add("okCorner"); } else { if (box && ok.parentElement !== box) box.appendChild(ok); ok.classList.remove("okCorner"); } };
    new MutationObserver(() => requestAnimationFrame(place)).observe(ov, { attributes: true, attributeFilter: ["hidden"] });
    new MutationObserver(() => requestAnimationFrame(place)).observe(document.body, { attributes: true, attributeFilter: ["class"] }); } catch (e) {}
'''
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
css = '''<style id="v203">
.inWin{position:relative}
#inOk.okCorner{position:absolute!important;right:12px!important;bottom:12px!important;left:auto!important;top:auto!important;width:auto!important;min-width:0!important;height:42px!important;padding:0 18px!important;margin:0!important;font-size:18px!important;z-index:5;box-shadow:0 3px 0 #3a2414!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
# Zurück aus einer anderen App: nur pausieren, wenn kein Fenster (Neuheit, Shop, Hack …) offen ist –
# sonst landet man nach «GOT IT» im Pausemenü statt direkt im Spiel
a = 'document.addEventListener("visibilitychange", () => { if (document.hidden && S.started && !S.over) S.paused = true; });'
assert s.count(a) == 1
s = s.replace(a, 'document.addEventListener("visibilitychange", () => { if (document.hidden && S.started && !S.over && !["ovIntro", "sheet", "ovHack", "ovJoin", "ovCamp", "ovGive", "ovOrders", "ovWave", "ovLines", "ovKills", "ovTime", "ovPause"].some(id => { const e = document.getElementById(id); return e && !e.hidden; })) S.paused = true; });')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
