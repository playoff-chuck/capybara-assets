# V697 (Martin 13.11. 10:49–10:59): neues Monster «Cuddle Zombie» (RU Натааа, ES Abrazona, PT Grudenta) ab Welle 57.
# Bild/Sprite: Nano Banana Pro nach Martins Vorgabe, Vorstellungsbilder in_blue/in_rosie_cuddle (Wüste wie Mumie).
# Fähigkeit: läuft sie neben einem Turm vorbei, umarmt sie ihn 10 s – der Turm schießt nicht; sie kichert alle 4–5 s (Mädchenlachen,
# Freesound 179671 «girly giggle» von AlucardsBride, CC0). Wird sie in den 10 s nicht erledigt, löst sich der Turm auf.
# Häufigkeit: ab W57 1 je Welle, alle 20 Wellen eine mehr (W77: 2, W97: 3 …). Test: ?test=cuddle (W57, jedes 3. Monster ist sie, 3000 Gold).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep('GAME_VER = "V696"', 'GAME_VER = "V697"')
rep('bear:"img/9ce1173bc3.webp"};', 'bear:"img/9ce1173bc3.webp",cuddle:"img/cuddle_spr.webp"};')
rep('tiger:2.8,bear:2.6};', 'tiger:2.8,bear:2.6,cuddle:2.8};')
rep('tiger: 0.4, bear: 0.46, norm: 0.33 }', 'tiger: 0.4, bear: 0.46, cuddle: 0.36, norm: 0.33 }')
rep('''["bear", "Grizzly", "North American giant. Thick fur swallows 2 damage of every hit, so bring big guns."],''',
'''["bear", "Grizzly", "North American giant. Thick fur swallows 2 damage of every hit, so bring big guns."],
  ["cuddle", "Cuddle Zombie", "Wants to hug everyone. Hugs a tower for 10 s – it can't shoot. Splat her in time or the tower dissolves."],''')
rep('''  bear:   ["Grizzly",  "Huge and furry. Every hit loses 2 damage in the fur.", ["HP ×3", "Speed ×0.7", "Fur −2"]],
};''', '''  bear:   ["Grizzly",  "Huge and furry. Every hit loses 2 damage in the fur.", ["HP ×3", "Speed ×0.7", "Fur −2"]],
  cuddle: ["Cuddle Zombie", "Hugs a tower for 10 s – it stops shooting. Too slow? The tower dissolves.", ["HP ×1.6", "Speed ×0.7", "Hug 10 s"]],
};''')
rep('tiger: 2.2, bear: 3.0, norm: 1 }[kind]', 'tiger: 2.2, bear: 3.0, cuddle: 1.6, norm: 1 }[kind]')
rep('tiger: 1.3, bear: 0.7, norm: 1 }[kind]', 'tiger: 1.3, bear: 0.7, cuddle: 0.7, norm: 1 }[kind]')
rep('tiger: 30, bear: 45 }[kind]', 'tiger: 30, bear: 45, cuddle: 24 }[kind]')
rep('tiger: 60, bear: 90 };', 'tiger: 60, bear: 90, cuddle: 45 };')
rep('mummy: G.mummyFrom, tiger: G.tigerFrom, bear: G.bearFrom }[k]', 'mummy: G.mummyFrom, tiger: G.tigerFrom, bear: G.bearFrom, cuddle: G.cuddleFrom || 57 }[k]')
rep('["jaguar", "mummy", "tiger", "bear", "elite"]', '["jaguar", "mummy", "tiger", "bear", "cuddle", "elite"]', 2)
rep('mummy: "Mummy", tiger: "Tiger", bear: "Bear" }', 'mummy: "Mummy", tiger: "Tiger", bear: "Bear", cuddle: "Cuddle Zombie" }')
rep('const volts = w >= G.voltFrom ? 1 + Math.floor((w - G.voltFrom) / 8) : 0;',
    'const volts = w >= G.voltFrom ? 1 + Math.floor((w - G.voltFrom) / 8) : 0; const cuF = G.cuddleFrom || 57, cuddles = w >= cuF ? 1 + Math.floor((w - cuF) / 20) : 0;   /* V697 */')
rep('''else if (w >= (G.bearFrom || 999) && w <= 120 && idx % 11 === 7) kind = "bear";''',
    '''else if ((S.testCuddle && idx % 3 === 1) || [...Array(cuddles)].some((_, k) => slot(k, cuddles) + 3 === idx)) kind = "cuddle";   /* V697: Cuddle Zombie */
  else if (w >= (G.bearFrom || 999) && w <= 120 && idx % 11 === 7) kind = "bear";''')
rep('''function stepMonster(m, dt) {
  if (m.slowT > 0) m.slowT -= dt;''', '''function cuddleStep(m, dt) {   /* V697: Cuddle Zombie umarmt Türme – 10 s kein Schuss, danach löst sich der Turm auf */
  if (m.hugCd > 0) m.hugCd -= dt;
  if (m.hug) {
    const t = S.towers.get(m.hug.c);
    if (!t) { m.hug = null; m.hugCd = 1.5; return false; }
    t.hugBy = m; m.hug.t += dt; m.hug.lt -= dt;
    if (m.hug.lt <= 0) { m.hug.lt = 4 + Math.random(); playGiggle(); }
    const sec = Math.ceil(10 - m.hug.t); if (sec !== m.hug.sec && sec > 0) { m.hug.sec = sec; fxText(t.x, t.y, `♥ ${sec}`, "#ff5c9a"); }   /* Countdown über dem Turm */
    if (m.hug.t >= 10) { S.towers.delete(m.hug.c); t.hugBy = null; snd("towerLost"); fxText(t.x, t.y, "Tower hugged away", "#ff7aa8");
      for (let i = 0; i < 12; i++) { const a = Math.random() * 6.283, v = 2 + Math.random() * 4; S.fx.push({ type: "spark", x: t.x, y: t.y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, t: 0, life: 0.6 }); }
      if (S.sel === t) closeSheet(); S.dirty = true; m.hug = null; m.hugCd = 3; try { window.__mpush && window.__mpush("hug", { d: { r: "lost" } }); } catch (e) {} }
    return true; }
  if (m.hugCd > 0) return false;
  let best = null, bd = 1.2;
  for (const t of S.towers.values()) { if (t.hugBy && !t.hugBy.dead && t.hugBy.hug && t.hugBy !== m) continue; const d = Math.hypot(t.x - m.x, t.y - m.y); if (d < bd) { bd = d; best = t; } }
  if (!best) return false;
  m.hug = { c: best.y * GW + best.x, t: 0, lt: 0.15 }; best.hugBy = m; fxText(best.x, best.y, "HUG!", "#ff7aa8"); return true; }
function stepMonster(m, dt) {
  if (m.slowT > 0) m.slowT -= dt;
  if (m.kind === "cuddle" && cuddleStep(m, dt)) return;''')
rep('''function stepTowers(dt) {
  for (const t of S.towers.values()) {''', '''function stepTowers(dt) {
  for (const t of S.towers.values()) {
    if (t.hugBy) { if (t.hugBy.dead || !t.hugBy.hug || !S.monsters.includes(t.hugBy)) t.hugBy = null; else continue; }   /* V697: umarmter Turm schießt nicht */''')
rep('''function playWolf() {''', '''let gigN = 0; function playGiggle() { try { if (SFX.muted) return; const a = new Audio(`sfx/giggle${1 + (gigN++ % 3)}.mp3`); a.volume = 0.55 * Math.min(1, Math.max(0.6, 8 * Math.pow(SFX.vol || 0.3, 2))); a.play().catch(() => {}); } catch (e) {} }   /* V697: Kichern Cuddle Zombie (CC0) */
function playWolf() {''')
rep('nuts4: 121,', 'nuts4: 121, cuddle: 57,')
rep('''/* V330: Test-Zugang Störungen + Easter Egg (Dev-Liste und ?test=…) */''', '''/* V697: Test-Link ?test=cuddle */ try { (() => { const _dj = devJump; devJump = function (w, kind) { const r = _dj.apply(this, arguments); if (kind === "cuddle") { S.testCuddle = true; S.gold = Math.max(S.gold || 0, 3000); S.lives = Math.max(S.lives || 0, 99); S.waveCD = 6; toast("TEST · CUDDLE ZOMBIE in wave 57 · 99 lives · build towers right next to the path", "HQ", 3500); } return r; }; })(); } catch (e) { console.error("v697", e); }
/* V330: Test-Zugang Störungen + Easter Egg (Dev-Liste und ?test=…) */''')
rep("""const sz=s*1.18;if(S.sel===t){ctx.strokeStyle='#ee7a2c';""", """const sz=s*1.18;if(t.hugBy&&t.hugBy.hug){const hp=Math.min(1,(t.hugBy.hug.t||0)/10),pu=0.5+0.5*Math.sin(performance.now()/160);ctx.save();ctx.fillStyle=`rgba(255,92,154,${(0.18+0.18*pu).toFixed(2)})`;ctx.beginPath();ctx.arc(cx,cy,s*0.6,0,7);ctx.fill();ctx.strokeStyle='rgba(255,255,255,.6)';ctx.lineWidth=Math.max(2,s*0.1);ctx.beginPath();ctx.arc(cx,cy,s*0.6,0,7);ctx.stroke();ctx.strokeStyle='#ff3d8b';ctx.beginPath();ctx.arc(cx,cy,s*0.6,-Math.PI/2,-Math.PI/2+hp*6.283);ctx.stroke();ctx.font=`${Math.round(s*0.55)}px system-ui`;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('💗',cx,cy-s*0.62-s*0.08*pu);ctx.restore();}   /* V697: umarmter Turm – rosa Kreis mit Fortschritt */ if(S.sel===t){ctx.strokeStyle='#ee7a2c';""")
open(dst, "w", encoding="utf8").write(s)
print("ok V697")
