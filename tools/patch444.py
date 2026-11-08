#!/usr/bin/env python3
"""V444 (Martin 08.11. 12:06–12:11):
- Unkraut: zweite Warnung ist jetzt eine Karte von Blue, die bestätigt werden muss (Spiel steht): «If the weed reaches the top row of the ring, it's GAME OVER»
- Elite-Turm: schießt 60 s lang mit Laser (rosa Strahl, durchschlägt alle Monster auf der Linie, eigener Laser-Sound)
- Reichweiten-Vorschau: Sprechblase von Rosie/Blue beim Halten ausgeblendet (Sweep-Fund)
- Elite-Turm-Wow in W6, W56, W106 (alle 50 Wellen), nie kaufbar
Nutzung: python3 tools/patch444.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('GAME_VER = "V443"', 'GAME_VER = "V444"')

# A) Sprechblase beim Halten weg
rep('.sheet{transition:opacity .18s}.sheet.peek{opacity:0}', '.sheet{transition:opacity .18s}.sheet.peek{opacity:0}body.peeking #buddy{opacity:0!important;transition:opacity .15s}')
rep('S.peek = { type, lvl }; held = false; sh.classList.add("peek");', 'S.peek = { type, lvl }; held = false; sh.classList.add("peek"); document.body.classList.add("peeking");')
rep('const end = () => { sh.classList.remove("peek"); if (S) S.peek = null; };', 'const end = () => { sh.classList.remove("peek"); document.body.classList.remove("peeking"); if (S) S.peek = null; };')

# B) Unkraut-Karte von Blue (Spiel steht, muss bestätigt werden)
rep('if (left <= 2 && !D.weedW2) { D.weedW2 = true; try { window.__rbSay && window.__rbSay("rb_weedlast", true); } catch (e) {} }',
    'if (left <= 2 && !D.weedW2) { D.weedW2 = true; try { window.__rbSay && window.__rbSay("rb_weedlast", true); } catch (e) {} try { weedCard(); } catch (e) {} }   /* V444: Karte */')
rep('function hintEnd() { if (!hintKey) return;',
    '''/* V444: eindringliche Unkraut-Warnung von Blue – wie eine Tipp-Karte, Spiel steht bis «Got it» */
function weedCard() {
  if (hintKey) { setTimeout(weedCard, 800); return; } hintKey = "weed"; try { if (S && S.started && !S.over) S.coachHold = true; } catch (e) {}
  const c = $("coach"); c.hidden = false; $("coachStep").textContent = "ALERT"; $("coachT").innerHTML = `<img src="${HERO_IMG.blue}" alt="" style="width:64px;height:64px;object-fit:contain;vertical-align:middle;margin:-10px 6px -6px -4px">WEED ALERT!`;
  $("coachS").textContent = "Blue: It's almost at the ring! If the weed grows into the top row of the ring, it's GAME OVER. Cut it NOW – Tesla storm or Sniper strike.";
  $("coachSkip").textContent = "Got it"; const a = $("coachArrow"), card = c.querySelector(".coachCard"); coachHi(null); a.style.display = "none";
  const br = $("board").getBoundingClientRect(); card.style.bottom = ""; card.style.top = (br.top + br.height * 0.5 - 90) + "px";
  try { snd("siren"); } catch (e) {} clearTimeout(hintT);   /* kein Auto-Ende */
}
window.__weedCard = weedCard;
function hintEnd() { if (!hintKey) return;''')

# C) Elite-Laser: Strahl, Durchschlag, Sound
rep('''      const ox = t.x + Math.cos(t.ang + Math.PI / 2) * off, oy = t.y + Math.sin(t.ang + Math.PI / 2) * off;
      if (w.type === "kan") {''',
'''      const ox = t.x + Math.cos(t.ang + Math.PI / 2) * off, oy = t.y + Math.sin(t.ang + Math.PI / 2) * off;
      if (t.eliteT > 0) {   /* V444: Elite-Turm schießt Laser – trifft alles auf der Linie bis zum Ziel */
        const dx = best.x - ox, dy = best.y - oy, L = Math.hypot(dx, dy) || 1, ex = ox + dx / L * (L + 0.6), ey = oy + dy / L * (L + 0.6);
        for (const m of S.monsters) { if (m.dead) continue; const px = m.x - ox, py = m.y - oy, u = Math.max(0, Math.min(1, (px * dx + py * dy) / (L * L))); if (Math.hypot(px - u * dx, py - u * dy) <= 0.45) hurt(m, st.dmg * (m === best ? 1 : 0.6)); }
        if (w.type === "frost") for (const m of S.monsters) if (!m.dead && Math.hypot(m.x - best.x, m.y - best.y) <= st.splash) m.slowT = st.slow;
        S.fx.push({ type: "laser", x1: ox, y1: oy, x2: ex, y2: ey, t: 0, life: 0.2 });
        const now = performance.now(); if (!window.__lzT || now - window.__lzT > 85) { window.__lzT = now; try { if (!SFX.muted) { const v = Math.min(1, Math.max(0.2, 3 * (SFX.vol || 0.3))); tone(1500, 320, 0.17, 0.07 * v, 0, "sawtooth", 3200); tone(2400, 1100, 0.09, 0.04 * v, 0, "square", 5000); } } catch (e) {} }
        return;
      }
      if (w.type === "kan") {''')
rep('else if (f.type === "tracer") { ctx.globalAlpha = k;',
    '''else if (f.type === "laser") { const x1 = C(f.x1), y1 = C(f.y1), x2 = C(f.x2), y2 = C(f.y2); ctx.lineCap = "round"; ctx.globalAlpha = k * 0.35; ctx.strokeStyle = "#ff6fb5"; ctx.lineWidth = Math.max(6, s * 0.42); ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
      ctx.globalAlpha = k; ctx.strokeStyle = "#ff3fa0"; ctx.lineWidth = Math.max(3, s * 0.18); ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke(); ctx.strokeStyle = "#fff6fb"; ctx.lineWidth = Math.max(1.2, s * 0.07); ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
      ctx.fillStyle = "#fff6fb"; ctx.beginPath(); ctx.arc(x2, y2, Math.max(3, s * 0.2) * k, 0, 7); ctx.fill(); ctx.lineCap = "butt"; }
    else if (f.type === "tracer") { ctx.globalAlpha = k;''')
# D) Elite-Turm (Rosie/Blue mit Fallschirm) kommt in W6 und dann alle 50 Wellen (W56, W106) – nie kaufbar (Martin 12:14)
rep('if (!wowDone("elite") && S.wave >= 6 && WOW.wt > 10 && wowOk(9) && S.inWave && performance.now() - WOW.tonT > 8000) {',
    'const eW = [6, 56, 106].find(w => S.wave >= w && S.wave <= w + 3 && !wowDone(w === 6 ? "elite" : "elite" + w));   /* V444: W6, W56, W106 */\n  if (eW && WOW.wt > 10 && wowOk(eW + 3) && S.inWave && performance.now() - WOW.tonT > 8000) {')
rep('if (tw) { wowSet("elite"); wowElite(tw); } }', 'if (tw) { wowSet(eW === 6 ? "elite" : "elite" + eW); wowElite(tw); } }')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
