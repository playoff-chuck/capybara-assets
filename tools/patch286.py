"""V286 (Martin 17:11): Nuts-Anzeige («☠ NUTS 1/30») verdeckte unten die Steine. Sie sitzt jetzt oben an der Stelle der rosa
Wellen-Nummer (die im Nuts-Umweg ohnehin nicht zählt), kompakt «☠ 1/30» mit kleinem +%-Wert darunter.
Martin 17:12: «Incoming …»-Sprachclip am Wellenstart 5× seltener (20 %)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V285";', 'const GAME_VER = "V286";')
rep('txt = `☠ NUTS ${Math.min(NZ_MAX, l)}/${NZ_MAX}` + (n.first ? `<small>+${n.cleared || 0} %</small>` : `<small>replay</small>`);',
    'txt = `☠ ${Math.min(NZ_MAX, l)}/${NZ_MAX}` + (n.first ? `<small>+${n.cleared || 0} %</small>` : `<small>replay</small>`);')
rep('  if (nzBadge._t !== txt) { nzBadge._t = txt; nzBadge.innerHTML = txt; }\n}',
    '''  if (nzBadge._t !== txt) { nzBadge._t = txt; nzBadge.innerHTML = txt; }
  try { const wn = document.getElementById("waveNum"), r = wn && wn.getBoundingClientRect(); if (r && r.width) { nzBadge.style.left = (r.left + r.width / 2) + "px"; nzBadge.style.top = (r.top + r.height / 2) + "px"; } } catch (e) {}
}''')
# Martin 17:12: «Incoming! Munchers!» usw. am Wellenstart 5× seltener (Sprachclip nur noch in jeder 5. Welle im Schnitt)
rep('if (!S.introNow) setTimeout(() => SFX.say(S.incomingKey || "Incoming!"), 1300);', 'if (!S.introNow && Math.random() < 0.2) setTimeout(() => SFX.say(S.incomingKey || "Incoming!"), 1300);')
css = r'''
<style id="v286nuts">
#nutsBadge{bottom:auto!important;top:40px;transform:translate(-50%,-50%)!important;z-index:45!important;display:flex;flex-direction:column;align-items:center;line-height:1;padding:3px 9px 2px!important;font-size:17px!important;opacity:1!important}
#nutsBadge[hidden]{display:none!important}
#nutsBadge small{margin:1px 0 0!important;font-size:10px!important}
body.inNuts #waveNum{visibility:hidden!important}
body.ovUp #nutsBadge,body.mapUp #nutsBadge{visibility:hidden}
</style>
'''
i = s.rindex('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
