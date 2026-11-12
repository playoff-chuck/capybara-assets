#!/usr/bin/env python3
# V660 (Martin 12.11. 13:40): Einsatz-Fenster («Boss-Karte» mit 25/50/100 %, HACK!) nur zeigen, wenn es etwas zu setzen gibt.
# Bei den ersten zwei Boss-Hacks (solange Coach Ollies Tipps kommen) und wenn das Gold für einen Einsatz nicht reicht (< 10)
# wird es übersprungen: Ankündigung → Ollies Tipps → Duell (Einsatz 0). Der erste Hack bleibt wie bisher gratis.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V659";', 'const GAME_VER = "V660";')
rep('''openHack = function () { const r = _oh2.apply(this, arguments); try { const f = first(); hb.classList.toggle("hkFirst", f); fst.hidden = !f;
      const gb = $("hkGo"); if (f) {''',
    '''openHack = function () { const r = _oh2.apply(this, arguments); try { const f = first(); hb.classList.toggle("hkFirst", f); fst.hidden = !f;
      const nb = !f && !(S && S.testRun) && (cnt() < 2 || (+$("hkRange").max || 0) < 10);   /* V660: nichts zu setzen → Einsatz-Fenster weg */
      const gb = $("hkGo"); if (f || nb) {''')
# Boss-Karte bleibt unsichtbar, bis das Duell läuft (vorher kam sie nach 0,4 s unter Ollies Tipps wieder zum Vorschein)
rep('setTimeout(() => { try { gb.click(); } catch (e) {} setTimeout(() => { hb.style.visibility = ""; }, 400); }, 30); }',
    'setTimeout(() => { try { gb.click(); } catch (e) {} const vt = setInterval(() => { try { if (hb.hidden || $("ovHack").hidden || HK.phase !== "bet") { clearInterval(vt); hb.style.visibility = ""; } } catch (e) { clearInterval(vt); } }, 150); }, 30); }   /* V660 */')
open(p, "w", encoding="utf-8").write(s); print("ok V660")
