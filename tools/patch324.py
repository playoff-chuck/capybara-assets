"""V324 (Martin 06.11. 21:55): Nach dem Tod weiter bei der ersten Welle des aktuellen Ortes (Orte = 5 Wellen).
Gestorben in Welle 125 → weiter ab 121, in 128 → ab 126, in 103 → ab 101. Höchststand geht nie verloren (Checkpoint sinkt nie).
Gilt für Hauptmenü «CONTINUE» und Game over «CONTINUE · WAVE N» (jetzt mit Ortsname)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V323";', 'const GAME_VER = "V324";')
rep('const c = Math.floor(((w | 0) - 1) / 10) * 10; if (c >= 10 && c > window.__cpGet())',
    'const c = Math.floor(((w | 0) - 1) / 5) * 5; if (c >= 5 && c > window.__cpGet())')
rep('if (b.dataset.cont && cp >= 10)', 'if (b.dataset.cont && cp >= 5)')
rep('{ const cp = window.__cpGet ? window.__cpGet() : 0; if (cp >= 10) { const P = wherePos(cp + 1)',
    '{ const cp = window.__cpGet ? window.__cpGet() : 0; if (cp >= 5) { const P = wherePos(cp + 1)')
rep('if (bc && cp >= 10 && !(S && S.nuts)) { bc.hidden = false; bc.innerHTML = `CONTINUE · WAVE ${cp + 1}`;',
    'if (bc && cp >= 5 && !(S && S.nuts)) { bc.hidden = false; bc.innerHTML = `CONTINUE · WAVE ${cp + 1} · ${String(wherePos(cp + 1).place || "")}`;')
rep('$("btnCp").addEventListener("click", () => { const m = MODE, cp = +LS.get("tarnturm-cp-" + m) || 0; if (cp >= 10) showCamp',
    '$("btnCp").addEventListener("click", () => { const m = MODE, cp = +LS.get("tarnturm-cp-" + m) || 0; if (cp >= 5) showCamp')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
