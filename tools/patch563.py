#!/usr/bin/env python3
# V563: Laden bleibt nach einem Kauf an derselben Stelle (Martin 10.11. 16:57) – vorher rutschte die Liste bei Zehntonne,
# Betonmischer, Lockdown um ~100 px. Jetzt: die angetippte Karte bleibt genau dort, wo der Finger war (Anker statt nur scrollTop).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V562";', 'const GAME_VER = "V563";')
rep('''  renderShop = function () { const v = grab(); const r = _rs.apply(this, arguments); put(v); requestAnimationFrame(() => put(v)); setTimeout(() => put(v), 60); return r; };''',
    '''  /* V563: Anker – die zuletzt angetippte Karte bleibt an ihrer Bildschirmstelle */
  let anc = null; document.addEventListener("pointerdown", e => { const b = e.target.closest && e.target.closest("#sheet [data-shop],#sheet [data-pocket]"); anc = b ? { sel: b.dataset.shop ? `[data-shop="${b.dataset.shop}"]` : `[data-pocket="${b.dataset.pocket}"]`, t: performance.now() } : null; }, true);
  const fix = (sel, top0) => { try { const el = document.querySelector("#sheet " + sel); const sc = document.querySelector("#sheet .shopTiles") || document.querySelector("#sheet .shopGrid"); if (!el || !sc) return; const d = el.getBoundingClientRect().top - top0; if (Math.abs(d) > 1) sc.scrollTop += d; } catch (e) {} };
  renderShop = function () { const v = grab(); let a = null; if (anc && performance.now() - anc.t < 3000) { const el = document.querySelector("#sheet " + anc.sel); if (el) a = { sel: anc.sel, top: el.getBoundingClientRect().top }; }
    const r = _rs.apply(this, arguments); put(v); if (a) fix(a.sel, a.top);
    requestAnimationFrame(() => { put(v); if (a) fix(a.sel, a.top); }); setTimeout(() => { put(v); if (a) fix(a.sel, a.top); }, 60); setTimeout(() => { if (a) fix(a.sel, a.top); }, 400); return r; };''')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
