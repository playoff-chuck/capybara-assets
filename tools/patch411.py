#!/usr/bin/env python3
# V411 (t12 Nr. 3, Martin 07.11. 21:49 «ja, mit Lokalkolorit»): Turm-Skins je Kontinent – Sandstein+Skarabäus (Afrika),
# Schnee+Laternen (Asien, auch Antarktis), Holz+Ahorn+Karo (Nordamerika). 9 Sprites img/skin_<kont>_<waffe>.webp (4 Bilder Nano Banana Pro, 0,55 $).
# Freigeschaltet, sobald der Kontinent 25 ★ (von 30) hat; gilt dann beim Spielen in diesem Kontinent. Anzeige im Squad File (TOWER SKINS).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V410";', 'const GAME_VER = "V411";')
rep("const TOW_SPR={};{const T={mg:\"img/9335afdf0f.webp\",kan:\"img/8d5eb7ae93.webp\",frost:\"img/595582df1c.webp\"};for(const k in T){const im=new Image();im.src=T[k];TOW_SPR[k]=im;}}",
    "const TOW_SPR={};{const T={mg:\"img/9335afdf0f.webp\",kan:\"img/8d5eb7ae93.webp\",frost:\"img/595582df1c.webp\"};for(const k in T){const im=new Image();im.src=T[k];TOW_SPR[k]=im;}}"
    "const SKIN_SPR={};for(const c of[\"africa\",\"asia\",\"namerica\"]){SKIN_SPR[c]={};for(const k of[\"mg\",\"kan\",\"frost\"]){const im=new Image();im.src=`img/skin_${c}_${k}.webp`;SKIN_SPR[c][k]=im;}}"
    "function skinSpr(ty){try{const c=curSkin();if(!c)return null;const im=SKIN_SPR[c]&&SKIN_SPR[c][ty];return im&&im.complete&&im.naturalWidth?im:null;}catch(e){return null;}}")
rep("const ty=t.w.some(w=>w.type==='kan')?'kan':t.w.some(w=>w.type==='frost')?'frost':'mg',im=TOW_SPR[ty];",
    "const ty=t.w.some(w=>w.type==='kan')?'kan':t.w.some(w=>w.type==='frost')?'frost':'mg',skm=skinSpr(ty),im=skm||TOW_SPR[ty];")
# Mit Skin: nur Seitenansicht (gespiegelt), keine Richtungsbilder (die haben die Camo-Basis)
rep("const now=performance.now(),v=towView(t,now),pick=x=>{const j=x?TOW_DIR[ty+(x===1?\"_front\":\"_back\")]:im;return j&&j.complete&&j.naturalWidth?j:im;}",
    "const now=performance.now(),v=skm?0:towView(t,now),pick=x=>{if(skm)return skm;const j=x?TOW_DIR[ty+(x===1?\"_front\":\"_back\")]:im;return j&&j.complete&&j.naturalWidth?j:im;}")
JS = r'''
/* V410: Turm-Skins je Kontinent (t12 Nr. 3) */
const SKIN_C = [["africa", "Africa", "Desert Stone"], ["asia", "Asia", "Winter Lantern"], ["namerica", "North America", "Log Cabin"]];
function contStars(ci) { const st = starsAll(); let n = 0; for (let i = 0; i < 6; i++) n += +st[ci * 6 + i] || 0; return n; }
function skinOwned(key) { if (key === "asia") return contStars(2) >= 25 || contStars(4) >= 25; return contStars(key === "africa" ? 1 : 3) >= 25; }   /* 25 von 30 ★ */
let _skinC = null, _skinW = -1;
function curSkin() { if (!S || !S.started || S.nuts) return null; const w = S.wave | 0; if (w === _skinW) return _skinC; _skinW = w;
  const ci = Math.min(4, Math.floor(Math.max(1, w) - 1) / 30 | 0), key = ci === 1 ? "africa" : ci === 2 || ci === 4 ? "asia" : ci === 3 ? "namerica" : null;
  _skinC = key && skinOwned(key) ? key : null; return _skinC; }
function skinHtml() { let got = 0; const cards = SKIN_C.map(c => { const on = skinOwned(c[0]); if (on) got++;
    return `<div class="mcCard ${on ? "t3" : "off"}"><img src="img/skin_${c[0]}_mg.webp" alt="" style="${on ? "" : "filter:grayscale(1) brightness(.55)"}"><i>${c[2]}</i><small>${on ? c[1] : `25 ★ in ${c[1]}`}</small></div>`; }).join("");
  return `<div class="albSec">TOWER SKINS<span>${got} / ${SKIN_C.length}</span></div><div class="mcGrid">${cards}</div>`; }
'''
rep('/* V408: Trophäenregal – Wahrzeichen aus den Boss-Hintergründen (t12 Nr. 9) */', JS + '/* V408: Trophäenregal – Wahrzeichen aus den Boss-Hintergründen (t12 Nr. 9) */')
rep('let h = sqHtml() + trophyHtml() + `<div class="albSec">CAREER</div>', 'let h = sqHtml() + trophyHtml() + skinHtml() + `<div class="albSec">CAREER</div>')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
