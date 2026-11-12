#!/usr/bin/env python3
# V667 (Martin 12.11. 15:51): dritte Grafikstufe «MINIMAL» für sehr alte Handys.
#  Stufen: FULL (alles) → LITE (V658) → MINIMAL: Schärfe 1-fach, Bildrate fest 30, höchstens 12 Partikel,
#  keine Himmel-/DJ-Animationen, keine Outfit-Effekte, keine Weichzeichner.
#  Automatik: Start auf schwacher Hardware (≤ 2 Kerne / ≤ 2 GB) gleich MINIMAL. Im LITE-Modus fällt es auf MINIMAL,
#  wenn ~5 s am Stück unter 25 FPS. Aus MINIMAL zurück auf LITE, wenn 2 min lang die 30 FPS sicher gehalten werden
#  (gleiche Sperrzeiten/Höchstzahl wie V665). General sagt jeden Wechsel an; Antippen → FULL.
#  Einstellungen: «GRAPHICS» schaltet FULL → LITE → MINIMAL → FULL.
import sys, os, re
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V666";', 'const GAME_VER = "V667";')
# Grundfunktionen
rep('function fxOn() { const p = fxPref(); return p !== "off" && p !== "auto-off"; }',
    'function fxOn() { const p = fxPref(); return p !== "off" && p !== "auto-off" && p !== "min" && p !== "auto-min"; }\nfunction minOn() { const p = fxPref(); return p === "min" || p === "auto-min"; }   /* V667 */')
rep('function liteApply() { try { document.body.classList.toggle("lite", liteOn()); } catch (e) {}',
    'function liteApply() { try { document.body.classList.toggle("lite", liteOn()); document.body.classList.toggle("minimal", minOn()); window.__minF = minOn(); } catch (e) {}')
i = s.find('function fxLabel() {'); j = s.find('}', s.find('textContent', i)) + 1
s = s[:i] + 'function fxLabel() { const b = $("setFx"); if (!b) return; const p = fxPref(); b.textContent = "GRAPHICS: " + (fxOn() ? "FULL" : minOn() ? (p === "auto-min" ? "MINIMAL (AUTO)" : "MINIMAL") : (p === "auto-off" ? "LITE (AUTO)" : "LITE")); }' + s[j:]
# Einstellungen: drei Stufen
rep('localStorage.setItem("capy-fx", on ? "off" : "on")', 'localStorage.setItem("capy-fx", on ? "off" : minOn() ? "on" : "min")')
# Bildschärfe, Partikel, 30 FPS
rep('DPR = Math.min((typeof liteOn === "function" && liteOn()) ? (FX_WEAK ? 1.5 : 2) : 3,', 'DPR = Math.min((typeof minOn === "function" && minOn()) ? 1 : (typeof liteOn === "function" && liteOn()) ? (FX_WEAK ? 1.5 : 2) : 3,')
rep('if (liteOn() && S && S.fx && S.fx.length > 36) S.fx.splice(0, S.fx.length - 36);', 'const cap = minOn() ? 12 : 36; if (liteOn() && S && S.fx && S.fx.length > cap) S.fx.splice(0, S.fx.length - cap);')
rep('function loop(now) {\n  const dt = ', 'function loop(now) {\n  if (window.__minF && now - last < 30) { requestAnimationFrame(loop); return; }   /* V667: MINIMAL = 30 Bilder/s */\n  const dt = ')
# Start auf schwacher Hardware
rep('if (FX_WEAK) fxAutoOff("hw");', 'if (FX_WEAK) fxAutoMin("hw");')
# fxAutoMin
rep('const FXM = { t0: 0, n: 0, sum: 0 };   /* V494: Bildrate im Spiel messen */',
    '''function fxAutoMin(why) { const p = fxPref(); if (FX_FORCE != null || (p != null && p !== "auto-off")) return; try { if (FXU.upAt) { FXU.next = performance.now() + (FXU.tries <= 1 ? 600000 : 1800000); FXU.upAt = 0; } FXU.t0 = 0; FXU.n = 0; FXU.sum = 0; FXU.good = 0; FXU.bad = 0; } catch (e) {}
  try { localStorage.setItem("capy-fx", "auto-min"); } catch (e) {} fxLabel(); liteApply(); try { window.__evLog && window.__evLog.push("perf", { d: { lite: 2, why: String(why || "") } }); } catch (e) {}
  try { if (S && S.fx) S.fx = S.fx.filter(f => f.type !== "ofx"); } catch (e) {} try { genHeadSync(); toast("MINIMAL GRAPHICS · Tap me for full graphics", "HQ", 4200); } catch (e) {} }   /* V667 */
const FXM = { t0: 0, n: 0, sum: 0 };   /* V494: Bildrate im Spiel messen */''')
# Messung im LITE/MINIMAL-Modus neu
i = s.find('function fxUpMeasure() {'); j = s.find('function fxMeasure() {')
s = s[:i] + '''function fxUpMeasure() { const now = performance.now(), d = FXU.t0 ? now - FXU.t0 : 0; FXU.t0 = now; const mn = fxPref() === "auto-min";   /* V665/V667 */
  if (!d || d > 200 || document.hidden || !S || !S.started || S.over || frozen()) { FXU.n = 0; FXU.sum = 0; return; }
  FXU.n++; FXU.sum += d; if (FXU.n < 60) return; const avg = FXU.sum / FXU.n, span = FXU.sum; FXU.n = 0; FXU.sum = 0;
  if (!mn) { if (avg > 40) FXU.bad = (FXU.bad || 0) + span; else FXU.bad = 0; if (FXU.bad >= 5000) { FXU.bad = 0; fxAutoMin("fps"); return; } }   /* LITE: ~5 s unter 25 FPS → MINIMAL */
  if (FX_WEAK || FXU.tries >= 2 || now < FXU.next) { FXU.good = 0; return; }
  if (avg < (mn ? 34.5 : 20)) FXU.good += span; else FXU.good = 0;   /* MINIMAL: 30 FPS sicher · LITE: ≥ 50 FPS */
  if (FXU.good < 120000) return; FXU.good = 0; FXU.tries++; FXU.upAt = now;
  try { if (mn) localStorage.setItem("capy-fx", "auto-off"); else localStorage.removeItem("capy-fx"); } catch (e) {} FXM.n = 0; FXM.sum = 0; FXM.t0 = 0; fxLabel(); liteApply(); genHeadSync();
  try { window.__evLog && window.__evLog.push("perf", { d: { lite: mn ? 1 : 0, why: "auto-up", n: FXU.tries } }); } catch (e) {}
  try { const g = document.getElementById("genAv"); if (g) { g.classList.remove("talk"); void g.offsetWidth; g.classList.add("talk"); } } catch (e) {}
  try { toast(mn ? "LITE GRAPHICS · A bit more sparkle" : "FULL GRAPHICS ARE BACK · Medals polished", "HQ", 3600); } catch (e) {} }
''' + s[j:]
rep('function fxMeasure() { if (FX_FORCE == null && fxPref() === "auto-off") { fxUpMeasure(); return; }',
    'function fxMeasure() { if (FX_FORCE == null && (fxPref() === "auto-off" || fxPref() === "auto-min")) { fxUpMeasure(); return; }')
# CSS
rep('/* V658: Leicht-Modus */', '/* V667: MINIMAL */ body.minimal #sky,body.minimal #sky *,body.minimal .dj *{animation:none!important}\n/* V658: Leicht-Modus */')
open(p, "w", encoding="utf-8").write(s); print("ok V667")
