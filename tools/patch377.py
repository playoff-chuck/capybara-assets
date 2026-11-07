"""V377 (Martin 07.11. 13:32): Weltkarte frei bewegen – mit einem Finger ziehen (verschieben), mit zwei Fingern zoomen (Pinch),
am PC Mausrad zoomen. Nur im freien Ansehen (browse), nicht während Flug-Szenen. Antippen eines Kontinents funktioniert weiter
(nur wenn nicht gezogen wurde)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V376";', 'const GAME_VER = "V377";')
rep('    vp.addEventListener("click", e => { if (mode !== "browse") return;',
    '''    { /* V377: ziehen + Pinch-Zoom + Mausrad */
      const pts = new Map(); let start = null, moved = false;
      const kNow = () => { const W = vp.clientWidth, H = vp.clientHeight; return Math.max(cam.k, W / BW, H / (BW * MAP_AR)); };
      const clampK = k => Math.max(1, Math.min(6, k));
      const snap = () => { const a = [...pts.values()]; return { a, cx: a.reduce((s, p) => s + p.x, 0) / a.length, cy: a.reduce((s, p) => s + p.y, 0) / a.length, d: a.length > 1 ? Math.hypot(a[0].x - a[1].x, a[0].y - a[1].y) : 0, cam: { ...cam } }; };
      vp.addEventListener("pointerdown", e => { if (mode !== "browse") return; pts.set(e.pointerId, { x: e.clientX, y: e.clientY }); try { vp.setPointerCapture(e.pointerId); } catch (er) {} start = snap(); if (pts.size === 1) moved = false; });
      vp.addEventListener("pointermove", e => { if (mode !== "browse" || !pts.has(e.pointerId) || !start) return; pts.get(e.pointerId).x = e.clientX; pts.get(e.pointerId).y = e.clientY;
        const n = snap(), dx = n.cx - start.cx, dy = n.cy - start.cy; if (Math.hypot(dx, dy) > 8 || (n.d && Math.abs(n.d - start.d) > 8)) moved = true; if (!moved) return;
        let k = start.cam.k; if (pts.size > 1 && start.d > 10) k = clampK(Math.max(start.cam.k, vp.clientWidth / BW) * n.d / start.d);
        const kk0 = Math.max(start.cam.k, vp.clientWidth / BW, vp.clientHeight / (BW * MAP_AR)), kk = Math.max(k, vp.clientWidth / BW, vp.clientHeight / (BW * MAP_AR));
        const r = vp.getBoundingClientRect(), fx = start.cx - r.left - vp.clientWidth / 2, fy = start.cy - r.top - vp.clientHeight / 2;
        const wx = start.cam.x + fx / (BW * kk0), wy = start.cam.y + fy / (BW * MAP_AR * kk0);   /* Weltpunkt unter den Fingern bleibt dort */
        cam = { x: wx - (fx + dx) / (BW * kk), y: wy - (fy + dy) / (BW * MAP_AR * kk), k };
        cam.x = Math.max(0, Math.min(1, cam.x)); cam.y = Math.max(0, Math.min(1, cam.y)); window.__camHold = 0; apply(0); });
      const up = e => { if (!pts.has(e.pointerId)) return; pts.delete(e.pointerId); start = pts.size ? snap() : null; if (moved) window.__mapDragT = performance.now(); };
      vp.addEventListener("pointerup", up); vp.addEventListener("pointercancel", up);
      vp.addEventListener("wheel", e => { if (mode !== "browse") return; e.preventDefault(); cam = { ...cam, k: clampK(kNow() * (e.deltaY < 0 ? 1.15 : 1 / 1.15)) }; apply(120); }, { passive: false });
    }
    vp.addEventListener("click", e => { if (mode !== "browse") return; if (performance.now() - (window.__mapDragT || 0) < 300) return;   /* V377: nach Ziehen kein Antippen */''')
rep('#ovMap .mapVp,#ovMap .mapTop{transition:opacity .7s ease}',
    '#ovMap .mapVp,#ovMap .mapTop{transition:opacity .7s ease}\n#ovMap.browse .mapVp{touch-action:none;cursor:grab}')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
