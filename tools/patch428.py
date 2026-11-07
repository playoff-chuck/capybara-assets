#!/usr/bin/env python3
# V428 (Martin 07.11. 23:54, Screenshot «da ist etwas doppelt»): gespiegelte Kartenränder (V427) entfernt – beim Herauszoomen
# erschienen doppelte Kanten/Ecken. Jetzt: Herauszoomen nur bis «Karte füllt den Bildschirm» bzw. so weit, wie der Kontinent es braucht;
# ist die Karte kleiner als der Bildschirm (Asien/Antarktis auf schmalen Handys), laufen Ober- und Unterkante weich ins Meer aus.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V427";', 'const GAME_VER = "V428";')
rep("return { x: (x0 + x1) / 2, y: (y0 + y1) / 2, k, fit: 1, sy: B.top + mT + hh / 2 }; }",
    "return { x: (x0 + x1) / 2, y: (y0 + y1) / 2, k, fit: 1, sy: B.top + mT + hh / 2, kmin: Math.min(k, Math.max(W / BW, H / (BW * MAP_AR))) }; }")
rep("return c.fit ? Math.max(c.k, W / BW) : Math.max(c.k, W / BW, H / (BW * MAP_AR)); }",
    "return c.fit ? Math.max(c.k, W / BW, c.kmin || 0) : Math.max(c.k, W / BW, H / (BW * MAP_AR)); }")
rep("const kk0 = kOf(start.cam), kk = kOf({ k, fit: start.cam.fit });", "const kk0 = kOf(start.cam), kk = kOf({ k, fit: start.cam.fit, kmin: start.cam.kmin });")
rep("k, fit: start.cam.fit, sy: start.cam.sy };", "k, fit: start.cam.fit, sy: start.cam.sy, kmin: start.cam.kmin };")
rep('world.style.transform = `translate(${tx}px,${ty}px) scale(${kk})`;', 'world.style.transform = `translate(${tx}px,${ty}px) scale(${kk})`; ov.classList.toggle("mapSmall", mh < H - 1);')
rep("#ovMap{background:#7fb9b6!important}",
    "#ovMap{background:#7fb9b6!important}\n#ovMap .mapFlip{display:none!important}\n"
    "#ovMap.mapSmall .mapImg{-webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 7%,#000 97%,transparent 100%);mask-image:linear-gradient(to bottom,transparent 0,#000 7%,#000 97%,transparent 100%)}\n"
    "#ovMap.mapSmall .mapWrap.wR{-webkit-mask-image:linear-gradient(to right,transparent 0,#000 5%),linear-gradient(to bottom,transparent 0,#000 7%,#000 97%,transparent 100%);mask-image:linear-gradient(to right,transparent 0,#000 5%),linear-gradient(to bottom,transparent 0,#000 7%,#000 97%,transparent 100%);-webkit-mask-composite:source-in;mask-composite:intersect}\n"
    "#ovMap.mapSmall .mapWrap.wL{-webkit-mask-image:linear-gradient(to right,#000 95%,transparent 100%),linear-gradient(to bottom,transparent 0,#000 7%,#000 97%,transparent 100%);mask-image:linear-gradient(to right,#000 95%,transparent 100%),linear-gradient(to bottom,transparent 0,#000 7%,#000 97%,transparent 100%);-webkit-mask-composite:source-in;mask-composite:intersect}")
open(dst, "w", encoding="utf-8").write(s)
print("ok")
