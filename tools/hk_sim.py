"""Boss-Hack-Duell als Simulation (Nachbau von hkGenSide/hkOutputs/hkResolve/hkBossThink aus index.html V361).
Spieler-Modell: gleiche Entscheidungslogik wie der Boss, aber mit eigenen Werten (Kapseln 5).
Aufruf: python3 hk_sim.py [n]  → JSON mit Gewinnquoten je Boss-Typ und Spielertyp."""
import random, json, sys
ROWS, TIME, PULSE, DT = 12, 10.0, 3.0, 1 / 30
BOSS_T = {
    "S": dict(caps=4, noise=2.2, cd=(1.1, 0.9), rush=1.2, rushCD=0.9, save=0),
    "M": dict(caps=4, noise=1.4, cd=(0.9, 0.7), rush=2.0, rushCD=0.6, save=1),
    "L": dict(caps=5, noise=0.9, cd=(0.75, 0.55), rush=2.6, rushCD=0.4, save=1),
    "XL": dict(caps=6, noise=0.5, cd=(0.6, 0.45), rush=3.0, rushCD=0.25, save=2)}
# Spielertypen: wie gut sie die Seite wählen und wann/wie überlegt sie feuern
PLAYERS = {
    "schwach": dict(caps=5, noise=2.0, cd=(1.1, 0.9), rush=1.5, rushCD=0.8, save=0, pick=0.5),
    "martin": dict(caps=5, noise=1.1, cd=(0.85, 0.6), rush=2.4, rushCD=0.45, save=1, pick=0.7),
    "stark": dict(caps=5, noise=0.6, cd=(0.7, 0.5), rush=2.8, rushCD=0.3, save=2, pick=0.85)}

def gen_side(rnd):
    rows, r = [None] * ROWS, 0
    while r < ROWS:
        x, two = rnd.random(), r < ROWS - 1
        if two and x < 0.16: rows[r], rows[r + 1] = "fork", "none"; r += 2; continue
        if two and x < 0.27: rows[r], rows[r + 1] = "join", "joinB"; r += 2; continue
        rows[r] = "dead" if x < 0.40 else "inv" if x < 0.51 else "rep" if x < 0.57 else "plain"; r += 1
    return rows

def side_value(rows):   # grobe Einschätzung, wie gut eine Verdrahtung ist (was ein Mensch in der Vorschau sieht)
    v = {"plain": 1, "rep": 1.8, "fork": 2, "join": 0.6, "joinB": 0, "none": 0, "dead": -0.3, "inv": -0.6}
    return sum(v[e] for e in rows)

def duel(boss, player, rnd):
    while True:
        sides = [gen_side(rnd), gen_side(rnd)]
        half = [i % 2 for i in range(ROWS)]; rnd.shuffle(half); cells = half[:]
        # Seitenwahl (12 s Vorschau): bessere Seite mit Wahrscheinlichkeit pick
        better = 0 if side_value(sides[0]) >= side_value(sides[1]) else 1
        me = better if rnd.random() < player["pick"] else 1 - better
        bo = 1 - me
        prm = {me: player, bo: BOSS_T[boss]}
        caps = {me: player["caps"], bo: BOSS_T[boss]["caps"]}
        pw = {0: {}, 1: {}}
        cdl = {me: 0.6 + rnd.random() * 0.6, bo: 0.9 + rnd.random() * 0.6}
        t = 0.0
        def on(s, r): p = pw[s].get(r); return p and (p["rep"] or p["until"] > t)
        def can(s, r): e = sides[s][r]; return e != "none" and not on(s, r)
        def fire(s, r):
            caps[s] -= 1; pw[s][r] = dict(at=t, until=t + PULSE, rep=sides[s][r] == "rep")
        def think(s):
            T = prm[s]
            if caps[s] <= 0: return
            cdl[s] -= DT
            left = TIME - t; rushing = left <= T["rush"]
            if cdl[s] > 0: return
            if not rushing and caps[s] <= T["save"]: cdl[s] = 0.15; return
            best, bs = None, -1e9
            own = lambda c: 0 if cells[c] == s else 1
            for r in range(ROWS):
                if not can(s, r): continue
                e = sides[s][r]; g = 0
                if e == "plain": g = own(r)
                elif e == "rep": g = own(r) + 0.8
                elif e == "fork": g = own(r) + own(r + 1)
                elif e == "inv": g = -1 if cells[r] == s else -0.3
                elif e == "dead": g = -0.6
                elif e == "join": p = pw[s].get(r + 1); g = own(r) if (p and p["until"] > t) else 0.25
                elif e == "joinB": p = pw[s].get(r - 1); g = own(r - 1) if (p and p["until"] > t) else 0.25
                sc = g + (rnd.random() - 0.5) * T["noise"]
                if sc > bs: bs, best = sc, r
            if best is not None and (bs > 0.2 or rushing): fire(s, best)
            cdl[s] = T["rushCD"] * (0.7 + rnd.random() * 0.6) if rushing else T["cd"][0] * (0.8 + rnd.random() * 0.8)
        def outputs(s):
            out, them = [], 1 - s
            for r, e in enumerate(sides[s]):
                if e in ("plain", "rep"):
                    if on(s, r): out.append((r, s, pw[s][r]["at"], pw[s][r]["rep"]))
                elif e == "inv":
                    if on(s, r): out.append((r, them, pw[s][r]["at"], False))
                elif e == "fork":
                    if on(s, r): out += [(r, s, pw[s][r]["at"], False), (r + 1, s, pw[s][r]["at"], False)]
                elif e == "join":
                    if on(s, r) and on(s, r + 1): out.append((r, s, max(pw[s][r]["at"], pw[s][r + 1]["at"]), False))
            return out
        while t < TIME:
            t += DT
            think(bo); think(me)
            best = [None] * ROWS
            for s in (0, 1):
                for c, col, at, rep in outputs(s):
                    b = best[c]
                    if b is None or (rep and not b[2]) or (rep == b[2] and at > b[1]): best[c] = (col, at, rep)
            for c, b in enumerate(best):
                if b: cells[c] = b[0]
        mine = sum(1 for c in cells if c == me)
        if mine != 6: return mine > 6, mine

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    rnd = random.Random(7); res = {}
    for pk, P in PLAYERS.items():
        res[pk] = {}
        for b in BOSS_T:
            w = sum(duel(b, P, rnd)[0] for _ in range(n))
            res[pk][b] = round(w / n, 4)
    print(json.dumps(res))
