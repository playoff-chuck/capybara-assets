import sys
# V722: Teilen-/Challenge-Bilder in allen Sprachen sauber (Martin 15.11.2026 20:06, Lenas Bild RU):
#  «ПОБЕЙ МОЙ РЕКОРД!» lief rechts aus dem Bild, «ИГРАТЬ БЕСПЛАТНО ▶» ragte über die rosa Taste.
#  Jetzt passen Aufruf und Tastentext sich der Breite an (shFit, misst die übersetzte Fassung). Einladungsbild ebenso.
#  Der Begleittext beim Teilen wird jetzt in der Spielsprache gesendet (vorher immer Englisch).
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V721";', 'const GAME_VER = "V722";')
rep('g.textAlign = "center"; g.font = "78px Bangers"; g.lineWidth = 12; g.strokeStyle = "#3a2414"; g.strokeText(I.call, bx + bw2 / 2, 1050);',
    'g.textAlign = "center"; shFit(g, I.call, "#px Bangers", 78, bw2 + 10); g.lineWidth = 12; g.strokeStyle = "#3a2414"; g.strokeText(I.call, bx + bw2 / 2, 1050);')
rep('g.fillStyle = "#fff"; g.font = "70px Bangers"; g.fillText("PLAY FREE ▶", bx + bw2 / 2, 1160);',
    'g.fillStyle = "#fff"; shFit(g, "PLAY FREE ▶", "#px Bangers", 70, bw2 - 56); g.fillText("PLAY FREE ▶", bx + bw2 / 2, 1160);')
rep('g.fillStyle = "#fff"; g.font = "64px Bangers"; g.fillText("PLAY FREE ▶", cx, 1204);',
    'g.fillStyle = "#fff"; shFit(g, "PLAY FREE ▶", "#px Bangers", 64, bw2 - 56); g.fillText("PLAY FREE ▶", cx, 1204);')
rep('await navigator.share({ files: [file], title: "Capybara Squad", text: I.text });', 'await navigator.share({ files: [file], title: "Capybara Squad", text: shText(I) });')
rep('else if (navigator.share) await navigator.share({ title: "Capybara Squad", text: I.text, url: SHARE_URL });', 'else if (navigator.share) await navigator.share({ title: "Capybara Squad", text: shText(I), url: SHARE_URL });')
rep('call: "CAN YOU GET 5 STARS?", text: `I cleared ${P.place} with ${o.n || 0}/5 stars in Capybara Squad! Can you beat it? ${chUrl("st", o.n || 1, o.g)}` }; }',
    'call: "CAN YOU GET 5 STARS?", text: `I cleared ${P.place} with ${o.n || 0}/5 stars in Capybara Squad! Can you beat it? ${chUrl("st", o.n || 1, o.g)}`, tpl: "I cleared # with #/# stars in Capybara Squad! Can you beat it? #", args: [T(P.place), o.n || 0, 5, chUrl("st", o.n || 1, o.g)] }; }')
rep('text: win ? `I beat all 150 waves of Capybara Squad with ${sc.toLocaleString("en-US")} points! Can you beat me? ${chUrl("sc", sc)}` : `I reached wave ${w} (${P.place}) in Capybara Squad with ${sc.toLocaleString("en-US")} points! Can you beat me? ${chUrl("sc", sc)}` };',
    'text: win ? `I beat all 150 waves of Capybara Squad with ${sc.toLocaleString("en-US")} points! Can you beat me? ${chUrl("sc", sc)}` : `I reached wave ${w} (${P.place}) in Capybara Squad with ${sc.toLocaleString("en-US")} points! Can you beat me? ${chUrl("sc", sc)}`,\n    tpl: win ? "I beat all # waves of Capybara Squad with # points! Can you beat me? #" : "I reached wave # (#) in Capybara Squad with # points! Can you beat me? #", args: win ? [150, sc.toLocaleString("en-US"), chUrl("sc", sc)] : [w, T(P.place), sc.toLocaleString("en-US"), chUrl("sc", sc)] };')
rep('async function shareCard(o) {', 'function shText(I) { try { if (I.tpl) { let t = T(I.tpl); if (t && t !== I.tpl && (t.match(/#/g) || []).length === I.args.length) { I.args.forEach(a => { t = t.replace("#", String(a)); }); return t; } } } catch (e) {} return I.text; }   /* V722 */\nwindow.__shText = o => shText(shInfo(o));\nasync function shareCard(o) {')
rep('try { await Promise.all([document.fonts.load("100px Bangers"), document.fonts.load(\'800 40px "Baloo 2"\')]); } catch (e) {}',
    'try { await Promise.all([document.fonts.load("100px Bangers", "AБЯ"), document.fonts.load(\'800 40px "Baloo 2"\', "AБЯ"), document.fonts.load(\'800 40px "Baloo 2"\')]); } catch (e) {}   /* V722: auch kyrillische Schrift laden */', 2)
open(dst, "w", encoding="utf-8").write(s)
import subprocess, os
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang722.py"), os.path.join(os.path.dirname(os.path.abspath(dst)), "lang")], check=True)
