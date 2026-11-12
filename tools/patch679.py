# V679: EIN ruhiges Startbild – kein dunkelgrüner Leerbildschirm vor dem Titelbild.
# Titelbild + sein CSS stehen jetzt ganz oben (erscheint, bevor die 2 MB Seite fertig gelesen ist),
# Hintergrund/Adressleiste im Titelbild-Ton, bis das Startbild weg ist; Bild wird vorgeladen.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
def cut(a, z):
    global s; i = s.index(a); j = s.index(z, i) + len(z); assert s.count(a) == 1, a[:40]; blk = s[i:j]; s = s[:i] + s[j:]; return blk
css = cut('/* V144 – Startbild beim Öffnen */', 'html:not(.fontsOk) #splash .spT,html:not(.fontsOk) #splash .spGo{visibility:hidden}   /* V675 */')
div = cut('<div id="splash" class="loading"', '<div class="spDots" aria-hidden="true"><i></i><i></i><i></i></div></div>')
css = css.replace('#splash{position:fixed;inset:0;z-index:200;background:#f4a07a;', '#splash{position:fixed;inset:0;z-index:200;background:linear-gradient(#df7973 0%,#e6a488 50%,#283624 100%);')
assert 'linear-gradient(#df7973' in css
HEAD = '<link rel="manifest" href="manifest.webmanifest?v=601"><meta name="theme-color" content="#2b3a22"></head><body>'
rep(HEAD, '<link rel="manifest" href="manifest.webmanifest?v=679"><meta name="theme-color" content="#df7973"><link rel="preload" as="image" href="img/b6f38631c6.webp">'
    '<style>/* V679 */html.boot,html.boot body{background:#df7973!important}\n' + css + '\n</style><script>document.documentElement.classList.add("boot")</script></head><body>\n' + div + '\n')
rep('sp.classList.add("out"); setTimeout(() => sp.remove(), 650); };',
    'sp.classList.add("out"); setTimeout(() => { sp.remove(); try { document.documentElement.classList.remove("boot"); const tc = document.querySelector(\'meta[name="theme-color"]\'); if (tc) tc.content = "#2b3a22"; } catch (e) {} }, 650); };   /* V679 */')
rep('const GAME_VER = "V678"', 'const GAME_VER = "V679"')
open(dst, "w", encoding="utf8").write(s)
# Manifest: Startfarbe der installierten App = Titelbild-Ton
import os, re
m = os.path.join(os.path.dirname(dst), "manifest.webmanifest")
t = open(m, encoding="utf8").read(); assert t.count('"background_color": "#2b3a22"') == 1
open(m, "w", encoding="utf8").write(t.replace('"background_color": "#2b3a22"', '"background_color": "#df7973"'))
print("ok", len(s))
