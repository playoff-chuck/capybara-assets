# V675: Startbild-Schrift erst zeigen, wenn Bangers geladen ist (kein Aufblitzen der Ersatzschrift); RU-Diplom: Symbole links weiter nach innen
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
A = '@media (prefers-reduced-motion: reduce){#splash .spT,#splash .spGo{animation:none}}'
rep(A, A + '\nhtml:not(.fontsOk) #splash .spT,html:not(.fontsOk) #splash .spGo{visibility:hidden}   /* V675 */')
rep('<div id="splash" class="loading"', '<script>(function(){var d=document.documentElement,ok=function(){d.classList.add("fontsOk")};try{if(!document.fonts||!document.fonts.load){ok();return;}setTimeout(ok,2500);Promise.all([document.fonts.load("64px Bangers","CAPYBARA SQUAD"),document.fonts.load("28px Bangers","НАЖМИ, ЧТОБЫ НАЧАТЬ")]).then(ok,ok);}catch(e){ok();}})();</script>\n<div id="splash" class="loading"')
A = '#tutSum .ctPaper li{padding:1.6cqw .5cqw;gap:2cqw}'
rep(A, A + '\n#tutSum .cert:not(.us) .ctPaper li{padding-left:3.5cqw}   /* V675: RU-Symbole weg vom Rahmen */')
rep('const GAME_VER = "V674"', 'const GAME_VER = "V675"')
open(dst, "w", encoding="utf8").write(s); print("ok")
