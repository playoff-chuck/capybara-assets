#!/usr/bin/env python3
"""V497 (Martin 09.11. 11:36–11:40):
- Startscreen-Logo (#stLogo) 35 % kleiner.
- Tipp-Karte (#tipBulb): GOT IT kleiner, rechts, erst sichtbar nach den 3 s Sperre (vorher grau, aber ohne Wirkung).
- Tutorial-/Hinweis-Fenster (#coach): «Got it» genauso – kleiner, rechts, erst nach 3 s sichtbar; «Skip tutorial» bleibt sofort da, aber auch rechts.
Aufruf: python3 tools/patch497.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V496";', 'const GAME_VER = "V497";')
rep('#stLogo{width:126px!important;height:106px!important}', '#stLogo{width:82px!important;height:69px!important}')
# Tipp-Karte
rep('#tipBulb button:disabled{opacity:.45}',
    '#tipBulb button{display:block;width:fit-content;margin-left:auto;font-size:13px!important;padding:4px 10px 3px!important;border-width:2px!important;box-shadow:0 2px 0 #3a2414!important;transition:opacity .25s}#tipBulb button:disabled{visibility:hidden;opacity:0}')
# Coach: «Got it» erst nach 3 s
rep('$("coachSkip").addEventListener("click", () => { if (TUT.on) tutEnd(TUT.step < TUT_STEPS.length - 1); else hintEnd(); });',
    'function coachArm() { const b = $("coachSkip"); b.classList.add("wait"); clearTimeout(coachArm.t); coachArm.t = setTimeout(() => b.classList.remove("wait"), 3000); }   /* V497: «Got it» erst nach 3 s zeigen */\n'
    '$("coachSkip").addEventListener("click", () => { if ($("coachSkip").classList.contains("wait")) return; if (TUT.on) tutEnd(TUT.step < TUT_STEPS.length - 1); else hintEnd(); });')
rep('$("coachSkip").textContent = last ? "Got it" : "Skip tutorial";',
    '$("coachSkip").textContent = last ? "Got it" : "Skip tutorial"; if (last) coachArm(); else { clearTimeout(coachArm.t); $("coachSkip").classList.remove("wait"); }')
rep('$("coachT").textContent = title; $("coachS").textContent = sub; $("coachSkip").textContent = "Got it";',
    '$("coachT").textContent = title; $("coachS").textContent = sub; $("coachSkip").textContent = "Got it"; coachArm();')
rep('$("coachSkip").textContent = "Got it"; const a = $("coachArrow"), card = c.querySelector(".coachCard"); coachHi(null); a.style.display = "none";',
    '$("coachSkip").textContent = "Got it"; coachArm(); const a = $("coachArrow"), card = c.querySelector(".coachCard"); coachHi(null); a.style.display = "none";')
rep('$("coach").hidden = true; coachHi(null); $("coachSkip").textContent = "Skip tutorial"; clearTimeout(hintT); }',
    '$("coach").hidden = true; coachHi(null); $("coachSkip").textContent = "Skip tutorial"; $("coachSkip").classList.remove("wait"); clearTimeout(hintT); }')
rep('#coach.genTalk #coachSkip{grid-area:sk;',
    '#coachSkip{display:block;width:fit-content;margin-left:auto!important}#coachSkip.wait{visibility:hidden}#coach.genTalk #coachSkip{grid-area:sk;justify-self:end;')
open(p, "w", encoding="utf-8").write(s); print("ok V497")
