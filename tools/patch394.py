"""V394: Wolf call (Martin, 07.11.): Shop-Item 500 Gold ab Welle 100 (wenn der Dieb kommt). In der Tasche → HOWL:
man hört einen echten Wolf heulen, der Dieb dreht um, rennt davon und lässt geklautes Gold zurück.
Der Wolf ist nur zu hören, nicht zu sehen. Tippen auf den Dieb mit Wolf in der Tasche ruft ihn ebenfalls.
Martin: nur Aufnahme 3 (Rudel, NPS Yellowstone, gemeinfrei) → sfx/wolf.mp3. Dieb dreht um und rennt davon, Gold bleibt da.
Sniper/Tesla wirken nicht mehr gegen den Dieb; alle Texte verweisen auf den Wolf.
Dateien: img/wolf_icon.webp (Nano Banana Pro, 0,14 $), sfx/wolf.mp3.
Aufruf: python3 tools/patch394.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
rep('const SNIPE_COST = 200, MIX_COST = 350, TESLA_COST = 500;', '''const SNIPE_COST = 200, MIX_COST = 350, TESLA_COST = 500, WOLF_COST = 500, WOLF_W = 100;   /* V%d: Wolf call */
function playWolf() { try { if (SFX.muted) return; const a = new Audio("sfx/wolf.mp3"); a.volume = Math.min(1, 3.6 * Math.pow(SFX.vol || 0.3, 2)) * (SFX.ch ? SFX.ch("f") : 1); a.play().catch(() => {}); } catch (e) {} }
function wolfCall() { const D = window.__dist && window.__dist.D, T = D && D.thief;
  if (!(S.wolves > 0)) { snd("nope"); return; }
  if (!T) { toast("NO THIEF AROUND · the wolf stays in your pocket", "POCKET", 1800); snd("nopeSoft"); return; }
  S.wolves--; S.mode = null; S.aim = null; playWolf();
  setTimeout(() => { if (D.thief !== T) return; T.flee = true; const g = T.stolen || 0; T.stolen = 0; if (g) S.gold += g;
    toast(g ? `THE WOLF SCARED HIM OFF · +${g} gold back` : "THE WOLF SCARED HIM OFF!", "HQ", 2200); praise("AWOOO!", 2, false);
    setTimeout(() => { if (D.thief === T) { D.thief = null; window.__thiefPos(null); } }, 1800); }, 900); }''' % NEW)
rep('ton:"img/ton_icon.webp",', 'ton:"img/ton_icon.webp",wolf:"img/wolf_icon.webp",')
# Shop-Reihe
rep('''  rows.push([unlockedAt("mix"), item("mix",''', '''  rows.push([WOLF_W, item("wolf", ICON.tesla, "Wolf call", WOLF_COST, (S.wave || 0) >= WOLF_W ? "A howl in the dark: the thief runs off and drops your gold." : `Locked · unlocks at wave ${WOLF_W}`, (S.wave || 0) >= WOLF_W ? "BUY" : `<i class="lk">🔒 WAVE ${WOLF_W}</i>`, (S.wave || 0) < WOLF_W || S.gold < WOLF_COST, "btn-accent")]);
  rows.push([unlockedAt("mix"), item("mix",''')
# Kauf
rep('''    else if (k === "mix") { if (!unlocked("mix") || S.gold < MIX_COST)''', '''    else if (k === "wolf") { if ((S.wave || 0) < WOLF_W || S.gold < WOLF_COST) { snd("nope"); return; } S.gold -= WOLF_COST; S.wolves = (S.wolves || 0) + 1; snd("shopBuy"); toast(`WOLF CALL · pocket ×${S.wolves}`, "ARMORY"); renderShop(); }
    else if (k === "mix") { if (!unlocked("mix") || S.gold < MIX_COST)''')
# Tasche
rep('''  if (S.tons > 0) h += shopItem("pocket", "ton",''', '''  if (S.wolves > 0) h += shopItem("pocket", "wolf", ICON.tesla, "Wolf call", `×${S.wolves}`, "Howl: a thief runs off and drops your gold.", "HOWL", !(window.__dist && window.__dist.D && window.__dist.D.thief), "btn-accent");
  if (S.tons > 0) h += shopItem("pocket", "ton",''')
rep('''if (b.dataset.pocket === "ton") { closeSheet(); startTon(); return; }''', '''if (b.dataset.pocket === "ton") { closeSheet(); startTon(); return; } if (b.dataset.pocket === "wolf") { closeSheet(); wolfCall(); return; }''')
# Speichern
rep('''    try { if (typeof SAVE_KEYS !== "undefined") ["banditDone", "banditNext"].forEach(''', '''    try { if (typeof SAVE_KEYS !== "undefined" && !SAVE_KEYS.includes("wolves")) SAVE_KEYS.push("wolves"); } catch (e) {}
    try { if (typeof SAVE_KEYS !== "undefined") ["banditDone", "banditNext"].forEach(''')
# Dieb antippen: nur noch Wolf
rep('''    let used = null;
    if (S.mode === "snipe" && S.snipes > 0) { S.snipes--; used = "snipe"; } else if (S.mode === "tesla" && S.teslas > 0) { S.teslas--; used = "tesla"; }
    if (!used) { toast((S.snipes > 0 || S.teslas > 0) ? "POCKET → Sniper or Tesla, then tap the thief" : "Only Sniper or Tesla can stop him!", "HQ", 1800); snd("nopeSoft"); return; }''',
    '''    if (T.flee) return; if (S.wolves > 0) { wolfCall(); return; }   /* V%d: nur der Wolf vertreibt den Dieb */
    toast("Only a WOLF CALL scares him off · find it in the shop", "HQ", 1800); snd("nopeSoft"); return;
    let used = null;''' % NEW)
rep('''thief: ["THIEF!", "Stop him with Tesla or Sniper"]''', '''thief: ["THIEF!", "A WOLF CALL scares him off · shop → Wolf call"]''')
rep(' + (S.wave >= 100 ? ", stops thieves." : ".")', ' + "."', 3)
rep('''|| !(S.mode === "snipe" || S.mode === "tesla")) return;''', '''|| true) return;   /* V%d: Sniper/Tesla nicht mehr gegen den Dieb */''' % NEW)
rep('''if (!T.stolen && T.t >= 10) {''', '''if (!T.stolen && !T.flee && T.t >= 10) {''')
rep('''const x = t < 8 ? x0''', '''let x = t < 8 ? x0''')
rep('''geht im gleichen Tempo weiter */''', '''geht im gleichen Tempo weiter */
    if (T.flee) { if (T.fx0 == null) { T.fx0 = T.lx != null ? T.lx : x; T.ft0 = t; } x = T.fx0 - (t - T.ft0) * 460; } T.lx = x;   /* V%d: flieht vor dem Wolf nach links */''' % NEW)
rep('''const t = T.t, P = pose(t), h = SZ - 14;''', '''const t = T.t, P = pose(t), h = SZ - 14; if (T.flee) { P.sx = -1; P.fi = 7 + Math.floor(t * 18) % 8; P.tilt = -0.08; P.bob = Math.abs(Math.sin(t * 18)) * 2; }''')
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
