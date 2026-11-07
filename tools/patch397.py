"""V397 (Martin, 07.11.):
- Wolf-Werbung in der Welle vor jedem Dieb (99, 109, 118, 129 …), Bild ad_wolf.webp (Nano Banana Pro 0,14 $), nur wenn noch kein Wolf in der Tasche.
- General schlägt nach dem Diebstahl den Wolf vor.
- Wolf call jederzeit einsetzbar (Shop: USE, Tasche: HOWL); ohne Dieb ist er verschwendet.
- Reiter MEDALS · HALL OF FAME · SQUAD als feste Leiste oben, immer an derselben Stelle; aktiver Reiter invers (dunkel, helle Schrift).
Aufruf: python3 tools/patch397.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
# --- Wolf jederzeit
rep('''  if (!T) { toast("NO THIEF AROUND · the wolf stays in your pocket", "POCKET", 1800); snd("nopeSoft"); return; }''',
    '''  if (!T) { S.wolves--; S.mode = null; S.aim = null; playWolf(); setTimeout(() => toast("AWOOO! · no thief around – howl wasted", "POCKET", 2000), 600); return; }''')
rep('''"HOWL", !(window.__dist && window.__dist.D && window.__dist.D.thief), "btn-accent");''', '''"HOWL", false, "btn-accent");''')
rep('ton:"img/ton_icon.webp",wolf:"img/wolf_icon.webp",', 'ton:"img/ton_icon.webp",wolf:"img/wolf_icon.webp",wolfuse:"img/wolf_icon.webp",')
rep('''  rows.push([WOLF_W, item("wolf",''', '''  if (S.wolves > 0) rows.push([WOLF_W - 0.1, shopItem("shop", "wolfuse", ICON.tesla, "Wolf call", `×${S.wolves}`, "Howl now: a thief runs off and drops your gold. No thief? Then it's wasted.", "USE", false, "btn-accent")]);
  rows.push([WOLF_W, item("wolf",''')
rep('''    else if (k === "wolf") {''', '''    else if (k === "wolfuse") { closeSheet(); wolfCall(); }
    else if (k === "wolf") {''')
# --- General schlägt Wolf vor
rep('''toast(`THIEF GRABBED ${T.stolen} GOLD!`, "ALERT", 1800);''', '''toast(`THIEF GRABBED ${T.stolen} GOLD!`, "ALERT", 1800); setTimeout(() => { if (D.thief === T && !T.flee) toast(S.wolves > 0 ? "QUICK! Use your WOLF CALL – he'll drop the gold!" : "Raccoons hate wolves! Get a WOLF CALL in the shop.", "HQ", 2800); }, 2100);''')
# --- Werbung
rep('''                 mix: { img: "img/ad_mix.webp",''', '''                 wolf: { img: "img/ad_wolf.webp", sale: "img/ad_wolf.webp", st: [[11, 37], [12, 74], [88, 18]], tag: "NIGHT WATCH", line: "Raccoon thieves are coming! One howl and they run – and drop your gold." },
                 mix: { img: "img/ad_mix.webp",''')
rep('''k === "lock" ? LOCK_COST : TON_COST;''', '''k === "lock" ? LOCK_COST : k === "wolf" ? WOLF_COST : TON_COST;''')
rep('''      else if (k === "mix") S.mixers = (S.mixers || 0) + 1; else if (k === "snipe")''', '''      else if (k === "wolf") S.wolves = (S.wolves || 0) + 1;
      else if (k === "mix") S.mixers = (S.mixers || 0) + 1; else if (k === "snipe")''')
rep('''    /* V299: Gratis-Air-Drops als Anzeige */''', '''    /* V%d: Wolf-Werbung in der Welle vor dem Dieb */
    const thiefW = w => { let x = 100, i = 0; const st = [10, 9, 11]; while (x < w) x += st[i++ %% 3]; return x === w; };
    setInterval(() => { try { const w = S && (S.wave || 0); if (!S || !S.started || S.over || S.nuts || S.testRun || !S.inWave || w < 99 || !thiefW(w + 1) || S.wolfAdW === w || S.wolves > 0) return;
      if (!calm() || !window.__offerOK()) return; S.wolfAdW = w; late = true; S.intro = true; S.adOpen = true; show("wolf", false); } catch (e) {} }, 900);
    try { if (typeof SAVE_KEYS !== "undefined" && !SAVE_KEYS.includes("wolfAdW")) SAVE_KEYS.push("wolfAdW"); } catch (e) {}
    /* V299: Gratis-Air-Drops als Anzeige */''' % NEW)
rep('''const INTRO_GEAR = {
''', '''const INTRO_GEAR = {
  wolf:  ["Wolf call",      "A howl in the dark: raccoon thieves run and drop your gold.", () => [`${typeof WOLF_COST !== "undefined" ? WOLF_COST : 500} gold`, "Scares thieves", "Gold comes back"]],
''')
# --- Reiter als feste Leiste
rep('''.awTabs{display:flex;gap:4px;margin:0 34px 8px 0}
.awTabs button{flex:1;min-width:0;padding:6px 2px;border-radius:10px;border:2px solid #3a2a1a;background:#ece0c8;color:#3a2a1a;font:400 15px/1 Bangers,system-ui;letter-spacing:.5px;box-shadow:0 2px 0 #3a2a1a}
.awTabs button.on{background:#ffd84d}
#ovHs .awTabs{margin:0 30px 8px 0}''', '''#awBar{position:fixed;left:50%;top:calc(env(safe-area-inset-top,0px) + 10px);transform:translateX(-50%);width:min(420px,calc(100vw - 24px));z-index:120;display:none;gap:5px}
body.awOn #awBar{display:flex}
#awBar button{flex:1;min-width:0;padding:9px 2px 7px;border-radius:12px;border:3px solid #3a2a1a;background:#fff6e6;color:#3a2a1a;font:400 17px/1 Bangers,system-ui!important;letter-spacing:.5px;box-shadow:0 3px 0 #3a2a1a!important;background:#fff6e6!important;background-image:none!important;color:#3a2a1a!important;margin:0!important;min-height:0!important}
#awBar button.on{background:#3a2a1a!important;color:#fff6e6!important}
body.awOn #ovAlbum,body.awOn #ovSquad{padding-top:calc(env(safe-area-inset-top,0px) + 62px)!important;align-items:flex-start!important}
body.awOn #ovHs{padding-top:calc(env(safe-area-inset-top,0px) + 62px)!important}''')
rep('''  const tabs = act => { for (const k in BOX) { const box = document.querySelector(BOX[k]); if (!box) continue; let t = box.querySelector(".awTabs");
      if (!t) { t = document.createElement("div"); t.className = "awTabs"; t.innerHTML = `<button data-aw="medals">MEDALS</button><button data-aw="hof">HALL OF FAME</button><button data-aw="squad">SQUAD</button>`; box.insertBefore(t, box.firstChild); }
      t.querySelectorAll("button").forEach(b => b.classList.toggle("on", b.dataset.aw === act)); } };''',
    '''  const bar = document.createElement("div"); bar.id = "awBar"; bar.className = "awTabs"; bar.innerHTML = `<button data-aw="medals">MEDALS</button><button data-aw="hof">HALL OF FAME</button><button data-aw="squad">SQUAD</button>`; document.body.appendChild(bar);
  const tabs = act => { bar.querySelectorAll("button").forEach(b => b.classList.toggle("on", b.dataset.aw === act)); };   /* V%d: feste Leiste, aktiver Reiter invers */
  let awAct = null; const _go0 = k => { awAct = k; document.body.classList.add("awOn"); };
  setInterval(() => { const open = Object.entries(OV).find(([k, o]) => { const e = $(o); return e && !e.hidden; }); if (!open) { if (document.body.classList.contains("awOn")) document.body.classList.remove("awOn"); awAct = null; return; }
    if (awAct && open[0] !== awAct) tabs(open[0]); }, 200);''' % NEW)
rep('''  const go = k => { for (const o of Object.values(OV)) { const e = $(o); if (e) e.hidden = true; } tabs(k);''',
    '''  const go = k => { for (const o of Object.values(OV)) { const e = $(o); if (e) e.hidden = true; } tabs(k); _go0(k);''')
rep('''(S.chomps > 0 ? 1 : 0) + (S.tons > 0 ? 1 : 0);
  if (kinds === 0 && coachLeft() <= 0) openShop();
  else if (S.locks > 0 || S.chomps > 0 || S.tons > 0 || coachLeft() > 0)''', '''(S.chomps > 0 ? 1 : 0) + (S.tons > 0 ? 1 : 0) + (S.wolves > 0 ? 1 : 0);
  if (kinds === 0 && coachLeft() <= 0) openShop();
  else if (S.locks > 0 || S.chomps > 0 || S.tons > 0 || S.wolves > 0 || coachLeft() > 0)''')
rep('''const nSp = (S.snipes > 0 ? 1 : 0) + (S.mixers > 0 ? 1 : 0) + (S.teslas > 0 ? 1 : 0) + (S.locks > 0 ? 1 : 0) + (S.chomps > 0 ? 1 : 0) + (S.tons > 0 ? 1 : 0);''', '''const nSp = (S.snipes > 0 ? 1 : 0) + (S.mixers > 0 ? 1 : 0) + (S.teslas > 0 ? 1 : 0) + (S.locks > 0 ? 1 : 0) + (S.chomps > 0 ? 1 : 0) + (S.tons > 0 ? 1 : 0) + (S.wolves > 0 ? 1 : 0);''')
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
