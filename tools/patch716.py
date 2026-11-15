import sys, os
# V716: Leistung auf schwachen Handys (Martin 15.11.2026 09:33, Punkt 1). Messung Google-Handytest: Galaxy A03s 4 FPS, A06 12 FPS ab Welle 30.
#  1) 211 CSS-Regeln «body:has(…)» lösten bei jeder DOM-Änderung (HUD 10×/s) eine Stil-Neuberechnung des ganzen Baums aus.
#     Jetzt beim Laden in Body-Klassen (hzN) umgeschrieben; ein MutationObserver setzt die Klassen (gleiches Ergebnis, ca. 50 % weniger Stilarbeit).
#  2) renderLever las bei jedem HUD-Takt slot.clientHeight (erzwungenes Layout) → nur noch bei Änderung.
#  3) HUD schreibt die Zahlen nur, wenn sie sich ändern.
#  Aufruf: python3 tools/patch716.py src dst   (tools/v716_hasfix.js muss daneben liegen)
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V715";', 'const GAME_VER = "V716";')
rep('''  $("sLives").textContent = S.lives; $("sGold").textContent = S.gold; $("sWave").textContent = S.wave; $("sScore").textContent = S.score.toLocaleString("en-US");
  $("sLines").textContent = S.lines; $("sKills").textContent = S.kills;''', '''  { const tx = (id, v) => { const e = $(id); v = String(v); if (e && e.textContent !== v) e.textContent = v; };   /* V716: nur bei Änderung schreiben */
    tx("sLives", S.lives); tx("sGold", S.gold); tx("sWave", S.wave); tx("sScore", S.score.toLocaleString("en-US")); tx("sLines", S.lines); tx("sKills", S.kills); }''')
rep('''  [...n.children].forEach((el, i) => { el.className = i === cur ? "on" : i <= mi ? "ok" : ""; });
  const h = slot.clientHeight - 12; $("lvKnob").style.top = (6 + h - h * cur / (SPEEDS.length - 1)) + "px";
  $("lvVal").textContent = "×" + SPEEDS[cur];''', '''  { const key = cur + ":" + mi + ":" + innerWidth + "x" + innerHeight; if (slot._lvKey === key) return; slot._lvKey = key; }   /* V716: kein erzwungenes Layout 10×/s */
  [...n.children].forEach((el, i) => { const c = i === cur ? "on" : i <= mi ? "ok" : ""; if (el.className !== c) el.className = c; });
  const h = slot.clientHeight - 12; if (h <= 0) slot._lvKey = ""; $("lvKnob").style.top = (6 + h - h * cur / (SPEEDS.length - 1)) + "px";
  { const v = "×" + SPEEDS[cur]; if ($("lvVal").textContent !== v) $("lvVal").textContent = v; }''')
HZ = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "v716_hasfix.js"), encoding="utf-8").read()
rep('</body></html>', '<script id="v716hz">' + HZ + '</script>\n</body></html>')
open(dst, "w", encoding="utf-8").write(s)
