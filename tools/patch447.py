#!/usr/bin/env python3
"""V447: Rosie am Fallschirm als echte 3D-Grafik (6 Schwing-Bilder img/chute_1…6.webp, Nano Banana Pro, Sheet 2 mit Helm, 0,28 $ gesamt).
Beim Elite-Wow springt der Partner mit dem neuen Schirm (Rosie); für Blue bleibt vorerst der gezeichnete Schirm.
Elite-Sticker im Turm-Menü rosa, Partner-Bild daneben (Martin 12:53).
Nutzung: python3 tools/patch447.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('GAME_VER = "V446"', 'GAME_VER = "V447"')
rep('d.innerHTML = `<img class="wpPlane" src="img/biplane.webp" alt="">` + ch(b, 1.0, 0, "")   /* V440: nur der Partner springt */;',
    '''const spr = b === "rosie";   /* V447: Rosie mit echtem Fallschirm-Sprite */
  d.innerHTML = `<img class="wpPlane" src="img/biplane.webp" alt="">` + (spr
    ? `<div class="wpChute spr" style="--sx:${Math.round(px(1.0))}px;--sy:${Math.round(py)}px;--tx:${pt.x}px;--ty:${pt.y}px"><img class="wpSpr" src="img/chute_1.webp" alt=""></div>`
    : ch(b, 1.0, 0, ""));
  if (spr) { const im = d.querySelector(".wpSpr"); const seq = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2]; let i = 0; const iv = setInterval(() => { if (!document.body.contains(d)) { clearInterval(iv); return; } i = (i + 1) % seq.length; im.src = `img/chute_${seq[i]}.webp`; }, 150); }''')
rep('@keyframes wowOpen{to{transform:scale(1)}}',
    '@keyframes wowOpen{to{transform:scale(1)}}\n.wpChute.spr .wpSpr{position:absolute;left:-44px;top:-110px;width:88px;height:110px;max-width:none;object-fit:contain;transform:scale(.2);transform-origin:50% 100%;animation:wowOpen .35s ease-out 1.25s forwards;filter:drop-shadow(0 3px 3px rgba(0,0,0,.35))}   /* V447 */')
# Elite-Sticker rosa mit Rosie daneben (Martin 12:53)
rep('.eliteTag{display:flex;align-items:center;gap:10px;background:linear-gradient(135deg,#ffd84d,#ff9f1a);',
    '.eliteTag img{width:64px;height:64px;object-fit:contain;flex:0 0 auto;margin:-10px -4px -10px -6px;filter:drop-shadow(0 2px 2px rgba(0,0,0,.3))}\n.eliteTag{display:flex;align-items:center;gap:10px;background:linear-gradient(135deg,#ffb3d6,#e86fa3);')
rep('.eliteTag small{display:block;font:700 12px var(--f-body);color:#5a3a1a;margin-top:2px}', '.eliteTag small{display:block;font:700 12px var(--f-body);color:#5a1a3a;margin-top:2px}')
rep('h += `<div class="eliteTag"><i>★</i><div><b>ELITE TOWER</b>', 'h += `<div class="eliteTag"><img src="${HERO_IMG[buddyKey()]}" alt=""><div><b>ELITE TOWER</b>')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
