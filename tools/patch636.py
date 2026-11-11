#!/usr/bin/env python3
# V636 (Martin 11.11. 16:08): Weltkarte – noch nicht geöffnete Kontinente (Asien, Nordamerika, Antarktis) und immer Australien ausgegraut
# (Ausgrau-Bilder lock_*.webp, wie in der Bezahl-Variante). Auf grauen Kontinenten keine Nuts-Punkte und -Namen; Nuts-Territorien bleiben.
# Geöffnet = beste je erreichte Welle hat den Kontinent erreicht (Start bei Welle c·30+1).
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V635";', 'const GAME_VER = "V636";')
rep('function fmMapSync(ov, pinsEl) { try { ov.querySelectorAll(".mapLock").forEach(i => { const lc = i.dataset.lc; i.hidden = !FM.on || (lc !== "aus" && FM.open(+lc)); });',
    '''function contGrey(c) { if (c === "aus") return true; c = +c; if (c < 2) return false; if (FM.on) return !FM.open(c); let b = 0; try { b = dailyBestW(); } catch (e) {} return b < c * 30 + 1; }   /* V636 */
function fmMapSync(ov, pinsEl) { try { ov.querySelectorAll(".mapLock").forEach(i => { i.hidden = !contGrey(i.dataset.lc); });
  setTimeout(() => pinsEl.querySelectorAll(".mNuts").forEach(n => { const g = contGrey(n.dataset.nz); const a = n.querySelector(".nzAnc"); if (a) a.style.display = g ? "none" : ""; n.classList.toggle("greyC", g); }), 0); window.__contGrey = contGrey;   /* V636: keine Nuts-Punkte/-Namen auf grauen Kontinenten */''')
open(p, "w", encoding="utf-8").write(s)
print("ok V636")
