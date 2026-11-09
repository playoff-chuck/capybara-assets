#!/usr/bin/env python3
"""V544 (Martin 09.11. 22:17): Sicherheitsabfrage beim HOW-TO-Knopf – Comic-Karte in der Bildschirmmitte
«START THE TUTORIAL AGAIN?» mit Figur, Knöpfen «YES, LET'S GO» und «CANCEL». Spiel steht, solange die Karte offen ist.
Ausschalten eines laufenden Tutorials bleibt ohne Abfrage.
Aufruf: python3 tools/patch544.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V543";', 'const GAME_VER = "V544";')
rep('''if (!S || !S.started || S.over) return; if (TUT.on) { tutEnd(true); return; } S.paused = false; tutStart(); });''',
    '''if (!S || !S.started || S.over) return; if (TUT.on) { tutEnd(true); return; } tutAsk(); });
  /* V544: Sicherheitsabfrage im Capybara-Comic-Stil */
  const st = document.createElement("style"); st.textContent = `#tutAsk{position:fixed;inset:0;z-index:95;display:grid;place-items:center;background:rgba(43,30,18,.45);opacity:0;transition:opacity .2s}
#tutAsk.on{opacity:1}#tutAsk[hidden]{display:none!important}
#tutAsk .taCard{position:relative;width:min(84vw,330px);background:#fff7e8;border:3px solid #3a2414;border-radius:24px;box-shadow:0 6px 0 #3a2414,0 14px 30px rgba(0,0,0,.4);padding:58px 18px 18px;text-align:center;transform:scale(.8) rotate(-2deg);transition:transform .32s cubic-bezier(.2,1.6,.4,1)}
#tutAsk.on .taCard{transform:none}
#tutAsk .taCard img{position:absolute;left:50%;top:-62px;width:112px;height:112px;object-fit:contain;transform:translateX(-50%);filter:drop-shadow(0 4px 0 rgba(58,36,20,.25))}
#tutAsk .taHat{position:absolute;right:16px;top:12px;width:42px;height:42px;border-radius:50%;background:#ffd34a;border:2.5px solid #3a2414;display:grid;place-items:center;transform:rotate(12deg)}#tutAsk .taHat svg{width:24px;height:24px}
#tutAsk b{display:block;font:400 26px/1.05 var(--f-display,"Bangers",sans-serif);letter-spacing:.04em;color:#3a2414;margin:4px 0 8px}
#tutAsk p{margin:0 0 16px;font:600 15px/1.35 "Baloo 2",Nunito,system-ui,sans-serif;color:#6b4a2b}
#tutAsk .taBtns{display:flex;gap:10px;justify-content:center}
#tutAsk button{flex:1;min-height:0;font:400 19px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.05em;color:#3a2414;border:2.5px solid #3a2414;border-radius:16px;box-shadow:0 4px 0 #3a2414;padding:11px 8px 9px}
#tutAsk button:active{transform:translateY(3px);box-shadow:0 1px 0 #3a2414}
#tutAsk .taYes{background:#7fd35a!important;color:#1f3a12!important}#tutAsk .taNo{background:#fff6e6!important}`; document.head.appendChild(st);
  const ask = document.createElement("div"); ask.id = "tutAsk"; ask.hidden = true;
  ask.innerHTML = '<div class="taCard"><img alt=""><span class="taHat">' + b.querySelector("svg").outerHTML + '</span><b>START THE TUTORIAL AGAIN?</b><p>We show you everything from the very first step.</p><div class="taBtns"><button type="button" class="taNo">CANCEL</button><button type="button" class="taYes">YES, LET\\'S GO</button></div></div>';
  document.body.appendChild(ask);
  function tutAskClose(go) { ask.classList.remove("on"); setTimeout(() => { ask.hidden = true; }, 200); try { snd("uiTap"); } catch (e) {} S.coachHold = false; window.__evtLast = performance.now();
    if (go && S && S.started && !S.over && !TUT.on) { S.paused = false; tutStart(); } }
  function tutAsk() { try { ask.querySelector("img").src = HERO_IMG[heroKey()]; } catch (e) {} S.coachHold = true; ask.hidden = false; requestAnimationFrame(() => ask.classList.add("on")); try { snd("radio"); } catch (e) {} }
  ask.querySelector(".taYes").addEventListener("click", e => { e.stopPropagation(); tutAskClose(true); });
  ask.querySelector(".taNo").addEventListener("click", e => { e.stopPropagation(); tutAskClose(false); });
  ask.addEventListener("click", e => { if (e.target === ask) tutAskClose(false); });''')
open(p, "w", encoding="utf-8").write(s); print("ok V544")
