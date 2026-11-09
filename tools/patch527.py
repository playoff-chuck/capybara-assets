#!/usr/bin/env python3
"""V527 (Martin 09.11. 19:48): Häkchen und Marker-Geräusch synchron, Geräusch 70 % leiser.
- sfx/pen.mp3 neu geschnitten: Abstrich (0,13 s) + Aufstrich (0,18 s) direkt hintereinander, Lautstärke ×0,3.
- Häkchen aus zwei Strichen: kurzer Abstrich 0,13 s, dann Aufstrich 0,18 s – genau wie im Ton.
- Ton wird vorher geladen; das Zeichnen startet, sobald der Ton wirklich spielt (Ereignis «playing», sonst nach 120 ms).
Aufruf: python3 tools/patch527.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V526";', 'const GAME_VER = "V527";')
rep('function dlFx(n) { try { if (SFX.muted) return; const a = new Audio("sfx/" + n + ".mp3?v=526");',
    'function dlPrep(n) { try { if (SFX.muted) return null; const a = new Audio("sfx/" + n + ".mp3?v=527"); a.preload = "auto"; a.volume = Math.min(1, Math.max(0.5, 8 * Math.pow(SFX.vol || 0.3, 2))); a.load(); return a; } catch (e) { return null; } }   /* V527 */\nfunction dlFx(n) { try { if (SFX.muted) return; const a = new Audio("sfx/" + n + ".mp3?v=527");')
rep('<svg class="dlChk" viewBox="0 0 100 100"><path d="M16 50 C22 55 30 64 38 75 C46 58 62 36 86 14"/></svg>',
    '<svg class="dlChk" viewBox="0 0 100 100"><path class="c1" pathLength="1" d="M16 50 C22 55 30 64 38 75"/><path class="c2" pathLength="1" d="M38 75 C46 58 62 36 86 14"/></svg>')
rep('  el.appendChild(o);\n  setTimeout(() => { o.classList.add("chk"); dlFx("pen"); }, 500);',
    '  el.appendChild(o); const pen = dlPrep("pen");\n  setTimeout(() => { let go = false; const draw = () => { if (go) return; go = true; o.classList.add("chk"); };\n    if (pen) { try { pen.addEventListener("playing", draw, { once: true }); pen.play().catch(draw); } catch (e) { draw(); } setTimeout(draw, 120); } else draw(); }, 500);')
rep('#dailyLeaf .dlChk path{fill:none;stroke:#1f6b2a;stroke-opacity:.88;stroke-width:7;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:120;stroke-dashoffset:120}',
    '#dailyLeaf .dlChk path{fill:none;stroke:#1f6b2a;stroke-opacity:.88;stroke-width:7;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1 1;stroke-dashoffset:1}')
rep('#dailyLeaf .dlOld.chk .dlChk path{stroke-dashoffset:0;transition:stroke-dashoffset .5s cubic-bezier(.5,0,.4,1) .03s}',
    '#dailyLeaf .dlOld.chk .dlChk path{stroke-dashoffset:0}#dailyLeaf .dlOld.chk .dlChk .c1{transition:stroke-dashoffset .13s linear}#dailyLeaf .dlOld.chk .dlChk .c2{transition:stroke-dashoffset .18s cubic-bezier(.3,0,.6,1) .13s}')
open(p, "w", encoding="utf-8").write(s); print("ok V527")
