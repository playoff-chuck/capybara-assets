#!/usr/bin/env python3
# V631 (Martin 11.11. 15:54): Bei der Sprechblasen-Karte des Generals (#coach – Hinweise und Kurs-Schritte, mit Zipfel zum General)
# wird die Musik NICHT mehr ausgeblendet. Ausblenden nur bei ganzseitigen bzw. bildschirmbreiten Tipp-Karten (СОВЕТ, Coach-Tipps, Coach-Werbung) und Pause.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V630";', 'const GAME_VER = "V631";')
rep('!S.mapShow && !S.tiltCard && !window.__tutSumOpen && !window.__certFade);',
    '!S.mapShow && !S.tiltCard && !window.__tutSumOpen && !window.__certFade && !genBubbleOnly());')
rep('function frozen() {', '''function genBubbleOnly() { try { if (!S.coachHold || S.paused) return false; const c = document.getElementById("coach"); if (!c || c.hidden) return false;   /* V631: General-Sprechblase hält das Spiel, Musik läuft weiter */
    if (window.__tipBulb && window.__tipBulb.open) return false; for (const id of ["ovHkTips", "ovCoachAd"]) { const o = document.getElementById(id); if (o && !o.hidden) return false; } return true; } catch (e) { return false; } }
function frozen() {''')
open(p, "w", encoding="utf-8").write(s)
print("ok V631")
