import sys
# V717: Wischsteuerung als zusätzliche Option (Martin 15.11.2026 17:51; Antworten 17:5x: «Finger ziehen», «Tipp auf Turm öffnet Menü»).
#  Schalter in den Einstellungen (Zahnrad / «Hero & name») («SWIPE CONTROLS: ON/off», LS capy-gest, Standard AN (Martin 17:58)). Knöpfe bleiben.
#  Auf dem Spielfeld: Finger ziehen links/rechts = Block folgt Feld für Feld; kurz tippen = drehen (auf einem Turm: Turm-Menü);
#  nach oben wischen = Block fallen lassen (harter Fall); weit nach unten ziehen = Block senken (je Feld ein Schritt).
#  Bau-/Ziel-Modi (Turm bauen, Sniper, Mixer, Tesla), Abwurf und Alarm behalten das alte Tippen.
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V716";', 'const GAME_VER = "V717";')
rep('''  <label for="setNick">Your player name · made up, not your real one</label>''',
    '''  <button type="button" id="pvGest" class="btn-small setGest">SWIPE CONTROLS: ON</button><style>.setGest{display:block;width:100%;margin:6px 0 10px;min-height:40px}</style>
  <label for="setNick">Your player name · made up, not your real one</label>''')
rep('''// ---------- Eingabe ----------
let towerId = 0;
''', r'''// ---------- Eingabe ----------
let towerId = 0;
/* V717: Wischsteuerung (Option) – nach dem Laden einrichten (LS wird weiter unten definiert) */
setTimeout(() => {
  let on = LS.get("capy-gest") !== "0", g = null;   /* Martin 17:58: standardmäßig AN, im Pause-Menü abschaltbar */
  const btn = $("pvGest"), paint = () => { if (btn) btn.textContent = "SWIPE CONTROLS: " + (on ? "ON" : "OFF"); }; paint();
  if (btn) btn.addEventListener("click", () => { on = !on; LS.set("capy-gest", on ? "1" : "0"); paint(); if (on) toast("DRAG = move · TAP = rotate · SWIPE UP = drop", "SWIPE"); });
  window.__gest = { get on() { return on; } };
  const free = () => !S.started || S.over || S.duel || S.drop || S.alert || S.mix || ["build", "snipe", "mix", "tesla"].includes(S.mode);
  cv.addEventListener("pointerdown", e => {
    if (!on || free() || performance.now() < (window.__tapGuard || 0)) return;
    e.stopImmediatePropagation(); e.preventDefault();
    const r = cv.getBoundingClientRect();
    g = { id: e.pointerId, x0: e.clientX, y0: e.clientY, t0: performance.now(), lx: e.clientX, ly: e.clientY, cw: r.width / GW, ch: r.height / GH, moved: false, down: 0, e };
    try { cv.setPointerCapture(e.pointerId); } catch (er) {}
  }, true);
  cv.addEventListener("pointermove", e => {
    if (!g || e.pointerId !== g.id) return;
    e.stopImmediatePropagation();
    const dx = e.clientX - g.lx, dy = e.clientY - g.ly;
    if (Math.abs(e.clientX - g.x0) > 10 || Math.abs(e.clientY - g.y0) > 10) g.moved = true;
    if (Math.abs(dx) >= g.cw * 0.9 && Math.abs(e.clientX - g.x0) > Math.abs(e.clientY - g.y0) * 0.6) { const n = Math.trunc(dx / (g.cw * 0.9)); for (let i = 0; i < Math.abs(n); i++) move(Math.sign(n)); g.lx += n * g.cw * 0.9; }
    if (e.clientY - g.y0 > g.ch * 1.5 && dy >= g.ch * 0.8) { const n = Math.trunc(dy / (g.ch * 0.8)); for (let i = 0; i < n; i++) softDrop(); g.ly += n * g.ch * 0.8; g.down += n; }
  }, true);
  const end = e => {
    if (!g || e.pointerId !== g.id) return;
    e.stopImmediatePropagation();
    const dt = performance.now() - g.t0, tx = e.clientX - g.x0, ty = e.clientY - g.y0, st = g; g = null;
    if (e.type === "pointercancel") return;
    if (ty < -Math.max(40, st.ch * 1.5) && Math.abs(ty) > Math.abs(tx) * 1.2 && dt < 600) { hardDrop(); return; }
    if (!st.moved && dt < 350) {
      const [x, y] = cvCell(st.e), t = (x >= 0 && y >= 0 && x < GW && y < GH) ? S.towers.get(y * GW + x) : null;
      if (t) { snd("towerTap"); openSheet(t); return; }
      if (S.sel) closeSheet();
      rotate();
    }
  };
  cv.addEventListener("pointerup", end, true); cv.addEventListener("pointercancel", end, true);
}, 0);
''')
open(dst, "w", encoding="utf-8").write(s)
import subprocess, os
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang717.py"), os.path.join(os.path.dirname(os.path.abspath(dst)), "lang")], check=True)
