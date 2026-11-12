# V681 (Martin 12.11. 18:14 zugestimmt): Ortswechsel neu – Feier 1,5 s auf dem Spielfeld, weiche Blende zur Karte,
# Flug sofort, 1 s Landung, weiche Blende zurück, «WAVE n · GET READY» 1,3 s vor dem Wellenstart.
# Dazu Test-Link ?test=eNN: springt in Welle NN und beendet sie nach 5 s (zeigt den Übergang zur nächsten Welle).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
# CSS der Feier auch für die Ebene über dem Spielfeld
for k, n in [("mapCel", 10), ("celConf", 2), ("celRays", 4), ("celTxt", 6)]:
    assert s.count("#ovMap ." + k) == n, (k, s.count("#ovMap ." + k)); s = s.replace("#ovMap ." + k, ":is(#ovMap,#celHost) ." + k)
rep('#ovMap[hidden]{display:none!important}', '#ovMap[hidden]{display:none!important}#ovMap.fadeIn{animation:mapFadeIn .5s ease both}@keyframes mapFadeIn{from{opacity:0}to{opacity:1}}#ovMap.fadeOut.q{transition-duration:.6s}#celHost{position:fixed;inset:0;z-index:989;pointer-events:none;overflow:hidden}   /* V681 */')
# celebrate mit wählbarer Ebene
rep('function celebrate(title, sub) { const c = document', 'function celebrate(title, sub, host) { host = host || ov; const c = document')
rep('ov.appendChild(c); ov.classList.add("cel");', 'host.appendChild(c); ov.classList.add("cel");')
old = r'''    function playPlace(w, done) { const P = posOf(w), prev = MAP_PTS[P.c][P.p - 1], nxt = MAP_PTS[P.c][P.p], oldN = nice(CONTS[P.c][2][P.p - 1]), newN = nice(CONTS[P.c][2][P.p]);
      seqDone = done; show("auto"); drawPins(P.g - 1); setMe(prev, true); go(contCam(P.c), 0);
      label(contName(P.c), `Next stop: ${newN}`, P.p === 5 ? "The landmark · the boss lives here" : `Waves ${w}–${w + 4}`);
      const end = celebrate(`${oldN.toUpperCase()} CLEARED!`, `Place ${P.g} of 30 done · onward!`);
      at(2300, end);
      at(3200, () => { fx("engine"); whoosh(); me.classList.add("fly"); hopMe(prev, nxt, 2600); });
      at(4300, whoosh);
      at(5850, () => { me.classList.remove("fly"); drawPins(P.g); const pin = pinsEl.querySelector(`.mPin[data-g="${P.g}"]`); pin && pin.classList.add("pop");
        label(contName(P.c), `Welcome to ${newN}!`, P.p === 5 ? "The landmark · the boss lives here" : `Waves ${w}–${w + 4}`); fx("tonHit"); setTimeout(() => fx("powerup"), 120); setTimeout(() => fx("coin"), 420); });
      at(8600, hide); }'''
new = r'''    function playPlace(w, done) { const P = posOf(w), prev = MAP_PTS[P.c][P.p - 1], nxt = MAP_PTS[P.c][P.p], oldN = nice(CONTS[P.c][2][P.p - 1]), newN = nice(CONTS[P.c][2][P.p]);   /* V681: neuer Ablauf */
      seqDone = done; let host = document.getElementById("celHost"); if (!host) { host = document.createElement("div"); host.id = "celHost"; document.body.appendChild(host); }
      const end = celebrate(`${oldN.toUpperCase()} CLEARED!`, `Place ${P.g} of 30 done · onward!`, host);   /* 0–1,5 s Feier auf dem Spielfeld */
      at(1500, () => { show("auto"); ov.classList.add("fadeIn"); drawPins(P.g - 1); setMe(prev, true); go(contCam(P.c), 0);
        label(contName(P.c), `Next stop: ${newN}`, P.p === 5 ? "The landmark · the boss lives here" : `Waves ${w}–${w + 4}`); end(); });   /* 1,5–2,0 s Blende */
      at(2000, () => { ov.classList.remove("fadeIn"); fx("engine"); whoosh(); me.classList.add("fly"); hopMe(prev, nxt, 2600); });   /* 2,0–4,6 s Flug */
      at(3100, whoosh);
      at(4600, () => { me.classList.remove("fly"); drawPins(P.g); const pin = pinsEl.querySelector(`.mPin[data-g="${P.g}"]`); pin && pin.classList.add("pop");
        label(contName(P.c), `Welcome to ${newN}!`, P.p === 5 ? "The landmark · the boss lives here" : `Waves ${w}–${w + 4}`); fx("tonHit"); setTimeout(() => fx("powerup"), 120); setTimeout(() => fx("coin"), 420); });   /* 4,6–5,6 s Landung */
      at(5600, () => ov.classList.add("fadeOut", "q"));   /* 5,6–6,2 s Blende zurück */
      at(6200, () => { ov.classList.remove("q"); hide(); }); }'''
rep(old, new)
rep('play(() => { S.paused = was; S.mapShow = false; busy = false; if (P.p === 0) { S.mapDoneFor = nw; S.waveCD = 6; return; } _sw2.apply(self, a); }); return; }',
    'play(() => { S.paused = was; S.mapShow = false; if (P.p === 0) { busy = false; S.mapDoneFor = nw; S.waveCD = 6; return; }\n              try { wowBanner(T(`WAVE ${nw}`), T("GET READY")); } catch (e) {} setTimeout(() => { busy = false; _sw2.apply(self, a); }, 1300); }); return; }   /* V681: 1,3 s «WAVE n · GET READY» */')
# Test-Link ?test=eNN
rep('if (q && /^w\\d{1,3}$/.test(q) && +q.slice(1) >= 1 && +q.slice(1) <= 150) map[q] = +q.slice(1);',
    'if (q && /^[we]\\d{1,3}$/.test(q) && +q.slice(1) >= 1 && +q.slice(1) <= 150) map[q] = +q.slice(1);   /* V681: eNN = Welle NN endet nach 5 s */')
rep('devJump(map[q], /^w\\d/.test(q) ? "" : q.replace(/\\d$/, ""));',
    'devJump(map[q], /^[we]\\d/.test(q) ? "" : q.replace(/\\d$/, "")); if (/^e\\d/.test(q)) { S.waveCD = 1; let t0 = 0; const ev = setInterval(() => { try { if (!S || !S.started || S.over) { clearInterval(ev); return; } if (!S.inWave || S.paused) return; if (!t0) t0 = performance.now(); if (performance.now() - t0 > 5000) { clearInterval(ev); S.toSpawn = 0; S.monsters.length = 0; setTimeout(() => { try { if (!S.inWave) S.waveCD = Math.min(S.waveCD, 1.5); } catch (e) {} }, 400); } } catch (e) { clearInterval(ev); } }, 250); }   /* V681 */')
rep('const GAME_VER = "V680"', 'const GAME_VER = "V681"')
open(dst, "w", encoding="utf8").write(s); print("ok", len(s))
