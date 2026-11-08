#!/usr/bin/env python3
"""V462 – Nuts-Disco: rote/pinke Spots schwenken über den DJ, Discokugel mit wandernden Lichtpunkten,
pulsierendes Farblicht. Nuts-Gold pro Level 500 (Martin 08.11. «D 500»).
Nutzung: python3 tools/patch462.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V461";', 'const GAME_VER = "V462";')
rep('perLevel: 1000', 'perLevel: 500')
rep('SQUAD KIT · 2× every special · 0 gold · +1000 per level', 'SQUAD KIT · 2× every special · 0 gold · +500 per level', s.count('SQUAD KIT · 2× every special · 0 gold · +1000 per level'))

css = r'''
#nzDisco{position:fixed;inset:0;pointer-events:none;z-index:5;display:none;overflow:hidden}
body.inNuts #nzDisco{display:block}
#nzDisco .nzWash{position:absolute;inset:0;mix-blend-mode:screen;background:radial-gradient(ellipse 60% 40% at 30% 60%,rgba(255,30,90,.16),transparent 70%),radial-gradient(ellipse 55% 40% at 75% 45%,rgba(120,60,255,.14),transparent 70%);animation:nzWash 2.4s ease-in-out infinite alternate}
@keyframes nzWash{0%{opacity:.35;filter:hue-rotate(0deg)}50%{opacity:1}100%{opacity:.5;filter:hue-rotate(-40deg)}}
#nzDisco .nzDots{position:absolute;left:50%;top:var(--by,120px);width:1400px;height:1400px;margin:-700px 0 0 -700px;mix-blend-mode:screen;opacity:.5;filter:blur(.6px);
background:radial-gradient(circle at 20% 30%,rgba(255,80,140,.9) 0 3px,transparent 6px),radial-gradient(circle at 70% 22%,rgba(255,210,90,.85) 0 3px,transparent 6px),radial-gradient(circle at 82% 60%,rgba(255,60,90,.9) 0 3.5px,transparent 7px),radial-gradient(circle at 35% 75%,rgba(120,200,255,.8) 0 3px,transparent 6px),radial-gradient(circle at 55% 45%,rgba(255,255,255,.8) 0 2px,transparent 5px),radial-gradient(circle at 12% 58%,rgba(230,90,255,.85) 0 3px,transparent 6px);
background-size:330px 330px;animation:nzSpin 14s linear infinite}
@keyframes nzSpin{to{transform:rotate(360deg)}}
#nzDisco .nzBall{position:absolute;left:var(--bx,50%);top:var(--by,120px);width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;
background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.95) 0 3px,rgba(255,255,255,0) 9px),repeating-linear-gradient(0deg,rgba(40,40,60,.55) 0 1px,transparent 1px 5px),repeating-linear-gradient(90deg,rgba(40,40,60,.55) 0 1px,transparent 1px 5px),linear-gradient(110deg,#b9c0d6,#f4f6ff 30%,#8e95ad 55%,#e8ecff 75%,#7c839b);
background-size:auto,auto,10px 10px,100% 100%;box-shadow:0 0 14px rgba(255,180,230,.8),0 0 34px rgba(255,60,140,.45);animation:nzBall 1.6s linear infinite}
#nzDisco .nzBall::before{content:"";position:absolute;left:50%;bottom:100%;width:2px;height:400px;margin-left:-1px;background:linear-gradient(0deg,#555,#222)}
@keyframes nzBall{to{background-position:0 0,0 0,10px 0,0 0}}
#nzDisco .nzBeam{position:absolute;top:-30px;width:160px;height:var(--bh,260px);margin-left:-80px;transform-origin:50% 0;mix-blend-mode:screen;filter:blur(3px);
clip-path:polygon(46% 0,54% 0,100% 100%,0 100%);background:linear-gradient(180deg,rgba(255,40,70,.55),rgba(255,40,70,.16) 70%,rgba(255,40,70,0));animation:nzSweep 2.6s ease-in-out infinite alternate}
#nzDisco .nzBeam.b2{background:linear-gradient(180deg,rgba(255,60,200,.5),rgba(255,60,200,.14) 70%,rgba(255,60,200,0));animation-duration:3.3s;animation-delay:-1.4s;animation-direction:alternate-reverse}
#nzDisco .nzBeam.b3{width:120px;margin-left:-60px;background:linear-gradient(180deg,rgba(255,20,20,.5),rgba(255,20,20,.14) 70%,rgba(255,20,20,0));animation-duration:1.9s;animation-delay:-.6s}
@keyframes nzSweep{0%{transform:rotate(var(--a0,-28deg))}100%{transform:rotate(var(--a1,28deg))}}
#nzDisco .nzHalo{position:absolute;width:150px;height:110px;margin:-55px 0 0 -75px;border-radius:50%;mix-blend-mode:screen;background:radial-gradient(ellipse,rgba(255,50,110,.55),rgba(255,50,110,0) 70%);animation:nzWash 1.2s ease-in-out infinite alternate}
@media (prefers-reduced-motion:reduce){#nzDisco *{animation:none!important}}
'''
i = s.rindex('</style>'); s = s[:i] + css + s[i:]

js = r"""<script>/* V462 Nuts-Disco */
(function(){
  let el = null;
  function mk(){
    el = document.createElement("div"); el.id = "nzDisco";
    el.innerHTML = '<div class="nzWash"></div><div class="nzDots"></div><div class="nzBeam"></div><div class="nzBeam b2"></div><div class="nzBeam b3"></div><div class="nzHalo"></div><div class="nzBall"></div>';
    document.body.appendChild(el);
  }
  function pos(){
    if (!document.body.classList.contains("inNuts")) return;
    if (!el) mk();
    const dj = document.querySelector("header .djBox"), r = dj && dj.getBoundingClientRect();
    const W = innerWidth;
    let dx = W - 70, dy = 60;
    if (r && r.width) { dx = r.left + r.width / 2; dy = r.top + r.height / 2; }
    const bs = el.querySelectorAll(".nzBeam");
    const xs = [dx - 70, dx + 40, Math.max(60, dx - 170)];
    bs.forEach((b, k) => {
      const x = xs[k], ang = Math.atan2(dx - x, dy + 30) * -180 / Math.PI;
      b.style.left = x + "px";
      b.style.setProperty("--bh", Math.round(Math.hypot(dx - x, dy + 30) + 160) + "px");
      b.style.setProperty("--a0", (ang - 15) + "deg"); b.style.setProperty("--a1", (ang + 15) + "deg");
    });
    const h = el.querySelector(".nzHalo"); h.style.left = dx + "px"; h.style.top = dy + "px";
    let hb = 110; document.querySelectorAll("canvas").forEach(c => { const q = c.getBoundingClientRect(); if (q.width > W * 0.6 && q.height > 200) hb = q.top; });
    el.style.setProperty("--bx", Math.round(W * 0.5) + "px");
    el.style.setProperty("--by", Math.round(hb + 30) + "px");
  }
  setInterval(pos, 400); addEventListener("resize", pos);
})();
</script>"""
i = s.rindex('</body>'); s = s[:i] + js + s[i:]
open(dst, "w", encoding="utf-8").write(s)
