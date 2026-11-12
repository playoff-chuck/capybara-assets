#!/usr/bin/env python3
# V662 (Martin 12.11. 14:10): Grafikmodus lustig und transparent über den General oben links.
#  - FULL: General in Parade-Uniform (eigenes Bild GEN_FULL; bis das Bild da ist = normales Bild)
#  - automatisch auf LITE: er wechselt ins normale Outfit und sagt es in der Sprechblase
#  - im LITE-Modus ist der General antippbar: Tipp → zurück auf FULL (automatische Messung läuft wieder)
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V661";', 'const GAME_VER = "V662";')
rep('const GEN_HEAD = "img/a9bbf4192f.webp";',
    '''const GEN_LITE = "img/a9bbf4192f.webp", GEN_FULL = GEN_FULL_IMG || GEN_LITE; let GEN_HEAD = (typeof fxOn === "function" && !fxOn()) ? GEN_LITE : GEN_FULL;   /* V662: Parade-Uniform = volle Grafik */''')
# Bild-Platzhalter (wird gesetzt, sobald das Parade-Bild da ist)
rep('const PORTRAIT = { general: "img/db5ec9685a.webp",', 'const GEN_FULL_IMG = "";   /* V662: Parade-Uniform des Generals */ const PORTRAIT = { general: "img/db5ec9685a.webp",')
# Sprechblase beim automatischen Umschalten
rep('try { toast("LITE GRAPHICS · smoother play on this phone", "HQ", 2400); } catch (e) {} }',
    'try { genHeadSync(); toast("PARADE\'S OVER! · Lite graphics for smoother play – tap me for full graphics", "HQ", 4200); } catch (e) {} }   /* V662 */')
# Hilfsfunktion + Antippen
rep('const FXM = { t0: 0, n: 0, sum: 0 };   /* V494: Bildrate im Spiel messen */',
    '''const FXM = { t0: 0, n: 0, sum: 0 };   /* V494: Bildrate im Spiel messen */
function genHeadSync() { try { const want = fxOn() ? GEN_FULL : GEN_LITE; if (GEN_HEAD === want) return; const old = GEN_HEAD; GEN_HEAD = want; const g = document.getElementById("genAv"); if (g && g.getAttribute("src") === old) g.src = want; } catch (e) {} }   /* V662 */
function genGoFull() { if (fxOn()) return; try { localStorage.removeItem("capy-fx"); } catch (e) {} FXM.n = 0; FXM.sum = 0; FXM.t0 = 0; fxLabel(); liteApply(); genHeadSync();
  try { window.__evLog && window.__evLog.push("perf", { d: { lite: 0, why: "general" } }); } catch (e) {} try { snd("uiTap"); } catch (e) {}
  try { const g = document.getElementById("genAv"); if (g) { g.classList.remove("talk"); void g.offsetWidth; g.classList.add("talk"); } } catch (e) {}
  try { toast("DRESS UNIFORM ON! · Full graphics are back – medals polished", "HQ", 3600); } catch (e) {} }   /* V662: Tipp auf den General */
document.addEventListener("click", e => { try { if (fxOn() || document.body.classList.contains("ovUp")) return; const g = document.getElementById("genAv"); if (!g || !g.getClientRects().length) return; const r = g.getBoundingClientRect();
  if (e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom) { e.stopPropagation(); e.preventDefault(); genGoFull(); } } catch (er) {} }, true);   /* Treffer über die Fläche des Generals (auch wenn ein Bild darüber liegt) */
setInterval(genHeadSync, 500);''')
rep('#genAv{display:none;position:fixed;', 'body.lite #genAv{pointer-events:auto!important;cursor:pointer}   #genAv{display:none;position:fixed;')
open(p, "w", encoding="utf-8").write(s); print("ok V662")
