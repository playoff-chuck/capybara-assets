"""V223: Medaillen-Album: Skills zuerst, dann Kontinente/Orte, Nuts ganz unten. Ein einziges Logo (MAIN_LOGO) für
Startbildschirm, Kopfzeile, Guide und Hall of Fame. Tutorial-Sprechblasen, Rosie/Blue, Meldungen und Hack-Pille über der Wellennummer (Wellennummer zieht in #app)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V222";', 'const GAME_VER = "V223";')
# Album-Reihenfolge
a = s.index('  html += `<div class="albSec">CONTINENTS'); b = s.index('  const sk = []; ALB_SK.forEach', a); e = s.index('\n', s.index('html += `<div class="albSec">SKILLS', b)) + 1
s = s[:a] + s[b:e] + s[a:b] + s[e:]
# ein Logo überall
rep('const LOGO_IMG = {"blue": "img/e4708ab1d1.webp", "rosie": "img/17f8029dc0.webp"}', 'const MAIN_LOGO = "img/logo_main.webp?v=218"; const LOGO_IMG = {"blue": MAIN_LOGO, "rosie": MAIN_LOGO}')
rep('im.src = "img/logo_main.webp?v=218"; im.width = 124;', 'im.src = MAIN_LOGO; im.width = 124;')
js = """
  /* V223: Sprechblasen aus #app (z-index 1) herausheben, damit sie über der Wellennummer liegen */
  try { for (const id of ["coach", "buddy"]) { const el = document.getElementById(id); if (el && el.parentElement !== document.body) document.body.appendChild(el); }
    const app = document.getElementById("app"), wn = document.getElementById("waveNum"); if (app && wn && wn.parentElement !== app) app.appendChild(wn); } catch (e) {}   // Wellennummer in dieselbe Ebene wie Meldungen/Hack-Pille
"""
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
css = '''<style id="v223">
/* Sprechblasen (Tutorial, General, Rosie/Blue) immer über der Wellennummer */
.coach,#coach{z-index:905!important}
#coach .coachCard{z-index:905!important}
#buddy{z-index:905!important}
header .brand .logoFull{height:54px!important;width:auto!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
