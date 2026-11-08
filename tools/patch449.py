#!/usr/bin/env python3
"""V449 Weltkarte (Martin 08.11. 11:50): Nuts-Territorien geheimnisvoll statt tot – je Kontinent in dunkler Kontinentfarbe
(Südamerika Dschungelgrün, Afrika Wüstengold, Asien Eisblau, Nordamerika Canyon-Rot): farbiger Nebel, leuchtende Irrlichter,
glimmende Augen, Zaun in Akzentfarbe; kein Grau-Filter mehr. Ortsschilder und Pins liegen jetzt über den Territorien.
Nutzung: python3 tools/patch449.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('GAME_VER = "V448"', 'GAME_VER = "V449"')

# Farben je Kontinent + Irrlichter + farbiger Nebel
rep('function nzLair(c, b) {   /* V378: geheimnisvolles Sperrgebiet, je Kontinent anders */',
    '''const NZ_COL = [ /* V449: dunkle Kontinentfarbe + Leuchtakzent */
  { b: "rgba(10,48,30,.78)", f: "rgba(60,170,110,.38)", a: "#7dffb8", e: "#5cf0a0" },
  { b: "rgba(70,42,8,.78)", f: "rgba(230,160,50,.36)", a: "#ffd27a", e: "#ffb347" },
  { b: "rgba(12,38,70,.78)", f: "rgba(110,190,240,.38)", a: "#aeeeff", e: "#7fdcff" },
  { b: "rgba(62,18,12,.78)", f: "rgba(230,100,60,.36)", a: "#ffb08a", e: "#ff8a5a" }];
const nzVars = c => { const K = NZ_COL[c] || NZ_COL[0]; return `--nzB:${K.b};--nzF:${K.f};--nzA:${K.a};--nzE:${K.e}`; };
function nzLair(c, b) {   /* V378: geheimnisvolles Sperrgebiet, je Kontinent anders · V449: in Kontinentfarbe, geheimnisvoll */''')
rep('''  return `<svg viewBox="0 0 80 64" aria-hidden="true"><ellipse cx="${cx}" cy="${cy + 2}" rx="${R[0] + 6}" ry="${R[1] + 5}" class="nzFog"/><polygon points="${fence}" fill="rgba(30,14,26,.55)" stroke="#2a1a22" stroke-width="1.2" stroke-dasharray="2 1.5"/>''',
'''  const K = NZ_COL[c] || NZ_COL[0], wisps = [[-14, -6, 0], [10, -10, 1.1], [16, 8, 2.3], [-8, 12, 0.6]].map(([dx, dy, d], i) => `<circle cx="${cx + dx}" cy="${cy + dy}" r="${1.6 + (i % 2) * 0.6}" class="nzWisp" style="animation-delay:${d}s"/>`).join("");
  return `<svg viewBox="0 0 80 64" aria-hidden="true"><ellipse cx="${cx}" cy="${cy + 2}" rx="${R[0] + 7}" ry="${R[1] + 6}" class="nzFog"/><ellipse cx="${cx - 6}" cy="${cy + 6}" rx="${R[0] * 0.7}" ry="${R[1] * 0.5}" class="nzFog nzFog2"/><polygon points="${fence}" class="nzFence" stroke-width="1.2" stroke-dasharray="2 1.5"/>${wisps}''')

# CSS: kein Grau-Filter, Farben über Variablen, Irrlichter, Pins über den Territorien
rep('.mNuts span{position:absolute;left:0;top:0;transform:translate(-50%,-50%) scale(var(--ik,1));width:80px!important;height:64px!important;min-width:0!important;padding:0!important;background:none!important;border:0!important;display:block;filter:grayscale(.7) brightness(.85)}',
    '.mNuts span{position:absolute;left:0;top:0;transform:translate(-50%,-50%) scale(var(--ik,1));width:80px!important;height:64px!important;min-width:0!important;padding:0!important;background:none!important;border:0!important;display:block;filter:drop-shadow(0 0 7px var(--nzF,rgba(120,90,140,.5)))}\n'
    '.mNuts{z-index:1}.mPin{z-index:3}   /* V449: Schilder und Pins über den Territorien */\n'
    '.nzFence{fill:var(--nzB,rgba(30,14,26,.55));stroke:var(--nzA,#2a1a22);stroke-opacity:.85}\n'
    '.nzWisp{fill:var(--nzA,#d9cfe0);opacity:0;animation:nzWisp 3.6s ease-in-out infinite}\n'
    '@keyframes nzWisp{0%{opacity:0;transform:translateY(0)}35%{opacity:.95}70%{opacity:.4}100%{opacity:0;transform:translateY(-7px)}}\n'
    '.nzFog2{animation-duration:7s;animation-direction:alternate-reverse}')
rep('.mNuts .nzFog{fill:rgba(120,90,140,.35);animation:nzFog 5s ease-in-out infinite alternate}', '.mNuts .nzFog{fill:var(--nzF,rgba(120,90,140,.35));animation:nzFog 5s ease-in-out infinite alternate}')
rep('.mNuts .nzEye{fill:#9a8aa0}', '.mNuts .nzEye{fill:var(--nzE,#9a8aa0);animation:nzEye 2.4s steps(2) infinite}')
rep('.mNuts .nzCrack{stroke:#9a8aa0}', '.mNuts .nzCrack{stroke:var(--nzA,#9a8aa0)}')
rep('.mNuts.on span{filter:drop-shadow(0 0 6px rgba(255,80,170,.7))}', '.mNuts.on span{filter:drop-shadow(0 0 9px var(--nzA,rgba(255,80,170,.7)))}')
rep('.mNuts.on .nzFog{fill:rgba(255,70,170,.32)}', '.mNuts.on .nzFog{fill:var(--nzF,rgba(255,70,170,.32))}')
rep('<div class="mNuts${b ? " on" : ""}" style="left:${(x * 100 - 6).toFixed(2)}%;top:${(y * 100 + 7).toFixed(2)}%"><span>${nzLair(c, b)}</span></div>',
    '<div class="mNuts${b ? " on" : ""}" style="left:${(x * 100 - 6).toFixed(2)}%;top:${(y * 100 + 7).toFixed(2)}%"><span style="${nzVars(c)}">${nzLair(c, b)}</span></div>')
# Totenköpfe: geisterhaft in Akzentfarbe, nur jeder zweite Pfosten
rep('<circle r="3.6" fill="#efe6d6" stroke="#2a1a22" stroke-width=".8"/><rect x="-2" y="1.8" width="4" height="2.6" rx=".6" fill="#efe6d6" stroke="#2a1a22" stroke-width=".6"/>',
    '<circle r="3.6" fill="var(--nzA,#efe6d6)" fill-opacity=".8" stroke="#2a1a22" stroke-width=".8"/><rect x="-2" y="1.8" width="4" height="2.6" rx=".6" fill="var(--nzA,#efe6d6)" fill-opacity=".8" stroke="#2a1a22" stroke-width=".6"/>')
rep('${P.filter((p, i) => p[1] < cy).map(skull).join("")}${P.filter((p, i) => p[1] >= cy).map(skull).join("")}',
    '${P.filter((p, i) => i % 2 === 0 && p[1] < cy).map(skull).join("")}${P.filter((p, i) => i % 2 === 0 && p[1] >= cy).map(skull).join("")}')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
