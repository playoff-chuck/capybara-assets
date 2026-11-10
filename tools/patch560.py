#!/usr/bin/env python3
# V560: Keine Zehntonne in gekippten Wellen (Martin 10.11. 16:25): Rettungs-Lucky (wirft sofort ab) und Sofort-Drops (tut/squad/weed)
# warten, solange das Feld um 90° gekippt ist; Lucky Supply hat dort keine Zehntonne auf den Walzen.
# Dazu RU: «radio online».
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V559";', 'const GAME_VER = "V560";')
rep('''    setInterval(() => { try { if (!ov.hidden || !S || !S.started || S.over || S.nuts || S.won || (S.wave || 0) < 30 || S.ton) return;''',
    '''    setInterval(() => { try { if (!ov.hidden || !S || !S.started || S.over || S.nuts || S.won || (S.wave || 0) < 30 || S.ton || S.rotMode) return;   /* V560: nicht im gekippten Feld */''')
rep('''    const PRa = () => (S && (S.wave || 0) >= 100) ? PR : PR.filter(p => p[0] !== "wolf");''',
    '''    const PRa = () => { let L = (S && (S.wave || 0) >= 100) ? PR : PR.filter(p => p[0] !== "wolf"); if (S && S.rotMode) L = L.filter(p => p[0] !== "ton"); return L; };   /* V560: keine Zehntonne im gekippten Feld */''')
rep('''        const [k, o] = dropQ.shift(); dropWait = false; showDrop(k, o);''',
    '''        if (S.rotMode && ["tut", "squad", "weed"].includes(dropQ[0][0])) { dropWait = false; setTimeout(pumpDrop, 2000); return; }   /* V560: Sofort-Zehntonne erst nach dem Kippen */
        const [k, o] = dropQ.shift(); dropWait = false; showDrop(k, o);''')
rep('''      else if (kind === "thief") toast(`TEST · THIEF comes a few seconds into wave ${w} · buy a WOLF CALL in the shop`, "HQ", 3000);''',
    '''      else if (kind === "thief") { S.wolves = Math.max(1, S.wolves || 0); toast(`TEST · THIEF comes a few seconds into wave ${w} · WOLF CALL is in your Pocket`, "HQ", 3000); }   /* V560: Wolf für die Aufnahme schon in der Tasche */''')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
