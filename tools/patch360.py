"""V360 (Martin 07.11. 02:38 «Beine beweglich»): echter Laufzyklus für den Dieb – 8 Bilder thief_w1..w8 (Nano Banana Pro, 0,28 $),
10 Bilder/s, hart gewechselt (kein Durchscheinen). Ablauf vereinfacht (Martin 02:47)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V359";', 'const GAME_VER = "V360";')
rep('const FR = [1, 2, 3, 4, 5, 6, 7].map(n => { const im = new Image(); im.decoding = "async"; im.src = "img/thief_" + n + ".webp"; return im; });',
    'const FR = [1, 2, 3, 4, 5, 6, 7].map(n => "thief_" + n).concat([1, 2, 3, 4, 5, 6, 7, 8].map(n => "thief_w" + n)).map(f => { const im = new Image(); im.decoding = "async"; im.src = "img/" + f + ".webp"; return im; });   /* V360: 7..14 = Laufzyklus */')
rep('if (ph === "walk") { const c = t * 3.6; fi = Math.floor(c) % 2; bob = (1 - Math.cos(c * Math.PI * 2)) * 1.3; }',
    'if (ph === "walk") { fi = 7 + Math.floor(t * 10) % 8; }')
rep('const walkSwap = T.prevFi != null && T.prevFi <= 1 && P.fi <= 1;',
    'const walkSwap = T.prevFi != null && T.prevFi >= 7 && P.fi >= 7;')
# Martin 02:47: einfacher Ablauf – reingehen, Gold sehen (große Augen), schnappen, rauslaufen. Kein Zurückschauen, kein Schleichen.
rep('function phase(t) { return t < 6 ? "walk" : t < 7.3 ? "back" : t < 8.4 ? "eye" : t < 10 ? "sneak" : t < 10.6 ? "grab" : "run"; }',
    'function phase(t) { return t < 8 ? "walk" : t < 9.4 ? "eye" : t < 10.6 ? "grab" : "run"; }')
rep('else if (ph === "grab") { fi = 5; tilt = 0.04 * Math.sin(Math.min(1, (t - 10) / 0.6) * Math.PI); }',
    'else if (ph === "grab") { fi = 5; tilt = 0.04 * Math.sin(Math.min(1, (t - 9.4) / 1.2) * Math.PI); }')
rep('const x = t < 6 ? x0 + (stop - x0) * (1 - Math.pow(1 - t / 6, 2))', 'const x = t < 8 ? x0 + (stop - x0) * (1 - Math.pow(1 - t / 8, 1.5))')
rep('      : t < 8.4 ? stop\n      : t < 10 ? stop + (reach - stop) * ease((t - 8.4) / 1.6)', '      : t < 9.4 ? stop\n      : t < 10 ? stop + (reach - stop) * ease((t - 9.4) / 0.6)')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
