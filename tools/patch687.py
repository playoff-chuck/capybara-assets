# V687 (Martin 12.11. 19:58): Ortswechsel – die Streifen auf Schwarz bleiben stehen (Verschnaufpause), unten steht gedämpft
# «TAP TO CONTINUE». Tippen (oder spätestens 30 s nach Beginn der Streifen) → weiter: 1,5 s Ausklingen, Streifen blenden
# zu Schwarz aus, Karte blendet ein, Flug, Landung, zurück über Schwarz. Platz für die Feier-Musik: window.__celMus(true/false).
import sys, os, json
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
rep('#ovMap.fadeIn2{animation:mapFadeIn 1.1s ease both}',
    '#ovMap.fadeIn2{animation:mapFadeIn 1.1s ease both}#celHost.tap{pointer-events:auto;cursor:pointer}#celHost .celTap{position:absolute;left:0;right:0;bottom:calc(env(safe-area-inset-bottom,0px) + 34px);z-index:8;text-align:center;font:700 15px/1.2 "Baloo 2",Nunito,system-ui,sans-serif;letter-spacing:.16em;color:rgba(255,255,255,.45);opacity:0;transition:opacity .9s ease;pointer-events:none}#celHost .celTap.on{opacity:1;animation:celTapP 2.4s ease-in-out .9s infinite}@keyframes celTapP{50%{opacity:.45}}   /* V687 */')
a = s.index('    function playPlace(w, done) {'); z0 = 'blk.classList.remove("on"); hide(); }); }   /* Level blendet wieder ein */'; z = s.index(z0, a) + len(z0)
assert s.count('    function playPlace(w, done) {') == 1 and z - a < 3600, (z - a)
new = r'''    /* V687: Feier-Musik (Chor) während der Streifen – blendet ein, wenn die Level-Musik aus ist, und in 1,5 s aus */
    const celMus = (() => { let a = null, iv = 0, act = false;
      const mk = () => { if (!a) { a = new Audio("sfx/place_choir.mp3?v=687"); a.preload = "auto"; } return a; };
      const ramp = (to, sec, then) => { clearInterval(iv); if (!a) return; const from = a.volume, n = Math.max(1, Math.round(sec * 30)); let i = 0; iv = setInterval(() => { i++; try { a.volume = Math.max(0, Math.min(1, from + (to - from) * i / n)); } catch (e) {} if (i >= n) { clearInterval(iv); then && then(); } }, 33); };
      try { setTimeout(() => { try { mk().load(); } catch (e) {} }, 15000); } catch (e) {}
      document.addEventListener("visibilitychange", () => { try { if (!a) return; if (document.hidden) a.pause(); else if (act) { const p = a.play(); p && p.catch && p.catch(() => {}); } } catch (e) {} });
      return on => { try { if (on) { if (!(SFX.music && SFX.music.on) || SFX.muted) return; mk(); act = true; try { a.currentTime = 0; } catch (e) {} a.volume = 0; const p = a.play(); p && p.catch && p.catch(() => {});
            ramp(Math.max(0.05, Math.min(1, (typeof TP_VOL === "function" ? TP_VOL() : 0.4) * 1.15)), 1.2); }
          else { if (!a || !act) return; act = false; ramp(0, 1.5, () => { try { a.pause(); } catch (e) {} }); } } catch (e) {} }; })();
    window.__celMus = celMus;
    function playPlace(w, done) { const P = posOf(w), prev = MAP_PTS[P.c][P.p - 1], nxt = MAP_PTS[P.c][P.p], oldN = nice(CONTS[P.c][2][P.p - 1]), newN = nice(CONTS[P.c][2][P.p]);   /* V687: Streifen warten auf Tippen */
      seqDone = done; let host = document.getElementById("celHost"); if (!host) { host = document.createElement("div"); host.id = "celHost"; document.body.appendChild(host); }
      let blk = document.getElementById("celBlack"); if (!blk) { blk = document.createElement("div"); blk.id = "celBlack"; document.body.appendChild(blk); }
      try { if (typeof TP !== "undefined" && TP.el && TP.key && !TP.el.paused) tpFade(0.0001, 1.5); else if (SFX.music && SFX.music.dim) SFX.music.dim(0.02); } catch (e) {}   /* 0–1,5 s Musik klingt aus */
      let end = null, gone = false, tap = null; const mus = on => { try { window.__celMus && window.__celMus(on); } catch (e) {} };
      const cont = () => { if (gone) return; gone = true; host.classList.remove("tap"); host.onclick = null; if (tap) tap.classList.remove("on"); try { snd("uiTap"); } catch (e) {} mus(false);   /* weiter: 1,5 s Ausklingen */
        const T0 = 1500;
        at(T0, () => { end && end(); if (tap) { tap.remove(); tap = null; } });   /* Streifen blenden zu Schwarz aus */
        at(T0 + 800, () => { show("auto"); ov.classList.add("fadeIn2"); drawPins(P.g - 1); setMe(prev, true); go(contCam(P.c), 0);
          label(contName(P.c), `Next stop: ${newN}`, P.p === 5 ? "The landmark · the boss lives here" : `Waves ${w}–${w + 4}`); });   /* Karte blendet aus dem Schwarz ein */
        at(T0 + 2000, () => { ov.classList.remove("fadeIn2"); fx("engine"); whoosh(); me.classList.add("fly"); hopMe(prev, nxt, 2600); });   /* Flug 2,6 s */
        at(T0 + 3100, whoosh);
        at(T0 + 4600, () => { me.classList.remove("fly"); drawPins(P.g); const pin = pinsEl.querySelector(`.mPin[data-g="${P.g}"]`); pin && pin.classList.add("pop");
          label(contName(P.c), `Welcome to ${newN}!`, P.p === 5 ? "The landmark · the boss lives here" : `Waves ${w}–${w + 4}`); fx("tonHit"); setTimeout(() => fx("powerup"), 120); setTimeout(() => fx("coin"), 420); });   /* Landung 1 s */
        at(T0 + 5600, () => ov.classList.add("fadeOut", "q"));   /* Karte blendet nach Schwarz aus */
        at(T0 + 6250, () => { ov.classList.remove("q"); blk.style.transitionDuration = ""; blk.classList.remove("on"); hide(); }); };   /* Level blendet wieder ein */
      at(1500, () => { end = celebrate(`${oldN.toUpperCase()} CLEARED!`, `Place ${P.g} of 30 done · onward!`, host); mus(true);   /* ab 1,5 s Streifen + Klänge (+ Feier-Musik) */
        blk.style.transitionDuration = "2.25s"; void blk.offsetWidth; blk.classList.add("on"); });   /* 1,5–3,75 s Spielscreen blendet hinter den Streifen nach Schwarz */
      at(3750, () => { fx("powerup"); setTimeout(() => fx("coin"), 260);
        tap = document.createElement("div"); tap.className = "celTap"; tap.textContent = "TAP TO CONTINUE"; host.appendChild(tap); requestAnimationFrame(() => requestAnimationFrame(() => tap && tap.classList.add("on")));
        host.classList.add("tap"); host.onclick = e => { try { e.stopPropagation(); } catch (x) {} cont(); }; });   /* ab 3,75 s: nur Streifen auf Schwarz, Tippen = weiter */
      at(31500, cont); }   /* spätestens 30 s nach Beginn der Streifen von selbst weiter */'''
s = s[:a] + new + s[z:]
rep('const GAME_VER = "V686"', 'const GAME_VER = "V687"')
open(dst, "w", encoding="utf8").write(s)
TR = {"ru": "НАЖМИ, ЧТОБЫ ПРОДОЛЖИТЬ", "es": "TOCA PARA CONTINUAR", "pt": "TOQUE PARA CONTINUAR", "de": "TIPPEN ZUM WEITERSPIELEN"}
for l, v in TR.items():
    p = os.path.join(os.path.dirname(dst), "lang", l + ".json"); t = open(p, encoding="utf8").read().rstrip()
    assert t.endswith("}") and '"TAP TO CONTINUE"' not in t, l
    t = t[:-1].rstrip() + ',\n"TAP TO CONTINUE": ' + json.dumps(v, ensure_ascii=False) + '\n}\n'; json.loads(t); open(p, "w", encoding="utf8").write(t)
print("ok", len(s))
