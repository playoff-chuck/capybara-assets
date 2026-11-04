"""V196: Guide-Fenster am Handy fast bildschirmfüllend, Liste scrollt innen; Sperr-Schild «WAVE n» lesbar."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('const GAME_VER = "V195";') == 1
s = s.replace('const GAME_VER = "V195";', 'const GAME_VER = "V196";')
css = '''<style id="v196">
/* V196 Guide groß */
#ovInfo.overlay.win:not([hidden]){position:fixed!important;left:8px!important;right:8px!important;top:calc(env(safe-area-inset-top,0px) + 8px)!important;bottom:calc(env(safe-area-inset-bottom,0px) + 8px)!important;
  width:auto!important;max-width:640px!important;height:auto!important;max-height:none!important;margin:0 auto!important;transform:none!important;
  display:flex!important;flex-direction:column!important;padding:18px 14px 12px!important;gap:8px!important;z-index:90}
#ovInfo h2{margin:0!important;font-size:32px!important}
#ovInfo .reTut{margin:0 auto!important}
#ovInfo .tabs{flex:0 0 auto}
#ovInfo .tabPane:not([hidden]){flex:1 1 auto!important;min-height:0!important;max-height:none!important;height:auto!important;overflow-y:auto!important;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;padding-bottom:12px}
#ovInfo .mRow{font-size:15px}
#ovInfo .mRow span{font-size:14.5px!important;line-height:1.35!important}
#ovInfo .mRow b{font-size:22px!important}
/* gesperrt: hell und lesbar */
.mRow em.lock{background:#efe6d2!important;color:#5a4630!important;border:2px solid #c9b48f!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
