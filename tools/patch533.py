#!/usr/bin/env python3
"""V533 (Martin 09.11. 20:50, Natascha): «Replay tutorial» lief im alten Spielstand (Türme/Blöcke schon da) – alle 5 Schritte
galten sofort als erledigt, Tutorial war in Sekunden «fertig» und kam auch beim Neustart nicht mehr.
Jetzt: Replay startet immer ein neues Spiel ab Welle 1 mit Tutorial (Fenster zu, Pause zu). Läuft schon ein Spiel über Welle 3,
fragt der Knopf erst nach («Tap again · new game from wave 1»).
Aufruf: python3 tools/patch533.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V532";', 'const GAME_VER = "V533";')
rep('''$("btnReTut").addEventListener("click", () => { SFX.init(); snd("uiTap"); LS.del("tarnturm-tut"); $("ovInfo").hidden = true;
  if (S && S.started && !S.over && !S.nuts) { $("ovStart").hidden = true; S.paused = false; tutStart(); } else toast("TUTORIAL · starts with your next game", "HQ", 2200); });''',
'''let reTutArm = 0;
$("btnReTut").addEventListener("click", () => { SFX.init(); snd("uiTap"); const b = $("btnReTut"), now = performance.now();   /* V533: immer neues Spiel ab Welle 1 */
  let w = 0; try { const sv = JSON.parse(LS.get("tarnturm-save") || "null"); w = Math.max(S && S.started && !S.over ? S.wave || 0 : 0, sv && sv.wave || 0); } catch (e) {}
  if (w > 3 && (!reTutArm || now - reTutArm > 3000)) { reTutArm = now; b.textContent = "Tap again · new game from wave 1"; setTimeout(() => { if (performance.now() - reTutArm >= 3000) b.textContent = "↺ Replay tutorial"; }, 3100); return; }
  reTutArm = 0; b.textContent = "↺ Replay tutorial"; LS.del("tarnturm-tut"); LS.del("tarnturm-save");
  for (const id of ["ovInfo", "ovPause", "ovSettings", "ovStart"]) { const o = $(id); if (o) o.hidden = true; }
  try { if (S && S.nuts) { LS.del("capy-nz-save"); NZ.frozen = null; window.__NZF = null; document.body.classList.remove("inNuts"); } } catch (e) {}
  try { tutAbort(); } catch (e) {} startGame(MODE); toast("TUTORIAL · new game from wave 1", "HQ", 1800); });''')
open(p, "w", encoding="utf-8").write(s); print("ok V533")
