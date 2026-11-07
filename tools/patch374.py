"""V374 (To-do 07/90, Martin 07.11. 13:06): 5 Sterne je Ort + Sterne auf der Karte + Windrose + Sterne-Statistik.
Kriterien je Ort (5 Wellen):
 ★1 Ort geschafft · ★2 kein Leben verloren · ★3 mindestens 5 Reihen · ★4 mindestens 5 Monster zerquetscht (Splat) · ★5 mindestens 1 Medaille verdient.
Bestwert je Ort bleibt gespeichert (localStorage «capy-stars»). Ort-Feier zeigt die echten Sterne statt immer drei."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V373";', 'const GAME_VER = "V374";')
# Zähler
rep('    m.dead = true; n++; S.kills += 5;', '    m.dead = true; n++; S.splatN = (S.splatN || 0) + 1; S.kills += 5;')
rep('  medalTag(); setTimeout(() => announce(`MEDAL ${S.medals}`', '  S.medGot = (S.medGot || 0) + 1; medalTag(); setTimeout(() => announce(`MEDAL ${S.medals}`')
rep('const SAVE_KEYS = ["rotN",', 'const SAVE_KEYS = ["pl", "splatN", "medGot", "lastStars", "rotN",')
# Ort-Beginn merken
rep('  S.wave++; queueIntros(S.wave);',
    '  S.wave++; queueIntros(S.wave);\n'
    '  if (!S.nuts && !S.testRun && (S.wave - 1) % 5 === 0) S.pl = { g: Math.floor((S.wave - 1) / 5), lives: S.lives, lines: S.lines || 0, splat: S.splatN || 0, med: S.medGot || 0 };   /* V374: Sterne je Ort */')
# Ort-Ende: Sterne berechnen und speichern
rep('      if (S.wave % 5 === 0) praise(`WAVE ${S.wave}!`',
    '      if (S.wave % 5 === 0 && !S.nuts && !S.testRun && S.pl && S.pl.g === Math.floor((S.wave - 1) / 5)) { const p = S.pl, st = [true, S.lives >= p.lives, (S.lines || 0) - p.lines >= 5, (S.splatN || 0) - p.splat >= 5, (S.medGot || 0) - p.med >= 1], n = st.filter(Boolean).length;   /* V374 */\n'
    '        S.lastStars = { g: p.g, n, st }; const all = starsAll(); if (n > (all[p.g] || 0)) { all[p.g] = n; try { LS.set("capy-stars", JSON.stringify(all)); } catch (e) {} }\n'
    '        setTimeout(() => toast(`PLACE STARS ${"★".repeat(n)}${"☆".repeat(5 - n)}`, "HQ", 2600), 2400); }\n'
    '      if (S.wave % 5 === 0) praise(`WAVE ${S.wave}!`')
# Hilfsfunktionen (vor startWave)
rep('function startWave() {',
    'function starsAll() { try { return JSON.parse(LS.get("capy-stars") || "{}") || {}; } catch (e) { return {}; } }   /* V374: Bestwert je Ort 0..29 */\n'
    'function starStr(n) { return "★".repeat(n) + "☆".repeat(5 - n); }\n'
    'function startWave() {')
# Feier: echte Sterne
rep('<em>★ ★ ★</em>', '<em>${S && S.lastStars ? starStr(S.lastStars.n) : "★ ★ ★"}</em>', 2)
# Karte: Sterne unter den Orten, Windrose + Statistik
rep('      pinsEl.innerHTML = h;',
    '      { const all = starsAll(); h = h.replace(/data-g="(\\d+)" style="([^"]*)"><i><\\/i>/g, (m0, gi, sty) => all[gi] ? `data-g="${gi}" style="${sty}"><i></i><b class="pStars">${"★".repeat(all[gi])}</b>` : m0); }   /* V374 */\n'
    '      pinsEl.innerHTML = h;\n'
    '      try { const all = starsAll(), v = Object.values(all), tot = v.reduce((a, b) => a + b, 0), cnt = [1, 2, 3, 4, 5].map(k => v.filter(x => x === k).length); let r = ov.querySelector(".mapRose");\n'
    '        if (!r) { r = document.createElement("div"); r.className = "mapRose"; ov.appendChild(r); }\n'
    '        r.innerHTML = `<svg viewBox="0 0 60 60" aria-hidden="true"><circle cx="30" cy="30" r="27" fill="#f3ead6" stroke="#3a2414" stroke-width="2.5"/><path d="M30 5 L35 30 L30 55 L25 30Z" fill="#3a2414"/><path d="M30 5 L35 30 L25 30Z" fill="#e0412c"/><path d="M5 30 L30 25 L55 30 L30 35Z" fill="#7a6a52"/><circle cx="30" cy="30" r="3.5" fill="#ffc93c" stroke="#3a2414" stroke-width="1.5"/><text x="30" y="14" text-anchor="middle" font-size="8" font-weight="700" fill="#fff">N</text></svg><div class="rsTot">★ ${tot} / 150</div><div class="rsCnt">${cnt.slice(0, 3).map((c, i) => `${i + 1}★ ${c}`).join(" · ")}<br>${cnt.slice(3).map((c, i) => `${i + 4}★ ${c}`).join(" · ")}</div>`; } catch (e) {}')
# CSS
rep('.mPin.done i{background:#ffc93c}',
    '.mPin.done i{background:#ffc93c}\n'
    '.mPin .pStars{position:absolute;left:50%;top:9px;transform:translateX(-50%);font-size:9px;line-height:1;letter-spacing:-1px;color:#ffc93c;text-shadow:0 0 2px #3a2414,0 0 2px #3a2414;white-space:nowrap;pointer-events:none}\n'
    '.mapRose{position:absolute;right:max(10px,env(safe-area-inset-right,0px));bottom:calc(env(safe-area-inset-bottom,0px) + 70px);z-index:5;display:flex;flex-direction:column;align-items:center;gap:2px;pointer-events:none;font:700 11px/1.1 system-ui,sans-serif;color:#fff;text-shadow:0 1px 2px #000}\n'
    '.mapRose svg{width:54px;height:54px;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}\n'
    '.mapRose .rsTot{font-size:13px;color:#ffc93c}\n'
    '.mapRose .rsCnt{font-size:9px;opacity:.9;text-align:center;line-height:1.25}')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
