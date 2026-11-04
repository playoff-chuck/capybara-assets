"""V210: Sprechblasen (General, Meldungen) immer ganz oben – nie unter Wellen-Nummer oder Anzeige;
Spielende ohne Tipp-Karte und ohne Scrollen (eigene Ebene über der Anzeige, kompakt)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('const GAME_VER = "V209";') == 1
s = s.replace('const GAME_VER = "V209";', 'const GAME_VER = "V210";')
js = '''
  try { window.__TT && (window.__TT.gameOver = w => gameOver(w)); } catch (e) {}
'''
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
css = '''<style id="v210">
/* Sprechblasen über allem im Spiel (unter Vollbild-Fenstern) */
#alert,#toast,#ticker,.ticker{z-index:900!important}
/* Spielende: kompakt, kein Scrollen, kein Tipp */
#ovOver .tipCard{display:none!important}
#ovOver:not([hidden]){position:fixed!important;inset:0!important;z-index:1000!important;margin:0!important;width:auto!important;height:auto!important;max-height:none!important;
  padding:calc(env(safe-area-inset-top,0px) + 10px) 12px calc(env(safe-area-inset-bottom,0px) + 10px)!important;overflow:hidden!important;display:flex!important;flex-direction:column!important;justify-content:center!important;gap:8px!important;
  background:rgba(20,28,16,.72)!important;backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);border:0!important;border-radius:0!important;transform:none!important}
#ovOver>*{width:min(400px,100%)!important;margin-left:auto!important;margin-right:auto!important;box-sizing:border-box}
#ovOver .aar{padding:10px 12px!important}
#ovOver .aar h2{font-size:30px!important;margin:2px 0!important}
#ovOver .hsScore span{font-size:44px!important}
#ovOver .aarStats{margin-top:4px!important}
#ovOver .aarStats b{font-size:22px!important}
#ovOver .hs{max-height:22vh!important;overflow-y:auto!important;margin:0!important}
#ovOver .campLine:empty{display:none!important}
#ovOver .hsEntry{padding:8px 10px!important}
#ovOver .overBtns{display:grid!important;grid-template-columns:1fr;gap:8px!important;margin:0!important}
#ovOver .overBtns>button{width:100%!important;margin:0!important;height:46px!important;min-height:0!important;font-size:17px!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
