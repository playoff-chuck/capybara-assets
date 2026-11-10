#!/usr/bin/env python3
# V583 (Martin 11.11. 01:11): Spielerliste zeigt nur echte Spieler
# - Test-Browser (Playwright/headless, navigator.webdriver) melden sich gar nicht mehr als Spieler
# - Martins Geräte melden «team» (Admin-Schlüssel oder Dev); alle Einträge mit demselben Gerätemodell zählen als Team
# - Einträge ohne gespielte Welle und unter 1 min (Tests, nur geöffnet) zählen nicht, außer gerade aktiv
# - Zähler oben nur echte Spieler; Knopf «Tests/Team zeigen» blendet den Rest ein
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V582";', 'const GAME_VER = "V583";')
rep('''      tut: localStorage.getItem("tarnturm-tut") === "1" ? 1 : 0, dev: localStorage.getItem("tarnturm-dev") === "1" ? 1 : 0, cs: !!localStorage.getItem("capy-cloudT") }; }''',
    '''      tut: localStorage.getItem("tarnturm-tut") === "1" ? 1 : 0, dev: localStorage.getItem("tarnturm-dev") === "1" ? 1 : 0, cs: !!localStorage.getItem("capy-cloudT"),
      team: (() => { try { return capyMe() ? 1 : 0; } catch (e) { return 0; } })() }; }   /* V583 */''')
rep('''  function profSend(start, force) { try { if (!force''', '''  function profSend(start, force) { try { if (navigator.webdriver) return;   /* V583: Test-Browser zählen nicht */ if (!force''')
rep('let LIST = [], NOW = Date.now(), scrollY = 0;', 'let LIST = [], NOW = Date.now(), scrollY = 0, SHOWALL = false;   /* V583 */')
rep('''  function renderList() { back.hidden = true; const L = LIST.slice().sort((a, b) => b.last - a.last);
    const today = LIST.filter(p => NOW - p.last < 86400000).length, week = LIST.filter(p => NOW - p.last < 7 * 86400000).length, now = LIST.filter(p => NOW - p.last < 600000).length;
    info.textContent = `${LIST.length} Spieler · groß = beste Welle · neueste oben`;
    let h = `<div class="aSum"><div><b>${LIST.length}</b><small>gesamt</small></div>''',
'''  function renderList() { back.hidden = true;
    /* V583: Tests und Team ausblenden */
    const model = p => devShort(p.d || {}), teamM = new Set(LIST.filter(p => (p.d || {}).team || (p.d || {}).dev).map(model).filter(m => / · /.test(m)));
    const isTest = p => { const d = p.d || {}; return !!d.bot || (!(Math.max(d.bw || 0, (d.cur && d.cur.w) || 0, d.cp || 0) > 0) && !((d.t || 0) > 60) && NOW - p.last > 600000); };   // Test-Browser oder nur geöffnet, nie gespielt
    const isTeam = p => { const d = p.d || {}; return !!d.team || !!d.dev || teamM.has(model(p)); };
    const REAL = LIST.filter(p => !isTest(p) && !isTeam(p)), hid = LIST.length - REAL.length, SRC = SHOWALL ? LIST : REAL;
    const L = SRC.slice().sort((a, b) => b.last - a.last);
    const today = REAL.filter(p => NOW - p.last < 86400000).length, week = REAL.filter(p => NOW - p.last < 7 * 86400000).length, now = REAL.filter(p => NOW - p.last < 600000).length;
    info.textContent = `${REAL.length} echte Spieler · groß = beste Welle · neueste oben`;
    let h = `<div class="aSum"><div><b>${REAL.length}</b><small>echte</small></div>''')
rep('''<div><b>${week}</b><small>7 Tage</small></div></div>`;
    if (!L.length)''', '''<div><b>${week}</b><small>7 Tage</small></div></div>`;
    if (hid) h += `<button type="button" class="aAll" style="display:block;width:100%;margin:0 0 10px;padding:8px;border:2px solid #3a2414;border-radius:12px;background:#fff6e3;font:inherit;color:#3a2414">${SHOWALL ? "Nur echte Spieler zeigen" : `+ ${hid} Tests/Team/nur geöffnet zeigen`}</button>`;
    if (!L.length)''')
rep('''<span class="aNm">${esc(d.nm || "– ohne Namen –")}${p.uid === "M2HL-KCQH" ? " (du)" : ""}</span>''',
    '''<span class="aNm">${esc(d.nm || "– ohne Namen –")}${isTeam(p) ? " (Team)" : isTest(p) ? " (Test)" : ""}</span>''')
rep('''body.addEventListener("click", e => { const r = e.target.closest(".aRow");''',
    '''body.addEventListener("click", e => { const a = e.target.closest(".aAll"); if (a) { SHOWALL = !SHOWALL; renderList(); return; } const r = e.target.closest(".aRow");''')
open(dst, "w", encoding="utf-8").write(s)
print("ok V583")
