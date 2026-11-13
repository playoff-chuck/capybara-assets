#!/usr/bin/env python3
"""Capybara Testbot nach «Kriterienkatalog Testbot (12.11.2026)».
Aufruf: python3 testbot.py GRUPPE VON BIS OUTDIR [SPRACHE]
Spielt mit simulierter Uhr (wie autotest60, Käufer-Profil) und prüft laufend die Katalogpunkte
B1/B4/B5 (Überlagerungen), B13/E1 (Knöpfe im Bild, nicht über dem Feld), C1 (Text ragt aus Box),
C7 (englische Reste), D1 (Hänger), D2 (Angebots-Abstand), A2/A5 (Lautstärkesprünge = Knackgefahr),
D-Unterbrechung (App-Wechsel alle 10 Wellen), F5 (JS-Fehler), F6/A17 (Ladefehler).
"""
import json, sys, time, subprocess, os, signal, socket, importlib.util
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("at60", os.path.join(HERE, "autotest60.py")); at60 = importlib.util.module_from_spec(spec)
sys.argv_save = sys.argv; sys.argv = [sys.argv[0]]; spec.loader.exec_module(at60); sys.argv = sys.argv_save

GROUPS = {
 "1": dict(name="Alt-klein", w=360, h=640, cpu=6, lang="ru"),
 "2": dict(name="Schmal-lang", w=360, h=800, cpu=3.7, lang="es"),
 "3": dict(name="Standard", w=412, h=915, cpu=3.7, lang="en"),
 "4": dict(name="Neu-schnell", w=412, h=915, cpu=1, lang="pt"),
 "5": dict(name="Tablet", w=800, h=1280, cpu=3.7, lang="ru"),
 "6": dict(name="iPhone", w=390, h=844, cpu=1, lang="en", webkit=True),
 "7": dict(name="Telegram+Schrift130", w=412, h=800, cpu=3.7, lang="ru", text=1.3,
           ua="Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36 Telegram-Android/11.2"),
}
G = GROUPS[sys.argv[1]]; FROM = int(sys.argv[2]); UNTIL = int(sys.argv[3]); OUT = sys.argv[4]; LANG = sys.argv[5] if len(sys.argv) > 5 else G["lang"]
NUTS = os.environ.get("NUTS")  # "c" → Nuts-Kontinent c, FROM/UNTIL = Level
TMAX = float(os.environ.get("TMAX", "75")); EXTRA = open(os.path.join(HERE, "extra.js"), encoding="utf8").read()
os.makedirs(OUT, exist_ok=True); SITE = os.environ.get("SITE", os.path.join(HERE, "..", "capy", "site"))

CHECK = r"""
(() => { const F = window.__FIND = window.__FIND || []; const seen = {}; const S0 = () => window.__TT && window.__TT.S;
  const add = (cat, key, msg, extra) => { const S = S0(); const k = cat + '|' + key; if (seen[k]) { seen[k].n++; return; } seen[k] = { n: 1 };
    F.push(Object.assign({ cat, key, msg: String(msg).slice(0, 200), w: S ? S.wave | 0 : -1, t: Math.round(performance.now() / 1000), shot: 1 }, extra || {})); };
  const vis = e => { if (!e || e.hidden) return false; const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity < 0.05) return false; const r = e.getBoundingClientRect(); return r.width > 2 && r.height > 2; };
  const R = e => e.getBoundingClientRect(), inter = (a, b) => !(a.right <= b.left + 2 || a.left >= b.right - 2 || a.bottom <= b.top + 2 || a.top >= b.bottom - 2);
  const MODAL = ['ovIntro','ovAd','ovBandit','ovHackAd','ovHack','ovJoin','ovSign','ovOrders','ovPause','ovOver','ovCoachAd','ovGive','ovSettings','ovTilt','tutSum','sheet','ovCloud'];
  const OFFER = ['ovAd','ovHackAd','ovBandit','ovCoachAd'];
  let lastClose = -1e9, prevOpen = {};
  /* A2/A5: Lautstärkesprünge ohne Rampe */
  try { const sv = AudioParam.prototype.setValueAtTime; AudioParam.prototype.setValueAtTime = function (v, t) { try { const c = (window.__TT && null); if (this.defaultValue === 1 && this.maxValue > 1e30 && this.value !== 1 && v <= 2 && this.value <= 2 && Math.abs(v - this.value) > 0.12 && this.value > 0.02 && v > 0.02) { const st = (new Error().stack || '').split('\n')[2] || ''; add('A2', st.trim().slice(0, 80), `Lautstärke springt ${this.value.toFixed(2)}→${(+v).toFixed(2)} ohne Rampe`, { shot: 0 }); } } catch (e) {} return sv.apply(this, arguments); }; } catch (e) {}
  try { const d = Object.getOwnPropertyDescriptor(HTMLMediaElement.prototype, 'volume'); Object.defineProperty(HTMLMediaElement.prototype, 'volume', { get() { return d.get.call(this); }, set(v) { try { const o = d.get.call(this); if (!this.paused && Math.abs(v - o) > 0.1) add('A5', (this.currentSrc || '').split('/').pop().split('?')[0], `Lautstärke springt ${o.toFixed(2)}→${(+v).toFixed(2)}`, { shot: 0 }); } catch (e) {} d.set.call(this, v); } }); } catch (e) {}
  let n = 0; window.__ADD = add; window.__VIS = vis; window.__R = R; window.__INTER = inter; window.__MODAL = MODAL;
  setInterval(() => { try { const S = S0(); if (!S || !S.started) return; n++;
    /* B1: mehr als ein Pflichtfenster gleichzeitig */
    const open = MODAL.filter(id => vis(document.getElementById(id))); if (window.__tipBulb && window.__tipBulb.open) open.push('tipBulb');
    if (open.length > 1) add('B1', open.sort().join('+'), 'Mehrere Fenster gleichzeitig: ' + open.join(', '));
    /* D2: Angebot < 30 s nach dem letzten Fenster */
    const now = performance.now();
    for (const id of MODAL) { const o = open.includes(id); if (prevOpen[id] && !o) lastClose = now; if (o && !prevOpen[id] && OFFER.includes(id) && now - lastClose < 30000) add('D2', id + '@' + (S.wave | 0), `${id} nur ${((now - lastClose) / 1000).toFixed(1)} s nach dem letzten Fenster`); prevOpen[id] = o; }
    /* B4/B5: Sprechblasen/Pillen über Fenstern */
    const fl = ['buddy', 'coach', 'djSong', 'hackPill', 'tipBulb'].map(id => document.getElementById(id)).filter(e => vis(e) && !(e.id === 'buddy' && !e.classList.contains('on')));
    for (const f of fl) for (const id of open) { const m = document.getElementById(id); if (m && m !== f && !m.contains(f) && inter(R(f), R(m.firstElementChild || m))) add('B4', f.id + '>' + id, `${f.id} liegt über Fenster ${id}`); }
    /* B13/E1: Bedienknöpfe im Bild und nicht über dem Spielfeld */
    const bd = document.getElementById('board');
    if (!open.length && vis(bd)) for (const b of document.querySelectorAll('.deck button')) if (vis(b)) { const r = R(b);
      if (r.left < -1 || r.top < -1 || r.right > innerWidth + 1 || r.bottom > innerHeight + 1) add('E1', b.id || b.className, `Knopf ${b.id} ragt aus dem Bildschirm`);
      if (inter(r, R(bd))) add('B13', b.id || b.className, `Knopf ${b.id} liegt über dem Spielfeld`); }
    /* C1: Text ragt aus seiner Box (alle 4 Takte) */
    if (n % 16 === 0) { for (const e of document.querySelectorAll('body *')) { if (!e.childNodes.length || e.children.length > 2 || ['SCRIPT','STYLE','svg','CANVAS','IMG','path','g'].includes(e.tagName)) continue;
        if (parseFloat(getComputedStyle(e).fontSize) < 4) continue; const own = [...e.childNodes].some(c => c.nodeType === 3 && c.textContent.trim().length > 1); if (!own || !vis(e)) continue;
        const cs = getComputedStyle(e), clip = /hidden|clip|auto|scroll/.test(cs.overflowX + cs.overflowY) || cs.textOverflow === 'ellipsis';
        const txt = (e.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 60); if (!txt) continue;
        if (clip && (e.scrollWidth > e.clientWidth + 5 || (cs.overflowY !== 'auto' && cs.overflowY !== 'scroll' && cs.lineHeight !== '0px' && e.scrollHeight > e.clientHeight + 4))) add('C1', txt, `Text abgeschnitten: «${txt}» (${Math.max(e.scrollWidth - e.clientWidth, e.scrollHeight - e.clientHeight)}px)`);
        const r = R(e); if (r.width > 4 && (r.right > innerWidth + 2 || r.left < -2)) add('C1', 'vp:' + txt, `Text ragt aus dem Bildschirm: «${txt}»`); } }
    /* C7: englische Reste */
    try { const m = window.__i18n && window.__i18n.miss ? window.__i18n.miss() : null; if (m && m.length && window.__LANG !== 'en') for (const x of m.slice(-20)) add('C7', String(x).replace(/\d+/g, '#').slice(0, 60), 'Nicht übersetzt: ' + String(x).slice(0, 80), { shot: 0 }); } catch (e) {}
  } catch (e) {} }, 500);
})();
"""

TEXT130 = r"""(() => { const f = 1.3; const go = e => { try { if (e.nodeType !== 1 || e.dataset.ts) return; const cs = getComputedStyle(e); const s = parseFloat(cs.fontSize); if (s) { e.style.fontSize = (s * f) + 'px'; e.dataset.ts = 1; } } catch (x) {} };
  const all = () => document.querySelectorAll('body *').forEach(go); document.addEventListener('DOMContentLoaded', () => { all(); new MutationObserver(ms => ms.forEach(m => m.addedNodes.forEach(n => { go(n); n.querySelectorAll && n.querySelectorAll('*').forEach(go); }))).observe(document.body, { childList: true, subtree: true }); }); })();"""

INTERRUPT_OFF = "(()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});Object.defineProperty(document,'visibilityState',{configurable:true,get:()=>'hidden'});document.dispatchEvent(new Event('visibilitychange'));window.dispatchEvent(new Event('blur'));})()"
INTERRUPT_ON = "(()=>{delete document.hidden;delete document.visibilityState;document.dispatchEvent(new Event('visibilitychange'));window.dispatchEvent(new Event('focus'));})()"
AFTER = "(()=>{let ac=null;try{ac=window.AU&&AU.ac&&AU.ac();}catch(e){} const S=window.__TT.S; return {ac: ac?ac.state:'?', paused: !!S.paused, open: [...document.querySelectorAll('[id^=ov]')].filter(e=>!e.hidden&&getComputedStyle(e).display!=='none').map(e=>e.id)};})()"

def free_port():
    with socket.socket() as so: so.bind(("127.0.0.1", 0)); return so.getsockname()[1]

def main():
    port = free_port(); srv = subprocess.Popen(["python3", "-m", "http.server", str(port)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
    time.sleep(1.5); res = {"group": G, "lang": LANG, "from": FROM, "until": UNTIL, "waves": [], "netfail": [], "console": [], "interrupt": [], "shots": []}
    try:
        with sync_playwright() as p:
            if G.get("webkit"): br = p.webkit.launch()
            else: br = p.chromium.launch(**({"executable_path": "/usr/bin/google-chrome"} if os.path.exists("/usr/bin/google-chrome") else {}), args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
            kw = dict(viewport={"width": G["w"], "height": G["h"]}, device_scale_factor=1, is_mobile=not G.get("webkit") or True, has_touch=True)
            if G.get("ua"): kw["user_agent"] = G["ua"]
            if G.get("webkit"): kw["user_agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1"
            if G.get("webkit"): kw.pop("is_mobile")
            ctx = br.new_context(**kw)
            ctx.route("**/api/**", lambda r: r.fulfill(status=200, content_type="application/json", body="{}"))
            ctx.add_init_script(f"try{{localStorage.setItem('capy-reset','276');localStorage.setItem('tarnturm-tut','1');localStorage.setItem('tarnturm-terms','1');localStorage.setItem('capy-lang','{LANG}');}}catch(e){{}}")
            ctx.add_init_script(f"window.__LANG={json.dumps(LANG)};"); ctx.add_init_script(CHECK); ctx.add_init_script(EXTRA)
            if G.get("text"): ctx.add_init_script(TEXT130)
            pg = ctx.new_page()
            if os.environ.get("THROTTLE") and G["cpu"] > 1 and not G.get("webkit"):
                cdp = ctx.new_cdp_session(pg); cdp.send("Emulation.setCPUThrottlingRate", {"rate": G["cpu"]})
            pg.on("console", lambda m: res["console"].append(m.text[:160]) if m.type == "error" else None)
            pg.on("pageerror", lambda e: res["console"].append("PAGEERROR " + str(e)[:160]))
            pg.on("requestfailed", lambda r: res["netfail"].append((r.url.split("/")[-1][:60], str(r.failure)[:60])))
            pg.on("response", lambda r: res["netfail"].append((r.url.split("/")[-1][:60], r.status)) if r.status >= 400 else None)
            pg.clock.install()
            pg.goto(f"http://localhost:{port}/index.html?lang={LANG}")
            pg.clock.run_for(3000)
            pg.evaluate("window.__AT_BUYER = true"); BOT = at60.BOT; _a = "(x.innerText || '').toUpperCase().includes(p)"; assert BOT.count(_a) == 1
            BOT = BOT.replace(_a, "(((x.innerText || '').toUpperCase().includes(p)) || (()=>{try{const q=String(window.__i18n.T(p)).toUpperCase();return q!==p&&(x.innerText || '').toUpperCase().includes(q)}catch(e){return false}})())")
            pg.evaluate(BOT)
            if NUTS:
                pg.evaluate(f"window.__TT.startGame('{os.environ.get('MODE', 'chill')}', 31)"); pg.clock.run_for(3000)
                pg.evaluate(f"(()=>{{const S=window.__TT.S; S.inWave=false; S.signOpen={int(NUTS)}+1; document.getElementById('signNuts').click(); const n=window.__TT.S.nuts; if({FROM}>1){{n.lvl={FROM}-1; n.cleared={FROM}-1; window.__TT.S.wave=n.base+{FROM}-1; window.__TT.S.gold+=500*({FROM}-1);}}}})()")
            else:
                pg.evaluate(f"window.__TT.startGame('{os.environ.get('MODE', 'chill')}', {FROM})")
            wall0 = time.time(); last = -1; last_t = 0; shot_n = 0; done_int = set()
            while True:
                pg.clock.run_for(5000)
                pg.evaluate("(()=>{const c=document.getElementById('coach'),k=document.getElementById('coachSkip');if(c&&!c.hidden&&k&&!k.hidden&&!k.classList.contains('wait')&&window.__TT.S.coachHold){k.click();}})()")
                pg.evaluate("(()=>{const g=document.querySelector('#ovHkTips:not([hidden]) .htGo');if(g&&!g.disabled)g.click();const c=document.getElementById('ovCoachAd');if(c&&!c.hidden){const b=[...c.querySelectorAll('button')].find(b=>b.offsetParent);if(b)b.click();}})()")
                pg.evaluate("(()=>{const h=document.getElementById('celHost');if(h&&h.classList.contains('tap')){const t=h.querySelector('.celTap');if(t)t.click();else h.click();}const S=window.__TT.S;if(S&&S.started&&!S.over&&S.lives<4)S.lives=6;const nb=document.getElementById('nrBack');})()")
                pg.evaluate("(()=>{const o=document.getElementById('ovPause');if(o&&!o.hidden){const b=[...o.querySelectorAll('button')].find(b=>b.offsetParent);if(b)b.click();}})()")
                pg.evaluate("(()=>{const b=[...document.querySelectorAll('.pBtn.pUp')].find(b=>b.offsetParent);if(b)b.click();})()")   # Umfrage beantworten
                pg.evaluate("(()=>{const A=window.__AT;if(!A)return;const t=performance.now();const IDS={intro:'ovIntro',ad:'ovAd',bandit:'ovBandit',hackAd:'ovHackAd',orders:'ovOrders',join:'ovJoin',sign:'ovSign',give:'ovGive',cloud:'ovCloud'};for(const k in IDS){const o=A.open[k];if(!o||t-o<20000)continue;const r=document.getElementById(IDS[k]);if(!r||r.hidden)continue;const bs=[...r.querySelectorAll('button,.btn,[role=button]')].filter(e=>e.offsetParent!==null&&!e.disabled);const b=bs.find(e=>e.classList.contains('btn-accent'))||bs[0];if(b){A.ev.push({t,k:'bot',e:'fallback:'+k+':'+(b.innerText||'').trim().slice(0,20),wave:window.__TT.S.wave});b.click();}}})()")   # Rückfall: Fenster > 20 s offen → ersten Knopf drücken
                # Screenshots für neue Funde
                for f in pg.evaluate("(window.__FIND||[]).filter(f=>f.shot===1).map((f,i)=>(f.shot=2,f))"):
                    if shot_n < 60:
                        fn = f"{f['cat']}_W{f['w']}_{shot_n:02d}.jpg"; shot_n += 1
                        try: pg.screenshot(path=os.path.join(OUT, fn), type="jpeg", quality=55, scale="css"); res["shots"].append({"file": fn, "cat": f["cat"], "msg": f["msg"]})
                        except Exception: pass
                st = pg.evaluate("(()=>{const S=window.__TT.S;return {w: S.nuts ? S.nuts.lvl : S.wave, nuts: !!S.nuts, over: !!S.over, t: performance.now(), inW: !!S.inWave}})()")
                # Unterbrechung (App-Wechsel) alle 10 Wellen in der Wellenpause
                if st["w"] % 10 == 5 and st["w"] not in done_int and st["inW"]:
                    done_int.add(st["w"]); pg.evaluate(INTERRUPT_OFF); pg.clock.run_for(5000); pg.evaluate(INTERRUPT_ON); pg.clock.run_for(3000)
                    a = pg.evaluate(AFTER); a["w"] = st["w"]; res["interrupt"].append(a)
                if st["w"] == last and st["t"] - last_t > 4 * 60000:
                    res["stall"] = pg.evaluate("(()=>{const S=window.__TT.S;return {w:S.wave,inWave:S.inWave,mon:S.monsters.length,intro:!!S.intro,paused:!!S.paused,open:Object.keys(window.__AT.open),vis:[...document.querySelectorAll('[id^=ov]')].filter(e=>!e.hidden&&getComputedStyle(e).display!=='none').map(e=>e.id)}})()")
                    pg.screenshot(path=os.path.join(OUT, f"D1_haenger_W{last}.jpg"), type="jpeg", quality=55, scale="css"); print("HAENGT", res["stall"], flush=True); break
                if st["w"] != last:
                    last_t = st["t"]; last = st["w"]; res["waves"].append({"w": last, "real": round(time.time() - wall0)}); print(f"G{sys.argv[1]} W{last:3d} real {time.time()-wall0:5.0f}s", flush=True)
                    json.dump({**res, "find": pg.evaluate("window.__FIND||[]"), "partial": True}, open(os.path.join(OUT, "result.json"), "w"), ensure_ascii=False)
                if st["w"] > UNTIL or st["over"] or (NUTS and not st["nuts"]) or time.time() - wall0 > TMAX * 60: break
            res["find"] = pg.evaluate("window.__FIND||[]"); res["at"] = pg.evaluate("({ev:(window.__AT.ev||[]).slice(-400),err:window.__AT.err})"); res["end"] = st
            br.close()
    finally:
        os.killpg(srv.pid, signal.SIGTERM)
    json.dump(res, open(os.path.join(OUT, "result.json"), "w"), ensure_ascii=False, indent=0)
    print("fertig", OUT, len(res.get("find", [])), "Funde")

if __name__ == "__main__":
    main()
