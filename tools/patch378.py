"""V378 (Martin 07.11. 13:35): Nuts-Territorien auf der Karte nicht formal-gleich, sondern je Kontinent ein seltsames,
abgeschlossenes, geheimnisvolles Bauwerk in Nebel, ringsum mit einem Zaun aus Totenköpfen abgesperrt.
Südamerika: versunkene schiefe Stufenpyramide · Afrika: geborstene Kuppel mit Riss · Asien: verdrehter Turm · Nordamerika: Bunker mit Antenne.
Unbesucht: grau, Fragezeichen. Besucht: glüht pink, kleines Schild «L x»."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V377";', 'const GAME_VER = "V378";')
rep('''          return `<div class="mNuts${b ? " on" : ""}" style="left:${(x * 100 - 6).toFixed(2)}%;top:${(y * 100 + 7).toFixed(2)}%"><span>☠ ${b ? "L" + b : "—"}</span></div>`; }).join(""));''',
'''          return `<div class="mNuts${b ? " on" : ""}" style="left:${(x * 100 - 6).toFixed(2)}%;top:${(y * 100 + 7).toFixed(2)}%"><span>${nzLair(c, b)}</span></div>`; }).join(""));''')
rep('function nzBest(c) {', '''function nzLair(c, b) {   /* V378: geheimnisvolles Sperrgebiet, je Kontinent anders */
  const R = [[34, 20, 0.9], [30, 23, 1.7], [27, 25, 2.6], [35, 19, 3.4]][c] || [32, 22, 1], cx = 40, cy = 34, N = 13;
  const pt = i => { const a = i / N * Math.PI * 2, w = 1 + 0.16 * Math.sin(a * 3 + R[2]) + 0.08 * Math.cos(a * 5 + R[2] * 2); return [cx + Math.cos(a) * R[0] * w, cy + Math.sin(a) * R[1] * w]; };
  const P = [...Array(N).keys()].map(pt), fence = P.map(p => p.map(v => v.toFixed(1)).join(",")).join(" ");
  const skull = ([x, y], i) => `<g transform="translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${(i * 37 % 30) - 15})"><line y1="2" y2="9" stroke="#2a1a22" stroke-width="1.6"/><circle r="3.6" fill="#efe6d6" stroke="#2a1a22" stroke-width=".8"/><rect x="-2" y="1.8" width="4" height="2.6" rx=".6" fill="#efe6d6" stroke="#2a1a22" stroke-width=".6"/><circle cx="-1.3" cy="-.3" r="1.05" fill="#1a0f14"/><circle cx="1.3" cy="-.3" r="1.05" fill="#1a0f14"/></g>`;
  const B = [ /* Bauwerke */
    '<path d="M22 46 L28 38 L33 38 L36 31 L42 31 L45 24 L51 26 L53 33 L57 34 L60 46Z" fill="#4a3a44" stroke="#1a0f14" stroke-width="1.2"/><path d="M45 24 L48 15 L51 26" fill="none" stroke="#1a0f14" stroke-width="1"/><circle cx="48" cy="34" r="2" class="nzEye"/>',
    '<path d="M24 46 Q26 22 42 20 Q58 22 58 46Z" fill="#3e3442" stroke="#1a0f14" stroke-width="1.2"/><path d="M42 20 L39 29 L44 33 L40 42" fill="none" class="nzCrack" stroke-width="1.6"/><ellipse cx="41" cy="46" rx="18" ry="2.5" fill="#1a0f14" opacity=".5"/>',
    '<path d="M36 47 L38 36 L33 33 L40 27 L36 22 L43 15 L42 9 L47 16 L45 23 L50 28 L44 33 L48 38 L46 47Z" fill="#45384a" stroke="#1a0f14" stroke-width="1.2"/><circle cx="42" cy="25" r="1.6" class="nzEye"/><circle cx="43" cy="37" r="1.3" class="nzEye"/>',
    '<path d="M22 46 L26 34 L56 34 L60 46Z" fill="#3f3a40" stroke="#1a0f14" stroke-width="1.2"/><rect x="31" y="38" width="7" height="3" fill="#1a0f14"/><rect x="43" y="38" width="7" height="3" fill="#1a0f14"/><path d="M48 34 L50 14 M46 20 L54 18 M47 25 L53 24" stroke="#1a0f14" stroke-width="1.2"/><circle cx="50" cy="13" r="1.8" class="nzEye"/>'][c] || '';
  return `<svg viewBox="0 0 80 64" aria-hidden="true"><ellipse cx="${cx}" cy="${cy + 2}" rx="${R[0] + 6}" ry="${R[1] + 5}" class="nzFog"/><polygon points="${fence}" fill="rgba(30,14,26,.55)" stroke="#2a1a22" stroke-width="1.2" stroke-dasharray="2 1.5"/>${B}${P.filter((p, i) => p[1] < cy).map(skull).join("")}${b ? "" : '<text x="41" y="34" text-anchor="middle" class="nzQ">?</text>'}${P.filter((p, i) => p[1] >= cy).map(skull).join("")}</svg>${b ? `<i class="nzL">☠ L${b}</i>` : ""}`;
}
function nzBest(c) {''')
rep('''.mNuts span{position:absolute;left:0;top:0;transform:translate(-50%,-50%) scale(var(--ik,1));white-space:nowrap;font:700 13px/1 system-ui,sans-serif!important;padding:4px 8px!important;border-radius:10px;width:auto!important;height:auto!important;min-width:0!important;background:rgba(40,20,40,.55);color:#ddd;border:1.5px dashed #b9a;opacity:.75}
.mNuts.on span{background:#3a1430;color:#ff9fd0;border:1.5px solid #ff6fb5;opacity:1;box-shadow:0 0 8px rgba(255,111,181,.6)}''',
'''.mNuts span{position:absolute;left:0;top:0;transform:translate(-50%,-50%) scale(var(--ik,1));width:80px!important;height:64px!important;min-width:0!important;padding:0!important;background:none!important;border:0!important;display:block;filter:grayscale(.7) brightness(.85)}
.mNuts span svg{width:80px;height:64px;display:block;overflow:visible}
.mNuts .nzFog{fill:rgba(120,90,140,.35);animation:nzFog 5s ease-in-out infinite alternate}
.mNuts .nzEye{fill:#9a8aa0}
.mNuts .nzCrack{stroke:#9a8aa0}
.mNuts .nzQ{font:700 18px/1 system-ui,sans-serif;fill:#d9cfe0;opacity:.8;animation:nzQ 2.6s ease-in-out infinite}
.mNuts.on span{filter:drop-shadow(0 0 6px rgba(255,80,170,.7))}
.mNuts.on .nzFog{fill:rgba(255,70,170,.32)}
.mNuts.on .nzEye{fill:#ff5fb0;animation:nzEye 1.8s steps(2) infinite}
.mNuts.on .nzCrack{stroke:#ff5fb0}
.mNuts .nzL{position:absolute;left:50%;bottom:-6px;transform:translateX(-50%);font:700 10px/1 system-ui,sans-serif;font-style:normal;color:#ffd0ea;background:#3a1430;border:1px solid #ff6fb5;border-radius:6px;padding:2px 5px;white-space:nowrap}
@keyframes nzFog{from{opacity:.6;transform:scale(.96)}to{opacity:1;transform:scale(1.05)}}
@keyframes nzQ{50%{opacity:.35}}
@keyframes nzEye{50%{opacity:.25}}
@media (prefers-reduced-motion:reduce){.mNuts *{animation:none!important}}''')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
