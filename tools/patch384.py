"""V384 (To-do 90 Rest): Ort auf der Karte antippen -> nochmal spielen.
Auf der Weltkarte (frei ansehen) einen geschafften Ort antippen -> Knopf «REPLAY <Ort>».
Spielt die 5 Wellen des Ortes als Checkpoint-Lauf (keine Bestenliste, kein Rekord). Sterne zaehlen (Bestwert).
Der Hauptspielstand bleibt unberuehrt: saveGame schreibt waehrend des Replays nur den eingefrorenen Stand
(wie beim Nuts-Abstecher), Tod/Restart loeschen ihn nicht. Danach Ergebniskarte -> Hauptmenue (Continue = Welttour)."""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')

# 1) Speichern: waehrend Replay nur den Hauptstand schreiben
rep('function saveGame() { if (S && S.nuts) {',
    'function saveGame() { if (S && S.replay) { if (window.__RPF) LS.set("tarnturm-save", JSON.stringify(window.__RPF)); return; } if (S && S.nuts) {')
# 2) Tod im Replay: kein Game over, Hauptstand bleibt
rep('function gameOver(why) { tutAbort();',
    'function gameOver(why) { tutAbort(); if (S && S.replay && !S.over) { replayEnd("fail"); return; }   /* V384 */')
# 3) Ende nach der 5. Welle des Ortes
rep('      if (S.wave % 5 === 0) praise(`WAVE ${S.wave}!`',
    '      if (S.replay && S.wave >= S.replay.end) { S.replay.fin = true; setTimeout(() => replayEnd("done"), 2900); }   /* V384 */\n'
    '      if (S.wave % 5 === 0) praise(`WAVE ${S.wave}!`')
# 4) Finale (W150) und Kontinent-Schild nicht im Replay
rep('S.over || S.won) return; if (S.wave >= 150', 'S.over || S.won || S.replay) return; if (S.wave >= 150')
rep('!S.started || S.over || S.nuts || S.won || S.paused', '!S.started || S.over || S.nuts || S.replay || S.won || S.paused')
# 5) Karten-Szenen nicht im Replay
rep('if (!busy && S && S.started && !S.over && !S.nuts && S.mapDoneFor', 'if (!busy && S && S.started && !S.over && !S.nuts && !S.replay && S.mapDoneFor')
rep('if (!fromWave && S && S.started && !S.over && !S.nuts) { busy = true;', 'if (!fromWave && !window.__rpStart && S && S.started && !S.over && !S.nuts) { busy = true;')
rep('if (typeof S !== "undefined" && S && S.started && !S.over && !S.nuts) return Math.max(1, S.wave || 1);',
    'if (typeof S !== "undefined" && S && S.started && !S.over && !S.nuts && !S.replay) return Math.max(1, S.wave || 1);')
# 6) Restart im Pausemenue beendet nur das Replay
rep('$("btnPNutsQuit").addEventListener("click"',
    '$("btnPRestart").addEventListener("click", e => { if (S && S.replay && !S.over) { e.stopImmediatePropagation(); $("ovPause").hidden = true; replayEnd("quit"); } }, true);   /* V384 */\n'
    '$("btnPNutsQuit").addEventListener("click"')
# 7) Start / Ende
rep('function startDetour(c) {', r'''/* V384: Ort nochmal spielen – Hauptspielstand bleibt unberuehrt */
function startReplay(g) {
  g = Math.max(0, Math.min(29, g | 0));
  if (S && S.nuts && !S.over) { toast("FINISH THE NUTS DETOUR FIRST", "HQ", 2000); return; }
  let main = null;
  if (S && S.replay && !S.over) main = window.__RPF || null;
  else if (S && S.started && !S.over) main = buildSave();
  else { try { main = JSON.parse(LS.get("tarnturm-save") || "null"); } catch (e) { main = null; } }
  window.__RPF = main; if (main) LS.set("tarnturm-save", JSON.stringify(main));
  const from = g * 5; window.__rpStart = true;
  try { startGame(MODES.pro ? "pro" : MODE, from); } finally { window.__rpStart = false; }
  S.cpRun = true; S.replay = { g, end: from + 5, best: starsAll()[g] || 0 }; S.mapDoneFor = from + 1;
  for (const id of ["ovStart", "ovOver", "ovPause"]) $(id).hidden = true;
  const P = wherePos(from + 1);
  setTimeout(() => { if (S && S.replay && !S.over) toast(`REPLAY · ${P.place} · waves ${from + 1}–${from + 5} · world tour save is safe`, "HQ", 3000); }, 3000);
}
function replayEnd(why) {
  if (!S || !S.replay || S.replay.ended) return; const R = S.replay; R.ended = true;
  S.over = true; S.paused = false; try { tutAbort(); } catch (e) {} try { SFX.music.stop(0.5); } catch (e) {}
  const main = window.__RPF; window.__RPF = null;
  if (main) LS.set("tarnturm-save", JSON.stringify(main)); else LS.del("tarnturm-save");
  try { endAlert(); if (S.drop) endDrop(); S.mix = null; $("mixer").hidden = true; S.mode = null; closeSheet(); } catch (e) {}
  for (const id of ["ovPause", "ovOver", "ovOrders", "ovHack", "ovSpec", "ovTilt", "ovGive", "ovJoin"]) { const el = $(id); if (el) el.hidden = true; }
  S.ordersOpen = false; S.duel = null;
  const toMenu = () => { try { $("btnHQ").click(); } catch (e) { renderModes(); $("ovStart").hidden = false; } };
  if (why === "quit") { toMenu(); return; }
  const P = wherePos(R.end), ok = why === "done", n = ok && S.lastStars && S.lastStars.g === R.g ? S.lastStars.n : 0, best = Math.max(R.best, starsAll()[R.g] || 0);
  const d = document.createElement("div"); d.id = "rpRes";
  d.innerHTML = `<div class="rpBox"><small>REPLAY · PLACE ${R.g + 1} OF 30</small><b>${ok ? P.place + " CLEARED!" : "REPLAY OVER"}</b>`
    + `<p class="rpSt">${starStr(n)}</p><span>${n > R.best ? "NEW BEST! " : ""}Best: ${starStr(best)}</span><em>Your world tour save is untouched.</em><button type="button" class="btn-accent">OK</button></div>`;
  document.body.appendChild(d); try { snd(ok ? "hkWin" : "nope"); } catch (e) {}
  d.querySelector("button").addEventListener("click", () => { try { SFX.init(); snd("uiTap"); } catch (e) {} d.remove(); toMenu(); });
}
try { window.__TT && Object.assign(window.__TT, { startReplay: g => startReplay(g), replayEnd: w => replayEnd(w), saveGame: () => saveGame(), gameOver: w => gameOver(w) }); } catch (e) {}
function startDetour(c) {''')
# 8) Karte: geschafften Ort antippen -> Replay-Knopf
rep('<div class="mapSkip">tap to skip</div>',
    '<button type="button" class="mapReplay" hidden></button><div class="mapSkip">tap to skip</div>')
rep('function hide() { clearSeq(); ov.hidden = true;',
    'function hide() { clearSeq(); try { ov.querySelector(".mapReplay").hidden = true; } catch (e) {} ov.hidden = true;')
rep('vp.addEventListener("click", e => { if (mode !== "browse") return; if (performance.now() - (window.__mapDragT || 0) < 300) return;',
    '''vp.addEventListener("click", e => { if (mode !== "browse") return; if (performance.now() - (window.__mapDragT || 0) < 300) return;
      { const rb = ov.querySelector(".mapReplay"); rb.hidden = true; let hit = null, hd = 30;   /* V384: geschafften Ort antippen -> nochmal spielen */
        ov.querySelectorAll(".mPin.done").forEach(el => { const r = el.querySelector("i").getBoundingClientRect(); if (!r.width) return; const dd = Math.hypot(e.clientX - (r.left + r.width / 2), e.clientY - (r.top + r.height / 2)); if (dd < hd) { hd = dd; hit = el; } });
        if (hit && !(S && S.nuts && !S.over)) { const g = +hit.dataset.g, c = Math.floor(g / 6), i = g % 6, st = starsAll()[g] || 0;
          rb.dataset.g = g; rb.innerHTML = `▶ REPLAY ${nice(CONTS[c][2][i])}<small>waves ${g * 5 + 1}–${g * 5 + 5} · ${starStr(st)}</small>`; rb.hidden = false;
          label(contName(c), nice(CONTS[c][2][i]), `Cleared · best ${starStr(st)} · replay for more stars`); try { snd("uiTap"); } catch (er) {} return; } }''')
rep('    ov.querySelector(".mapClose").addEventListener("click", e => {',
    '''    ov.querySelector(".mapReplay").addEventListener("click", e => { e.stopPropagation(); const g = +e.currentTarget.dataset.g; try { SFX.init(); snd("start"); } catch (er) {} hide(); startReplay(g); });
    ov.querySelector(".mapClose").addEventListener("click", e => {''')
# 9) CSS
rep('#ovMap.browse.fromStart .mPin.cur em::after',
    '''#ovMap .mapReplay{position:absolute;left:50%;bottom:calc(84px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:6;min-width:220px;max-width:calc(100% - 32px);padding:10px 18px;border:3px solid #3a2414;border-radius:16px;background:linear-gradient(180deg,#ffb347,#ff8a1f);color:#fff;font:inherit;font-size:19px;font-weight:900;-webkit-text-stroke:1.2px #3a2414;paint-order:stroke fill;box-shadow:0 4px 0 #3a2414;cursor:pointer;line-height:1.15}
#ovMap .mapReplay small{display:block;font-size:13px;-webkit-text-stroke:0;color:#3a2414;font-weight:800;margin-top:2px}
#ovMap .mapReplay[hidden]{display:none}
#rpRes{position:fixed;inset:0;z-index:2147483002;display:flex;align-items:center;justify-content:center;background:rgba(20,12,6,.62);padding:16px}
#rpRes .rpBox{background:#f3ead6;border:3px solid #3a2414;border-radius:18px;box-shadow:0 6px 0 #3a2414;padding:18px 20px;max-width:340px;width:100%;text-align:center;color:#3a2414;display:flex;flex-direction:column;gap:6px}
#rpRes small{font-weight:800;letter-spacing:.06em;opacity:.75}#rpRes b{font-size:24px;line-height:1.1}#rpRes .rpSt{margin:4px 0;font-size:34px;color:#ffb400;-webkit-text-stroke:1.5px #3a2414;letter-spacing:2px}#rpRes em{font-style:normal;font-size:13px;opacity:.8}#rpRes button{margin-top:8px;min-height:48px;font-size:20px}
#ovMap.browse.fromStart .mPin.cur em::after''')
open(dst, 'w', encoding='utf-8').write(s)
print("ok", NEW)
