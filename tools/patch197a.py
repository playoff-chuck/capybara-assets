"""V197: Abstände über/unter dem Shop-Banner halbiert, Banner feste 86 px, Text nicht mehr unter dem Preis."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('const GAME_VER = "V196";') == 1
s = s.replace('const GAME_VER = "V196";', 'const GAME_VER = "V197";')
css = '''<style id="v197a">
#sheet .ledgerTop{min-height:0!important;height:auto!important;margin-bottom:8px!important;padding-bottom:0!important}
#sheet .ledgerTop .ledgerBig{display:none!important}
#sheetIn.shopV .shopGrid{padding-top:0!important}
#sheet .coachAd{margin:0!important}
#sheet .coachAd .ad.ad3{height:86px!important;min-height:0!important;max-height:86px!important;padding:0!important}
#sheet .coachAd + .shopCat{margin-top:0!important}
.coachAd .ad.ad3 .txt{right:100px!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
