# V706 (Freigaben Martin 13.11. 09:20, Punkte 3 und 6):
# - Coach-Angebot (ovCoachAd) zählt als offenes Fenster → Join öffnet nicht mehr darüber, wartet auf die nächste Pause.
# - Blue/Rosie-Blase (#buddy) unsichtbar, solange ein Fenster offen ist (Funk-Blase #coach bleibt wie bisher).
# - gameover.mp4 wird separat auf 44,1 kHz neu kodiert (Server, ffmpeg).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep('GAME_VER = "V705"', 'GAME_VER = "V706"')
rep('function uiWinOpen() { try { const v = id => { const e = document.getElementById(id); return e && !e.hidden && getComputedStyle(e).display !== "none"; }; if (v("ovHackAd")) return true;',
    'function uiWinOpen() { try { const v = id => { const e = document.getElementById(id); return e && !e.hidden && getComputedStyle(e).display !== "none"; }; if (v("ovHackAd") || v("ovCoachAd")) return true;   /* V706: Coach-Angebot zählt als Fenster */')
rep('window.__playScreen = () => {',
    '/* V706: Blue/Rosie-Blase aus, solange ein Fenster offen ist */\n'
    'setInterval(() => { try { const b = document.getElementById("buddy"); if (!b) return; const vis = e => !e.hidden && getComputedStyle(e).display !== "none" && getComputedStyle(e).visibility !== "hidden";\n'
    '  const open = (typeof uiWinOpen === "function" && uiWinOpen()) || [...document.querySelectorAll(\'body > [id^="ov"]\')].some(vis); b.style.visibility = open ? "hidden" : ""; } catch (e) {} }, 250);\n'
    'window.__playScreen = () => {')
open(dst, "w", encoding="utf8").write(s)
print("ok V706")
