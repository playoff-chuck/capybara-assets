#!/usr/bin/env python3
# V599 (Martin 11.11. 07:48–07:53): (1) 10T-Airdrop erst 10 s nach dem Diplom. (2) Lektion 8 «SPLAT THEM»: der fallende Stein wird – auch wenn er
# schon vor der Lektion erschienen ist – über die Monster am rechten Rand gesetzt (aktuelle Steinform, rechter Rand stark bevorzugt).
# (3) Fortschritts-Pille «n/10» oben im Tutorial in der Farbe der Coach-Jacke (Petrol) statt Grün.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V598";', 'const GAME_VER = "V599";')
rep('''if (ov && ov.hidden) window.__TT.ad.showDrop("tut"); else if (window.__dropAd) window.__dropAd("tut"); } catch (e) {} }, 900);''',
    '''if (ov && ov.hidden) window.__TT.ad.showDrop("tut"); else if (window.__dropAd) window.__dropAd("tut"); } catch (e) {} }, 10000);   /* V598→V599: 10 s nach dem Diplom */''')
rep('''function tutSplatPlace() {   /* V587: Stein, der beim DROP ein Monster trifft (rechte Seite bevorzugt) */''',
    '''function tutSplatPlace(only) {   /* V587: Stein, der beim DROP ein Monster trifft (rechte Seite bevorzugt) · V599: only = nur diese Form */''')
rep('''    for (const k of KEYS) { let cells = SHAPES[k].c.map(p => p.slice());''',
    '''    for (const k of (only ? [only] : KEYS)) { let cells = SHAPES[k].c.map(p => p.slice());''')
rep('''const sc = 1000 + (m.cx >= W / 2 ? 500 : 0) + (k === "I" ? 50 : 0) + py + Math.random();''',
    '''const sc = 1000 + (m.cx >= W / 2 ? 500 : 0) + (m.cx >= W - 2 ? 800 : 0) + (k === "I" ? 50 : 0) + py + Math.random();''')
rep('''  const b = tutSplatPlace(); if (!b || collide(b.cells, b.px, p.y)) return; if (b.k !== p.k) return; p.cells = b.cells; p.x = b.px;''',
    '''  const b = tutSplatPlace(p.k); if (!b || collide(b.cells, b.px, p.y)) return; p.cells = b.cells; p.x = b.px;''')
rep('''tutBar .tbHead span{font-size:16px;letter-spacing:.04em;color:#fff;background:#58cc02;border:2px solid #2f7d0a;border-radius:999px;padding:3px 9px 2px;box-shadow:0 2px 0 #2f7d0a''',
    '''tutBar .tbHead span{font-size:16px;letter-spacing:.04em;color:#fff;background:#2f8f9b;border:2px solid #1c5a62;border-radius:999px;padding:3px 9px 2px;box-shadow:0 2px 0 #1c5a62''')
rep('''          const sc = 1000 + (m.cx >= W / 2 ? 500 : 0) + (m.cx >= W - 2 ? 800 : 0) + (k === "I" ? 50 : 0) + py + Math.random(); if (sc > bs) { bs = sc; best = { k, cells: cells.map(c => c.slice()), px }; } } } } }
  return best; }''', '''          const sc = 1000 + (m.cx >= W / 2 ? 500 : 0) + (m.cx >= W - 2 ? 800 : 0) + (k === "I" ? 50 : 0) + py + Math.random(); if (sc > bs) { bs = sc; best = { k, cells: cells.map(c => c.slice()), px }; } } } } }
  if (!best && only) { let cells = SHAPES[only].c.map(p => p.slice()), bx = -99;   /* V599: kein Treffer möglich → ganz rechts über den Ring-Eingang, wo die Monster herunterkommen */
    for (let px = -3; px < W + 3; px++) { if (collide(cells, px, 0)) continue; if (!cells.every(([x]) => px + x >= 1 && px + x <= W - 2)) continue; if (px > bx) bx = px; }
    if (bx > -99) best = { k: only, cells, px: bx, edge: 1 }; }
  return best; }''')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
