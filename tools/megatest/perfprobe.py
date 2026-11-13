#!/usr/bin/env python3
"""Megatest F1/F6: echte Uhr. Je Gerätegruppe FPS bei W5/W45/W95 (8 s messen), Grafikstufe; Ladezeit bei 3G (nur Chromium)."""
import json, os, sys, time, subprocess, signal, socket
from playwright.sync_api import sync_playwright
sys.argv_save = sys.argv; HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1]; OUT = sys.argv[2]
GROUPS = {"1": dict(name="Alt-klein", w=360, h=640, cpu=6), "2": dict(name="Schmal-lang", w=360, h=800, cpu=3.7), "3": dict(name="Standard", w=412, h=915, cpu=3.7),
          "4": dict(name="Neu-schnell", w=412, h=915, cpu=1), "5": dict(name="Tablet", w=800, h=1280, cpu=3.7), "6": dict(name="iPhone", w=390, h=844, cpu=1, webkit=True),
          "7": dict(name="Telegram+Schrift130", w=412, h=800, cpu=3.7)}
FPS_MIN = {"1": 24, "2": 24, "3": 40, "4": 40, "5": 40, "6": 40, "7": 24}
with socket.socket() as so: so.bind(("127.0.0.1", 0)); port = so.getsockname()[1]
srv = subprocess.Popen(["python3", "-m", "http.server", "--bind", "127.0.0.1", str(port)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid); time.sleep(1.5)
res = []
INIT = "try{localStorage.setItem('capy-reset','276');localStorage.setItem('tarnturm-tut','1');localStorage.setItem('tarnturm-terms','1');localStorage.setItem('capy-lang','en');}catch(e){}"
FPS = "new Promise(r=>{let n=0,t0=performance.now(),mx=0,l=t0;const f=t=>{n++;mx=Math.max(mx,t-l);l=t;if(t-t0<8000)requestAnimationFrame(f);else r({fps:n*1000/(t-t0),maxGap:mx,lite:(document.body.className.match(/lite\\S*/g)||[]).join(' ')});};requestAnimationFrame(f);})"
try:
    with sync_playwright() as p:
        for gk, G in GROUPS.items():
            try:
                br = p.webkit.launch() if G.get("webkit") else p.chromium.launch(**({"executable_path": "/usr/bin/google-chrome"} if os.path.exists("/usr/bin/google-chrome") else {}), args=["--mute-audio"])
                ctx = br.new_context(viewport={"width": G["w"], "height": G["h"]}, device_scale_factor=1, has_touch=True); ctx.add_init_script(INIT)
                ctx.route("**/api/**", lambda r: r.fulfill(status=200, content_type="application/json", body="{}"))
                pg = ctx.new_page()
                if not G.get("webkit") and G["cpu"] > 1: ctx.new_cdp_session(pg).send("Emulation.setCPUThrottlingRate", {"rate": G["cpu"]})
                t0 = time.time(); pg.goto(f"http://localhost:{port}/index.html"); pg.wait_for_function("!!(window.__TT&&window.__TT.startGame)", timeout=60000); load = time.time() - t0
                row = {"g": gk, "name": G["name"], "load_local_s": round(load, 1), "waves": []}
                for w in (5, 45, 95):
                    pg.evaluate(f"window.__TT.startGame('chill',{w})"); pg.wait_for_timeout(9000)
                    pg.evaluate("(()=>{const S=window.__TT.S;S.waveCD=0;try{window.__TT.startWave()}catch(e){}})()"); pg.wait_for_timeout(6000)
                    m = pg.evaluate(FPS); m["w"] = w; m["ok"] = m["fps"] >= FPS_MIN[gk]; row["waves"].append(m)
                res.append(row); print(json.dumps(row), flush=True); br.close()
            except Exception as e:
                res.append({"g": gk, "name": G["name"], "error": str(e)[:200]}); print("ERR", gk, e, flush=True)
        # F6: 3G-Ladezeit (Chromium, Standard-Gerät, leerer Cache)
        try:
            br = p.chromium.launch(**({"executable_path": "/usr/bin/google-chrome"} if os.path.exists("/usr/bin/google-chrome") else {}), args=["--mute-audio"])
            ctx = br.new_context(viewport={"width": 412, "height": 915}); ctx.add_init_script(INIT); pg = ctx.new_page()
            cdp = ctx.new_cdp_session(pg); cdp.send("Network.enable"); cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": 300, "downloadThroughput": 1.6e6 / 8 * 0.9, "uploadThroughput": 750e3 / 8 * 0.9})
            t0 = time.time(); pg.goto(f"http://localhost:{port}/index.html", timeout=120000); pg.wait_for_function("!!(window.__TT&&window.__TT.startGame)", timeout=120000); t1 = time.time() - t0
            pg.wait_for_load_state("networkidle", timeout=180000); t2 = time.time() - t0
            res.append({"f6": True, "ready_s": round(t1, 1), "idle_s": round(t2, 1), "ok": t1 <= 35}); print("F6", t1, t2, flush=True); br.close()
        except Exception as e:
            res.append({"f6": True, "error": str(e)[:200]})
finally:
    os.killpg(srv.pid, signal.SIGTERM)
json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=0); print("perf fertig")
