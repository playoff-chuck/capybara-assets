#!/usr/bin/env python3
# V597 (Martin 11.11. 07:39 «Schicke blocks gleich so dass sich Linie bildet!!!»): Lektion 1 «DROP A BLOCK» – beim ersten Tipp auf DROP
# werden die übrigen leeren inneren Felder der Reihe, in der der Stein landet, aufgefüllt: die Reihe schließt sich sofort (Gold + Effekt).
# Einmal je Kurs (TUT.l1fill). Außerdem (Martin 07:41): der eingeflogene Tutorial-Stein (#tutPieceCv) liegt nie über Pause/Karte.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V596";', 'const GAME_VER = "V597";')
rep('''const _hd = hardDrop; hardDrop = function () { try { if (TUT.on && TUT.step === 0 && S && !S.duel) TUT.dropTap = (TUT.dropTap || 0) + 1; } catch (e) {} return _hd.apply(this, arguments); };''',
    '''const _hd = hardDrop; hardDrop = function () { try { if (TUT.on && TUT.step === 0 && S && !S.duel) TUT.dropTap = (TUT.dropTap || 0) + 1; } catch (e) {}
    try { const p = S.piece; if (TUT.on && TUT.step === 0 && !TUT.l1fill && p && !S.duel && !S.rotMode && canAct() && performance.now() >= (S.dropLockUntil || 0)) {   /* V597: erste Reihe schließt sich sofort */
      const W = VW(); let py = p.y; while (!collide(p.cells, p.x, py + 1)) py++; let low = 0; for (const [, y] of p.cells) low = Math.max(low, py + y);
      const mine = new Set(p.cells.filter(([, y]) => py + y === low).map(([x]) => p.x + x)); let col = 0;
      for (let x = 1; x < W - 1; x++) { const v = S.grid[vIdx(x, low)]; if (v && v !== TNT) { col = v; break; } }
      for (let x = 1; x < W - 1; x++) if (!mine.has(x) && !S.grid[vIdx(x, low)]) S.grid[vIdx(x, low)] = col || ((x % 4) + 1);
      TUT.l1fill = 1; } } catch (e) {}
    return _hd.apply(this, arguments); };''')
rep("TUT.on = true;", "TUT.on = true; TUT.l1fill = 0;")
rep('''!S.rotMode && !S.shop && !S.sel && (() => { const sh = document.getElementById("sheet"); return !sh || sh.hidden; })();   /* V589: nie über dem Laden */''',
    '''!S.rotMode && !S.shop && !S.sel && !S.paused && !S.mapShow && !S.mapFly && (() => { const sh = document.getElementById("sheet"), op = document.getElementById("ovPause"); return (!sh || sh.hidden) && (!op || op.hidden); })();   /* V589: nie über dem Laden · V597: nie über Pause/Karte */''')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
