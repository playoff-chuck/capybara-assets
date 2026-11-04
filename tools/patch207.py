"""V207: Pausemenü – Karte nie breiter als der Bildschirm (rechts nichts abgeschnitten), sitzt höher,
liegt über den Steuerknöpfen; bei geöffnetem Sound wird das Spieltempo ausgeblendet."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('const GAME_VER = "V206";') == 1
s = s.replace('const GAME_VER = "V206";', 'const GAME_VER = "V207";')
css = '''<style id="v207">
#ovPause.pauseOv:not([hidden]){z-index:1000!important;align-items:flex-start!important;justify-content:flex-start!important;flex-direction:column!important;padding-top:calc(env(safe-area-inset-top,0px) + 76px)!important;overflow-y:auto!important}
#ovPause .pCard{align-self:center!important;box-sizing:border-box!important;width:min(340px,calc(100vw - 28px))!important;max-width:calc(100vw - 28px)!important;margin:0 auto!important}
#ovPause .pCard *{box-sizing:border-box}
#ovPause .pCard.sndOpen .pVol{width:100%!important;max-width:100%!important;overflow:hidden}
#ovPause .pVol .pvRow{display:grid!important;grid-template-columns:62px minmax(0,1fr) 42px!important;gap:8px!important;align-items:center}
#ovPause .pVol .pvRow input{width:100%!important;min-width:0!important}
#ovPause .pVol .pvRow b{text-align:right;font-size:12px!important}
#ovPause .pCard.sndOpen .pSpeed{display:none!important}
body:has(#ovPause:not([hidden])) .deck,body:has(#ovPause:not([hidden])) #pauseFab{visibility:hidden!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
