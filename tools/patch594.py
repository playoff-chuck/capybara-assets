#!/usr/bin/env python3
# V594 (Nachtplan 11.11. Punkt 2, Martin «Ja» 01:44): Metrik-Erfassung. Jedes Ereignis mit Spieler-Nr. (uid), Kanal (ch: ?src= / ru / app / pwa / web)
# und team; Test-Browser (navigator.webdriver) senden nichts. Neue Ereignisse: tut (Lektion n + Sekunden), tutskip, cert, hack (shown/accept/decline/
# win/lose/abort + Einsatz), set (Musik/Ton/Sprache), buy, spec, cancel, ad (seen/free/buy/later), death (Welle, Ursache, wie oft dort), restart,
# perf (FPS < 40), Ladezeit im start. Admin-Spielerliste: neuer Knopf «Analyse» (/admin/stats, nur echte Spieler).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V593";', 'const GAME_VER = "V594";')
# 1) Senden: Test-Browser aus, uid/ch/team mitschicken
rep('''    const ON = window.__evForce || /(^|\\.)playcapybarasquad\\.com$|sslip\\.io$/.test(location.hostname);''',
    '''    const ON = (window.__evForce || /(^|\\.)playcapybarasquad\\.com$|(^|\\.)capybarasquad\\.ru$|sslip\\.io$/.test(location.hostname)) && (!navigator.webdriver || window.__evForce === 2);   /* V594: Test-Browser zählen nicht */''')
rep('''    function body() { return JSON.stringify({ ver: GAME_VER, sess, dev: dev(), plat, br, sw: screen.width | 0, sh: screen.height | 0, mem: navigator.deviceMemory || null, ev: q.splice(0, 12) }); }''',
    '''    const ch = (() => { try { const v = new URLSearchParams(location.search).get("src"); if (v && /^[a-z0-9_-]{1,12}$/i.test(v)) localStorage.setItem("capy-src", v.toLowerCase()); const st = localStorage.getItem("capy-src"); if (st) return st; } catch (e) {}
      if (/\\.ru$/.test(location.hostname)) return "ru"; if (/^android-app:/.test(document.referrer || "")) return "app"; try { if (matchMedia("(display-mode: standalone)").matches) return "pwa"; } catch (e) {} return "web"; })();   /* V594 */
    const uidV = () => { try { return capyUid(); } catch (e) { return ""; } }, teamV = () => { try { return !!capyMe(); } catch (e) { return false; } };
    function body() { return JSON.stringify({ ver: GAME_VER, sess, dev: dev(), plat, br, sw: screen.width | 0, sh: screen.height | 0, mem: navigator.deviceMemory || null, uid: uidV(), ch, team: teamV(), ev: q.splice(0, 12) }); }''')
rep('''    function push(k, extra) { if (q.length > 40) return; q.push(Object.assign({ k, w: wave(), scr: scr(), m: mins() }, extra || {})); }''',
    '''    let fT = 0;
    function push(k, extra) { if (q.length > 60) return; q.push(Object.assign({ k, w: wave(), scr: scr(), m: mins() }, extra || {})); if (q.length >= 12 && !fT) fT = setTimeout(() => { fT = 0; flush(false); }, 1500); }''')
rep('''    push("start"); setTimeout(() => flush(false), 4000);''',
    '''    setTimeout(() => { let ld = 0; try { const n = performance.getEntriesByType("navigation")[0]; ld = Math.round((n && (n.loadEventEnd || n.domContentLoadedEventEnd)) || performance.now()); } catch (e) {}
      let lang = "en"; try { lang = LS.get("capy-lang") || I18N.lang || "en"; } catch (e) {}
      push("start", { d: { ld, mu: LS.get("tarnturm-music") !== "0" ? 1 : 0, sn: LS.get("tarnturm-mute") === "1" ? 0 : 1, lang } }); flush(false); }, 4000);   /* V594: Ladezeit, Musik, Ton, Sprache */''')
# 2) Beobachter für die neuen Ereignisse
rep('''    window.__evLog = { q, flush, push, sess, plat, br, scr };''',
    '''    /* V594: Metrik-Beobachter (Trichter, Boss-Hack, Bedienung, Frust, Technik) */
    try { const P = { tut: false, step: -1, t0: 0, cert: false, over: false, S: null, died: 0, pill: false, ad: false, c: null, g: 0, wp: 0, why: "",
        set: [LS.get("tarnturm-music"), LS.get("tarnturm-mute"), LS.get("capy-lang")], fr: 0, ft: performance.now() };
      const vis = id => { const e = document.getElementById(id); return !!(e && !e.hidden && e.offsetParent !== null); };
      const cnt = () => ({ ton: S.tons | 0, mix: S.mixers | 0, snipe: S.snipes | 0, tesla: S.teslas | 0, chomp: S.chomps | 0, lock: S.locks | 0, wolf: S.wolves | 0 });
      const wpn = () => { try { return [...S.towers.values()].reduce((a, t) => a + ((t.w && t.w.length) || 0), 0); } catch (e) { return 0; } };
      try { const _te = tutEnd; tutEnd = function (skipped) { try { if (skipped && TUT.on) push("tutskip", { d: { n: (TUT.step | 0) + 1, s: Math.round((performance.now() - P.t0) / 1000) } }); } catch (e) {} return _te.apply(this, arguments); }; } catch (e) {}
      try { const _sd = startDuel; startDuel = function (keep) { const r = _sd.apply(this, arguments); try { if (!keep) push("hack", { d: { r: "accept", st: HK.stake | 0, c: HK.coach ? 1 : 0 } }); } catch (e) {} return r; }; } catch (e) {}
      try { const _hf = hkFinish; hkFinish = function () { try { const mine = HK.cells.filter(c => c === HK.me).length; if (mine !== 6) push("hack", { d: { r: mine > 6 ? "win" : "lose", st: HK.stake | 0, c: HK.coach ? 1 : 0 } }); } catch (e) {} return _hf.apply(this, arguments); }; } catch (e) {}
      try { const _ch = closeHack; closeHack = function () { try { const ph = HK.phase; if (ph === "bet") push("hack", { d: { r: "decline", c: HK.coach ? 1 : 0 } }); else if (ph && ph !== "done" && ph !== "off") push("hack", { d: { r: "abort", ph, c: HK.coach ? 1 : 0 } }); } catch (e) {} return _ch.apply(this, arguments); }; } catch (e) {}
      try { const _go = gameOver; gameOver = function (why) { try { P.why = String(why || "").slice(0, 24); } catch (e) {} return _go.apply(this, arguments); }; } catch (e) {}
      document.addEventListener("click", e => { try { const t = e.target && e.target.closest ? e.target : null; if (!t) return;
        if (t.closest("#buildCancel")) push("cancel", { d: { b: (document.body.className.match(/\\b(snipe|mix|tesla|build)\\w*/) || [""])[0].slice(0, 16) } });
        else if (t.closest("#adFree")) push("ad", { d: { a: "free" } }); else if (t.closest("#adBuy")) push("ad", { d: { a: "buy" } }); else if (t.closest("#adLater")) push("ad", { d: { a: "later" } }); } catch (x) {} }, true);
      const fr = () => { P.fr++; requestAnimationFrame(fr); }; requestAnimationFrame(fr);
      setInterval(() => { try { const now = performance.now();
        if (typeof TUT !== "undefined") { if (TUT.on) { if (!P.tut) { P.tut = true; P.t0 = now; P.step = -1; } if (TUT.step !== P.step) { P.step = TUT.step; push("tut", { d: { n: (TUT.step | 0) + 1, s: Math.round((now - P.t0) / 1000) } }); } } else P.tut = false; }
        if (!P.cert) { const ts = document.getElementById("tutSum"); if (ts && !ts.hidden && ts.querySelector(".cert")) { P.cert = true; push("cert", { d: { s: P.t0 ? Math.round((now - P.t0) / 1000) : 0 } }); } }
        const st = [LS.get("tarnturm-music"), LS.get("tarnturm-mute"), LS.get("capy-lang")];
        if (st.join("|") !== P.set.join("|")) { const d = {}; if (st[0] !== P.set[0]) d.music = st[0] === "0" ? 0 : 1; if (st[1] !== P.set[1]) d.mute = st[1] === "1" ? 1 : 0; if (st[2] !== P.set[2]) d.lang = String(st[2] || "").slice(0, 5); P.set = st; push("set", { d }); }
        const pill = vis("hackPill"); if (pill && !P.pill) push("hack", { d: { r: "shown" } }); P.pill = pill;
        const ad = vis("ovAd"); if (ad && !P.ad) push("ad", { d: { a: "seen" } }); P.ad = ad;
        if (typeof S === "undefined" || !S) return;
        if (S !== P.S) { if (P.died) push("restart", { d: { pw: P.died } }); P.died = 0; P.S = S; P.over = !!S.over; P.c = null; }
        if (S.started && !P.over && S.over && !S.replay) { const w = S.wave | 0; let n = 1; try { const m = JSON.parse(LS.get("capy-ev-dw") || "{}"); n = m[w] = (m[w] || 0) + 1; LS.set("capy-ev-dw", JSON.stringify(m)); } catch (e) {}
          push("death", { d: { why: P.why || "?", n, nz: S.nuts ? 1 : 0 } }); P.died = w || 1; P.why = ""; }
        P.over = !!S.over;
        if (S.started && !S.over && !S.replay) { const c = cnt(), g = S.gold | 0, wp = wpn();
          if (P.c) { const paid = g < P.g; for (const k in c) { if (c[k] < P.c[k]) push("spec", { d: { k } }); else if (c[k] > P.c[k] && paid) push("buy", { d: { k } }); } if (wp > P.wp && paid) push("buy", { d: { k: "weapon" } }); }
          P.c = c; P.g = g; P.wp = wp; }
        if (now - P.ft >= 60000) { const fps = Math.round(P.fr * 1000 / (now - P.ft)); if (!document.hidden && S.started && !S.paused && !S.over && fps < 40) push("perf", { d: { fps } }); P.fr = 0; P.ft = now; }
      } catch (e) {} }, 500);
      document.addEventListener("visibilitychange", () => { P.fr = 0; P.ft = performance.now(); });
    } catch (e) {}
    window.__evLog = { q, flush, push, sess, plat, br, scr, ch };''')
# 3) Admin: Reiter «Analyse»
rep('''    let h = `<div class="aSum"><div><b>${REAL.length}</b>''',
    '''    let h = `<button type="button" class="aStat" style="display:block;width:100%;margin:0 0 10px;padding:9px;border:2px solid #3a2414;border-radius:12px;background:#ffd84d;font:inherit;font-weight:800;color:#3a2414">📊 Analyse · Trichter, Ausstiege, Boss-Hack</button><div class="aSum"><div><b>${REAL.length}</b>''')
rep('''  body.addEventListener("click", e => { const a = e.target.closest(".aAll");''',
    '''  async function renderStats(days) { days = days || 30; scrollY = body.scrollTop; back.hidden = false; info.textContent = `Analyse · ${days} Tage · nur echte Spieler`; body.innerHTML = '<div class="aMsg">Lade Analyse …</div>';   /* V594 */
    let j = null; try { const r = await fetch(API_BASE + "/admin/stats", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ token: tokenGet(), days }), cache: "no-store" }); j = r.ok ? await r.json() : null; } catch (e) {}
    if (!j || !j.ok) { body.innerHTML = '<div class="aMsg">Analyse nicht verfügbar (Server oder Schlüssel).</div>'; return; }
    const kv = (k, v) => `<div class="aKV"><span>${esc(k)}</span><b>${v}</b></div>`, sec = (t, rows) => `<div class="aSec">${t}</div><div class="aCard">${rows.length ? rows.join("") : kv("–", "noch keine Daten")}</div>`;
    const pc = (a, b) => b ? Math.round(100 * a / b) + " %" : "–", obj = o => Object.entries(o || {}).sort((a, b) => b[1] - a[1]).map(([k, v]) => kv(k, num(v)));
    const HK_DE = { shown: "angeboten", accept: "angenommen", decline: "abgelehnt", win: "gewonnen", lose: "verloren", abort: "abgebrochen" };
    let h = `<div class="aSum"><div><b>${j.players}</b><small>Spieler</small></div><div><b>${num(j.events)}</b><small>Ereignisse</small></div><div><b>${j.days}</b><small>Tage</small></div></div>`;
    h += `<div style="display:flex;gap:6px;margin:0 0 10px">${[1, 7, 30, 90].map(d => `<button type="button" class="aDays" data-d="${d}" style="flex:1;padding:7px;border:2px solid #3a2414;border-radius:10px;background:${d === days ? "#ffd84d" : "#fff6e3"};font:inherit;color:#3a2414">${d} T</button>`).join("")}</div>`;
    h += sec("TRICHTER", (j.funnel || []).map(f => kv(f.step, `${num(f.n)} · ${f.pct} %`)));
    h += sec("TUTORIAL ÜBERSPRUNGEN BEI", Object.entries(j.skipAt || {}).map(([k, v]) => kv("Lektion " + k, num(v))));
    h += sec("AUSSTIEG OHNE RÜCKKEHR (> 30 min)", (j.exits || []).map(x => kv(x.where, num(x.n))));
    const hk = j.hack || {}; h += sec("BOSS-HACK", Object.keys(HK_DE).filter(k => hk[k]).map(k => kv(HK_DE[k], num(hk[k]))).concat(hk.shown ? [kv("Annahme-Quote", pc(hk.accept || 0, hk.shown))] : []).concat((hk.win || hk.lose) ? [kv("Sieg-Quote", pc(hk.win || 0, (hk.win || 0) + (hk.lose || 0)))] : []));
    h += sec("TODE NACH WELLE", (j.deathsByWave || []).map(x => kv("Welle " + x[0], num(x[1]))));
    const mo = j.musicOff || {}, rt = j.return || {};
    h += sec("BEDIENUNG", [kv("Musik aus", mo.of ? `${mo.off} von ${mo.of} · ${pc(mo.off, mo.of)}` : "–")].concat(obj(j.set).map(x => x.replace("<span>", "<span>umgestellt: ").replace("music=0", "Musik aus").replace("music=1", "Musik an").replace("mute=1", "Ton aus").replace("mute=0", "Ton an").replace("lang=", "Sprache "))));
    h += sec("WIEDERKEHR", [kv("Tag 1", rt.d1of ? `${rt.d1} von ${rt.d1of} · ${pc(rt.d1, rt.d1of)}` : "–"), kv("Tag 7", rt.d7of ? `${rt.d7} von ${rt.d7of} · ${pc(rt.d7, rt.d7of)}` : "–")]);
    h += sec("KAUF · SPEZIAL · ANGEBOTE", obj(j.buy).map(x => x.replace("<span>", "<span>Kauf ")).concat(obj(j.spec).map(x => x.replace("<span>", "<span>Einsatz "))).concat(obj(j.ad).map(x => x.replace("<span>", "<span>Angebot "))));
    const pf = j.perf || {}, lm = j.loadMs || {};
    h += sec("TECHNIK · KANAL", [kv("Ruckeln (< 40 FPS)", pf.n ? `${pf.n}× · Ø ${pf.avgFps} FPS` : "keins"), kv("Ladezeit (Median)", lm.median ? (lm.median / 1000).toFixed(1) + " s" : "–")].concat(obj(j.channels)));
    h += '<div class="aMsg" style="font-size:12px">Zählt ab V594 (vorher ohne Spieler-Nr.). Ohne Team, Tests und Dev-Geräte.</div>';
    body.innerHTML = h; body.scrollTop = 0; }
  body.addEventListener("click", e => { const st = e.target.closest(".aStat"); if (st) { try { snd("uiTap"); } catch (er) {} renderStats(30); return; } const dd = e.target.closest(".aDays"); if (dd) { renderStats(+dd.dataset.d); return; } const a = e.target.closest(".aAll");''')
open(dst, "w", encoding="utf-8").write(s)
print("ok V594")
