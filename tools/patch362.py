"""V362 (Martin 07.11. 02:55): Dieb greift genau in die Gold-Anzeige (Hand statt Körpermitte unter dem Gold);
beim Weglaufen bewegen sich die Beine (Renn-Zyklus mit Geldsack thief_r1..r4, Nano Banana Pro 0,14 $)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V361";', 'const GAME_VER = "V362";')
rep('.concat([1, 2, 3, 4, 5, 6, 7, 8].map(n => "thief_w" + n))', '.concat([1, 2, 3, 4, 5, 6, 7, 8].map(n => "thief_w" + n)).concat([1, 2, 3, 4].map(n => "thief_r" + n))')
rep('else { fi = 6; const c = t * 2.6; bob = (1 - Math.cos(c * Math.PI * 2)) * 2.4; tilt = 0.07 + Math.sin(c * Math.PI * 2) * 0.035; }',
    'else { fi = 15 + Math.floor(t * 9) % 4; tilt = 0.05; }   /* V362: Renn-Zyklus mit Geldsack */')
rep('const t = T.t, reach = Math.max(cr.left + SZ / 2, gx - 18), stop = reach - 30',
    'const t = T.t, sc0 = Math.max(0.62, Math.min(1, (feet - 26) / (SZ - 5))), reach = Math.max(cr.left + SZ / 2, gx - 38 * sc0), stop = reach - 30')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
