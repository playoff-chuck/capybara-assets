#!/usr/bin/env python3
# V413 (t12 Nr. 2): Outfits für Blue & Rosie (nur Kosmetik) – je 4 Outfits: Shades (30 ★), Explorer (60 ★), Winter (90 ★), Champion (120 ★).
# 8 Sprites img/outfit_<held>_<n>.webp (2 Bilder Nano Banana Pro, 0,28 $). Auswahl im Squad File (OUTFITS), gespeichert in capy-outfit-<held>.
# HERO_IMG wird dynamisch (Getter) – alle Sprechblasen, Karten, Buddy-Bilder zeigen das gewählte Outfit.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V412";', 'const GAME_VER = "V413";')
rep('const HERO_IMG = {"blue": "img/e8b742aa03.webp", "rosie": "img/cf7539bf2e.webp"};',
    'const HERO_BASE = {"blue": "img/e8b742aa03.webp", "rosie": "img/cf7539bf2e.webp"};\n'
    'const OUTFIT = [["Standard", 0], ["Shades", 30], ["Explorer", 60], ["Winter", 90], ["Champion", 120]];   /* V413: Name, Sterne */\n'
    'function outfitImg(k, n) { return n ? `img/outfit_${k}_${n}.webp` : HERO_BASE[k]; }\n'
    'function outfitSel(k) { try { const n = +localStorage.getItem("capy-outfit-" + k) || 0; return n >= 0 && n <= 4 ? n : 0; } catch (e) { return 0; } }\n'
    'const HERO_IMG = { get blue() { return outfitImg("blue", outfitSel("blue")); }, get rosie() { return outfitImg("rosie", outfitSel("rosie")); } };')
CSS = """.ofRow{display:grid;grid-template-columns:repeat(5,1fr);gap:4px;margin-bottom:6px}.ofRow .mcCard{padding:2px 2px 3px;cursor:pointer}.ofRow .mcCard.on{border-color:#ee7a2c;background:#ffe9d2;box-shadow:0 2px 0 #c45a1a}.ofRow .mcCard i{font-size:9px}.ofRow .mcCard small{font-size:8px}
</style>"""
rep(".trCup.off small{color:#7a7a70}\n</style>", ".trCup.off small{color:#7a7a70}\n" + CSS)
JS = r'''
/* V413: Outfits – Auswahl im Squad File */
function outfitHtml() { const st = starsAll(), stars = Object.values(st).reduce((a, b) => a + (+b || 0), 0); let h = "";
  for (const k of ["blue", "rosie"]) { const sel = outfitSel(k);
    h += `<div class="albSec">${k.toUpperCase()}'S OUTFITS<span>${OUTFIT.filter(o => stars >= o[1]).length} / 5</span></div><div class="ofRow">` + OUTFIT.map((o, n) => { const on = stars >= o[1];
      return `<div class="mcCard ${on ? (n === sel ? "on" : "t3") : "off"}" data-of="${k}:${n}"><img src="${outfitImg(k, n)}" alt=""><i>${o[0]}</i><small>${on ? (n === sel ? "wearing" : "tap to wear") : o[1] + " ★"}</small></div>`; }).join("") + `</div>`; }
  return h; }
document.addEventListener("click", e => { const c = e.target.closest && e.target.closest("[data-of]"); if (!c || c.classList.contains("off")) return; const [k, n] = c.dataset.of.split(":");
  try { localStorage.setItem("capy-outfit-" + k, n); } catch (er) {} try { snd("uiTap"); } catch (er) {} try { const img = document.querySelector("#startMain .heroImg"); } catch (er) {} openSquad(); });
'''
rep('/* V408: Trophäenregal – Wahrzeichen aus den Boss-Hintergründen (t12 Nr. 9) */', JS + '/* V408: Trophäenregal – Wahrzeichen aus den Boss-Hintergründen (t12 Nr. 9) */')
rep('let h = sqHtml() + trophyHtml() + skinHtml() + `<div class="albSec">CAREER</div>', 'let h = sqHtml() + trophyHtml() + skinHtml() + outfitHtml() + `<div class="albSec">CAREER</div>')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
