#!/usr/bin/env python3
"""Tutorial-Bot (V593, 11.11.): spielt das Tutorial wie ein Spieler, folgt dem gelben Pfeil, prüft Fehler (Hänger, Figuren, Fenster, Block über Laden, Pfeil trifft Block, Urkunde + Spruch).
Aufruf im Repo: python3 tools/tutbot.py <runs> <out.json>   (Bildschirmgrößen/Sprachen in VIEWS)"""
import json, sys, time, subprocess, os, signal, socket
from playwright.sync_api import sync_playwright
RUNS = int(sys.argv[1]) if len(sys.argv) > 1 else 1
OUT = sys.argv[2] if len(sys.argv) > 2 else "tutbot.json"
SP = os.path.dirname(os.path.abspath(OUT))
with socket.socket() as so: so.bind(("127.0.0.1", 0)); PORT = so.getsockname()[1]
VIEWS = [(362, 780, "ru"), (360, 740, "ru"), (360, 640, "ru"), (412, 915, "ru"), (360, 640, "ru"), (362, 780, "ru"), (390, 844, "en"), (412, 732, "ru"),
         (360, 740, "ru"), (412, 915, "de"), (375, 667, "ru"), (393, 873, "es"), (362, 780, "ru")]
WATCH = r"""
(() => { const L = window.__TB = { bad: [], steps: {}, msgs: 0, say: [] }; let lastMsg = null, bud = false;
  const vis = id => { const e = document.getElementById(id); return !!(e && !e.hidden && e.getClientRects().length && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden'); };
  try { const X = window.__TT.SFX, o = X.say; X.say = function (k) { L.say.push(k); return o.apply(this, arguments); }; } catch (e) {}
  setInterval(() => { try { const T = window.__TUTT.T, S = window.__TT.S; if (!T.on) return;
    if (!(T.step in L.steps)) L.steps[T.step] = Math.round(performance.now());
    const m = window.__msgCur && window.__msgCur.m; if (m && m !== lastMsg) { lastMsg = m; L.msgs++; if (L.msgs > 1) L.bad.push('Meldung im Tutorial: ' + m.kind + ' ' + m.title); }
    const b = document.getElementById('buddy'), bo = !!(b && b.classList.contains('on')); if (bo && !bud) L.bad.push('Figur sichtbar im Tutorial (Schritt ' + (T.step + 1) + ')'); bud = bo;
    for (const id of ['ovIntro', 'ovAd', 'ovBandit', 'ovCoachAd', 'ovOrders', 'ovJoin']) if (vis(id)) { if (!L['w' + id]) L.bad.push('Fenster im Tutorial: ' + id + ' (Schritt ' + (T.step + 1) + ')'); L['w' + id] = 1; }
    const sh = document.getElementById('sheet'); if (sh && !sh.hidden) { const c = document.getElementById('tutPieceCv'); if (c && c.width) { const g = c.getContext('2d'); const d = g.getImageData(0, 0, c.width, Math.min(c.height, c.width * 2)).data; let n = 0; for (let i = 3; i < d.length; i += 400) if (d[i] > 0) n++; if (n > 3 && !L.wShop) { L.bad.push('Block über dem Laden (Schritt ' + (T.step + 1) + ')'); L.wShop = 1; } } }
  } catch (e) {} }, 250); })();
"""
def main():
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd="site", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
    time.sleep(1.5); results = []
    try:
        with sync_playwright() as p:
            br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
            for run in range(RUNS):
                W, H, lang = VIEWS[run % len(VIEWS)]
                ctx = br.new_context(viewport={"width": W, "height": H}, has_touch=False)
                ctx.route("**/api/**", lambda r: r.fulfill(status=200, content_type="application/json", body="{}"))
                ctx.add_init_script("try{localStorage.setItem('capy-reset','276');localStorage.setItem('tarnturm-terms','1');localStorage.setItem('capy-lang','" + lang + "');}catch(e){}")
                pg = ctx.new_page(); errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
                pg.goto(f"http://localhost:{PORT}/index.html"); time.sleep(3)
                pg.evaluate("(()=>{const s=document.getElementById('splash');if(s)s.click();})()"); time.sleep(0.5)
                pg.evaluate("(()=>{const s=document.getElementById('splash');if(s)s.remove();})()")
                pg.evaluate("(()=>{const bs=[...document.querySelectorAll('#ovStart button')].filter(b=>b.offsetParent);bs.sort((a,b)=>b.offsetWidth*b.offsetHeight-a.offsetWidth*a.offsetHeight);bs[0]&&bs[0].click();})()")
                pg.evaluate(WATCH)
                t0 = time.time(); last_step = -1; step_t = time.time(); stuck = None; cert = False; clicks = []; towers0 = 0
                while time.time() - t0 < 420:
                    time.sleep(0.45)
                    st = pg.evaluate("""(()=>{const T=window.__TUTT.T,S=window.__TT.S;const a=document.getElementById('comicArrow');const ar=a&&a.style.display!=='none'&&a.getClientRects().length?a.getBoundingClientRect():null;
                      const vis=id=>{const e=document.getElementById(id);return !!(e&&!e.hidden&&e.getClientRects().length&&getComputedStyle(e).display!=='none')};
                      const sum=document.getElementById('tutSum');
                      return {on:T.on,step:T.step,mode:S.mode,shop:!!S.shop,sel:!!S.sel,tw:S.towers.size,arrow:ar?{x:ar.left+ar.width/2,top:ar.top,bot:ar.bottom,left:ar.left,right:ar.right,up:a.classList.contains('up'),side:a.classList.contains('side')}:null,
                        sum:sum?vis('tutSum'):false,mapUp:document.body.classList.contains('mapUp'),over:!!S.over,ask:vis('tutAsk')}})()""")
                    if st["sum"]:
                        cert = True; time.sleep(4.5)
                        pg.evaluate("(()=>{const b=[...document.querySelectorAll('#tutSum button')].find(b=>!b.disabled);b&&b.click();})()"); time.sleep(1.5); break
                    if st["over"]: break
                    if st["mapUp"]: pg.mouse.click(W // 2, H // 2); continue
                    for ov in ["ovIntro", "ovAd", "ovBandit", "ovCoachAd"]:
                        pg.evaluate(f"(()=>{{const o=document.getElementById('{ov}');if(o&&!o.hidden){{const b=[...o.querySelectorAll('button')].filter(b=>!b.disabled&&b.offsetParent).pop();b&&b.click();}}}})()")
                    if not st["on"]:
                        if time.time() - t0 > 30 and not cert: pass
                        continue
                    if st["step"] != last_step: last_step = st["step"]; step_t = time.time()
                    elif time.time() - step_t > 75: stuck = {"step": st["step"] + 1, "state": st}; break
                    a = st["arrow"]
                    if st["mode"] == "snipe":
                        pg.mouse.click(W // 2, int(H * 0.45)); continue
                    if a:
                        if a["side"]: x, y = a["right"] + 24, (a["top"] + a["bot"]) / 2
                        elif a["up"]: x, y = a["x"], a["top"] - 8
                        else: x, y = a["x"], a["bot"] + 10
                        info = pg.evaluate(f"(()=>{{const e=document.elementFromPoint({x},{y});return e?(e.id||e.className||e.tagName)+'':''}})()")
                        if st["mode"] == "build":
                            cell = pg.evaluate(f"(()=>{{try{{const c=window.__TT.cvCell({{clientX:{x},clientY:{y}}});const S=window.__TT.S;if(!c)return null;const gx=c[0]??c.x,gy=c[1]??c.y;return {{gx,gy,block:!!S.grid[gy*12+gx]}}}}catch(e){{return 'err '+e}}}})()")
                            clicks.append({"step": st["step"] + 1, "x": round(x), "y": round(y), "cell": cell})
                            if isinstance(cell, dict) and not cell.get("block"): pass
                        pg.mouse.click(x, y)
                    else:
                        if st["step"] in (0, 2, 7) or (not st["shop"] and not st["sel"] and st["mode"] is None):
                            pg.evaluate("document.getElementById('bDrop').click()")
                        if st["step"] == 1: pg.evaluate("document.getElementById('bRot').click()")
                        if st["sel"] or st["shop"]:
                            pg.evaluate("(()=>{const b=document.getElementById('sClose');if(b&&b.offsetParent)b.click();})()")
                tb = pg.evaluate("window.__TB")
                r = {"run": run + 1, "view": f"{W}x{H}", "lang": lang, "secs": round(time.time() - t0), "cert": cert, "stuck": stuck, "errs": errs, "bad": tb.get("bad"), "steps": tb.get("steps"), "msgs": tb.get("msgs"), "say_cert": "cert_done" in (tb.get("say") or []), "buildClicks": clicks[:12]}
                print(json.dumps(r, ensure_ascii=False)[:600], flush=True); results.append(r)
                pg.screenshot(path=os.path.join(SP, f"tb_run{run+1}.png")); ctx.close()
            br.close()
    finally:
        os.killpg(srv.pid, signal.SIGTERM)
    json.dump(results, open(OUT, "w"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
