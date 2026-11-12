#!/usr/bin/env python3
# V665 (Martin 12.11. 14:25):
#  1) Boss-Hack: Einsatz-Fenster ab dem 3. Hack wieder sicher da. V660 zählte über Ollies Tipp-Zähler – der blieb in manchen Läufen
#     unter 2, dann kam das Einsatz-Fenster nie. Jetzt eigener Zähler «capy-hk-n» (Hacks insgesamt); wer schon einen Hack hatte, zählt als erfahren.
#     Weiterhin ohne Einsatz-Fenster, wenn das Gold nicht für einen Einsatz reicht (< 10).
#  2) Automatische Rückkehr auf volle Grafik: im LITE-Modus (automatisch) 2 Minuten am Stück ≥ 50 FPS → FULL + General-Spruch.
#     Bricht es danach wieder ein → LITE und nächster Versuch frühestens nach 10, dann 30 Minuten; höchstens 2 Versuche je Sitzung.
#     Nicht auf schwacher Hardware (≤ 2 Kerne / ≤ 2 GB), nicht bei Pause/Menüs/Fenstern.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V664";', 'const GAME_VER = "V665";')
rep('const nb = !f && !(S && S.testRun) && (cnt() < 2 || (+$("hkRange").max || 0) < 10);',
    '''let hn = 9; try { if (!(S && S.testRun)) { let c0 = LS.get("capy-hk-n"); if (c0 == null) c0 = LS.get("capy-hk-first") === "1" ? 2 : 0; hn = (+c0 || 0) + 1; LS.set("capy-hk-n", String(hn)); } } catch (e) {}   /* V665: eigener Hack-Zähler */
      const nb = !f && !(S && S.testRun) && (hn <= 2 || (+$("hkRange").max || 0) < 10);''')
# Auto-Rückkehr
rep('function fxMeasure() { if (fxPref() != null || FX_FORCE != null) return; const now = performance.now(), d = FXM.t0 ? now - FXM.t0 : 0; FXM.t0 = now;',
    '''const FXU = { t0: 0, n: 0, sum: 0, good: 0, tries: 0, next: 0, upAt: 0 };   /* V665: Rückkehr auf volle Grafik */
function fxUpMeasure() { const now = performance.now(), d = FXU.t0 ? now - FXU.t0 : 0; FXU.t0 = now;
  if (FX_WEAK || FXU.tries >= 2 || now < FXU.next) { FXU.n = 0; FXU.sum = 0; FXU.good = 0; return; }
  if (!d || d > 200 || document.hidden || !S || !S.started || S.over || frozen()) { FXU.n = 0; FXU.sum = 0; return; }
  FXU.n++; FXU.sum += d; if (FXU.n < 60) return; const avg = FXU.sum / FXU.n, span = FXU.sum; FXU.n = 0; FXU.sum = 0;
  if (avg < 20) FXU.good += span; else FXU.good = 0;   /* ≥ 50 FPS ohne Unterbrechung */
  if (FXU.good < 120000) return; FXU.good = 0; FXU.tries++; FXU.upAt = now;
  try { localStorage.removeItem("capy-fx"); } catch (e) {} FXM.n = 0; FXM.sum = 0; FXM.t0 = 0; fxLabel(); liteApply(); genHeadSync();
  try { window.__evLog && window.__evLog.push("perf", { d: { lite: 0, why: "auto-up", n: FXU.tries } }); } catch (e) {}
  try { const g = document.getElementById("genAv"); if (g) { g.classList.remove("talk"); void g.offsetWidth; g.classList.add("talk"); } } catch (e) {}
  try { toast("FULL GRAPHICS ARE BACK · Medals polished", "HQ", 3600); } catch (e) {} }
function fxMeasure() { if (FX_FORCE == null && fxPref() === "auto-off") { fxUpMeasure(); return; } if (fxPref() != null || FX_FORCE != null) return; const now = performance.now(), d = FXM.t0 ? now - FXM.t0 : 0; FXM.t0 = now;''')
rep('function fxAutoOff(why) { if (fxPref() != null || FX_FORCE != null) return;',
    'function fxAutoOff(why) { if (fxPref() != null || FX_FORCE != null) return; try { if (FXU.upAt) { FXU.next = performance.now() + (FXU.tries <= 1 ? 600000 : 1800000); FXU.upAt = 0; } FXU.t0 = 0; FXU.n = 0; FXU.sum = 0; FXU.good = 0; } catch (e) {}   /* V665: Sperrzeit nach Rückfall */')
open(p, "w", encoding="utf-8").write(s); print("ok V665")
