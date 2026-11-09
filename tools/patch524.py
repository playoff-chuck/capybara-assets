#!/usr/bin/env python3
"""V524 (Martin 09.11. 17:43): Weltkarte – Schilder überschneiden sich nie.
Algorithmus (gierig nach Vorrang): aktueller Ort > Nuts-Schilder (NUTS-Tafel, ☠ L-Schild) > übrige Ortsnamen.
Jedes Schild probiert der Reihe nach feste Plätze (oben / unten / links / rechts bzw. unter / links / rechts vom Gebiet).
Erst streng (keine anderen Schilder, keine Punkte, nicht unter Leisten/Rand), dann locker (Punkte dürfen berührt werden),
sonst wird es ausgeblendet. Läuft nach jedem Schwenk/Zoom.
Aufruf: python3 tools/patch524.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V523";', 'const GAME_VER = "V524";')
i = s.find('    function declutter() { try { const ems = [...pinsEl.querySelectorAll(".mPin em")];'); j = s.find('    window.__mapDeclutter = declutter;', i); assert i > 0 and j > i
s = s[:i] + '''    function declutter() { try {   /* V524: keine Überschneidungen – jedes Schild sucht sich einen freien Platz */
        const PC = ["dn", "lf", "rt", "hid"], all = [...pinsEl.querySelectorAll(".mPin em, .nzTag, .nzL")]; all.forEach(e => e.classList.remove(...PC));
        const obs = []; for (const sel of [".mapTop", ".mapBar", ".mapRose"]) { const el = ov.querySelector(sel); if (el && el.getClientRects().length) obs.push(el.getBoundingClientRect()); }
        const dots = [...pinsEl.querySelectorAll(".mPin i, .nzPin")].filter(d => d.getClientRects().length).map(d => [d, d.getBoundingClientRect()]);
        const W = vp.clientWidth, H = vp.clientHeight, placed = [], hit = (r, q, m) => r.left < q.right + m && r.right > q.left - m && r.top < q.bottom + m && r.bottom > q.top - m;
        const bad = (e, r, strict) => r.left < 2 || r.right > W - 2 || r.top < 2 || r.bottom > H - 2 || obs.some(q => hit(r, q, 0)) || placed.some(q => hit(r, q, 3))
          || (strict && dots.some(([d, q]) => !e.parentNode.contains(d) && hit(r, q, 1)));
        const cur = pinsEl.querySelector(".mPin.cur em"), nz = [...pinsEl.querySelectorAll(".nzTag, .nzL")].filter(e => e.getClientRects().length);
        const order = [cur, ...nz, ...all.filter(e => e !== cur && !nz.includes(e) && e.matches(".mPin em"))].filter(Boolean);
        for (const e of order) { let ok = false;
          for (const strict of [true, false]) { for (const c of ["", "dn", "lf", "rt"]) { e.classList.remove(...PC); if (c) e.classList.add(c); const r = e.getBoundingClientRect();
              if (!r.width || !bad(e, r, strict) || (e === cur && !c && !strict)) { placed.push(r); ok = true; break; } } if (ok) break; }
          if (!ok) { e.classList.remove(...PC); e.classList.add("hid"); } } } catch (e) {} }
''' + s[j:]
rep('#ovMap .mPin em.hid{visibility:hidden}', '''#ovMap .mPin em.hid{visibility:hidden}
#ovMap .mPin em.lf{top:0!important;left:-14px!important;transform:translate(-100%,-50%)!important}#ovMap .mPin em.rt{top:0!important;left:14px!important;transform:translate(0,-50%)!important}
.mNuts .nzTag.dn{top:-58px!important}.mNuts .nzTag.lf{top:22px!important;left:-44px!important;transform:translate(-100%,0)!important}.mNuts .nzTag.rt{top:22px!important;left:44px!important;transform:none!important}.mNuts .nzTag.hid{visibility:hidden}
.mNuts .nzL.dn{top:auto!important;bottom:-4px!important}.mNuts .nzL.lf{left:0!important;top:50%!important;transform:translate(-100%,-50%)!important}.mNuts .nzL.rt{left:100%!important;top:50%!important;transform:translate(0,-50%)!important}.mNuts .nzL.hid{visibility:hidden}''')
open(p, "w", encoding="utf-8").write(s); print("ok V524")
