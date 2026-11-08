#!/usr/bin/env python3
"""V465 – Nuts-Disco: dauerhafter weißer Spotkegel von oben auf den DJ (Martin 08.11. 16:51).
Nutzung: python3 tools/patch465.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V464";', 'const GAME_VER = "V465";')
css = '''
#nzDisco .nzKey{position:absolute;top:-10px;width:var(--kw,150px);height:var(--kh,140px);margin-left:calc(var(--kw,150px) / -2);mix-blend-mode:screen;filter:blur(2.5px);
clip-path:polygon(40% 0,60% 0,100% 100%,0 100%);background:linear-gradient(180deg,rgba(255,250,235,.6),rgba(255,250,235,.32) 75%,rgba(255,250,235,.1))}
#nzDisco .nzPool{position:absolute;width:var(--kw,150px);height:60px;margin:-30px 0 0 calc(var(--kw,150px) / -2);border-radius:50%;mix-blend-mode:screen;background:radial-gradient(ellipse,rgba(255,250,235,.45),rgba(255,250,235,.15) 55%,rgba(255,250,235,0) 72%)}
body.inNuts header .djBox{z-index:9!important}
body.inNuts::before{-webkit-mask-image:radial-gradient(ellipse 95px 85px at var(--djx,85%) var(--djy,60px),transparent 45%,#000 100%);mask-image:radial-gradient(ellipse 95px 85px at var(--djx,85%) var(--djy,60px),transparent 45%,#000 100%)}
body.inNuts header .djBox img{filter:brightness(1.3) drop-shadow(0 0 10px rgba(255,248,225,.55))!important}
'''
i = s.rindex('</style>'); s = s[:i] + css + s[i:]
rep('#nzDisco{position:fixed;inset:0;pointer-events:none;z-index:5;', '#nzDisco{position:fixed;inset:0;pointer-events:none;z-index:39;')   # V465: im .app unter dem Header, DJ liegt drüber
rep('    document.body.appendChild(el);\n  }\n  function pos(){', '    (document.querySelector(".app") || document.body).appendChild(el);\n  }\n  function pos(){')
rep('<div class="nzHalo"></div>\';', '<div class="nzHalo"></div><div class="nzKey"></div><div class="nzPool"></div>\';')
rep('    const h = el.querySelector(".nzHalo"); h.style.left = dx + "px"; h.style.top = dy + "px";',
    '    const h = el.querySelector(".nzHalo"); h.style.left = dx + "px"; h.style.top = dy + "px";\n'
    '    const kw = r && r.width ? Math.round(r.width * 1.35) : 150, ky = r && r.height ? r.bottom - 8 : dy + 40;   /* V465: weißer Dauer-Spot */\n'
    '    const ke = el.querySelector(".nzKey"), pe = el.querySelector(".nzPool"); el.style.setProperty("--kw", kw + "px");\n'
    '    ke.style.left = dx + "px"; ke.style.setProperty("--kh", Math.round(ky + 10) + "px"); pe.style.left = dx + "px"; pe.style.top = ky + "px";\n'
    '    document.body.style.setProperty("--djx", Math.round(dx) + "px"); document.body.style.setProperty("--djy", Math.round(dy) + "px");')
open(dst, "w", encoding="utf-8").write(s)
print("ok V465")
