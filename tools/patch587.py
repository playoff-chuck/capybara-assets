#!/usr/bin/env python3
# V587 (Martin 11.11. 01:26–01:29): Tutorial
# - Kurs-Streifen: «TUTORIAL»-Titel weg, General oben links doppelt so groß; die Aufgabenkarte ist seine Sprechblase
#   (Zipfel zeigt nach oben auf den General)
# - Lektion «Monster plätten»: der Stein kommt gleich passend über einem Monster (bevorzugt rechte Seite) – nur noch DROP drücken
# - Lektion 9 (und überhaupt bis zur Urkunde): keine Rosie/Blue-Figur beim Einsatz eines Specials (buddyHelp), Missions-Zähler bleibt
# - (01:31) Kleine «Got it/Понятно»-Knöpfe im Tutorial weg (Lektionen gehen über ihre Bedingung/Zeit weiter)
# - (01:32) Der fallende Block ist auch beim Abdunkeln ganz zu sehen (über Dunkel, Karte und Streifen), damit man ihn drehen kann
# - Urkunde: Spruch in Martins Stimme (HeyGen «Martin 4min»), Schlüssel cert_done
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V586";', 'const GAME_VER = "V587";')

# Spruch zur Urkunde
rep('const VOICE_TEXT = {"weed_warn": ', 'const VOICE_TEXT = {"cert_done": "Congratulations! You\'ve graduated from the Capybara Academy. All the best on your path through life!", "weed_warn": ')
rep('window.__certNow = () => { window.__tutSumPend = 0; window.__tutSumNow = false; window.__tutSumOpen = true; S.coachHold = true;',
    'window.__certNow = () => { window.__tutSumPend = 0; window.__tutSumNow = false; window.__tutSumOpen = true; S.coachHold = true; setTimeout(() => { try { SFX.say("cert_done", 1, 1, "cert_done"); } catch (e) {} }, 1200);   /* V587: Martins Spruch */')

# keine Helfer-Figur bis zur Urkunde
rep('''function buddyHelp(kind) { try { window.__msnEv && window.__msnEv("use_" + kind); } catch (e) {}
  const el = document.getElementById("buddy"), q = BUDDY_SAY[kind]; if (!el || !q) return;''',
'''function buddyHelp(kind) { try { window.__msnEv && window.__msnEv("use_" + kind); } catch (e) {}
  try { if ((typeof TUT !== "undefined" && TUT.on) || window.__tutSumPend || window.__tutSumNow || window.__tutSumOpen) return; } catch (e) {}   /* V587: bis zur Urkunde keine Figur */
  const el = document.getElementById("buddy"), q = BUDDY_SAY[kind]; if (!el || !q) return;''')

# Lektion «Monster plätten»: Stein über einem Monster
rep('''  try { if (TUT.on && TUT_STEPS[TUT.step] && /FILL A ROW/.test(TUT_STEPS[TUT.step].t) && !S.rotMode) {''',
'''  try { if (TUT.on && TUT_STEPS[TUT.step] && /SPLAT THEM/.test(TUT_STEPS[TUT.step].t) && !S.rotMode) { const b = tutSplatPlace(); if (b) { S.piece = makePiece(b.k); S.piece.tnt = -1; S.piece.cells = b.cells; S.piece.x = b.px; S.piece.__auto = S.piece.x + "," + JSON.stringify(S.piece.cells); } } } catch (e) {}   /* V587 */
  try { if (TUT.on && TUT_STEPS[TUT.step] && /FILL A ROW/.test(TUT_STEPS[TUT.step].t) && !S.rotMode) {''')
rep('function tutRowKey() {   /* V586',
'''function tutSplatPlace() {   /* V587: Stein, der beim DROP ein Monster trifft (rechte Seite bevorzugt) */
  const W = VW(), mons = (S.monsters || []).filter(m => !m.dead); if (!mons.length) return null;
  let best = null, bs = -1;
  for (const m of mons) { const tg = new Set([Math.round(m.cx) + "," + Math.round(m.cy), Math.round(m.x) + "," + Math.round(m.y)]); if (m.next) tg.add(m.next[0] + "," + m.next[1]);
    for (const k of KEYS) { let cells = SHAPES[k].c.map(p => p.slice());
      for (let r = 0; r < 4; r++) { if (r) cells = rotCells(k, cells);
        for (let px = -3; px < W + 3; px++) { if (collide(cells, px, 0)) continue; let py = 0; while (!collide(cells, px, py + 1)) py++;
          const hit = cells.some(([x, y]) => tg.has((px + x) + "," + (py + y))); if (!hit) continue;
          const sc = 1000 + (m.cx >= W / 2 ? 500 : 0) + (k === "I" ? 50 : 0) + py + Math.random(); if (sc > bs) { bs = sc; best = { k, cells: cells.map(c => c.slice()), px }; } } } } }
  return best; }
function tutRowKey() {   /* V586''')

# Streifen: General groß, kein Titel; Karte = Sprechblase des Generals
CSS = r'''<style id="v587">
#tutBar .tbMain{display:grid!important;grid-template-columns:auto 1fr;grid-template-rows:auto auto;column-gap:10px;align-items:center}
#tutBar .tbHead{display:contents!important}
#tutBar .tbHead b{display:none!important}
#tutBar .tbLogo{grid-column:1;grid-row:1/3;width:60px!important;height:60px!important;border-radius:14px!important;border-width:3px!important;box-shadow:0 3px 0 #3a2414!important}
#tutBar .tbHead span{grid-column:2;grid-row:1;justify-self:end}
#tutBar .tbMain{grid-template-columns:auto minmax(0,1fr)!important}
#tutBar .tbTrack{grid-column:2;grid-row:2;margin-top:2px!important;min-width:0}
#tutBar .tbDot{width:min(30px,calc((100vw - 104px) / 10.8))!important;height:min(30px,calc((100vw - 104px) / 10.8))!important}
body.tutBarOn #coach.genTalk .coachCard::before{left:var(--tbTail,18px)!important;top:-15px!important;width:24px!important;height:16px!important;clip-path:polygon(0 100%,50% 0,100% 100%)!important}
body.tutBarOn #coach.genTalk .coachCard::after{left:calc(var(--tbTail,18px) + 5px)!important;top:-9px!important;width:14px!important;height:11px!important;clip-path:polygon(0 100%,50% 0,100% 100%)!important}
</style>
'''
rep('</body>', CSS + '</body>')
rep('/* V584: neue Aufgabe – 3 s alles dunkel',
'''/* V587: Zipfel der Aufgabenkarte zeigt auf den General im Streifen */
setInterval(() => { try { if (!document.body.classList.contains("tutBarOn")) return; const card = document.querySelector("#coach .coachCard"), lg = document.querySelector("#tutBar .tbLogo"); if (!card || !lg) return;
  const c = card.getBoundingClientRect(), l = lg.getBoundingClientRect(); if (!c.width) return; const x = Math.max(10, Math.min(c.width - 34, l.left + l.width / 2 - c.left - 12)); card.style.setProperty("--tbTail", Math.round(x) + "px"); } catch (e) {} }, 250);
/* V584: neue Aufgabe – 3 s alles dunkel''')
# keine Got-it-Knöpfe im Tutorial
rep('$("coachSkip").hidden = !last;   /* V584: kein «Skip» oben rechts */', '$("coachSkip").hidden = true;   /* V584/V587: kein Skip und kein «Got it» im Kurs */')
# Block beim Abdunkeln sichtbar
rep('    ox.clearRect(0, 0, W, H); shown = true; if (S.tutDimT > performance.now()) return;   /* V584 */\n',
    '    ox.clearRect(0, 0, W, H); shown = true; const dimNow = S.tutDimT > performance.now();   /* V587: Block bleibt sichtbar */\n')
rep('      if (!over(x0, y0, w, h, cr) && !over(x0, y0, w, h, br)) continue;',
    '      if (!dimNow && !over(x0, y0, w, h, cr) && !over(x0, y0, w, h, br)) continue;')
# Monster-Lektion: Stein folgt dem Monster, solange der Spieler ihn nicht bewegt hat
rep('function tutRowKey() {   /* V586',
"""setInterval(() => { try { if (!(TUT.on && S && S.piece && TUT_STEPS[TUT.step] && /SPLAT THEM/.test(TUT_STEPS[TUT.step].t) && !S.rotMode)) return; const p = S.piece;
  const sg = p.x + "," + JSON.stringify(p.cells); if (p.__auto && p.__auto !== sg) return;   // Spieler hat bewegt/gedreht
  const b = tutSplatPlace(); if (!b || collide(b.cells, b.px, p.y)) return; if (b.k !== p.k) return; p.cells = b.cells; p.x = b.px; p.__auto = p.x + "," + JSON.stringify(p.cells); } catch (e) {} }, 300);   /* V587 */
function tutRowKey() {   /* V586""")

open(dst, "w", encoding="utf-8").write(s)
print("ok V587")
