"""V217: Neues Logo (Turm aus Fallsteinen) oben links auf dem Startscreen, feste Größe und Position;
7× Tippen darauf schaltet den Dev-Modus. Im Spiel bleibt das kleine Logo."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('const GAME_VER = "V216";') == 1
s = s.replace('const GAME_VER = "V216";', 'const GAME_VER = "V217";')
js = '''
  /* V217: Startscreen-Logo */
  try { const st = document.getElementById("ovStart"); if (st && !document.getElementById("stLogo")) { const im = document.createElement("img"); im.id = "stLogo"; im.alt = "Capybara Squad"; im.src = "img/logo_main.webp"; im.width = 124; im.height = 126;
      im.addEventListener("pointerdown", e => { e.stopPropagation(); const lg = document.querySelector(".logo"); if (lg) lg.dispatchEvent(new PointerEvent("pointerdown", { bubbles: false })); }); st.appendChild(im); } } catch (e) {}
'''
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
pre = '<link rel="preload" as="image" href="img/logo_main.webp">'
k = s.find('<title>'); s = s[:k] + pre + s[k:]
css = '''<style id="v217">
#stLogo{position:fixed!important;left:50%!important;margin-left:-62px!important;top:calc(env(safe-area-inset-top,0px) + 0px)!important;width:124px!important;height:126px!important;object-fit:contain;z-index:80!important;filter:drop-shadow(0 3px 4px rgba(0,0,0,.35));cursor:pointer;-webkit-tap-highlight-color:transparent;user-select:none}
#ovStart[hidden] #stLogo,#ovStart:not(.artReady) #stLogo{display:none!important}
body:has(#ovStart:not([hidden])) header .brand .logoFull,body:has(#ovStart:not([hidden])) header .brand{visibility:hidden!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
