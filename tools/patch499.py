#!/usr/bin/env python3
"""V499 (Martin 09.11. 11:57):
1) Air-Drop-Tutorial: nach dem ersten geschenkten Ten-ton (Welle 8) führt der General Schritt für Schritt:
   SHOP antippen → USE beim Ten-ton antippen. Einmal pro Gerät (capy-tut-ton), «Skip» sofort möglich.
2) Elite-Turm (Partner bringt den Laser): im Turm-Menü Sticker «MAX · LASER», auf dem Feld beim Turm Bild des Partners + Sticker «MAX».
   Läuft der Laser ab oder ist der Turm weg, verschwindet beides (wird nur bei eliteT > 0 gezeichnet).
Aufruf: python3 tools/patch499.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V498";', 'const GAME_VER = "V499";')

# --- 1) Ten-ton-Tutorial ---
rep('function hintEnd() { if (!hintKey) return; hintKey = null;',
    'function hintEnd() { if (!hintKey) return; if (hintKey === "tontut") { TONTUT.st = 0; LS.set("capy-tut-ton", "1"); $("coach").classList.remove("tt2"); document.querySelectorAll(".ttPulse").forEach(x => x.classList.remove("ttPulse")); } hintKey = null;')
rep('function showCamp(action, label) { tutAbort();',
    '''/* V499: Air-Drop-Tutorial – wie setzt man den geschenkten Ten-ton ein? */
const TONTUT = { st: 0 };
function tonTutCard(title, sub, el) { const c = $("coach"), a = $("coachArrow"), card = c.querySelector(".coachCard"); c.hidden = false; c.classList.toggle("tt2", TONTUT.st === 2); document.querySelectorAll(".ttPulse").forEach(x => x.classList.remove("ttPulse")); if (TONTUT.st === 2 && el) el.classList.add("ttPulse");
  $("coachStep").textContent = "AIR DROP"; $("coachT").textContent = title; $("coachS").textContent = sub; $("coachSkip").textContent = "Skip"; $("coachSkip").classList.remove("wait"); coachHi(el);
  const br = $("board").getBoundingClientRect();
  if (el) { const r = el.getBoundingClientRect(), below = r.top < window.innerHeight * 0.5; a.style.display = "block"; a.textContent = below ? "▲" : "▼"; a.style.left = (r.left + r.width / 2) + "px";
    if (below) { a.style.top = (r.bottom + 4) + "px"; card.style.bottom = ""; card.style.top = (r.bottom + 40) + "px"; } else { a.style.top = (r.top - 34) + "px"; card.style.bottom = ""; card.style.top = (br.top + 6) + "px"; } }
  else { a.style.display = "none"; card.style.bottom = ""; card.style.top = (br.top + 6) + "px"; } }
function tonTutTick() { try {
  if (!S || !S.started || S.over || S.nuts || S.testRun || S.replay) { if (TONTUT.st && hintKey === "tontut") { hintKey = null; S && (S.coachHold = false); $("coach").hidden = true; coachHi(null); TONTUT.st = 0; } return; }
  if (!TONTUT.st) {
    if (LS.get("capy-tut-ton") === "1" || !(S.tons > 0) || !S.tonGift || !Object.keys(S.tonGift).length || TUT.on || hintKey || S.ton) return;
    if (uiWinOpen() || S.drop || S.shop || S.paused || S.mapShow || S.ordersOpen || S.intro || S.adOpen || S.mode || S.sel) return;
    if (window.__tipBulb && window.__tipBulb.open) return;
    hintKey = "tontut"; TONTUT.st = 1; S.coachHold = true;
    tonTutCard("USE YOUR AIR DROP", "Your Ten-ton drop is waiting in the SHOP. Tap SHOP.", $("bBuild")); snd("radio"); return; }
  if (S.ton) { hintEnd(); toast("NICE DROP! · keep the next one for a high stack", "HQ", 2400); try { SFX.say("Nice!"); } catch (e) {} return; }
  const pk = S.shop && $("sheetIn").classList.contains("pk"), btn = pk ? document.querySelector('#sheetIn [data-pocket="ton"]') : null;
  if (TONTUT.st === 1 && btn) { TONTUT.st = 2; try { btn.scrollIntoView({ block: "center" }); } catch (e) {} setTimeout(() => { if (TONTUT.st === 2) tonTutCard("DROP IT!", "Tap USE at the Ten-ton drop. It crushes monsters and squeezes your stack to half.", btn); }, 250); }
  else if (TONTUT.st === 2 && !pk) { TONTUT.st = 1; tonTutCard("USE YOUR AIR DROP", "Your Ten-ton drop is waiting in the SHOP. Tap SHOP.", $("bBuild")); }
} catch (e) {} }
setInterval(tonTutTick, 400);
window.__tonTut = { tick: tonTutTick, get st() { return TONTUT.st; } };
function showCamp(action, label) { tutAbort();''')

# --- 2) Elite-Turm: Sticker + Partnerbild ---
rep('h += `<div class="eliteTag"><img src="${HERO_IMG[buddyKey()]}" alt=""><div><b>ELITE TOWER</b>',
    'h += `<div class="eliteTag"><em class="maxSt">MAX · LASER</em><img src="${HERO_IMG[buddyKey()]}" alt=""><div><b>ELITE TOWER</b>')
rep('ctx.strokeText("ELITE", cx, cy - s * 0.62); ctx.fillStyle = "#ffd84d"; ctx.fillText("ELITE", cx, cy - s * 0.62); ctx.restore(); }   /* V379 */',
    'ctx.restore(); }   /* V379 · V499: Text durch Sticker + Partnerbild ersetzt (nach dem Turm gezeichnet) */')
rep('    if (drawTowSprite(ctx, t, cx, cy, s)) { if (heightBonus(t) >= 0.5) {',
    '    if (t.eliteT > 0) S._eliteDraw = (S._eliteDraw || []).concat([[t, cx, cy]]);   /* V499 */\n    if (drawTowSprite(ctx, t, cx, cy, s)) { if (heightBonus(t) >= 0.5) {')
# nach der Turm-Schleife zeichnen: Hook in drawOfx-unabhängigen Teil – direkt vor dem Zeichnen der Effekte
rep('function drawOfx(f, k, s, g2) {',
    '''const ELITE_PIC = {};
function eliteBadges(s) { const L = S._eliteDraw; S._eliteDraw = null; if (!L) return;   /* V499: Partnerbild + MAX-Sticker am Elite-Turm */
  const src = HERO_IMG[buddyKey()]; let im = ELITE_PIC[src]; if (!im) { im = new Image(); im.src = src; ELITE_PIC[src] = im; }
  for (const [t, cx, cy] of L) { if (!(t.eliteT > 0) || !S.towers.has(t.y * GW + t.x)) continue; const al = Math.min(1, t.eliteT / 2);
    ctx.save(); ctx.globalAlpha = al;
    if (im.complete && im.naturalWidth) { const z = s * 0.95, k = Math.min(z / im.naturalWidth, z / im.naturalHeight), w = im.naturalWidth * k, h = im.naturalHeight * k; ctx.shadowColor = "rgba(0,0,0,.4)"; ctx.shadowBlur = s * 0.12; ctx.drawImage(im, cx + s * 0.2, cy - s * 0.5 - h * 0.85, w, h); ctx.shadowBlur = 0; }
    ctx.translate(cx - s * 0.18, cy - s * 0.66); ctx.rotate(-0.2); const fz = Math.max(9, s * 0.34); ctx.font = `400 ${fz}px Bangers,system-ui,sans-serif`; const tw = ctx.measureText("MAX").width, pw = tw + fz * 0.7, ph = fz * 1.15;
    ctx.fillStyle = "#ff2f8a"; ctx.strokeStyle = "#3a2414"; ctx.lineWidth = Math.max(1.5, s * 0.07); ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(-pw / 2, -ph / 2, pw, ph, ph * 0.3); else ctx.rect(-pw / 2, -ph / 2, pw, ph); ctx.fill(); ctx.stroke();
    ctx.fillStyle = "#fff"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("MAX", 0, fz * 0.04); ctx.restore(); } }
function drawOfx(f, k, s, g2) {''')
rep('ctx.fillText("+", cx, cy + s * 0.02); }\n  }\n  // Monster\n  const now = performance.now();',
    'ctx.fillText("+", cx, cy + s * 0.02); }\n  }\n  try { eliteBadges(s); } catch (e) {}   /* V499 */\n  // Monster\n  const now = performance.now();')
rep('.eliteTag i{font-style:normal;font-size:26px;line-height:1}',
    '.eliteTag i{font-style:normal;font-size:26px;line-height:1}.eliteTag{position:relative}html body #coach.tt2,html body #coach.tt2 .coachCard,html body #coach.tt2 .coachArrow{visibility:visible!important}html body #coach.tt2{z-index:9999!important}html body #coach.tt2 .coachCard{background:#fff7e8!important;border:3px solid #3a2414!important;box-shadow:0 4px 0 #3a2414!important}html body #coach.tt2 #coachT{color:#3a2414!important}html body #coach.tt2 #coachS{color:#5a4030!important}.ttPulse{animation:ttP .7s ease-in-out infinite alternate;outline:3px solid #ff2f8a;outline-offset:2px}@keyframes ttP{from{transform:scale(1)}to{transform:scale(1.12)}}.eliteTag .maxSt{position:absolute;right:-8px;top:-14px;background:#ff2f8a;color:#fff;font:400 15px/1 var(--f-display,"Bangers",sans-serif);font-style:normal;letter-spacing:.05em;padding:4px 8px 3px;border:2.5px solid #3a2414;border-radius:8px;transform:rotate(8deg);box-shadow:0 2px 0 #3a2414;z-index:1}')
open(p, "w", encoding="utf-8").write(s); print("ok V499")
