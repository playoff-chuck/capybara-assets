import sys, os, subprocess
# V727 (Martin 16.11.2026 «Ок»): Tutorial-Ausstieg bei Schritt 4–6 (Turm bauen) entschärfen.
#  1) Text nennt den gelben Wagen-Knopf statt «SHOP» (Knopf zeigt nur ein Symbol).
#  2) Shop im Tutorial: Boss-Hack-Banner, Training, Spezial und gesperrte Dinge weg (außer im Spezial-Schritt).
#  3) Schritt «Baue einen Turm»: Steine stehen still, bis der Shop offen ist.
#  4) Im Baumodus des Tutorials wird der fallende Stein nicht gezeichnet (lag über dem Hinweistext).
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V726";', 'const GAME_VER = "V727";')
rep('s: "Tap SHOP, then PLACE.", at: "bBuild"', 's: "Tap the orange cart button, then PLACE.", at: "bBuild"')
rep('S.tiltCard || S.gestInfo || !!(window.__tipBulb && window.__tipBulb.open); }',
    'S.tiltCard || S.gestInfo || !!(window.__tipBulb && window.__tipBulb.open) || tutBuildHold(); }\nfunction tutBuildHold() { try { return !!(TUT.on && (TUT_STEPS[TUT.step] || {}).ar === "build"); } catch (e) { return false; } }   /* V727 */')
rep('if (lzk2 < 1 && p && S.started && !S.over) {', 'if (lzk2 < 1 && p && S.started && !S.over && !(TUT.on && S.mode === "build")) {   /* V727 */')
rep('''  $("sheetIn").innerHTML = h; $("sheetIn").classList.add("pk", "shopV");''',
    '''  $("sheetIn").innerHTML = h; try { if (TUT.on && (TUT_STEPS[TUT.step] || {}).ar !== "spec") { const si = $("sheetIn"); si.querySelectorAll(".shopItem.cSpe,.shopCat.cSpe,.shopItem.cTra,.shopCat.cTra,.coachAd").forEach(e => e.remove()); si.querySelectorAll(".shopItem").forEach(e => { if (e.querySelector(".lk")) e.remove(); }); } } catch (e) {}   /* V727: Tutorial-Shop aufgeräumt */ $("sheetIn").classList.add("pk", "shopV");''')
open(dst, "w", encoding="utf-8").write(s)
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang727.py"), os.path.join(os.path.dirname(os.path.abspath(dst)), "lang")], check=True)
