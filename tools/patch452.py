#!/usr/bin/env python3
"""V452 (Martin 08.11. 13:18–13:20):
- Guide «Gadgets»: neue Icons (Sprites wie im Shop), dazu Chomper, Ten-ton, Lockdown, Wolf call und Elite-Turm (nicht kaufbar, W6 · 56 · 106).
- Hall of Fame: feste Spalten – Platz | Name | Sterne | Zahlen – alles in einer Linie; blauer runder Schließen-Knopf wie bei Medals/Squad.
- Reiter MEDALS · HALL OF FAME · SQUAD tanzen bei den ersten drei Einstiegen abwechselnd (zeigt, dass es weitere Reiter gibt).
Nutzung: python3 tools/patch452.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V451";', 'const GAME_VER = "V452";')

# --- Guide: Gadgets ---
rep('''    ["tesla", ICON.tesla, "Tesla storm", `${TESLA_COST} gold · wonder weapon: lightning wipes a 4×4 target. Splats count three times.`, "tesla"],
  ];
  $("armsList").innerHTML = arms.map(([k, icon, name, desc]) => `<div class="mRow">${icon}<div><b>${name}</b><span>${desc}</span></div>${tag(unlockedAt(k))}</div>`).join("");''',
'''    ["tesla", ICON.tesla, "Tesla storm", `${TESLA_COST} gold · wonder weapon: lightning wipes a 4×4 target. Splats count three times.`, "tesla"],
    ["chomp", ICON.chomp, "Chomper", `${CHOMP_COST} gold · steel jaws run the ring backwards and eat every monster and block in their way.`, "chomp"],
    ["ton", ICON.ton, "Ten-ton drop", `${TON_COST} gold · giant weight: crushes every monster above the stack and squeezes all blocks to half. HQ drops a free one before weed seeds land.`, "ton"],
    ["lock", ICON.lock, "Lockdown", `${LOCK_COST} gold · ${LOCK_TIME} s time stop. Free every ${LOCK_NEED} rows.`, "lock"],
    ["wolf", ICON.tesla, "Wolf call", `${WOLF_COST} gold · a howl in the dark: the raccoon thief drops your gold and runs. Also a Lucky Supply prize.`, "wolf"],
    ["elite", "", "Elite tower", `Not for sale · your partner parachutes in with it. 60 s pink laser that burns everything on its line. Waves 6, 56 and 106.`, "elite"],
  ];   /* V452: alle Gadgets, Sprite-Icons */
  const gIcon = (k, icon) => k === "elite" ? `<img class="gIco" src="img/chute_1.webp" alt="">` : (typeof ICO_SPR !== "undefined" && ICO_SPR[k]) ? `<img class="gIco" src="${ICO_SPR[k]}" alt="">` : icon;
  const gTag = k => k === "elite" ? `<em class="elite">W6 · 56 · 106</em>` : k === "wolf" ? tag(WOLF_W) : tag(unlockedAt(k));
  $("armsList").innerHTML = arms.map(([k, icon, name, desc]) => `<div class="mRow">${gIcon(k, icon)}<div><b>${name}</b><span>${desc}</span></div>${gTag(k)}</div>`).join("");''')
rep('.mRow canvas,.mRow svg{width:40px;height:40px;display:block}',
    '.mRow canvas,.mRow svg{width:40px;height:40px;display:block}.mRow img.gIco{width:40px;height:40px;display:block;object-fit:contain;transform:scale(1.15);filter:drop-shadow(0 2px 2px rgba(0,0,0,.35))}.mRow em.elite{background:#ffd3ea;color:#8a2a5a;border:1px solid #c23f8a}')

# --- Hall of Fame: Spalten in einer Linie ---
rep('.hs .row{display:grid;grid-template-columns:20px 1fr auto auto;gap:6px;text-align:left;padding:1px 6px;border-radius:3px;color:var(--fg);line-height:1.2}',
    '.hs .row{display:grid;grid-template-columns:28px minmax(0,1fr) 92px 96px;gap:6px;text-align:left;padding:1px 6px;border-radius:3px;color:var(--fg);line-height:1.2;align-items:baseline}'
    '.hs .row span:nth-child(1){text-align:right}.hs .row span:nth-child(2){overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.hs .row span:nth-child(3){text-align:right;white-space:nowrap}.hs .row span:nth-child(4){text-align:right;white-space:nowrap}'
    '#hsPlaces .prRow span:nth-child(3){letter-spacing:-1px}   /* V452: feste Spalten – Sterne, Zahlen, Level untereinander */')
# Nuts-Liste: Level in die 4. Spalte (unter W-Nummern), Splats in die 3.
rep('<div class="row${markT && e.t === markT ? " me" : ""}"><span>${i + 1}.</span><span>${e.name}</span><span>L${e.wave | 0}</span><span>${(e.kills || 0) ? e.kills + "✕" : ""}</span></div>',
    '<div class="row${markT && e.t === markT ? " me" : ""}"><span>${i + 1}.</span><span>${e.name}</span><span>${(e.kills || 0) ? e.kills + "✕" : ""}</span><span>L${e.wave | 0}</span></div>')
# Schließen-Knopf blau und rund wie bei Medals/Squad
rep('<button class="xBtn" id="btnHsClose" aria-label="Close"><svg viewBox="0 0 24 24"><path d="M5 5l14 14M19 5L5 19" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg></button>',
    '<button class="albX" id="btnHsClose" aria-label="Close">✕</button>')
rep('#ovSettings{z-index:65}#ovHs{z-index:65}#ovHs .hsBox{max-height:min(64vh,540px);overflow-y:auto}#ovHs .hs{width:100%}',
    '#ovSettings{z-index:65}#ovHs{z-index:65}#ovHs .hsBox{max-height:min(64vh,540px);overflow-y:auto}#ovHs .hs{width:100%}#ovHs .hsBox{position:relative}#ovHs .hsBox .albX{top:8px;right:8px;width:40px!important;height:40px!important;min-height:0!important;padding:0!important;line-height:1!important;font-size:20px!important}#ovHs .hs{max-width:none!important}')

# --- Reiter tanzen bei den ersten drei Einstiegen ---
rep('  const go = k => { for (const o of Object.values(OV)) { const e = $(o); if (e) e.hidden = true; } tabs(k); _go0(k);',
    '''  const dance = () => { try { const n = +(LS.get("capy-aw-dance") || 0); if (n >= 3 || document.body.classList.contains("awOn")) return; LS.set("capy-aw-dance", n + 1); bar.classList.add("dance"); setTimeout(() => bar.classList.remove("dance"), 5200); } catch (e) {} };   /* V452: erste drei Einstiege */
  const go = k => { dance(); for (const o of Object.values(OV)) { const e = $(o); if (e) e.hidden = true; } tabs(k); _go0(k);''')
rep('#awBar button.on{background:#3a2a1a!important;color:#fff6e6!important}', '''#awBar button.on{background:#3a2a1a!important;color:#fff6e6!important}
#awBar.dance button{animation:awDance 1.5s ease-in-out 3}#awBar.dance button:nth-child(2){animation-delay:.5s}#awBar.dance button:nth-child(3){animation-delay:1s}
@keyframes awDance{0%,100%{transform:translateY(0) rotate(0)}25%{transform:translateY(-7px) rotate(-2.5deg)}50%{transform:translateY(0) rotate(0)}75%{transform:translateY(-4px) rotate(2deg)}}
@media (prefers-reduced-motion:reduce){#awBar.dance button{animation:none}}''')

open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
