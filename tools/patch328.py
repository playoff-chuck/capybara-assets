"""V328 (Martin 06.11., To-do 95): Easter Egg je Kontinent (max. 1× pro Spiel und Kontinent).
Auslöser: der fallende Stein wird 3× hintereinander gegen den linken oder rechten Rand gedrückt.
Dann: Fenster mit Hintergrund img/egg_bg.webp (Höhlentempel), Mosaik 10×12 baut sich auf, der fehlende lange Stein fällt hinein,
unten «YOU FOUND AN EASTER EGG!» + «+5000» (Punkte, S.eggBonus fließt in calcScore). Kein «SECRET LEVEL»-Titel.
Motive: Südamerika Herz · Afrika Capybara · Asien Squad-Capybara mit Helm · Nordamerika Mammutbaum · Antarktis Pinguin.
Test-Hook window.__egg(contIndex)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V327";', 'const GAME_VER = "V328";')
rep('<div id="ovTilt" hidden>',
    '<div id="ovEgg" hidden><div class="eggIn"><canvas id="eggCv" width="400" height="480"></canvas><div class="eggTxt"><b>YOU FOUND AN EASTER EGG!</b><span>+5000</span></div><small class="eggTap">tap to continue</small></div></div>\n      <div id="ovTilt" hidden>')
rep('#ovTilt{position:fixed;', '''#ovEgg{position:fixed;inset:0;z-index:260;display:flex;align-items:center;justify-content:center;padding:16px;background:#0b0a14 url(img/egg_bg.webp) center/cover no-repeat;opacity:0;transition:opacity .45s ease;cursor:pointer}
#ovEgg[hidden]{display:none}
#ovEgg.on{opacity:1}
#ovEgg .eggIn{display:flex;flex-direction:column;align-items:center;gap:14px;width:min(340px,88vw)}
#ovEgg canvas{width:100%;height:auto;aspect-ratio:10/12;border-radius:10px;box-shadow:0 0 0 4px #2a2236,0 0 0 7px #c9a63a,0 0 40px rgba(255,214,120,.45),0 10px 30px rgba(0,0,0,.6)}
#ovEgg .eggTxt{display:flex;flex-direction:column;align-items:center;gap:2px;opacity:0;transform:translateY(10px) scale(.9);transition:all .5s cubic-bezier(.3,1.6,.5,1)}
#ovEgg.done .eggTxt{opacity:1;transform:none}
#ovEgg .eggTxt b{font-family:"Bangers",var(--f-display);font-weight:400;font-size:clamp(24px,7.6vw,34px);letter-spacing:.04em;color:#fff6e6;-webkit-text-stroke:2px #3a1d10;paint-order:stroke fill;text-shadow:0 4px 0 #3a1d10,0 0 18px rgba(255,214,120,.7);text-align:center;line-height:1}
#ovEgg .eggTxt span{font-family:"Bangers",var(--f-display);font-size:clamp(34px,11vw,52px);color:#ffcf3d;-webkit-text-stroke:2px #3a1d10;paint-order:stroke fill;text-shadow:0 4px 0 #3a1d10;line-height:1}
#ovEgg .eggTap{font-family:var(--f-ui);font-weight:700;font-size:12px;letter-spacing:.14em;color:#e9dcff;opacity:0;transition:opacity .4s}
#ovEgg.tap .eggTap{opacity:.8}
#ovTilt{position:fixed;''')
JS = r'''
/* V328: Easter Egg je Kontinent */
try { (() => {
  // 10×12 Mosaike · 1 blau 2 gelb 3 grün 4 türkis 5 orange 6 lila 7 rosa 8 hellgrau · GAP = die 4 Felder des fehlenden langen Steins
  const EGG = [
    { k: "samerica", m: ["3333333333", "3377337733", "3777777773", "3777777773", "3777777773", "3377777733", "3337777333", "3333773333", "3333333333", "3323333233", "3333333333", "3333333333"], gap: [[4, 2], [4, 3], [4, 4], [4, 5]] },
    { k: "africa", m: ["2222222222", "2222222222", "2222222222", "2222225552", "2555555565", "5555555552", "5555555552", "2555555522", "2522522522", "3333333333", "3333333333", "3333333333"], gap: [[2, 5], [3, 5], [4, 5], [5, 5]] },
    { k: "asia", m: ["4444444444", "4443333444", "4433333344", "4333333334", "4455555544", "4465555644", "4455555544", "4455665544", "4445555444", "4455555544", "4555555554", "4555555554"], gap: [[5, 8], [5, 9], [5, 10], [5, 11]] },
    { k: "namerica", m: ["1111311111", "1113331111", "1133333111", "1113331111", "1133333111", "1333333311", "1113531111", "1133533311", "1333533331", "1111511111", "1111511111", "3333533333"], gap: [[4, 8], [4, 9], [4, 10], [4, 11]] },
    { k: "antarctica", m: ["1111111111", "1111661111", "1116666111", "1168668611", "1166556611", "1668888661", "6688888866", "6688888866", "1688888861", "1668888661", "1155115511", "4444444444"], gap: [[4, 5], [4, 6], [4, 7], [4, 8]] } ];
  SAVE_KEYS.push("eggBonus", "eggDone");
  const _cs = calcScore; calcScore = function () { return _cs.apply(this, arguments) + (S && S.eggBonus || 0); };
  const _fz = frozen; frozen = function () { return _fz.apply(this, arguments) || !!(S && S.eggOpen); };
  const _ca = canAct; canAct = function () { return !(S && S.eggOpen) && _ca.apply(this, arguments); };
  const _uw = uiWinOpen; uiWinOpen = function () { if (S && S.eggOpen) return true; return _uw.apply(this, arguments); };
  // Auslöser: 3× hintereinander gegen den Rand
  let push = { n: 0, dir: 0, piece: -1 };
  const _mv = move; move = function (dx) {
    try { const p = S && S.piece; if (p && canAct() && !S.rotMode && !S.nuts && !S.duel) {
        const W = VW(), wall = p.cells.some(([x]) => p.x + x + dx < 0 || p.x + x + dx >= W);
        if (wall) { if (push.dir !== dx || push.piece !== S.pieceNo) push = { n: 0, dir: dx, piece: S.pieceNo }; push.n++;
          if (push.n >= 3) { push.n = 0; const c = wherePos(S.wave).c; S.eggDone = S.eggDone || {}; if (!S.eggDone[c] && S.inWave !== undefined && inPlay()) { S.eggDone[c] = 1; openEgg(c); return; } } }
        else push.n = 0; } } catch (e) {}
    return _mv.apply(this, arguments); };
  function tileCol(v) { if (v === 8) return ["#d8d2c0", "#b9b2a0"]; const set = CAMO[v - 1]; return [set[0], set[2] || set[1]]; }
  function openEgg(ci) {
    const E = EGG[Math.max(0, Math.min(EGG.length - 1, ci))], ov = $("ovEgg"), cvE = $("eggCv"), g = cvE.getContext("2d");
    S.eggOpen = true; ov.classList.remove("on", "done", "tap"); ov.hidden = false; requestAnimationFrame(() => ov.classList.add("on"));
    snd("siren");
    const CW = 40, gapSet = new Set(E.gap.map(([x, y]) => y * 10 + x)), order = [...Array(120).keys()].filter(i => !gapSet.has(i)).sort(() => Math.random() - 0.5);
    const gx = E.gap[0][0], gy = E.gap[0][1], vert = E.gap[1][0] === gx, gv = +E.m[gy][gx];
    const t0 = performance.now(), T_TILES = 1100, T_FALL0 = 1500, T_FALL = 650; let landed = false, closeOK = false, raf = 0;
    function tile(x, y, v, a = 1, sc = 1) { const [c1, c2] = tileCol(v), px = x * CW, py = y * CW, pad = 2 + (1 - sc) * CW / 2;
      g.globalAlpha = a; g.fillStyle = c2; g.fillRect(px + pad, py + pad, CW - 2 * pad, CW - 2 * pad);
      g.fillStyle = c1; g.fillRect(px + pad + 3, py + pad + 3, CW - 2 * pad - 6, CW - 2 * pad - 7);
      g.fillStyle = "rgba(255,255,255,.22)"; g.fillRect(px + pad + 3, py + pad + 3, CW - 2 * pad - 6, 4); g.globalAlpha = 1; }
    function frame(now) {
      const t = now - t0; g.clearRect(0, 0, 400, 480); g.fillStyle = "#17121f"; g.fillRect(0, 0, 400, 480);
      g.strokeStyle = "rgba(255,255,255,.05)"; for (let i = 1; i < 10; i++) { g.beginPath(); g.moveTo(i * CW, 0); g.lineTo(i * CW, 480); g.stroke(); } for (let i = 1; i < 12; i++) { g.beginPath(); g.moveTo(0, i * CW); g.lineTo(400, i * CW); g.stroke(); }
      const shown = Math.min(order.length, Math.floor(order.length * t / T_TILES));
      for (let i = 0; i < shown; i++) { const c = order[i], x = c % 10, y = (c / 10) | 0, age = (t - i / order.length * T_TILES) / 180; tile(x, y, +E.m[y][x], Math.min(1, age), Math.min(1, 0.4 + age * 0.6)); }
      if (t < T_FALL0 + T_FALL) { for (const [x, y] of E.gap) { g.strokeStyle = `rgba(255,214,120,${0.35 + 0.35 * Math.sin(t / 120)})`; g.lineWidth = 2; g.strokeRect(x * CW + 3, y * CW + 3, CW - 6, CW - 6); } }
      if (t >= T_FALL0) { const k = Math.min(1, (t - T_FALL0) / T_FALL), e = k * k, dy = (1 - e) * (vert ? (gy + 4) * CW : (gy + 1) * CW);
        g.save(); g.translate(0, -dy); for (const [x, y] of E.gap) tile(x, y, gv); g.restore();
        if (k >= 1 && !landed) { landed = true; snd("drop"); setTimeout(() => snd("lines", 4), 120); ov.classList.add("done"); try { SFX.say("Unbelievable!"); } catch (e) {} setTimeout(() => { closeOK = true; ov.classList.add("tap"); }, 1400); setTimeout(close, 7000); } }
      if (landed) { const k = Math.min(1, (t - T_FALL0 - T_FALL) / 900); g.fillStyle = `rgba(255,240,190,${0.55 * (1 - k)})`; g.fillRect(0, 0, 400, 480);
        const sh = ((t / 6) % 700) - 150; const gr = g.createLinearGradient(sh, 0, sh + 120, 480); gr.addColorStop(0, "rgba(255,255,255,0)"); gr.addColorStop(0.5, "rgba(255,255,255,.18)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(0, 0, 400, 480); }
      raf = requestAnimationFrame(frame); }
    let closed = false;
    function close() { if (closed) return; closed = true; cancelAnimationFrame(raf); S.eggBonus = (S.eggBonus || 0) + 5000; ov.classList.remove("on"); setTimeout(() => { ov.hidden = true; S.eggOpen = false; }, 450); try { checkScore(); } catch (e) {} toast("EASTER EGG · +5000 points", "HQ", 1800); }
    ov.onclick = () => { if (closeOK) close(); };
    raf = requestAnimationFrame(frame);
  }
  window.__egg = c => openEgg(c == null ? wherePos(S.wave).c : c);
})(); } catch (e) { console.error("v328", e); }
'''
anchor = '})();\n</script>'
p = s.rindex(anchor); s = s[:p] + JS + s[p:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
