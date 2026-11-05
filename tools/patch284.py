"""V284 (Martin 17:04): Ort geschafft – Strahlen und Sterne springen nicht mehr. Titel, Sterne und Strahlen blenden weich ein
(kein Überschwingen, kein Pulsieren), am Ende blenden alle in 0,7 s aus und die Karte blendet weich zurück."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V283";', 'const GAME_VER = "V284";')
css = r'''
<style id="v284cel">
#ovMap .mapCel{transition:opacity .6s ease!important}
#ovMap .mapCel.out{opacity:0!important;transition:opacity .7s ease!important}
#ovMap .celRays{opacity:0;transition:opacity .9s ease}
#ovMap .mapCel.on .celRays{opacity:1}
#ovMap .celTxt{transform:scale(.97);opacity:0}
#ovMap .mapCel.on .celTxt{animation:celFade .8s ease-out forwards!important}
@keyframes celFade{to{transform:scale(1);opacity:1}}
#ovMap .celTxt em{animation:none!important;opacity:0;transition:opacity .8s ease .5s}
#ovMap .mapCel.on .celTxt em{opacity:1}
#ovMap .mapVp,#ovMap .mapTop,#ovMap .mapSkip{transition:opacity .7s ease}
@media (prefers-reduced-motion:reduce){#ovMap .celRays{animation:none!important}}
</style>
'''
i = s.rindex('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
s = open(dst, encoding='utf-8').read()
# Martin 17:05: Angebote (Werbung, Lucky Supply, Boss-Hack, Rufzeichen) nur am laufenden Spielscreen – nie im Shop, Turm-Menü,
# Boss-Hack, Pause oder einem anderen Menü/Fenster. Gilt auch für die Boss-Hack-Ausnahme.
rep('window.__offerOK = (force) => force ?',
    '''window.__playScreen = () => { try { const v = id => { const e = document.getElementById(id); return e && !e.hidden && getComputedStyle(e).display !== "none"; };
    return !!(S && S.started && !S.over && !S.paused && !S.shop && !S.sel && !S.mode && !S.duel && !S.intro && !S.mapShow && !S.ordersOpen && !S.joinOpen && !S.banditOpen && !S.signOpen && !S.hackAdOpen
      && !v("sheet") && !v("ovStart") && !v("ovPause") && !uiWinOpen() && !document.body.classList.contains("mapUp") && !(typeof TUT !== "undefined" && TUT.on) && !document.hidden); } catch (e) { return false; } };
window.__offerOK = (force) => !window.__playScreen() ? false : force ?''')
open(dst, 'w', encoding='utf-8').write(s)
s = open(dst, encoding='utf-8').read()
# Martin 17:06: General-Statistik 10 s stehen lassen, nur die Statistik selbst (keine Kleinschrift darunter)
rep('try { const st = window.__genStat && window.__genStat(); if (st) say = st; } catch (e) {}',
    'try { const st = window.__genStat && window.__genStat(); if (st) { msgPush({ kind: "alert", title: st.toUpperCase(), sub: "", tag: "HQ", hold: 10000, low: true }); return; } } catch (e) {}')
i = s.rindex('</body>'); s = s[:i] + '<style id="v284sub">#alSub:empty{display:none!important}</style>\n' + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
