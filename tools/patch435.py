#!/usr/bin/env python3
# V435 (t14): 10 Herausforderungs-Links an Freunde (?ch=...), Squad File «CHALLENGES», Ergebnis lokal, «CHALLENGE DONE!»
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V434";', 'const GAME_VER = "V435";')

# Share-Texte mit Herausforderungs-Link
rep('Can you get 5? ${SHARE_URL}`', 'Can you beat it? ${chUrl("st", o.n || 1, o.g)}`')
rep('points! Can you beat me? ${SHARE_URL}`', 'points! Can you beat me? ${chUrl("sc", sc)}`', 2)

# Squad File
rep('let h = sqHtml() + msnHtml() + trophyHtml()', 'let h = sqHtml() + msnHtml() + chHtml() + trophyHtml()')

# Boss-Duell gewonnen
rep('HK.phase = "done"; const win = mine > 6;', 'HK.phase = "done"; const win = mine > 6; try { if (win && !HK.coach && S && !S.testRun) chHit("hk", 1); } catch (e) {}')

CODE = r'''
/* V435 (t14): 10 Herausforderungen an Freunde – Link ?ch=<art>-<wert>[-<ort>], Ergebnis nur lokal (capy-ch), keine Belohnung */
const CH_T = { sc: "Beat my score of {v}", w: "Reach wave {v}", st: "Get {v} ★ at {p}", k1: "Splat 100 monsters in one wave", c4: "Clear 4 lines at once",
  nz: "Reach Nuts level 10", ct: "Clear a continent without a Ten-ton", pw: "Finish 10 waves in a row without losing a life", hk: "Hack a boss on the first try", sp: "Squish 10 monsters with falling blocks in one wave" };
const CH_LATER = { sc: "Beat my score · play a run first", w: "Reach my wave · play a run first", st: "Stars at a place · clear a place first" };
const CH_ORD = ["sc", "w", "st", "k1", "c4", "nz", "ct", "pw", "hk", "sp"];
function chPlace(g) { try { return wherePos(g * 5 + 1).place; } catch (e) { return "place " + (g + 1); } }
function chTxt(c) { return (CH_T[c.k] || "").replace("{v}", (+c.v || 0).toLocaleString("en-US")).replace("{p}", chPlace(+c.g || 0)); }
function chOkVal(k, v, g) { if (!CH_T[k]) return false; if (k === "sc") return v >= 1 && v <= 1e12; if (k === "w") return v >= 2 && v <= 150; if (k === "st") return v >= 1 && v <= 5 && g >= 0 && g <= 29; return true; }
function chUrl(k, v, g) { if (k === "sc" && !(+v >= 1)) return SHARE_URL; return SHARE_URL + "/?ch=" + k + (v != null ? "-" + Math.round(+v || 0) : "") + (g != null ? "-" + (g | 0) : ""); }
function chLoad() { let a = null; try { a = JSON.parse(localStorage.getItem("capy-ch") || "null"); } catch (e) {} return Array.isArray(a) ? a.filter(c => c && CH_T[c.k]) : []; }
let CH = chLoad(); const chTQ = [];
function chSave() { try { localStorage.setItem("capy-ch", JSON.stringify(CH)); } catch (e) {} }
(() => { try { const q = new URLSearchParams(location.search), raw = (q.get("ch") || "").toLowerCase(); if (!raw) return;
  q.delete("ch"); try { history.replaceState(null, "", location.pathname + (q.toString() ? "?" + q : "") + location.hash); } catch (e) {}
  const m = /^([a-z0-9]{1,3})(?:-(\d{1,12}))?(?:-(\d{1,2}))?$/.exec(raw); if (!m) return; const k = m[1], v = m[2] != null ? +m[2] : 1, g = m[3] != null ? +m[3] : null;
  if (!chOkVal(k, v, g)) return; const c = { k, v, t: Date.now() }; if (k === "st") c.g = g;
  CH = CH.filter(x => !(x.k === k && (k !== "st" || x.g === g))); CH.unshift(c); CH = CH.slice(0, 10); chSave(); } catch (e) {} })();
function chHit(k, val, g) { let ch = false;
  for (const c of CH) { if (c.d || c.k !== k) continue; if (k === "st" && c.g !== g) continue; if ((k === "sc" || k === "w" || k === "st") && !(val >= c.v)) continue;
    c.d = Date.now(); ch = true; chTQ.push(c); }
  if (ch) chSave(); }
{ const _me = window.__msnEv; window.__msnEv = (k, c) => { try { _me && _me(k, c); } catch (e) {} try { if (!S || !S.started || S.over || S.testRun) return;
    if (k === "clr" && c >= 4) chHit("c4", 1);
    else if (k === "use_ton" && S.chCt) S.chCt.ok = false;
    else if (k === "wave" && !S.nuts && !S.replay) { S.chPW = c > 0 ? 0 : (S.chPW || 0) + 1; if (S.chPW >= 10) chHit("pw", 1);
      if (S.wave % 30 === 0 && S.chCt && S.chCt.ok && S.chCt.ci === S.wave / 30 - 1 && !(c > 0 && S.lives <= 0)) chHit("ct", 1); }
  } catch (e) {} }; }
let chB = null, chLS = null, chHiT = -1e9;
setInterval(() => { try {
  if (!S || !S.started || S.over || S.testRun) { chB = null; return; }
  const main = !S.nuts && !S.replay;
  if (main) { const sc = S.score || 0; if (sc > (+LS.get("capy-ch-best") || 0)) LS.set("capy-ch-best", sc); chHit("sc", sc); chHit("w", S.wave || 0);
    if (S.inWave && S.wave % 30 === 1 && (!S.chCt || S.chCt.ci !== (S.wave - 1) / 30)) S.chCt = { ci: (S.wave - 1) / 30, ok: true }; }
  if (S.nuts && (S.nuts.cleared || 0) >= 10) chHit("nz", 1);
  if (S.lastStars && S.lastStars !== chLS) { chHit("st", S.lastStars.n || 0, S.lastStars.g); chLS = S.lastStars; }
  if (!S.nuts) { if (S.inWave) { if (!chB || chB.S !== S || chB.w !== S.wave) chB = { S, w: S.wave, k: S.kills || 0, sp: S.splatN || 0 };
      else { if ((S.kills || 0) - chB.k >= 100) chHit("k1", 1); if ((S.splatN || 0) - chB.sp >= 10) chHit("sp", 1); } } else chB = null; }
  if (!msnCalm() || !msnIdle() || performance.now() - msnTT < 3500) return;
  if (chTQ.length) { msnTT = performance.now(); const c = chTQ.shift(); toast(`CHALLENGE DONE! · ${chTxt(c)}`, "SQUAD", 2800); try { snd("powerup"); } catch (e) {} return; }
  const nw = CH.find(c => !c.a && !c.d); if (nw && !S.inWave && performance.now() - chHiT > 6000 && performance.now() - (window.__msgShowT || -1e9) > 4000) { chHiT = performance.now(); nw.a = 1; chSave(); announce("FRIEND CHALLENGE", chTxt(nw), "HQ", 3000); }
} catch (e) {} }, 500);
function chSendVal(k) { if (k === "sc") { const b = +LS.get("capy-ch-best") || 0; return b > 0 ? { v: b } : null; }
  if (k === "w") { const b = msnBestW(); return b >= 2 ? { v: Math.min(150, b) } : null; }
  if (k === "st") { const st = starsAll(); let g = -1, n = 0; for (const [kk, vv] of Object.entries(st)) if ((+vv || 0) >= n && +vv > 0) { n = +vv; g = +kk; } return g >= 0 ? { v: n, g } : null; }
  return {}; }
function chHtml() { const f = c => c.d ? `<b>✓ DONE</b>` : `<b>OPEN</b>`;
  const got = CH.length ? CH.map(c => `<div class="msnRow chRow${c.d ? " chDone" : ""}"><span>${chTxt(c)}</span>${f(c)}</div>`).join("") : `<div class="msnRow"><span>Friends can send you challenges with a link.</span></div>`;
  const send = CH_ORD.map(k => { const o = chSendVal(k), c = o ? { k, v: o.v, g: o.g } : null;
    return `<div class="msnRow chRow"><span>${c ? chTxt(c) : CH_LATER[k]}</span>${c ? `<button type="button" class="chSend" data-ch="${k}">SEND</button>` : `<b style="opacity:.5">LATER</b>`}</div>`; }).join("");
  return `<div class="albSec">FRIEND CHALLENGES<span>${CH.filter(c => c.d).length} / ${CH.length}</span></div><div class="msnBox">${got}</div><div class="albSec">CHALLENGE A FRIEND<span>10</span></div><div class="msnBox chBox">${send}</div>`; }
let chBusy = false;
async function chSend(k, btn) { if (chBusy) return; const o = chSendVal(k); if (!o) return; chBusy = true;
  const c = { k, v: o.v, g: o.g }, url = chUrl(k, k === "sc" || k === "w" || k === "st" ? o.v : null, k === "st" ? o.g : null), text = `Capybara Squad challenge: ${chTxt(c)}! Can you do it?`;
  try { if (navigator.share) { try { await navigator.share({ title: "Capybara Squad", text, url }); } catch (e) {} return; }
    try { await navigator.clipboard.writeText(text + " " + url); if (btn) btn.textContent = "COPIED!"; } catch (e) { if (btn) btn.textContent = "…"; try { toast(url.replace("https://", ""), "SQUAD", 3500); } catch (er) {} } }
  finally { chBusy = false; } }
document.addEventListener("click", e => { const b = e.target.closest && e.target.closest(".chSend"); if (!b) return; e.stopPropagation(); try { SFX.init(); snd("uiTap"); } catch (er) {} chSend(b.dataset.ch, b); });
try { const st = document.createElement("style"); st.textContent = `.chRow{align-items:center}.chRow.chDone{background:#eef8e6;border-color:#9cc97a}.chRow.chDone b{color:#4f7a2a}
#ovSquad .chSend{flex:none!important;width:auto!important;min-width:0!important;height:22px!important;min-height:0!important;margin:0!important;padding:0 10px!important;border-radius:999px!important;border:2px solid #3a2414!important;background:#ff5fa2!important;box-shadow:0 2px 0 #3a2414!important;color:#fff!important;font-family:Bangers,system-ui!important;font-size:13px!important;letter-spacing:.5px!important;line-height:1!important;cursor:pointer;transform:none!important}
#ovSquad .chSend::before,#ovSquad .chSend::after{display:none!important}`; document.head.appendChild(st); } catch (e) {}
window.__ch = { get L() { return CH; }, hit: (k, v, g) => chHit(k, v, g), tq: () => chTQ.length, html: () => chHtml(), url: (k, v, g) => chUrl(k, v, g), reload: () => { CH = chLoad(); } };   /* Test-Haken */
'''
anchor = 'document.addEventListener("click", e => { if (!e.target.closest("#btnShare")) return; try { SFX.init(); snd("uiTap"); } catch (er) {} shareResult({ kind: "over" }); });\n'
rep(anchor, anchor + CODE.lstrip("\n"))
open(dst, "w", encoding="utf-8").write(s)
print("ok", len(s))
