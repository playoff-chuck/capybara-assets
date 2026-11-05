"""V271 (Martin 05.11. 15:28–15:33):
- Doppeldecker: Capybara sitzt im Flugzeug (Oberkörper nach unten verlängert, liegt hinter dem Rumpf) – kein Schweben mehr,
  wackelt weiter im Wind (img/biplane_cap2.webp).
- «Incoming»-Meldung in 7 Varianten (Incoming, Heads up, On the radar, Here they come, Contact, Eyes open, Brace for) und nur
  noch alle 2–3 Wellen.
- Tutorial: Schritt 5 «Hold the ring» bleibt 20 s stehen (mit «Good luck, squad!»), dann schließt das Tutorial.
- Waffen mit Anzeige (Kanone, Ten-ton, Mischer, Frost, Sniper, Chomper, Tesla, Lockdown): das alte «New gadget»-Fenster
  entfällt. Ten-ton: das Geschenk kommt in Welle 5 direkt als «Free gift»-Anzeige; alle anderen kommen als Sale-Anzeige,
  sobald bezahlbar (Abstandsregel)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V270";', 'const GAME_VER = "V271";')
rep('<img class="bpCap" src="img/biplane_cap.webp" alt="">', '<img class="bpCap" src="img/biplane_cap2.webp" alt="">')
rep('.biPlane .bpCap{left:43.08%;top:6.67%;width:28.46%;height:38.89%;transform-origin:50% 95%;', '.biPlane .bpCap{left:43.08%;top:6.67%;width:28.46%;height:48.89%;transform-origin:50% 80%;')
rep('if (!S.introNow) announce(`INCOMING: ${newest[2]}`, parts.join(" · "), "RADIO", 1600);',
    'if (!S.introNow && (!S.incNext || S.wave >= S.incNext)) { S.incNext = S.wave + 2 + Math.floor(Math.random() * 2); const IV = ["INCOMING", "HEADS UP", "ON THE RADAR", "HERE THEY COME", "CONTACT", "EYES OPEN", "BRACE FOR"]; announce(`${IV[Math.floor(Math.random() * IV.length)]}: ${newest[2]}`, parts.join(" · "), "RADIO", 1600); }')
# Alte Neuheiten-Fenster für Waffen mit Anzeige ersetzen
rep('showIntro = function (q) { const r = _si.apply(this, arguments);\n      try { if (q && q.t === "gear" && AD[q.k] && !S.nuts) {',
    '''showIntro = function (q) {
      if (q && q.t === "gear" && AD[q.k] && !S.nuts && !window.__newsPrev) { try {   // V271: Anzeige statt altem Fenster
          S.seen = S.seen || {}; S.seen["g:" + q.k] = true; S.introWave = S.wave; S.adDue = S.adDue || {};
          if (q.k === "ton") { if (!S.tonIntroGift) { S.tonIntroGift = true; S.tons = (S.tons || 0) + 1; } S.adDue.ton = 1; late = true; S.intro = true; S.adOpen = true; show("ton", false); }
          else S.adDue[q.k] = 1;
        } catch (e) { console.error("ad", e); } return; }
      const r = _si.apply(this, arguments);
      try { if (q && q.t === "gear" && AD[q.k] && !S.nuts) {''')
try:
    rep('try { if (typeof SAVE_KEYS !== "undefined") ["statNext", "statSeen",', 'try { if (typeof SAVE_KEYS !== "undefined") ["incNext", "statNext", "statSeen",')
except AssertionError: pass
open(dst, 'w', encoding='utf-8').write(s); print('ok')
# Nachtrag 15:35: Tutorial-Schritt 5 «Hold the ring» 20 s sichtbar, dann Ende mit «Good luck!»
s = open(dst, encoding='utf-8').read()
rep('{ t: "HOLD THE RING", s: "Monsters run the lane. Full laps cost lives. Clear rows for gold.", at: "board", done: () => S.kills >= 1 || (S.inWave && S.playT > 14) },',
    '{ t: "HOLD THE RING", s: "Monsters run the lane. Full laps cost lives. Clear rows for gold. Good luck, squad!", at: "board", done: () => TUT.t >= 20 },')
open(dst, 'w', encoding='utf-8').write(s); print('ok2')
