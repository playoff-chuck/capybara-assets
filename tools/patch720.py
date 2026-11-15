import sys
# V720 (Martin 15.11.2026 20:02–20:05):
#  0) Ergebnis-Bildschirm: Knöpfe 3 s gesperrt (blass), erst dann per Knopf weiter – kein versehentliches Weitertippen.
#  3) Karte: «☠ Nuts 97 %» → «☠ Nuts 58 / 120 levels done» (klar: geschafft / gesamt).
#  1) Game-over-Bildschirm beim Tod dramatisch: schwarzer Hintergrund mit Friedhof bei Nacht, Zombies, ein Zombie-Capybara
#     (Nano Banana Pro, img/over_grave.webp, 0,14 $). Nicht beim Sieg (S.won). Titel rot. Bild wird vorab geladen.
#  2) Wischsteuerung: «nach oben wischen = fallen lassen» löst nicht mehr so leicht aus (Lena verlor 2× bei W91/92 kurz nach
#     Einführung der Gesten, 1 Linie in der ganzen Runde – Verdacht auf versehentliches Fallenlassen). Jetzt nötig: mind. 2,5 Felder
#     (≥ 60 px) nach oben, klar senkrecht (2× mehr als seitlich), schneller Wisch (< 450 ms).
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V719";', 'const GAME_VER = "V720";')
rep('<!doctype html><html><head>', '<!doctype html><html><head><style>html{background:#df7973}</style>')   # V720: kein weißer Blitz beim App-Start (Martin 20:10) – Hintergrund ab dem ersten Byte im Startbild-Ton
rep('if (ty < -Math.max(40, st.ch * 1.5) && Math.abs(ty) > Math.abs(tx) * 1.2 && dt < 600) { hardDrop(); return; }',
    'if (ty < -Math.max(60, st.ch * 2.5) && Math.abs(ty) > Math.abs(tx) * 2 && dt < 450) { hardDrop(); return; }   /* V720: strenger */')
rep('<style id="v719css">', '''<style id="v720css">
#ovOver.deadOv{background:linear-gradient(180deg,rgba(0,0,0,.72) 0%,rgba(0,0,0,.45) 45%,rgba(0,0,0,.08) 72%,rgba(0,0,0,0) 100%),url(img/over_grave.webp) center bottom/cover no-repeat,#000!important}
#ovOver .overBtns,#ovOver .hsScore,#ovOver .campLine{position:relative}
#ovOver .overBtns::after,#ovOver .hsScore::after,#ovOver .campLine::after{content:"";position:absolute;inset:-6px;z-index:5;animation:ovGate 3s step-end forwards}
#ovOver .overBtns button,#ovOver #btnShare,#ovOver .campLine button{animation:ovFade 3s ease-in forwards}
@keyframes ovGate{0%{visibility:visible}100%{visibility:hidden}}
@keyframes ovFade{0%,85%{opacity:.35}100%{opacity:1}}
#ovOver.deadOv #overTitle{color:#d8322a!important;text-shadow:0 2px 0 rgba(0,0,0,.25)}
#ovOver.deadOv .aar,#ovOver.deadOv .hs,#ovOver.deadOv .hsEntry,#ovOver.deadOv .campLine{box-shadow:0 14px 40px rgba(0,0,0,.6),0 0 0 1px rgba(120,255,140,.08)}
</style>
<script id="v720js">(() => { try {
  const ov = document.getElementById("ovOver"); if (!ov) return;
  const set = () => { try { const S = window.__TT && window.__TT.S; ov.classList.toggle("deadOv", !ov.hidden && !!(S && S.over && !S.won && !S.replay)); } catch (e) {} };   /* Sperre 3 s: per CSS-Animation (startet bei jedem Öffnen neu) */
  new MutationObserver(set).observe(ov, { attributes: true, attributeFilter: ["hidden"] });
  setTimeout(() => { try { const i = new Image(); i.src = "img/over_grave.webp"; } catch (e) {} }, 8000);   /* vorab laden */
} catch (e) {} })();</script>
<style id="v719css">''')
rep('<div class="rsNuts">☠ Nuts ${nzf} %</div>', '<div class="rsNuts">☠ Nuts ${nzb.reduce((a, b) => a + b, 0)} / ${4 * NZ_MAX} levels done</div>')   # V720: statt unklarer «97 %» (Martin 20:05)
open(dst, "w", encoding="utf-8").write(s)
import subprocess, os
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang720.py"), os.path.join(os.path.dirname(os.path.abspath(dst)), "lang")], check=True)
