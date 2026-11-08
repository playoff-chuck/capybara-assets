#!/usr/bin/env python3
"""V463 – Zahnrad-Menü als Vollbild-Overlay (nicht mehr im Spielfeld abgeschnitten, so groß wie möglich).
Anführer-Monster (Martin 08.11. «Top, passt»): Welle 6–40, jedes 6. Monster +60 % Leben, +25 % Tempo, rotes Leuchten, doppeltes Gold. Nicht in Nuts.
Nutzung: python3 tools/patch463.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V462";', 'const GAME_VER = "V463";')
# Anführer
rep('''      if (S.nuts.lvl % 10 === 0 && !S.nuts.bossOut) {   /* V454: Boss-Level L10/20/30 */''',
    '''      if (S.nuts.lvl % 10 === 0 && !S.nuts.bossOut) {   /* V454: Boss-Level L10/20/30 */''')
i = s.index('    if (S.nuts) for (let i = n0; i < S.monsters.length; i++) { const m = S.monsters[i]; const f = nutsHp(S.nuts.lvl);')
s = s[:i] + ('    if (!S.nuts && S.wave >= 6 && S.wave <= 40) for (let i = n0; i < S.monsters.length; i++) { const m = S.monsters[i]; S.ldN = (S.ldN || 0) + 1;   /* V463: Anführer */\n'
             '      if (S.ldN % 6 === 0 && !m.boss) { m.hp *= 1.6; if (m.max) m.max *= 1.6; m.speed *= 1.25; m.lead = true; if (m.reward) m.reward *= 2; } }\n') + s[i:]
rep(';function drawMonSprite(ctx,m,cx,cy,s,now){const k=m.kind,im=MON_SPR[k];if(!im||!im.complete||!im.naturalWidth)return false;',
    ';function drawMonSprite(ctx,m,cx,cy,s,now){const k=m.kind,im=MON_SPR[k];if(!im||!im.complete||!im.naturalWidth)return false;'
    'if(m.lead){const rr=s*(MON_R[k]||0.33)*1.25,pu=0.55+0.45*Math.abs(Math.sin(now/180));ctx.save();const g=ctx.createRadialGradient(cx,cy,rr*0.3,cx,cy,rr*1.35);g.addColorStop(0,"rgba(255,40,40,0)");g.addColorStop(0.6,`rgba(255,40,40,${(0.55*pu).toFixed(2)})`);g.addColorStop(1,"rgba(255,40,40,0)");ctx.fillStyle=g;ctx.beginPath();ctx.arc(cx,cy,rr*1.35,0,7);ctx.fill();ctx.restore();}')

css = '''
#ovSettings{position:fixed!important;inset:0!important;z-index:80!important;height:auto!important;background:rgba(24,14,6,.6)!important;overflow:hidden!important;display:flex;align-items:center!important;justify-content:center!important;padding:0!important}
#ovSettings[hidden]{display:none!important}
#ovSettings .joinBox{transform-origin:50% 50%!important}
'''
i = s.rindex('</style>'); s = s[:i] + css + s[i:]
rep("const avail = innerHeight - 20, h = box.getBoundingClientRect().height; const r = box.getBoundingClientRect(), k = Math.min(1, (innerWidth - 20) / Math.max(1, r.width), Math.max(0.6, avail / Math.max(1, h)));",
    "const avail = innerHeight - 24, h = box.getBoundingClientRect().height; const r = box.getBoundingClientRect(), k = Math.min(1.2, (innerWidth - 16) / Math.max(1, r.width), Math.max(0.6, avail / Math.max(1, h)));   /* V463: Vollbild, darf größer werden */")
open(dst, "w", encoding="utf-8").write(s)
print("ok V463")
