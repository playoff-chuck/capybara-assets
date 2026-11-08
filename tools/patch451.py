#!/usr/bin/env python3
"""V451: Nuts-Territorien auf der Weltkarte bekommen einen Pin + Schild «NUTS · <Ork-Wort>» je Kontinent.
Antippen vor Abschluss des Kontinents -> Meldung oben im Kartenkopf («Finish … first · n of 6 places cleared · then the Nuts detour opens»).
Nach Abschluss (oder Nuts bereits freigeschaltet) -> Nuts-Abstecher startet (laufendes Spiel: sofort; vom Startscreen: Spielstand laden, dann Abstecher).
(Martin 08.11. 13:08)
Nutzung: python3 tools/patch451.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V450";', 'const GAME_VER = "V451";')

# 1) Ork-Wörter je Kontinent (erfunden, keine echten Namen)
rep('const nzName = c => CONTS[c][1];',
    'const nzName = c => CONTS[c][1];\n'
    'const NZ_WORD = ["SKULLGROG", "GORKAZAR", "FROSTGNAW", "GRUMBLEFANG"];   /* V451: verrücktes Ork-Wort je Nuts-Territorium */\n'
    'const nzWord = c => NZ_WORD[c] || "GRAKMAW";')

# 2) Pin + Schild unter dem Territorium, antippbar
rep('<div class="mNuts${b ? " on" : ""}" style="left:${(x * 100 - 6).toFixed(2)}%;top:${(y * 100 + 7).toFixed(2)}%"><span style="${nzVars(c)}">${nzLair(c, b)}</span></div>',
    '<div class="mNuts${b ? " on" : ""}" data-nz="${c}" style="left:${(x * 100 - 6).toFixed(2)}%;top:${(y * 100 + 7).toFixed(2)}%"><span style="${nzVars(c)}">${nzLair(c, b)}</span><b class="nzAnc" style="${nzVars(c)}"><i class="nzPin"></i><em class="nzTag">NUTS<small>${nzWord(c)}</small></em></b></div>')

# 3) Antippen: Meldung oben oder Abstecher starten (vor dem Kontinent-Klick, der sonst den Ort anzeigt)
rep('    vp.addEventListener("click", e => { if (mode !== "browse") return; if (performance.now() - (window.__mapDragT || 0) < 300) return;\n      { const rb = ov.querySelector(".mapReplay");',
    '    vp.addEventListener("pointerdown", e => { try { window.__nzHit = e.target && e.target.closest ? e.target.closest(".mNuts") : null; } catch (er) { window.__nzHit = null; } }, true);   /* V451: Ziel merken – setPointerCapture leitet den Klick auf die Fläche um */\n'
    '    vp.addEventListener("click", e => {   /* V451: Nuts-Schild/-Pin/-Territorium antippen */\n'
    '      const nz = window.__nzHit; window.__nzHit = null; if (!nz || mode !== "browse") return; if (performance.now() - (window.__mapDragT || 0) < 300) return;\n'
    '      e.stopPropagation(); e.stopImmediatePropagation(); const c = +nz.dataset.nz, nm = contName(c), w = curWave(), g = posOf(w).g, done = Math.max(0, Math.min(6, g - c * 6));\n'
    '      ov.classList.remove("wv"); ov.querySelector(".mapWorldBtn").textContent = "WORLD"; go(contCam(c), 800); ov.querySelector(".mapReplay").hidden = true;\n'
    '      const open = w > NZ_BASES[c] || nzUnl().includes(c);\n'
    '      if (!open) { label(nm, `NUTS · ${nzWord(c)}`, `Finish ${nm} first · ${done} of 6 places cleared · then the Nuts detour opens`); try { snd("close"); } catch (er) {} nz.classList.remove("shake"); void nz.offsetWidth; nz.classList.add("shake"); return; }\n'
    '      if (S && S.nuts && !S.over) { label(nm, `NUTS · ${nzWord(c)}`, "You are already on a Nuts detour · finish or leave it first"); try { snd("uiTap"); } catch (er) {} return; }\n'
    '      const running = !!(S && S.started && !S.over && !S.nuts && !S.replay), rs = document.getElementById("btnResume"), hasSave = !!(rs && rs.getClientRects().length);\n'
    '      if (!running && !hasSave) { label(nm, `NUTS · ${nzWord(c)}`, "Start your tour first · the Nuts detour opens from the pause menu"); try { snd("uiTap"); } catch (er) {} return; }\n'
    '      label(nm, `NUTS · ${nzWord(c)}`, `${NZ_MAX} levels · no mercy · best L${nzBest(c)}`); try { snd("start"); } catch (er) {}\n'
    '      const kick = () => { try { if (S && S.started && !S.over && !S.nuts) { for (const id of ["ovStart", "ovOver", "ovPause"]) $(id).hidden = true; startDetour(c); } } catch (er) {} };\n'
    '      if (running) { hide(); setTimeout(kick, 80); return; }\n'
    '      ov.querySelector(".mapClose").click(); setTimeout(() => rs.click(), 60); const t0 = performance.now(), wait = () => { if (S && S.started && !S.over && !S.nuts && !S.replay) { setTimeout(kick, 120); return; } if (performance.now() - t0 < 4000) requestAnimationFrame(wait); }; setTimeout(wait, 200); });\n'
    '    vp.addEventListener("click", e => { if (mode !== "browse") return; if (performance.now() - (window.__mapDragT || 0) < 300) return;\n      { const rb = ov.querySelector(".mapReplay");')

# 4) Stil: Pin + Schild, antippbar, Wackeln bei «noch gesperrt»
rep('.mNuts{z-index:1}.mPin{z-index:3}   /* V449: Schilder und Pins über den Territorien */',
    '.mNuts{z-index:1}.mPin{z-index:3}   /* V449: Schilder und Pins über den Territorien */\n'
    '.mNuts .nzPin{position:absolute;left:-7px;top:30px;width:14px;height:14px;border-radius:50%;border:2.5px solid #2a1a22;background:var(--nzA,#efe6d6);box-sizing:border-box;box-shadow:0 0 8px var(--nzE,#ff8a5a),0 2px 0 rgba(42,26,34,.6);pointer-events:auto;cursor:pointer;animation:nzPin 1.6s ease-in-out infinite}\n'
    '.mNuts .nzTag{position:absolute;left:0;top:42px;transform:translateX(-50%);white-space:nowrap;font:400 14px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.06em;font-style:normal;color:#fff;background:#2a1a22;border:2.5px solid var(--nzA,#efe6d6);border-radius:10px;padding:3px 8px 2px;box-shadow:0 2px 0 #1a0f14,0 0 10px var(--nzF,rgba(120,90,140,.5));pointer-events:auto;cursor:pointer;text-align:center;display:grid;gap:1px}\n'
    '.mNuts .nzTag small{font:400 9.5px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.12em;color:var(--nzA,#efe6d6)}\n'
    '.mNuts span{pointer-events:auto;cursor:pointer}.mNuts .nzL{bottom:auto;top:-12px}\n'
    '.mNuts.shake .nzTag,.mNuts.shake .nzPin{animation:nzShake .45s ease-in-out 1}\n'
    '@keyframes nzPin{0%,100%{box-shadow:0 0 6px var(--nzE,#ff8a5a),0 2px 0 rgba(42,26,34,.6)}50%{box-shadow:0 0 14px var(--nzE,#ff8a5a),0 2px 0 rgba(42,26,34,.6)}}\n'
    '@keyframes nzShake{0%,100%{translate:0 0}20%{translate:-4px 0}40%{translate:4px 0}60%{translate:-3px 0}80%{translate:3px 0}}\n'
    '.mNuts .nzAnc{position:absolute;left:0;top:0;width:0;height:0;display:block;transform:scale(var(--ik,1));transform-origin:0 0;pointer-events:none}')

open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
