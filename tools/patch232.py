"""V232: Wellennummer endgültig unter allen Sprechblasen. Ursache: Es gibt kein #app (nur .app), der Umzug aus V223
lief ins Leere; #waveNum lag im body (z 43) über der ganzen .app-Ebene (z 1) mit Meldungen, Buchhalter, Hack-Pille,
Ticker, DJ-Box. Jetzt wohnt #waveNum in der Kopfzeile von .app (z 44 dort) – damit liegen Buchhalter, Meldungen,
Ticker, Hack-Pille, DJ-Box, Coach/General, Rosie/Blue und alle Fenster darüber. Wird alle 300 ms geprüft."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V231";', 'const GAME_VER = "V232";')
js = '''
  /* V232: Wellennummer in die Kopfzeile der .app-Ebene (niedrigste Priorität) */
  try { const home = () => document.querySelector(".app > header") || document.querySelector("header");
    const fix = () => { const wn = document.getElementById("waveNum"), h = home(); if (wn && h && wn.parentElement !== h) h.appendChild(wn); };
    fix(); setInterval(fix, 300); } catch (e) {}
'''
i = s.rfind('})();\\n</script>'.replace('\\\\n', '\\n')); i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
css = '''<style id="v232">
#waveNum{z-index:44!important}
.lockPill,#lockPill,.radioBand,#radioBand,#ovFb{z-index:50!important}
body.ovUp #waveNum,body:has(#ovHack:not([hidden])) #waveNum{visibility:hidden!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
