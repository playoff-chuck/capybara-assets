import sys
# V715: Ergebnis-Screen dichter – passt ohne Scrollen (Martin 14.11.2026 23:12). Punktzahl und Teilen in einer Zeile,
#  kleinere Blue-Karte, Knöpfe «Neu starten» und «Hauptmenü» nebeneinander, Bestenliste kompakter, Blue-Figur unten aus.
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V714";', 'const GAME_VER = "V715";')
CSS = """<style id="v715dense">
#ovOver:not([hidden]){padding-top:calc(env(safe-area-inset-top,0px) + 6px)!important;padding-bottom:8px!important;gap:6px!important;justify-content:flex-start!important}
body:has(#ovOver:not([hidden])) #buddy{display:none!important}
#ovOver .aar{gap:3px!important;padding:8px 12px!important}
#ovOver .aarHead{margin:0!important}
#ovOver .finImg{display:none!important}
#ovOver #overTitle{font-size:clamp(26px,8vw,34px)!important;line-height:1!important;margin:0!important}
#ovOver .comfort{margin:3px 0!important;padding:3px 8px 3px 3px!important;gap:8px!important;width:100%;box-sizing:border-box}
#ovOver .comfort img{width:40px!important;height:40px!important}
#ovOver .comfort small{font-size:10px!important}
#ovOver .comfort b{font-size:15px!important;line-height:1.1!important}
#ovOver .hsScore{display:grid!important;grid-template-columns:auto auto;grid-template-rows:auto auto;column-gap:14px;row-gap:0;align-items:center;justify-content:center;margin:2px 0!important}
#ovOver .hsScore span{grid-column:1;grid-row:1;font-size:clamp(30px,9vw,40px)!important;text-align:center}
#ovOver .hsScore small{grid-column:1;grid-row:2;text-align:center;margin:0!important}
#ovOver .hsScore .shareBtn{grid-column:2;grid-row:1/3;margin:0!important;min-height:0!important;padding:7px 14px!important;font-size:16px!important}
#ovOver .aarStats{margin-top:2px!important;padding-top:4px!important}
#ovOver .aarStats b{font-size:17px!important}
#ovOver #btnOMap{min-height:0!important;padding:6px 10px!important;margin-top:4px!important}
#ovOver #hsOver{margin-top:0!important;padding:6px 12px 6px!important}
#ovOver #hsOver h4{font-size:15px!important;margin:2px 0!important}
#ovOver #hsOver h4:first-child{padding-bottom:3px!important;margin-bottom:2px!important;font-size:11px!important}
#ovOver #hsOver .row{padding:1px 4px!important;font-size:13px}
#ovOver .overBtns{grid-template-columns:1.45fr 1fr!important;gap:6px!important;margin:0!important}
#ovOver .overBtns>#btnCp{grid-column:1/-1}
#ovOver .overBtns>button:not(#btnCp){height:40px!important;font-size:13.5px!important;letter-spacing:0!important;padding:0 6px!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#ovOver .overBtns>button:not(#btnCp):only-of-type,#ovOver .overBtns>button[hidden]~button:last-child{grid-column:auto}
@media (max-height:700px){#ovOver .aarHead .aarTag{display:none!important}#ovOver .comfort img{width:34px!important;height:34px!important}#ovOver .comfort b{font-size:14px!important}#ovOver #hsOver h4:first-child{display:none!important}#ovOver .aarStats span{font-size:9px!important}}
</style>
</head>"""
rep('</head>', CSS)
open(dst, "w", encoding="utf-8").write(s)
print("ok")
