#!/usr/bin/env python3
# V659 (Martin 12.11. 13:35/13:36):
#  1) Umfrage «How do you like the game?» hat oberste Priorität: immer ganz oben (über jedem Fenster),
#     nicht wegklickbar, kein automatisches Ausblenden, verschwindet erst nach einer Antwort.
#     Unbeantwortet bleibt sie auch nach Neuladen bestehen (Merker "s" = gezeigt, "1" = beantwortet).
#  2) Mayday-Zehntonne (Rettung bei hohem Stapel) nur BIS Welle 30 (vorher: erst AB Welle 30). Nicht im Tutorial.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V658";', 'const GAME_VER = "V659";')

# --- 2) Mayday bis Welle 30
rep('V316: Rettungs-Lucky-Supply ab Welle 30, wenn der Stapel 5 Felder unter die Decke reicht */',
    'V316/V659: Rettungs-Lucky-Supply BIS Welle 30, wenn der Stapel 5 Felder unter die Decke reicht */')
rep('|| S.won || (S.wave || 0) < 30 || S.ton || S.rotMode) return;   /* V560: nicht im gekippten Feld */',
    '|| S.won || (S.wave || 0) > 30 || (typeof TUT !== "undefined" && TUT.on) || S.ton || S.rotMode) return;   /* V560: nicht im gekippten Feld · V659: nur bis W30, nicht im Kurs */')

# --- 1) Umfrage ganz oben
rep('#pollCard{position:fixed;left:50%;top:calc(env(safe-area-inset-top,0px) + 118px);z-index:72;',
    '#pollCard{position:fixed;left:50%;top:calc(env(safe-area-inset-top,0px) + 118px);z-index:2147483000;')
rep('''function pollShow(at) { if (!live() || S.nuts) return; pAt = at; try { LS.set("capy-poll-" + at, "1"); } catch (e) {}''',
    '''function pollShow(at) { if (!pc.hidden && pc.classList.contains("on") && pAt === at) return; pAt = at; try { LS.set("capy-poll-" + at, "s"); } catch (e) {}   /* V659: "s" = gezeigt, offen */
      try { if (pc.parentNode !== document.body || document.body.lastElementChild !== pc) document.body.appendChild(pc); } catch (e) {}''')
rep('''pc.hidden = false; requestAnimationFrame(() => pc.classList.add("on")); try { snd("uiTap"); } catch (e) {}
      clearTimeout(pT); pT = setTimeout(() => { ev("poll", { v: "x", at }); pollHide(); }, 12000); }''',
    '''pc.hidden = false; requestAnimationFrame(() => pc.classList.add("on")); try { snd("uiTap"); } catch (e) {}
      clearTimeout(pT); }   /* V659: kein automatisches Ausblenden */''')
rep('''if (!b) return; const v = +b.dataset.v; ev("poll", { v, at: pAt }); try { snd("uiTap"); } catch (er) {} clearTimeout(pT);''',
    '''if (!b) return; const v = +b.dataset.v; ev("poll", { v, at: pAt }); try { LS.set("capy-poll-" + pAt, "1"); } catch (er) {} try { snd("uiTap"); } catch (er) {} clearTimeout(pT);''')
rep('''const go = () => { if (!live() || S.nuts) return; if (typeof uiWinOpen === "function" && uiWinOpen()) { setTimeout(go, 2500); return; } pollShow(at); };
      if (typeof window.__whenCalm === "function") window.__whenCalm(go, 4000); else setTimeout(go, 4000); }''',
    '''setTimeout(() => pollShow(at), 1500); }   /* V659: sofort, über allem */''')
rep('''setInterval(() => { try { if (!pc.hidden && pc.classList.contains("on") && ((typeof uiWinOpen === "function" && uiWinOpen()) || !live())) { clearTimeout(pT); pollHide(); try { LS.set("capy-poll-" + pAt, "0"); } catch (e) {} if (live()) pollLater(pAt); } } catch (e) {} }, 700);''',
    '''setInterval(() => { try {   /* V659: offene Umfrage bleibt sichtbar und ganz oben (auch nach Neuladen) */
      if (pc.hidden) { for (const at of [7, 17]) if (LS.get("capy-poll-" + at) === "s" || LS.get("capy-poll-" + at) === "0") { pollShow(at); break; } }
      else if (document.body.lastElementChild !== pc) document.body.appendChild(pc); } catch (e) {} }, 700);''')
# --- 3) «Thanks!»-Karte nur so breit wie das Wort (Martin 13:36)
rep('#pollCard[hidden]{display:none}', '#pollCard[hidden]{display:none}\n#pollCard.thx{width:auto;max-width:86vw;padding:8px 18px}#pollCard.thx b{margin:2px 0;white-space:nowrap}#pollCard.thx .pWhy{margin-top:6px}')
rep("""pc.innerHTML = '<small>QUICK QUESTION</small>""", """pc.classList.remove("thx"); pc.innerHTML = '<small>QUICK QUESTION</small>""")
rep("""pc.innerHTML = '<b>Thanks!</b>'""", """pc.classList.add("thx"); pc.innerHTML = '<b>Thanks!</b>'""")
open(p, "w", encoding="utf-8").write(s); print("ok V659")
