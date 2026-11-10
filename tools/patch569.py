#!/usr/bin/env python3
# V569 (Martin 10.11. 23:05): Ergebnis-Fenster (Game over) aufgeräumt: «RESULTS»-Plakette mittig und sauber,
# Modus darunter, Punktzahl groß und zentriert (lief links aus dem Bild), TEILEN darunter (lief rechts raus).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V568";', 'const GAME_VER = "V569";')
CSS = '''<style id="v569over">
#ovOver .aar{overflow:hidden!important;padding:14px 14px 12px!important;text-align:center}
#ovOver .aarHead{flex-direction:column!important;align-items:center!important;justify-content:center!important;gap:6px!important;margin:0 0 4px!important}
#ovOver .aarTag{display:inline-flex!important;align-items:center;justify-content:center;height:24px!important;padding:0 14px!important;line-height:1!important;font-size:11px!important;letter-spacing:.18em!important;box-shadow:0 2px 0 rgba(58,36,20,.35)}
#ovOver .aarMode{display:block;max-width:100%;font-size:12px!important;line-height:1.25!important;letter-spacing:.1em!important;text-align:center}
#ovOver .aar h2{margin:2px 0 8px!important;line-height:1!important}
#ovOver .hsScore{flex-direction:column!important;align-items:center!important;gap:2px!important;margin:6px 0 4px!important}
#ovOver .hsScore span{font-size:clamp(40px,14vw,58px)!important;line-height:.95!important;max-width:100%}
#ovOver .hsScore small{font-size:11px!important;letter-spacing:.2em!important;margin:0 0 6px}
#ovOver .hsScore .shareBtn{margin:0!important;height:34px!important;padding:0 20px!important;font-size:17px!important}
#ovOver .aarStats{margin-top:8px!important}
#ovOver .aarStats>div{min-width:0}
#ovOver .aarStats span{font-size:10px!important;letter-spacing:.1em!important;white-space:nowrap}
#ovOver .hsEntry label{font-size:10px!important;letter-spacing:.1em!important;line-height:1.35!important}
</style>
'''
rep("</body>", CSS + "</body>")
open(dst, "w", encoding="utf-8").write(s)
print("ok")
