#!/usr/bin/env python3
"""V455 – Daily Drop + Daily Mission als Kalenderblatt rechts am Startscreen (Martin 08.11. 12:41/13:09/13:10/13:59).
- Kalenderblatt (rechts oben, Capybara-Look): Datum, Tag der 7-Tage-Kette, Tagesmission mit Fortschritt, Belohnung, Kettenpunkte (1 Schutztag je Woche).
- Daily Drop ab bester Welle 10: ein Gratis-Special für den nächsten Lauf (Tag 1–6 wechselnd, Tag 7 Ten-ton); Antippen → Karte mit CLAIM.
- Daily Mission ab bester Welle 20: eine Aufgabe je Tag (Splats / Reihen / Wellen / Türme / Dreier-Reihen), Belohnung 300 Squad-XP; erledigt → SEND TO FRIEND (Teilen-Link ?ch=…).
- Kette: gestern gespielt → +1; ein ausgelassener Tag je Woche wird durch den Schutztag überbrückt; sonst zurück auf Tag 1. Tag 7 → danach wieder Tag 1.
- Speicher capy-daily; Testläufe zählen nicht. Test: https://playcapybarasquad.com/?test=daily (setzt beste Welle auf 25, Kette Tag 3).
Nutzung: python3 tools/patch455.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V454";', 'const GAME_VER = "V455";')

# ---------- JS ----------
JS = r'''
/* ===== V455: Daily Drop + Daily Mission (Kalenderblatt) ===== */
const DAILY_DROP_W = 10, DAILY_MSN_W = 20, DAILY_XP = 300;
const DAILY_DROPS = [["snipe", "Sniper strike", "snipes", 13], ["lock", "Lockdown", "locks", 25], ["mix", "Concrete mixer", "mixers", 9], ["chomp", "Chomper", "chomps", 17], ["tesla", "Tesla storm", "teslas", 21], ["snipe", "Sniper strike", "snipes", 13], ["ton", "Ten-ton drop", "tons", 8]];
const DAILY_MSN = [["k", "Splat {n} monsters", [40, 60, 90]], ["l", "Clear {n} rows", [12, 18, 25]], ["w", "Finish {n} waves", [6, 10, 15]], ["t", "Build {n} towers", [6, 9, 12]], ["c3", "Clear 3 rows at once {n} times", [1, 2, 3]], ["sp", "Squish {n} monsters with blocks", [3, 5, 8]]];
function dailyKey(d = new Date()) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
function dailyWeek(d = new Date()) { const x = new Date(d); x.setHours(0, 0, 0, 0); x.setDate(x.getDate() - ((x.getDay() + 6) % 7)); return dailyKey(x); }
function dailyLoad() { let D = null; try { D = JSON.parse(LS.get("capy-daily") || "null"); } catch (e) {} if (!D || typeof D !== "object") D = {}; D.streak = +D.streak || 0; D.sent = Array.isArray(D.sent) ? D.sent : []; return D; }
let DAILY = dailyLoad();
function dailySave() { try { LS.set("capy-daily", JSON.stringify(DAILY)); } catch (e) {} }
function dailyBestW() { try { return Math.max(msnBestW(), +LS.get("tarnturm-cp-" + MODE) || 0); } catch (e) { return 0; } }
function dailyDay() { return DAILY.streak > 0 ? ((DAILY.streak - 1) % 7) + 1 : 1; }
function dailyRoll() {   /* neuer Tag: Kette fortschreiben, Mission würfeln */
  const today = dailyKey(); if (DAILY.day === today) return false;
  const y = new Date(); y.setDate(y.getDate() - 1); const yk = dailyKey(y), b = new Date(); b.setDate(b.getDate() - 2); const bk = dailyKey(b), wk = dailyWeek();
  if (!DAILY.day) DAILY.streak = 1;
  else if (DAILY.day === yk) DAILY.streak += 1;
  else if (DAILY.day === bk && DAILY.shieldWk !== wk) { DAILY.streak += 1; DAILY.shieldWk = wk; DAILY.shieldUsed = today; }   /* ein ausgelassener Tag je Woche */
  else DAILY.streak = 1;
  DAILY.day = today; DAILY.claimed = false;
  const bw = dailyBestW(), pool = DAILY_MSN.filter(m => !(m[0] === "t" && bw < 3)), pick = pool[Math.floor(Math.random() * pool.length)], tier = bw >= 60 ? 2 : bw >= 35 ? 1 : 0;
  DAILY.m = { k: pick[0], n: pick[2][tier], p: 0, txt: pick[1].replace("{n}", pick[2][tier]), done: false, xp: false };
  dailySave(); return true; }
function dailyDrop() { const i = dailyDay() - 1, bw = dailyBestW(); let d = DAILY_DROPS[i]; if (bw < d[3]) d = DAILY_DROPS[6]; return d; }
function dailyGate() { return dailyBestW() >= DAILY_DROP_W; }
function dailyMsnGate() { return dailyBestW() >= DAILY_MSN_W; }
function dailyAdd(key, v) { try { if (!DAILY.m || DAILY.m.done || DAILY.m.k !== key || !v || v <= 0) return; if (!S || !S.started || S.over || S.testRun || S.nuts || S.replay) return;
    DAILY.m.p = Math.min(DAILY.m.n, (DAILY.m.p || 0) + v);
    if (DAILY.m.p >= DAILY.m.n) { DAILY.m.done = true; DAILY.m.xp = true; try { MSN.xp = (MSN.xp || 0) + DAILY_XP; msnSave(); } catch (e) {} msnTQ.push({ txt: "DAILY MISSION · " + DAILY.m.txt, xp: DAILY_XP }); }
    dailySave(); dailyLeaf(); } catch (e) {} }
{ const _ma = msnAdd; msnAdd = function (key, v) { try { dailyAdd(key, v); } catch (e) {} return _ma.apply(this, arguments); }; }
{ const _me = window.__msnEv; window.__msnEv = (k, c) => { try { if (k === "wave" && S && S.lives > 0 && !S.over) dailyAdd("w", 1); if (k === "clr" && c >= 3) dailyAdd("c3", 1); } catch (e) {} try { return _me && _me(k, c); } catch (e) {} }; }
function dailyClaim() { if (!dailyGate() || DAILY.claimed) return false; const d = dailyDrop(); DAILY.claimed = true; DAILY.pend = d[2]; DAILY.pendName = d[1]; dailySave(); return d; }
function dailyGrant() { try { if (!DAILY.pend || !S || !S.started || S.testRun || S.nuts || S.replay) return; const f = DAILY.pend, nm = DAILY.pendName || "Daily drop"; S[f] = (S[f] || 0) + 1; DAILY.pend = null; DAILY.pendName = null; dailySave(); setTimeout(() => { try { toast(`DAILY DROP · ${nm.toUpperCase()} in your Pocket`, "SUPPLY", 2600); } catch (e) {} }, 4000); } catch (e) {} }
{ const _sg = startGame; startGame = function () { const r = _sg.apply(this, arguments); try { dailyGrant(); } catch (e) {} return r; }; }
const DAILY_MON = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"], DAILY_WD = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];
function dailyLeaf() {
  let el = document.getElementById("dailyLeaf"); const st = document.getElementById("ovStart");
  if (!dailyGate()) { if (el) el.remove(); return; }
  dailyRoll();
  if (!el) { el = document.createElement("div"); el.id = "dailyLeaf"; el.setAttribute("role", "button"); el.tabIndex = 0; st.appendChild(el); el.addEventListener("click", e => { e.stopPropagation(); try { SFX.init(); snd("uiTap"); } catch (er) {} dailyCard(); }); }
  const now = new Date(), day = dailyDay(), d = dailyDrop(), m = dailyMsnGate() ? DAILY.m : null, shieldDay = (() => { try { const s = new Date(DAILY.shieldUsed); if (DAILY.shieldWk === dailyWeek() && !isNaN(s)) return ((DAILY.streak - Math.round((now - s) / 864e5)) - 1) % 7 + 1; } catch (e) {} return 0; })();
  const dots = [1, 2, 3, 4, 5, 6, 7].map(i => `<i class="${i < day ? "on" : i === day ? "now" : ""}${i === shieldDay ? " shield" : ""}">${i < day ? "✓" : i === shieldDay ? "🛡" : i}</i>`).join("");
  el.innerHTML = `<i class="ring l"></i><i class="ring r"></i><div class="head">${DAILY_WD[now.getDay()]} · ${DAILY_MON[now.getMonth()]} ${now.getDate()}<b>DAY ${day}</b></div><div class="body">`
    + (m ? `<div class="tag">DAILY MISSION</div><div class="task">${m.txt}</div><div class="dlBar"><b style="width:${Math.round(100 * Math.min(1, (m.p || 0) / m.n))}%"></b></div><div class="num"><span>${m.p || 0} / ${m.n}</span><span>${m.done ? "done ✓" : "today"}</span></div>` : `<div class="tag">DAILY MISSION</div><div class="task dim">Opens at wave ${DAILY_MSN_W}</div>`)
    + `<div class="rew${DAILY.claimed ? " got" : ""}"><img src="${(typeof ICO_SPR !== "undefined" && ICO_SPR[d[0]]) || ""}" alt="">${DAILY.claimed ? `${d[1]}<br>${DAILY.pend ? "in your next run" : "collected"}` : `${d[1]}<br>Daily Drop · tap`}</div>`
    + `<div class="streak">${dots}</div><div class="sub">7-day chain · 1 shield day</div><i class="corner"></i></div>`;
}
function dailyCard() {
  dailyRoll(); const d = dailyDrop(), m = dailyMsnGate() ? DAILY.m : null, day = dailyDay();
  let ov = document.getElementById("ovDaily"); if (!ov) { ov = document.createElement("div"); ov.id = "ovDaily"; ov.className = "overlay"; document.body.appendChild(ov); ov.addEventListener("click", e => { if (e.target === ov || e.target.closest(".dlX")) { ov.hidden = true; dailyLeaf(); } }); }
  ov.innerHTML = `<div class="dlBox"><button class="albX dlX" aria-label="Close">✕</button><h2>DAILY</h2><div class="dlDay">Day ${day} of 7 · ${DAILY.streak} day${DAILY.streak === 1 ? "" : "s"} in a row</div>
    <div class="dlSec">DAILY DROP</div><div class="dlRow"><img src="${(typeof ICO_SPR !== "undefined" && ICO_SPR[d[0]]) || ""}" alt=""><div><b>${d[1]}</b><span>${day === 7 ? "Day-7 bonus · the big one" : "Lands in your Pocket at the start of your next run"}</span></div>${DAILY.claimed ? `<em class="dlGot">${DAILY.pend ? "NEXT RUN" : "✓"}</em>` : `<button class="btn-accent dlClaim">CLAIM</button>`}</div>
    <div class="dlSec">DAILY MISSION${m ? ` <small>+${DAILY_XP} XP</small>` : ""}</div>`
    + (m ? `<div class="dlRow"><div class="dlBig">${m.done ? "✓" : Math.round(100 * (m.p || 0) / m.n) + "%"}</div><div><b>${m.txt}</b><span>${m.p || 0} / ${m.n}${m.done ? " · done" : " · counts in your main run"}</span></div>${m.done ? `<button class="btn-accent dlSend">SEND TO FRIEND</button>` : ""}</div>` : `<div class="dlRow"><div class="dlBig">🔒</div><div><b>Opens at wave ${DAILY_MSN_W}</b><span>Best wave so far: ${dailyBestW()}</span></div></div>`)
    + `<div class="dlSec">THE CHAIN</div><div class="dlChain">${[1, 2, 3, 4, 5, 6, 7].map(i => `<i class="${i < day ? "on" : i === day ? "now" : ""}">${i}<small>${DAILY_DROPS[i - 1][1].split(" ")[0]}</small></i>`).join("")}</div><div class="dlNote">Play on 7 days in a row for the Ten-ton. Miss one day a week – the shield keeps your chain.</div></div>`;
  ov.hidden = false;
  const cb = ov.querySelector(".dlClaim"); if (cb) cb.addEventListener("click", e => { e.stopPropagation(); const got = dailyClaim(); if (got) { try { snd("powerup"); } catch (er) {} dailyCard(); } });
  const sb = ov.querySelector(".dlSend"); if (sb) sb.addEventListener("click", async e => { e.stopPropagation(); const t0 = sb.textContent, note = t => { sb.textContent = t; setTimeout(() => { sb.textContent = t0; }, 3500); };
    const url = SHARE_URL + "/?ch=dm-" + (m.k) + "-" + m.n, text = `Daily mission done: ${m.txt}. Your turn – can you do it today?`;
    if (navigator.share) { try { await navigator.share({ title: "Capybara Squad", text, url }); note("SENT!"); } catch (er) { if (!(er && er.name === "AbortError")) note("LINK: " + url.replace("https://", "")); } return; }
    try { await navigator.clipboard.writeText(text + " " + url); note("LINK COPIED!"); } catch (er) { note("LINK: " + url.replace("https://", "")); } });
}
setInterval(() => { try { const st = document.getElementById("ovStart"); if (!st || st.hidden || document.body.classList.contains("awOn")) { const el = document.getElementById("dailyLeaf"); if (el && (!st || st.hidden)) el.remove(); return; } if (!document.getElementById("dailyLeaf") || dailyKey() !== DAILY.day) dailyLeaf(); } catch (e) {} }, 800);
try { if (new URLSearchParams(location.search).get("test") === "daily") { LS.set("tarnturm-cp-" + MODE, "25"); const y = new Date(); y.setDate(y.getDate() - 1); DAILY = { day: dailyKey(y), streak: 2, sent: [] }; dailySave(); } } catch (e) {}
window.__daily = { add: dailyAdd, leaf: dailyLeaf, card: dailyCard, roll: dailyRoll, get D() { return DAILY; } };
/* ===== Ende V455 ===== */
'''
rep('/* Zähler: vorhandene Funktionen umhüllen */', JS + '\n/* Zähler: vorhandene Funktionen umhüllen */')

# ---------- CSS ----------
CSS = r'''
/* V455: Daily-Kalenderblatt rechts am Startscreen */
#dailyLeaf{position:fixed;right:12px;top:calc(env(safe-area-inset-top,0px) + 96px);width:148px;z-index:60;font-family:"Baloo 2",system-ui,sans-serif;color:#3a2414;transform:rotate(2.5deg);filter:drop-shadow(0 6px 0 rgba(58,36,20,.55)) drop-shadow(0 10px 14px rgba(0,0,0,.35));cursor:pointer;text-align:left}
#dailyLeaf .ring{position:absolute;top:-9px;width:10px;height:18px;border:3px solid #3a2414;border-radius:6px;background:#e9e2d2;box-sizing:border-box;z-index:2}
#dailyLeaf .ring.l{left:28px}#dailyLeaf .ring.r{right:28px}
#dailyLeaf .head{background:linear-gradient(#ff7fbd,#e94c95);border:3px solid #3a2414;border-bottom:0;border-radius:14px 14px 0 0;padding:9px 10px 5px;text-align:center;color:#fff;font:400 12px/1 Bangers,sans-serif;letter-spacing:.14em;text-shadow:0 2px 0 #7a1d4a}
#dailyLeaf .head b{display:block;font-size:28px;letter-spacing:.04em;margin-top:2px;text-shadow:0 3px 0 #7a1d4a;font-weight:400}
#dailyLeaf .body{background:#fff7e8;border:3px solid #3a2414;border-top:3px dashed #3a2414;border-radius:0 0 14px 14px;padding:8px 10px 9px;position:relative}
#dailyLeaf .tag{font:400 11px/1 Bangers,sans-serif;letter-spacing:.12em;color:#d94c8c}
#dailyLeaf .task{font-weight:800;font-size:13px;line-height:1.15;margin:3px 0 6px}#dailyLeaf .task.dim{opacity:.6;font-weight:700}
#dailyLeaf .dlBar{height:12px;border:2px solid #3a2414;border-radius:999px;background:#e9e2d2;overflow:hidden;box-sizing:border-box;width:100%;display:block}
#dailyLeaf .dlBar b{display:block!important;height:100%!important;border-radius:999px;margin:0!important;padding:0!important;font-size:0;background:linear-gradient(#ffd75e,#f2b51c);transition:width .4s}
#dailyLeaf .num{display:flex;justify-content:space-between;font-size:11px;font-weight:700;margin-top:3px;color:#7a5a3c}
#dailyLeaf .rew{display:flex;align-items:center;gap:6px;margin-top:6px;background:#ffe6a8;border:2px solid #3a2414;border-radius:10px;padding:3px 6px;font-size:11px;font-weight:800;line-height:1.2}
#dailyLeaf .rew.got{background:#dff3cf}#dailyLeaf .rew img{width:24px;height:24px;object-fit:contain;flex:0 0 auto}
#dailyLeaf .streak{display:flex;gap:3px;justify-content:center;margin-top:7px}
#dailyLeaf .streak i{width:16px;height:16px;border-radius:50%;border:2px solid #3a2414;background:#e9e2d2;box-sizing:border-box;font:400 9px/12px Bangers,sans-serif;text-align:center;font-style:normal;color:#3a2414}
#dailyLeaf .streak i.on{background:#9fd18a}#dailyLeaf .streak i.now{background:#ff6fb5;color:#fff;transform:scale(1.15)}#dailyLeaf .streak i.shield{background:#aeeeff}
#dailyLeaf .sub{font-size:9.5px;text-align:center;color:#7a5a3c;margin-top:3px;letter-spacing:.04em}
#dailyLeaf .corner{position:absolute;right:-2px;bottom:-2px;width:22px;height:22px;background:linear-gradient(135deg,transparent 50%,#e9d9b8 50%);border-radius:0 0 12px 0}
@media (max-width:380px){#dailyLeaf{width:132px;top:calc(env(safe-area-inset-top,0px) + 92px)}}
#ovDaily{z-index:66}#ovDaily .dlBox{position:relative;width:min(380px,calc(100vw - 24px));background:#fff7e8;border:3px solid #3a2414;border-radius:18px;box-shadow:0 6px 0 #3a2414;padding:14px 14px 16px;color:#3a2414;font-family:"Baloo 2",system-ui,sans-serif;text-align:left}
#ovDaily h2{font-family:Bangers,system-ui;letter-spacing:1px;font-size:30px;margin:0 0 2px;text-align:center;color:var(--hero,#4fa3ff);-webkit-text-stroke:1px #3a2a1a}
#ovDaily .dlDay{text-align:center;font-weight:700;color:#7a5a3c;font-size:13px;margin-bottom:6px}
#ovDaily .dlSec{margin:10px 0 4px;font-family:Bangers,system-ui;font-size:18px;letter-spacing:.5px;display:flex;justify-content:space-between;align-items:baseline}#ovDaily .dlSec small{font:700 12px "Baloo 2",system-ui;color:#d94c8c}
#ovDaily .dlRow{display:grid;grid-template-columns:44px minmax(0,1fr) auto;gap:10px;align-items:center;background:#fff;border:2px solid #e6d6bb;border-radius:12px;padding:8px 10px}
#ovDaily .dlRow img{width:44px;height:44px;object-fit:contain}#ovDaily .dlRow b{display:block;font-size:15px;line-height:1.2}#ovDaily .dlRow span{display:block;font-size:12px;color:#7a5a3c}
#ovDaily .dlBig{font-family:Bangers,system-ui;font-size:26px;text-align:center;color:#d94c8c}
#ovDaily .dlRow button{min-height:36px;padding:4px 12px;font-size:14px;border-radius:999px}
#ovDaily .dlGot{font-family:Bangers,system-ui;color:#5f8a2e;letter-spacing:.5px;font-style:normal}
#ovDaily .dlChain{display:flex;gap:4px;justify-content:space-between}#ovDaily .dlChain i{flex:1;min-width:0;text-align:center;font-style:normal;border:2px solid #3a2414;border-radius:10px;background:#e9e2d2;padding:4px 0 3px;font:400 14px/1 Bangers,system-ui}
#ovDaily .dlChain i small{display:block;font:700 8.5px/1.1 "Baloo 2",system-ui;margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding:0 2px}
#ovDaily .dlChain i.on{background:#9fd18a}#ovDaily .dlChain i.now{background:#ff6fb5;color:#fff}
#ovDaily .dlNote{font-size:12px;color:#7a5a3c;margin-top:8px;text-align:center}
'''
rep('#btnOMap span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}\n</style>', '#btnOMap span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}\n' + CSS + '</style>')

open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
