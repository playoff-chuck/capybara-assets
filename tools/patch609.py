#!/usr/bin/env python3
# V609 (Martin 11.11. 11:23/11:24): Einstellungen → «↺ Replay tutorial» für alle Spieler, ohne den Spielstand zu verlieren.
# Knopf sichert alle Spielstände (tarnturm-*/capy-* außer Geräte-/Admin-/Sprach-Schlüsseln) in capy-tutbak und startet das Tutorial.
# Nach dem Diplom (oder «Пропустить») wird neu geladen; ganz am Anfang des ersten Skripts wird die Sicherung zurückgeschrieben.
# Der alte Guide-Knopf (neues Spiel ab Welle 1) nutzt jetzt denselben sicheren Weg.
# Aufruf: patch609.py <site-Ordner>
import sys, json, os
site = sys.argv[1]
p = os.path.join(site, "index.html")
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V608";', 'const GAME_VER = "V609";')
KEEP = r"^(tarnturm-dev|tarnturm-terms|capy-adm|capy-uid|capy-cloud|capy-reset|capy-lang|capy-tutbak|capy-tutDone|capy-tutBack)$"
# 1) Rückschreiben ganz früh (vor dem capy-reset-Block)
rep('<script>try{if(localStorage.getItem("capy-reset")!=="276"){',
    '<script>try{if(localStorage.getItem("capy-tutDone")==="1"){var tb=localStorage.getItem("capy-tutbak");if(tb){var bk=JSON.parse(tb),dk=[];for(var di=0;di<localStorage.length;di++){var dkk=localStorage.key(di);if(dkk&&/^(tarnturm|capy)/.test(dkk)&&!/' + KEEP + '/.test(dkk))dk.push(dkk);}dk.forEach(function(k){localStorage.removeItem(k);});for(var bkk in bk)localStorage.setItem(bkk,bk[bkk]);localStorage.setItem("tarnturm-tut","1");localStorage.setItem("capy-tutBack","1");}localStorage.removeItem("capy-tutbak");localStorage.removeItem("capy-tutDone");}}catch(e){}   /* V609: Spielstand nach dem Tutorial zurück */\n'
    'try{if(localStorage.getItem("capy-reset")!=="276"){')
# 2) Knopf + Hinweis in den Einstellungen
rep('<button id="setFx" class="btn-small" type="button">EFFECTS: ON</button></div>',
    '<button id="setFx" class="btn-small" type="button">EFFECTS: ON</button></div><div class="setTut"><button id="setReTut" class="btn-small" type="button">↺ Replay tutorial</button><small>Your game stays saved. After the certificate you are back exactly where you left off.</small></div>')
rep('#ovSettings .setRow{flex-wrap:wrap}',
    '#ovSettings .setRow{flex-wrap:wrap} #ovSettings .setTut{display:flex;flex-direction:column;align-items:center;gap:4px;margin-top:8px} #ovSettings .setTut small{color:#c0392b;font-weight:700;font-size:12px;line-height:1.25;text-align:center;max-width:300px}')
# 3) Sicherer Start + alter Guide-Knopf umgeleitet
rep('// Guide: Tutorial wiederholen\nlet reTutArm = 0;',
    '''// V609: Tutorial wiederholen, Spielstand bleibt erhalten
function tutReplaySafe() { try { SFX.init(); snd("uiTap"); } catch (e) {}
  try { saveGame(); } catch (e) {}
  try { if (!localStorage.getItem("capy-tutbak")) { const bk = {}, keep = /''' + KEEP + '''/; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k && /^(tarnturm|capy)/.test(k) && !keep.test(k)) bk[k] = localStorage.getItem(k); } localStorage.setItem("capy-tutbak", JSON.stringify(bk)); } localStorage.removeItem("capy-tutDone"); }
  catch (e) { toast("Not enough space to save your game", "HQ", 2200); return; }
  LS.del("tarnturm-tut"); LS.del("tarnturm-save");
  for (const id of ["ovInfo", "ovPause", "ovSettings", "ovStart"]) { const o = $(id); if (o) o.hidden = true; }
  try { if (S && S.nuts) { LS.del("capy-nz-save"); NZ.frozen = null; window.__NZF = null; document.body.classList.remove("inNuts"); } } catch (e) {}
  try { tutAbort(); } catch (e) {} startGame(MODE); toast("TUTORIAL · your game is saved", "HQ", 2400); }
function tutBackHome() { try { if (!localStorage.getItem("capy-tutbak")) return false; localStorage.setItem("capy-tutDone", "1"); toast("WELCOME BACK · loading your saved game", "HQ", 1800); setTimeout(() => location.reload(), 1700); return true; } catch (e) { return false; } }
window.__tutBackHome = tutBackHome; window.__tutReplaySafe = tutReplaySafe;
$("setReTut").addEventListener("click", tutReplaySafe);
$("btnReTut").addEventListener("click", e => { e.stopImmediatePropagation(); tutReplaySafe(); }, true);
try { if (localStorage.getItem("capy-tutBack") === "1") { localStorage.removeItem("capy-tutBack"); setTimeout(() => { try { toast("WELCOME BACK · your game is restored", "HQ", 2400); } catch (e) {} }, 2500); } } catch (e) {}
// Guide: Tutorial wiederholen
let reTutArm = 0;''')
# 4) Zurück nach Diplom bzw. Überspringen
rep('function sumClose() { sumScore();', 'function sumClose() { try { if (window.__tutBackHome && window.__tutBackHome()) { sum.classList.remove("on"); window.__tutSumOpen = false; return; } } catch (e) {} sumScore();')
rep('LS.set("tarnturm-tut", "1"); if (!skipped) {', 'LS.set("tarnturm-tut", "1"); if (skipped) { try { window.__tutBackHome && window.__tutBackHome(); } catch (e) {} } if (!skipped) {')
open(p, "w", encoding="utf-8").write(s)

H = "Your game stays saved. After the certificate you are back exactly where you left off."
T = {
 "en": {H: H, "TUTORIAL · your game is saved": "TUTORIAL · your game is saved", "WELCOME BACK · loading your saved game": "WELCOME BACK · loading your saved game",
        "WELCOME BACK · your game is restored": "WELCOME BACK · your game is restored", "Not enough space to save your game": "Not enough space to save your game"},
 "ru": {H: "Твоя игра сохранится. После похвального листа вернёшься ровно туда, где остановился.", "TUTORIAL · your game is saved": "ОБУЧЕНИЕ · твоя игра сохранена",
        "WELCOME BACK · loading your saved game": "С ВОЗВРАЩЕНИЕМ · загружаем твою игру", "WELCOME BACK · your game is restored": "С ВОЗВРАЩЕНИЕМ · твоя игра на месте",
        "Not enough space to save your game": "Не хватает места, чтобы сохранить игру"},
 "de": {H: "Dein Spielstand bleibt gespeichert. Nach dem Diplom geht es genau dort weiter, wo du warst.", "TUTORIAL · your game is saved": "TUTORIAL · dein Spiel ist gespeichert",
        "WELCOME BACK · loading your saved game": "WILLKOMMEN ZURÜCK · dein Spiel lädt", "WELCOME BACK · your game is restored": "WILLKOMMEN ZURÜCK · dein Spiel ist zurück",
        "Not enough space to save your game": "Zu wenig Speicher für deinen Spielstand"},
 "es": {H: "Tu partida queda guardada. Tras el diploma vuelves justo donde lo dejaste.", "TUTORIAL · your game is saved": "TUTORIAL · tu partida está guardada",
        "WELCOME BACK · loading your saved game": "BIENVENIDO DE NUEVO · cargando tu partida", "WELCOME BACK · your game is restored": "BIENVENIDO DE NUEVO · tu partida ha vuelto",
        "Not enough space to save your game": "No hay espacio para guardar tu partida"},
 "pt": {H: "Seu jogo fica salvo. Depois do diploma você volta exatamente de onde parou.", "TUTORIAL · your game is saved": "TUTORIAL · seu jogo está salvo",
        "WELCOME BACK · loading your saved game": "BEM-VINDO DE VOLTA · carregando seu jogo", "WELCOME BACK · your game is restored": "BEM-VINDO DE VOLTA · seu jogo voltou",
        "Not enough space to save your game": "Sem espaço para salvar seu jogo"},
}
for l, m in T.items():
    q = os.path.join(site, "lang", l + ".json"); d = json.loads(open(q, encoding="utf-8").read()); d.update(m)
    open(q, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=0))
print("ok V609")
