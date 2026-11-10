#!/usr/bin/env python3
# V567 (Martin 10.11. 21:07): ?test=cert zeigt die Urkunde direkt – nicht erst nach Spielstart/ohne offene Fenster,
# sondern sobald Splash und Sprachwahl weg sind (vorher wartete der Link oft ewig).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V566";', 'const GAME_VER = "V567";')
rep('if (q === "cert") { const w8 = () => { try { if (!S || !S.started || S.intro || document.body.classList.contains("mapUp") || uiWinOpen()) { setTimeout(w8, 500); return; } setTimeout(() => { try { window.__certNow(); } catch (e) {} }, 5000); } catch (e) {} }; setTimeout(w8, 800); }',
    'if (q === "cert") { let n8 = 0; const w8 = () => { try { const vis = id => { const e = document.getElementById(id); if (!e || e.hidden) return false; const c = getComputedStyle(e); return c.display !== "none" && c.visibility !== "hidden" && +c.opacity > 0.05; }; if ((vis("splash") || vis("ovLang")) && n8++ < 120) { setTimeout(w8, 400); return; } setTimeout(() => { try { const t = document.getElementById("tutSum"); if (t) t.style.zIndex = "1001"; window.__certNow(); } catch (e) {} }, 700); } catch (e) {} }; setTimeout(w8, 500); }   /* V567: Urkunde sofort, auch über der Weltkarte */')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
