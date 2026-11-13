# Erzeugt megatest.py aus testbot.py (Injektionen statt Kopie, damit testbot.py unverändert bleibt).
import re
s = open('/root/megatest/testbot.py', encoding='utf8').read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep("  let n = 0;\n", "  let n = 0; window.__ADD = add; window.__VIS = vis; window.__R = R; window.__INTER = inter; window.__MODAL = MODAL;\n")
rep('G = GROUPS[sys.argv[1]]; FROM = int(sys.argv[2]); UNTIL = int(sys.argv[3]); OUT = sys.argv[4]; LANG = sys.argv[5] if len(sys.argv) > 5 else G["lang"]',
    'G = GROUPS[sys.argv[1]]; FROM = int(sys.argv[2]); UNTIL = int(sys.argv[3]); OUT = sys.argv[4]; LANG = sys.argv[5] if len(sys.argv) > 5 else G["lang"]\n'
    'NUTS = os.environ.get("NUTS")  # "c" → Nuts-Kontinent c, FROM/UNTIL = Level\n'
    'TMAX = float(os.environ.get("TMAX", "75")); EXTRA = open(os.path.join(HERE, "extra.js"), encoding="utf8").read()')
rep('device_scale_factor=2,', 'device_scale_factor=1,')
rep('ctx.add_init_script(CHECK)', 'ctx.add_init_script(CHECK); ctx.add_init_script(EXTRA)')
rep("""            pg.evaluate(f"window.__TT.startGame('{os.environ.get('MODE', 'chill')}', {FROM})")""",
    """            if NUTS:
                pg.evaluate(f"window.__TT.startGame('{os.environ.get('MODE', 'chill')}', 31)"); pg.clock.run_for(3000)
                pg.evaluate(f"(()=>{{const S=window.__TT.S; S.inWave=false; S.signOpen={int(NUTS)}+1; document.getElementById('signNuts').click(); const n=window.__TT.S.nuts; if({FROM}>1){{n.lvl={FROM}-1; n.cleared={FROM}-1; window.__TT.S.wave=n.base+{FROM}-1; window.__TT.S.gold+=500*({FROM}-1);}}}})()")
            else:
                pg.evaluate(f"window.__TT.startGame('{os.environ.get('MODE', 'chill')}', {FROM})")""")
# Schleife: TAP TO CONTINUE, Leben auffüllen, Nuts-Level als Fortschritt
rep("""                pg.evaluate("(()=>{const o=document.getElementById('ovPause');""",
    """                pg.evaluate("(()=>{const h=document.getElementById('celHost');if(h&&h.classList.contains('tap')){const t=h.querySelector('.celTap');if(t)t.click();else h.click();}const S=window.__TT.S;if(S&&S.started&&!S.over&&S.lives<4)S.lives=6;const nb=document.getElementById('nrBack');})()")
                pg.evaluate("(()=>{const o=document.getElementById('ovPause');""")
rep("""st = pg.evaluate("({w: window.__TT.S.wave, over: !!window.__TT.S.over, t: performance.now(), inW: !!window.__TT.S.inWave})")""",
    """st = pg.evaluate("(()=>{const S=window.__TT.S;return {w: S.nuts ? S.nuts.lvl : S.wave, nuts: !!S.nuts, over: !!S.over, t: performance.now(), inW: !!S.inWave}})()")""")
rep("if st[\"w\"] > UNTIL or st[\"over\"] or time.time() - wall0 > 110 * 60: break",
    "if st[\"w\"] > UNTIL or st[\"over\"] or (NUTS and not st[\"nuts\"]) or time.time() - wall0 > TMAX * 60: break")
rep("if shot_n < 80:", "if shot_n < 60:")
open('/root/megatest/megatest.py', 'w', encoding='utf8').write(s); print('megatest.py ok', len(s))
