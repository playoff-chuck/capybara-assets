"""V202: Neuheiten-Fenster – kein altes Bild mehr beim Wechsel (neues Bild blendet erst nach dem Laden ein,
Fenster blendet weich auf), Wisch-Geräusch statt Funk-Knacken."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V201";', 'const GAME_VER = "V202";')
rep('w.querySelector("img").src = fs;',
    '{ const im = w.querySelector("img"); if (im.getAttribute("src") !== fs) { im.classList.add("ldg"); im.onload = im.onerror = () => im.classList.remove("ldg"); im.src = fs; if (im.complete && im.naturalWidth) im.classList.remove("ldg"); } }')
rep('snd("radio"); setTimeout(() => SFX.say(mon ? "newmonster" : "newgear"), 300);',
    'swoosh(); setTimeout(() => SFX.say(mon ? "newmonster" : "newgear"), 350);')
fn = '''function swoosh() { try { const ac = SFX._ac && SFX._ac(), out = SFX._out && SFX._out(); if (!ac || !out || SFX.muted) return;
  const d = 0.5, n = Math.floor(ac.sampleRate * d), buf = ac.createBuffer(1, n, ac.sampleRate), ch = buf.getChannelData(0); for (let i = 0; i < n; i++) ch[i] = Math.random() * 2 - 1;
  const src = ac.createBufferSource(); src.buffer = buf; const bp = ac.createBiquadFilter(); bp.type = "bandpass"; bp.Q.value = 1.4; const g = ac.createGain(); const t = ac.currentTime;
  bp.frequency.setValueAtTime(350, t); bp.frequency.exponentialRampToValueAtTime(3200, t + 0.28); bp.frequency.exponentialRampToValueAtTime(900, t + d);
  g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.55, t + 0.12); g.gain.exponentialRampToValueAtTime(0.0001, t + d);
  src.connect(bp); bp.connect(g); g.connect(out); src.start(t); src.stop(t + d + 0.02); } catch (e) {} }
'''
rep('function closeIntro() {', fn + 'function closeIntro() {')
css = '''<style id="v202">
#ovIntro .inWinImg{transition:opacity .25s ease}
#ovIntro .inWinImg.ldg{opacity:0!important}
#ovIntro:not([hidden]){animation:inFade .28s ease-out}
@keyframes inFade{from{opacity:0;transform:translateY(8px) scale(.98)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){#ovIntro:not([hidden]){animation:none}}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
