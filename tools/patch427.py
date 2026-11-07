#!/usr/bin/env python3
# V427 (Martin 07.11. 23:37): Karte – alle Ortsschilder des aktuellen Kontinents sichtbar (Antarktis: aktueller Ort ± 1),
# Kamera passt sich ein (zwischen Kopfleiste und Knopfleiste, Platz für Schilder), Karte darf kleiner als der Bildschirm sein
# (oben/unten gespiegelt fortgesetzt, keine Lücke), überlappende Schilder klappen unter den Pin oder werden ausgeblendet.
# Vorher: in Asien lagen Taiga/Ice Port außerhalb, Ice Palace unter der Kopfleiste; in der Antarktis Schild unter der Knopfleiste.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V426";', 'const GAME_VER = "V427";')
rep('<img class="mapImg" src="img/worldmap.webp" alt="World map" draggable="false">',
    '<img class="mapImg" src="img/worldmap.webp" alt="World map" draggable="false"><img class="mapImg mapFlip fT" src="img/worldmap.webp" alt="" draggable="false"><img class="mapImg mapFlip fB" src="img/worldmap.webp" alt="" draggable="false">')
rep("      const W = vp.clientWidth, H = vp.clientHeight, kk = Math.max(cam.k, W / BW, H / (BW * MAP_AR)), mw = BW * kk, mh = BW * MAP_AR * kk;   /* V317: Karte deckt immer den ganzen Bildschirm */\n      let tx = W / 2 - cam.x * mw, ty = H / 2 - cam.y * mh;",
    "      const W = vp.clientWidth, H = vp.clientHeight, kk = kOf(cam), mw = BW * kk, mh = BW * MAP_AR * kk;   /* V317: Karte deckt den Bildschirm · V427: außer im Einpass-Modus (fit) */\n      let tx = W / 2 - cam.x * mw, ty = (cam.fit && cam.sy != null ? cam.sy : H / 2) - cam.y * mh;")
rep("      if (cam.free) ty = Math.max(H - mh, Math.min(0, H * .80 - mh)); else if (mh >= H)",
    "      if (cam.fit) { /* V427: frei, oben/unten gespiegelt fortgesetzt */ } else if (cam.free) ty = Math.max(H - mh, Math.min(0, H * .80 - mh)); else if (mh >= H)")
# contCam ersetzen
a = s.index("    function contCam(c) {")
b = s.index("return { x: (x0 + x1) / 2, y: (y0 + y1) / 2 + .02, k }; }", a) + len("return { x: (x0 + x1) / 2, y: (y0 + y1) / 2 + .02, k }; }")
s = s[:a] + r'''    function kOf(c) { const W = vp.clientWidth || innerWidth, H = vp.clientHeight || innerHeight; return c.fit ? Math.max(c.k, W / BW) : Math.max(c.k, W / BW, H / (BW * MAP_AR)); }
    function safeBox() { const H = vp.clientHeight || innerHeight; let top = 10, bot = H - 10;
      try { const r = ov.querySelector(".mapTop").getBoundingClientRect(); if (r.height) top = r.bottom + 6; } catch (e) {}
      try { const bar = ov.querySelector(".mapBar"); if (bar && bar.getClientRects().length) { const r = bar.getBoundingClientRect(); if (r.height) bot = r.top - 6; } } catch (e) {}
      if (bot - top < 160) { top = 10; bot = H - 10; } return { top, bot }; }
    function curPins(c) { let P = MAP_PTS[c]; if (c === 4) { const g = posOf(curWave()).g, i = Math.max(0, Math.min(5, g - 24)); P = P.slice(Math.max(0, i - 1), Math.min(6, i + 2)); } return P; }
    function contCam(c) {   /* V427: alle Schilder des Kontinents (Antarktis: Ort ± 1) zwischen Kopf- und Knopfleiste */
      const W = vp.clientWidth || innerWidth, H = vp.clientHeight || innerHeight, B = safeBox(), P = curPins(c);
      const xs = P.map(p => p[0]), ys = P.map(p => p[1]), x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
      const mX = 66, mT = 48, mB = 26, hh = Math.max(80, B.bot - B.top - mT - mB);
      const kW = (W - 2 * mX) / Math.max(.004, (x1 - x0) * BW), kH = hh / Math.max(.004, (y1 - y0) * BW * MAP_AR), kMin = Math.max(1.6, H / (2 * BW * MAP_AR) + .1);
      const k = Math.max(kMin, Math.min(4.2, kW, kH));
      return { x: (x0 + x1) / 2, y: (y0 + y1) / 2, k, fit: 1, sy: B.top + mT + hh / 2 }; }
    function declutter() { try { const ems = [...pinsEl.querySelectorAll(".mPin em")]; ems.forEach(e => e.classList.remove("dn", "hid"));
        const cur = pinsEl.querySelector(".mPin.cur em"), obs = [];
        for (const sel of [".mapTop", ".mapBar", ".mapRose"]) { const el = ov.querySelector(sel); if (el && el.getClientRects().length) obs.push(el.getBoundingClientRect()); }
        const W = vp.clientWidth, H = vp.clientHeight, placed = [];
        const bad = r => r.left < 2 || r.right > W - 2 || r.top < 2 || r.bottom > H - 2 || obs.some(q => r.left < q.right && r.right > q.left && r.top < q.bottom && r.bottom > q.top) || placed.some(q => r.left < q.right + 4 && r.right > q.left - 4 && r.top < q.bottom + 2 && r.bottom > q.top - 2);
        for (const e of [cur, ...ems.filter(x => x !== cur)]) { if (!e) continue; let r = e.getBoundingClientRect();
          if (e !== cur && bad(r)) { e.classList.add("dn"); r = e.getBoundingClientRect(); if (bad(r)) { e.classList.add("hid"); continue; } }
          placed.push(r); } } catch (e) {} }
    window.__mapDeclutter = declutter;'''  + s[b:]
rep("    function go(c, ms) { cam = c; window.__camHold = ms ? performance.now() + ms : 0; apply(ms); }",
    "    function go(c, ms) { cam = c; window.__camHold = ms ? performance.now() + ms : 0; apply(ms); clearTimeout(go._t); go._t = setTimeout(declutter, (ms || 0) + 80); }")
rep('${gi === g ? `<em>${nice(CONTS[c][2][i])}</em>` : ""}',
    '${gi === g ? `<em>${nice(CONTS[c][2][i])}</em>` : (c === Math.floor(Math.max(0, Math.min(29, g)) / 6) && (c !== 4 || Math.abs(i - (Math.max(0, Math.min(29, g)) - 24)) <= 1)) ? `<em class="sub">${nice(CONTS[c][2][i])}</em>` : ""}')
rep("      const kNow = () => { const W = vp.clientWidth, H = vp.clientHeight; return Math.max(cam.k, W / BW, H / (BW * MAP_AR)); };",
    "      const kNow = () => kOf(cam);")
rep("const kk0 = Math.max(start.cam.k, vp.clientWidth / BW, vp.clientHeight / (BW * MAP_AR)), kk = Math.max(k, vp.clientWidth / BW, vp.clientHeight / (BW * MAP_AR));",
    "const kk0 = kOf(start.cam), kk = kOf({ k, fit: start.cam.fit });")
rep("fx = start.cx - r.left - vp.clientWidth / 2, fy = start.cy - r.top - vp.clientHeight / 2;",
    "fx = start.cx - r.left - vp.clientWidth / 2, fy = start.cy - r.top - (start.cam.fit && start.cam.sy != null ? start.cam.sy : vp.clientHeight / 2);")
rep("cam = { x: wx - (fx + dx) / (BW * kk), y: wy - (fy + dy) / (BW * MAP_AR * kk), k };",
    "cam = { x: wx - (fx + dx) / (BW * kk), y: wy - (fy + dy) / (BW * MAP_AR * kk), k, fit: start.cam.fit, sy: start.cam.sy };")
rep("start = pts.size ? snap() : null; if (moved) window.__mapDragT = performance.now(); };",
    "start = pts.size ? snap() : null; if (moved) { window.__mapDragT = performance.now(); setTimeout(declutter, 60); } };")
CSS = """/* V427: Karte – Schilder & Einpassen */
#ovMap .mapFlip{top:auto;bottom:auto;transform:scaleY(-1)}
#ovMap .mapFlip.fT{top:-100%;-webkit-mask-image:linear-gradient(to bottom,#000 0,#000 6%,transparent 20%);mask-image:linear-gradient(to bottom,#000 0,#000 6%,transparent 20%)}
#ovMap .mapFlip.fB{top:100%;-webkit-mask-image:linear-gradient(to top,#000 0,#000 6%,transparent 20%);mask-image:linear-gradient(to top,#000 0,#000 6%,transparent 20%)}
#ovMap{background:#7fb9b6!important}
#ovMap .mPin em.sub{font-size:12px!important;padding:3px 6px 2px!important;border-width:2px!important;box-shadow:0 1px 0 #3a2414!important;background:#fff7e8!important;opacity:.95}
#ovMap .mPin.done em.sub{color:#4f7a2a}
#ovMap .mPin.open em.sub{color:#7a6a52}
#ovMap .mPin em.dn{top:24px!important;transform:translate(-50%,0)!important}
#ovMap .mPin em.hid{visibility:hidden}
</style>"""
rep("#ovMap .mapBar .mapWorldBtn{display:none!important}   /* V416 */\n", "#ovMap .mapBar .mapWorldBtn{display:none!important}   /* V416 */\n" + CSS.replace("</style>", ""))
open(dst, "w", encoding="utf-8").write(s)
print("ok")
