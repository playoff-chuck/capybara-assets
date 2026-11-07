"""V402: t12 Nr. 7 – Bestwerte je Ort (Martin 07.11. 18:20: «7 Bestenliste je Ort»).
Je Ort (30) lokal: beste Sterne (gab es schon, capy-stars) + meiste Splats und Reihen innerhalb der 5 Wellen des Ortes
(neu, capy-place-rec). Anzeige: Hall of fame → Abschnitt «PLACE RECORDS» (nach Kontinent, nur erreichte Orte),
Weltkarte → geschafften Ort antippen zeigt zusätzlich die Bestwerte. Zählt auch beim REPLAY. Kein Balancing, keine Kosten.
Aufruf: python3 tools/patch402.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
# 1) Start-Stand je Ort um Splats erweitern
rep('''splat: S.splatN || 0, med: S.medGot || 0 };   /* V374: Sterne je Ort */''',
    '''splat: S.splatN || 0, med: S.medGot || 0, kills: S.kills || 0 };   /* V374: Sterne je Ort · V%d: Splats je Ort */''' % NEW)
# 2) Bestwerte beim Ortsende speichern
rep('''S.lastStars = { g: p.g, n, st }; const all = starsAll(); if (n > (all[p.g] || 0)) { all[p.g] = n; try { LS.set("capy-stars", JSON.stringify(all)); } catch (e) {} }''',
    '''S.lastStars = { g: p.g, n, st }; const all = starsAll(); if (n > (all[p.g] || 0)) { all[p.g] = n; try { LS.set("capy-stars", JSON.stringify(all)); } catch (e) {} }
        if (p.kills != null) { const rr = placeRecAll(), o = rr[p.g] || {}, k = Math.max(0, (S.kills || 0) - p.kills), l = Math.max(0, (S.lines || 0) - p.lines); rr[p.g] = { k: Math.max(o.k || 0, k), l: Math.max(o.l || 0, l) }; try { LS.set("capy-place-rec", JSON.stringify(rr)); } catch (e) {} }   /* V%d */''' % NEW)
# 3) Hilfsfunktionen
rep('''function starStr(n) { return "★".repeat(n) + "☆".repeat(5 - n); }''',
    '''function starStr(n) { return "★".repeat(n) + "☆".repeat(5 - n); }
function placeRecAll() { try { return JSON.parse(LS.get("capy-place-rec") || "{}") || {}; } catch (e) { return {}; } }   /* V%d: Bestwerte je Ort 0..29 {k: Splats, l: Reihen} */
function placeRecHtml() {
  const st = starsAll(), rr = placeRecAll(), nice = t => t.toLowerCase().replace(/\\b\\w/g, m => m.toUpperCase());
  const tot = Object.values(st).reduce((a, b) => a + (+b || 0), 0); let h = `<h4>PLACE RECORDS · ★ ${tot} / 150</h4>`, any = false;
  CONTS.forEach((C, c) => { const rows = C[2].map((nm, i) => { const g = c * 6 + i; if (!(g in st) && !rr[g]) return ""; any = true; const r = rr[g] || {};
      return `<div class="row prRow"><span>${g + 1}.</span><span>${nice(nm)}</span><span class="prSt">${starStr(+st[g] || 0)}</span><span>${r.k != null ? r.k + "✕ · " + (r.l || 0) + "≡" : "–"}</span></div>`; }).join("");
    if (rows) h += `<div class="prCont">${nice(C[1])}</div>` + rows; });
  return any ? h + `<div class="prKey">✕ splats · ≡ rows · best in that place's 5 waves</div>` : h + `<div class="row"><span>–</span><span>Clear a place to set your first record</span><span></span><span></span></div>`;
}''' % NEW)
# 4) Abschnitt in der Hall of fame
rep('''<div class="hs" id="hsList"></div><div class="hs" id="hsNuts"></div>''',
    '''<div class="hs" id="hsList"></div><div class="hs" id="hsNuts"></div><div class="hs" id="hsPlaces"></div>''')
rep('''$("btnHs").addEventListener("click", () => { const box = $("hsNuts"); box.innerHTML = "";''',
    '''$("btnHs").addEventListener("click", () => { try { $("hsPlaces").innerHTML = placeRecHtml(); } catch (e) {} });   /* V%d */
$("btnHs").addEventListener("click", () => { const box = $("hsNuts"); box.innerHTML = "";''' % NEW)
rep('''#hsNuts:empty{display:none}''',
    '''#hsNuts:empty{display:none}#hsPlaces:empty{display:none}#hsPlaces .prCont{margin:6px 0 1px;font:700 11px/1.2 var(--f-display),sans-serif;letter-spacing:.08em;text-transform:uppercase;opacity:.75}#hsPlaces .prSt{color:#e8a915;letter-spacing:-1px;white-space:nowrap}#hsPlaces .prKey{margin-top:5px;font-size:11px;opacity:.7}''')
# 5) Weltkarte: Bestwerte beim Antippen
rep('''label(contName(c), nice(CONTS[c][2][i]), `Cleared · best ${starStr(st)} · replay for more stars`);''',
    '''const pr = placeRecAll()[g]; label(contName(c), nice(CONTS[c][2][i]), `Cleared · best ${starStr(st)}${pr ? ` · ${pr.k}✕ ${pr.l || 0}≡` : ""} · replay for more stars`);   /* V%d */''' % NEW)
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
