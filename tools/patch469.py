#!/usr/bin/env python3
"""V469 – t136: Daily-Kalenderblatt schrumpft auf kleinen Screens, bis es den CONTINUE/PLAY-Knopf nicht mehr verdeckt
(360×640, alle Sprachen); Spielname «CAPYBARA SQUAD» im Titel/Splash wird nie übersetzt (translate="no").
Nutzung: python3 tools/patch469.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V468";', 'const GAME_VER = "V469";')
# Spielname nie übersetzen
rep('<div class="spT">CAPYBARA<span>SQUAD</span></div>', '<div class="spT" translate="no">CAPYBARA<span>SQUAD</span></div>')
rep('<h1>CAPYBARA<span>SQUAD</span></h1>', '<h1 translate="no">CAPYBARA<span>SQUAD</span></h1>')
rep('const p = n.parentNode; if (!p || I18N_SKIP.has(p.nodeName)) return; const m = i18nDone.get(n);',
    'const p = n.parentNode; if (!p || I18N_SKIP.has(p.nodeName)) return; if (p.closest && p.closest("[translate=no]")) return;   /* V469 */ const m = i18nDone.get(n);')
# Daily-Blatt: Skalierung über --dlS, Ursprung oben rechts
rep('z-index:60;font-family:"Baloo 2",system-ui,sans-serif;color:#3a2414;transform:rotate(2.5deg);',
    'z-index:60;font-family:"Baloo 2",system-ui,sans-serif;color:#3a2414;transform:rotate(2.5deg) scale(var(--dlS,1));transform-origin:100% 0;')
rep('    + `<div class="streak">${dots}</div><div class="sub">7-day chain · 1 shield day</div><i class="corner"></i></div>`;\n}',
    '    + `<div class="streak">${dots}</div><div class="sub">7-day chain · 1 shield day</div><i class="corner"></i></div>`;\n'
    '  dailyFit();\n}\n'
    '/* V469 (t136): Blatt darf den CONTINUE/PLAY-Knopf nie verdecken – sonst kleiner (min. 0,55) */\n'
    'function dailyFit() { try { const el = document.getElementById("dailyLeaf"); if (!el) return;\n'
    '  const bt = [...document.querySelectorAll("#modeList .playBtn, #btnResume")].find(b => b.getClientRects().length && !b.hidden); if (!bt) { el.style.removeProperty("--dlS"); return; }\n'
    '  const top = el.getBoundingClientRect().top, h = el.offsetHeight, w = el.offsetWidth, r = bt.getBoundingClientRect(), vw = window.innerWidth;\n'
    '  if (!h || r.right < vw - 12 - w) { el.style.removeProperty("--dlS"); return; }\n'
    '  const room = r.top - 8 - top, k = h > room ? Math.max(.55, room / h) : 1;\n'
    '  const v = k >= .999 ? "" : k.toFixed(3); if ((el.style.getPropertyValue("--dlS") || "") !== v) { if (v) el.style.setProperty("--dlS", v); else el.style.removeProperty("--dlS"); }\n'
    '} catch (e) {} }\n'
    'window.addEventListener("resize", () => dailyFit());')
# auch nach Sprachwechsel/Rendern der Knöpfe nachziehen (Intervall läuft ohnehin alle 0,8 s)
rep('if (!document.getElementById("dailyLeaf") || dailyKey() !== DAILY.day) dailyLeaf(); } catch (e) {} }, 800);',
    'if (!document.getElementById("dailyLeaf") || dailyKey() !== DAILY.day) dailyLeaf(); else dailyFit(); } catch (e) {} }, 800);')
open(dst, "w", encoding="utf-8").write(s)
print("ok V469")
