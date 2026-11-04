"""V194: Shop-Banner – alte V182/V190-Regeln (Stern, Drehen, Blinken) greifen nicht mehr ins neue Banner."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('const GAME_VER = "V193";') == 1
s = s.replace('const GAME_VER = "V193";', 'const GAME_VER = "V194";')
css = '''<style id="v194a">
/* V194: neues Banner gegen alte Varianten-Regeln absichern */
.coachAd .ad.ad3 .p{width:auto!important;height:auto!important;margin:0!important;clip-path:none!important;animation:none!important;transform:translateY(-50%)!important;border-radius:12px!important;background:linear-gradient(#ffe57a,#f2b51e)!important;color:#3a2414!important;border:2px solid #3a2414!important;display:block!important;font-family:inherit}
.coachAd .ad.ad3 .p b{font-size:24px!important;-webkit-text-stroke:0!important;color:#3a2414!important}
.coachAd .ad.ad3 .p i{font-size:10px!important;color:#3a2414!important}
.coachAd .ad.ad3 .k{background:none!important;border:0!important;padding:0!important;animation:none!important;color:#ffd75e!important;letter-spacing:.12em!important;font-size:10px!important}
.coachAd .ad.ad3 .h{font-size:clamp(19px,5.6vw,24px)!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.coachAd .ad.ad3 .s{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
