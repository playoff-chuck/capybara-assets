"""V365 (Martin 07.11. 08:17): Musik bleibt weg.
1) tpStop pausierte verzögert auch ein direkt danach gestartetes Stück (Restart / Main menu) -> Generationszähler.
2) Wächter: hängt das Element pausiert, obwohl ein Stück laufen soll -> neu abspielen; Ladefehler -> nächstes Stück.
3) Ein-Fenster-Stummschaltung: zweimal hintereinander stumm (versteckt + anderes Fenster) vergaß, dass Musik lief.
4) Musik-Kanalregler linear statt quadratisch; «All» = 0 heißt wirklich 0 (vorher Rückfall auf 30 %)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V364";', 'const GAME_VER = "V365";')
rep('const TP = { el: null, src: null, g: null, key: null, pool: [], wave: -1, paused: false, synthOn: false };',
    'const TP = { el: null, src: null, g: null, key: null, pool: [], wave: -1, paused: false, synthOn: false, gen: 0, pend: false, errT: 0, stuck: 0 };')
rep('  a.addEventListener("ended", () => tpNext());\n',
    '  a.addEventListener("ended", () => tpNext());\n'
    '  a.addEventListener("error", () => { if (!TP.key || Date.now() - TP.errT < 3000) return; TP.errT = Date.now(); setTimeout(() => { if (TP.key) tpNext(); }, 1000); });   // V365: Ladefehler -> nächstes Stück\n')
rep('Math.pow(SFX.vol || 0.3, 2) * 1.5) * Math.pow(SFX.ch("m"), 2)',
    'Math.pow(SFX.vol == null ? 0.3 : SFX.vol, 2) * 1.5) * SFX.ch("m")', 2)   # Suno-Player + Weltkarten-Musik
rep('const a = tpEl(); TP.key = key; TP.paused = false; const go = () => { a.src',
    'const a = tpEl(); TP.key = key; TP.paused = false; TP.stopping = false; const g = ++TP.gen; TP.pend = true; const go = () => { if (g !== TP.gen) return; TP.pend = false; a.src')
rep('function tpStop(f = 0.5) { if (!TP.el) return; tpFade(0.0001, f); const a = TP.el; setTimeout(() => { if (TP.key === null || TP.stopping) a.pause(); TP.stopping = false; }, f * 1000 + 60); TP.stopping = true; TP.key = null; }',
    'function tpStop(f = 0.5) { if (!TP.el) return; tpFade(0.0001, f); const a = TP.el, g = ++TP.gen; TP.pend = false; setTimeout(() => { if (g === TP.gen) { a.pause(); TP.stopping = false; } }, f * 1000 + 60); TP.stopping = true; TP.key = null; }   // V365: pausiert nur, wenn seitdem kein neues Stück gestartet wurde')
rep('setInterval(() => { const a = TP.el; if (a && !a.paused && TP.key && !TP.paused) {',
    'setInterval(() => { const a = TP.el; const hold = document.body.classList.contains("mapUp") || !!window.__tpHack || !!window.__tpHush || !!(typeof S !== "undefined" && S && S.duel);   // Karte, Hack/Duell und Ein-Fenster-Stummschaltung halten die Musik selbst an\n'
    '  if (a && a.paused && a.src && TP.key && !TP.paused && !TP.pend && !TP.stopping && SFX.music.on && !document.hidden && !hold) { if (++TP.stuck >= 4) { TP.stuck = 0; const p = a.play(); if (p && p.catch) p.catch(() => {}); tpFade(0.5, 0.8); } return; } TP.stuck = 0;   // V365: Wächter – hängt die Musik 2 s grundlos, neu abspielen\n'
    '  if (a && !a.paused && TP.key && !TP.paused) {')
rep('hackNow = hackUp; try {', 'hackNow = hackUp; window.__tpHack = hackUp || hackHeld; try {')
rep('const hush = on => { try { allAudio().forEach(a => { if (on) { a.dataset.wasPlaying = a.paused ? "0" : "1"; a.pause(); } else if (a.dataset.wasPlaying === "1" && TP.key && !TP.paused) { const p = a.play();',
    'const hush = on => { window.__tpHush = on; try { allAudio().forEach(a => { if (on) { if (!a.paused) a.dataset.wasPlaying = "1"; a.pause(); } else if (a.dataset.wasPlaying === "1" && TP.key && !TP.paused) { a.dataset.wasPlaying = "0"; const p = a.play();')   # V365: zweites Stummschalten löschte «lief»
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
