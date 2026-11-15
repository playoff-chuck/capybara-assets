import sys
# V721: Game-over-Friedhof deckt den ganzen Bildschirm (vorher endete das Bild über dem Bedienfeld).
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V720";', 'const GAME_VER = "V721";')
rep('#ovOver.deadOv{background:linear-gradient(180deg,rgba(0,0,0,.72) 0%,rgba(0,0,0,.45) 45%,rgba(0,0,0,.08) 72%,rgba(0,0,0,0) 100%),url(img/over_grave.webp) center bottom/cover no-repeat,#000!important}',
    '#ovOver.deadOv{background:#000!important}#ovOver.deadOv::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;background:linear-gradient(180deg,rgba(0,0,0,.7) 0%,rgba(0,0,0,.42) 45%,rgba(0,0,0,.06) 75%,rgba(0,0,0,0) 100%),url(img/over_grave.webp) center bottom/cover no-repeat,#000}')
open(dst, "w", encoding="utf-8").write(s)
