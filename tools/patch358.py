"""V358 (Martin 07.11. 02:23): Dieb lief auf Höhe der Gold-Anzeige durch die Kopfleiste und überdeckte den Kreis des Generals.
Jetzt läuft er auf der oberen Spur des Spielfelds (Füße auf der Spur) und greift von unten in die Gold-Anzeige."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V357";', 'const GAME_VER = "V358";')
rep('const gy = r.top + r.height / 2, t = T.t, stop = r.left - 112, reach = r.left - 84, end = innerWidth + SZ;',
    'const cvE = document.getElementById("cv"), cr = cvE ? cvE.getBoundingClientRect() : { left: 0, top: 120, width: innerWidth };   /* V358: auf der oberen Spur */\n'
    '    const gw = (window.__gdim && window.__gdim()[0]) || 12, cell = cr.width / gw, feet = cr.top + cell * 0.92, gx = r.left + r.width / 2;\n'
    '    const t = T.t, reach = Math.max(cr.left + SZ / 2, gx - 18), stop = reach - 30, end = innerWidth + SZ;')
rep("el.style.transform = `translate(${(x - SZ / 2).toFixed(1)}px,${Math.round(Math.max(gy - SZ + 30, 4))}px)`;",
    "el.style.transform = `translate(${(x - SZ / 2).toFixed(1)}px,${Math.round(feet - SZ + 5)}px)`;")
rep('const x = t < 6 ? -SZ + (stop + SZ) * (1 - Math.pow(1 - t / 6, 2))',
    'const x0 = cr.left - SZ / 2, x = t < 6 ? x0 + (stop - x0) * (1 - Math.pow(1 - t / 6, 2))')
# kleine Bildschirme: kleiner zeichnen und erst rechts vom General-Kreis einblenden
rep("const x0 = cr.left - SZ / 2, x = t < 6",
    "const sc = Math.max(0.62, Math.min(1, (feet - 26) / (SZ - 5))), ga = (document.getElementById(\"genAv\") || { getBoundingClientRect: () => null }).getBoundingClientRect();\n"
    "    let x0 = cr.left - SZ / 2, fade = 1; if (ga && ga.width && feet - (SZ - 5) * sc < ga.bottom) { x0 = Math.max(x0, ga.right + SZ * sc / 2 + 6); fade = Math.min(1, t / 0.6); }\n"
    "    const x = t < 6")
rep("el.style.transform = `translate(${(x - SZ / 2).toFixed(1)}px,${Math.round(feet - SZ + 5)}px)`;",
    "el.style.transformOrigin = \"50% 100%\"; el.style.opacity = fade.toFixed(2); el.style.transform = `translate(${(x - SZ / 2).toFixed(1)}px,${Math.round(feet - SZ + 5)}px) scale(${sc.toFixed(3)})`;")
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
