#!/usr/bin/env python3
# V566 (Martin 10.11. 20:15): Abschlusskarte des Tutorials sieht aus wie ein russischer «Похвальный лист» (Schul-Urkunde):
# Papier mit Ornamentrahmen, Lorbeer, Stern, drei «Fächer» mit Note 5 (je Sprache die Bestnote), Unterschrift des Generals,
# roter Stempel. Belohnung +1000 Punkte: nach «ПРИНЯТЬ» zählt die Punkteanzeige oben hoch (S.bonusPts fließt in den Score).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V565";', 'const GAME_VER = "V566";')
rep('''function calcScore() { return Math.round(Math.max(0, S.wave) * S.lines * S.kills * speedMul() * (S.nuts ? 1 : 1 + Math.min(120, S.nutsBonus || 0) / 100)); }''',
    '''function calcScore() { return Math.round(Math.max(0, S.wave) * S.lines * S.kills * speedMul() * (S.nuts ? 1 : 1 + Math.min(120, S.nutsBonus || 0) / 100)) + (S.bonusPts | 0); }   /* V566: Bonuspunkte (Tutorial-Urkunde) */''')

LAUREL = '<svg class="ctLaur" viewBox="0 0 120 40" aria-hidden="true"><g fill="#6f8f3a" stroke="#3f5a1e" stroke-width="1"><path d="M58 36 Q32 34 8 14" fill="none" stroke="#3f5a1e" stroke-width="2"/><ellipse cx="14" cy="17" rx="7" ry="3" transform="rotate(-35 14 17)"/><ellipse cx="22" cy="24" rx="7" ry="3" transform="rotate(-25 22 24)"/><ellipse cx="31" cy="29" rx="7" ry="3" transform="rotate(-15 31 29)"/><ellipse cx="41" cy="33" rx="7" ry="3" transform="rotate(-8 41 33)"/><ellipse cx="18" cy="11" rx="6" ry="2.6" transform="rotate(-70 18 11)"/><ellipse cx="27" cy="18" rx="6" ry="2.6" transform="rotate(-60 27 18)"/><ellipse cx="37" cy="24" rx="6" ry="2.6" transform="rotate(-50 37 24)"/><path d="M62 36 Q88 34 112 14" fill="none" stroke="#3f5a1e" stroke-width="2"/><ellipse cx="106" cy="17" rx="7" ry="3" transform="rotate(35 106 17)"/><ellipse cx="98" cy="24" rx="7" ry="3" transform="rotate(25 98 24)"/><ellipse cx="89" cy="29" rx="7" ry="3" transform="rotate(15 89 29)"/><ellipse cx="79" cy="33" rx="7" ry="3" transform="rotate(8 79 33)"/><ellipse cx="102" cy="11" rx="6" ry="2.6" transform="rotate(70 102 11)"/><ellipse cx="93" cy="18" rx="6" ry="2.6" transform="rotate(60 93 18)"/><ellipse cx="83" cy="24" rx="6" ry="2.6" transform="rotate(50 83 24)"/></g><path d="M60 4 l3.5 7.2 7.9 1.1 -5.7 5.6 1.3 7.9 -7-3.7 -7 3.7 1.3-7.9 -5.7-5.6 7.9-1.1z" fill="#e8b520" stroke="#7a4a0a" stroke-width="1.4" stroke-linejoin="round"/></svg>'
ROW = lambda ic, t: f'<li><i>{ic}</i><span>{t}</span><b class="ctMark"><em>A+</em><small>excellent</small></b></li>'
CERT = ('<div class="tsCard cert"><div class="ctRib">CAPYBARA ACADEMY</div><img class="ctHero" alt="">' + LAUREL +
        '<h3>CERTIFICATE OF ACHIEVEMENT</h3><p class="ctSub">for excellent results in recruit training</p>'
        '<ul>' + ROW("🧱", "Blocks are your ground – full rows disappear and pay gold.") + ROW("🏰", "Towers shoot the monsters on the ring – each one that gets round costs a ♥ life.") + ROW("🎁", "Specials wait in the SHOP – tap USE.") + '</ul>'
        '<div class="ctFoot"><div class="ctSign"><em>Bristle</em><small>General Bristle</small></div><div class="ctStamp"><svg viewBox="0 0 100 92" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"><ellipse cx="27" cy="15" rx="9" ry="8"/><ellipse cx="73" cy="15" rx="9" ry="8"/><path d="M17 34 Q17 13 50 13 Q83 13 83 34 L85 60 Q85 86 50 88 Q15 86 15 60 Z"/><rect x="29" y="50" width="42" height="28" rx="14"/></g><g fill="currentColor"><circle cx="34" cy="37" r="4.2"/><circle cx="66" cy="37" r="4.2"/><ellipse cx="42" cy="61" rx="3.2" ry="2.4"/><ellipse cx="58" cy="61" rx="3.2" ry="2.4"/></g><path d="M44 70 Q50 74 56 70" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg><b>PASSED</b></div></div>'
        '<div class="ctPrize">+1000 POINTS</div><button type="button" disabled>ACCEPT</button></div>')
a = s.index("  sum.innerHTML = '<div class=\"tsCard\">"); b = s.index("\n", a)
s = s[:a] + "  sum.innerHTML = '" + CERT.replace("'", "\\'") + "';   /* V566: Похвальный лист */" + s[b:]
rep('try { sum.querySelector(".tsCard>img").src = HERO_IMG[heroKey()]; } catch (e) {}', 'try { sum.querySelector(".ctHero").src = HERO_IMG[heroKey()]; sum.querySelector(".cert").classList.toggle("us", (I18N.lang || "en") !== "ru"); const gr = { ru: "5", de: "1" }[I18N.lang] || "A+"; sum.querySelectorAll(".ctMark em").forEach(e => { e.textContent = gr; }); } catch (e) {}   /* V566: RU Похвальный лист, sonst US-High-School-Urkunde */')
rep('function sumClose() { sum.classList.remove("on");',
    '''function sumScore() { try { const goal = (S.bonusPts | 0) + 1000, st = Math.max(1, Math.round((goal - (S.bonusPts | 0)) / 40)); const el = document.getElementById("sScore"), pill = el && (el.closest(".score") || el.parentElement); if (pill) pill.classList.add("ctPop");
      let k = 0; const it = setInterval(() => { try { if (!S || !S.started) { clearInterval(it); return; } S.bonusPts = Math.min(goal, (S.bonusPts | 0) + st); checkScore(); hud(); if (k++ % 6 === 0) snd("sell"); if (S.bonusPts >= goal) { clearInterval(it); snd("powerup"); setTimeout(() => pill && pill.classList.remove("ctPop"), 600); } } catch (e) { clearInterval(it); } }, 35); } catch (e) {} }
  function sumClose() { sumScore(); sum.classList.remove("on");''')
CSS = r'''
<style id="v566cert">
#tutSum{z-index:9000!important}
#tutSum .tsCard.cert{width:min(92vw,360px);max-height:92vh;overflow:auto;padding:16px 14px 14px;border-radius:6px;border:0;background:#fbf3dc radial-gradient(ellipse at 50% 0%,#fffaf0 0%,#f6e8c4 70%,#efdcae 100%);box-shadow:0 0 0 3px #b8892a,0 0 0 6px #fbf3dc,0 0 0 8px #8a1f1f,0 14px 34px rgba(0,0,0,.5);text-align:center;color:#3a2414;font-family:Georgia,"Times New Roman","Noto Serif",serif}
#tutSum .cert::before{content:"";position:absolute;inset:7px;border:2px solid #b8892a;border-radius:3px;pointer-events:none;background:repeating-linear-gradient(45deg,transparent 0 6px,rgba(184,137,42,.10) 6px 7px) border-box;-webkit-mask:linear-gradient(#000 0 0) border-box,linear-gradient(#000 0 0) padding-box;-webkit-mask-composite:xor;mask-composite:exclude;padding:5px}
#tutSum .cert::after{content:"";position:absolute;inset:13px;border:1px solid rgba(138,31,31,.55);border-radius:2px;pointer-events:none}
#tutSum .ctRib{position:relative;z-index:1;display:inline-block;background:#b3261e;color:#ffe9a8;font:700 11px/1 Georgia,serif;letter-spacing:.18em;padding:6px 16px 5px;margin-top:4px;clip-path:polygon(0 0,100% 0,94% 50%,100% 100%,0 100%,6% 50%)}
#tutSum .tsCard>img.ctHero{position:relative;z-index:1;display:block;left:auto;top:auto;transform:none;filter:none;width:70px;height:70px;margin:8px auto -6px;border-radius:50%;object-fit:cover;object-position:50% 20%;background:#fff6dc;border:3px solid #b8892a;box-shadow:0 0 0 3px #fbf3dc,0 0 0 5px #8a1f1f}
#tutSum .ctLaur{position:relative;z-index:1;display:block;width:150px;height:44px;margin:-2px auto 0}
#tutSum .cert h3{position:relative;z-index:1;margin:2px 0 2px;font:700 25px/1.05 Georgia,"Times New Roman","Noto Serif",serif;letter-spacing:.05em;color:#8a1f1f;text-transform:uppercase;text-shadow:0 1px 0 #fff3cf}
#tutSum .ctSub{position:relative;z-index:1;margin:0 8px 10px;font:italic 400 14px/1.3 Georgia,"Times New Roman",serif;color:#5a3d22}
#tutSum .cert ul{position:relative;z-index:1;list-style:none;margin:0 6px 10px;padding:0;display:grid;gap:0;border-top:1.5px solid #b8892a}
#tutSum .cert li{display:flex;gap:8px;align-items:center;background:none;border:0;border-bottom:1px dashed #c9a35a;border-radius:0;padding:7px 2px}
#tutSum .cert li i{font-style:normal;font-size:20px}
#tutSum .cert li span{flex:1;text-align:left;font:400 13.5px/1.3 Georgia,"Times New Roman","Noto Serif",serif;color:#3a2414}
#tutSum .ctMark{flex:0 0 auto;display:grid;justify-items:center;width:58px}
#tutSum .ctMark em{display:grid;place-items:center;min-width:34px;height:34px;padding:0 4px;box-sizing:border-box;border:2px solid #c8161b;border-radius:50%;color:#c8161b;font:italic 700 18px/1 Georgia,serif;transform:rotate(-8deg)}
#tutSum .ctMark small{display:block;margin-top:2px;font:italic 400 10.5px/1 Georgia,serif;color:#c8161b;letter-spacing:0;background:none;border:0;padding:0}
#tutSum .ctFoot{position:relative;z-index:1;display:flex;align-items:center;justify-content:space-between;margin:2px 10px 8px}
#tutSum .ctSign{text-align:left}
#tutSum .ctSign em{display:block;font:italic 400 26px/1 "Brush Script MT","Segoe Script",cursive,Georgia;color:#1d3f8a;transform:rotate(-6deg);margin:0 0 -2px 6px}
#tutSum .ctSign small{display:block;border:0;border-top:1px solid #3a2414;padding:3px 0 0;font:400 11px/1 Georgia,serif;color:#5a3d22;background:none;letter-spacing:0;border-radius:0}
#tutSum .ctStamp{position:relative;width:84px;height:80px;color:rgba(31,79,184,.82);transform:rotate(-13deg);mix-blend-mode:multiply;filter:url(#none) contrast(1.05)}
#tutSum .ctStamp svg{position:absolute;inset:0;width:100%;height:100%}
#tutSum .ctStamp b{position:absolute;left:-6px;right:-6px;top:41%;transform:rotate(-4deg);display:block;text-align:center;font:700 12.5px/1 Georgia,"Times New Roman",serif;letter-spacing:.1em;color:currentColor;background:rgba(253,246,226,.7);border:2px solid currentColor;border-radius:3px;padding:3px 2px 2px}
#tutSum .ctPrize{position:relative;z-index:1;display:inline-block;margin:0 0 10px;background:linear-gradient(180deg,#ffe07a,#e8b520);border:2px solid #7a4a0a;border-radius:999px;padding:6px 18px 5px;font:700 16px/1 Georgia,serif;letter-spacing:.04em;color:#3a2414;box-shadow:0 3px 0 #7a4a0a}
#tutSum .cert button{position:relative;z-index:1;font:700 19px/1 Georgia,"Times New Roman",serif;letter-spacing:.08em;text-transform:uppercase;background:#2f7d32!important;color:#fff6dc!important;border:2px solid #1b4a1d;border-radius:8px;box-shadow:0 4px 0 #1b4a1d;padding:12px 8px 10px}
.ctPop{animation:ctPop .35s ease-in-out infinite alternate}
@keyframes ctPop{from{transform:scale(1);filter:none}to{transform:scale(1.12);filter:drop-shadow(0 0 8px #ffd23a)}}
#tutSum .cert.us{background:#fdfaf1 radial-gradient(ellipse at 50% 30%,#ffffff 0%,#f7f1df 75%,#ece2c4 100%);box-shadow:0 0 0 3px #c9a227,0 0 0 6px #fdfaf1,0 0 0 9px #1f3a6b,0 14px 34px rgba(0,0,0,.5)}
#tutSum .cert.us::before{border-color:#c9a227;background:repeating-linear-gradient(90deg,transparent 0 5px,rgba(31,58,107,.10) 5px 6px) border-box}
#tutSum .cert.us::after{border-color:rgba(31,58,107,.5)}
#tutSum .cert.us .ctRib{background:#1f3a6b;color:#f3d77a;clip-path:none;border-radius:2px;border-top:2px solid #c9a227;border-bottom:2px solid #c9a227}
#tutSum .cert.us>img.ctHero{border-color:#c9a227;box-shadow:0 0 0 3px #fdfaf1,0 0 0 5px #1f3a6b}
#tutSum .cert.us .ctLaur g{fill:#c9a227;stroke:#8a6a12}#tutSum .cert.us .ctLaur path[fill="none"]{stroke:#8a6a12}
#tutSum .cert.us h3{color:#1f3a6b;font:italic 700 26px/1.05 "Old English Text MT","UnifrakturMaguntia",Georgia,"Times New Roman",serif;letter-spacing:.02em;text-transform:none}
#tutSum .cert.us .ctSub{color:#3b4a66}
#tutSum .cert.us ul{border-top-color:#c9a227}#tutSum .cert.us li{border-bottom-color:#d6c48d}
#tutSum .cert.us .ctSign em{color:#1f3a6b}
#tutSum .cert.us button{background:#1f3a6b!important;border-color:#0f2142;box-shadow:0 4px 0 #0f2142}
@media (max-height:700px){#tutSum .tsCard>img.ctHero{width:50px;height:50px;margin-top:4px}#tutSum .ctLaur{height:30px;width:110px}#tutSum .ctSub{margin-bottom:6px}#tutSum .ctFoot{margin-bottom:4px}#tutSum .cert h3{font-size:21px}#tutSum .cert li{padding:5px 2px}#tutSum .cert li span{font-size:12.5px}#tutSum .ctStamp{width:68px;height:64px}}
</style>
'''
rep('<style id="v277arr">', CSS + '<style id="v277arr">')
# Martin 20:17: Testlink ?test=cert – nach 5 s kommt die Urkunde
rep('const map = { shock: 9, ton: 9,', 'const map = { cert: 1, shock: 9, ton: 9,')
rep('if (q === "ton") { S.tons = (S.tons || 0) + 2;', 'if (q === "cert") { const w8 = () => { try { if (!S || !S.started || S.intro || document.body.classList.contains("mapUp") || uiWinOpen()) { setTimeout(w8, 500); return; } setTimeout(() => { try { window.__certNow(); } catch (e) {} }, 5000); } catch (e) {} }; setTimeout(w8, 800); }   /* V566 */ if (q === "ton") { S.tons = (S.tons || 0) + 2;')
rep("""    window.__tutSumPend = 0; window.__tutSumOpen = true; S.coachHold = true;""",
    """    window.__certNow();
  } catch (e) {} }, 400);
  window.__certNow = () => { window.__tutSumPend = 0; window.__tutSumOpen = true; S.coachHold = true;""")
rep("""    sum.hidden = false; requestAnimationFrame(() => sum.classList.add("on")); try { snd("powerup"); } catch (e) {}
  } catch (e) {} }, 400);""", """    sum.hidden = false; requestAnimationFrame(() => sum.classList.add("on")); try { snd("powerup"); } catch (e) {} };""")

open(dst, "w", encoding="utf-8").write(s)
print("ok")
