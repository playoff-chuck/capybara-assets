#!/usr/bin/env python3
"""V484 – Der erste Gratis-Ten-ton (Wow «SQUAD INCOMING», W1–6) kommt nicht mehr von selbst, sondern als Air-Drop-Karte «SQUAD INCOMING · DROP IT ▶»;
nach dem Bestätigen fällt der Ten-ton sofort (Martin 08.11. 23:28: «nicht einfach machen, sondern als Airdrop kommen lassen, bestätigen und gleich einlösen»).
Nutzung: python3 tools/patch484.py src dst"""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); v = int(m.group(1))
rep(m.group(0), f'const GAME_VER = "V{v + 1}";')
# Wow: Banner + Karte statt sofortigem Abwurf
rep('''      snd("horn"); setTimeout(() => { if (!S.over) { S.tons = (S.tons || 0) + 1; startTon(); } }, 1500); } }''',
    '''      snd("horn"); setTimeout(() => { if (!S.over) { S.tons = (S.tons || 0) + 1; if (window.__dropAd) window.__dropAd("squad"); else startTon(); } }, 1500); } }   /* V484: als Air-Drop-Karte, DROP IT löst sofort aus */''')
# Karte
rep('''                 weed: { img: "img/ad_drop_free.webp", name: "WEED DEFENSE DROP",''',
    '''                 squad: { img: "img/ad_drop_free.webp", name: "SQUAD INCOMING", line: "Your partner sends a free Ten-ton drop. Confirm it and it falls right now – flattens the whole stack!", met: ["+1 Ten-ton", "Drops now"], btn: "DROP IT ▶" },   /* V484 */
                 weed: { img: "img/ad_drop_free.webp", name: "WEED DEFENSE DROP",''')
# Beim Schließen: wie weed sofort abwerfen
rep('''if (window.__dropKind === "weed") { window.__dropKind = null;''',
    '''if (window.__dropKind === "squad") { window.__dropKind = null; setTimeout(() => { try { if (S && S.started && !S.over && !S.ton) startTon(); } catch (e) {} }, 400); }   /* V484 */
      else if (window.__dropKind === "weed") { window.__dropKind = null;''')
# Sprachclip wie beim normalen Drop
rep('''const vl = { ton: "ad_drop", friend: "ad_drop", sweep: "ad_sweep",''', '''const vl = { ton: "ad_drop", friend: "ad_drop", squad: "ad_drop", sweep: "ad_sweep",''')
rep('''if (kind === "sweep" || kind === "ton" || kind === "friend") [0.5, 0.8]''', '''if (kind === "sweep" || kind === "ton" || kind === "friend" || kind === "squad") [0.5, 0.8]''')
open(dst, "w", encoding="utf-8").write(s); print("ok", v + 1)
