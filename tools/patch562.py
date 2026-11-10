#!/usr/bin/env python3
# V562: Aufnahme-Links springen zuverlässig (Martin tippte auf «ДАЛЬШЕ», bevor der Sprung kam → alter Spielstand):
# mit ?test=… ist der Startbildschirm nicht antippbar, Sprung sofort nach dem Splash. RU: Nuts-Level, Preise mit Münze.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V561";', 'const GAME_VER = "V562";')
rep('  if (q && map[q]) { const go = () => { setTimeout(() => {', '  if (q && map[q]) { try { document.body.classList.add("testLink"); } catch (e) {} const go = () => { setTimeout(() => { try { document.body.classList.remove("testLink"); } catch (e) {}')
rep('/* V439: Elite-Wow direkt in W6 testen */ }, 700); };', '/* V439: Elite-Wow direkt in W6 testen */ }, 250); };')
rep('#ovMap{position:fixed;inset:0;z-index:990;', 'body.testLink #ovStart{pointer-events:none!important;opacity:.35}\n#ovMap{position:fixed;inset:0;z-index:990;')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
