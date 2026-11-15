import sys, os, subprocess
# V724 (Martin 15.11.2026 20:36, Screenshot mit Streichungen): Tod-Bildschirm dunkel und klar.
#  Oben groß «YOU DIED!»; weg: RESULTS-Kopf + Modus-Zeile, «Blue sagt»-Blase, Punktzahl, Bestenliste.
#  Alles dunkel, halb durchsichtig (Friedhof scheint durch), weiße Schrift. Nur beim Tod (#ovOver.deadOv).
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V723";', 'const GAME_VER = "V724";')
rep('const ow = $("overWhere"); if (ow) { const dead = S && !S.won && !S.nuts && !S.replay; ow.hidden = !dead; if (dead) {',
    'const ow = $("overWhere"); if (ow) { const dead = S && !S.won && !S.nuts && !S.replay; ow.hidden = !dead; if (dead) { $("overTitle").textContent = "YOU DIED!";   /* V724 */')
G = "#ovOver.deadOv"
CSS = f'''<style id="v724css">
{G} .aarHead,{G} .comfort,{G} #overScore,{G} .hsScore>small,{G} #hsOver{{display:none!important}}
{G} .aar,{G} .hsEntry,{G} .campLine:not(:empty){{background:rgba(8,10,14,.6)!important;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);border:1.5px solid rgba(255,255,255,.16)!important;box-shadow:0 12px 36px rgba(0,0,0,.55)!important;color:#fff!important}}
{G} .aar *,{G} .hsEntry *,{G} .campLine *{{color:#fff;-webkit-text-stroke:0!important;text-shadow:none}}
{G} #overTitle{{color:#ff3b30!important;font-size:46px!important;letter-spacing:.03em;text-shadow:0 0 18px rgba(255,40,30,.45),0 2px 0 #000!important;margin:2px 0 8px!important}}
{G} .aarStats{{border-color:rgba(255,255,255,.14)!important;background:transparent!important}}
{G} .aarStats b{{color:#fff!important}}{G} .aarStats span{{color:rgba(255,255,255,.62)!important}}
{G} .hsScore{{justify-content:center!important;min-height:0!important;margin:2px 0!important}}
{G} #overWhere .owBox{{box-shadow:none!important;border-width:1.5px!important}}
{G} #overWhere .owGot{{background:rgba(150,20,20,.36)!important;border-color:rgba(255,95,85,.65)!important}}
{G} #overWhere .owNext{{background:rgba(30,120,40,.36)!important;border-color:rgba(120,235,110,.6)!important}}
{G} #overWhere small,{G} #overWhere em{{color:rgba(255,255,255,.8)!important}}
{G} #overWhere .owGot b{{color:#ff6a5f!important}}{G} #overWhere .owNext b{{color:#7cf06e!important}}{G} #overWhere .owArrow{{color:#fff!important}}
{G} button,{G} .btn-accent{{background:rgba(255,255,255,.08)!important;border:1.5px solid rgba(255,255,255,.32)!important;color:#fff!important;box-shadow:none!important;-webkit-text-stroke:0!important;text-shadow:none!important}}
{G} #btnCp{{background:rgba(40,140,50,.55)!important;border-color:#7cf06e!important}}
{G} #btnShare{{background:rgba(255,95,162,.3)!important;border-color:rgba(255,95,162,.85)!important}}
{G} input{{background:rgba(255,255,255,.1)!important;color:#fff!important;border-color:rgba(255,255,255,.3)!important}}
{G} label{{color:rgba(255,255,255,.75)!important}}
</style>
<style id="v723css">'''
rep('<style id="v723css">', CSS)
open(dst, "w", encoding="utf-8").write(s)
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang724.py"), os.path.join(os.path.dirname(os.path.abspath(dst)), "lang")], check=True)
