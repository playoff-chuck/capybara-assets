"""V204: Nach dem Coach-Training (aus dem Shop) führt «Back» zurück in den Shop statt ins Spiel."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V203";', 'const GAME_VER = "V204";')
rep('function closeHack() { window.__hackBack = true; HK.coach = false;', 'function closeHack() { const wasCoach = !!HK.coach; window.__hackBack = true; HK.coach = false;')
rep('HK.phase = "off"; S.duel = false; S.hackDone = S.wave; }', 'HK.phase = "off"; S.duel = false; S.hackDone = S.wave; if (wasCoach && S.started && !S.over) setTimeout(() => { try { openShop(); } catch (e) {} }, 80); }')
rep('snd(win ? "hkWin" : "hkLose"); $("hkAgain").textContent = "AGAIN ▶"; return; }', 'snd(win ? "hkWin" : "hkLose"); $("hkAgain").textContent = "AGAIN ▶"; $("hkBack").textContent = "Back to the shop"; return; }')
rep('document.querySelector(".hkScoreL").innerHTML = `<span>YOU</span><span>BOSS</span>`;', 'document.querySelector(".hkScoreL").innerHTML = `<span>YOU</span><span>BOSS</span>`; $("hkBack").textContent = "Back to the game";')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
