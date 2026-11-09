#!/usr/bin/env python3
"""V534 (Martin 09.11. 20:53/20:54):
- Tutorial-Knopf (Doktorhut-Icon) unten links rechts neben dem rosa Knopf, sichtbar bis Welle 10. Startet das Tutorial im laufenden Spiel.
- Tutorial-Schritte zählen ab dem Start des Tutorials (vorher: «schon ein Turm da» = sofort erledigt).
- Rechts oben: nur noch die Versionsnummer und nur für Martin (Dev-Modus oder Spieler-Nr. M2HL-KCQH). Spieler-Nr. nur im Zahnrad-Menü.
Aufruf: python3 tools/patch534.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V533";', 'const GAME_VER = "V534";')
# Versionsnummer nur für Martin
rep('t.className = "verTag"; t.textContent = GAME_VER + "\\n" + capyUid(); o.appendChild(t);',
    't.className = "verTag"; t.textContent = GAME_VER; t.hidden = !capyMe(); o.appendChild(t);')
rep('function supportText() {', 'function capyMe() { try { return localStorage.getItem("tarnturm-dev") === "1" || capyUid() === "M2HL-KCQH"; } catch (e) { return false; } }   /* V534: nur Martin sieht die Version oben */\nfunction supportText() {')
rep('.verTag{white-space:pre;', '.verTag[hidden]{display:none!important}.verTag{white-space:pre;')
# Tutorial: Schritte relativ zum Start
rep('function tutStart() { TUT.on = true;', 'function tutStart() { TUT.b = { p: S.pieceNo || 0, tw: S.towers.size, wp: [...S.towers.values()].reduce((a, t) => a + t.w.length, 0) }; TUT.on = true;')
rep('done: () => S.pieceNo >= 1 },', 'done: () => S.pieceNo >= ((TUT.b && TUT.b.p) || 0) + 1 },')
rep('done: () => S.mode === "build" || S.towers.size >= 1 },', 'done: () => S.mode === "build" || S.towers.size > ((TUT.b && TUT.b.tw) || 0) },')
rep('done: () => S.towers.size >= 1 },', 'done: () => S.towers.size > ((TUT.b && TUT.b.tw) || 0) },')
rep('done: () => [...S.towers.values()].some(t => t.w.length) && !S.sel },', 'done: () => [...S.towers.values()].reduce((a, t) => a + t.w.length, 0) > ((TUT.b && TUT.b.wp) || 0) && !S.sel },')
# Knopf
rep('function tutEnd(skipped) {', '''/* V534: Tutorial-Knopf bis Welle 10 */
{ const b = document.createElement("button"); b.id = "bTut"; b.type = "button"; b.setAttribute("aria-label", "Tutorial"); b.hidden = true;
  b.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4 1.5 9 12 14l10.5-5z" fill="#3a2414"/><path d="M5.5 11.2v4.3c0 1.6 2.9 3 6.5 3s6.5-1.4 6.5-3v-4.3L12 14.3z" fill="#3a2414"/><path d="M21 9.3v5.2" stroke="#3a2414" stroke-width="1.6" stroke-linecap="round"/><circle cx="21" cy="15.6" r="1.4" fill="#ffd34a" stroke="#3a2414" stroke-width="1"/></svg><b>HOW TO</b>';
  document.body.appendChild(b);
  b.addEventListener("click", () => { try { SFX.init(); snd("uiTap"); } catch (e) {} if (!S || !S.started || S.over || TUT.on) return; S.paused = false; tutStart(); b.hidden = true; });
  setInterval(() => { try { const w = document.getElementById("bWave"), r = w && w.getBoundingClientRect(), ovOpen = [...document.querySelectorAll(".overlay,#ovMap,#ovPause,#ovStart")].some(o => !o.hidden && o.getClientRects().length && getComputedStyle(o).display !== "none");
      const show = !!(r && r.width && S && S.started && !S.over && !S.nuts && !S.replay && !S.testRun && (S.wave || 1) <= 10 && !TUT.on && !S.paused && !ovOpen);
      if (b.hidden === show) b.hidden = !show; if (show) { b.style.left = Math.round(r.right + 10) + "px"; b.style.top = Math.round(r.top + r.height / 2 - 26) + "px"; } } catch (e) {} }, 300); }
function tutEnd(skipped) {''')
rep('.verTag[hidden]{display:none!important}', '.verTag[hidden]{display:none!important}#bTut{position:fixed;z-index:58;width:52px;height:52px;min-height:0;padding:0;border-radius:50%;background:#fff6e6;border:3px solid #3a2414;box-shadow:0 4px 0 #3a2414;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0}#bTut[hidden]{display:none!important}#bTut svg{width:28px;height:28px;margin-top:2px}#bTut b{font:400 9px/1 Bangers,system-ui;letter-spacing:.04em;color:#3a2414;margin-top:-1px}')
open(p, "w", encoding="utf-8").write(s); print("ok V534")
