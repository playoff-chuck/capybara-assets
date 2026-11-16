import sys
# V729 (Martin 16.11.2026, Feedback Sergej, Firefox/MacBook):
# 1) Tutorial «Baue einen Turm»: Steine halten höchstens 12 s (und solange der Baumodus offen ist), dann fallen sie wieder.
#    V727 hielt sie unbegrenzt an – wer nicht baute, sah keine neuen Steine mehr.
# 2) WASD-Steuerung (über e.code, unabhängig von der Tastaturbelegung): W drehen, A/D links/rechts, S runter; Tasche jetzt Q.
# 3) Weniger Last am Desktop: höchstens 60 Bilder/s (120-Hz-Bildschirme), Desktop-Auflösung max. 1,5×.
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V728";', 'const GAME_VER = "V729";')
rep('function tutBuildHold() { try { return !!(TUT.on && (TUT_STEPS[TUT.step] || {}).ar === "build"); } catch (e) { return false; } }',
    'function tutBuildHold() { try { if (!(TUT.on && (TUT_STEPS[TUT.step] || {}).ar === "build")) { window.__tbh0 = 0; return false; } const n = performance.now(); if (!window.__tbh0) window.__tbh0 = n; return S.mode === "build" || n - window.__tbh0 < 12000; } catch (e) { return false; } }   /* V729: höchstens 12 s */')
rep('''  const k = e.key;
  if (S.duel && !["ArrowLeft"''', '''  const k = ({ KeyW: "ArrowUp", KeyA: "ArrowLeft", KeyS: "ArrowDown", KeyD: "ArrowRight", KeyQ: "s" })[e.code] || (e.key === "s" || e.key === "S" ? "" : e.key);   /* V729: WASD, Tasche auf Q */
  if (S.duel && !["ArrowLeft"''')
rep('if (window.__minF && now - last < 30) { requestAnimationFrame(loop); return; }',
    'if (now - last < (window.__minF ? 30 : 12)) { requestAnimationFrame(loop); return; }   /* V729: höchstens 60 Bilder/s */')
rep('function resize() {\n', 'window.__deskF = (() => { try { return matchMedia("(pointer: fine)").matches && !(navigator.maxTouchPoints > 0); } catch (e) { return false; } })();   /* V729 */\nfunction resize() {\n')
rep(': 3, window.devicePixelRatio || 1);   /* V658 */', ': (window.__deskF ? 1.5 : 3), window.devicePixelRatio || 1);   /* V658 */   /* V729: Desktop max 1,5 */')
open(dst, "w", encoding="utf-8").write(s)
print("ok V729")
