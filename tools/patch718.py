import sys, os, subprocess
# V718: Info-Knopf unten links in der Bedienkapsel (Martin 15.11.2026 18:21). Antippen: Spiel hält an,
#  über dem Spielfeld schweben 5 Gesten (links/rechts ziehen, tippen = drehen, hoch wischen = fallen, runter ziehen = senken)
#  im ruhigen «Apple-Stil» (dünne weiße Linien, Glas-Kärtchen, Systemschrift). Nochmal antippen (oder irgendwo tippen): weg, Spiel läuft weiter.
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V717";', 'const GAME_VER = "V718";')
rep('''      <button id="bDrop" class="btn-accent" aria-label="Hard drop"><svg><use href="#i-drop"/></svg><span class="lbl">DROP</span></button>''',
    '''      <button id="bDrop" class="btn-accent" aria-label="Hard drop"><svg><use href="#i-drop"/></svg><span class="lbl">DROP</span></button>
      <button id="bInfo" type="button" aria-label="How to play with gestures"><i>i</i></button>''')
CSS = r'''<style id="v718css">
.deckIn .pad #bInfo{grid-area:po;display:flex!important;align-items:center;justify-content:center;background:transparent!important;box-shadow:none!important;border:2px dashed rgba(255,246,230,.55)!important;border-radius:12px!important;min-height:0!important;height:auto!important;padding:0!important;cursor:pointer;-webkit-tap-highlight-color:transparent}
#bInfo i{width:22px;height:22px;border-radius:50%;border:2px solid #fff6e6;color:#fff6e6;display:flex;align-items:center;justify-content:center;font:italic 700 14px/1 Georgia,"Times New Roman",serif;box-sizing:border-box}
#bInfo.on{border-style:solid!important;border-color:#fff6e6!important}
#bInfo.on i{background:#fff6e6;color:#3a2a1a}
#gestOv{position:fixed;left:0;top:0;right:0;z-index:2147483000;display:none;touch-action:none;-webkit-user-select:none;user-select:none;
 background:radial-gradient(120% 80% at 50% 45%,rgba(18,20,28,.5),rgba(8,9,14,.74));-webkit-backdrop-filter:blur(7px) saturate(120%);backdrop-filter:blur(7px) saturate(120%);
 font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","SF Pro Text","Helvetica Neue","Inter",system-ui,sans-serif;color:#fff;opacity:0;transition:opacity .28s ease}
#gestOv.show{display:block}#gestOv.vis{opacity:1}
#gestOv .gHead{position:absolute;left:0;right:0;text-align:center;font-size:11px;font-weight:600;letter-spacing:.24em;text-transform:uppercase;opacity:.62}
#gestOv .gFoot{position:absolute;left:0;right:0;text-align:center;font-size:12.5px;font-weight:500;letter-spacing:.01em;opacity:.7}
#gestOv .gOff{position:absolute;left:12%;right:12%;text-align:center;font-size:12px;font-weight:500;opacity:.85;padding:7px 12px;border-radius:12px;background:rgba(255,255,255,.1);border:.5px solid rgba(255,255,255,.28)}
#gestOv svg{position:absolute;overflow:visible}
#gestOv .gCard{position:absolute;transform:translate(-50%,-50%);padding:9px 14px 8px;border-radius:16px;text-align:center;white-space:nowrap;
 background:linear-gradient(180deg,rgba(255,255,255,.2),rgba(255,255,255,.1));border:.5px solid rgba(255,255,255,.42);
 box-shadow:0 10px 30px rgba(0,0,0,.28),inset 0 .5px 0 rgba(255,255,255,.55);-webkit-backdrop-filter:blur(18px) saturate(170%);backdrop-filter:blur(18px) saturate(170%)}
#gestOv .gCard b{display:block;font-size:15px;font-weight:600;letter-spacing:-.01em;line-height:1.15}
#gestOv .gCard small{display:block;font-size:11.5px;font-weight:500;opacity:.72;margin-top:2px;letter-spacing:.01em}
@keyframes gL{0%,100%{transform:translateX(0);opacity:.95}50%{transform:translateX(-9px);opacity:1}}
@keyframes gR{0%,100%{transform:translateX(0);opacity:.95}50%{transform:translateX(9px);opacity:1}}
@keyframes gU{0%,100%{transform:translateY(0);opacity:.95}50%{transform:translateY(-9px);opacity:1}}
@keyframes gD{0%,100%{transform:translateY(0);opacity:.95}50%{transform:translateY(9px);opacity:1}}
@keyframes gP{0%{r:14;opacity:.85}100%{r:34;opacity:0}}
#gestOv .aL{animation:gL 1.8s cubic-bezier(.45,0,.25,1) infinite}#gestOv .aR{animation:gR 1.8s cubic-bezier(.45,0,.25,1) infinite}
#gestOv .aU{animation:gU 1.8s cubic-bezier(.45,0,.25,1) infinite}#gestOv .aD{animation:gD 1.8s cubic-bezier(.45,0,.25,1) infinite}
#gestOv .pulse{animation:gP 1.8s cubic-bezier(.2,.6,.3,1) infinite}#gestOv .pulse.p2{animation-delay:.9s}
@media (prefers-reduced-motion:reduce){#gestOv .aL,#gestOv .aR,#gestOv .aU,#gestOv .aD,#gestOv .pulse{animation:none}}
</style>'''
rep('<script id="v716hz">', CSS + '\n<div id="gestOv" aria-hidden="true"></div>\n<script id="v718gest">' + r'''
(() => { try {
  const ov = document.getElementById("gestOv"), btn = document.getElementById("bInfo"); if (!ov || !btn) return;
  const T = k => { try { return window.__i18n.T(k); } catch (e) { return k; } };
  let open = false, wasPaused = false;
  const NS = "http://www.w3.org/2000/svg";
  const el = (tag, cls, txt) => { const e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
  const card = (x, y, title, sub) => { const c = el("div", "gCard"); c.style.left = x + "px"; c.style.top = y + "px"; c.appendChild(el("b", "", title)); c.appendChild(el("small", "", sub)); return c; };
  function build() {
    ov.textContent = "";
    const pad = document.querySelector(".deckIn .pad") || document.querySelector(".deck"), cv = document.getElementById("cv");
    const bottom = pad ? Math.max(120, pad.getBoundingClientRect().top - 4) : innerHeight * 0.8;
    ov.style.height = bottom + "px";
    const r = cv ? cv.getBoundingClientRect() : { left: 0, top: 0, width: innerWidth, height: bottom };
    const cx = r.left + r.width / 2, top = Math.max(r.top, 40), bot = Math.min(r.top + r.height, bottom - 10), cy = (top + bot) / 2;
    const W = Math.min(r.width, innerWidth) , armX = Math.min(W * 0.36, 150), armY = Math.min((bot - top) * 0.3, 180);
    const svg = document.createElementNS(NS, "svg"); svg.setAttribute("width", innerWidth); svg.setAttribute("height", bottom); svg.style.left = "0"; svg.style.top = "0";
    const g = (cls) => { const e = document.createElementNS(NS, "g"); if (cls) e.setAttribute("class", cls); svg.appendChild(e); return e; };
    const path = (parent, d, w, op) => { const p = document.createElementNS(NS, "path"); p.setAttribute("d", d); p.setAttribute("fill", "none"); p.setAttribute("stroke", "#fff"); p.setAttribute("stroke-width", w || 1.6); p.setAttribute("stroke-linecap", "round"); p.setAttribute("stroke-linejoin", "round"); if (op) p.setAttribute("opacity", op); parent.appendChild(p); return p; };
    const circ = (parent, x, y, rr, cls, fill, w) => { const c = document.createElementNS(NS, "circle"); c.setAttribute("cx", x); c.setAttribute("cy", y); c.setAttribute("r", rr); c.setAttribute("fill", fill || "none"); c.setAttribute("stroke", "#fff"); c.setAttribute("stroke-width", w || 1.6); if (cls) c.setAttribute("class", cls); parent.appendChild(c); return c; };
    /* feine Führungslinien vom Zentrum */
    const guide = g(); for (const [dx, dy] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) path(guide, `M${cx + dx * 26} ${cy + dy * 26} L${cx + dx * (dx ? armX - 30 : 0)} ${cy + dy * (dy ? armY - 30 : 0)}`, 1, .35).setAttribute("stroke-dasharray", "2 5");
    /* Tippen: Punkt mit zwei Wellen */
    const tap = g(); circ(tap, cx, cy, 14, "pulse"); circ(tap, cx, cy, 14, "pulse p2"); circ(tap, cx, cy, 9, "", "rgba(255,255,255,.95)", 0);
    /* Pfeile (Chevron + kurzer Schaft) */
    const chev = (cls, x, y, dir) => { const a = g(cls); const s = 11;
      const d = dir === "l" ? `M${x + s} ${y - s} L${x} ${y} L${x + s} ${y + s}` : dir === "r" ? `M${x - s} ${y - s} L${x} ${y} L${x - s} ${y + s}` : dir === "u" ? `M${x - s} ${y + s} L${x} ${y} L${x + s} ${y + s}` : `M${x - s} ${y - s} L${x} ${y} L${x + s} ${y - s}`;
      path(a, d, 2.2); const sh = dir === "l" ? `M${x} ${y} L${x + 26} ${y}` : dir === "r" ? `M${x} ${y} L${x - 26} ${y}` : dir === "u" ? `M${x} ${y} L${x} ${y + 26}` : `M${x} ${y} L${x} ${y - 26}`; path(a, sh, 2.2);
      if (dir === "u") path(a, `M${x - s} ${y - 7 + s} L${x} ${y - 7} L${x + s} ${y - 7 + s}`, 2.2, .55);   /* Doppelpfeil = ganz nach unten fallen lassen */
    };
    chev("aL", cx - armX + 12, cy, "l"); chev("aR", cx + armX - 12, cy, "r"); chev("aU", cx, cy - armY + 14, "u"); chev("aD", cx, cy + armY - 14, "d");
    ov.appendChild(svg);
    if (cy - armY - 44 - 30 > top + 40) { const head = el("div", "gHead", T("Swipe controls")); head.style.top = (top + 14) + "px"; ov.appendChild(head); }   /* nur wenn Platz */
    ov.appendChild(card(cx, cy + 56, T("Tap"), T("Rotate")));
    ov.appendChild(card(cx - armX + 22, cy + 52, T("Drag left"), T("Move")));
    ov.appendChild(card(cx + armX - 22, cy + 52, T("Drag right"), T("Move")));
    ov.appendChild(card(cx, cy - armY - 44, T("Swipe up"), T("Drop")));
    ov.appendChild(card(cx, cy + armY + 36, T("Drag down"), T("Lower")));
    if (window.__gest && !window.__gest.on) { const o = el("div", "gOff", T("Swipe controls are off · turn them on in Settings")); o.style.top = (bottom - 92) + "px"; ov.appendChild(o); }
    const f = el("div", "gFoot", T("Tap ⓘ to play on")); f.style.top = (bottom - 34) + "px"; ov.appendChild(f);
  }
  function setOpen(v) {
    const S = window.__TT && window.__TT.S;
    if (v === open) return; open = v; btn.classList.toggle("on", v);
    if (v) { build(); ov.classList.add("show"); requestAnimationFrame(() => ov.classList.add("vis")); if (S) S.gestInfo = true; }
    else { ov.classList.remove("vis"); setTimeout(() => { if (!open) ov.classList.remove("show"); }, 280); if (S) S.gestInfo = false; }
  }
  btn.addEventListener("pointerdown", e => { e.preventDefault(); e.stopPropagation(); setOpen(!open); });
  btn.addEventListener("click", e => { if (e.detail === 0) setOpen(!open); });
  ov.addEventListener("pointerdown", e => { e.preventDefault(); setOpen(false); });
  addEventListener("resize", () => { if (open) build(); });
  window.__gestInfo = { open: () => setOpen(true), close: () => setOpen(false), get isOpen() { return open; } };
} catch (e) { console.error("v718", e); } })();
</script>
<script id="v716hz">''')
rep('S.mix || S.tiltCard || !!(window.__tipBulb && window.__tipBulb.open); }', 'S.mix || S.tiltCard || S.gestInfo || !!(window.__tipBulb && window.__tipBulb.open); }')   # V718
open(dst, "w", encoding="utf-8").write(s)
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang718.py"), os.path.join(os.path.dirname(os.path.abspath(dst)), "lang")], check=True)
