#!/usr/bin/env python3
# V410 (t15): Türme in 4 Richtungen – Seitenbild (rechts/links gespiegelt) + neue Bilder «zu uns» (front) und «weg» (back)
# je Waffe (MG, Cannon, Frost). Umschalten nach Schusswinkel in 90°-Sektoren mit Hysterese, 140 ms Überblenden.
# Bilder: img/tow_<mg|kan|frost>_<front|back>.webp (Nano Banana Pro / Flash, Hintergrund freigestellt, Sockel auf Originalbild ausgerichtet).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V409";', 'const GAME_VER = "V410";')
rep('for(const k in T){const im=new Image();im.src=T[k];TOW_SPR[k]=im;}}function drawTowSprite(',
    'for(const k in T){const im=new Image();im.src=T[k];TOW_SPR[k]=im;}}'
    'const TOW_DIR={};for(const k of["mg","kan","frost"])for(const d of["front","back"]){const im=new Image();im.decoding="async";im.src="img/tow_"+k+"_"+d+".webp";TOW_DIR[k+"_"+d]=im;}'
    'function towView(t,now){if(!t._aim)return 0;const a=t.ang||0,c=Math.abs(Math.cos(a)),sn=Math.sin(a),H=0.12,o=t._vw||0;let v=o;if(o===0){if(Math.abs(sn)>c+H)v=sn>0?1:2;}else if(c>Math.abs(sn)+H)v=0;else v=sn>0?1:2;if(v!==o){t._vwP=o;t._vwT=now;t._vw=v;}return v;}'
    'function drawTowSprite(')
rep('ctx.save();ctx.translate(cx,cy);if(Math.cos(t.ang||0)<0)ctx.scale(-1,1);ctx.drawImage(im,-sz/2,-sz*0.58,sz,sz);ctx.restore();const n=t.w.length',
    '{const now=performance.now(),v=towView(t,now),pick=x=>{const j=x?TOW_DIR[ty+(x===1?"_front":"_back")]:im;return j&&j.complete&&j.naturalWidth?j:im;},'
    'dr=(x,al)=>{if(al<=0)return;ctx.save();ctx.globalAlpha*=al;ctx.translate(cx,cy);if(x===0&&Math.cos(t.ang||0)<0)ctx.scale(-1,1);ctx.drawImage(pick(x),-sz/2,-sz*0.58,sz,sz);ctx.restore();},'
    'p=t._vwT?Math.min(1,(now-t._vwT)/140):1;if(p<1)dr(t._vwP||0,1);dr(v,p);}const n=t.w.length')
rep('      t.ang = Math.atan2(best.y - t.y, best.x - t.x);', '      t.ang = Math.atan2(best.y - t.y, best.x - t.x); t._aim = 1;')
open(dst, "w", encoding="utf-8").write(s)
print("ok", len(s))
