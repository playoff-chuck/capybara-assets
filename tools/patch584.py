#!/usr/bin/env python3
# V584 (Martin 11.11. 01:15): Tutorial
# - Knopf «Skip tutorial» oben rechts in der Tutorial-Karte entfällt («Got it» bleibt, wo eine Lektion ihn braucht)
# - Abbrechen über den Hut-Knopf unten: öffnet im Tutorial ein zweites Menü «SKIP THE TUTORIAL?» mit
#   «KEEP LEARNING» / «SKIP TUTORIAL» (Spiel steht, solange es offen ist)
# - Jede neue Aufgabe: 3 s lang alles dunkel außer Kurs-Streifen oben und Aufgabenkarte, dann wieder hell
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V583";', 'const GAME_VER = "V584";')

# Hut-Knopf im Tutorial → Menü statt sofort beenden
rep('if (TUT.on) { tutEnd(true); return; } tutAsk(); });', 'if (TUT.on) { tutAsk(true); return; } tutAsk(); });   /* V584: im Kurs zweites Menü */')
rep('''  function tutAskClose(go) { ask.classList.remove("on"); setTimeout(() => { ask.hidden = true; }, 200); try { snd("uiTap"); } catch (e) {} S.coachHold = false; window.__evtLast = performance.now();
    if (go && S && S.started && !S.over && !TUT.on) { S.paused = false; tutStart(); } }
  function tutAsk() { try { ask.querySelector("img").src = HERO_IMG[heroKey()]; } catch (e) {} S.coachHold = true;''',
'''  const TA = { b: ask.querySelector("b"), p: ask.querySelector("p"), no: ask.querySelector(".taNo"), yes: ask.querySelector(".taYes") }, TA0 = { b: TA.b.textContent, p: TA.p.textContent, no: TA.no.textContent, yes: TA.yes.textContent };
  function tutAskClose(go) { ask.classList.remove("on"); setTimeout(() => { ask.hidden = true; }, 200); try { snd("uiTap"); } catch (e) {} const sk = ask.dataset.m === "skip"; ask.dataset.m = ""; window.__evtLast = performance.now();
    if (sk) { if (go && TUT.on) { S.coachHold = false; tutEnd(true); } else { try { const st = TUT_STEPS[TUT.step]; S.coachHold = !!(st && st.got && false); } catch (e) { S.coachHold = false; } } return; }   /* V584 */
    S.coachHold = false;
    if (go && S && S.started && !S.over && !TUT.on) { S.paused = false; tutStart(); } }
  function tutAsk(skip) { try { ask.querySelector("img").src = HERO_IMG[heroKey()]; } catch (e) {} ask.dataset.m = skip ? "skip" : "";
    if (skip) { TA.b.textContent = "SKIP THE TUTORIAL?"; TA.p.textContent = "You can start it again any time with this hat button (until wave 10)."; TA.no.textContent = "KEEP LEARNING"; TA.yes.textContent = "SKIP TUTORIAL"; }
    else { TA.b.textContent = TA0.b; TA.p.textContent = TA0.p; TA.no.textContent = TA0.no; TA.yes.textContent = TA0.yes; }
    S.coachHold = true;''')

# Skip-Knopf in der Karte nur noch als «Got it»
rep('S.coachHold = false; $("coachSkip").textContent = last ? "Got it" : "Skip tutorial";',
    'S.coachHold = false; $("coachSkip").textContent = last ? "Got it" : "Skip tutorial"; $("coachSkip").hidden = !last;   /* V584: kein «Skip» oben rechts */')
for a in ['$("coachSkip").textContent = "Got it"; coachArm();']:
    c = s.count(a); assert c >= 1, a
    s = s.replace(a, '$("coachSkip").textContent = "Got it"; $("coachSkip").hidden = false; coachArm();')
rep('function tutAbort() { if (TUT.on) { TUT.on = false; S.coachHold = false; $("coachSkip").textContent = "Skip tutorial";',
    'function tutAbort() { if (TUT.on) { TUT.on = false; S.coachHold = false; $("coachSkip").textContent = "Skip tutorial"; $("coachSkip").hidden = false;')

# 3 s Abdunkeln bei jeder neuen Aufgabe
rep('/* V573: fallender Block über der Tutorial-Karte */\n',
'''/* V584: neue Aufgabe – 3 s alles dunkel außer Kurs-Streifen und Aufgabenkarte */
try { (() => { const d = document.createElement("div"); d.id = "tutDim"; document.body.appendChild(d);
  const st = document.createElement("style"); st.textContent = "#tutDim{position:fixed;inset:0;z-index:903;background:rgba(12,7,3,.8);opacity:0;pointer-events:none;transition:opacity .35s ease}#tutDim.on{opacity:1}"; document.head.appendChild(st);
  let t = null; window.__tutDim = () => { clearTimeout(t); d.classList.add("on"); try { S.tutDimT = performance.now() + 3000; } catch (e) {} t = setTimeout(() => d.classList.remove("on"), 3000); };
  let last = -1; setInterval(() => { const on = typeof TUT !== "undefined" && TUT.on; if (!on) { last = -1; if (d.classList.contains("on")) { clearTimeout(t); d.classList.remove("on"); } return; }
    const c = document.getElementById("coach"), vis = c && !c.hidden && c.getClientRects().length && !document.body.classList.contains("ovUp") && !document.body.classList.contains("mapUp");
    if (vis && TUT.step !== last) { last = TUT.step; window.__tutDim(); } }, 150); })(); } catch (e) { console.error("v584 dim", e); }
/* V573: fallender Block über der Tutorial-Karte */
''')
# während des Abdunkelns steht das Spiel, der fallende Block wird nicht über die Karte gezeichnet
rep('  if (!(S.lockT > 0) && !(S.tutEnter > performance.now())) S.gravT += dt;', '  if (!(S.lockT > 0) && !(S.tutEnter > performance.now()) && !(S.tutDimT > performance.now())) S.gravT += dt;')
rep('    ox.clearRect(0, 0, W, H); shown = true;\n', '    ox.clearRect(0, 0, W, H); shown = true; if (S.tutDimT > performance.now()) return;   /* V584 */\n')
open(dst, "w", encoding="utf-8").write(s)
print("ok V584")
