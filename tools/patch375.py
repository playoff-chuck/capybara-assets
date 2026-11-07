"""V375 (To-do 08, Martin): Nuts-Territorien auf der Karte + Nuts-Faktor.
Je Kontinent mit Nuts-Abstecher (Südamerika, Afrika, Asien, Nordamerika) ein Totenkopf-Gebiet mit bestem Level.
Nuts-Faktor = Durchschnitt über alle 4 Territorien von (bestes Level / 15): 15 = 100 %, 30 = 200 %. Steht unter der Windrose."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V374";', 'const GAME_VER = "V375";')
rep('        r.innerHTML = `<svg viewBox="0 0 60 60" aria-hidden="true">',
    '        const nzb = [0, 1, 2, 3].map(c => { try { return nzBest(c); } catch (e) { return 0; } }), nzf = Math.round(nzb.reduce((a, b) => a + b / 15, 0) / 4 * 100);   /* V375: Nuts-Territorien + Faktor */\n'
    '        pinsEl.insertAdjacentHTML("beforeend", nzb.map((b, c) => { const P = MAP_PTS[c]; if (!P) return ""; const x = P.reduce((a, p) => a + p[0], 0) / P.length, y = P.reduce((a, p) => a + p[1], 0) / P.length;\n'
    '          return `<div class="mNuts${b ? " on" : ""}" style="left:${(x * 100 - 6).toFixed(2)}%;top:${(y * 100 + 7).toFixed(2)}%"><span>☠ ${b ? "L" + b : "—"}</span></div>`; }).join(""));\n'
    '        r.innerHTML = `<svg viewBox="0 0 60 60" aria-hidden="true">')
rep('`${i + 4}★ ${c}`).join(" · ")}</div>`;',
    '`${i + 4}★ ${c}`).join(" · ")}</div><div class="rsNuts">☠ Nuts ${nzf} %</div>`;')
rep('.mapRose .rsCnt{font-size:9px;opacity:.9;text-align:center;line-height:1.25}',
    '.mapRose .rsCnt{font-size:9px;opacity:.9;text-align:center;line-height:1.25}\n'
    '.mapRose .rsNuts{font-size:11px;color:#ff6fb5}\n'
    '.mNuts{position:absolute;width:0;height:0;pointer-events:none}\n'
    '.mNuts span{position:absolute;left:0;top:0;transform:translate(-50%,-50%) scale(var(--ik,1));white-space:nowrap;font:700 13px/1 system-ui,sans-serif!important;padding:4px 8px!important;border-radius:10px;width:auto!important;height:auto!important;min-width:0!important;background:rgba(40,20,40,.55);color:#ddd;border:1.5px dashed #b9a;opacity:.75}\n'
    '.mNuts.on span{background:#3a1430;color:#ff9fd0;border:1.5px solid #ff6fb5;opacity:1;box-shadow:0 0 8px rgba(255,111,181,.6)}')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
