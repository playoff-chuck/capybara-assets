"""V225: Weltkarte nachgebessert: Stecknadeln auf die gemalten Orte gesetzt (Tempel, Pyramide, Eispalast, Wälder,
Seen, Canyon), Antarktis zoomt nah auf den aktuellen Ort (statt ganze Breite), Musik läuft während der Kartenszenen
weiter, das Pausemenü taucht dabei nicht mehr versteckt im Hintergrund auf."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V224";', 'const GAME_VER = "V225";')
rep('[[.262, .705], [.236, .615], [.252, .505], [.288, .468], [.282, .640], [.314, .556]]', '[[.270, .677], [.235, .612], [.243, .501], [.287, .462], [.275, .560], [.314, .551]]')
rep('[[.452, .415], [.514, .522], [.574, .522], [.468, .338], [.583, .348], [.538, .362]]', '[[.451, .414], [.541, .573], [.509, .492], [.469, .341], [.581, .391], [.538, .354]]')
rep('[[.585, .168], [.678, .245], [.738, .305], [.700, .150], [.872, .192], [.826, .132]]', '[[.585, .167], [.677, .245], [.738, .305], [.699, .150], [.871, .191], [.825, .124]]')
rep('[[.137, .305], [.126, .176], [.186, .296], [.209, .228], [.282, .262], [.248, .165]]', '[[.137, .305], [.126, .173], [.186, .294], [.209, .228], [.282, .260], [.247, .163]]')
# Antarktis: nah am aktuellen Ort
rep('    function contCam(c) { const P = MAP_PTS[c],', '''    function contCam(c) { if (c === 4) { const g = posOf(curWave()).g, i = Math.max(0, Math.min(5, g - 24)), P4 = MAP_PTS[4], nx = P4[Math.min(5, i + 1)][0], x = (P4[i][0] + nx) / 2;
        return { x, y: .90, k: Math.max(2, Math.min(3.2, vp.clientWidth / (.30 * BW))), free: 1 }; }
      const P = MAP_PTS[c],''')
rep('if (mh >= H) ty = Math.min(0, Math.max(H - mh, ty)); else ty = (H - mh) / 2;', 'if (cam.free) ty = H * .80 - mh; else if (mh >= H) ty = Math.min(0, Math.max(H - mh, ty)); else ty = (H - mh) / 2;')
# Musik weiter, Pausemenü nicht dahinter
rep('if (play) { busy = true; const was = S.paused; S.paused = true;\n            play(() => { S.paused = was; busy = false;',
    'if (play) { busy = true; const was = S.paused; S.paused = true; S.mapShow = true;\n            play(() => { S.paused = was; S.mapShow = false; busy = false;')
rep('SFX.music.setPaused(SFX.music.playing !== 0 && !!frozen() && !S.drop && !S.alert && !S.mix && !S.duel);',
    'SFX.music.setPaused(SFX.music.playing !== 0 && !!frozen() && !S.drop && !S.alert && !S.mix && !S.duel && !S.mapShow);')
rep('want = !!(S.paused && S.started && !S.over && $("ovStart").hidden', 'want = !!(S.paused && !S.mapShow && S.started && !S.over && $("ovStart").hidden')
css = """<style id="v225">
/* Stecknadeln und Held in Bildschirm-Pixeln (eine Gegenskalierung am Anker) */
#ovMap .mPin,#ovMap .mapMe{transform:scale(var(--ik,1));transform-origin:0 0}
#ovMap .mPin i,#ovMap .mPin em,#ovMap .mapMe img{transform:none!important}
#ovMap .mPin em{transform:translate(-50%,-100%)!important}
#ovMap .mapMe img{left:-23px;top:-60px;transform-origin:50% 100%}
#ovMap .mapMe.hop img{animation:mHop2 .3s ease-in-out infinite alternate}
@keyframes mHop2{to{transform:rotate(8deg) translateY(-4px)}}
#ovMap.auto .mPin.cur em{top:-70px}
</style>
"""
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
