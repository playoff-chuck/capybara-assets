#!/usr/bin/env python3
"""Automatischer Testlauf W1–W60 mit Zeitleiste gegen die Ablauf-Regeln (Fenster & Anzeigen).
Spielt mit simulierter Uhr (Playwright clock), Bot schließt Fenster wie ein Spieler,
Leben/Gold werden aufgefüllt, damit der Lauf durchkommt und alle Angebote fällig werden.
Aufruf: [BUYER=1] python3 tools/autotest60.py [bis_welle] [ausgabe.json] [ab_welle]   (BUYER=1: kauft Anzeigen, hackt den Boss)
"""
import json, sys, time, subprocess, os, signal
from playwright.sync_api import sync_playwright

UNTIL = int(sys.argv[1]) if len(sys.argv) > 1 else 60
OUT = sys.argv[2] if len(sys.argv) > 2 else "autotest60.json"
FROM = int(sys.argv[3]) if len(sys.argv) > 3 else 0   # Start ab Checkpoint-Welle (z. B. 30)
import socket
def _free_port():   # freier Port: ein hängengebliebener alter Testserver darf nie eine alte Version ausliefern (06.11.)
    with socket.socket() as so: so.bind(("127.0.0.1", 0)); return so.getsockname()[1]
PORT = _free_port()

BOT = r"""
(() => {
  const LOG = window.__AT = { ev: [], open: {}, t0: performance.now(), err: [] };
  const now = () => performance.now();
  const vis = id => { const e = document.getElementById(id); return !!(e && !e.hidden && getComputedStyle(e).display !== 'none'); };
  const W = () => {
    const S = window.__TT && window.__TT.S; if (!S) return {};
    const b = document.body.classList;
    return {
      intro: vis('ovIntro') || b.contains('introWin'), give: vis('ovGive'), ad: vis('ovAd'), bandit: vis('ovBandit') || !!S.banditOpen,
      hackAd: vis('ovHackAd') || !!S.hackAdOpen, duel: vis('ovHack') || !!S.duel, join: vis('ovJoin') || !!S.joinOpen, sign: vis('ovSign') || !!S.signOpen,
      orders: vis('ovOrders') || !!S.ordersOpen, map: b.contains('mapUp') || !!S.mapShow || !!S.mapFly, drop: !!S.drop,
      pause: vis('ovPause') || !!S.paused, sheet: vis('sheet'), over: vis('ovOver') || !!S.over, cloud: vis('ovCloud'),
    };
  };
  const title = k => { const id = {intro:'ovIntro',ad:'ovAd',bandit:'ovBandit',hackAd:'ovHackAd',orders:'ovOrders',join:'ovJoin',duel:'ovHack',sign:'ovSign'}[k];
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
    const BUY = !!window.__AT_BUYER;
    if (w.ad && age('ad') > 3600) { const r = document.getElementById('ovAd'); click(pick(r, BUY ? ['I WANT IT', 'BUY', "IT'S FREE", 'THANKS', 'GOT IT', "LET'S GO", 'NO THANKS', 'LATER'] : ['NO THANKS', 'LATER', 'THANKS', "IT'S FREE", 'GOT IT', "LET'S GO"]) , 'ad'); }
    if (w.bandit && age('bandit') > 3600 && Math.floor(age('bandit') / 1000) % 2 === 0) click(pick(document.getElementById('ovBandit'), ['SPIN', 'COLLECT', 'TAKE', 'GRAB', 'GOT IT', 'OK', 'NO THANKS', 'LATER', 'CLOSE']), 'bandit');
    /* Notbremse: Fenster hängt > 15 s → ersten sichtbaren Knopf darin drücken und protokollieren */
    { const IDS = { intro: 'ovIntro', ad: 'ovAd', bandit: 'ovBandit', hackAd: 'ovHackAd', orders: 'ovOrders', join: 'ovJoin', duel: 'ovHack', sign: 'ovSign' };
      for (const k of Object.keys(IDS)) if (w[k] && age(k) > 15000 && Math.floor(age(k) / 1000) % 3 === 0) {
        const r = document.getElementById(IDS[k]); const b = r && btns(r)[0]; LOG.ev.push({ t, k: 'stuck', e: k + ':' + (b ? (b.innerText || '').trim().slice(0, 20) : 'kein Knopf'), wave: S.wave }); if (b) b.click(); } }
    if (w.hackAd && age('hackAd') > 3600) click(pick(document.getElementById('ovHackAd'), BUY ? ['HACK THE BOSS', 'HACK', 'LATER'] : ['LATER', 'NO THANKS']), 'hackAd');
    if (w.duel && age('duel') > 2500 && Math.floor(age('duel') / 1000) % 2 === 0) { const r = document.getElementById('ovHack');
      if (BUY) { const p25 = r && [...r.querySelectorAll('.hkChips button')].find(b => /25/.test(b.textContent)); p25 && p25.click(); }
      click(pick(r, BUY ? ['HACK!', 'CONTINUE', 'COLLECT', 'OK', 'BACK', 'CLOSE', 'SKIP'] : ['SKIP', 'CONTINUE', 'CLOSE', 'OK', 'BACK']), 'duel'); }
    if (BUY && S.duel && window.__TT && window.__TT.HK && ['pick', 'play'].includes(window.__TT.HK.phase)) { try { const cv = document.getElementById('hackCv'), r = cv.getBoundingClientRect();
        const x = r.left + r.width * (0.2 + Math.random() * 0.6), y = r.top + r.height * (0.3 + Math.random() * 0.5);
        for (const ty of ['pointerdown', 'pointerup']) cv.dispatchEvent(new PointerEvent(ty, { bubbles: true, clientX: x, clientY: y, pointerId: 1, isPrimary: true })); cv.dispatchEvent(new MouseEvent('click', { bubbles: true, clientX: x, clientY: y })); } catch (e) {} }   /* Käufer tippt im Duell */
    if (w.orders && age('orders') > 2500) click(pick(document.getElementById('ovOrders'), ['ACCEPT', 'GO', 'OK', 'SKIP']) || btns(document.getElementById('ovOrders'))[0], 'orders');
    if (w.join && age('join') > 2500) click(pick(document.getElementById('ovJoin'), ['LATER', 'SKIP', 'NO THANKS', 'NOT NOW']) || btns(document.getElementById('ovJoin')).slice(-1)[0], 'join');
    if (w.sign && age('sign') > 3000) click(document.getElementById('signNext'), 'sign');
    if (w.give && age('give') > 2500) click(document.getElementById('gOk'), 'give');   /* Orden-Geschenk */
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
            if os.environ.get("BUYER"): pg.evaluate("window.__AT_BUYER = true")   # Käufer-Profil: kauft Anzeigen, hackt den Boss
            pg.evaluate(BOT)
            pg.evaluate(f"window.__TT.startGame('chill', {FROM})")
            wall0 = time.time(); last = -1; last_t = 0
            while True:
                pg.clock.run_for(5000)
                st = pg.evaluate("({w: window.__TT.S.wave, over: !!window.__TT.S.over, t: performance.now()})")
                if st["w"] == last and st["t"] - last_t > 10 * 60000:
                    dump = pg.evaluate("(()=>{const S=window.__TT.S;return {inWave:S.inWave,toSpawn:S.toSpawn,mon:S.monsters.length,cd:S.waveCD,intro:!!S.intro,paused:!!S.paused,open:Object.keys(window.__AT.open),body:document.body.className,vis:[...document.querySelectorAll('[id^=ov]')].filter(e=>!e.hidden&&getComputedStyle(e).display!=='none').map(e=>e.id)}})()")
                    print("HAENGT in Welle", last, dump, flush=True); st["stall"] = dump; break
                if st["w"] != last:
                    last_t = st["t"]
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
