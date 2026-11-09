#!/usr/bin/env python3
"""V512: Nuts-Abstecher fortsetzen (Martin 09.11. 16:25): Wer in einer Nuts-Höhle pausiert und ins Menü geht (oder die App schließt),
bekommt im Menü die Wahl: «CONTINUE NUTS» (zurück in die Höhle, gleicher Stand) oder «MAIN ROAD» (Hauptspiel; der Abstecher wird abgebrochen).
- Nuts-Stand separat in localStorage «capy-nz-save» (Feld, Türme, Monster, Level, Hauptspiel-Stand dahinter).
- Gelöscht, sobald der Abstecher endet oder man das Hauptspiel wählt.
Aufruf: python3 tools/patch512.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V511";', 'const GAME_VER = "V512";')
# speichern
rep('if (S && S.nuts) { if (window.__NZF) LS.set("tarnturm-save", JSON.stringify(window.__NZF)); return; }',
    'if (S && S.nuts) { if (window.__NZF) LS.set("tarnturm-save", JSON.stringify(window.__NZF)); try { const f = buildSave(); if (f && window.__NZF && !NZ.ending) LS.set("capy-nz-save", JSON.stringify({ frame: f, nuts: S.nuts, main: window.__NZF, first: !!NZ.first })); } catch (e) {} return; }   /* V512 */')
# löschen: Abstecher endet / startet neu / zurück ins Hauptspiel
rep('function nutsEnd(why) {\n  if (!S || !S.nuts || NZ.ending) return; NZ.ending = true;',
    'function nutsEnd(why) {\n  if (!S || !S.nuts || NZ.ending) return; NZ.ending = true; LS.del("capy-nz-save");   /* V512 */')
rep('const fr = buildSave(); if (!fr) return; NZ.frozen = fr; window.__NZF = fr;',
    'const fr = buildSave(); if (!fr) return; LS.del("capy-nz-save"); NZ.frozen = fr; window.__NZF = fr;')
rep('function nutsResume(c, cleared, first) {\n  const fr = NZ.frozen;', 'function nutsResume(c, cleared, first) {\n  LS.del("capy-nz-save"); const fr = NZ.frozen;')
rep('if (window.ONE_MODE) { const cp = window.__cpGet ? window.__cpGet() : 0; if (b.dataset.cont && cp >= 5) { startGame(k, cp); return; } startGame(k); return; }',
    'if (window.ONE_MODE) { if (S && S.nuts && S.started && !S.over && !NZ.ending) { $("ovStart").hidden = true; nutsEnd("quit"); return; }   /* V512: Hauptspiel gewählt → Abstecher endet wie «Quit detour» (Ergebnis, dann zurück auf die Hauptstraße) */ if (nzHasSave()) { LS.del("capy-nz-save"); NZ.frozen = null; window.__NZF = null; document.body.classList.remove("inNuts"); } const cp = window.__cpGet ? window.__cpGet() : 0; if (b.dataset.cont && cp >= 5) { startGame(k, cp); return; } startGame(k); return; }')
# Menü: Wahl anzeigen
rep('      $("modeList").innerHTML = `<button class="modeBtn playBtn" data-mode="pro" data-cont="1"><span class="mName">CONTINUE ▶</span><span class="mSub">Wave ${cp + 1} · ${nm(P.cont[1])} · ${nm(P.place)}</span></button><button class="newRun" data-mode="pro" data-new="1">Start over · wave 1</button>`; return; } }',
    '      const nz = nzHasSave(); $("modeList").innerHTML = (nz ? `<button class="modeBtn playBtn nzCont" data-nzcont="1"><span class="mName">CONTINUE NUTS ▶</span><span class="mSub">${nz}</span></button>` : "") + `<button class="modeBtn playBtn${nz ? " mainAlt" : ""}" data-mode="pro" data-cont="1"><span class="mName">${nz ? "MAIN ROAD ▶" : "CONTINUE ▶"}</span><span class="mSub">Wave ${cp + 1} · ${nm(P.cont[1])} · ${nm(P.place)}${nz ? " · ends the detour" : ""}</span></button><button class="newRun" data-mode="pro" data-new="1">Start over · wave 1</button>`; return; } }')
rep('function nutsResume(c, cleared, first) {',
    '''/* V512: Nuts-Stand im Menü */
function nzHasSave() {   /* liefert Untertitel oder "" */
  try { if (S && S.nuts && S.started && !S.over && !NZ.ending) return `${nzWord(S.nuts.c)} · level ${Math.max(1, S.nuts.lvl || 1)} of ${NZ_MAX}`;
    const d = JSON.parse(LS.get("capy-nz-save") || "null"); if (d && d.frame && d.main && d.nuts) return `${nzWord(d.nuts.c)} · level ${Math.max(1, d.nuts.lvl || 1)} of ${NZ_MAX}`; } catch (e) {}
  return ""; }
function nutsContinue() {
  SFX.init(); snd("confirm");
  if (S && S.nuts && S.started && !S.over && !NZ.ending) { $("ovStart").hidden = true; $("ovPause").hidden = true; S.paused = false; nzBadgeSync(); try { TP.key = null; SFX.music.start(S.wave); } catch (e) {} return; }
  let d = null; try { d = JSON.parse(LS.get("capy-nz-save") || "null"); } catch (e) {}
  if (!d || !d.frame || !d.main || !d.nuts) { LS.del("capy-nz-save"); renderModes(); return; }
  NZ.frozen = d.main; window.__NZF = d.main; NZ.first = !!d.first; NZ.ending = false;
  if (!loadGame(d.frame)) { LS.del("capy-nz-save"); NZ.frozen = null; window.__NZF = null; renderModes(); return; }
  S.nuts = d.nuts; S.cpRun = true; S.ff = false; S.dirty = true; rebuild(); nzBadgeSync(); lvLabel(); try { TP.key = null; } catch (e) {}
  setTimeout(() => toast(`BACK IN THE NUTS · ${nzWord(S.nuts.c)} · level ${Math.max(1, S.nuts.lvl || 1)}`, "NUTS", 2400), 900); }
document.addEventListener("click", e => { const b = e.target.closest && e.target.closest("[data-nzcont]"); if (b) { e.stopPropagation(); nutsContinue(); } }, true);
window.__nzCont = { has: () => nzHasSave(), go: () => nutsContinue() };
function nutsResume(c, cleared, first) {''')
rep('#ovSettings .setRow{flex-wrap:wrap}', '#ovSettings .setRow{flex-wrap:wrap}\n.modeBtn.nzCont{background:linear-gradient(180deg,#5a2a3a,#2a1a22)!important;color:#fff!important;border-color:#ff5a6a!important}.modeBtn.nzCont .mSub{color:#ffb3c0!important}.modeBtn.mainAlt{margin-top:8px}')
# Menü/HQ in der Höhle beendet den Abstecher nicht mehr – nur pausieren + speichern
rep('for (const id of ["btnPMenu", "btnHQ"]) $(id).addEventListener("click", e => { if (S && S.nuts && !S.over) { e.stopImmediatePropagation(); e.preventDefault(); nutsEnd("quit"); } }, true);',
    '/* V512: Menü/HQ in der Nuts-Höhle pausiert nur – Fortsetzen oder Hauptspiel im Menü wählen */')
# Startbildschirm (btnResume): zusätzlich «CONTINUE NUTS», Haupt-Knopf wird «MAIN ROAD»
rep('  $("btnResume").hidden = !(sv && sv.grid); if (sv && sv.grid) $("btnResume").innerHTML = `CONTINUE<span class="lbl">WORLD TOUR · WAVE ${sv.wave} · ${(sv.score || 0).toLocaleString("en-US")} PTS</span>`;',
    '''  $("btnResume").hidden = !(sv && sv.grid); if (sv && sv.grid) $("btnResume").innerHTML = `CONTINUE<span class="lbl">WORLD TOUR · WAVE ${sv.wave} · ${(sv.score || 0).toLocaleString("en-US")} PTS</span>`;
  { const nz = nzHasSave(); let nb = document.getElementById("btnNzCont");   /* V512 */
    if (nz) { if (!nb) { nb = document.createElement("button"); nb.id = "btnNzCont"; nb.className = "btn-big nzContBig"; nb.dataset.nzcont = "1"; $("btnResume").parentNode.insertBefore(nb, $("btnResume")); }
      nb.hidden = false; nb.innerHTML = `CONTINUE NUTS ▶<span class="lbl">${nz}</span>`; if (sv && sv.grid) $("btnResume").innerHTML = `MAIN ROAD<span class="lbl">WAVE ${sv.wave} · ends the Nuts detour</span>`; }
    else if (nb) nb.hidden = true; }''')
rep('$("btnResume").addEventListener("click", () => { SFX.init(); snd("confirm"); showCamp(',
    '$("btnResume").addEventListener("click", e => { if (S && S.nuts && S.started && !S.over && !NZ.ending) { e.stopImmediatePropagation(); SFX.init(); snd("confirm"); $("ovStart").hidden = true; nutsEnd("quit"); } else if (nzHasSave()) { LS.del("capy-nz-save"); NZ.frozen = null; window.__NZF = null; document.body.classList.remove("inNuts"); } }, true);   /* V512 */\n$("btnResume").addEventListener("click", () => { SFX.init(); snd("confirm"); showCamp(')
rep('.modeBtn.nzCont{', '#btnNzCont{position:absolute!important;left:50%!important;transform:translateX(-50%)!important;width:min(340px,calc(100% - 16px))!important;bottom:122px!important;margin:0!important;z-index:7!important;background:linear-gradient(180deg,#7a2a3a,#3a1622)!important;color:#fff!important;border-color:#ff5a6a!important}#btnNzCont .lbl{color:#ffc2cc!important}.modeBtn.nzCont{')
open(p, "w", encoding="utf-8").write(s); print("ok V512")
