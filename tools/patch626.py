#!/usr/bin/env python3
# V626 (Martin 11.11. 13:33):
# 1) Coach-Tipps: Tipp 3 (Sackgassen) raus, «Timer entscheidet» wird Nr. 3 – drei Tipps.
# 2) Erster Boss-Hack gratis: Startkarte nur «Босс вызывает тебя на взлом!» + «ДАЛЕЕ ▶» (kein Einsatz, kein Text dazu) → Ollie-Tipps → Duell ohne Einsatz.
# 3) Kein Gratis-Probelauf mehr (zweiter Hack gleich mit Gold-Einsatz).
import sys, os, json
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V625";', 'const GAME_VER = "V626";')
rep('''    ["3", "WATCH OUT: DEAD ENDS", "A wire with ⊥ leads nowhere – don't waste a capsule on it. ∞ stays lit to the end – grab it early."],
    ["4", "THE TIMER DECIDES",''', '''    ["3", "THE TIMER DECIDES",''')
rep("Coach Ollie: four tricks – and the boss is yours!", "Coach Ollie: three tricks – and the boss is yours!")
# erster Hack gratis
rep('fst.textContent = "First hack: your stake is fixed at 10 % of your gold.";', 'fst.textContent = "The boss challenges you to a hack!";')
rep('''      if (f) { const rg = $("hkRange"); rg.value = Math.max(0, Math.min(+rg.max || 0, Math.round((S.gold | 0) * 0.1 / 10) * 10)); hkStakeUI(); } } catch (e) {} return r; };''',
    '''      const gb = $("hkGo"); if (f) { $("hkRange").value = 0; hkStakeUI(); gb.textContent = "NEXT ▶"; } else if (gb.textContent !== "HACK!") gb.textContent = "HACK!"; } catch (e) {} return r; };   /* V626: erster Hack gratis */''')
rep('hb.classList.remove("hkFirst"); fst.hidden = true; } catch (e) {} }, true);', 'hb.classList.remove("hkFirst"); fst.hidden = true; $("hkGo").textContent = "HACK!"; } catch (e) {} }, true);')
rep('#hackBet.hkFirst #hkRange,#hackBet.hkFirst .hkChips{display:none!important}#hkFirstP{margin:4px 0 8px;font:800 14px/1.25 "Baloo 2",sans-serif;color:#ffd84d;text-align:center}',
    '#hackBet.hkFirst #hkRange,#hackBet.hkFirst .hkChips,#hackBet.hkFirst .hkStake,#hackBet.hkFirst>p:not(#hkFirstP),#hackBet.hkFirst #hkSkip,#hackBet.hkFirst #hkTrial,#hackBet.hkFirst #hkTrialP{display:none!important}#hkFirstP{margin:6px 0 14px;font:800 18px/1.3 "Baloo 2",sans-serif;color:#3a2414;text-align:center}')
# kein Probelauf mehr
rep('const offer = () => { try { return LS.get("capy-hk-trial") !== "1" && !HK.coach', 'const offer = () => { try { return false && LS.get("capy-hk-trial") !== "1" && !HK.coach')
rep('setTimeout(() => { try { window.__hkTips.showThen(() => openHack(true)); } catch (e) {} }, 5300);', 'setTimeout(() => { try { openHack(true); } catch (e) {} }, 5300);')
rep('const th = !!(S && S.testRun && S.testKind === "hack");', 'const th = !!(S && S.testRun && (S.testKind === "hack" || S.testKind === "tips"));')
open(p, "w", encoding="utf-8").write(s)
K = ["Coach Ollie: three tricks – and the boss is yours!", "The boss challenges you to a hack!", "NEXT ▶"]
T = {"en": K, "ru": ["Тренер Олли: три приёма – и босс твой!", "Босс вызывает тебя на взлом!", "ДАЛЕЕ ▶"],
     "de": ["Coach Ollie: drei Tricks – und der Boss gehört dir!", "Der Boss fordert dich zum Hack heraus!", "WEITER ▶"],
     "es": ["Entrenador Ollie: tres trucos ¡y el jefe es tuyo!", "¡El jefe te reta a un hackeo!", "SIGUIENTE ▶"],
     "pt": ["Treinador Ollie: três truques – e o chefe é seu!", "O chefe te desafia para um hack!", "PRÓXIMO ▶"]}
for l, vals in T.items():
    q = os.path.join(site, "lang", l + ".json"); d = json.loads(open(q, encoding="utf-8").read())
    for k, v in zip(K, vals):
        if k == "NEXT ▶" and k in d: continue
        d[k] = v
    open(q, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=0))
print("ok V626")
