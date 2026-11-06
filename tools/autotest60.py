#!/usr/bin/env python3
"""Automatischer Testlauf W1–W60 mit Zeitleiste gegen die Ablauf-Regeln (Fenster & Anzeigen).
Spielt mit simulierter Uhr (Playwright clock), Bot schließt Fenster wie ein Spieler,
Leben/Gold werden aufgefüllt, damit der Lauf durchkommt und alle Angebote fällig werden.
Aufruf: python3 tools/autotest60.py [bis_welle] [ausgabe.json]
"""
import json, sys, time, subprocess, os, signal
from playwright.sync_api import sync_playwright

UNTIL = int(sys.argv[1]) if len(sys.argv) > 1 else 60
OUT = sys.argv[2] if len(sys.argv) > 2 else "autotest60.json"
PORT = 8765

BOT = r"""
(() => {
  const LOG = window.__AT = { ev: [], open: {}, t0: performance.now(), err: [] };
  const now = () => performance.now();
  const vis = id => { const e = document.getElementById(id); return !!(e && !e.hidden && getComputedStyle(e).display !== 'none'); };
  const W = () => {
    const S = window.__TT && window.__TT.S; if (!S) return {};
    const b = document.body.classList;
    return {
      intro: vis('ovIntro') || b.contains('introWin'), ad: vis('ovAd'), bandit: vis('ovBandit') || !!S.banditOpen,
      hackAd: vis('ovHackAd') || !!S.hackAdOpen, duel: vis('ovHack') || !!S.duel, join: vis('ovJoin') || !!S.joinOpen || !!S.signOpen,
      orders: vis('ovOrders') || !!S.ordersOpen, map: b.contains('mapUp') || !!S.mapShow || !!S.mapFly, drop: !!S.drop,
      pause: vis('ovPause') || !!S.paused, sheet: vis('sheet'), over: vis('ovOver') || !!S.over, cloud: vis('ovCloud'),
    };
  };
  const title = k => { const id = {intro:'ovIntro',ad:'ovAd',bandit:'ovBandit',hackAd:'ovHackAd',orders:'ovOrders',join:'ovJoin',duel:'ovHack'}[k];
    const e = id && document.getElementById(id); return e ? (e.innerText || '').replace(/\s+/g, ' ').slice(0, 70) : ''; };
  const btns = root => [...(root || document).querySelectorAll('button, .btn, [role=button]')].filter(e => e.offsetParent !== null && !e.disabled);
  const pick = (root, prefs) => { const bs = btns(root); for (const p of prefs) { const b = bs.find(x => (x.innerText || '').toUpperCase().includes(p)); if (b) return b; } return null; };
  window.addEventListener('error', e => LOG.err.push({ t: now(), m: String(e.message).slice(0, 120) }));
  let prev = {};
  setInterval(() => {
    const S = window.__TT && window.__TT.S; if (!S || !S.started) return;
    if (S.lives < 20) S.lives = 50;
    if (S.gold < 1500) S.gold = 1500;
    { /* Stapel klein halten: alles oberhalb der unteren 6 Reihen leeren, sonst Game over durch Decke */
      const GW = 12, GH = 18; let ch = false;
      for (let i = 0; i < (GH - 6) * GW; i++) if (S.grid[i]) { S.grid[i] = 0; ch = true; if (S.towers && S.towers.delete) S.towers.delete(i); }
      if (ch) { S.dirty = true; S.dist = null; } }
    /* Türme ersetzen: jedes Monster nach 8 s erledigen, sonst laufen sie endlos Runden und die Welle endet nie */
    for (const m of S.monsters) { m.__at = m.__at || now(); if (now() - m.__at > 8000) m.dead = true; }
    const w = W(), t = now();
    for (const k of Object.keys(w)) {
      if (w[k] && !prev[k]) { LOG.open[k] = t; LOG.ev.push({ t, k, e: 'open', wave: S.wave, ttl: title(k), ps: null }); }
      if (!w[k] && prev[k]) { LOG.ev.push({ t, k, e: 'close', wave: S.wave }); delete LOG.open[k]; }
    }
    prev = w;
    // Bot: wie ein Spieler nach ~2,5 s reagieren (Angebote ablehnen, sobald möglich)
    const age = k => t - (LOG.open[k] || t);
    const click = (b, why) => { if (b) { LOG.ev.push({ t, k: 'bot', e: why + ':' + (b.innerText || '').trim().slice(0, 20), wave: S.wave }); b.click(); return true; } return false; };
    if (w.intro && age('intro') > 2500) click(pick(document.getElementById('ovIntro'), ['GOT IT', "LET'S GO", 'OK']), 'intro');
    if (w.ad && age('ad') > 3600) { const r = document.getElementById('ovAd'); click(pick(r, ['NO THANKS', 'LATER', "IT'S FREE", 'GOT IT', "LET'S GO"]) , 'ad'); }
    if (w.bandit && age('bandit') > 3600) click(pick(document.getElementById('ovBandit'), ['NO THANKS', 'LATER', 'SKIP', 'CLOSE']), 'bandit');
    if (w.hackAd && age('hackAd') > 3600) click(pick(document.getElementById('ovHackAd'), ['LATER', 'NO THANKS']), 'hackAd');
    if (w.orders && age('orders') > 2500) click(pick(document.getElementById('ovOrders'), ['ACCEPT', 'GO', 'OK', 'SKIP']) || btns(document.getElementById('ovOrders'))[0], 'orders');
    if (w.join && age('join') > 2500) click(pick(document.getElementById('ovJoin'), ['LATER', 'SKIP', 'NO THANKS', 'NOT NOW']) || btns(document.getElementById('ovJoin')).slice(-1)[0], 'join');
    if (w.drop && age('drop') > 2500) click(pick(document, ['COLLECT', 'GRAB', 'TAKE', 'GOT IT', 'OPEN', "IT'S FREE"]), 'drop');
    if (w.map && age('map') > 4000 && (Math.floor(age('map') / 1500) % 2 === 0)) {
      const b = pick(document, ['CONTINUE', "LET'S GO", 'GO', 'NEXT']); if (b) click(b, 'map');
      else { const c = document.elementFromPoint(206, 600); if (c) { c.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, clientX: 206, clientY: 600 })); c.dispatchEvent(new PointerEvent('pointerup', { bubbles: true, clientX: 206, clientY: 600 })); c.click(); } }
    }
    if (w.pause && age('pause') > 1500) click(pick(document.getElementById('ovPause'), ['RESUME', 'CONTINUE', 'PLAY']), 'pause');
  }, 250);
})();
"""

def main():
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd="site",
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
    time.sleep(1.5)
    res = {}
    try:
        with sync_playwright() as p:
            br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
            ctx = br.new_context(viewport={"width": 412, "height": 915}, device_scale_factor=1)
            ctx.route("**/api/**", lambda r: r.fulfill(status=200, content_type="application/json", body="{}"))
            ctx.add_init_script("""try{localStorage.setItem('capy-reset','276');localStorage.setItem('tarnturm-tut','1');localStorage.setItem('tarnturm-terms','1');}catch(e){}""")
            pg = ctx.new_page()
            cons = []
            pg.on("console", lambda m: cons.append(m.text[:160]) if m.type == "error" else None)
            pg.on("pageerror", lambda e: cons.append("PAGEERROR " + str(e)[:160]))
            pg.clock.install()
            pg.goto(f"http://localhost:{PORT}/index.html")
            pg.clock.run_for(3000)
            pg.evaluate(BOT)
            pg.evaluate("window.__TT.startGame('chill', 0)")
            wall0 = time.time(); last = -1
            while True:
                pg.clock.run_for(5000)
                st = pg.evaluate("({w: window.__TT.S.wave, over: !!window.__TT.S.over, t: performance.now()})")
                if st["w"] != last:
                    last = st["w"]; print(f"W{st['w']:3d}  Spielzeit {st['t']/1000/60:5.1f} min  real {time.time()-wall0:5.0f} s", flush=True)
                if st["w"] > UNTIL or st["over"] or time.time() - wall0 > 3 * 3600:
                    break
            res = pg.evaluate("window.__AT")
            res["console"] = cons[-80:]
            res["end"] = st
            br.close()
    finally:
        os.killpg(srv.pid, signal.SIGTERM)
    json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=0)
    print("gespeichert", OUT, len(res.get("ev", [])), "Ereignisse")

if __name__ == "__main__":
    main()
