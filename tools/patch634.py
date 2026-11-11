#!/usr/bin/env python3
# V634 (Martin 11.11. 16:00): Erster Boss-Hack – nur die violette Boss-Werbung («ПОБЕДИ БОССА!»), die Boss-Karte («Босс вызывает тебя на взлом!») entfällt:
# nach «ВЗЛОМАТЬ БОССА» direkt Ollies Tipps, dann das Gratis-Duell.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V633";', 'const GAME_VER = "V634";')
rep('const gb = $("hkGo"); if (f) { $("hkRange").value = 0; hkStakeUI(); gb.textContent = "NEXT ▶"; }',
    'const gb = $("hkGo"); if (f) { $("hkRange").value = 0; hkStakeUI(); gb.textContent = "NEXT ▶"; hb.style.visibility = "hidden"; setTimeout(() => { try { gb.click(); } catch (e) {} setTimeout(() => { hb.style.visibility = ""; }, 400); }, 30); }   /* V634: Boss-Karte überspringen */')
open(p, "w", encoding="utf-8").write(s)
print("ok V634")
