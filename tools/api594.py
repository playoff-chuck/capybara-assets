#!/usr/bin/env python3
# V594 capy-api: Metrik-Erfassung (Martin 11.11. 01:44 «Ja»): events + uid/ch/team/data, neue kinds, /admin/stats
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('EVENT_KINDS = ("start", "error", "leave", "back", "wave")',
    'EVENT_KINDS = ("start", "error", "leave", "back", "wave", "tut", "tutskip", "cert", "hack", "set", "buy", "spec", "cancel", "ad", "death", "restart", "perf")   # V594')
rep('''def init_db():
    with db() as c:
        c.executescript(SCHEMA)
''', '''def init_db():
    with db() as c:
        c.executescript(SCHEMA)
        cols = {r[1] for r in c.execute("PRAGMA table_info(events)")}   # V594: Metrik-Spalten, alte Zeilen bleiben
        for col, typ in (("uid", "TEXT"), ("ch", "TEXT"), ("team", "INTEGER DEFAULT 0"), ("data", "TEXT")):
            if col not in cols:
                c.execute(f"ALTER TABLE events ADD COLUMN {col} {typ}")
        c.execute("CREATE INDEX IF NOT EXISTS events_uid ON events(uid, t)")
''')
rep('''                max(0.0, min(64.0, float(d.get("mem")))) if isinstance(d.get("mem"), (int, float)) and not isinstance(d.get("mem"), bool) else None)
        t, rows = now_ms(), []''', '''                max(0.0, min(64.0, float(d.get("mem")))) if isinstance(d.get("mem"), (int, float)) and not isinstance(d.get("mem"), bool) else None)
        uid = d.get("uid") if isinstance(d.get("uid"), str) and UID_RE.fullmatch(d.get("uid")) else None   # V594
        ext = (uid, clean_text(d.get("ch"), 12) or None, 1 if d.get("team") is True or d.get("team") == 1 else 0)
        t, rows = now_ms(), []''')
rep('''            rows.append((t, base[0], base[1], k, integer(e.get("w"), "w", 0, MAX_WAVE, 0), clean_text(e.get("scr"), 16),
                         clean_text(e.get("msg"), 200), clean_text(e.get("src"), 80), mins) + base[2:])''',
    '''            dd = clean_profile(e.get("d")) if isinstance(e.get("d"), dict) else None
            dj = json.dumps(dd, separators=(",", ":"))[:400] if dd else None
            rows.append((t, base[0], base[1], k, integer(e.get("w"), "w", 0, MAX_WAVE, 0), clean_text(e.get("scr"), 16),
                         clean_text(e.get("msg"), 200), clean_text(e.get("src"), 80), mins) + base[2:] + ext + (dj,))''')
rep('''c.executemany("INSERT INTO events(t,ver,sess,kind,wave,scr,msg,src,mins,dev,plat,br,sw,sh,mem) "
                              "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)''',
    '''c.executemany("INSERT INTO events(t,ver,sess,kind,wave,scr,msg,src,mins,dev,plat,br,sw,sh,mem,uid,ch,team,data) "
                              "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)''')
rep('''            if self.route()[0] == "/events":
                if not rate_ok''', '''            if self.route()[0] == "/admin/stats":   # V594: Analyse (nur echte Spieler)
                if not rate_ok(self.client_ip(), "ad", 30):
                    return self.send_json(429, {"error": "too many requests"})
                d = self.parse_json(raw, n)
                tok = d.get("token")
                with db() as c:
                    hs = [x["v"] for x in c.execute("SELECT v FROM kv WHERE k='admin:hash' OR k LIKE 'admin:hash:%'").fetchall()]
                    th = hashlib.sha256(tok.encode()).hexdigest() if isinstance(tok, str) else ""
                    if not (th and any(hmac.compare_digest(h, th) for h in hs)):
                        return self.send_json(403, {"error": "forbidden"})
                    try: days = max(1, min(EVENT_RETENTION_DAYS, int(d.get("days") or 30)))
                    except Exception: days = 30
                    return self.send_json(200, admin_stats(c, days))
            if self.route()[0] == "/events":
                if not rate_ok''')
rep('''def save_key(code):''', '''def admin_stats(c, days):
    """V594: Trichter, Ausstiege, Boss-Hack, Musik aus, Wiederkehr – nur echte Spieler (ohne team/dev/bot)."""
    now = now_ms(); since = now - days * 86400 * 1000
    bad = set(ADMIN_UIDS)
    for r in c.execute("SELECT uid, data FROM players"):
        try: dd = json.loads(r["data"])
        except Exception: dd = {}
        if dd.get("team") or dd.get("dev") or dd.get("bot"): bad.add(r["uid"])
    ev = [r for r in c.execute("SELECT t, sess, kind, wave, scr, uid, ch, data FROM events WHERE t >= ? AND uid IS NOT NULL AND dev=0 AND COALESCE(team,0)=0 ORDER BY t", (since,)) if r["uid"] not in bad]
    def dj(r):
        try: return json.loads(r["data"]) if r["data"] else {}
        except Exception: return {}
    U = {}
    sess_last = {}
    hack, deaths, perf, loads, chans, spec, buys, ads, sets = {}, {}, [], [], {}, {}, {}, {}, {}
    for r in ev:
        u = U.setdefault(r["uid"], {"first": r["t"], "last": r["t"], "tut": 0, "cert": 0, "w": 0, "mu": None, "skip": 0, "start": 0, "ch": r["ch"] or "?"})
        u["last"] = r["t"]; k = r["kind"]; x = dj(r)
        sess_last[r["sess"]] = (r["t"], r["scr"] or "?", r["wave"] or 0, k)
        if k in ("wave", "death") or (r["wave"] or 0) > 0: u["w"] = max(u["w"], r["wave"] or 0)
        if k == "start":
            if "mu" in x: u["mu"] = x.get("mu")
            if isinstance(x.get("ld"), (int, float)) and 0 < x["ld"] < 120000: loads.append(x["ld"])
        if k == "tut": u["tut"] = max(u["tut"], int(x.get("n") or 0)); u["start"] = 1
        if k == "wave" and (r["wave"] or 0) >= 1: u["start"] = 1
        if k == "tutskip": u["skip"] = max(u["skip"], int(x.get("n") or 1)); u["start"] = 1
        if k == "cert": u["cert"] = 1
        if k == "hack": hack[str(x.get("r") or "?")] = hack.get(str(x.get("r") or "?"), 0) + 1
        if k == "death": deaths[r["wave"] or 0] = deaths.get(r["wave"] or 0, 0) + 1
        if k == "perf" and isinstance(x.get("fps"), (int, float)): perf.append(x["fps"])
        if k == "spec": spec[str(x.get("k") or "?")] = spec.get(str(x.get("k") or "?"), 0) + 1
        if k == "buy": buys[str(x.get("k") or "?")] = buys.get(str(x.get("k") or "?"), 0) + 1
        if k == "ad": ads[str(x.get("a") or "?")] = ads.get(str(x.get("a") or "?"), 0) + 1
        if k == "set":
            for kk in ("music", "mute", "lang"):
                if kk in x: sets[f"{kk}={x[kk]}"] = sets.get(f"{kk}={x[kk]}", 0) + 1
                if kk == "music" and kk in x: u["mu"] = x[kk]
    for u in U.values(): chans[u["ch"]] = chans.get(u["ch"], 0) + 1
    n = len(U)
    steps = [("geöffnet", n), ("gestartet", sum(1 for u in U.values() if u["start"] or u["w"] > 0))]
    for i in range(1, 11): steps.append((f"Lektion {i}", sum(1 for u in U.values() if u["tut"] >= i)))
    steps += [("Urkunde", sum(1 for u in U.values() if u["cert"])), ("Welle 5", sum(1 for u in U.values() if u["w"] >= 5)),
              ("Welle 10", sum(1 for u in U.values() if u["w"] >= 10)), ("Welle 30", sum(1 for u in U.values() if u["w"] >= 30))]
    funnel = [{"step": a, "n": b, "pct": round(100 * b / n, 1) if n else 0} for a, b in steps]
    ex = {}
    for t, scr, w, k in sess_last.values():
        if now - t > 30 * 60 * 1000:
            key = f"{scr} · W{w}"; ex[key] = ex.get(key, 0) + 1
    exits = sorted(({"where": k, "n": v} for k, v in ex.items()), key=lambda x: -x["n"])[:15]
    mu_known = [u for u in U.values() if u["mu"] is not None]
    old1 = [u for u in U.values() if now - u["first"] > 86400000]; old7 = [u for u in U.values() if now - u["first"] > 7 * 86400000]
    ret1 = sum(1 for u in old1 if u["last"] - u["first"] > 20 * 3600000); ret7 = sum(1 for u in old7 if u["last"] - u["first"] > 7 * 86400000 - 4 * 3600000)
    loads.sort()
    return {"ok": True, "days": days, "players": n, "events": len(ev), "funnel": funnel, "exits": exits,
            "skipAt": {str(i): sum(1 for u in U.values() if u["skip"] == i) for i in range(1, 11) if any(u["skip"] == i for u in U.values())},
            "hack": hack, "deathsByWave": sorted(([w, c2] for w, c2 in deaths.items()), key=lambda x: -x[1])[:12],
            "musicOff": {"off": sum(1 for u in mu_known if not u["mu"]), "of": len(mu_known)},
            "return": {"d1": ret1, "d1of": len(old1), "d7": ret7, "d7of": len(old7)},
            "perf": {"n": len(perf), "avgFps": round(sum(perf) / len(perf), 1) if perf else None},
            "loadMs": {"n": len(loads), "median": loads[len(loads) // 2] if loads else None},
            "channels": chans, "spec": spec, "buy": buys, "ad": ads, "set": sets}

def save_key(code):''')
open(p, "w", encoding="utf-8").write(s)
print("ok api594")
