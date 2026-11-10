#!/usr/bin/env python3
# V591 (Martin 11.11. 01:57): Tutorial
# - Abdunkeln bei neuer Aufgabe ganz entfernt (Martin 01:59: «verwirrt»); Blöcke fallen normal, Einflug von oben bleibt
# - Im Tutorial keine Sonder-Bildschirme: keine Vorstellungs-Fenster (neues Monster/neue Waffe) und keine Angebots-Werbung –
#   sie kommen danach im normalen Spiel
# - Vom General nur eine kurze Begrüßung (erste Meldung), danach keine weiteren General-Meldungen bis zum Ende des Tutorials
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V590";', 'const GAME_VER = "V591";')
rep('  if (!(S.lockT > 0) && !(S.tutEnter > performance.now()) && !(S.tutDimT > performance.now())) S.gravT += dt;',
    '  if (!(S.lockT > 0) && !(S.tutEnter > performance.now())) S.gravT += dt;   /* V591: im Dunkeln fällt alles normal */')
rep('''function showIntro(q) {
  const mon''', '''function showIntro(q) {
  try { if (typeof TUT !== "undefined" && TUT.on) { S.introQ = S.introQ || []; S.introQ.unshift(q); return; } } catch (e) {}   /* V591: im Tutorial keine Vorstellung – kommt später */
  const mon''')
rep('show(k, sale) { const free = sale === "free";', 'show(k, sale) { try { if (typeof TUT !== "undefined" && TUT.on) return; } catch (e) {} const free = sale === "free";   /* V591: keine Werbung im Tutorial */')
rep('''function msgPush(m) {
''', '''function msgPush(m) {
  try { if (typeof TUT !== "undefined" && TUT.on) { if (S.tutGreet) return; S.tutGreet = 1; } else if (S) S.tutGreet = 0; } catch (e) {}   /* V591: im Tutorial nur eine Begrüßung vom General */
''')
rep('  let t = null; window.__tutDim = () => { clearTimeout(t); d.classList.add("on");', '  let t = null; window.__tutDim = () => { return;   /* V591: kein Abdunkeln mehr */ clearTimeout(t); d.classList.add("on");')
open(dst, "w", encoding="utf-8").write(s)
print("ok V591")
