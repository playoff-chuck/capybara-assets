"""sim13: sim12 mit LINEAREM Anstieg (V482): Anzahl 11→65, Grunt-HP 15,6→1320,8, Tempo 1,28→1,67, Anführer ab W6 jedes 6., ab W57 jedes 5. + Blöcke linear 0,87→0,61 s/Zeile. Basis sim12: sim10 + Anführer (V463) + HPF/WEEDLOSS per Umgebung. Capybara Squad – Simulation v10 (08.11.2026, Stand V457) – Spielertypen «Wie Martin» und «Etwas schlechter» (martin-).
Neu gegenüber sim9: Unkraut (V438) = Game over, wenn es nicht geschnitten wird (Wahrscheinlichkeit je Spielertyp); Mehr-Samen-Wellen W106/126/131 mit Gratis-Ten-ton (V446);
Elite-Laserturm W6/56/106 (V444) senkt in seiner Welle den Monsterdruck (−30 % Leben-Verlust). Ansonsten wie sim9 (Stand V361).
Aufruf: python3 sim10.py n hk_res.json out.jsonl seed [typ=martin|martin-]
Basis sim8 (Kampf-, Kauf- und Steinmodell) + Live-Werte V361:
- ab W21 bis W150: Monster-HP x0,4, Tempo x0,65, Anzahl x0,55; Steine fallen 1,8x langsamer; zusätzlich ab W30 /0,9, ab W50 /0,93, W91–120 /0,92
- HP-Stufen: ab W20 x1,15, ab W50 x1,25; W91–110 x0,75, W111–120 x0,85, W121–150 x0,90
- Air Drops: Wellen-Gold (20+5W), Ten-ton-Geschenke W5 (Vorstellung) + W8/14/22, Clean Sweep (100+15W Gold + Medaille)
- Boss-Hack an den echten Angebotswellen (HK_WAVES), Einsatz, Boss-Topf je Einsatz/Welle, Gewinnquote aus hk_sim.py (Nachbau des Duells)
- Dieb W100/110/119/130/140/149 (halbes Gold), Easter Egg +1000 Gold je Kontinent, Kontinentwechsel: Türme voll erstattet, Feld leer
- Störungen (Bildausfall, Magnet, Unkraut) und Sonderwellen erhöhen das Steinrisiko in ihrer Welle
Aufruf: python3 sim9.py n hk_res.json out.json"""
import json, sys, random, statistics as st
from collections import Counter, defaultdict
sys.path.insert(0, ".")
import sim8 as S8
from functools import lru_cache
_ws, _uc = S8.wstat, S8.upc
_G = {}
@lru_cache(maxsize=None)
def _wsc(t, l): return _ws(_G["G"], t, l)
@lru_cache(maxsize=None)
def _ucc(t, l): return _uc(_G["G"], t, l)
S8.wstat = lambda G, t, l: _wsc(t, l)
S8.upc = lambda G, t, l: _ucc(t, l)
TOWER, MAXW = 50, 150
HK_WAVES = {8, 12, 18, 22, 28, 32, 38, 42, 48, 52, 58, 62, 68, 72, 78, 82, 88, 92, 98, 102, 107, 112, 117, 121, 127, 132, 138, 142, 148}
HK_LOW = 175
THIEF = {100, 110, 119, 130, 140, 149}
BLK = {w for w in range(65, 151) if (w - 65) % 18 == 0}
MAG = {80, 92, 105, 117}
WEED = {81}            # einzelne Unkräuter (V426)
WEED_N = {106: 3, 126: 4, 136: 5}   # V426/V446: mehrere Samen am Ortsanfang, davor Gratis-Ten-ton
ELITE = {6, 56, 106}
SPEC = {15, 55, 69, 81, 95, 23, 57, 71, 83, 97, 37, 59, 73, 85, 41, 45, 61, 75, 89, 99, 35, 51, 67, 79, 93, 47, 65, 77, 87}
SPEC = SPEC | {w + 100 for w in SPEC if w + 100 <= 150}
CONT = {31, 61, 91, 121}
# Annahmen zum Verhalten «Wie Martin» (keine echten Daten auf dem Server)
A = dict(hkTake=0.9, hkStake=(0.25, 0.5), thiefStop=0.5, eggFind=0.6, pdDist=0.02, pdSpec=0.01, weedCut=0.95, weedCutN=0.90)
TYPES = {"martin": dict(), "martin-": dict(e=(0.54, 0.07), lim=(0.49, 0.05), lines=3.0, linegold=55, spend=0.80, splat=0.7, speed=[(1, .93), (1.5, .07)], thiefStop=0.35, eggFind=0.45, weedCut=0.88, weedCutN=0.80, hkTake=0.9)}
PTYPE = "martin"

import os
HPF = json.loads(os.environ.get("HPF", "[[30,0.7],[60,0.6],[90,0.55],[120,0.7],[150,0.4]]"))
WEEDLOSS = int(os.environ.get("WEEDLOSS", "3"))

LIN = {"n": (11, 65), "hp": (15.6, 1320.8), "sp": (1.28, 1.67)}
def lin(k, w): a, b = LIN[k]; return a + (b - a) * (max(1, min(150, w)) - 1) / 149
def basehp(G, w): return G["hpBase"] * (1 + G.get("hpLin", 0) * (w - 1)) * G["hpGrow"] ** (w - 1)
def leadf(w, hp=True):   # Anführer: jedes 6. (W6–56) / 5. (ab W57) Monster, +60 % HP, +25 % Tempo
    if w < 6: return 1
    k = 6 if w <= 56 else 5
    return 1 + (0.6 if hp else 0.25) / k
def hpmul_lin(G, w): return lin("hp", w) / basehp(G, w) * leadf(w, True) * (0.75 if ((w - 1) % 30 < 3 and w > 30) else 1)   # V485 Anlaufpolster
def spmul_lin(G, w): return lin("sp", w) / min(G["spMax"], G["spBase"] + G["spGrow"] * w) * leadf(w, False)
def hpmul(w):
    m = 1.25 if w >= 50 else 1.15 if w >= 20 else 1
    m *= 0.75 if 91 <= w <= 110 else 0.85 if 111 <= w <= 120 else 0.90 if 121 <= w <= 150 else 1
    f = 1
    for hi, v in HPF:
        if w <= hi: f = v; break
    lead = 1.12 if 6 <= w <= 40 else 1   # V463 Anführer (jedes 6. Monster +60 % HP, +25 % Tempo) ≈ +12 %
    return m * lead * (f if 21 <= w <= 150 else 1)

def grav(G, w, lines):
    return 0.87 + (0.61 - 0.87) * (max(1, min(150, w)) - 1) / 149   # V483: Blöcke linear
    g = S8.grav(G, w, lines)
    if w <= 4: g *= 1.1   # V456   # enthält die alten Teiler (W30/40/50/60)
    if 21 <= w <= 150: g *= 1.8
    g /= (0.9 if w >= 30 else 1) * (0.93 if w >= 50 else 1) * (0.92 if 91 <= w <= 120 else 1)
    return g

def boss_pool(stake, w):
    if w >= 25: return ["M", "L", "XL"] if stake <= 2 * HK_LOW else ["L", "XL"]
    return ["S", "M", "L"] if stake <= HK_LOW else ["M", "L", "XL"]

def tower_value(G, towers):
    v = 0
    for tw in towers:
        v += TOWER
        for t, l in tw:
            v += G["weap"][t]["cost"] + sum(S8.upc(G, t, k) for k in range(1, l))
    return v

def run(G, HK, rnd, log):
    Sk = dict(S8.SK["martin"]); Sk.update({k: v for k, v in TYPES[PTYPE].items() if k in Sk}); e = max(0.15, rnd.gauss(*Sk["e"])); lim = max(0.12, rnd.gauss(*Sk["lim"])); spd = S8.pick(rnd, Sk["speed"])
    gold, lives, medals, mprog, lines, spawned, cardm, tons = G["startGold"], G["lives"], 0, 0, 0, 0, 1.0, 0
    towers = []; unl = G["unlock"]; cash = Counter(); goldAt = {}; eggs = set()
    for w in range(1, MAXW + 1):
        if w in CONT:   # V355: Türme voll erstattet, Feld leer
            v = tower_value(G, towers); gold += v; cash["refund"] += v; towers = []
        if w == unl.get("ton", 99): tons += 1; cash["gifts"] += 1
        tier = (w - 1) // 3
        N = int(round(lin("n", w)))   # V482 linear
        tp = S8.taper(w)
        g0 = gold; gold = S8.buy(G, Sk, w, gold, towers, unl); cash["spent"] += g0 - gold

        leaks, inc = S8.fight(G, Sk, w, N, spawned, towers, medals, e, cardm, hpmul_lin(G, w), spmul_lin(G, w)); spawned += N
        inc *= G["goldMul"] * tp; gold += inc; cash["kills"] += inc
        if w in ELITE and leaks: leaks = int(leaks * 0.7)   # V444: Elite-Laser 60 s
        lives -= leaks; medals = max(0, medals - leaks)
        if leaks: mprog = 0
        mprog += sum(1 for _ in range(4) if rnd.random() < Sk["splat"] / 4)
        while mprog >= 4 and medals < 4: mprog -= 4; medals += 1
        lines += Sk["lines"]
        wg = (20 + 5 * w) * G["goldMul"] * tp; lg = Sk["linegold"] * G["goldMul"] * tp
        gold += wg + lg; cash["waveGold"] += wg; cash["lines"] += lg
        if rnd.random() < Sk["sweep"]: sw = 100 + 15 * w; gold += sw; cash["sweep"] += sw; medals = min(4, medals + 1)
        if w % 20 == 0: cardm = Sk["card"]
        if w in (8, 14, 22): tons += 1; cash["gifts"] += 1
        c = (w - 1) // 30
        if c not in eggs and w % 30 == 10 and rnd.random() < A["eggFind"]: eggs.add(c); gold += 1000; cash["egg"] += 1000
        if w in WEED or w in WEED_N:   # V438: Unkraut nicht geschnitten -> Game over
            if w in WEED_N: tons += 1
            wc = (A["weedCutN"] if w in WEED_N else A["weedCut"]) - (0.05 if w in (126, 136) else 0)   # V482: +30 % Wachstum -> etwas seltener geschnitten
            if rnd.random() >= wc: lives -= WEEDLOSS; cash["weedhit"] = cash.get("weedhit", 0) + 1
            if lives <= 0: return dict(w=w, why="weed", cash=cash, goldAt=goldAt, lives=lives)
        if w in THIEF:
            stolen = gold // 2
            if rnd.random() >= A["thiefStop"]: gold -= stolen; cash["thief"] -= stolen; log["thief"].append(stolen)
        if w in HK_WAVES and w < 150 and gold >= 10 and rnd.random() < A["hkTake"]:
            stake = max(10, int(gold * rnd.uniform(*A["hkStake"]) // 10 * 10)); boss = rnd.choice(boss_pool(stake, w))
            win = rnd.random() < HK[boss]
            gold += stake if win else -stake; cash["hack"] += stake if win else -stake
            log["hk"].append((w, stake, boss, win))
        if towers and rnd.random() < 0.02 * len(towers) * (1.2 - e): towers.pop(rnd.randrange(len(towers)))
        goldAt[w] = gold
        if lives <= 0: return dict(w=w, why="monsters", cash=cash, goldAt=goldAt, lives=lives)
        g = grav(G, w, lines) / spd
        pd = 0.002 if g >= lim else min(0.5, 0.04 + 2.0 * (lim - g) / lim)
        if w in BLK or w in MAG or w in WEED: pd += A["pdDist"]
        if w in SPEC: pd += A["pdSpec"]
        if rnd.random() < pd:
            if tons > 0: tons -= 1
            else: return dict(w=w, why="blocks", cash=cash, goldAt=goldAt, lives=lives)
    return dict(w=MAXW, why="finished", cash=cash, goldAt=goldAt, lives=lives)

if __name__ == "__main__":
    # Aufruf: sim9.py n hk_res.json out.jsonl seed [hkTake]
    n = int(sys.argv[1]); HK = json.load(open(sys.argv[2]))["martin"]; out = sys.argv[3]; seed = int(sys.argv[4])
    if len(sys.argv) > 5: PTYPE = sys.argv[5]
    for k, v in TYPES[PTYPE].items():
        if k in A: A[k] = v
    G = json.load(open("G_V361.json")); _G["G"] = G; rnd = random.Random(seed)
    with open(out, "w") as f:
        for i in range(n):
            log = defaultdict(list); r = run(G, HK, rnd, log)
            ga = {w: round(r["goldAt"][w]) for w in r["goldAt"] if w % 5 == 0 or w == r["w"]}
            f.write(json.dumps(dict(w=r["w"], why=r["why"], cash={k: round(v) for k, v in r["cash"].items()}, ga=ga, hk=log["hk"], th=log["thief"], lv=r["lives"])) + "\n")
