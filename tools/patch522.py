#!/usr/bin/env python3
"""V522 (Martin 09.11. 17:04/17:35): Kalenderblatt – Häkchen wie mit dem Stift aufs Papier geschrieben (dunkle Tinte, kein Leuchten)
mit Schreibgeräusch (sfx/pen.mp3), dann Abreißen mit Geräusch «Perforiert weich» (sfx/tear.mp3).
Heute schon geschaffte Mission wird einmal nochmal gezeigt (Migration v522).
Aufruf: python3 tools/patch522.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V521";', 'const GAME_VER = "V522";')
rep('else if (!DAILY.v519) {', 'else if (!DAILY.v522) {')
rep('DAILY.v519 = 1; }', 'DAILY.v519 = 1; DAILY.v522 = 1; }')
rep('<svg class="dlChk" viewBox="0 0 100 100"><path d="M18 54 L42 76 L84 24"/></svg>',
    '<svg class="dlChk" viewBox="0 0 100 100"><path d="M16 50 C22 55 30 64 38 75 C46 58 62 36 86 14"/></svg>')
rep('setTimeout(() => { o.classList.add("chk"); try { SFX.init(); snd("confirm"); } catch (e) {} }, 500);\n  setTimeout(() => { o.classList.add("tear"); try { snd("uiTap"); } catch (e) {} }, 1900);\n  setTimeout(() => o.remove(), 3100);',
    'setTimeout(() => { o.classList.add("chk"); dlFx("pen"); }, 500);\n  setTimeout(() => { o.classList.add("tear"); dlFx("tear"); }, 1600);\n  setTimeout(() => o.remove(), 2800);')
rep('/* V519: altes Blatt mit grünem Häkchen abreißen */',
    '/* V519: altes Blatt mit grünem Häkchen abreißen */\nfunction dlFx(n) { try { if (SFX.muted) return; const a = new Audio("sfx/" + n + ".mp3"); a.volume = Math.min(1, Math.max(0.5, 8 * Math.pow(SFX.vol || 0.3, 2))); a.play().catch(() => {}); } catch (e) {} }   /* V522 */')
rep('#dailyLeaf .dlChk{position:absolute;left:50%;top:52%;width:120%;height:120%;transform:translate(-50%,-50%) scale(.4);opacity:0;pointer-events:none;overflow:visible;filter:drop-shadow(0 3px 0 #1d5e1d)}',
    '#dailyLeaf .dlChk{position:absolute;left:50%;top:50%;width:105%;height:105%;transform:translate(-50%,-50%) rotate(-4deg);opacity:0;pointer-events:none;overflow:visible;mix-blend-mode:multiply}')
rep('#dailyLeaf .dlChk path{fill:none;stroke:#35c435;stroke-width:16;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:110;stroke-dashoffset:110}',
    '#dailyLeaf .dlChk path{fill:none;stroke:#1f6b2a;stroke-opacity:.88;stroke-width:7;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:120;stroke-dashoffset:120}')
rep('#dailyLeaf .dlOld.chk .dlChk{opacity:1;transform:translate(-50%,-50%) scale(1);transition:transform .35s cubic-bezier(.2,1.6,.4,1),opacity .15s}',
    '#dailyLeaf .dlOld.chk .dlChk{opacity:1}')
rep('#dailyLeaf .dlOld.chk .dlChk path{stroke-dashoffset:0;transition:stroke-dashoffset .45s ease-out .1s}',
    '#dailyLeaf .dlOld.chk .dlChk path{stroke-dashoffset:0;transition:stroke-dashoffset .5s cubic-bezier(.5,0,.4,1) .03s}')
open(p, "w", encoding="utf-8").write(s); print("ok V522")
