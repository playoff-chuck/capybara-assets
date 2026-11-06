"""V348 (Martin 07.11. 00:10): Dieb schöner gezeichnet und lebendiger:
Ringelshirt, Mütze, Augenmaske mit beweglichen Pupillen, Schuhe, Schatten, Laufzyklus mit schwingenden Armen.
Ablauf: läuft 6 s heran → bleibt kurz vor dem Gold stehen und schaut zurück (dreht sich um, «?») → schaut zum Gold («!») →
schleicht auf Zehenspitzen hin → schnappt das Gold (Arm greift) → rennt mit dem Geldsack 20 s zum rechten Rand.
Abschuss-Zeitpunkte unverändert (10 s bis zum Griff)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V347";', 'const GAME_VER = "V348";')
rep('const SZ = 64, DPR = Math.min(3, window.devicePixelRatio || 1);', 'const SZ = 84, DPR = Math.min(3, window.devicePixelRatio || 1);')
i = s.find('  function sprite(T) {'); j = s.find('  el.addEventListener("pointerdown", ev => {', i); assert 0 < i < j
NEW = r'''  // Ablauf (Sekunden): 0–6 laufen · 6–7,3 umschauen · 7,3–8,4 zum Gold schauen · 8,4–10 schleichen · 10 greifen · 10–30 rennen
  function phase(t) { return t < 6 ? "walk" : t < 7.3 ? "back" : t < 8.4 ? "eye" : t < 10 ? "sneak" : t < 10.6 ? "grab" : "run"; }
  function sprite(T) {
    g.setTransform(DPR, 0, 0, DPR, 0, 0); g.clearRect(0, 0, SZ, SZ);
    const t = T.t, ph = phase(t), moving = ph === "walk" || ph === "sneak" || ph === "run";
    const f = ph === "run" ? 13 : ph === "sneak" ? 6 : 9, cyc = Math.sin(t * f), bob = moving ? Math.abs(cyc) * (ph === "run" ? 3 : 2) : 0;
    const dir = ph === "back" ? -1 : 1, look = ph === "back" ? 1 : ph === "eye" ? 1 : 0.5, lean = ph === "run" ? 0.14 : ph === "sneak" ? 0.08 : 0;
    const k = 1.05;   // Grundmaßstab
    g.save(); g.translate(SZ / 2, SZ - 10);
    g.fillStyle = "rgba(0,0,0,.25)"; g.beginPath(); g.ellipse(0, 4, 15, 3.5, 0, 0, 6.29); g.fill();   // Schatten
    g.scale(dir * k, k); g.translate(0, -bob); g.rotate(lean);
    // Beine + Schuhe
    const sw = moving ? cyc * (ph === "run" ? 9 : ph === "sneak" ? 4 : 7) : 0, tip = ph === "sneak" ? -2 : 0;
    [[-4, sw], [4, -sw]].forEach(([lx, a]) => { g.save(); g.translate(lx, -18); g.rotate(a * 0.045);
      g.fillStyle = "#23232b"; g.fillRect(-3, 0, 6, 15); g.fillStyle = "#111"; g.beginPath(); g.ellipse(2, 16 + tip, 5.5, 3, 0, 0, 6.29); g.fill(); g.restore(); });
    // hinterer Arm
    g.save(); g.translate(-2, -34); g.rotate(moving ? -cyc * 0.6 : 0.2); g.fillStyle = "#c9c9d2"; g.fillRect(-2.5, 0, 5, 13); g.fillStyle = "#8a5a2b"; g.beginPath(); g.arc(0, 14, 3, 0, 6.29); g.fill(); g.restore();
    // Körper mit Ringelshirt
    g.save(); g.beginPath(); g.ellipse(0, -28, 10, 13, 0, 0, 6.29); g.clip();
    for (let y = -42; y < -14; y += 5) { g.fillStyle = ((y + 42) / 5) % 2 ? "#f2f2f2" : "#1d1d24"; g.fillRect(-12, y, 24, 5); } g.restore();
    g.strokeStyle = "#0d0d10"; g.lineWidth = 1.2; g.beginPath(); g.ellipse(0, -28, 10, 13, 0, 0, 6.29); g.stroke();
    // Geldsack über der Schulter
    if (T.stolen) { g.save(); g.translate(-11, -38); g.rotate(-0.3 + cyc * 0.08); g.fillStyle = "#b08a4a"; g.strokeStyle = "#5a4310"; g.lineWidth = 1.3;
      g.beginPath(); g.ellipse(0, 4, 9, 10, 0, 0, 6.29); g.fill(); g.stroke(); g.fillStyle = "#8a6a32"; g.fillRect(-3, -7, 6, 4);
      g.fillStyle = "#ffd84a"; g.font = "bold 11px sans-serif"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("$", 0, 5); g.restore(); }
    // Kopf
    g.save(); g.translate(1, -48); g.rotate(ph === "eye" ? 0.12 : ph === "back" ? -0.05 : 0);
    g.fillStyle = "#c48a5a"; g.beginPath(); g.arc(0, 0, 9, 0, 6.29); g.fill();
    g.fillStyle = "#16161c"; g.beginPath(); g.arc(0, -2, 9.6, Math.PI, 0); g.fill(); g.fillRect(-10, -3.5, 20, 3.5); g.fillStyle = "#2a2a34"; g.fillRect(-10.5, -4, 21, 2.2);   // Mütze
    g.beginPath(); g.arc(0, -11, 2.4, 0, 6.29); g.fill();   // Bommel
    g.fillStyle = "#16161c"; g.fillRect(-8.8, 0.5, 17.6, 5.2);   // Augenmaske
    const px = look * 1.4; g.fillStyle = "#fff"; g.beginPath(); g.ellipse(-3.2, 3, 2.3, 1.9, 0, 0, 6.29); g.ellipse(3.6, 3, 2.3, 1.9, 0, 0, 6.29); g.fill();
    g.fillStyle = "#111"; g.beginPath(); g.arc(-3.2 + px, 3.1, 1, 0, 6.29); g.arc(3.6 + px, 3.1, 1, 0, 6.29); g.fill();
    g.strokeStyle = "#5a2f18"; g.lineWidth = 1.2; g.beginPath(); if (T.stolen || ph === "eye") g.arc(1.5, 6.5, 2.6, 0.2, 2.6); else { g.moveTo(-1, 7.5); g.lineTo(3.5, 7); } g.stroke();   // Grinsen
    g.restore();
    // vorderer Arm (greift beim Diebstahl)
    g.save(); g.translate(3, -34); const ga = ph === "grab" ? -1.25 : ph === "eye" ? -0.6 : moving ? cyc * 0.6 : -0.15; g.rotate(ga);
    g.fillStyle = "#e4e4ea"; g.fillRect(-2.5, 0, 5, 13); g.fillStyle = "#c48a5a"; g.beginPath(); g.arc(0, 14, 3, 0, 6.29); g.fill(); g.restore();
    g.restore();
    // Zeichen über dem Kopf
    const mark = ph === "back" ? "?" : ph === "eye" ? "!" : "";
    if (mark) { g.save(); g.translate(SZ / 2 + 12, 12); g.fillStyle = "#fff"; g.strokeStyle = "#16161c"; g.lineWidth = 1.5; g.beginPath(); g.arc(0, 0, 8, 0, 6.29); g.fill(); g.stroke();
      g.fillStyle = mark === "!" ? "#e0412f" : "#16161c"; g.font = "bold 12px sans-serif"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(mark, 0, 1); g.restore(); }
    if (!T.stolen && t < 10) { g.fillStyle = "#ff4a3a"; g.strokeStyle = "#fff"; g.lineWidth = 3; g.font = "bold 13px sans-serif"; g.textAlign = "center"; const n = String(Math.max(0, Math.ceil(10 - t))); g.strokeText(n, SZ / 2 - 14, 12); g.fillText(n, SZ / 2 - 14, 12); }
  }
  window.__thiefPos = T => { if (!T) { el.style.display = "none"; return; }
    const ge = document.getElementById("sGold"), r = ge ? ge.getBoundingClientRect() : { left: innerWidth / 2, width: 0, top: 40, height: 0 };
    const gx = r.left + r.width / 2, gy = r.top + r.height / 2, t = T.t, stop = gx - 46;
    const x = t < 6 ? -SZ + (stop + SZ) * (t / 6) : t < 8.4 ? stop : t < 10 ? stop + (gx - 14 - stop) * ((t - 8.4) / 1.6) : (gx - 14) + (innerWidth + SZ - gx + 14) * Math.min(1, (t - 10) / 20);
    el.style.display = "block"; el.style.transform = `translate(${Math.round(x - SZ / 2)}px,${Math.round(gy - SZ + 22)}px)`; sprite(T); };
'''
s = s[:i] + NEW + s[j:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
