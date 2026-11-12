#!/usr/bin/env python3
# V652 (Martin 12.11. 11:01): Dieb mitschreiben – Ereignis «thief» (come / steal / wolf / tap / gone) mit Gold und Welle,
# Zähler im Spielerprofil (thf: kam, stahl, Gold gestohlen, Gold zurück, Gold verloren, Wolf).
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V651";', 'const GAME_VER = "V652";')
rep('function wolfCall() {',
    'function thiefEv(a, d) { try { const C = JSON.parse(localStorage.getItem("capy-thf") || "{}"); const g = (d && d.g) | 0;   /* V652: Dieb mitschreiben */\n'
    '    if (a === "come") C.n = (C.n || 0) + 1; else if (a === "steal") { C.s = (C.s || 0) + 1; C.gs = (C.gs || 0) + g; } else if (a === "wolf") { C.wf = (C.wf || 0) + 1; C.gb = (C.gb || 0) + g; } else if (a === "gone") C.gl = (C.gl || 0) + g;\n'
    '    C.lw = (S && S.wave) | 0; C.lt = Date.now(); localStorage.setItem("capy-thf", JSON.stringify(C)); } catch (e) {}\n'
    '  try { window.__evLog && window.__evLog.push("thief", { d: Object.assign({ a, gold: (S && S.gold) | 0 }, d || {}) }); if (a !== "come") window.__evLog.flush(false); } catch (e) {} }\n'
    'function wolfCall() {')
rep('    if (k === "thief") D.thief = { x: -0.8, t: 0, stolen: 0 };',
    '    if (k === "thief") { D.thief = { x: -0.8, t: 0, stolen: 0 }; thiefEv("come", {}); }')
rep('if (!T.stolen && !T.flee && T.t >= 10) { T.stolen = Math.floor(S.gold / 2); S.gold -= T.stolen;',
    'if (!T.stolen && !T.flee && T.t >= 10) { T.stolen = Math.floor(S.gold / 2); S.gold -= T.stolen; thiefEv("steal", { g: T.stolen, wl: S.wolves | 0 });')
rep('      if (T.t >= 30) { if (T.stolen) toast(`THIEF GOT AWAY · −${T.stolen} gold`, "HQ", 1800); D.thief = null; } }',
    '      if (T.t >= 30) { thiefEv("gone", { g: T.stolen | 0 }); if (T.stolen) toast(`THIEF GOT AWAY · −${T.stolen} gold`, "HQ", 1800); D.thief = null; } }')
rep('setTimeout(() => { if (D.thief !== T) return; T.flee = true; const g = T.stolen || 0; T.stolen = 0; if (g) S.gold += g;',
    'setTimeout(() => { if (D.thief !== T) return; T.flee = true; const g = T.stolen || 0; T.stolen = 0; if (g) S.gold += g; thiefEv("wolf", { g });')
rep('    toast("Only a WOLF CALL scares him off · find it in the shop", "HQ", 1800); snd("nopeSoft"); return;',
    '    thiefEv("tap", {}); toast("Only a WOLF CALL scares him off · find it in the shop", "HQ", 1800); snd("nopeSoft"); return;')
# Profil
rep('      tut: localStorage.getItem("tarnturm-tut") === "1" ? 1 : 0,',
    '      thf: (() => { try { return JSON.parse(localStorage.getItem("capy-thf") || "null"); } catch (e) { return null; } })(),   /* V652 */\n'
    '      tut: localStorage.getItem("tarnturm-tut") === "1" ? 1 : 0,')
# Admin Spieler
rep('kv("Todesursachen", esc(byT))]);',
    'kv("Todesursachen", esc(byT)), kv("Dieb", d.thf ? `kam ${d.thf.n || 0}× · stahl ${d.thf.s || 0}× · ${num(d.thf.gs || 0)} Gold weg · ${num(d.thf.gb || 0)} per Wolf zurück · ${num(d.thf.gl || 0)} verloren · zuletzt W${d.thf.lw || 0}` : "noch nie (ab V652)")]);   /* V652 */')
# Admin Analyse
rep('      h += sec("TIPP-KARTEN", obj(x.tips));',
    '      h += sec("TIPP-KARTEN", obj(x.tips));\n'
    '      { const t = x.thief || {}; h += sec("DIEB (AB WELLE 100)", t.come || t.steal ? [kv("Aufgetaucht", num(t.come || 0)), kv("Gold gestohlen", `${num(t.steal || 0)}× · ${num(t.gs || 0)} Gold`), kv("Per Wolf zurück", `${num(t.wolf || 0)}× · ${num(t.gb || 0)} Gold`), kv("Entkommen mit Gold", `${num(t.gone || 0)}× · ${num(t.gl || 0)} Gold`), kv("Angetippt ohne Wolf", num(t.tap || 0))] : []); }   /* V652 */')
open(p, "w", encoding="utf-8").write(s)
print("ok V652")
