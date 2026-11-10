#!/usr/bin/env python3
# V573 (Martin 11.11. 00:09): Im Tutorial fliegt der fallende Block ÜBER die Tutorial-Karte (nicht darunter).
# Eine durchsichtige Zeichenfläche über der Karte kopiert die Zellen des fallenden Teils aus dem Spielfeld.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V572";', 'const GAME_VER = "V573";')
JS = r'''
/* V573: fallender Block über der Tutorial-Karte */
try { (() => {
  const oc = document.createElement("canvas"); oc.id = "tutPieceCv"; document.body.appendChild(oc); const ox = oc.getContext("2d"); let shown = false;
  function frame() { requestAnimationFrame(frame); try {
    const coach = document.getElementById("coach"), on = typeof TUT !== "undefined" && TUT.on && S && S.started && !S.over && S.piece && coach && !coach.hidden && !cv.classList.contains("rot") && !cv.classList.contains("rotR") && !S.rotMode;
    if (!on) { if (shown) { ox.clearRect(0, 0, oc.width, oc.height); shown = false; } return; }
    const dpr = window.devicePixelRatio || 1, W = Math.round(innerWidth * dpr), H = Math.round(innerHeight * dpr); if (oc.width !== W || oc.height !== H) { oc.width = W; oc.height = H; }
    ox.clearRect(0, 0, W, H); shown = true;
    const card = coach.querySelector(".coachCard"), cr = card && card.getBoundingClientRect(); if (!cr || !cr.width) return;
    const r = cv.getBoundingClientRect(), sx = cv.width / r.width, sy = cv.height / r.height, p = S.piece;
    for (const [x, y] of p.cells) { const [gx, gy] = v2g(p.x + x, p.y + y); if (gy < 0) continue;
      const a = cvPt(gx, gy), b = cvPt(gx + 1, gy + 1), x0 = Math.min(a.x, b.x), y0 = Math.min(a.y, b.y), w = Math.abs(b.x - a.x), h = Math.abs(b.y - a.y);
      if (x0 + w < cr.left || x0 > cr.right || y0 + h < cr.top || y0 > cr.bottom) continue;   // nur dort, wo die Karte drüberliegt
      ox.drawImage(cv, (x0 - r.left) * sx, (y0 - r.top) * sy, w * sx, h * sy, x0 * dpr, y0 * dpr, w * dpr, h * dpr); }
  } catch (e) {} }
  requestAnimationFrame(frame);
})(); } catch (e) { console.error("v573", e); }
'''
rep('const TUT_SNAP = () =>', JS + 'const TUT_SNAP = () =>')
rep("</body>", '<style id="v573">#tutPieceCv{position:fixed;left:0;top:0;width:100vw;height:100vh;z-index:907;pointer-events:none}</style>\n</body>')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
