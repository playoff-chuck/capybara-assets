"""V244: Finale aufgeräumt. Nach Welle 150 kommt zuerst «World tour complete» – neue Orden stehen als Zeile auf der
Finale-Karte (kein Orden-Fenster mehr davor). Kein Boss-Signal und kein «Paused» nach der letzten Welle, keine
Lob-Meldungen über der Karte. Karten-Knopf im Ergebnis ohne abgeschnittenen Text («Reached <Ort> · map»)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V243";', 'const GAME_VER = "V244";')
# kein Boss-Signal nach der letzten Welle
rep('if (hkOfferWave(S.wave)) S.hackPending = S.wave;', 'if (hkOfferWave(S.wave) && S.wave < 150) S.hackPending = S.wave;')
# kein «Paused» zwischen letzter Welle und Finale-Karte
rep('want = !!(S.paused && !S.mapShow && S.started', 'want = !!(S.paused && !S.mapShow && !S.won && S.started')
rep('S.drop ? "" : S.mapShow ? "" : S.paused ? "Paused"', 'S.drop ? "" : (S.mapShow || S.won) ? "" : S.paused ? "Paused"')
# keine Meldungen über der Finale-Karte
rep('function msgTick() {\n  if (msgBusy > performance.now() || !MSGQ.length) return;',
    'function msgTick() {\n  if (S && S.won && S.over) { MSGQ.length = 0; return; }   // V244\n  if (msgBusy > performance.now() || !MSGQ.length) return;')
# Orden auf der Finale-Karte statt Fenster davor
rep('''function albTry() {
  if (!albQ.length || !$("ovGive").hidden) return;
''', '''function finMedals(ms) {   // V244
  const st = $("ovOver").querySelector(".aarStats"); if (!st || !ms.length) return;
  let box = $("finMedals"); if (!box) { box = document.createElement("div"); box.id = "finMedals"; box.innerHTML = '<small></small><div class="fmRow"></div>'; st.insertAdjacentElement("afterend", box); }
  const row = box.querySelector(".fmRow"); ms.sort((a, b) => albRank(b) - albRank(a));
  for (const m of ms) { const d = document.createElement("span"); d.className = "fm " + (m.tint || ""); d.innerHTML = `<img src="${MED_IMG[m.img]}" alt=""><b></b>`; d.querySelector("b").textContent = m.name; row.appendChild(d); }
  const n = row.children.length; box.querySelector("small").textContent = n === 1 ? "NEW MEDAL" : n > 4 ? `${n} NEW MEDALS · all in your album` : `${n} NEW MEDALS`; box.hidden = false; try { snd("powerup"); } catch (e) {}
}
function albTry() {
  if (!albQ.length || !$("ovGive").hidden) return;
  if (typeof S !== "undefined" && S && S.won) { if (!$("ovOver").hidden) finMedals(albQ.splice(0)); return; }   // V244: Finale zuerst, Orden stehen auf der Karte
''')
rep('const _g = gameOver; gameOver = function () { const r = _g.apply(this, arguments); try { ov.classList.toggle("won", !!(S && S.won));',
    'const _g = gameOver; gameOver = function () { const r = _g.apply(this, arguments); try { const fm = document.getElementById("finMedals"); if (fm) { fm.hidden = true; fm.querySelector(".fmRow").innerHTML = ""; } } catch (e) {} try { ov.classList.toggle("won", !!(S && S.won));')
# Karten-Knopf: Text passt immer
rep('b.innerHTML = PIN_SVG + `<span>You reached <b>${nice(P.place)}</b> · map</span>`;',
    'b.innerHTML = PIN_SVG + ((() => { try { return S && S.won; } catch (e) { return false; } })() ? `<span><b>Your world tour</b> · map</span>` : `<span>Reached <b>${nice(P.place)}</b> · map</span>`);')
css = '''<style id="v244">
#finMedals{align-self:stretch;box-sizing:border-box;margin:6px 0 0;padding:5px 6px 6px;background:#fff;border:3px solid #3a2414;border-radius:14px;box-shadow:0 3px 0 #3a2414;text-align:center}
#finMedals[hidden]{display:none}
#finMedals small{display:block;font:900 10px/1.2 var(--f-ui,system-ui);letter-spacing:.08em;color:#b0328c;margin-bottom:3px}
#finMedals .fmRow{display:flex;justify-content:center;gap:4px}
#finMedals .fm{display:flex;flex-direction:column;align-items:center;gap:1px;min-width:0;flex:0 1 25%}
#finMedals .fm:nth-child(n+5){display:none}
#finMedals .fm img{width:34px;height:34px;object-fit:contain;animation:fmPop .5s cubic-bezier(.2,1.5,.4,1) both}
#finMedals .fm:nth-child(2) img{animation-delay:.12s}#finMedals .fm:nth-child(3) img{animation-delay:.24s}#finMedals .fm:nth-child(4) img{animation-delay:.36s}
#finMedals .fm b{font:800 10px/1.1 var(--f-ui,system-ui);color:#3a2414;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
@keyframes fmPop{0%{transform:scale(.2) rotate(-25deg);opacity:0}100%{transform:none;opacity:1}}
#btnOMap{letter-spacing:0!important}
#ovOver.won{overflow-y:auto!important;justify-content:safe center!important}
@media (max-height:800px){#ovOver.won .finImg{max-height:16vh!important}#finMedals{padding:3px 6px 4px}#finMedals .fm img{width:28px;height:28px}}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
