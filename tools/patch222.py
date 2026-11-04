"""V222: Betonmischer animiert – Räder drehen sich (Felgen mit Speichen + Profil), Trommel dreht (wandernde Streifen)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('const GAME_VER = "V221";') == 1
s = s.replace('const GAME_VER = "V221";', 'const GAME_VER = "V222";')
wheel = '<svg viewBox="0 0 100 100"><g fill="none" stroke="rgba(255,255,255,.28)" stroke-width="5" stroke-linecap="round">' + ''.join(f'<path d="M50 6v8" transform="rotate({a} 50 50)"/>' for a in range(0, 360, 30)) + '</g><circle cx="50" cy="50" r="17" fill="#8a8f86" stroke="#2a2018" stroke-width="4"/><g stroke="#2a2018" stroke-width="4" stroke-linecap="round">' + ''.join(f'<path d="M50 50v-14" transform="rotate({a} 50 50)"/>' for a in (0, 72, 144, 216, 288)) + '</g><circle cx="50" cy="50" r="5" fill="#2a2018"/></svg>'
js = '''
  /* V222: Mischer-Animation */
  try { const mx = document.getElementById("mixer"); if (mx && !mx.querySelector(".mxW")) { const W = '%s';
      mx.insertAdjacentHTML("beforeend", '<i class="mxDrum"></i><i class="mxW mxW1">' + W + '</i><i class="mxW mxW2">' + W + '</i>'); } } catch (e) {}
''' % wheel.replace("'", "\\'")
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
css = '''<style id="v222">
#mixer{position:fixed}
#mixer .mxW{position:absolute;width:28.5%;height:36.7%;top:60.5%;display:block;animation:mxSpin .55s linear infinite;pointer-events:none}
#mixer .mxW svg{width:100%!important;height:100%!important;display:block!important}
#mixer .mxW1{left:15.6%}
#mixer .mxW2{left:53.8%}
#mixer .mxDrum{position:absolute;inset:0;display:block;pointer-events:none;-webkit-mask:url(img/mixer_drummask.png) center/100% 100% no-repeat;mask:url(img/mixer_drummask.png) center/100% 100% no-repeat;
  background:repeating-linear-gradient(115deg,rgba(90,40,10,0) 0 14px,rgba(90,40,10,.28) 14px 22px,rgba(255,255,255,.22) 22px 26px,rgba(90,40,10,0) 26px 40px);background-size:80px 80px;animation:mxDrum .9s linear infinite;mix-blend-mode:multiply}
@keyframes mxSpin{to{transform:rotate(360deg)}}
@keyframes mxDrum{to{background-position:80px 0}}
@media (prefers-reduced-motion:reduce){#mixer .mxW,#mixer .mxDrum{animation:none}}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
