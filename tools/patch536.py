#!/usr/bin/env python3
"""V536 (Martin 09.11. 21:16–21:19):
1) Karten-Intro: gelber Zielpfeil «River Bank ▶» weg (nur im Intro-Flug).
2) Ankunftsbild (Rosie + Blue): nur noch EIN Zoom – der Kreis aus dem Punkt öffnet sich halb so schnell (1,4 s → 2,8 s),
   das Bild selbst zoomt nicht mehr nach. Zeiten danach verlängert, damit das Bild gleich lang voll zu sehen ist.
3) App-Icon nach Logo C1 (icons/*.png neu, Manifest mit ?v=536).
4) Admin-Knopf nur auf Martins Handy (uid M2HL-KCQH bzw. Dev-Modus) links neben dem Ton-Knopf im Startmenü:
   Spielerliste mit laufender Nummer, Fortschritt, Gerät; Antippen → Details (Spielzeit, Bildschirmzeit, Tode …).
   Jedes Gerät meldet dafür sein Spielprofil an /api/player (Server-Patch tools/api536.py).
Aufruf: python3 tools/patch536.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)

rep('const GAME_VER = "V535";', 'const GAME_VER = "V536";')
rep('<link rel="manifest" href="manifest.webmanifest">', '<link rel="manifest" href="manifest.webmanifest?v=536">')
rep('<link rel="apple-touch-icon" href="icons/icon-192.png">', '<link rel="apple-touch-icon" href="icons/icon-192.png?v=536">')

# 1) Zielpfeil im Intro aus
rep('function flyPlane(a, b, ms) {', 'function flyPlane(a, b, ms, nod) {')
rep('destPtr(b, t < 1 ? x : -1, y);', 'destPtr(b, t < 1 && !nod ? x : -1, y);   /* V536: nod = ohne Zielpfeil */')
rep('flyPlane([1.04, .2], RB, 4600); });', 'flyPlane([1.04, .2], RB, 4600, true); });')

# 2) Ankunftsbild: ein Zoom, halb so schnell
rep('#ovMap .mapArrive.fromPt.on{clip-path:circle(150vmax at var(--ox,50%) var(--oy,50%))}',
    '#ovMap .mapArrive.fromPt.on{clip-path:circle(150vmax at var(--ox,50%) var(--oy,50%));transition:clip-path 2.8s cubic-bezier(.55,0,.3,1)}')
rep('#ovMap .mapArrive.fromPt img{transform-origin:var(--ox,50%) var(--oy,50%);transform:scale(1.35);transition:transform 4.5s cubic-bezier(.2,.7,.3,1)}',
    '#ovMap .mapArrive.fromPt img{transform:none;transition:none}')
rep('#ovMap .mapArrive.fromPt.on img{transform:scale(1)}', '#ovMap .mapArrive.fromPt.on img{transform:none}')
rep('object-position:50% 60%;transform:scale(1.08);transition:transform 4.5s ease-out}', 'object-position:50% 60%;transform:none;transition:none}')
rep('#ovMap .mapArrive.on img{transform:scale(1)}', '#ovMap .mapArrive.on img{transform:none}')
rep('at(9000, () => { try { arr && arr.classList.remove("on"); } catch (e) {} });\n      at(10600, hide); }',
    'at(10400, () => { try { arr && arr.classList.remove("on"); } catch (e) {} });   /* V536: Öffnen 2,8 s statt 1,4 s */\n      at(12000, hide); }')
rep('at(11800 - sk, hide); }', 'at(13200 - sk, hide); }   /* V536: +1,4 s für das langsamere Öffnen */')

# 3+4) Spielprofil + Admin
ADM = r'''
/* V536: Spielprofil je Gerät (für Martins Admin-Übersicht) + Admin-Knopf */
try { (() => {
  const LSJ = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k) || "null"); return v == null ? d : v; } catch (e) { return d; } };
  const LSS = (k, v) => { try { localStorage.setItem(k, typeof v === "string" ? v : JSON.stringify(v)); } catch (e) {} };
  const playing = () => !!(S && S.started && !S.over && !S.testRun && !S.replay);
  /* Bildschirmzeit (App sichtbar) + beste erreichte Welle */
  setInterval(() => { try { if (document.hidden) return; LSS("capy-scr", String((+localStorage.getItem("capy-scr") || 0) + 10));
      if (playing() && !S.nuts && (S.wave || 0) > (+localStorage.getItem("capy-maxw") || 0)) LSS("capy-maxw", String(S.wave | 0)); } catch (e) {} }, 10000);
  /* Tode zählen */
  const _goP = gameOver; gameOver = function (why) { try { if (S && S.started && !S.over && !S.testRun && !S.replay) { const w = String(why || "");
        if (!/World tour complete/i.test(w)) { const D = LSJ("capy-deaths", {}); D.n = (D.n || 0) + (S.nuts ? 0 : 1); D.nz = (D.nz || 0) + (S.nuts ? 1 : 0);
          const k = /stack|ceiling/i.test(w) ? "blk" : /weed/i.test(w) ? "weed" : "mon"; D.by = D.by || {}; D.by[k] = (D.by[k] || 0) + 1; D.lw = S.wave | 0; D.lt = Date.now(); LSS("capy-deaths", D); } } } catch (e) {}
    const r = _goP.apply(this, arguments); setTimeout(() => profSend(false, true), 1500); return r; };
  function profBuild() { const L = sqLife(), D = LSJ("capy-deaths", {}), st = starsAll(), dv = devInfo().split(" | ");
    let cur = null; try { if (S && S.started && !S.over) cur = S.nuts ? { nz: 1, c: S.nuts.c, lv: (S.nuts.cleared || 0) + 1 } : { w: S.wave | 0 }; } catch (e) {}
    let nzs = null; try { const d = JSON.parse(LS.get("capy-nz-save") || "null"); if (d && d.nuts) nzs = { c: d.nuts.c, lv: (d.nuts.cleared || 0) + 1 }; } catch (e) {}
    let msnD = 0; try { msnD = (MSN && MSN.d && MSN.d.length) || 0; } catch (e) {}
    let dly = 0; try { dly = (DAILY && DAILY.streak) || 0; } catch (e) {}
    let tz = ""; try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; } catch (e) {}
    return { uid: capyUid(), ver: GAME_VER, nm: LS.get("tarnturm-nick") || "", hero: heroKey(), of: outfitSel(heroKey()), lang: I18N.lang || "en",
      os: dv[0] || "", app: dv[1] || "", scr: dv[2] || "", loc: dv[3] || "", tz,
      cp: window.__cpGet ? window.__cpGet() : 0, bw: Math.max(getBest("pro") || 0, +localStorage.getItem("capy-maxw") || 0), cur, nzs,
      nzb: [0, 1, 2, 3].map(c => { try { return nzBest(c); } catch (e) { return 0; } }),
      st: Object.values(st).reduce((a, b) => a + (+b || 0), 0), pl: Object.keys(st).length, md: Object.keys((ALB && ALB.got) || {}).length,
      lv: (() => { try { return sqLevel(); } catch (e) { return 1; } })(), xp: (() => { try { return sqXP(); } catch (e) { return 0; } })(), ms: msnD, dly,
      fr: +localStorage.getItem("capy-squad-n") || 0, k: L.k || 0, l: L.l || 0, w: L.w || 0, r: L.r || 0, t: Math.round(L.t || 0),
      scrT: +localStorage.getItem("capy-scr") || 0, d: D.n || 0, dnz: D.nz || 0, dby: D.by || {}, dlw: D.lw || 0,
      tut: localStorage.getItem("tarnturm-tut") === "1" ? 1 : 0, dev: localStorage.getItem("tarnturm-dev") === "1" ? 1 : 0, cs: !!localStorage.getItem("capy-cloudT") }; }
  let lastSend = 0;
  function profSend(start, force) { try { if (!force && !start && Date.now() - lastSend < 60000) return; lastSend = Date.now(); const b = profBuild(); if (start) b.start = true;
      fetch(API_BASE + "/player", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(b), keepalive: true }).catch(() => {}); } catch (e) {} }
  setTimeout(() => profSend(true), 6000);
  setInterval(() => { if (!document.hidden && playing()) profSend(false); }, 120000);
  document.addEventListener("visibilitychange", () => { if (document.hidden) profSend(false, true); });
  window.__prof = profBuild;

  /* Admin-Knopf + Übersicht (nur Martin) */
  if (!capyMe()) return;
  const st = document.createElement("style"); st.textContent = `
#stAdm{position:fixed;top:calc(env(safe-area-inset-top,0px) + 12px);right:calc(env(safe-area-inset-right,0px) + 66px);width:44px;height:44px;min-width:0;min-height:0;padding:0;border-radius:50%;border:2px solid #3a2414;background:#fff6e6;color:#3a2414;display:grid;place-items:center;z-index:60;box-shadow:0 3px 0 #3a2414;cursor:pointer}
#stAdm svg{width:24px;height:24px}#ovStart[hidden]~#stAdm,#stAdm[hidden]{display:none!important}
body:has(.overlay.joinOv:not([hidden])) #stAdm,body:has(#ovDaily:not([hidden])) #stAdm,body:has(#ovSettings:not([hidden])) #stAdm{display:none!important}
#ovAdm{position:fixed;inset:0;z-index:9500;background:#f6ead2;color:#3a2414;display:flex;flex-direction:column;font-family:"Baloo 2",Nunito,system-ui,sans-serif}
#ovAdm[hidden]{display:none!important}
#ovAdm .aHead{flex:none;display:flex;align-items:center;gap:8px;padding:calc(env(safe-area-inset-top,0px) + 10px) 12px 10px;background:#3a2414;color:#fff6e6}
#ovAdm .aHead h2{flex:1;margin:0;font:400 24px/1 Bangers,Oswald,system-ui;letter-spacing:.04em}
#ovAdm .aHead small{display:block;font:600 12px/1.2 "Baloo 2",Nunito,system-ui;opacity:.8;letter-spacing:0}
#ovAdm .aBtn{flex:none;width:40px;height:40px;min-height:0;padding:0;border-radius:50%;border:2px solid #fff6e6;background:transparent;color:#fff6e6;font:700 20px/1 system-ui;display:grid;place-items:center}
#ovAdm .aBody{flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding:10px 10px calc(env(safe-area-inset-bottom,0px) + 24px)}
#ovAdm .aBody::-webkit-scrollbar{display:none}
#ovAdm .aRow{display:grid;grid-template-columns:38px 1fr auto;gap:2px 10px;align-items:center;background:#fffaf0;border:2px solid #3a2414;border-radius:14px;padding:8px 10px;margin:0 0 8px;box-shadow:0 2px 0 #3a2414;width:100%;text-align:left;color:inherit;font:inherit;min-height:0}
#ovAdm .aNo{grid-row:1/3;font:400 20px/1 Bangers,Oswald,system-ui;text-align:center;color:#8a5a2b}
#ovAdm .aNm{font:700 16px/1.2 "Baloo 2",Nunito,system-ui;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#ovAdm .aW{font:400 18px/1 Bangers,Oswald,system-ui;text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
#ovAdm .aSub{grid-column:2/4;font:500 12px/1.25 "Baloo 2",Nunito,system-ui;color:#6b4a2b;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#ovAdm .aDot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#bba68a;margin-right:5px;vertical-align:1px}#ovAdm .aDot.on{background:#3fae3f}#ovAdm .aDot.day{background:#f0b52a}
#ovAdm .aSum{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:0 0 10px}
#ovAdm .aSum div{background:#fffaf0;border:2px solid #3a2414;border-radius:12px;padding:6px 4px;text-align:center}
#ovAdm .aSum b{display:block;font:400 22px/1 Bangers,Oswald,system-ui}#ovAdm .aSum small{font:600 11px/1.1 "Baloo 2",Nunito,system-ui;color:#6b4a2b}
#ovAdm .aSec{font:400 17px/1 Bangers,Oswald,system-ui;letter-spacing:.05em;color:#8a5a2b;margin:14px 2px 6px}
#ovAdm .aCard{background:#fffaf0;border:2px solid #3a2414;border-radius:14px;padding:4px 12px;box-shadow:0 2px 0 #3a2414}
#ovAdm .aKV{display:grid;grid-template-columns:44% 1fr;gap:8px;padding:7px 0;border-bottom:1px dashed #d9c3a0;font:500 14px/1.3 "Baloo 2",Nunito,system-ui}
#ovAdm .aKV:last-child{border-bottom:0}#ovAdm .aKV span{color:#6b4a2b}#ovAdm .aKV b{font-weight:700;word-break:break-word;font-variant-numeric:tabular-nums}
#ovAdm .aMsg{text-align:center;padding:40px 16px;font:600 15px/1.4 "Baloo 2",Nunito,system-ui;color:#6b4a2b}`;
  document.head.appendChild(st);
  const btn = document.createElement("button"); btn.id = "stAdm"; btn.type = "button"; btn.setAttribute("translate", "no"); btn.setAttribute("aria-label", "Admin");
  btn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="8" r="3.4" fill="#3a2414"/><path d="M2.5 19c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6z" fill="#3a2414"/><circle cx="17" cy="9" r="2.6" fill="#8a5a2b"/><path d="M14.6 13.4c.7-.3 1.5-.4 2.4-.4 2.9 0 4.9 2 4.9 5h-5.2c0-1.8-.8-3.4-2.1-4.6z" fill="#8a5a2b"/></svg>';
  const ov = document.createElement("div"); ov.id = "ovAdm"; ov.hidden = true; ov.setAttribute("translate", "no");
  ov.innerHTML = '<div class="aHead"><button class="aBtn aBack" type="button" hidden>‹</button><h2>SPIELER<small class="aInfo">lädt …</small></h2><button class="aBtn aRef" type="button">↻</button><button class="aBtn aX" type="button">✕</button></div><div class="aBody"></div>';
  document.body.appendChild(ov); document.body.appendChild(btn);
  setInterval(() => { try { const so = document.getElementById("ovStart"); btn.hidden = !(so && !so.hidden) || !ov.hidden; } catch (e) {} }, 300);
  const body = ov.querySelector(".aBody"), info = ov.querySelector(".aInfo"), back = ov.querySelector(".aBack");
  let LIST = [], NOW = Date.now(), scrollY = 0;
  const esc = v => String(v == null ? "" : v).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const num = n => (+n || 0).toLocaleString("de-DE");
  const dur = sec => { sec = Math.round(+sec || 0); const h = Math.floor(sec / 3600), m = Math.round((sec % 3600) / 60); return h ? `${h} h ${m} min` : `${m} min`; };
  const ago = t => { const s = Math.max(0, (NOW - t) / 1000); if (s < 90) return "gerade eben"; if (s < 3600) return `vor ${Math.round(s / 60)} min`; if (s < 86400) return `vor ${Math.round(s / 3600)} h`; const d = Math.round(s / 86400); return d === 1 ? "vor 1 Tag" : `vor ${d} Tagen`; };
  const dt = t => { const d = new Date(t), z = n => String(n).padStart(2, "0"); return `${z(d.getDate())}.${z(d.getMonth() + 1)}.${String(d.getFullYear()).slice(2)} ${z(d.getHours())}:${z(d.getMinutes())}`; };
  const KONT = ["Südamerika", "Afrika", "Asien", "Nordamerika", "Antarktis"], NZW = ["Südamerika", "Afrika", "Asien", "Nordamerika"];
  const where = w => { w = +w || 0; if (w < 1) return "noch nicht gestartet"; const c = Math.min(4, Math.floor((w - 1) / 30)), i = Math.min(5, Math.floor(((w - 1) % 30) / 5)); let pl = ""; try { pl = CONTS[c][2][i].toLowerCase().replace(/\b\w/g, m => m.toUpperCase()); } catch (e) {} return KONT[c] + (pl ? " · " + pl : ""); };
  const nowWave = d => (d.cur && d.cur.w) || Math.max(d.cp || 0, 0);
  const devShort = d => (d.os || "").split(" · ").slice(0, 2).join(" · ");
  function tokenGet() { return localStorage.getItem("capy-adm") || ""; }
  async function claim() { try { const r = await fetch(API_BASE + "/admin/claim", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ uid: capyUid() }) }); const j = await r.json(); if (j && j.token) { LSS("capy-adm", j.token); return j.token; } } catch (e) {} return ""; }
  async function load() { info.textContent = "lädt …"; body.innerHTML = '<div class="aMsg">Lade Spielerdaten …</div>'; back.hidden = true;
    let tok = tokenGet(); if (!tok) tok = await claim();
    if (!tok) { info.textContent = "kein Zugang"; body.innerHTML = '<div class="aMsg">Auf diesem Gerät ist kein Admin-Schlüssel hinterlegt.<br>Bitte Claude Bescheid geben, dann wird er neu freigeschaltet.</div>'; return; }
    try { const r = await fetch(API_BASE + "/admin/players", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ token: tok }), cache: "no-store" });
      if (r.status === 403) { info.textContent = "kein Zugang"; body.innerHTML = '<div class="aMsg">Admin-Schlüssel ungültig.<br>Bitte Claude Bescheid geben.</div>'; return; }
      const j = await r.json(); LIST = (j && j.list) || []; NOW = (j && j.now) || Date.now(); renderList(); } catch (e) { info.textContent = "offline"; body.innerHTML = '<div class="aMsg">Server nicht erreichbar.</div>'; } }
  function renderList() { back.hidden = true; const L = LIST.slice().sort((a, b) => b.last - a.last);
    const today = LIST.filter(p => NOW - p.last < 86400000).length, week = LIST.filter(p => NOW - p.last < 7 * 86400000).length, now = LIST.filter(p => NOW - p.last < 600000).length;
    info.textContent = `${LIST.length} Spieler · groß = beste Welle · neueste oben`;
    let h = `<div class="aSum"><div><b>${LIST.length}</b><small>gesamt</small></div><div><b>${now}</b><small>jetzt aktiv</small></div><div><b>${today}</b><small>heute</small></div><div><b>${week}</b><small>7 Tage</small></div></div>`;
    if (!L.length) h += '<div class="aMsg">Noch keine Spieler gemeldet.<br>Geräte melden sich ab Version V536 beim nächsten Öffnen.</div>';
    h += L.map(p => { const d = p.d || {}, w = nowWave(d), live = NOW - p.last < 600000 ? "on" : NOW - p.last < 86400000 ? "day" : "";
      const nz = d.cur && d.cur.nz ? ` · im Nuts L${d.cur.lv}` : "", bw = Math.max(d.bw || 0, (d.cur && d.cur.w) || 0);
      return `<button class="aRow" type="button" data-uid="${esc(p.uid)}"><span class="aNo">#${p.no}</span><span class="aNm">${esc(d.nm || "– ohne Namen –")}${p.uid === "M2HL-KCQH" ? " (du)" : ""}</span><span class="aW">W${bw}</span>
        <span class="aSub"><i class="aDot ${live}"></i>${esc(where(w || bw))}${nz}${d.d ? ` · ${d.d}× gestorben` : ""}</span><span class="aSub">${esc(devShort(d) || "Gerät unbekannt")} · ${ago(p.last)} · ${dur(d.t)} gespielt</span></button>`; }).join("");
    body.innerHTML = h; body.scrollTop = scrollY; }
  function renderOne(uid) { const p = LIST.find(x => x.uid === uid); if (!p) return; scrollY = body.scrollTop; back.hidden = false; const d = p.d || {}, w = nowWave(d);
    info.textContent = `Spieler #${p.no} · ${uid}`;
    const kv = (k, v) => `<div class="aKV"><span>${k}</span><b>${v}</b></div>`, sec = (t, rows) => `<div class="aSec">${t}</div><div class="aCard">${rows.join("")}</div>`;
    const by = d.dby || {}, byT = [["mon", "Monster"], ["blk", "Stapel voll"], ["weed", "Unkraut"]].filter(x => by[x[0]]).map(x => `${x[1]} ${by[x[0]]}`).join(" · ") || "–";
    const nzb = (d.nzb || []).map((v, i) => v ? `${NZW[i]} L${v}` : "").filter(Boolean).join(" · ") || "–";
    const cur = d.cur ? (d.cur.nz ? `Nuts ${NZW[d.cur.c] || ""} · Level ${d.cur.lv}` : `Welle ${d.cur.w} · ${where(d.cur.w)}`) : "nicht im Spiel";
    let h = sec("SPIELER", [kv("Nummer", "#" + p.no), kv("Name", esc(d.nm || "– ohne Namen –")), kv("Spieler-Nr.", esc(uid)), kv("Figur", esc((d.hero === "rosie" ? "Rosie" : "Blue") + (d.of ? " · Outfit " + d.of : ""))),
      kv("Sprache", esc(d.lang || "en")), kv("Version", esc(d.ver || "–")), kv("Erster Kontakt", dt(p.first)), kv("Zuletzt", dt(p.last) + " · " + ago(p.last)), kv("App-Starts", num(p.n)), kv("Tutorial", d.tut ? "abgeschlossen" : "nein"), kv("Cloud-Save", d.cs ? "ja" : "nein")]);
    h += sec("FORTSCHRITT", [kv("Gerade", esc(cur)), kv("Checkpoint", d.cp ? `Welle ${d.cp + 1} · ${esc(where(d.cp + 1))}` : "–"), kv("Beste Welle", `${Math.max(d.bw || 0, (d.cur && d.cur.w) || 0)} · ${esc(where(Math.max(d.bw || 0, (d.cur && d.cur.w) || 0)))}`),
      kv("Sterne", `${num(d.st)} ★ · ${d.pl || 0} von 30 Orten`), kv("Medaillen", `${d.md || 0} / 81`), kv("Squad Level", `${d.lv || 1} · ${num(d.xp)} XP`), kv("Missionen", num(d.ms)),
      kv("Daily-Kette", d.dly ? `Tag ${d.dly}` : "–"), kv("Geworbene Freunde", num(d.fr)), kv("Nuts-Bestwerte", esc(nzb)), kv("Nuts offen", d.nzs ? `${NZW[d.nzs.c] || ""} · Level ${d.nzs.lv}` : "–")]);
    h += sec("SPIELZEIT & TODE", [kv("Spielzeit", dur(d.t)), kv("Bildschirmzeit", dur(d.scrT)), kv("Läufe", num(d.r)), kv("Wellen geschafft", num(d.w)), kv("Monster gesplattet", num(d.k)), kv("Reihen", num(d.l)),
      kv("Tode Hauptspiel", num(d.d) + (d.dlw ? ` · zuletzt in Welle ${d.dlw}` : "")), kv("Tode Nuts", num(d.dnz)), kv("Todesursachen", esc(byT))]);
    h += sec("GERÄT", [kv("System", esc(d.os || "–")), kv("App / Browser", esc(d.app || "–")), kv("Bildschirm", esc(d.scr || "–")), kv("Sprache Gerät", esc(d.loc || "–")), kv("Zeitzone", esc(d.tz || "–")), kv("Dev-Modus", d.dev ? "an" : "aus")]);
    body.innerHTML = h; body.scrollTop = 0; }
  body.addEventListener("click", e => { const r = e.target.closest(".aRow"); if (r) { try { snd("uiTap"); } catch (er) {} renderOne(r.dataset.uid); } });
  back.addEventListener("click", () => { try { snd("uiTap"); } catch (e) {} renderList(); });
  ov.querySelector(".aRef").addEventListener("click", () => { try { snd("uiTap"); } catch (e) {} scrollY = 0; load(); });
  ov.querySelector(".aX").addEventListener("click", () => { try { snd("uiTap"); } catch (e) {} ov.hidden = true; });
  btn.addEventListener("click", () => { try { SFX.init(); snd("uiTap"); } catch (e) {} ov.hidden = false; scrollY = 0; profSend(false, true); load(); });
  window.__adm = { load, renderOne, list: () => LIST };
})(); } catch (e) { console.error("v536 adm", e); }
'''
rep('})(); } catch (e) { console.error("v339", e); }\n})();\n</script>',
    '})(); } catch (e) { console.error("v339", e); }\n' + ADM + '})();\n</script>')
open(p, "w", encoding="utf-8").write(s); print("ok V536")
