"""V250: Sanfte Vibration (Martin 05.11. 09:56): nicht bei Stein/Abschuss; leicht bei geräumter Reihe (2–3 Reihen etwas mehr),
stärker bei verlorenem Leben, Boss-Signal und Game over. Ziel 5–7 pro Minute: leichte Impulse höchstens 7 je 60 s und frühestens 4 s
nach dem letzten; starke immer (mind. 0,3 s Abstand). Schalter «Vibration on/off» im Pausemenü (nur wenn das Gerät vibrieren kann;
im iPhone-Browser gibt es keine Vibration). Gespeichert in tarnturm-vib.
Einarmiger Bandit als eigener Testpunkt im Dev-Menü «Special waves» (Eintrag «Lucky Supply»): startet ein Testspiel
und öffnet den Automaten sofort. (Daneben bleibt der Knopf «Bandit» in der Dev-Leiste.)"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V249";', 'const GAME_VER = "V250";')
rep('<button id="pvMute" class="btn-small">Mute</button></div>', '<button id="pvMute" class="btn-small">Mute</button><button id="pvVib" class="btn-small" hidden>Vibration: on</button></div>')
rep('["Ten-ton drop", "IN POCKET · WAVE 5", 5, "ton"]]', '["Ten-ton drop", "IN POCKET · WAVE 5", 5, "ton"], ["Lucky Supply", "BANDIT · ONE FREE SPIN", 3, "bandit"]]')
js = '''
  /* V250: Testpunkt «Lucky Supply» im Specials-Menü */
  try { document.getElementById("specList").addEventListener("click", e => { const bt = e.target.closest("button[data-i]"); if (!bt) return; const it = SPECIALS[+bt.dataset.i]; if (!it || it[3] !== "bandit") return;
      e.stopImmediatePropagation(); e.preventDefault(); try { SFX.init(); } catch (er) {} devJump(3); setTimeout(() => { try { window.__TT.bandit.open(true); } catch (er) {} }, 2600); }, true); } catch (e) { console.error("specBandit", e); }
  /* sanfte Vibration */
  try { (() => { const can = typeof navigator.vibrate === "function"; const vb = document.getElementById("pvVib");
      let on = LS.get("tarnturm-vib") !== "0"; const paint = () => { if (vb) { vb.hidden = !can; vb.textContent = "Vibration: " + (on ? "on" : "off"); } }; paint();
      const hist = []; let lastAny = 0, lastLight = 0;
      function buzz(pat, strong) { if (!can || !on || document.hidden) return; const now = performance.now(); if (now - lastAny < 300) return;
        while (hist.length && now - hist[0] > 60000) hist.shift();
        if (!strong && (hist.length >= 7 || now - lastLight < 4000)) return;
        try { navigator.vibrate(pat); } catch (e) { return; } hist.push(now); lastAny = now; if (!strong) lastLight = now; }
      if (vb) vb.addEventListener("click", e => { e.stopPropagation(); on = !on; LS.set("tarnturm-vib", on ? "1" : "0"); paint(); if (on) buzz([25], true); });
      window.__vib = buzz;
      let pl = null, pv = null, pHack = 0, pOver = false;
      setInterval(() => { if (!S || !S.started) { pl = pv = null; pOver = false; return; }
        if (pl != null && S.lines > pl && !S.over) { const d = S.lines - pl; buzz(d >= 3 ? [20, 40, 20] : [d === 2 ? 22 : 14], false); }
        if (pv != null && S.lives < pv && !S.over) buzz([45, 60, 45], true);
        if ((S.hackOfferUntil || 0) > performance.now() && S.hackOfferUntil !== pHack) { pHack = S.hackOfferUntil; buzz([35, 50, 35], true); }
        if (S.over && !pOver) buzz([60, 80, 60], true);
        pl = S.lines; pv = S.lives; pOver = !!S.over; }, 120);
      window.__TT && (window.__TT.vib = { buzz, get hist() { return hist.slice(); } });
    })(); } catch (e) { console.error("vib", e); }
'''
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
