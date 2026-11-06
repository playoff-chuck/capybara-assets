"""V361 (Martin 07.11. 02:51): Auf schmalen Handys lief der Dieb auf der Stelle (Start rechts vom General-Kreis = schon am Ziel).
Jetzt kommt er immer von links ins Bild und läuft hinter dem General-Kreis durch (Kreis wird aus dem Dieb ausgeblendet)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V360";', 'const GAME_VER = "V361";')
rep('let x0 = cr.left - SZ / 2, fade = 1; if (ga && ga.width && feet - (SZ - 5) * sc < ga.bottom) { x0 = Math.max(x0, ga.right + SZ * sc / 2 + 6); fade = Math.min(1, t / 0.6); }',
    'let x0 = Math.min(cr.left, 0) - SZ * sc / 2 - 4, fade = 1;   /* V361: immer von links herein */')
rep('el.style.transformOrigin = "50% 100%"; el.style.opacity = fade.toFixed(2);',
    'el.style.transformOrigin = "50% 100%"; el.style.opacity = fade.toFixed(2);\n'
    '    { const tx = x - SZ / 2, ty = Math.round(feet - SZ + 5); let mk = "none";   /* V361: hinter dem General-Kreis durch */\n'
    '      if (ga && ga.width) { const ax = ga.left + ga.width / 2, ay = ga.top + ga.height / 2, ar = ga.width / 2 + 3, lx = SZ / 2 + (ax - tx - SZ / 2) / sc, ly = SZ + (ay - ty - SZ) / sc, lr = ar / sc;\n'
    '        if (lx + lr > 0 && lx - lr < SZ && ly + lr > 0 && ly - lr < SZ) mk = `radial-gradient(circle ${lr.toFixed(1)}px at ${lx.toFixed(1)}px ${ly.toFixed(1)}px, transparent ${(lr - 0.5).toFixed(1)}px, #000 ${(lr + 0.5).toFixed(1)}px)`; }\n'
    '      if (el.__mk !== mk) { el.__mk = mk; el.style.webkitMaskImage = mk; el.style.maskImage = mk; } }')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
