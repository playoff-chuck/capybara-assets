"""V209: Spielstand nie mehr versehentlich weg – gibt es einen gespeicherten Lauf, ist CONTINUE der große Knopf
(genau dort weiter: Welle, Punkte, Türme, Gold …); ein neuer Lauf nur über «New world tour» mit Doppeltipp.
Pausemenü: Restart-Warnung wieder sichtbar."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('const GAME_VER = "V208";') == 1
s = s.replace('const GAME_VER = "V208";', 'const GAME_VER = "V209";')
js = '''
  /* V209: gespeicherter Lauf → CONTINUE vorne, neuer Lauf nur mit Bestätigung */
  try { const res = document.getElementById("btnResume");
    let nb = document.getElementById("btnNewTour");
    if (res && !nb) { nb = document.createElement("button"); nb.id = "btnNewTour"; nb.type = "button"; nb.className = "btn-small newTour"; nb.textContent = "New world tour"; res.insertAdjacentElement("afterend", nb);
      let arm = 0; nb.addEventListener("click", e => { e.stopPropagation(); const now = performance.now();
        if (!arm || now - arm > 3000) { arm = now; nb.textContent = "Tap again \\u2013 your current run ends"; nb.classList.add("armed"); try { snd("uiTap"); } catch (er) {}
          setTimeout(() => { if (performance.now() - arm >= 3000) { arm = 0; nb.textContent = "New world tour"; nb.classList.remove("armed"); } }, 3100); return; }
        arm = 0; nb.textContent = "New world tour"; nb.classList.remove("armed"); try { LS.del("tarnturm-save"); } catch (er) {}
        const p = document.querySelector("#modeList button"); if (p) p.click(); }); }
    setInterval(() => { const has = !!(res && !res.hidden); document.body.classList.toggle("hasSave", has); if (nb) nb.hidden = !has; }, 300);
    const rb = document.getElementById("btnPRestart"), card = () => document.querySelector("#ovPause .pCard");
    if (rb) new MutationObserver(() => { const c = card(); if (c) c.classList.toggle("rArmed", /again/i.test(rb.textContent)); }).observe(rb, { childList: true, characterData: true, subtree: true });
  } catch (e) {}
'''
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
css = '''<style id="v209">
body.hasSave #modeList{display:none!important}
body.hasSave #btnResume{position:relative;z-index:20}
#btnNewTour{display:block;position:relative;z-index:20;margin:8px auto 0!important;height:34px!important;padding:0 16px!important;font-size:13px!important;background:rgba(255,248,232,.92)!important}
#btnNewTour[hidden]{display:none!important}
#btnNewTour.armed{background:#ffe1e1!important;border-color:#b8402c!important;color:#7a1f12!important}
#ovPause .pCard.rArmed .pauseHint{display:block!important;margin:0!important;text-align:center;font-size:12px!important;color:#b8402c!important}
#ovPause .pRow button{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
