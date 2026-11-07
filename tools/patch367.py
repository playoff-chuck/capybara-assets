"""V367 (Martin 07.11. 08:17): Während Tutorial und Ideengeber (General-Hinweiskarten «NEW») hält das Spiel im Hintergrund an.
- Hinweiskarte offen -> S.coachHold: Spiel steht (frozen), Musik läuft weiter; «Got it», Antippen oder 5,5 s schließen.
- Tutorial Schritt 1–4 wartete schon (Welle/Block stehen). Schritt 5 «HOLD THE RING» lief bisher 20 s mit laufender Welle
  im Hintergrund -> jetzt steht das Spiel, bis «Got it» getippt wird."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V366";', 'const GAME_VER = "V367";')
rep('function frozen() { return !S.started || S.over || S.paused ||', 'function frozen() { return !S.started || S.over || S.paused || S.coachHold ||')
rep('!S.mapShow && !S.tiltCard);\n  if (S.mix) stepMix(dt);', '!S.mapShow && !S.tiltCard && !S.coachHold);\n  if (S.mix) stepMix(dt);')
rep('LS.set("tarnturm-hint-" + key, "1"); hintKey = key;', 'LS.set("tarnturm-hint-" + key, "1"); hintKey = key; try { if (S && S.started && !S.over) S.coachHold = true; } catch (e) {}   /* V367: Spiel steht, solange der General erklärt */')
rep('function hintEnd() { if (!hintKey) return; hintKey = null;', 'function hintEnd() { if (!hintKey) return; hintKey = null; try { if (S) S.coachHold = false; } catch (e) {}')
rep('{ t: "HOLD THE RING", s: "Monsters run the lane. Full laps cost lives. Clear rows for gold. Good luck, squad!", at: "board", done: () => TUT.t >= 20 },',
    '{ t: "HOLD THE RING", s: "Monsters run the lane. Full laps cost lives. Clear rows for gold. Good luck, squad!", at: "board", done: () => false },   /* V367: endet mit «Got it», Spiel steht bis dahin */')
rep('tutShow(); }\nfunction tutEnd(skipped) { TUT.on = false; $("coach").hidden = true; coachHi(null);',
    'tutShow(); }\nfunction tutEnd(skipped) { TUT.on = false; S.coachHold = false; $("coachSkip").textContent = "Skip tutorial"; $("coach").hidden = true; coachHi(null);')
rep('$("coachT").textContent = st.t; $("coachS").textContent = st.s; snd("radio"); tutPlace(); }',
    '$("coachT").textContent = st.t; $("coachS").textContent = st.s; const last = TUT.step === TUT_STEPS.length - 1; S.coachHold = last; $("coachSkip").textContent = last ? "Got it" : "Skip tutorial"; snd("radio"); tutPlace(); }')
rep('$("coachSkip").addEventListener("click", () => { if (TUT.on) tutEnd(true); else hintEnd(); });',
    '$("coachSkip").addEventListener("click", () => { if (TUT.on) tutEnd(TUT.step < TUT_STEPS.length - 1); else hintEnd(); });')
rep('function tutAbort() { if (TUT.on) { TUT.on = false; $("coach").hidden = true; coachHi(null); } }',
    'function tutAbort() { if (TUT.on) { TUT.on = false; S.coachHold = false; $("coachSkip").textContent = "Skip tutorial"; $("coach").hidden = true; coachHi(null); } }')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
