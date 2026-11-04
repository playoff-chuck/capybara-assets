"""V224: Weltkarte im Spiel.
- Große Karte (#ovMap): eigener Kontinent nah, Orte als Stecknadeln (geschafft gold, aktuell rosa mit Held, offen grau,
  Wahrzeichen als Stern), gepunkteter Weg. «WORLD» zoomt heraus, Kontinent antippen zoomt hinein.
- Öffnen: Startbildschirm (Kartenknopf links neben Hall of Fame), Pausemenü («WORLD MAP»), Game over («You reached …»).
- Automatisch: erster Start (Flugzeug fliegt nach South America), neuer Ort alle 5 Wellen (Held hüpft weiter, ~2,6 s),
  neuer Kontinent W31/61/91/121 (raus, Flugzeug fliegt, rein, ~5 s). Antippen überspringt. Spiel steht solange still.
- Nuts-Abstecher: keine Karte."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V223";', 'const GAME_VER = "V224";')
rep('<link rel="preload" as="image" href="img/mixer_big.webp">', '<link rel="preload" as="image" href="img/mixer_big.webp"><link rel="preload" as="image" href="img/worldmap.webp">')

js = r'''
  /* ===== V224: Weltkarte ===== */
  try {
    const MAP_AR = 768 / 1376;
    const MAP_PTS = [
      [[.262, .705], [.236, .615], [.252, .505], [.288, .468], [.282, .640], [.314, .556]],   // South America
      [[.452, .415], [.514, .522], [.574, .522], [.468, .338], [.583, .348], [.538, .362]],   // Africa
      [[.585, .168], [.678, .245], [.738, .305], [.700, .150], [.872, .192], [.826, .132]],   // Asia
      [[.137, .305], [.126, .176], [.186, .296], [.209, .228], [.282, .262], [.248, .165]],   // North America
      [[.195, .930], [.322, .925], [.456, .930], [.600, .920], [.720, .930], [.836, .925]]];  // Antarctica
    const contName = c => ["SOUTH AMERICA", "AFRICA", "ASIA", "NORTH AMERICA", "ANTARCTICA"][c];
    const nice = t => t.toLowerCase().replace(/\b\w/g, m => m.toUpperCase());
    const ov = document.createElement("div"); ov.id = "ovMap"; ov.hidden = true;
    ov.innerHTML = `<div class="mapVp"><div class="mapWorld"><img class="mapImg" src="img/worldmap.webp" alt="World map" draggable="false"><svg class="mapPath" viewBox="0 0 1000 ${Math.round(1000 * MAP_AR)}" preserveAspectRatio="none"></svg><div class="mapPins"></div><div class="mapPlane">✈️</div><div class="mapMe"><img alt=""></div></div></div>
      <div class="mapTop"><small class="mapCont"></small><b class="mapPlace"></b><span class="mapSub"></span></div>
      <div class="mapBar"><button type="button" class="mapWorldBtn">WORLD</button><button type="button" class="mapClose">CLOSE</button></div>
      <div class="mapSkip">tap to skip</div>`;
    document.body.appendChild(ov);
    const vp = ov.querySelector(".mapVp"), world = ov.querySelector(".mapWorld"), pinsEl = ov.querySelector(".mapPins"), pathEl = ov.querySelector(".mapPath"), plane = ov.querySelector(".mapPlane"), me = ov.querySelector(".mapMe");
    let cam = { x: .5, y: .5, k: 1 }, BW = 400, mode = null, seqT = [], seqDone = null;
    const curWave = () => { try { if (typeof S !== "undefined" && S && S.started && !S.over && !S.nuts) return Math.max(1, S.wave || 1); } catch (e) {} try { const d = JSON.parse(LS.get("tarnturm-save") || "null"); if (d && d.wave && !d.nuts) return Math.max(1, d.wave); } catch (e) {} return 1; };
    const posOf = w => { const P = wherePos(w); return { c: P.c, p: P.p, g: P.c * 6 + P.p }; };
    function layout() { const W = vp.clientWidth || innerWidth; BW = W; world.style.width = BW + "px"; world.style.height = BW * MAP_AR + "px"; }
    function apply(anim) {
      const W = vp.clientWidth, H = vp.clientHeight, mw = BW * cam.k, mh = BW * MAP_AR * cam.k;
      let tx = W / 2 - cam.x * mw, ty = H / 2 - cam.y * mh;
      if (mw >= W) tx = Math.min(0, Math.max(W - mw, tx)); else tx = (W - mw) / 2;
      if (mh >= H) ty = Math.min(0, Math.max(H - mh, ty)); else ty = (H - mh) / 2;
      world.style.transition = anim ? `transform ${anim}ms cubic-bezier(.45,0,.25,1)` : "none";
      world.style.transform = `translate(${tx}px,${ty}px) scale(${cam.k})`; world.style.setProperty("--ik", 1 / cam.k);
    }
    function contCam(c) { const P = MAP_PTS[c], xs = P.map(p => p[0]), ys = P.map(p => p[1]), pad = .07;
      const x0 = Math.min(...xs) - pad, x1 = Math.max(...xs) + pad, y0 = Math.min(...ys) - pad * 1.6, y1 = Math.max(...ys) + pad * 1.6;
      const W = vp.clientWidth, H = vp.clientHeight * .78, k = Math.max(1, Math.min(5, W / ((x1 - x0) * BW), H / ((y1 - y0) * BW * MAP_AR)));
      return { x: (x0 + x1) / 2, y: (y0 + y1) / 2 + .02, k }; }
    function worldCam() { const W = vp.clientWidth, H = vp.clientHeight; return { x: .5, y: .5, k: Math.max(1, Math.min(H / (BW * MAP_AR) * .62, 2.2)) }; }
    function go(c, ms) { cam = c; apply(ms); }
    function drawPins(g) {   // g = globaler Index des aktuellen Ortes (0..29)
      let h = ""; MAP_PTS.forEach((P, c) => P.forEach((p, i) => { const gi = c * 6 + i, st = gi < g ? "done" : gi === g ? "cur" : "open";
        h += `<div class="mPin ${st}${i === 5 ? " star" : ""}" data-g="${gi}" style="left:${p[0] * 100}%;top:${p[1] * 100}%"><i></i>${gi === g ? `<em>${nice(CONTS[c][2][i])}</em>` : ""}</div>`; }));
      pinsEl.innerHTML = h;
      const H = Math.round(1000 * MAP_AR); pathEl.innerHTML = MAP_PTS.map((P, c) => `<polyline points="${P.map(p => (p[0] * 1000).toFixed(1) + "," + (p[1] * H).toFixed(1)).join(" ")}" class="${c * 6 + 5 < g ? "done" : ""}"/>`).join("");
    }
    function setMe(pt, on) { me.style.left = pt[0] * 100 + "%"; me.style.top = pt[1] * 100 + "%"; me.classList.toggle("on", !!on); try { me.querySelector("img").src = HERO_IMG[heroKey()]; } catch (e) {} }
    function label(cont, place, sub) { ov.querySelector(".mapCont").textContent = cont || ""; ov.querySelector(".mapPlace").textContent = place || ""; ov.querySelector(".mapSub").textContent = sub || ""; }
    function placeSub(w) { const P = wherePos(w), left = 5 - P.d, lm = (5 - P.p) * 5 - P.d; return P.p === 5 ? `Landmark · boss waits here · wave ${w}` : `Wave ${w} · next stop in ${left} wave${left > 1 ? "s" : ""} · landmark in ${lm}`; }
    function clearSeq() { seqT.forEach(clearTimeout); seqT = []; }
    function at(ms, f) { seqT.push(setTimeout(f, ms)); }
    function show(m) { mode = m; layout(); ov.hidden = false; ov.className = m === "browse" ? "browse" : "auto"; document.body.classList.add("mapUp"); }
    function hide() { clearSeq(); ov.hidden = true; mode = null; document.body.classList.remove("mapUp"); plane.classList.remove("on"); const f = seqDone; seqDone = null; if (f) f(); }
    /* frei ansehen */
    function openMap(w, why) { clearSeq(); w = w || curWave(); const P = posOf(w); show("browse"); drawPins(P.g); setMe(MAP_PTS[P.c][P.p], false);
      label(contName(P.c), why === "over" ? `You reached ${nice(CONTS[P.c][2][P.p])}` : nice(CONTS[P.c][2][P.p]), placeSub(w));
      go(worldCam(), 0); requestAnimationFrame(() => requestAnimationFrame(() => go(contCam(P.c), 900))); try { snd("open"); } catch (e) {} }
    ov.querySelector(".mapClose").addEventListener("click", e => { e.stopPropagation(); try { snd("close"); } catch (er) {} hide(); });
    ov.querySelector(".mapWorldBtn").addEventListener("click", e => { e.stopPropagation(); const wv = ov.classList.toggle("wv"); const P = posOf(curWave()); go(wv ? worldCam() : contCam(P.c), 800); ov.querySelector(".mapWorldBtn").textContent = wv ? "MY CONTINENT" : "WORLD"; try { snd("uiTap"); } catch (er) {} });
    vp.addEventListener("click", e => { if (mode !== "browse") return; const r = world.getBoundingClientRect(), nx = (e.clientX - r.left) / r.width, ny = (e.clientY - r.top) / r.height;
      let best = -1, bd = 9; MAP_PTS.forEach((P, c) => P.forEach(p => { const d = Math.hypot(p[0] - nx, (p[1] - ny) * MAP_AR); if (d < bd) { bd = d; best = c; } }));
      if (best >= 0 && bd < .12) { ov.classList.remove("wv"); ov.querySelector(".mapWorldBtn").textContent = "WORLD"; go(contCam(best), 800); const g = posOf(curWave()).g; const done = Math.max(0, Math.min(6, g - best * 6));
        label(contName(best), best * 6 > g ? "Not yet reached" : nice(CONTS[best][2][Math.min(5, Math.max(0, g - best * 6))]), best * 6 > g ? `Arrive at wave ${best * 30 + 1}` : `${done} of 6 places cleared`); try { snd("uiTap"); } catch (er) {} } });
    /* automatische Szenen */
    ov.addEventListener("click", () => { if (mode === "auto") hide(); });
    function flyPlane(a, b, ms) { plane.classList.add("on"); const t0 = performance.now(), ang = Math.atan2((b[1] - a[1]) * MAP_AR, b[0] - a[0]) * 180 / Math.PI;
      const step = now => { if (mode !== "auto") return; const t = Math.min(1, (now - t0) / ms), e = t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2, x = a[0] + (b[0] - a[0]) * e, y = a[1] + (b[1] - a[1]) * e - Math.sin(Math.PI * e) * .12;
        plane.style.left = x * 100 + "%"; plane.style.top = y * 100 + "%"; plane.style.setProperty("--a", (ang - Math.cos(Math.PI * e) * 18) + "deg"); if (t < 1) requestAnimationFrame(step); else plane.classList.remove("on"); };
      requestAnimationFrame(step); try { SFX.swoosh && SFX.swoosh(); } catch (e) {} }
    const cen = c => { const P = MAP_PTS[c]; return [P.reduce((a, p) => a + p[0], 0) / 6, P.reduce((a, p) => a + p[1], 0) / 6]; };
    function hopMe(a, b, ms) { const t0 = performance.now(); me.classList.add("on", "hop");
      const step = now => { if (mode !== "auto") return; const t = Math.min(1, (now - t0) / ms), x = a[0] + (b[0] - a[0]) * t, y = a[1] + (b[1] - a[1]) * t - Math.sin(Math.PI * t) * .05;
        me.style.left = x * 100 + "%"; me.style.top = y * 100 + "%"; if (t < 1) requestAnimationFrame(step); else me.classList.remove("hop"); };
      requestAnimationFrame(step); }
    function playPlace(w, done) { const P = posOf(w), prev = MAP_PTS[P.c][P.p - 1], nxt = MAP_PTS[P.c][P.p]; seqDone = done; show("auto"); drawPins(P.g - 1); setMe(prev, true);
      label(contName(P.c), `Next stop: ${nice(CONTS[P.c][2][P.p])}`, P.p === 5 ? "The landmark · the boss lives here" : `Waves ${w}–${w + 4}`); go(contCam(P.c), 0);
      at(450, () => { hopMe(prev, nxt, 900); try { snd("uiTap"); } catch (e) {} }); at(1400, () => { drawPins(P.g); try { snd("coin"); } catch (e) {} }); at(2700, hide); }
    function playCont(w, done) { const P = posOf(w), oc = Math.max(0, P.c - 1); seqDone = done; show("auto"); drawPins(P.g); setMe(MAP_PTS[oc][5], true);
      label(contName(oc), "Continent cleared!", `Next: ${contName(P.c)}`); go(contCam(oc), 0);
      at(700, () => { me.classList.remove("on"); go(worldCam(), 1000); });
      at(1600, () => { label("", "Flying to " + nice(contName(P.c)), ""); flyPlane(cen(oc), cen(P.c), 1600); });
      at(3300, () => { go(contCam(P.c), 1000); }); at(4300, () => { setMe(MAP_PTS[P.c][0], true); label(contName(P.c), `Welcome to ${nice(contName(P.c))}!`, `First stop: ${nice(CONTS[P.c][2][0])}`); try { snd("coin"); } catch (e) {} });
      at(5600, hide); }
    function playIntro(done) { seqDone = done; show("auto"); drawPins(0); setMe(MAP_PTS[0][0], false); label("", "The world tour begins", "5 continents · 30 places · 150 waves");
      go(worldCam(), 0); at(900, () => flyPlane([1.02, .25], cen(0), 1700)); at(2700, () => go(contCam(0), 1000));
      at(3700, () => { setMe(MAP_PTS[0][0], true); label("SOUTH AMERICA", "First stop: River Bank", "Waves 1–5 · the Jungle Temple waits at wave 26"); try { snd("coin"); } catch (e) {} }); at(5200, hide); }
    /* Einhängen vor dem Wellenstart */
    let busy = false;
    const _sw2 = startWave; startWave = function () { const a = arguments, self = this;
      try { if (!busy && S && S.started && !S.over && !S.nuts) { const nw = (S.wave || 0) + 1, P = wherePos(nw);
          let play = null; if (nw === 1 && !LS.get("tarnturm-mapintro")) { play = playIntro; LS.set("tarnturm-mapintro", "1"); }
          else if (nw > 1 && nw <= 150 && P.d === 0) play = P.p === 0 ? (d => playCont(nw, d)) : (d => playPlace(nw, d));
          if (play) { busy = true; const was = S.paused; S.paused = true;
            play(() => { S.paused = was; busy = false; _sw2.apply(self, a); }); return; } } } catch (e) { busy = false; }
      if (busy) return; return _sw2.apply(this, a); };
    /* Knöpfe */
    const PIN_SVG = '<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><path d="M3 6.5l5.5-2 7 2.5 5.5-2v13l-5.5 2-7-2.5-5.5 2z" fill="#9fd3c7" stroke="#3a2414" stroke-width="1.8" stroke-linejoin="round"/><path d="M8.5 4.5v13M15.5 7v13" stroke="#3a2414" stroke-width="1.4"/><path d="M12 5.2c-2 0-3.3 1.4-3.3 3.2 0 2.4 3.3 5.6 3.3 5.6s3.3-3.2 3.3-5.6c0-1.8-1.3-3.2-3.3-3.2z" fill="#ff5fa8" stroke="#3a2414" stroke-width="1.4"/><circle cx="12" cy="8.4" r="1.2" fill="#fff"/></svg>';
    { const b = document.createElement("button"); b.type = "button"; b.id = "btnMap"; b.className = "btn-small"; b.setAttribute("aria-label", "World map"); b.innerHTML = PIN_SVG;
      b.addEventListener("click", () => { try { SFX.init(); } catch (e) {} openMap(); }); document.body.appendChild(b);
      const place = () => { const h = document.getElementById("btnHs"); if (!h) return; const r = h.getBoundingClientRect(); if (!r.width) return; b.style.left = Math.round(r.left - r.width - 8) + "px"; b.style.top = Math.round(r.top) + "px"; };
      setInterval(place, 400); addEventListener("resize", place); place(); }
    { const pr = document.getElementById("btnPResume"); if (pr) { const b = document.createElement("button"); b.type = "button"; b.id = "btnPMap"; b.className = "btn-small"; b.innerHTML = PIN_SVG + "<span>WORLD MAP</span>"; pr.insertAdjacentElement("afterend", b); b.addEventListener("click", e => { e.stopPropagation(); openMap(); }); } }
    { const st = document.querySelector("#ovOver .aarStats"); if (st) { const b = document.createElement("button"); b.type = "button"; b.id = "btnOMap"; b.className = "btn-small"; st.insertAdjacentElement("afterend", b);
        b.addEventListener("click", () => { let w = 1; try { w = Math.max(1, S.wave || 1); } catch (e) {} openMap(w, "over"); });
        new MutationObserver(() => { const o = document.getElementById("ovOver"); if (o && !o.hidden) { let w = 1; try { w = Math.max(1, S.wave || 1); } catch (e) {} const P = wherePos(w); b.innerHTML = PIN_SVG + `<span>You reached <b>${nice(P.place)}</b> · map</span>`; } }).observe(document.getElementById("ovOver"), { attributes: true, attributeFilter: ["hidden"] }); } }
    addEventListener("resize", () => { if (!ov.hidden) { layout(); apply(0); } });
    window.__TT && Object.assign(window.__TT, { openMap, playPlace: w => playPlace(w, null), playCont: w => playCont(w, null), playIntro: () => playIntro(null), mapCam: () => cam });
  } catch (e) { console.warn("map", e); }
'''
i = s.rfind('})();\n</script>'); assert i > 0
s = s[:i] + js + s[i:]

css = '''<style id="v224">
/* V224 Weltkarte */
#ovMap{position:fixed;inset:0;z-index:990;background:#6faaab;overflow:hidden;-webkit-tap-highlight-color:transparent;user-select:none;-webkit-user-select:none}
#ovMap[hidden]{display:none!important}
#ovMap .mapVp{position:absolute;inset:0;overflow:hidden}
#ovMap .mapWorld{position:absolute;left:0;top:0;transform-origin:0 0;will-change:transform}
#ovMap .mapImg{position:absolute;inset:0;width:100%;height:100%;max-width:none!important;display:block;pointer-events:none}
#ovMap .mapPath{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}
#ovMap .mapPath polyline{fill:none;stroke:#3a2414;stroke-width:2.4;stroke-dasharray:2 6;stroke-linecap:round;opacity:.55;vector-effect:non-scaling-stroke}
#ovMap .mapPath polyline.done{stroke:#c98a12;opacity:.8}
#ovMap .mPin{position:absolute;width:0;height:0}
#ovMap .mPin i{position:absolute;left:-9px;top:-9px;width:18px;height:18px;border-radius:50%;border:2.5px solid #3a2414;background:#e9e2d2;box-sizing:border-box;transform:scale(var(--ik,1));box-shadow:0 2px 0 rgba(58,36,20,.6)}
#ovMap .mPin.done i{background:#ffc93c}
#ovMap .mPin.cur i{background:#ff5fa8;animation:mPulse 1.1s ease-in-out infinite}
#ovMap .mPin.star i{left:-12px;top:-12px;width:24px;height:24px;border-radius:4px;clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%);border:0;background:#3a2414}
#ovMap .mPin.star i::after{content:"";position:absolute;inset:3px;clip-path:inherit;background:#e9e2d2}
#ovMap .mPin.star.done i::after{background:#ffc93c}#ovMap .mPin.star.cur i::after{background:#ff5fa8}
#ovMap .mPin em{position:absolute;left:0;top:-14px;transform:translate(-50%,-100%) scale(var(--ik,1));transform-origin:50% 100%;white-space:nowrap;font:400 15px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.04em;color:#3a2414;background:#fff;border:2.5px solid #3a2414;border-radius:10px;padding:4px 8px 3px;box-shadow:0 2px 0 #3a2414;font-style:normal}
@keyframes mPulse{50%{box-shadow:0 0 0 6px rgba(255,95,168,.35),0 2px 0 rgba(58,36,20,.6)}}
#ovMap .mapMe{position:absolute;width:0;height:0;opacity:0;transition:opacity .25s}
#ovMap .mapMe.on{opacity:1}
#ovMap .mapMe img{position:absolute;max-width:none!important;max-height:none!important;left:-23px;top:-58px;width:46px;height:46px;object-fit:cover;object-position:50% 18%;border-radius:50%;border:3px solid #3a2414;background:#fff7e8;transform:scale(var(--ik,1));transform-origin:50% 110%;box-shadow:0 3px 0 #3a2414}
#ovMap .mapMe.hop img{animation:mHop .3s ease-in-out infinite alternate}
@keyframes mHop{to{transform:scale(var(--ik,1)) rotate(8deg)}}
#ovMap .mapPlane{position:absolute;opacity:0;font-size:38px;line-height:1;pointer-events:none;transform:translate(-50%,-50%) scale(var(--ik,1)) rotate(var(--a,0deg));filter:drop-shadow(0 6px 4px rgba(0,0,0,.3))}
#ovMap .mapPlane.on{opacity:1}
#ovMap .mapTop{position:absolute;left:12px;right:12px;top:calc(env(safe-area-inset-top,0px) + 12px);margin:0 auto;max-width:420px;background:#fff7e8;border:3px solid #3a2414;border-radius:18px;box-shadow:0 4px 0 #3a2414;padding:8px 12px 9px;text-align:center;display:grid;gap:2px;pointer-events:none;min-height:66px;box-sizing:border-box;align-content:center}
#ovMap .mapCont{font:800 11px/1 "Baloo 2",sans-serif;letter-spacing:.16em;color:#d94c8c;min-height:11px}
#ovMap .mapPlace{font:400 26px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.03em;color:#3a2414}
#ovMap .mapSub{font:700 12.5px/1.2 "Baloo 2",sans-serif;color:#7a5a3c;min-height:15px}
#ovMap .mapBar{position:absolute;left:0;right:0;bottom:calc(env(safe-area-inset-bottom,0px) + 16px);display:flex;justify-content:center;gap:10px}
#ovMap .mapBar button{min-width:120px;height:46px;border-radius:999px;border:3px solid #3a2414;background:#fff7e8;color:#3a2414;font:400 20px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.05em;box-shadow:0 3px 0 #3a2414;cursor:pointer;padding:0 16px}
#ovMap .mapBar .mapClose{background:#ff8fc4}
#ovMap.auto .mapBar{display:none}
#ovMap .mapSkip{display:none;position:absolute;left:0;right:0;bottom:calc(env(safe-area-inset-bottom,0px) + 18px);text-align:center;font:800 12px/1 "Baloo 2",sans-serif;letter-spacing:.14em;color:rgba(255,255,255,.85);text-shadow:0 1px 2px rgba(0,0,0,.5);text-transform:uppercase}
#ovMap.auto .mapSkip{display:block}
#btnMap{display:none;position:fixed!important;left:228px;top:auto;bottom:auto;width:52px!important;height:52px!important;min-width:0!important;min-height:0!important;padding:0!important;place-items:center;z-index:60}
body:has(#ovStart:not([hidden])):has(#startMain:not([hidden])) #btnMap{display:grid!important}
body:has(#ovStart:not([hidden])):has(.overlay.win:not([hidden])) #btnMap,body:has(#ovAlbum:not([hidden])) #btnMap,body.mapUp #btnMap{display:none!important}
#btnPMap{display:flex!important;flex-direction:row!important;line-height:1!important;align-items:center;justify-content:center;gap:6px;height:40px!important;font-size:15px!important;width:100%!important;margin:0!important}
#btnPMap svg,#btnOMap svg{display:block!important;width:22px!important;height:22px!important;flex:0 0 auto}
#btnOMap{display:flex!important;flex-direction:row!important;line-height:1!important;overflow:hidden;align-items:center;justify-content:center;gap:6px;width:100%;height:36px;min-height:0!important;margin:8px 0 0!important;font-size:13.5px!important;padding:0 10px!important}
#btnOMap svg{width:22px;height:22px;flex:0 0 auto}
#btnOMap span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
