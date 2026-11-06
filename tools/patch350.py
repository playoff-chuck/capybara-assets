"""V350 (Martin 07.11. 00:23–00:26):
Dieb: neu als Waschbär-Einbrecher (schwarzer Pulli, schwarze Kappe) aus 7 Nano-Banana-Bildern (img/thief_1…7.webp, 0,14 $),
im Stil der Spielfiguren. Animation: Laufzyklus (2 Bilder), umschauen (dreht sich um), Hände reiben beim Blick aufs Gold,
auf Zehenspitzen schleichen, greifen, mit Geldsack wegrennen (Hüpfen + Vorlage). «?»/«!» und Countdown bleiben.
Unkraut: kommt nie in Dreh-Wellen (Sidewinder) und nie später als 3 Wellen vor dem Kontinentwechsel –
neue Wellen 86 / 110 / 130 (statt 90 / 110 / 130); verwelkt sofort, wenn eine Dreh-Welle beginnt oder der Kontinent wechselt."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V349";', 'const GAME_VER = "V350";')
# Unkraut-Regeln
rep('if (k === "weed") return [90, 110, 130].includes(w);', 'if (k === "weed") return [86, 110, 130].includes(w) && !ROT_BASES.includes(specBase(w)) && (w - 1) % 30 < 27;')
rep('if (S.rotMode) { D.mag = null; D.blk = null; }', 'if (S.rotMode) { D.mag = null; D.blk = null; if (D.weed) { D.weed = null; toast("WEEDS WITHERED", "HQ", 1400); } }')
rep('if (D.weed && ++D.weed.waves > 2) {', 'if (D.weed && (++D.weed.waves > 2 || (S.wave - 1) % 30 === 0 || ROT_BASES.includes(specBase()))) {')
# Dieb mit Bildern
rep('const SZ = 84, DPR', 'const SZ = 96, DPR')
i = s.find('  function sprite(T) {'); j = s.find('  window.__thiefPos = T =>', i); assert 0 < i < j
NEW = r'''  const FR = [1, 2, 3, 4, 5, 6, 7].map(n => { const im = new Image(); im.decoding = "async"; im.src = "img/thief_" + n + ".webp"; return im; });
  function sprite(T) {
    g.setTransform(DPR, 0, 0, DPR, 0, 0); g.clearRect(0, 0, SZ, SZ);
    const t = T.t, ph = phase(t); let fi = 0, flip = false, bob = 0, tilt = 0, sy = 1;
    if (ph === "walk") { fi = Math.floor(t * 5.5) % 2; bob = Math.abs(Math.sin(t * 17.3)) * 2.2; }
    else if (ph === "back") { fi = 2; flip = t > 6.3 && t < 7.15; }
    else if (ph === "eye") { fi = 3; bob = Math.abs(Math.sin(t * 22)) * 0.9; }
    else if (ph === "sneak") { fi = 4; bob = Math.abs(Math.sin(t * 7)) * 2.6; tilt = Math.sin(t * 7) * 0.035; }
    else if (ph === "grab") { fi = 5; tilt = 0.04; }
    else { fi = 6; bob = Math.abs(Math.sin(t * 15)) * 4; tilt = 0.08 + Math.sin(t * 15) * 0.04; sy = 1 + Math.sin(t * 30) * 0.035; }
    const im = FR[fi];
    if (im.complete && im.naturalWidth) {
      const h = SZ - 14, w = h * im.naturalWidth / im.naturalHeight;
      g.save(); g.translate(SZ / 2, SZ - 5);
      g.fillStyle = "rgba(0,0,0,.22)"; g.beginPath(); g.ellipse(0, 0, w * 0.32 * (1 - bob / 20), 3.5, 0, 0, 6.29); g.fill();
      g.translate(0, -bob); g.rotate(tilt); g.scale(flip ? -1 : 1, sy); g.drawImage(im, -w / 2, -h, w, h); g.restore(); }
    const mark = ph === "back" ? "?" : ph === "eye" ? "!" : "";
    if (mark) { g.save(); g.translate(SZ / 2 + 22, 11); g.fillStyle = "#fff"; g.strokeStyle = "#16161c"; g.lineWidth = 1.5; g.beginPath(); g.arc(0, 0, 8, 0, 6.29); g.fill(); g.stroke();
      g.fillStyle = mark === "!" ? "#e0412f" : "#16161c"; g.font = "bold 12px sans-serif"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(mark, 0, 1); g.restore(); }
    if (!T.stolen && t < 10) { g.fillStyle = "#ff4a3a"; g.strokeStyle = "#fff"; g.lineWidth = 3; g.font = "bold 13px sans-serif"; g.textAlign = "center"; const n = String(Math.max(0, Math.ceil(10 - t))); g.strokeText(n, SZ / 2 - 22, 12); g.fillText(n, SZ / 2 - 22, 12); }
  }
'''
s = s[:i] + NEW + s[j:]
rep('translate(${Math.round(x - SZ / 2)}px,${Math.round(gy - SZ + 22)}px)', 'translate(${Math.round(x - SZ / 2)}px,${Math.round(Math.max(gy - SZ + 30, 4))}px)')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
