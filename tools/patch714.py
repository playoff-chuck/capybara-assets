import sys, os, json, re
# V714: Browser-Version – Wellen 1–60 (Südamerika, Afrika) gratis; ab Welle 61 Sperre mit Bild (img/lock_cont.webp, Nano Banana Pro)
#  und Link in die App: RuStore in Russland (.ru-Domain, RuStore-App oder russische Zeitzone), sonst Google Play (Martin 14.11.2026 22:37).
#  In den Apps (RuStore-WebView, Play-TWA) bleibt vorerst alles offen – Kauf in der App folgt mit dem Billing.
#  Ausnahmen: Team (tarnturm-dev=1, capy-adm), Freischaltung capy-tour=1 (?tour=open), Ticket (capy-ticket=1). Nuts/Wiederholung/Testlauf nie gesperrt.
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V713";', 'const GAME_VER = "V714";')
JS = r'''
/* V714: Browser – ab Welle 61 weiter in der App */
try { (() => { const q = new URLSearchParams(location.search), ref = document.referrer || "";
  if (/^android-app:\/\/com\.playcapybarasquad\.app/.test(ref) || q.get("src") === "play") localStorage.setItem("capy-play", "1");
  if (q.get("tour") === "open") localStorage.setItem("capy-tour", "1"); } )(); } catch (e) {}
const WEB_FREE_W = 60;
function isApp() { try { return localStorage.getItem("capy-rustore") === "1" || localStorage.getItem("capy-play") === "1" || /; wv\)/.test(navigator.userAgent || ""); } catch (e) { return false; } }
function webLocked() { try { if (isApp()) return false; if (localStorage.getItem("tarnturm-dev") === "1" || localStorage.getItem("capy-adm") || localStorage.getItem("capy-tour") === "1" || FM.ticket()) return false; return true; } catch (e) { return false; } }
function inRussia() { try { if (/\.ru$/.test(location.hostname) || localStorage.getItem("capy-rustore") === "1") return true; const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
  return /^(Europe\/(Moscow|Kaliningrad|Samara|Volgograd|Saratov|Ulyanovsk|Astrakhan|Kirov|Simferopol)|Asia\/(Yekaterinburg|Omsk|Novosibirsk|Barnaul|Tomsk|Novokuznetsk|Krasnoyarsk|Irkutsk|Chita|Yakutsk|Khandyga|Vladivostok|Ust-Nera|Magadan|Sakhalin|Srednekolymsk|Kamchatka|Anadyr))$/.test(tz); } catch (e) { return false; } }
let gateQuiet = 0;
function gateShow() { let ov = document.getElementById("ovGate"); if (!ov) { ov = document.createElement("div"); ov.id = "ovGate"; ov.className = "overlay"; ov.hidden = true; document.body.appendChild(ov);
    ov.addEventListener("click", e => { e.stopPropagation(); const b = e.target.closest("button,a"); if (!b) return; try { snd("uiTap"); } catch (er) {} if (b.dataset.a === "later") { ov.hidden = true; gateQuiet = performance.now() + 20000; } }); }
  const ru = inRussia(), url = ru ? "https://www.rustore.ru/catalog/app/ru.capybarasquad.game" : "https://play.google.com/store/apps/details?id=com.playcapybarasquad.app";
  ov.innerHTML = `<div class="fmCard"><div class="fmPic" style="background-image:url(img/lock_cont.webp);background-position:50% 55%"><span class="fmTag">🔒 WORLD TOUR</span><span class="fmLockN">🔒 <span>ASIA</span></span></div><div class="fmBody"><h2>THE WORLD TOUR GOES ON IN THE APP</h2><p>South America and Africa are free in the browser. Asia, North America and Antarctica – 90 more waves, new monsters and bosses – are waiting in the app.</p><a class="fmStore" href="${url}" target="_blank" rel="noopener">${ru ? "GET IT ON RUSTORE ▶" : "GET IT ON GOOGLE PLAY ▶"}</a><button class="fmOk" data-a="later">Later</button></div></div>`;
  try { i18nApplyAll(); } catch (e) {} ov.hidden = false; try { snd("radio"); } catch (e) {} }
window.__gate = { show: gateShow, locked: webLocked, isApp, inRussia };
{ const _swW = startWave; startWave = function () { try { if (webLocked() && S && !S.nuts && !S.replay && !S.testRun && (S.wave | 0) + 1 > WEB_FREE_W) { S.waveCD = 3; const ov = document.getElementById("ovGate"); if ((!ov || ov.hidden) && performance.now() > gateQuiet) gateShow(); return; } } catch (e) {} return _swW.apply(this, arguments); }; }
'''
rep('})(); } catch (e) { console.error("v536 adm", e); }\n})();\n</script>', '})(); } catch (e) { console.error("v536 adm", e); }\n' + JS + '})();\n</script>')
# Karte: im Browser gesperrte Kontinente grau
rep('function contGrey(c) { if (c === "aus") return true; c = +c; if (c < 2) return false; if (FM.on) return !FM.open(c);',
    'function contGrey(c) { if (c === "aus") return true; c = +c; if (c < 2) return false; try { if (typeof webLocked === "function" && webLocked()) return true; } catch (e) {} if (FM.on) return !FM.open(c);')
css = "".join(re.findall(r'#ovFm[^{}]*\{[^}]*\}', s)).replace("#ovFm", "#ovGate")
rep('</head>', '<style id="v714gate">' + css + '#ovGate .fmStore{display:block;margin:4px 0 0;padding:12px 10px;background:#3fae3f;color:#fff;text-decoration:none;border:3px solid #3a2414;border-radius:14px;box-shadow:0 4px 0 #3a2414;font:400 22px/1 Bangers,Oswald,system-ui;letter-spacing:.05em;-webkit-text-stroke:.6px #1d4a1d}#ovGate .fmPic{height:190px}</style>\n</head>')
open(dst, "w", encoding="utf-8").write(s)
L = os.path.join(os.path.dirname(os.path.abspath(dst)), "lang")
ADD = {  # ru, es, pt, de
 "🔒 WORLD TOUR": ("🔒 КРУГОСВЕТКА", "🔒 VUELTA AL MUNDO", "🔒 VOLTA AO MUNDO", "🔒 WELTREISE"),
 "THE WORLD TOUR GOES ON IN THE APP": ("КРУГОСВЕТКА ПРОДОЛЖАЕТСЯ В ПРИЛОЖЕНИИ", "LA VUELTA AL MUNDO SIGUE EN LA APP", "A VOLTA AO MUNDO CONTINUA NO APP", "DIE WELTREISE GEHT IN DER APP WEITER"),
 "South America and Africa are free in the browser. Asia, North America and Antarctica – 90 more waves, new monsters and bosses – are waiting in the app.": (
   "Южная Америка и Африка в браузере бесплатны. Азия, Северная Америка и Антарктида – ещё 90 волн, новые монстры и боссы – ждут тебя в приложении.",
   "Sudamérica y África son gratis en el navegador. Asia, Norteamérica y la Antártida – 90 oleadas más, monstruos y jefes nuevos – te esperan en la app.",
   "América do Sul e África são grátis no navegador. Ásia, América do Norte e Antártida – mais 90 ondas, monstros e chefões novos – esperam por você no app.",
   "Südamerika und Afrika sind im Browser gratis. Asien, Nordamerika und die Antarktis – 90 weitere Wellen, neue Monster und Bosse – warten in der App."),
 "GET IT ON RUSTORE ▶": ("СКАЧАТЬ В RUSTORE ▶", "DESCÁRGALO EN RUSTORE ▶", "BAIXE NA RUSTORE ▶", "BEI RUSTORE LADEN ▶"),
 "GET IT ON GOOGLE PLAY ▶": ("СКАЧАТЬ В GOOGLE PLAY ▶", "DESCÁRGALO EN GOOGLE PLAY ▶", "BAIXE NO GOOGLE PLAY ▶", "BEI GOOGLE PLAY LADEN ▶"),
}
for i, l in enumerate(["ru", "es", "pt", "de"]):
    p = os.path.join(L, l + ".json"); d = json.load(open(p, encoding="utf8"))
    for k, v in ADD.items():
        if k not in d: d[k] = v[i]
    open(p, "w", encoding="utf8").write(json.dumps(d, ensure_ascii=False, indent=0) + "\n")
print("ok")
