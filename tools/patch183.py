s=open('v182.html',encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(n,a[:70]); s=s.replace(a,b)
# Blöcke: ab W30 -10 %, ab W50 nochmals -7 %, W91-120 -8 % (Martin 04.11.)
rep('* ordv("gravMul") / (S.wave >= 60 ? 0.7716 : S.wave >= 50 ? 0.857375 : S.wave >= 40 ? 0.9025 : S.wave >= 30 ? 0.95 : 1);',
    '* ordv("gravMul") / (S.wave >= 60 ? 0.7716 : S.wave >= 50 ? 0.857375 : S.wave >= 40 ? 0.9025 : S.wave >= 30 ? 0.95 : 1) / ((S.wave >= 30 ? 0.9 : 1) * (S.wave >= 50 ? 0.93 : 1) * (S.wave >= 91 && S.wave <= 120 ? 0.92 : 1));   /* V183: ab W30 −10 %, ab W50 −7 %, W91–120 −8 % */')
# Monster-HP: Rabatt läuft aus (W101-110 x0,85, W111-120 x0,95)
rep('(!S.nuts && w >= 91 && w <= 100 ? 0.75 : 1)','(S.nuts ? 1 : w >= 91 && w <= 100 ? 0.75 : w >= 101 && w <= 110 ? 0.85 : w >= 111 && w <= 120 ? 0.95 : 1)')
# Nuts: HP wie Welle 12, +9 %/Level; Tempo -10 %; Blöcke -10 % (Zone 3 zusätzlich 15 %); 10 % weniger Monster
rep('function nutsGrav(l) { return 0.85 * Math.pow(0.955, l); }','/* V183 (Martin 04.11., simuliert): Monster starten wie Welle 12 (+9 %/Level), 10 % langsamer, 10 % weniger; Blöcke 10 % langsamer, Zone 3 zusätzlich 15 % */\nfunction nzHpW(w) { return (1 + (G.hpLin || 0) * (w - 1)) * Math.pow(G.hpGrow, w - 1) * (w >= 50 ? 1.25 : w >= 20 ? 1.15 : 1); }\nfunction nutsGrav(l) { const z = S && S.nuts ? S.nuts.c : 0; return (z === 2 ? 1.15 : 1) / 0.9 * Math.pow(0.96, l); }')
rep('function nutsHp(l) { return 1.3 * Math.pow(1.09, l); }','function nutsHp(l) { const b = S && S.nuts ? S.nuts.base : 30; return nzHpW(12) / nzHpW(b) * Math.pow(1.09, l); }')
rep('function nutsSpd(l) { return 1.05 + 0.015 * l; }','function nutsSpd(l) { return 0.9 * (1.05 + 0.015 * l); }')
rep('function nutsCount(l) { return 6 + 2 * l; }','function nutsCount(l) { return Math.max(3, Math.round(0.9 * (6 + 2 * l))); }')
rep('S.wave = NZ_BASES[c]; S.gold = NZ_KIT.gold; S.lives = NZ_KIT.lives;','S.wave = NZ_BASES[c]; S.gold = NZ_KIT.gold + NZ_KIT.towerGold; S.lives = NZ_KIT.lives; S.snipes = 2; S.mixers = 2; S.teslas = 2; S.chomps = 2; S.tons = 2; S.locks = 2;   /* V183: Grundausstattung – von jedem Special 2 Stück, dazu Gold für 2 voll ausgebaute Türme */')
rep('const NZ_KIT = { gold: 600, lives: 5 };','const NZ_KIT = { gold: 600, towerGold: 1000, lives: 5 };')
rep('setTimeout(() => toast(NZ.first ? "FIRST TRY COUNTS · +1 % MAIN SCORE PER LEVEL" : "REPLAY · NUTS BOARD & MEDALS ONLY", "HQ", 2600), 3200);','setTimeout(() => toast(NZ.first ? "FIRST TRY COUNTS · +1 % MAIN SCORE PER LEVEL" : "REPLAY · NUTS BOARD & MEDALS ONLY", "HQ", 2600), 3200); setTimeout(() => toast("SQUAD KIT · 2× every special · +1000 gold for towers", "ARMORY", 2600), 6200);')
rep('ver: "V182", wave: S.wave','ver: "V183", wave: S.wave')
open('v183.html','w',encoding='utf-8').write(s); print('ok')
