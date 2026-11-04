"""V213: Startscreen – Bild verschiebt sich nie mehr; großer Knopf (PLAY bzw. CONTINUE) immer an derselben Stelle,
«New world tour» klein darunter. Die Knöpfe liegen über dem Bildrahmen statt ihn zu verdrängen."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('const GAME_VER = "V212";') == 1
s = s.replace('const GAME_VER = "V212";', 'const GAME_VER = "V213";')
css = '''<style id="v213">
#startMain{position:relative!important}
#startMain .heroStart{flex:1 1 auto!important;height:100%!important;min-height:0!important}
#startMain .squad,#startMain #btnResume{position:absolute!important;left:50%!important;transform:translateX(-50%)!important;width:min(340px,calc(100% - 16px))!important;bottom:56px!important;margin:0!important;z-index:7!important}
#startMain .squad .modes{margin:0!important}
#startMain .squad .modes,#startMain .squad .modeBtn{margin:0!important;width:100%!important;max-width:none!important;box-sizing:border-box}
#startMain .squad .modeBtn{height:76px!important}
#ovStart:not(.artReady) #startMain{visibility:hidden!important}
#startMain #btnNewTour{position:absolute!important;left:50%!important;transform:translateX(-50%)!important;bottom:12px!important;margin:0!important;z-index:7!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
a = 'if (performance.now() - t0 > 1500) { ov.classList.add("artReady"); return; } setTimeout(chk, 30); };\n  chk(); setTimeout(() => ov.classList.add("artReady"), 2500); })();'
assert s.count(a) == 1, 'fallback'
s = s.replace(a, a.replace('> 1500', '> 4000').replace('2500)', '5000)'))
# Startbilder (Rahmen, Titelbild, Hintergrund) schon beim Laden der Seite holen – während «Tap to start»
pre = '<link rel="preload" as="image" href="img/d328f1a428.webp"><link rel="preload" as="image" href="img/b6f38631c6.webp"><link rel="preload" as="image" href="img/2510465d7d.webp">'
k = s.find('<title>'); assert k > 0
s = s[:k] + pre + s[k:]
pj = '<script>try{["img/d328f1a428.webp","img/b6f38631c6.webp","img/2510465d7d.webp","img/e24cf5d037.webp"].forEach(function(u){var i=new Image();i.src=u;if(i.decode)i.decode().catch(function(){});(window.__PRE0=window.__PRE0||[]).push(i);});}catch(e){}</script>'
s = s[:k] + pj + s[k:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
