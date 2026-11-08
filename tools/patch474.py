#!/usr/bin/env python3
"""V474 – Daily Drop: 7-Tage-Kette mit großzügigen XP + etwas Gold statt täglichem Special (Frage B, Martin 08.11. 20:12 «ja»).
Tag 1–7: 200/300/400/500/600/800/1000 XP sofort fürs Squad Level, 100/150/200/250/300/400/500 Gold zu Beginn des nächsten Laufs;
Tag 7 zusätzlich ein Ten-ton. Schutztag bleibt. Nutzung: python3 tools/patch474.py src dst"""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

m = re.search(r'const GAME_VER = "V(\d+)";', s); v = int(m.group(1))
rep(m.group(0), f'const GAME_VER = "V{v + 1}";')

# Kette
rep('const DAILY_DROP_W = 10, DAILY_MSN_W = 20, DAILY_XP = 300;',
    'const DAILY_DROP_W = 10, DAILY_MSN_W = 20, DAILY_XP = 300;\n'
    'const DAILY_CHAIN = [[200, 100], [300, 150], [400, 200], [500, 250], [600, 300], [800, 400], [1000, 500]];   /* V474: [XP sofort, Gold im nächsten Lauf] je Tag; Tag 7 + Ten-ton */\n'
    'function dailyRew(day) { const c = DAILY_CHAIN[Math.max(0, Math.min(6, (day || dailyDay()) - 1))]; return { xp: c[0], gold: c[1], ton: (day || dailyDay()) === 7 }; }')

# Claim: XP sofort, Gold (+ Ten-ton) für den nächsten Lauf
rep('function dailyClaim() { if (!dailyGate() || DAILY.claimed) return false; const d = dailyDrop(); DAILY.claimed = true; DAILY.pend = d[2]; DAILY.pendName = d[1]; dailySave(); return d; }',
    'function dailyClaim() { if (!dailyGate() || DAILY.claimed) return false; const d = dailyDrop(), r = dailyRew(); DAILY.claimed = true; DAILY.pendGold = r.gold; DAILY.pend = r.ton ? "tons" : null; DAILY.pendName = r.ton ? "Ten-ton drop" : null;\n'
    '  try { MSN.xp = (MSN.xp || 0) + r.xp; msnSave(); } catch (e) {} dailySave(); return d; }   /* V474 */')
rep('function dailyGrant() { try { if (!DAILY.pend || !S || !S.started || S.testRun || S.nuts || S.replay) return; const f = DAILY.pend, nm = DAILY.pendName || "Daily drop"; S[f] = (S[f] || 0) + 1; DAILY.pend = null; DAILY.pendName = null; dailySave(); setTimeout(() => { try { toast(`DAILY DROP · ${nm.toUpperCase()} in your Pocket`, "SUPPLY", 2600); } catch (e) {} }, 4000); } catch (e) {} }',
    'function dailyGrant() { try { if ((!DAILY.pend && !DAILY.pendGold) || !S || !S.started || S.testRun || S.nuts || S.replay) return; const f = DAILY.pend, nm = DAILY.pendName || "Daily drop", g = +DAILY.pendGold || 0;\n'
    '  if (f) S[f] = (S[f] || 0) + 1; if (g > 0) S.gold = (S.gold || 0) + g; DAILY.pend = null; DAILY.pendName = null; DAILY.pendGold = 0; dailySave();\n'
    '  setTimeout(() => { try { toast(f ? `DAILY DROP · +${g} gold · ${nm.toUpperCase()} in your Pocket` : `DAILY DROP · +${g} gold`, "SUPPLY", 2600); } catch (e) {} }, 4000); } catch (e) {} }   /* V474: Gold + Tag-7-Ten-ton */')

# Kalenderblatt
rep('    + `<div class="rew${DAILY.claimed ? " got" : ""}"><img src="${(typeof ICO_SPR !== "undefined" && ICO_SPR[d[0]]) || ""}" alt="">${DAILY.claimed ? `${d[1]}<br>${DAILY.pend ? "in your next run" : "collected"}` : `${d[1]}<br>Daily Drop · tap`}</div>`',
    '    + (() => { const r = dailyRew(day), ico = r.ton ? `<img src="${(typeof ICO_SPR !== "undefined" && ICO_SPR.ton) || ""}" alt="">` : `<b class="dlCoin">★</b>`;   /* V474 */\n'
    '        return `<div class="rew${DAILY.claimed ? " got" : ""}">${ico}<span>${DAILY.claimed ? `+${r.gold} gold<br>${DAILY.pend || DAILY.pendGold ? "in your next run" : "collected"}` : `+${r.xp} XP${r.ton ? " · Ten-ton" : ""}<br>+${r.gold} gold · tap`}</span></div>`; })()')
# Karte
rep('    <div class="dlSec">DAILY DROP</div><div class="dlRow"><img src="${(typeof ICO_SPR !== "undefined" && ICO_SPR[d[0]]) || ""}" alt=""><div><b>${d[1]}</b><span>${day === 7 ? "Day-7 bonus · the big one" : "Lands in your Pocket at the start of your next run"}</span></div>',
    '    <div class="dlSec">DAILY DROP</div><div class="dlRow">${(r => r.ton ? `<img src="${(typeof ICO_SPR !== "undefined" && ICO_SPR.ton) || ""}" alt="">` : `<div class="dlBig">★</div>`)(dailyRew(day))}<div><b>+${dailyRew(day).xp} XP · +${dailyRew(day).gold} gold</b><span>${day === 7 ? "Day-7 bonus · plus a Ten-ton drop" : "XP now · gold at the start of your next run"}</span></div>')
rep('`<i class="${i < day ? "on" : i === day ? "now" : ""}">${i}<small>${DAILY_DROPS[i - 1][1].split(" ")[0]}</small></i>`',
    '`<i class="${i < day ? "on" : i === day ? "now" : ""}">${i}<small>${i === 7 ? "Ten-ton" : "+" + DAILY_CHAIN[i - 1][0] + " XP"}</small></i>`')
rep('<div class="dlNote">Play on 7 days in a row for the Ten-ton. Miss one day a week – the shield keeps your chain.</div>',
    '<div class="dlNote">XP count right away, gold lands in your next run. Play on 7 days in a row for the Ten-ton. Miss one day a week – the shield keeps your chain.</div>')
# Stern-Icon im Blatt
rep('/* V469 (t136): Blatt darf den CONTINUE/PLAY-Knopf nie verdecken',
    '{ const st = document.createElement("style"); st.textContent = "#dailyLeaf .rew .dlCoin{display:inline-block;width:26px;height:26px;line-height:26px;text-align:center;border-radius:50%;background:#ffd34a;color:#7a4b00;font-family:Bangers,system-ui;font-size:18px;flex:0 0 auto}"; document.head.appendChild(st); }   /* V474 */\n'
    '/* V469 (t136): Blatt darf den CONTINUE/PLAY-Knopf nie verdecken')
open(dst, "w", encoding="utf-8").write(s); print("ok", v + 1)
