#!/usr/bin/env python3
# V647 (Martin 12.11. 09:44):
# 1) Mehr Metriken (Frust / Abbruch / Wohlfühlen): je Welle Dauer, verlorene Leben, Reihen, Splats, höchster Stapel, Tempo (wend);
#    knapp am Ende (near), 45 s keine Eingabe (idle), Menü/Neustart aus dem Spiel (quit), Sitzungslänge (sess),
#    Tipp-Karten (tip), Umfrage (poll), Bewertung (rate). Server (capy-api V647) wertet aus: Wut-Abbruch, Schnell-Neustart …
# 2) Einstellungen: «Bewerte das Spiel» 1–5 Sterne + Nachricht → /api/feedback (Admin-Analyse zeigt Bewertungen und Nachrichten).
# 4) Karte «Stapel zu hoch» kommt wieder (max. 1× je 5 Wellen, bis W30).
# 3) Schwebende Kurz-Umfrage nach Welle 7 und 17: «How do you like the game?» 👍 😐 👎, blockiert nichts, 12 s sichtbar.
import sys, os, json
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V646";', 'const GAME_VER = "V647";')

# --- Tipp-Karten zählen
rep('shopB.hidden = !shopOn;   /* V646 */',
    'shopB.hidden = !shopOn;   /* V646 */ try { window.__evLog && window.__evLog.push("tip", { d: { k: T.k, a: "shown" } }); } catch (e) {}   /* V647 */')
rep('close(); try { openShop(); setTimeout(',
    'try { window.__evLog && window.__evLog.push("tip", { d: { k: "stack", a: "shop" } }); } catch (er) {} close(); try { openShop(); setTimeout(')

# Karte «Stapel zu hoch» (Martin 09:52): jedes Mal, wenn der Stapel 4 Reihen unter der Decke ist – höchstens 1× je 5 Wellen, bis Welle 30; ab W8 mit Shop-Knopf
rep('{ k: "stack", c: () => S.wave <= 40 && GH - stackHeight() <= 4,', '{ k: "stack", rep: 5, c: () => S.wave <= 30 && GH - stackHeight() <= 4,')
rep('const seen = i => { try { return LS.get("tarnturm-tipb-" + TIPS[i].k) === "1"; } catch (e) { return true; } };',
    'const seen = i => { try { const T = TIPS[i]; if (T.rep) { const lw = +(LS.get("tarnturm-tipb-" + T.k + "-w") || -99); return (S.wave | 0) - lw < T.rep; } return LS.get("tarnturm-tipb-" + T.k) === "1"; } catch (e) { return true; } };   /* V647: wiederkehrende Karte */')
rep('try { LS.set("tarnturm-tipb-" + T.k, "1"); } catch (e) {}', 'try { LS.set("tarnturm-tipb-" + T.k, "1"); if (T.rep) LS.set("tarnturm-tipb-" + T.k + "-w", String(S.wave | 0)); } catch (e) {}')

# --- Admin-Analyse: neue Abschnitte (Daten von capy-api V647 unter j.x)
rep("h += '<div class=\"aMsg\" style=\"font-size:12px\">Zählt ab V594",
    "{ const x = j.x || {}, rt2 = x.rating || {}, pl = x.poll || {};   /* V647 */\n"
    "      h += sec(\"BEWERTUNG (1–5 STERNE)\", rt2.n ? [kv(\"Durchschnitt\", `${rt2.avg} ★ · ${rt2.n} Bewertungen`)].concat([5, 4, 3, 2, 1].map(i => kv(\"★\".repeat(i), num((rt2.dist || {})[i] || 0)))) : []);\n"
    "      h += sec(\"UMFRAGE «WIE GEFÄLLT DIR DAS SPIEL?»\", Object.keys(pl).sort().map(k => { const v = pl[k], tot = v.up + v.mid + v.down; return kv(k.replace(\"W\", \"nach Welle \"), `👍 ${v.up} · 😐 ${v.mid} · 👎 ${v.down} · ohne Antwort ${v.skip}` + (tot ? ` · ${pc(v.up, tot)} 👍` : \"\")); }));\n"
    "      const nsum = o => Object.values(o || {}).reduce((a, b) => a + b, 0);\n"
    "      h += sec(\"FRUST-SIGNALE\", [kv(\"Tod → App zu in 20 s\", num(x.rage || 0)), kv(\"Tod → sofort Neustart\", num(x.quickRestart || 0)), kv(\"Knapp am Ende (2 Reihen)\", num(nsum(x.near))), kv(\"45 s keine Eingabe\", num(nsum(x.idle))), kv(\"Sitzung (Median)\", x.sessMedian ? Math.round(x.sessMedian / 60) + \" min · \" + x.sessN + \" Sitzungen\" : \"–\")].concat(obj(x.quits).map(r => r.replace(\"<span>\", \"<span>Verlassen über \"))));\n"
    "      h += sec(\"JE WELLE: DAUER · LEBEN VERLOREN · STAPEL\", (x.waves || []).slice(0, 60).map(r => kv(\"W\" + r.w + \" (\" + r.n + \")\", `${r.sec} s · ${r.lives} Leben · ${r.lossPct} % mit Verlust · Stapel ${r.stack}`)));\n"
    "      h += sec(\"TIPP-KARTEN\", obj(x.tips));\n"
    "      h += sec(\"NACHRICHTEN\", (x.feedback || []).slice(0, 40).map(f => `<div class=\"aKV\" style=\"display:block\"><span>${esc(new Date(f.t).toLocaleString(\"de-AT\"))} · ${f.stars ? \"★\".repeat(f.stars) : \"–\"} · ${esc(f.src || \"\")}${f.w ? \" · W\" + f.w : \"\"} · ${esc(f.lang || \"\")} ${esc(f.ch || \"\")}${f.team ? \" · TEAM\" : \"\"}</span><b style=\"display:block;white-space:pre-wrap;font-weight:600\">${esc(f.msg || \"\")}</b></div>`)); }\n"
    "    h += '<div class=\"aMsg\" style=\"font-size:12px\">Zählt ab V594")

# --- Einstellungen: Bewertung
STARS = "".join(f'<button type="button" class="rStar" data-s="{i}" aria-label="{i} of 5"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.6l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 17.4l-5.8 3.1 1.1-6.5-4.7-4.6 6.5-.9z"/></svg></button>' for i in range(1, 6))
rep('<div class="setRow"><button id="setCloud"',
    f'<div class="setRate"><div class="hpHead">RATE THE GAME</div><div class="rateRow"><div class="rateStars" id="setStars">{STARS}</div><button id="setMsg" class="btn-small" type="button">✉ MESSAGE</button></div></div><div class="setRow"><button id="setCloud"')

CSS = r'''
.setRate{display:flex;flex-direction:column;align-items:center;gap:4px;margin-top:6px}
.rateRow{display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap}
.rateStars{display:flex;gap:2px}
button.rStar{width:40px!important;height:40px!important;min-height:0!important;padding:0!important;border:0!important;background:none!important;box-shadow:none!important;cursor:pointer;transition:transform .12s;display:inline-flex;align-items:center;justify-content:center}
button.rStar svg{width:100%;height:100%;fill:#efe3c8;stroke:#3a2414;stroke-width:1.6;stroke-linejoin:round}
button.rStar.on svg{fill:#ffc531}button.rStar:active{transform:scale(.88)}
#ovRate{position:fixed;inset:0;z-index:90;display:flex;align-items:center;justify-content:center;background:rgba(30,18,8,.55);padding:calc(env(safe-area-inset-top,0px) + 12px) 12px calc(env(safe-area-inset-bottom,0px) + 12px)}
#ovRate[hidden]{display:none}
#ovRate .rBox{width:min(380px,100%);background:#fff6e2;border:3px solid #3a2414;border-radius:18px;box-shadow:0 4px 0 #3a2414;padding:14px 16px 16px;display:flex;flex-direction:column;gap:10px;color:#3a2414}
#ovRate h2{margin:0;font:400 24px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.04em;text-align:center}
#ovRate .rateStars{justify-content:center}#ovRate button.rStar{width:50px!important;height:50px!important}
#ovRate textarea{width:100%;box-sizing:border-box;min-height:96px;resize:vertical;border:2.5px solid #3a2414;border-radius:12px;padding:8px 10px;font:500 15px/1.35 var(--f-body,"Baloo 2",sans-serif);color:#3a2414;background:#fffdf6}
#ovRate small{font:600 12px/1.3 var(--f-body,"Baloo 2",sans-serif);color:#7a5a3e;text-align:center}
#ovRate .rBtns{display:flex;gap:10px}#ovRate .rBtns button{flex:1;min-height:46px}
#ovRate .rMsg{min-height:1.2em;text-align:center;font:700 13px/1.3 var(--f-body,"Baloo 2",sans-serif)}
#pollCard{position:fixed;left:50%;top:calc(env(safe-area-inset-top,0px) + 118px);z-index:72;width:min(300px,86vw);transform:translate(-50%,-14px) scale(.92);opacity:0;transition:opacity .3s,transform .35s cubic-bezier(.2,1.5,.4,1);background:#fff6e2;border:3px solid #3a2414;border-radius:20px;box-shadow:0 4px 0 #3a2414,0 10px 26px rgba(0,0,0,.28);padding:10px 12px 12px;text-align:center;color:#3a2414}
#pollCard.on{opacity:1;transform:translate(-50%,0) scale(1);animation:pollBob 3.2s ease-in-out .4s infinite}
@keyframes pollBob{0%,100%{margin-top:0}50%{margin-top:-5px}}
#pollCard[hidden]{display:none}
#pollCard small{display:block;font:700 10px/1 var(--f-body,"Baloo 2",sans-serif);letter-spacing:.18em;color:#c0782a}
#pollCard b{display:block;margin:4px 0 10px;font:400 21px/1.05 var(--f-display,"Bangers",sans-serif);letter-spacing:.03em}
#pollCard .pRow{display:flex;justify-content:center;gap:14px}
#pollCard .pBtn{width:62px;height:62px;border-radius:50%;border:3px solid #3a2414;box-shadow:0 3px 0 #3a2414;font:400 32px/1 sans-serif;display:flex;align-items:center;justify-content:center;padding:0;cursor:pointer}
#pollCard .pBtn:active{transform:translateY(2px);box-shadow:0 1px 0 #3a2414}
#pollCard .pUp{background:#9fdc7c}#pollCard .pMid{background:#ffe38f;width:52px;height:52px;font-size:27px;align-self:center}#pollCard .pDown{background:#ffa592}
#pollCard .pWhy{margin-top:10px;font:400 16px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.05em;background:#ffd84d;border:2.5px solid #3a2414;border-radius:12px;box-shadow:0 3px 0 #3a2414;padding:7px 12px 5px;color:#3a2414}
@media (prefers-reduced-motion:reduce){#pollCard.on{animation:none}}
'''
rep('body:has(.bar:not(.off)) .nextRow{gap:3px!important}', 'body:has(.bar:not(.off)) .nextRow{gap:3px!important}' + CSS.replace("\n", "") + '   /* V647 */')

JS = r'''
  /* V647: Erleben messen, Bewertung, Kurz-Umfrage W7/W17 */
  try { (() => {
    const E = () => window.__evLog, ev = (k, d) => { try { E() && E().push(k, { d }); } catch (e) {} };
    const T0 = performance.now(); let lastIn = performance.now(), W = null, wavesSess = 0;
    ["pointerdown", "keydown"].forEach(t => addEventListener(t, () => { lastIn = performance.now(); }, true));
    document.addEventListener("click", e => { try { const t = e.target && e.target.closest ? e.target : null; if (!t) return;
      if (t.closest("#btnPMenu")) ev("quit", { a: "menu" }); else if (t.closest("#btnPRestart")) ev("quit", { a: "restart" }); else if (t.closest("#btnPNutsQuit")) ev("quit", { a: "nuts" }); } catch (x) {} }, true);
    document.addEventListener("visibilitychange", () => { if (document.hidden) { ev("sess", { s: Math.round((performance.now() - T0) / 1000), wv: wavesSess }); try { E() && E().flush(true); } catch (e) {} } });
    const live = () => typeof S !== "undefined" && S && S.started && !S.over && !S.replay && !S.testRun;
    setInterval(() => { try {
      if (!live()) { W = null; return; }
      const now = performance.now(), inW = !!S.inWave, w = S.wave | 0;
      if (W && (!inW || w !== W.w)) { ev("wend", { s: Math.round((now - W.t) / 1000), lv: Math.max(0, W.l - (S.lives | 0)), ln: Math.max(0, (S.lines | 0) - W.ln), k: Math.max(0, (S.kills | 0) - W.k), mx: W.mx, g: S.gold | 0, x: S.speed || 1, nz: S.nuts ? 1 : 0 });
        wavesSess++; const done = W.w; W = null; if (!S.nuts && (done === 7 || done === 17)) pollLater(done); }
      if (inW && !W) W = { w, t: now, l: S.lives | 0, ln: S.lines | 0, k: S.kills | 0, mx: 0, near: 0, idle: 0 };
      if (W && inW) { let h = 0; try { h = stackHeight(); } catch (e) {} W.mx = Math.max(W.mx, h);
        if (!W.near && h && GH - h <= 2) { W.near = 1; ev("near", { h }); }
        if (!W.idle && !S.paused && !document.hidden && now - lastIn > 45000) { W.idle = 1; ev("idle", { s: Math.round((now - lastIn) / 1000) }); } }
    } catch (e) {} }, 500);

    /* Bewertung: Sterne + Nachricht */
    const ov = document.createElement("div"); ov.id = "ovRate"; ov.hidden = true;
    ov.innerHTML = '<div class="rBox" role="dialog" aria-modal="true"><h2>RATE CAPYBARA SQUAD</h2><div class="rateStars" id="rateStars">' + [1, 2, 3, 4, 5].map(i => `<button type="button" class="rStar" data-s="${i}" aria-label="${i} of 5"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.6l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 17.4l-5.8 3.1 1.1-6.5-4.7-4.6 6.5-.9z"/></svg></button>`).join("") + '</div>'
      + '<textarea id="rateText" maxlength="1000" rows="4" placeholder="Your message (optional) – what do you like, what bugs you?"></textarea><small>Please no personal data like phone or email.</small>'
      + '<div class="rBtns"><button type="button" id="rateCancel">Cancel</button><button type="button" id="rateSend" class="btn-accent">SEND ▶</button></div><div class="rMsg" id="rateMsg"></div></div>';
    document.body.appendChild(ov);
    let rStars = 0, rSrc = "settings", held = false;
    const paint = (box, n) => box.querySelectorAll(".rStar").forEach(b => b.classList.toggle("on", +b.dataset.s <= n));
    const msgEl = ov.querySelector("#rateMsg"), txt = ov.querySelector("#rateText"), sendB = ov.querySelector("#rateSend");
    function openRate(stars, src) { try { txt.placeholder = T("Your message (optional) – what do you like, what bugs you?"); } catch (e) {} rStars = stars | 0; rSrc = src || "settings"; paint(ov, rStars); msgEl.textContent = ""; sendB.disabled = false; ov.hidden = false;
      try { if (live() && !S.paused && !S.coachHold) { S.coachHold = true; held = true; } } catch (e) {} try { snd("uiTap"); } catch (e) {} }
    function closeRate() { ov.hidden = true; try { if (held) { S.coachHold = false; held = false; window.__evLast = performance.now(); } } catch (e) {} }
    window.__openRate = openRate;
    ov.querySelector("#rateStars").addEventListener("click", e => { const b = e.target.closest(".rStar"); if (!b) return; rStars = +b.dataset.s; paint(ov, rStars); try { snd("uiTap"); } catch (er) {} });
    ov.querySelector("#rateCancel").addEventListener("click", () => { try { snd("uiTap"); } catch (e) {} closeRate(); });
    ov.addEventListener("click", e => { if (e.target === ov) closeRate(); });
    sendB.addEventListener("click", async () => { const m = (txt.value || "").trim();
      if (!rStars && !m) { msgEl.textContent = T("Tap 1 to 5 stars or write a message."); return; }
      sendB.disabled = true; msgEl.textContent = T("Sending …"); let ok = false;
      try { const L = E() || {}; const r = await fetch(API_BASE + "/feedback", { method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ stars: rStars || null, msg: m, uid: (() => { try { return capyUid(); } catch (e) { return ""; } })(), ver: GAME_VER, ch: L.ch || "", lang: (typeof I18N !== "undefined" && I18N.lang) || "en", src: rSrc, w: (typeof S !== "undefined" && S && S.wave) | 0, plat: L.plat || "" }) });
        ok = r.ok; } catch (e) {}
      if (ok) { ev("rate", { s: rStars, src: rSrc, len: m.length }); try { if (rStars) LS.set("capy-rated", String(rStars)); } catch (e) {} txt.value = ""; msgEl.textContent = T("Thanks! Your message reached the team.");
        try { const ss = document.getElementById("setStars"); if (ss) paint(ss, rStars); } catch (e) {} setTimeout(closeRate, 1600); }
      else { sendB.disabled = false; msgEl.textContent = T("Couldn't send – check your connection and try again."); } });
    try { const ss = document.getElementById("setStars"); if (ss) { paint(ss, +(LS.get("capy-rated") || 0));
      ss.addEventListener("click", e => { const b = e.target.closest(".rStar"); if (b) openRate(+b.dataset.s, "settings"); }); }
      const mb = document.getElementById("setMsg"); if (mb) mb.addEventListener("click", () => openRate(+(LS.get("capy-rated") || 0), "settings")); } catch (e) {}

    /* Kurz-Umfrage nach W7 und W17: schwebend, blockiert nichts */
    const pc = document.createElement("div"); pc.id = "pollCard"; pc.hidden = true; document.body.appendChild(pc);
    let pT = 0, pAt = 0;
    function pollHide() { clearTimeout(pT); pc.classList.remove("on"); setTimeout(() => { if (!pc.classList.contains("on")) pc.hidden = true; }, 320); }
    function pollShow(at) { if (!live() || S.nuts) return; pAt = at; try { LS.set("capy-poll-" + at, "1"); } catch (e) {}
      pc.innerHTML = '<small>QUICK QUESTION</small><b>How do you like the game?</b><div class="pRow"><button type="button" class="pBtn pUp" data-v="1" aria-label="Good">👍</button><button type="button" class="pBtn pMid" data-v="0" aria-label="Okay">😐</button><button type="button" class="pBtn pDown" data-v="-1" aria-label="Not good">👎</button></div>';
      pc.hidden = false; requestAnimationFrame(() => pc.classList.add("on")); try { snd("uiTap"); } catch (e) {}
      clearTimeout(pT); pT = setTimeout(() => { ev("poll", { v: "x", at }); pollHide(); }, 12000); }
    pc.addEventListener("click", e => { const b = e.target.closest(".pBtn"); const why = e.target.closest(".pWhy");
      if (why) { pollHide(); openRate(0, "poll"); return; }
      if (!b) return; const v = +b.dataset.v; ev("poll", { v, at: pAt }); try { snd("uiTap"); } catch (er) {} clearTimeout(pT);
      pc.innerHTML = '<b>Thanks!</b>' + (v <= 0 ? '<button type="button" class="pWhy">TELL US WHY ▶</button>' : ""); pT = setTimeout(pollHide, v <= 0 ? 7000 : 2200); });
    function pollLater(at) { try { if (LS.get("capy-poll-" + at) === "1") return; } catch (e) { return; }
      const go = () => { if (!live() || S.nuts) return; if (typeof uiWinOpen === "function" && uiWinOpen()) { setTimeout(go, 2500); return; } pollShow(at); };
      if (typeof window.__whenCalm === "function") window.__whenCalm(go, 4000); else setTimeout(go, 4000); }
    setInterval(() => { try { if (!pc.hidden && pc.classList.contains("on") && ((typeof uiWinOpen === "function" && uiWinOpen()) || !live())) { clearTimeout(pT); pollHide(); try { LS.set("capy-poll-" + pAt, "0"); } catch (e) {} if (live()) pollLater(pAt); } } catch (e) {} }, 700);
    window.__pollShow = pollShow;
  })(); } catch (e) { console.error("v647", e); }
'''
rep('    window.__evLog = { q, flush, push, sess, plat, br, scr, ch };\n  })(); } catch (e) {}\n',
    '    window.__evLog = { q, flush, push, sess, plat, br, scr, ch };\n  })(); } catch (e) {}\n' + JS)
open(p, "w", encoding="utf-8").write(s)

# Übersetzungen anhängen (nur fehlende Schlüssel, Reihenfolge behalten)
TR = {
 "RATE THE GAME": ("ОЦЕНИ ИГРУ", "VALORA EL JUEGO", "AVALIE O JOGO"),
 "✉ MESSAGE": ("✉ НАПИСАТЬ", "✉ MENSAJE", "✉ MENSAGEM"),
 "RATE CAPYBARA SQUAD": ("ОЦЕНИ CAPYBARA SQUAD", "VALORA CAPYBARA SQUAD", "AVALIE CAPYBARA SQUAD"),
 "Your message (optional) – what do you like, what bugs you?": ("Твоё сообщение (по желанию) – что нравится, что мешает?", "Tu mensaje (opcional): ¿qué te gusta y qué te molesta?", "Sua mensagem (opcional): do que você gosta, o que te incomoda?"),
 "Please no personal data like phone or email.": ("Пожалуйста, без личных данных – без телефона и почты.", "Por favor, sin datos personales como teléfono o correo.", "Por favor, sem dados pessoais como telefone ou e-mail."),
 "SEND ▶": ("ОТПРАВИТЬ ▶", "ENVIAR ▶", "ENVIAR ▶"),
 "Tap 1 to 5 stars or write a message.": ("Нажми от 1 до 5 звёзд или напиши сообщение.", "Toca de 1 a 5 estrellas o escribe un mensaje.", "Toque de 1 a 5 estrelas ou escreva uma mensagem."),
 "Sending …": ("Отправляем …", "Enviando …", "Enviando …"),
 "Thanks! Your message reached the team.": ("Спасибо! Сообщение дошло до команды.", "¡Gracias! Tu mensaje llegó al equipo.", "Valeu! Sua mensagem chegou à equipe."),
 "Couldn't send – check your connection and try again.": ("Не отправилось – проверь интернет и попробуй ещё раз.", "No se pudo enviar: revisa la conexión e inténtalo de nuevo.", "Não deu para enviar – confira a conexão e tente de novo."),
 "QUICK QUESTION": ("КОРОТКИЙ ВОПРОС", "PREGUNTA RÁPIDA", "PERGUNTA RÁPIDA"),
 "How do you like the game?": ("Как тебе игра?", "¿Qué te parece el juego?", "O que você está achando do jogo?"),
 "Thanks!": ("Спасибо!", "¡Gracias!", "Valeu!"),
 "TELL US WHY ▶": ("РАССКАЖИ ПОЧЕМУ ▶", "CUÉNTANOS POR QUÉ ▶", "CONTA PRA GENTE ▶"),
}
for i, l in enumerate(("en", "ru", "es", "pt")):
    q = os.path.join(site, "lang", f"{l}.json"); d = json.load(open(q, encoding="utf-8"))
    for k, v in TR.items():
        if k not in d: d[k] = k if l == "en" else v[i - 1]
    with open(q, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=0)
print("ok V647")
