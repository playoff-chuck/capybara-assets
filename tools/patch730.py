import sys
# V730 (Martin 18.11.2026, Foto Siegbildschirm RU): «Endbild design mit Nano Banana, aufräumen».
# Siegbildschirm (#ovOver.won) wie der Tod-Bildschirm V724 aufgebaut: Vollbild-Hintergrund img/over_won.webp
# (Nano Banana Pro: Blue + Rosie auf dem Globus, Feuerwerk), dunkle halb durchsichtige Kästen, goldener Titel.
# Weg: RESULTS-Etikett, Blase von Blue, kleiner SHARE-Knopf neben der Punktzahl (Einladen bleibt unten als großer Knopf),
# Bestenliste (#hsOver, oft «noch keine Einträge»). Punktzahl passt jetzt immer in die Breite; Ordensnamen zweizeilig.
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V729";', 'const GAME_VER = "V730";')
CSS = '''<style id="v730css">
#ovOver.won{background:#0b0d2a!important;justify-content:flex-start!important}
#ovOver.won::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;background:linear-gradient(180deg,rgba(6,8,28,.35) 0%,rgba(6,8,28,.2) 55%,rgba(6,8,28,0) 72%),url(img/over_won.webp) center bottom/cover no-repeat,#0b0d2a}
#ovOver.won .aarTag,#ovOver.won .comfort,#ovOver.won #btnShare,#ovOver.won #hsOver,#ovOver.won .finImg{display:none!important}
#ovOver.won .aar,#ovOver.won .hsEntry,#ovOver.won .campLine:not(:empty){background:rgba(10,12,40,.58)!important;-webkit-backdrop-filter:blur(5px);backdrop-filter:blur(5px);border:1.5px solid rgba(255,214,110,.4)!important;box-shadow:0 12px 36px rgba(0,0,0,.5)!important;color:#fff!important}
#ovOver.won .aar *,#ovOver.won .hsEntry *,#ovOver.won .campLine *{-webkit-text-stroke:0!important;text-shadow:none}
#ovOver.won .aarHead{justify-content:center!important}
#ovOver.won .aarMode{color:#ffd98a!important;letter-spacing:.08em}
#ovOver.won #overTitle{color:#ffd34d!important;font-size:clamp(30px,10vw,44px)!important;line-height:.98!important;letter-spacing:.02em;text-shadow:0 0 18px rgba(255,200,60,.55),0 2px 0 #3a1d00!important;margin:2px 0 6px!important;text-align:center}
#ovOver.won .hsScore{flex-direction:column!important;align-items:center!important;justify-content:center!important;min-height:0!important;margin:0!important;gap:0!important}
#ovOver.won #overScore{display:block;max-width:100%;white-space:nowrap;font-size:clamp(30px,11vw,48px)!important;line-height:1!important;color:#ffb43a!important;text-shadow:0 0 14px rgba(255,150,40,.45)!important}
#ovOver.won .hsScore>small{color:rgba(255,255,255,.7)!important}
#ovOver.won .aarStats{border-color:rgba(255,255,255,.16)!important;background:transparent!important}
#ovOver.won .aarStats b{color:#fff!important}#ovOver.won .aarStats span{color:rgba(255,255,255,.62)!important}
#ovOver.won #finMedals{background:rgba(255,255,255,.07)!important;border:1.5px solid rgba(255,214,110,.35)!important;box-shadow:none!important}
#ovOver.won #finMedals small{color:#ffd98a!important}
#ovOver.won #finMedals .fm b{color:#fff!important;white-space:normal!important;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;text-align:center;line-height:1.15}
#ovOver.won #btnOMap{background:rgba(255,255,255,.08)!important;border:1.5px solid rgba(255,255,255,.32)!important;box-shadow:none!important;color:#fff!important}
#ovOver.won #btnOMap *{color:#fff!important}
#ovOver.won .overBtns button{box-shadow:none!important;-webkit-text-stroke:0!important;text-shadow:none!important}
#ovOver.won #btnModes{background:rgba(10,12,40,.55)!important;border:1.5px solid rgba(255,255,255,.4)!important;color:#fff!important}
#ovOver.won #btnRestart{background:linear-gradient(180deg,#ffcf4a,#ff9a1f)!important;border:1.5px solid #ffe7a0!important;color:#3a1d00!important}
#ovOver.won input{background:rgba(255,255,255,.1)!important;color:#fff!important;border-color:rgba(255,255,255,.3)!important}
#ovOver.won label{color:rgba(255,255,255,.75)!important}
</style>
<style id="v724css">'''
rep('<style id="v724css">', CSS)
open(dst, "w", encoding="utf-8").write(s)
print("ok V730")
