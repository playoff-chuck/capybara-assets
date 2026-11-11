#!/usr/bin/env python3
# V619 (Martin 11.11. 12:55): Vor dem ersten Boss-Hack ganzseitige Werbe-Einblendung: Coach Ollie gibt 4 Gratis-Tipps (Bild Nano Banana Pro, img/hk_tips.webp),
# muss bestätigt werden (3 s Sperre). Einmalig (capy-hk-tips). Spiel steht solange (coachHold → Musik blendet aus).
import sys, os, json
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
img = os.path.join(site, "img", "hk_tips.webp")
if not os.path.exists(img):
    from PIL import Image
    Image.open("/srv/media/hk_tips_coach.png").convert("RGB").save(img, quality=80, method=6)
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V618";', 'const GAME_VER = "V619";')
JS = r'''/* V619: Coach Ollie – 4 Gratis-Tipps vor dem ersten Boss-Hack */
try { (() => {
  const st = document.createElement("style");
  st.textContent = `#ovHkTips{position:fixed;inset:0;z-index:9600;display:flex;flex-direction:column;justify-content:space-between;opacity:0;transition:opacity .3s;background:#14240f url("img/hk_tips.webp?v=619") center top/cover no-repeat}
#ovHkTips.on{opacity:1}#ovHkTips[hidden]{display:none!important}
#ovHkTips::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,16,6,.78) 0,rgba(10,16,6,.15) 22%,rgba(10,16,6,0) 38%,rgba(10,20,8,.55) 55%,rgba(8,18,8,.9) 100%);pointer-events:none}
#ovHkTips .htTop{position:relative;text-align:center;padding:max(18px,env(safe-area-inset-top)) 14px 0;color:#fff}
#ovHkTips .htK{display:inline-block;font:800 12px/1 "Baloo 2",sans-serif;letter-spacing:.12em;color:#3a2414;background:#ffd23a;border:2px solid #3a2414;border-radius:999px;padding:6px 12px 5px;box-shadow:0 2px 0 #3a2414}
#ovHkTips h2{margin:8px 0 0;font:400 clamp(34px,11vw,50px)/1 Bangers,Impact,sans-serif;letter-spacing:.04em;color:#fff;text-shadow:0 3px 0 #3a2414,0 0 14px rgba(255,210,58,.55)}
#ovHkTips .htSub{margin:4px 0 0;font:800 15px/1.2 "Baloo 2",sans-serif;color:#ffe9a8;text-shadow:0 2px 2px #000}
#ovHkTips .htBot{position:relative;padding:0 12px max(12px,env(safe-area-inset-bottom))}
#ovHkTips ol{list-style:none;margin:0 0 10px;padding:0;display:grid;gap:7px}
#ovHkTips li{display:flex;gap:10px;align-items:center;background:#fff6dc;border:3px solid #3a2414;border-radius:16px;padding:8px 10px;box-shadow:0 3px 0 #3a2414}
#ovHkTips li>i{flex:0 0 34px;height:34px;border-radius:50%;display:grid;place-items:center;background:#ffd23a;border:2px solid #3a2414;font:400 18px/1 Bangers,sans-serif;font-style:normal;color:#3a2414}
#ovHkTips li b{display:block;font:400 19px/1 Bangers,Impact,sans-serif;letter-spacing:.04em;color:#2f6f4f}
#ovHkTips li span{display:block;font:700 14px/1.25 "Baloo 2",sans-serif;color:#3a2414}
#ovHkTips .htGo{position:relative;display:flex!important;flex-direction:row!important;align-items:center;justify-content:center;gap:8px;white-space:nowrap;width:100%;min-height:0;padding:13px 10px;font:400 24px/1 Bangers,Impact,sans-serif;letter-spacing:.05em;background:#7fd35a!important;color:#1f3a12!important;border:3px solid #3a2414!important;border-radius:16px;box-shadow:0 4px 0 #3a2414!important}
#ovHkTips .htGo:disabled{opacity:.55}#ovHkTips .htGo em{display:inline;font-style:normal;opacity:.8}
@media (max-height:700px){#ovHkTips li{padding:6px 9px}#ovHkTips li span{font-size:13px}#ovHkTips li b{font-size:17px}#ovHkTips h2{font-size:34px}#ovHkTips .htSub{display:none}}`;
  document.head.appendChild(st);
  const ov = document.createElement("div"); ov.id = "ovHkTips"; ov.hidden = true;
  const tips = [["1", "PICK YOUR SIDE", "At the start choose the side with more ∞ and Y forks."],
    ["2", "TAP RIGHT AWAY", "As soon as it starts, tap your buttons: a lit wire paints a centre cell in your colour."],
    ["3", "WATCH OUT: DEAD ENDS", "A wire with ⊥ leads nowhere – don't waste a capsule on it. ∞ stays lit to the end – grab it early."],
    ["4", "THE TIMER DECIDES", "When time runs out, whoever has more cells in their colour wins."]];
  ov.innerHTML = '<div class="htTop"><span class="htK">FREE TIPS FROM THE COACH</span><h2>BOSS HACK</h2><p class="htSub">Coach Ollie: four tricks – and the boss is yours!</p></div>'
    + '<div class="htBot"><ol>' + tips.map(t => `<li><i>${t[0]}</i><div><b>${t[1]}</b><span>${t[2]}</span></div></li>`).join("") + '</ol><button type="button" class="htGo" disabled>GOT IT – LET\'S HACK!<em>3</em></button></div>';
  document.body.appendChild(ov);
  const go = ov.querySelector(".htGo"); let after = null, tI = 0;
  const need = () => { try { return LS.get("capy-hk-tips") !== "1" && S && S.started && !S.over && !S.nuts && !S.testRun && !S.replay; } catch (e) { return false; } };
  function show(cb) { after = cb; try { S.coachHold = true; } catch (e) {} ov.hidden = false; requestAnimationFrame(() => ov.classList.add("on")); try { snd("radio"); } catch (e) {}
    go.disabled = true; let n = 3; const em = go.querySelector("em"); em.textContent = n; clearInterval(tI);
    tI = setInterval(() => { n--; if (n > 0) { em.textContent = n; return; } clearInterval(tI); em.textContent = ""; go.disabled = false; }, 1000); }
  go.addEventListener("click", e => { e.stopPropagation(); if (go.disabled) return; try { LS.set("capy-hk-tips", "1"); } catch (x) {} try { snd("uiTap"); } catch (x) {}
    ov.classList.remove("on"); setTimeout(() => { ov.hidden = true; }, 300); try { S.coachHold = false; } catch (x) {} const f = after; after = null; if (f) f(); });
  const _oh = openHack; openHack = function (force) { if (!need() || (!force && !hkOfferOn())) return _oh.apply(this, arguments); show(() => _oh(true)); };
  window.__hkTips = { show: () => show(null), need };
})(); } catch (e) { console.error("v619 hkTips", e); }

/* V587: Zipfel der Aufgabenkarte zeigt auf den General im Streifen */'''
rep('/* V587: Zipfel der Aufgabenkarte zeigt auf den General im Streifen */', JS)
open(p, "w", encoding="utf-8").write(s)
K = ["FREE TIPS FROM THE COACH", "BOSS HACK", "Coach Ollie: four tricks – and the boss is yours!", "PICK YOUR SIDE", "At the start choose the side with more ∞ and Y forks.",
     "TAP RIGHT AWAY", "As soon as it starts, tap your buttons: a lit wire paints a centre cell in your colour.",
     "WATCH OUT: DEAD ENDS", "A wire with ⊥ leads nowhere – don't waste a capsule on it. ∞ stays lit to the end – grab it early.",
     "THE TIMER DECIDES", "When time runs out, whoever has more cells in their colour wins.", "GOT IT – LET'S HACK!"]
T = {"ru": ["БЕСПЛАТНЫЕ СОВЕТЫ ТРЕНЕРА", "ВЗЛОМ БОССА", "Тренер Олли: четыре приёма – и босс твой!", "ВЫБЕРИ СТОРОНУ", "В начале выбирай сторону, где больше ∞ и развилок Y.",
            "ЖМИ СРАЗУ", "Как только старт – жми свои кнопки: горящий провод красит клетку в центре в твой цвет.",
            "ОСТОРОЖНО: ТУПИКИ", "Провод с ⊥ никуда не ведёт – не трать на него капсулу. ∞ горит до конца – хватай его пораньше.",
            "РЕШАЕТ ТАЙМЕР", "Когда время выйдет, побеждает тот, у кого больше клеток своего цвета.", "ПОНЯЛ – ВЗЛАМЫВАЕМ!"],
     "de": ["GRATIS-TIPPS VOM TRAINER", "BOSS-HACK", "Coach Ollie: vier Tricks – und der Boss gehört dir!", "WÄHLE DEINE SEITE", "Nimm am Anfang die Seite mit mehr ∞ und Y-Gabeln.",
            "SOFORT TIPPEN", "Sobald es losgeht, tippe deine Knöpfe: Ein leuchtender Draht färbt ein Mittelfeld in deiner Farbe.",
            "VORSICHT: SACKGASSEN", "Ein Draht mit ⊥ führt nirgendwohin – keine Kapsel verschwenden. ∞ leuchtet bis zum Schluss – früh schnappen.",
            "DER TIMER ENTSCHEIDET", "Wenn die Zeit um ist, gewinnt, wer mehr Felder in seiner Farbe hat.", "VERSTANDEN – HACKEN!"],
     "es": ["CONSEJOS GRATIS DEL ENTRENADOR", "HACKEO AL JEFE", "Entrenador Ollie: cuatro trucos ¡y el jefe es tuyo!", "ELIGE TU LADO", "Al empezar, elige el lado con más ∞ y bifurcaciones Y.",
            "PULSA YA", "En cuanto empiece, pulsa tus botones: un cable encendido pinta una celda central de tu color.",
            "OJO: CALLEJONES", "Un cable con ⊥ no lleva a nada: no gastes una cápsula ahí. ∞ sigue encendido hasta el final: cógelo pronto.",
            "DECIDE EL TEMPORIZADOR", "Cuando se acaba el tiempo, gana quien tenga más celdas de su color.", "¡ENTENDIDO, A HACKEAR!"],
     "pt": ["DICAS GRÁTIS DO TREINADOR", "HACK DO CHEFE", "Treinador Ollie: quatro truques – e o chefe é seu!", "ESCOLHA SEU LADO", "No início, escolha o lado com mais ∞ e bifurcações Y.",
            "TOQUE LOGO", "Assim que começar, toque nos seus botões: um fio aceso pinta uma célula central com a sua cor.",
            "CUIDADO: BECOS", "Um fio com ⊥ não leva a lugar nenhum – não gaste uma cápsula nele. ∞ fica aceso até o fim – pegue cedo.",
            "O CRONÔMETRO DECIDE", "Quando o tempo acaba, vence quem tiver mais células da sua cor.", "ENTENDI – BORA HACKEAR!"]}
T["en"] = K
for l, vals in T.items():
    q = os.path.join(site, "lang", l + ".json"); d = json.loads(open(q, encoding="utf-8").read())
    for k, v in zip(K, vals):
        if k == "BOSS HACK" and k in d: continue
        d[k] = v
    open(q, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=0))
print("ok V619")
