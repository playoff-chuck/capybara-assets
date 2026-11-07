#!/usr/bin/env python3
# V430 (Dauer-Arbeiter d-1842, t13/t110): 60 Mini-Missionen, XP-only für Squad Level (kein Balancing-Eingriff).
# 3 Missionen gleichzeitig, 15 Arten × 4 Stufen; Belohnung 100/200/400/800 XP (zählt in sqXP). Waffen-Missionen erst nach Freischaltung (beste Welle).
# Neue Mission meldet der General in der Wellenpause («NEW MISSION», nur bei leerer Meldungs-Warteschlange); erledigt → Toast «MISSION COMPLETE».
# Anzeige: Pausemenü (kompakt) + Squad File «MISSIONS x / 60». Speicher capy-msn (Cloud save automatisch). Keine Zählung in Testläufen.
# Fix: seit V421 warf «snd = function» (const snd) im V331-Block «Assignment to constant variable» → alle Rosie/Blue-Haken danach waren aus.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V429";', 'const GAME_VER = "V430";')
rep('const snd = (n, ...a) => SFX.play(n, ...a);', 'let snd = (n, ...a) => SFX.play(n, ...a);   /* V430: let – V421 umhüllt snd */')
rep('S.inWave = false; if (S.nuts) nutsLevelDone(); else {', 'S.inWave = false; try { window.__msnEv && window.__msnEv("wave", S.waveLeaks || 0); } catch (e) {} if (S.nuts) nutsLevelDone(); else {')
rep('function buddyHelp(kind) {', 'function buddyHelp(kind) { try { window.__msnEv && window.__msnEv("use_" + kind); } catch (e) {}')
rep('if (c) { S.lines += c;', 'if (c) { S.lines += c; try { window.__msnEv && window.__msnEv("clr", c); } catch (e) {}', 3)
rep('function sqXP(L) { L = L || sqLife(); return (L.k || 0) + 10 * (L.l || 0) + 50 * (L.w || 0); }',
    'function sqXP(L) { L = L || sqLife(); return (L.k || 0) + 10 * (L.l || 0) + 50 * (L.w || 0) + msnXP(); }   /* V430: + Missions-XP */')
rep('let h = sqHtml() + trophyHtml()', 'let h = sqHtml() + msnHtml() + trophyHtml()')
rep('<p class="pauseHint" id="pauseHint">', '<div class="pMsn" id="pMsn"></div><p class="pauseHint" id="pauseHint">')
CODE = r'''/* V430: Mini-Missionen (t13) – XP-only, 3 gleichzeitig, 60 in 4 Stufen */
const MSN_T = [   /* id, Text, Ziele je Stufe, Waffe (Freischaltung) */
  ["k", "Splat {n} monsters", [40, 120, 300, 800]],
  ["l", "Clear {n} lines", [10, 25, 60, 150]],
  ["c2", "Clear 2+ lines at once ×{n}", [1, 3, 6, 12]],
  ["c3", "Clear 3+ lines at once ×{n}", [1, 2, 4, 8]],
  ["c4", "Clear 4 lines at once ×{n}", [1, 1, 2, 4]],
  ["w", "Finish {n} waves", [3, 8, 20, 40]],
  ["p", "Finish {n} waves without losing a life", [2, 5, 10, 20]],
  ["t", "Build {n} towers", [2, 5, 10, 20]],
  ["sp", "Squish {n} monsters with a falling block", [2, 8, 20, 50]],
  ["ton", "Drop {n} Ten-ton", [1, 2, 3, 5], "ton"],
  ["mix", "Use {n} Concrete mixer", [1, 2, 3, 5], "mix"],
  ["snipe", "Use {n} Sniper strike", [1, 2, 4, 6], "snipe"],
  ["chomp", "Send out {n} Chomper", [1, 2, 3, 5], "chomp"],
  ["tesla", "Use {n} Tesla storm", [1, 2, 3, 5], "tesla"],
  ["lock", "Use {n} Lockdown", [1, 2, 3, 4], "lock"]];
const MSN_XP = [100, 200, 400, 800];
function msnId(ti, s) { return MSN_T[ti][0] + s; }
function msnDef(id) { const s = +id.slice(-1), ti = MSN_T.findIndex(t => t[0] === id.slice(0, -1)); if (ti < 0) return null; const t = MSN_T[ti], n = t[2][s];
  return { id, s, ti, key: t[0], n, w: t[3], xp: MSN_XP[s], txt: t[1].replace("{n}", n.toLocaleString("en-US")).replace(/ ×1$/, "") + (n === 1 || !t[3] ? "" : "s") }; }
function msnLoad() { let M = null; try { M = JSON.parse(localStorage.getItem("capy-msn") || "null"); } catch (e) {} if (!M || typeof M !== "object") M = {}; M.a = Array.isArray(M.a) ? M.a : []; M.p = M.p || {}; M.d = Array.isArray(M.d) ? M.d : []; M.xp = +M.xp || 0; return M; }
let MSN = msnLoad();
function msnSave() { try { localStorage.setItem("capy-msn", JSON.stringify(MSN)); } catch (e) {} }
function msnXP() { return (MSN && +MSN.xp) || 0; }
function msnBestW() { let b = 0; try { const st = starsAll(), k = Object.keys(st).map(Number); if (k.length) b = Math.max(...k) * 5 + 5; } catch (e) {} try { if (S && S.wave) b = Math.max(b, S.wave); } catch (e) {} return b; }
function msnOk(d, bw) { return !d.w || bw >= unlockedAt(d.w); }
function msnPick(free) { const bw = msnBestW(), done = new Set(MSN.d), act = new Set(MSN.a.map(id => id.slice(0, -1))), hasW = !free && MSN.a.some(id => (msnDef(id) || {}).w);   /* höchstens 1 Waffen-Mission gleichzeitig */
  const tier = Math.min(3, Math.floor(MSN.d.length / 15));
  for (let s = 0; s <= 3; s++) { const order = [tier, ...[0, 1, 2, 3].filter(x => x !== tier)][s];   /* zuerst aktuelle Stufe, dann die übrigen */
    const c = MSN_T.map((t, ti) => msnDef(msnId(ti, order))).filter(d => d && !done.has(d.id) && !act.has(d.key) && msnOk(d, bw) && !(hasW && d.w) && (order === 0 || done.has(d.key + (order - 1))));
    if (c.length) return c[Math.floor(Math.random() * c.length)].id; }
  return free ? null : msnPick(true); }
function msnFill(announceNew) { let added = 0; while (MSN.a.length < 3) { const id = msnPick(); if (!id) break; MSN.a.push(id); MSN.p[id] = 0; added++; if (announceNew) MSN.q = (MSN.q || []).concat(id); } if (added) msnSave(); return added; }
let msnTQ = [];
function msnAdd(key, v) { if (!v || v <= 0) return; try { if (!S || !S.started || S.over || S.testRun) return; } catch (e) { return; }
  let ch = false;
  for (const id of MSN.a.slice()) { if (id.slice(0, -1) !== key) continue; const d = msnDef(id); if (!d) continue;
    MSN.p[id] = Math.min(d.n, (MSN.p[id] || 0) + v); ch = true;
    if (MSN.p[id] >= d.n) { MSN.a = MSN.a.filter(x => x !== id); delete MSN.p[id]; MSN.d.push(id); MSN.xp += d.xp; msnTQ.push(d); msnFill(true); } }
  if (ch) msnSave(); }
window.__msnEv = (k, c) => { if (k === "wave") { if (S && S.lives > 0 && !S.over) { msnAdd("w", 1); if (!(c > 0)) msnAdd("p", 1); } return; }
  if (k === "clr") { if (c >= 2) msnAdd("c2", 1); if (c >= 3) msnAdd("c3", 1); if (c >= 4) msnAdd("c4", 1); return; }
  if (k.startsWith("use_")) msnAdd(k.slice(4), 1); };
let msnB = null, msnFirstSaid = false, msnTT = -1e9;
function msnIdle() { try { return !MSGQ.length && msgBusy < performance.now(); } catch (e) { return true; } }
function msnCalm() { try { return !uiWinOpen() && !frozen() && !S.paused && !(typeof TUT !== "undefined" && TUT.on) && !overShown() && !S.mapShow && !S.mapFly; } catch (e) { return false; } }
setInterval(() => { try {
  if (!S || !S.started || S.over || S.testRun) { msnB = null; return; }
  if (!MSN.a.length && !MSN.d.length) msnFill(false);
  const cur = { S, k: S.kills || 0, l: S.lines || 0, t: S.towersBuilt || 0, sp: S.splatN || 0 };
  if (msnB && msnB.S === S) {
    const dk = cur.k - msnB.k, dl = cur.l - msnB.l, dt = cur.t - msnB.t, ds = cur.sp - msnB.sp;
    if (dk > 0 && dk < 5000) msnAdd("k", dk); if (dl > 0 && dl < 200) msnAdd("l", dl); if (dt > 0 && dt < 50) msnAdd("t", dt); if (ds > 0 && ds < 500) msnAdd("sp", ds);
  }
  msnB = cur;
  if (msnTQ.length && msnCalm() && msnIdle() && performance.now() - msnTT > 3500) { msnTT = performance.now(); const d = msnTQ.shift(); toast(`MISSION COMPLETE · ${d.txt} · +${d.xp} XP`, "SQUAD", 2600); try { snd("powerup"); } catch (e) {} }
  else if (!S.inWave && msnCalm() && msnIdle() && S.wave >= 3) {
    if (!msnFirstSaid && !LS.get("capy-msn-hi") && MSN.a.length) { msnFirstSaid = true; LS.set("capy-msn-hi", "1"); MSN.q = []; msnSave(); announce("3 MISSIONS FOR YOU", "Pause shows them · each one gives Squad XP", "HQ", 3200); }
    else if (MSN.q && MSN.q.length && performance.now() - (window.__msgShowT || -1e9) > 4000) { MSN.q = MSN.q.filter(x => MSN.a.includes(x)); const id = MSN.q.shift(); msnSave(); const d = id && msnDef(id); if (d) announce("NEW MISSION", d.txt, "HQ", 2600); }
  }
  const pm = $("pMsn"); if (pm && !$("ovPause").hidden) { const h = msnRows(true); if (pm.innerHTML !== h) pm.innerHTML = h; }
} catch (e) {} }, 500);
function msnRows(small) { if (!MSN.a.length) msnFill(false);
  const rows = MSN.a.map(id => { const d = msnDef(id); if (!d) return ""; const p = MSN.p[id] || 0, pc = Math.round(100 * p / d.n);
    return `<div class="msnRow"><span>${d.txt}</span><b>${p.toLocaleString("en-US")}/${d.n.toLocaleString("en-US")}</b><i style="width:${Math.max(3, pc)}%"></i></div>`; }).join("");
  return small ? `<small>MISSIONS · ${MSN.d.length} / 60</small>${rows || '<div class="msnRow"><span>All missions done!</span></div>'}` : rows; }
function msnHtml() { return `<div class="albSec">MISSIONS<span>${MSN.d.length} / 60 · ${MSN.xp.toLocaleString("en-US")} XP</span></div><div class="msnBox">${msnRows(false) || '<div class="msnRow"><span>All missions done!</span></div>'}</div>`; }
try { const st = document.createElement("style"); st.textContent = `.pMsn{margin:6px 0 0;text-align:left}.pMsn small{display:block;font-family:var(--f-display);letter-spacing:.06em;font-size:13px;opacity:.85;margin-bottom:2px}
.msnRow{position:relative;display:flex;justify-content:space-between;gap:6px;background:#fff;border:2px solid #d8c7a6;border-radius:10px;padding:3px 8px 5px;margin:0 0 3px;font-size:11px;font-weight:800;line-height:1.15;color:#3a2a1a;overflow:hidden}
.msnRow b{font-family:Bangers,system-ui;font-weight:400;font-size:13px;letter-spacing:.5px;white-space:nowrap}.msnRow i{position:absolute;left:0;bottom:0;height:3px;background:#7cc35a}
.msnBox{margin-bottom:6px}`; document.head.appendChild(st); } catch (e) {}
window.__msn = { get M() { return MSN; }, add: (k, v) => msnAdd(k, v), reset: () => { MSN = msnLoad(); }, def: id => msnDef(id), tq: () => msnTQ.length, calm: () => msnCalm() };   /* Test-Haken */

'''
rep('/* V410: Turm-Skins je Kontinent (t12 Nr. 3) */', CODE + '/* V410: Turm-Skins je Kontinent (t12 Nr. 3) */')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
