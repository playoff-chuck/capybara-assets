# V682 (Martin 12.11. 19:24): Ortswechsel-Übergang anders – alles über Schwarz:
# 0–1,5 s Musik klingt aus · 1,5–4,5 s Streifen-Feier mit Klängen (doppelt so lang) · Streifen weg ·
# Level blendet nach Schwarz aus (ohne Musik) · Karte blendet sanft ein · Flug · Landung · Karte blendet nach Schwarz aus ·
# Level blendet wieder ein · «WAVE n · GET READY».
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
rep('#celHost{position:fixed;inset:0;z-index:989;pointer-events:none;overflow:hidden}',
    '#celHost{position:fixed;inset:0;z-index:989;pointer-events:none;overflow:hidden}#celBlack{position:fixed;inset:0;z-index:988;background:#000;opacity:0;pointer-events:none;transition:opacity .8s ease}#celBlack.on{opacity:1}#ovMap.fadeIn2{animation:mapFadeIn 1.1s ease both}   /* V682 */')
a = s.index('    function playPlace(w, done) {'); z0 = 'at(6200, () => { ov.classList.remove("q"); hide(); }); }'; z = s.index(z0, a) + len(z0)
assert s.count('    function playPlace(w, done) {') == 1 and z - a < 2600, (z - a)
new = r'''    function playPlace(w, done) { const P = posOf(w), prev = MAP_PTS[P.c][P.p - 1], nxt = MAP_PTS[P.c][P.p], oldN = nice(CONTS[P.c][2][P.p - 1]), newN = nice(CONTS[P.c][2][P.p]);   /* V682: alles über Schwarz */
      seqDone = done; let host = document.getElementById("celHost"); if (!host) { host = document.createElement("div"); host.id = "celHost"; document.body.appendChild(host); }
      let blk = document.getElementById("celBlack"); if (!blk) { blk = document.createElement("div"); blk.id = "celBlack"; document.body.appendChild(blk); }
      try { if (typeof TP !== "undefined" && TP.el && TP.key && !TP.el.paused) tpFade(0.0001, 1.5); else if (SFX.music && SFX.music.dim) SFX.music.dim(0.02); } catch (e) {}   /* 0–1,5 s Musik klingt aus */
      let end = null;
      at(1500, () => { end = celebrate(`${oldN.toUpperCase()} CLEARED!`, `Place ${P.g} of 30 done · onward!`, host); });   /* 1,5–4,5 s Streifen + Klänge */
      at(3000, () => { fx("powerup"); setTimeout(() => fx("coin"), 260); });
      at(4500, () => { end && end(); });   /* Streifen weg */
      at(5100, () => blk.classList.add("on"));   /* 5,1–5,9 s Level blendet nach Schwarz aus, keine Musik */
      at(6000, () => { show("auto"); ov.classList.add("fadeIn2"); drawPins(P.g - 1); setMe(prev, true); go(contCam(P.c), 0);
        label(contName(P.c), `Next stop: ${newN}`, P.p === 5 ? "The landmark · the boss lives here" : `Waves ${w}–${w + 4}`); });   /* 6,0–7,1 s Karte blendet sanft ein */
      at(7200, () => { ov.classList.remove("fadeIn2"); fx("engine"); whoosh(); me.classList.add("fly"); hopMe(prev, nxt, 2600); });   /* 7,2–9,8 s Flug */
      at(8300, whoosh);
      at(9800, () => { me.classList.remove("fly"); drawPins(P.g); const pin = pinsEl.querySelector(`.mPin[data-g="${P.g}"]`); pin && pin.classList.add("pop");
        label(contName(P.c), `Welcome to ${newN}!`, P.p === 5 ? "The landmark · the boss lives here" : `Waves ${w}–${w + 4}`); fx("tonHit"); setTimeout(() => fx("powerup"), 120); setTimeout(() => fx("coin"), 420); });   /* 9,8–10,8 s Landung */
      at(10800, () => ov.classList.add("fadeOut", "q"));   /* 10,8–11,4 s Karte blendet nach Schwarz aus */
      at(11450, () => { ov.classList.remove("q"); blk.classList.remove("on"); hide(); }); }   /* Level blendet wieder ein */'''
s = s[:a] + new + s[z:]
rep('const GAME_VER = "V681"', 'const GAME_VER = "V682"')
open(dst, "w", encoding="utf8").write(s); print("ok", len(s))
