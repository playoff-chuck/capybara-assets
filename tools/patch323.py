"""V323 (Martin 06.11. 21:14): 3 Tipps in den ersten Runden – Capybara mit Glühbirne («Erleuchtung»).
Je einmal pro Gerät, nie zusammen mit einem anderen Fenster (5 s Ruhe), 3 s nicht wegklickbar, dann «GOT IT».
1) W2: Monster mit Steinen erschlagen – Block nach unten beschleunigen (DROP, Mitte unten), gelber Pfeil zeigt hin.
2) W4: Kanone am rechten Rand → erste Runden ohne Probleme.
3) W5: Die äußersten Felder links und rechts müssen nicht voll sein, damit eine Zeile verschwindet.
Bild: img/tip_bulb.webp (Nano Banana Pro, 0,14 $)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V322";', 'const GAME_VER = "V323";')
rep('return v("ovIntro") || v("ovHack")', 'return !!(window.__tipBulb && window.__tipBulb.open) || v("ovIntro") || v("ovHack")')   # Tipp zählt als Fenster
CSS = '''
/* V323: Tipps mit Glühbirnen-Capybara */
#tipBulb{position:fixed;left:50%;bottom:calc(env(safe-area-inset-bottom,0px) + 190px);transform:translate(-50%,20px) scale(.9);opacity:0;transition:opacity .3s,transform .3s cubic-bezier(.2,1.5,.4,1);z-index:70;width:min(92vw,380px);display:grid;grid-template-columns:78px 1fr;gap:8px;align-items:center;background:#fff7e8;border:3px solid #3a2414;border-radius:18px;box-shadow:0 5px 0 #3a2414,0 10px 24px rgba(0,0,0,.35);padding:8px 12px 10px 6px}
#tipBulb.on{opacity:1;transform:translate(-50%,0) scale(1)}
#tipBulb img{width:78px;height:auto;align-self:end;margin-top:-34px}
#tipBulb b{display:block;font:400 20px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.04em;color:#3a2414}
#tipBulb small{display:block;font:700 10px/1 var(--f-body,"Baloo 2",sans-serif);letter-spacing:.18em;color:#c0782a;margin-bottom:3px}
#tipBulb p{margin:4px 0 8px;font:600 14px/1.3 var(--f-body,"Baloo 2",sans-serif);color:#3a2414}
#tipBulb button{font:400 16px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.05em;background:#ffd84d;color:#3a2414;border:2.5px solid #3a2414;border-radius:12px;box-shadow:0 3px 0 #3a2414;padding:6px 14px 4px}
#tipBulb button:disabled{opacity:.45}
#tipArrow{position:fixed;z-index:71;width:46px;height:60px;pointer-events:none;animation:tipBob .7s ease-in-out infinite}
@keyframes tipBob{50%{transform:translateY(-8px)}}
'''
i = s.index('</style>'); s = s[:i] + CSS + s[i:]
JS = r'''
/* V323: drei Tipps in den ersten Runden */
try { (() => {
  const TIPS = [
    { w: 2, t: "SPLAT THEM WITH BLOCKS!", p: "Blocks squash monsters. Speed a block down onto them – tap DROP.", at: "bDrop" },
    { w: 4, t: "CANNON ON THE RIGHT EDGE", p: "Mount a cannon on a block at the right edge – it gets you through the first waves with ease." },
    { w: 5, t: "EDGES DON'T COUNT", p: "The outer squares on the left and right don't need blocks – a row clears without them." }];
  const card = document.createElement("div"); card.id = "tipBulb"; card.hidden = true;
  card.innerHTML = '<img src="img/tip_bulb.webp" alt=""><div><small>TIP</small><b></b><p></p><button type="button" disabled>GOT IT</button></div>'; document.body.appendChild(card);
  const arr = document.createElement("div"); arr.id = "tipArrow"; arr.hidden = true;
  arr.innerHTML = '<svg viewBox="0 0 64 84" width="46" height="60"><path d="M20 4 Q32 1 44 4 L45 44 L60 44 Q63 46 61 49 L34 81 Q32 83 30 81 L3 49 Q1 46 4 44 L19 44 Z" fill="#ffd23a" stroke="#17150c" stroke-width="4.5" stroke-linejoin="round"/></svg>'; document.body.appendChild(arr);
  const btn = card.querySelector("button"); let cur = null, armT = 0;
  const seen = i => { try { return LS.get("tarnturm-tipb-" + i) === "1"; } catch (e) { return true; } };
  function place() { if (!cur || !cur.at) { arr.hidden = true; return; } const el = document.getElementById(cur.at); if (!el || !el.offsetParent) { arr.hidden = true; return; } const r = el.getBoundingClientRect(); arr.hidden = false; arr.style.left = (r.left + r.width / 2 - 23) + "px"; arr.style.top = (r.top - 64) + "px"; }
  function close() { if (!cur) return; card.classList.remove("on"); arr.hidden = true; setTimeout(() => { card.hidden = true; }, 300); cur = null; window.__evtLast = performance.now(); }
  btn.addEventListener("click", e => { e.stopPropagation(); if (performance.now() < armT) return; try { snd("uiTap"); } catch (er) {} close(); });
  function show(i) { const T = TIPS[i]; cur = T; try { LS.set("tarnturm-tipb-" + i, "1"); } catch (e) {}
    card.querySelector("b").textContent = T.t; card.querySelector("p").textContent = T.p; btn.disabled = true; armT = performance.now() + 3000;
    card.hidden = false; requestAnimationFrame(() => card.classList.add("on")); place(); try { snd("radio"); } catch (e) {}
    setTimeout(() => { if (cur === T) btn.disabled = false; }, 3000); }
  window.__tipBulb = { show, close, get open() { return !!cur; } };
  setInterval(() => { try {
    if (cur) { place(); if (!S || !S.started || S.over) close(); return; }
    if (!S || !S.started || S.over || S.nuts || S.testRun || (typeof TUT !== "undefined" && TUT.on) || !S.inWave) return;
    const i = TIPS.findIndex((T, k) => !seen(k) && S.wave >= T.w && S.wave <= T.w + 3); if (i < 0) return;
    if (performance.now() - (window.__waveStartAt || 0) < 3000) return;
    if (uiWinOpen() || S.paused || S.mapShow || S.ordersOpen || S.drop || S.mode || S.sel || S.shop || performance.now() - (window.__evtLast || -1e9) < 5000) return;
    show(i); } catch (e) {} }, 400);
})(); } catch (e) { console.error("v323 tips", e); }
'''
anchor = '})();\n</script>'
p = s.rindex(anchor); s = s[:p] + JS + s[p:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
