"""V379 (Martin 07.11. «Alle 3 bauen»): drei Wow-Momente fürs erste Spiel (je einmal pro Gerät, Link ?wow=1 setzt sie zurück).
1) SQUAD INCOMING: ~18 s nach Wellenbeginn (W1–6, nicht im Tutorial, mind. 3 Monster über dem Stapel) schicken Rosie & Blue einen
   Gratis-Ten-ton. Beim Aufprall Zeitlupe, Goldregen, Vibration.
2) Garantierter erster Dreifach-Splat: Trifft ein Stein (W1–6) das erste Mal 1–2 Monster, kommen bis zu 2 Monster aus der Nähe dazu.
   «SPLAT ×3!», Zeitlupe, Vibration, +50 Gold, Goldregen.
3) ELITE-Turm: nach ~2,5 min Spielzeit fliegt der Doppeldecker übers Feld, Rosie & Blue springen mit Fallschirm auf den ersten
   Turm mit Waffe. Der Turm glüht 60 s golden als «ELITE» und schießt doppelt so schnell."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V378";', 'const GAME_VER = "V379";')
# Zeitlupe im Hauptloop
rep('try { update(dt * (S.started && !S.over ? (S.speed || 1) * resumeK() : 1));',
    'try { update(dt * (S.started && !S.over ? (S.speed || 1) * resumeK() * wowSlowK() : 1)); try { wowTick(dt); } catch (e) {}')
# Helfer + Ablauf
rep('function stackTopRow() {', r'''/* V379: Wow-Momente fürs erste Spiel */
const WOW = { slowUntil: 0, wt: 0, pt: 0, tonT: -1e9, lastWave: -1 };
try { if (new URLSearchParams(location.search).get("wow") === "1") ["ton", "splat", "elite"].forEach(k => LS.del("capy-wow-" + k)); } catch (e) {}
window.__wow = { W: WOW, done: k => wowDone(k), drop: () => hardDrop(), frozen: () => frozen(), tut: () => TUT.on };   /* Test-Haken */
function wowDone(k) { return LS.get("capy-wow-" + k) === "1"; }
function wowSet(k) { LS.set("capy-wow-" + k, "1"); }
function wowSlowK() { return performance.now() < WOW.slowUntil ? 0.28 : 1; }
function wowSlow(ms) { WOW.slowUntil = performance.now() + ms; document.body.classList.add("wowSlow"); setTimeout(() => { if (performance.now() >= WOW.slowUntil - 30) document.body.classList.remove("wowSlow"); }, ms + 20); }
function wowBuzz(p) { try { window.__vib && window.__vib(p, true); } catch (e) {} }
function wowCoins(n = 28) { const d = document.createElement("div"); d.className = "wowCoins"; d.setAttribute("aria-hidden", "true");
  d.innerHTML = Array.from({ length: n }, () => `<i style="left:${(Math.random() * 96).toFixed(1)}%;animation-delay:${(Math.random() * 0.7).toFixed(2)}s;animation-duration:${(1.3 + Math.random() * 0.9).toFixed(2)}s;--r:${Math.round(Math.random() * 720 - 360)}deg">$</i>`).join("");
  document.body.appendChild(d); [0, 180, 360, 600].forEach(t => setTimeout(() => snd("coin"), t)); setTimeout(() => d.remove(), 2800); }
function wowBanner(t, sub) { const d = document.createElement("div"); d.className = "wowBan"; d.innerHTML = `<b>${t}</b>${sub ? `<small>${sub}</small>` : ""}`; document.body.appendChild(d); setTimeout(() => d.remove(), 2000); }
function wowOk() { return S.started && !S.over && !S.nuts && !S.testRun && !(TUT && TUT.on) && !frozen() && (S.wave || 0) >= 1 && S.wave <= 6; }
function wowTick(dt) {
  if (!S || !S.started || S.over) return;
  if (S.wave !== WOW.lastWave) { WOW.lastWave = S.wave; WOW.wt = 0; }
  if (S.inWave && !frozen()) WOW.wt += dt;
  if (!frozen()) WOW.pt += dt;
  // 1) SQUAD INCOMING – Gratis-Ten-ton
  if (!wowDone("ton") && wowOk() && S.inWave && WOW.wt > 18 && !S.ton) {
    const top = stackTopRow(); if (S.monsters.filter(m => !m.dead && m.y < top - 0.5).length >= 3) {
      wowSet("ton"); WOW.tonT = performance.now(); S.wowTon = true; wowBanner("SQUAD INCOMING!", `${heroKey() === "rosie" ? "Blue" : "Rosie"} sends a free Ten-ton drop`);
      snd("horn"); setTimeout(() => { if (!S.over) { S.tons = (S.tons || 0) + 1; startTon(); } }, 1500); } }
  // 3) ELITE-Turm
  if (!wowDone("elite") && WOW.pt > 150 && wowOk() && S.inWave && performance.now() - WOW.tonT > 8000) {
    let tw = null; for (const t of S.towers.values()) if (t.w && t.w.length) { tw = t; break; }
    if (tw) { wowSet("elite"); wowElite(tw); } }
}
function wowElite(t) {
  const pt = (() => { try { return cvPt(t.x + 0.5, t.y + 0.5); } catch (e) { return { x: innerWidth / 2, y: innerHeight / 2 }; } })();
  const d = document.createElement("div"); d.className = "wowPlane"; d.setAttribute("aria-hidden", "true");
  const h = heroKey(), b = buddyKey();
  d.innerHTML = `<img class="wpPlane" src="img/biplane.webp" alt=""><div class="wpChute" style="--tx:${pt.x}px;--ty:${pt.y}px"><span class="cA"></span><img src="${HERO_IMG[h]}" alt=""></div><div class="wpChute b2" style="--tx:${pt.x + 26}px;--ty:${pt.y}px"><span class="cA"></span><img src="${HERO_IMG[b]}" alt=""></div>`;
  document.body.appendChild(d); snd("engine");
  setTimeout(() => { if (S.over) return; t.eliteT = 60; snd("powerup"); wowBuzz([40, 40, 90]); announce("ELITE TOWER", "Rosie & Blue on board · 2× fire rate for 60 s", "SQUAD", 2400); }, 3300);
  setTimeout(() => d.remove(), 4200);
}
function stackTopRow() {''')
# 1) Aufprall des Gratis-Ten-ton
rep('      T.hit = true; T.ht = T.t; snd("tonHit"); S.shake = 1;',
    '      T.hit = true; T.ht = T.t; snd("tonHit"); S.shake = 1; if (S.wowTon) { S.wowTon = false; wowSlow(1600); wowCoins(); wowBuzz([80, 50, 160]); }   /* V379 */')
rep('  snd("tonFall"); toast("HEADS UP!", "POCKET", 1000);', '  snd("tonFall"); if (!S.wowTon) toast("HEADS UP!", "POCKET", 1000);')
# 2) Garantierter Dreifach-Splat
rep('  const hit = new Set(), H = VH(), W = VW(), sweep = Math.max(3, (p.fromY != null ? p.y - p.fromY : 0));\n  for (const [x, y] of p.cells) for (let d = 0; d <= sweep; d++) { const u = p.x + x, v = p.y + y - d; if (v < 0 || v >= H || u < 0 || u >= W) continue; const c = vIdx(u, v); if (d && S.grid[c]) break; hit.add(c); }',
    '''  const hit = new Set(), H = VH(), W = VW(), sweep = Math.max(3, (p.fromY != null ? p.y - p.fromY : 0));
  for (const [x, y] of p.cells) for (let d = 0; d <= sweep; d++) { const u = p.x + x, v = p.y + y - d; if (v < 0 || v >= H || u < 0 || u >= W) continue; const c = vIdx(u, v); if (d && S.grid[c]) break; hit.add(c); }
  try { if (!wowDone("splat") && S.started && !S.over && !S.nuts && !S.testRun && S.wave >= 1 && S.wave <= 6 && performance.now() - WOW.tonT > 6000 && hit.size >= 3) {   /* V379: erster Dreifach-Splat garantiert */
    const inHit = m => [m.cy * GW + m.cx, Math.round(m.y) * GW + Math.round(m.x), Math.floor(m.y) * GW + Math.floor(m.x), Math.ceil(m.y) * GW + Math.ceil(m.x)].some(c => hit.has(c));
    const alive = S.monsters.filter(m => !m.dead), first = alive.filter(inHit);
    if (first.length >= 1 && first.length < 3) { const f = first[0], more = alive.filter(m => !inHit(m) && Math.hypot(m.x - f.x, m.y - f.y) < 7).sort((a, b) => Math.hypot(a.x - f.x, a.y - f.y) - Math.hypot(b.x - f.x, b.y - f.y)).slice(0, 3 - first.length);
      if (first.length + more.length >= 3) { const cs = [...hit].sort((a, b) => Math.abs(a % GW - f.x) - Math.abs(b % GW - f.x)); more.forEach((m, k) => { const c = cs[k % cs.length]; m.cx = c % GW; m.cy = (c / GW) | 0; m.x = m.cx; m.y = m.cy; m.next = null; });
        S.wowSplat = true; wowSet("splat"); } } } } catch (e) {}''')
rep('  if (!c && cr) { if (cr >= 3) praise("SPLATASTIC!", 3, "Splatastic!");',
    '  if (S.wowSplat) { S.wowSplat = false; if (cr >= 3) { const g = 50; S.gold += g; wowSlow(1300); wowCoins(22); wowBuzz([60, 40, 120]); setTimeout(() => toast(`FIRST TRIPLE SPLAT · +${g} gold`, "SQUAD", 1800), 1400); if (!c) { praise("SPLAT ×3!", 4, "Splatastic!"); gridChanged(); spawnPiece(); return; } } }\n'
    '  if (!c && cr) { if (cr >= 3) praise("SPLATASTIC!", 3, "Splatastic!");')
# 3) ELITE: doppelte Feuerrate + Glühen
rep('      w.cd = 1 / st.rate;', '      w.cd = 1 / st.rate / (t.eliteT > 0 ? 2 : 1);')
rep('function stepTowers(dt) {\n  for (const t of S.towers.values()) {', 'function stepTowers(dt) {\n  for (const t of S.towers.values()) {\n    if (t.eliteT > 0) t.eliteT -= dt;   /* V379 */')
rep('    const cx = C(t.x), cy = C(t.y);',
    '''    const cx = C(t.x), cy = C(t.y);
    if (t.eliteT > 0) { const ph = performance.now() / 1000, a = 0.55 + 0.35 * Math.sin(ph * 6); ctx.save(); ctx.globalAlpha = Math.min(1, t.eliteT / 2) * a; const g = ctx.createRadialGradient(cx, cy, s * 0.2, cx, cy, s * 1.1); g.addColorStop(0, "rgba(255,216,77,.95)"); g.addColorStop(1, "rgba(255,216,77,0)"); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, s * 1.1, 0, 7); ctx.fill();
      ctx.globalAlpha = Math.min(1, t.eliteT / 2); ctx.font = `700 ${Math.max(9, s * 0.36)}px system-ui,sans-serif`; ctx.textAlign = "center"; ctx.lineWidth = Math.max(2, s * 0.1); ctx.strokeStyle = "#3a2414"; ctx.strokeText("ELITE", cx, cy - s * 0.62); ctx.fillStyle = "#ffd84d"; ctx.fillText("ELITE", cx, cy - s * 0.62); ctx.restore(); }   /* V379 */''')
# CSS
rep('.mNuts{position:absolute;width:0;height:0;pointer-events:none}',
    '''.mNuts{position:absolute;width:0;height:0;pointer-events:none}
.wowCoins{position:fixed;inset:0;pointer-events:none;z-index:2147482000;overflow:hidden}
.wowCoins i{position:absolute;top:-40px;width:26px;height:26px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff3b0,#f2cf5b 45%,#c99a1c);border:2px solid #7a5a10;color:#7a5a10;font:900 14px/22px system-ui,sans-serif;text-align:center;font-style:normal;animation:wowCoin 1.6s cubic-bezier(.45,.05,.8,.6) forwards}
@keyframes wowCoin{to{transform:translateY(calc(100vh + 80px)) rotate(var(--r,360deg))}}
.wowBan{position:fixed;left:50%;top:30%;transform:translate(-50%,-50%);z-index:2147482100;pointer-events:none;text-align:center;animation:wowBan 2s ease-out forwards}
.wowBan b{display:block;font:400 44px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.04em;color:#ffd84d;-webkit-text-stroke:2px #3a2414;text-shadow:0 4px 0 #3a2414,0 0 18px rgba(255,190,40,.7);white-space:nowrap}
.wowBan small{display:inline-block;margin-top:8px;font:700 13px/1.2 system-ui,sans-serif;color:#fff7e8;background:#3a2414;border-radius:10px;padding:5px 10px}
@keyframes wowBan{0%{opacity:0;transform:translate(-50%,-50%) scale(.3)}12%{opacity:1;transform:translate(-50%,-50%) scale(1.12)}20%{transform:translate(-50%,-50%) scale(1)}80%{opacity:1}100%{opacity:0;transform:translate(-50%,-60%) scale(1)}}
body.wowSlow #board{filter:saturate(1.35) contrast(1.06)}
.wowPlane{position:fixed;inset:0;pointer-events:none;z-index:2147482000;overflow:hidden}
.wowPlane .wpPlane{position:absolute;top:9%;left:-160px;width:150px;max-width:none;animation:wowFly 3.4s linear forwards}
@keyframes wowFly{to{transform:translateX(calc(100vw + 330px))}}
.wowPlane .wpChute{position:absolute;left:0;top:0;width:0;height:0;opacity:0;animation:wowChute 2.3s ease-in 1s forwards}
.wowPlane .wpChute.b2{animation-delay:1.25s}
.wowPlane .wpChute img{position:absolute;left:-17px;top:-34px;width:34px;height:34px;max-width:none;border-radius:50%;border:2px solid #3a2414;background:#fff7e8;object-fit:cover;object-position:50% 18%}
.wowPlane .cA{position:absolute;left:-24px;top:-70px;width:48px;height:26px;border-radius:24px 24px 4px 4px;background:repeating-linear-gradient(90deg,#ff6fb5 0 12px,#fff7e8 12px 24px);border:2px solid #3a2414}
.wowPlane .cA::after{content:"";position:absolute;left:8px;right:8px;top:24px;height:12px;border-left:1.5px solid #3a2414;border-right:1.5px solid #3a2414}
@keyframes wowChute{0%{opacity:1;transform:translate(42vw,13vh) scale(.6)}100%{opacity:1;transform:translate(var(--tx),var(--ty)) scale(1)}}
@media (prefers-reduced-motion:reduce){.wowCoins,.wowPlane .wpPlane{display:none}.wowBan{animation-duration:2.3s}}''')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
