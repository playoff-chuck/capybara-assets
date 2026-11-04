"""V215: 10-Tonner im Comic-Stil (neues Gewicht im Spiel und im Shop/Guide), Rosie/Blue-Einblendung comichafter:
springt mit Wackeln von unten an den Rand, Sprechblase mit Spitze zur Figur, kleiner und näher am Spielfeld."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V214";', 'const GAME_VER = "V215";')
rep('ton:"img/07edb4cdd7.webp"', 'ton:"img/ton_icon.webp"')
# Neues Gewicht zeichnen (Bild), alte Zeichnung als Rückfall
rep('function drawTon(s, W) {', '''const TON_IMG = new Image(); TON_IMG.src = "img/ton_weight.webp";
function drawTon(s, W) {
  const T0 = S.ton; if (T0 && TON_IMG.complete && TON_IMG.naturalWidth) {
    const y = T0.y * s, now = performance.now() / 1000, falling = !T0.hit, sway = falling ? Math.sin(now * 9) * s * 0.05 : 0;
    const bw = W - s * 1.4, cx = W / 2, ar = TON_IMG.naturalHeight / TON_IMG.naturalWidth, iw = Math.min(bw * 0.62, (5.2 * s) / ar), ih = iw * ar;
    const sq = T0.hit ? Math.max(0, 1 - (T0.t || 0) * 4) : 0, sx = 1 + sq * 0.14, sy = 1 - sq * 0.16;   // Aufprall: kurz platt drücken
    ctx.save(); ctx.translate(cx + sway, y + 3 * s);
    if (falling) { ctx.strokeStyle = "rgba(40,30,20,.45)"; ctx.lineWidth = Math.max(2, s * 0.09); ctx.lineCap = "round"; for (const k of [-0.32, -0.1, 0.12, 0.34]) { ctx.beginPath(); ctx.moveTo(k * iw, -ih - s * 0.3); ctx.lineTo(k * iw, -ih - s * (1.2 + Math.abs(k) * 2)); ctx.stroke(); } }
    ctx.strokeStyle = "#3a2414"; ctx.lineWidth = Math.max(3, s * 0.13); ctx.beginPath(); ctx.moveTo(0, -ih + ih * 0.05); ctx.lineTo(0, -ih - 4000); ctx.stroke();
    ctx.scale(sx, sy); ctx.drawImage(TON_IMG, -iw / 2, -ih, iw, ih); ctx.restore(); return; }
  return drawTonOld(s, W); }
function drawTonOld(s, W) {''')
i = s.rfind('})();\n</script>'); s = s[:i] + '\n  try { window.__TT && (window.__TT.startTon = () => startTon(), window.__TT.buddyHelp = k => buddyHelp(k)); } catch (e) {}\n' + s[i:]
css = '''<style id="v215">
/* Rosie/Blue-Hilfe: comichaft, harmonisch */
#buddy{bottom:calc(env(safe-area-inset-bottom,0px) + 196px)!important;width:min(34vw,150px)!important;transition:transform .5s cubic-bezier(.2,1.6,.4,1)!important}
#buddy.l{left:6px!important;transform:translate(-130%,30px) rotate(-12deg)!important}
#buddy.r{right:6px!important;transform:translate(130%,30px) rotate(12deg)!important}
#buddy.on.l{transform:rotate(-4deg)!important;animation:budWob 1.2s ease-in-out .45s infinite}
#buddy.on.r{transform:rotate(4deg)!important;animation:budWobR 1.2s ease-in-out .45s infinite}
@keyframes budWob{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(1deg) translateY(-3px)}}
@keyframes budWobR{0%,100%{transform:rotate(4deg)}50%{transform:rotate(-1deg) translateY(-3px)}}
#buddy img{filter:drop-shadow(0 3px 0 rgba(58,36,20,.55)) drop-shadow(0 6px 8px rgba(0,0,0,.25))!important}
#buddy .say{position:relative;white-space:normal!important;max-width:min(62vw,230px)!important;width:max-content;text-align:center;font-family:"Bangers","Impact",sans-serif!important;font-size:clamp(16px,4.8vw,21px)!important;line-height:1!important;color:#3a2414!important;background:#fff!important;border:3px solid #3a2414!important;border-radius:16px!important;padding:6px 10px 5px!important;margin-bottom:10px!important;box-shadow:0 3px 0 #3a2414!important;transform:rotate(-2deg)}
#buddy .say::after{content:"";position:absolute;bottom:-13px;left:42%;width:18px;height:14px;background:#fff;border:3px solid #3a2414;border-top:0;border-left:0;transform:skewX(-25deg) rotate(35deg);border-radius:0 0 4px 0}
#buddy.r .say{transform:rotate(2deg);align-self:flex-end;margin-right:8px!important}
#buddy.l .say{margin-left:8px!important}
#buddy.l .say{align-self:flex-start}
#buddy{align-items:stretch!important}
#buddy.l .say::after{left:30%}
#buddy.r .say::after{left:60%}
#buddy .say small{font-family:"Baloo 2",sans-serif!important;font-weight:800!important;font-size:10px!important;letter-spacing:.1em!important;color:#d94c8c!important;margin-top:2px}
@media (prefers-reduced-motion:reduce){#buddy.on.l,#buddy.on.r{animation:none}}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
