s=open('v186.html',encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(n,a[:70]); s=s.replace(a,b)
rep('ver: "V186", wave: S.wave','ver: "V187", wave: S.wave')
rep('if (rr) { x = rr.left + (rr.width - d) / 2; y = dr2 ? dr2.top + (dr2.height - d) / 2 : rr.top - d + 8; }',
    '''let big = false; { const gA = document.getElementById("genAv"), gr0 = gA && gA.getBoundingClientRect(), free = pr.left - 8;   /* V187: Pause groß links unten, unter dem General, auf Höhe der Kapselmitte */
      if (innerWidth < 700 && free >= 64) { d2 = Math.round(Math.max(52, Math.min(72, free - 20, pr.height * 0.62))); const cx = gr0 && gr0.width ? gr0.left + gr0.width / 2 : 8 + free / 2; x = Math.max(8, Math.min(pr.left - d2 - 8, cx - d2 / 2)); y = pr.top + (pr.height - d2) / 2; big = true; } }
    if (big) {} else if (rr) { x = rr.left + (rr.width - d) / 2; y = dr2 ? dr2.top + (dr2.height - d) / 2 : rr.top - d + 8; }''')
rep('S2("width", d2 + "px"); S2("height", d2 + "px");','S2("width", d2 + "px"); S2("height", d2 + "px"); document.body.classList.toggle("pauseBig", big);')
rep('else { set(sc, cx - sc.offsetWidth / 2, top - 2); const y2 = top - 2 + sc.offsetHeight + 5, w2 = gd.offsetWidth + 5 + nx.offsetWidth; set(gd, cx - w2 / 2, y2); set(nx, cx - w2 / 2 + gd.offsetWidth + 5, y2); } }',
    'else { /* V187 (Martin): 2×2 – Score über Herz/Gold, Wellen-Nummer über den nächsten Steinen */ const gap = 6, w2 = gd.offsetWidth + gap + nx.offsetWidth, x0 = Math.round(cx - w2 / 2), y2 = top - 2 + sc.offsetHeight + 5; set(sc, x0 + (gd.offsetWidth - sc.offsetWidth) / 2, top - 2); set(gd, x0, y2); set(nx, x0 + gd.offsetWidth + gap, y2); } }')
rep('const right = gr && gr.left > r.right ? gr.left : r.right + 12 + n.offsetWidth, cx = (r.right + right) / 2, cy = pr ? pr.top + pr.height / 2 : (gr ? gr.top + gr.height / 2 : r.top + r.height / 2);',
    'const right = gr && gr.left > r.right ? gr.left : r.right + 12 + n.offsetWidth; let cx = (r.right + right) / 2, cy = pr ? pr.top + pr.height / 2 : (gr ? gr.top + gr.height / 2 : r.top + r.height / 2);   /* V187: am Handy über den nächsten Steinen, auf Höhe des Scores */ { const nxe = document.querySelector(".bar>.cell"), sce = document.querySelector(".bar>.score"); if (document.body.classList.contains("hudNarrow") && nxe && sce && nxe.getClientRects().length) { const a = nxe.getBoundingClientRect(), b = sce.getBoundingClientRect(); cx = a.left + a.width / 2; cy = b.top + b.height / 2; } }')
css='''<style id="v187">
/* V187: am Handy nur noch EIN Pause-Knopf (links unten, groß); oben rechts entfällt */
body.pauseBig #bPauseTop{display:none!important}
body.hudNarrow #waveNum{font-size:34px!important;line-height:1!important}
body.pauseBig #bWave{min-height:0!important;border-width:4px!important;box-shadow:0 5px 0 #3a2414!important}
</style>
'''
i=s.rfind('</body>'); s=s[:i]+css+s[i:]
open('v187.html','w',encoding='utf-8').write(s); print('ok')
