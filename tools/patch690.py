# V690 (Martin 12.11. 21:34 «2»): Kontinentwechsel (W30/60/90/120) bekommt dieselbe Verschnaufpause wie der Ortswechsel:
# Level-Musik aus -> Streifen + Hymne, Spielscreen blendet nach Schwarz -> «TAP TO CONTINUE» (Tippen oder 30 s) ->
# 1,5 s Hymne aus -> Streifen zu Schwarz -> Wegweiser bzw. Weltkarte ueber Schwarz -> nach der Karte Level-Musik 2 s ein.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
NEW = r'''    window.__celMus = celMus;
    /* V690: Kontinentwechsel – dieselbe Verschnaufpause wie beim Ortswechsel (Streifen + Hymne über Schwarz, Tippen = weiter); danach Wegweiser/Karte über Schwarz */
    window.__contPause = (name, c, then) => {
      let host = document.getElementById("celHost"); if (!host) { host = document.createElement("div"); host.id = "celHost"; document.body.appendChild(host); }
      let blk = document.getElementById("celBlack"); if (!blk) { blk = document.createElement("div"); blk.id = "celBlack"; document.body.appendChild(blk); }
      let hadTP = false, musBack = false, end = null, gone = false, tap = null, iv = 0; clearTimeout(window.__celHushT);
      const lvlBack = () => { if (musBack) return; musBack = true; clearTimeout(window.__celHushT); window.__tpHush = false;
        try { if (hadTP && TP.el && TP.key && !TP.paused && SFX.music.on && !document.hidden && TP.el.paused) { TP.el.volume = 0; const p = TP.el.play(); if (p && p.catch) p.catch(() => {}); tpFade(0.5, 2.0); } } catch (e) {} };
      const blkOff = () => { try { blk.style.transitionDuration = ""; blk.classList.remove("on"); document.body.classList.remove("contBlk"); } catch (e) {} };
      try { if (typeof TP !== "undefined" && TP.el && TP.key && !TP.el.paused) { hadTP = true; window.__tpHush = true; tpFade(0.0001, 1.5); setTimeout(() => { try { if (window.__tpHush && !musBack) TP.el.pause(); } catch (e) {} }, 1560); window.__celHushT = setTimeout(lvlBack, 600000); }
            else if (SFX.music && SFX.music.dim) SFX.music.dim(0.02); } catch (e) {}
      const mus = on => { try { window.__celMus && window.__celMus(on); } catch (e) {} };
      document.body.classList.add("contBlk"); host.classList.add("tap"); host.onclick = e => { try { e.stopPropagation(); } catch (x) {} };   /* bis «TAP TO CONTINUE» nichts durchlassen */
      const cont = () => { if (gone) return; gone = true; host.onclick = e => { try { e.stopPropagation(); } catch (x) {} }; if (tap) tap.classList.remove("on"); try { snd("uiTap"); } catch (e) {} mus(false);
        setTimeout(() => { try { end && end(); } catch (e) {} if (tap) { tap.remove(); tap = null; } }, 1500);   /* Streifen blenden zu Schwarz aus */
        setTimeout(() => { host.classList.remove("tap"); host.onclick = null;
          try { then && then(); } catch (e) { console.error("contPause", e); }
          try { if (document.getElementById("ovSign").hidden && S && !S.nuts) window.__fromSign = true; } catch (e) {}   /* ohne Wegweiser: keine zweite Feier auf der Karte */
          let sawMap = false; const t0 = performance.now();
          iv = setInterval(() => { try { const up = document.body.classList.contains("mapUp"), sign = !document.getElementById("ovSign").hidden, dt = performance.now() - t0;
              if (up && !sawMap) { sawMap = true; setTimeout(blkOff, 300); }   /* Karte liegt über dem Schwarz */
              const out = sawMap ? !up : (!S || !S.started || S.over || !!S.nuts || (!sign && dt > 4000) || dt > 600000);
              if (out) { clearInterval(iv); blkOff(); setTimeout(lvlBack, 400); } } catch (e) { clearInterval(iv); blkOff(); lvlBack(); } }, 200); }, 2300); };
      setTimeout(() => { end = celebrate(`${name} CLEARED!`, `Continent ${c + 1} of 5 · the world tour goes on`, host); mus(true);
        blk.style.transitionDuration = "2.25s"; void blk.offsetWidth; blk.classList.add("on"); }, 1500);
      setTimeout(() => { if (gone) return; fx("powerup"); setTimeout(() => fx("coin"), 260);
        tap = document.createElement("div"); tap.className = "celTap"; tap.textContent = "TAP TO CONTINUE"; host.appendChild(tap); requestAnimationFrame(() => requestAnimationFrame(() => tap && tap.classList.add("on")));
        host.onclick = e => { try { e.stopPropagation(); } catch (x) {} cont(); }; }, 3750);
      setTimeout(cont, 31500); };'''
rep('    window.__celMus = celMus;', NEW)
rep('  window.__contCel = (name, c, then) => {\n', '  window.__contCel = (name, c, then) => { if (window.__contPause) return window.__contPause(name, c, then);   /* V690 */\n')
rep('#celBlack.on{opacity:1}', '#celBlack.on{opacity:1}body.contBlk #ovSign{z-index:989}')   # Wegweiser liegt ueber dem Schwarz, unter der Karte
rep('const GAME_VER = "V689"', 'const GAME_VER = "V690"')
open(dst, "w", encoding="utf8").write(s); print("ok", len(s))
