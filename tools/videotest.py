#!/usr/bin/env python3
# Aufruf (im Repo): python3 tools/videotest.py [bis] [ausgabe_ordner] [ab]   Umgebung: SITE=site VW=412 VH=915
# Auswertung: python3 tools/video_auswertung.py ausgabe_ordner
"""Video-Analyse: Spielt W1–UNTIL mit simulierter Uhr (Bot aus autotest60), macht alle STEP ms einen Screenshot
und ein DOM-Protokoll sichtbarer Overlay-Elemente. Auswertung: hängende Elemente, Überdeckungen."""
import json, sys, time, subprocess, os, signal, socket
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from autotest60 import BOT
BOT = BOT.replace("['SPIN', 'COLLECT'", "['SPIN', 'DROP IT', 'COLLECT'")   # Rettungs-Lucky: DROP IT
from playwright.sync_api import sync_playwright
UNTIL = int(sys.argv[1]) if len(sys.argv) > 1 else 60
OUT = sys.argv[2] if len(sys.argv) > 2 else "video"
FROM = int(sys.argv[3]) if len(sys.argv) > 3 else 0
STEP = 2500
os.makedirs(OUT, exist_ok=True)
def _free_port():
    with socket.socket() as so: so.bind(("127.0.0.1", 0)); return so.getsockname()[1]
PORT = _free_port()
SNAP = r"""
() => {
  const vw = innerWidth, vh = innerHeight, out = [];
  const RX = /toast|ann|bubble|alert|msg|card|banner|crate|book|wow|hint|tip|badge|djSong|genAv|buddy|coach|cel|pop|stamp|praise|breach|sign|drop|ov[A-Z]|sheet|ad[A-Z]|bandit|hack|intro|join|map|pause|over|cloud|awBar|hkMiss|nuts|comicArrow|radio|fx|flash|say|rb|gen|ledger|doc|mission|msn/i;
  const seen = new Set();
  for (const e of document.querySelectorAll('body *')) {
    if (e.tagName === 'SCRIPT' || e.tagName === 'STYLE' || e.tagName === 'LINK') continue;
    const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.08) continue;
    if (cs.position !== 'fixed' && cs.position !== 'absolute') continue;
    const r = e.getBoundingClientRect(); if (r.width < 24 || r.height < 16) continue;
    if (r.right < 0 || r.bottom < 0 || r.left > vw || r.top > vh) continue;
    const key = (e.id || '') + '|' + String(e.className || '').slice(0, 40);
    if (!RX.test(key) && !(parseInt(cs.zIndex) >= 40)) continue;
    // nur oberste Overlay-Knoten: Kinder eines bereits gelisteten Elements überspringen
    let p = e.parentElement, skip = false; while (p) { if (seen.has(p)) { skip = true; break; } p = p.parentElement; } if (skip) continue;
    seen.add(e);
    const txt = (e.innerText || e.getAttribute('alt') || '').replace(/\s+/g, ' ').trim().slice(0, 50);
    out.push({ k: key, z: cs.zIndex, r: [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)], t: txt, op: +parseFloat(cs.opacity).toFixed(2) });
  }
  const S = window.__TT && window.__TT.S;
  return { wave: S ? S.wave : -1, inWave: !!(S && S.inWave), now: performance.now(), el: out };
}
"""
EXTRA = r"""
/* videotest: Glühbirnen-Tipp (tipBulb) wie ein Spieler nach ~3,5 s mit GOT IT schließen */
setInterval(() => {
  const S = window.__TT && window.__TT.S; if (!S || !S.started) return;
  const t = document.getElementById('tipBulb');
  if (t && !t.hidden && getComputedStyle(t).display !== 'none') { t.__at = t.__at || performance.now(); if (performance.now() - t.__at > 3500) { const b = t.querySelector('button:not(:disabled)'); if (b) { b.click(); t.__at = 0; window.__AT.ev.push({ t: performance.now(), k: 'bot', e: 'tip:' + b.innerText.trim().slice(0, 20), wave: S.wave }); } } } else if (t) t.__at = 0;
}, 300);
"""
def main():
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=os.environ.get("SITE", "site"), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
    time.sleep(1.5); frames = []; cons = []
    try:
        with sync_playwright() as p:
            br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox", "--autoplay-policy=no-user-gesture-required", "--mute-audio"])
            ctx = br.new_context(viewport={"width": int(os.environ.get("VW", 412)), "height": int(os.environ.get("VH", 915))}, device_scale_factor=1)
            ctx.route("**/api/**", lambda r: r.fulfill(status=200, content_type="application/json", body="{}"))
            ctx.add_init_script("""try{localStorage.setItem('capy-reset','276');localStorage.setItem('tarnturm-tut','1');localStorage.setItem('tarnturm-terms','1');if(!localStorage.getItem('capy-lang'))localStorage.setItem('capy-lang','en');}catch(e){}""")
            pg = ctx.new_page()
            pg.on("console", lambda m: cons.append(m.text[:160]) if m.type == "error" else None)
            pg.on("pageerror", lambda e: cons.append("PAGEERROR " + str(e)[:200]))
            pg.clock.install(); pg.goto(f"http://localhost:{PORT}/index.html"); pg.clock.run_for(3000)
            pg.evaluate(BOT); pg.evaluate(EXTRA); pg.evaluate(f"window.__TT.startGame('chill', {FROM})")
            wall0 = time.time(); last = -1; last_t = 0; i = 0
            while True:
                pg.clock.run_for(STEP); i += 1
                snap = pg.evaluate(SNAP); snap["i"] = i
                pg.screenshot(path=f"{OUT}/f{i:05d}.jpg", type="jpeg", quality=45)
                frames.append(snap)
                w = snap["wave"]
                if w != last: last = w; last_t = snap["now"]; print(f"W{w:3d} frame {i} real {time.time()-wall0:5.0f}s", flush=True)
                if snap["now"] - last_t > 10 * 60000: print("HAENGT", w, flush=True); break
                if w > UNTIL or time.time() - wall0 > 3 * 3600: break
                over = pg.evaluate("!!window.__TT.S.over")
                if over: print("GAME OVER", flush=True); break
            at = pg.evaluate("window.__AT"); br.close()
    finally:
        os.killpg(srv.pid, signal.SIGTERM)
    json.dump({"frames": frames, "console": cons[-100:], "at": at}, open(f"{OUT}/frames.json", "w"), ensure_ascii=False)
    print("gespeichert", len(frames), "frames")
if __name__ == "__main__": main()
