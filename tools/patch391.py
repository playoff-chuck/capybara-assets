"""V391: t12 Nr. 10 Karriere-Seite + Nr. 4 Monster Cards (Martin, 07.11.).
Neuer Knopf «Squad» im Hauptmenü → Karte «SQUAD FILE»: Karriere-Zahlen (Splats, Reihen, Wellen, Läufe, Spielzeit,
Sterne, Orte, Medaillen) und Monster Cards (je Monster Bronze 100 / Silber 1000 / Gold 5000 Splats, lebenslang).
Neuer lokaler Zähler capy-mcards {kind: n} (in killMilestones, gepuffert).
Aufruf: python3 tools/patch391.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
# Knopf
rep('''<button id="btnAlbum" class="btn-small">Medals</button></div>''',
    '''<button id="btnAlbum" class="btn-small">Medals</button><button id="btnSquad" class="btn-small">Squad</button></div>''')
# Overlay
rep('''      <div id="ovAlbum" hidden>''',
    '''      <div id="ovSquad" hidden><div class="albBox"><button class="albX" id="sqX" aria-label="Close">✕</button><h2>SQUAD FILE</h2><div id="sqBody"></div></div></div>
      <div id="ovAlbum" hidden>''')
# CSS
rep('''#ovAlbum,#ovGive{position:fixed;''', '''#ovSquad{position:fixed;inset:0;z-index:90;display:flex;align-items:center;justify-content:center;padding:12px;background:rgba(40,28,16,.55)}
#ovSquad[hidden]{display:none}
.sqStats{display:grid;grid-template-columns:1fr 1fr;gap:5px}
.sqStats div{background:#fff;border:2px solid #d8c7a6;border-radius:12px;padding:6px 8px;line-height:1.1}
.sqStats b{display:block;font-family:Bangers,system-ui;font-size:22px;letter-spacing:.5px}
.sqStats small{font-size:10px;font-weight:800;opacity:.7}
.mcGrid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.mcCard{border-radius:12px;background:#ece0c8;border:3px solid #d8c7a6;padding:4px 4px 5px;text-align:center;position:relative}
.mcCard img{width:100%;aspect-ratio:1;object-fit:contain}
.mcCard.off img{filter:grayscale(1) brightness(.2);opacity:.45}
.mcCard i{display:block;font-style:normal;font-size:11px;font-weight:900;line-height:1.1}
.mcCard small{display:block;font-size:9.5px;font-weight:800;opacity:.7}
.mcCard em{position:absolute;top:3px;right:4px;font-style:normal;font-size:9px;font-weight:900;border-radius:8px;padding:1px 5px;background:#3a2a1a;color:#fff}
.mcCard.t1{border-color:#c07a3a;background:#f6e2cc}.mcCard.t1 em{background:#c07a3a}
.mcCard.t2{border-color:#9aa6b2;background:#eef2f6}.mcCard.t2 em{background:#7b8794}
.mcCard.t3{border-color:#f0c24a;background:#fff6d6;box-shadow:0 2px 0 #d9a520}.mcCard.t3 em{background:#d9a520}
#ovAlbum,#ovGive{position:fixed;''')
# Zähler je Monster
rep('''function killMilestones(m) {
''', '''function killMilestones(m) {
  try { if (!S.testRun && m && m.kind) { MC.n[m.kind] = (MC.n[m.kind] || 0) + 1; MC.dirty = true; } } catch (e) {}   /* V%d: Monster Cards */
''' % NEW)
# Logik + Knopf (nach Album-Knopf)
rep('''$("btnAlbum").addEventListener("click", () => { SFX.init(); openAlbum(); });''',
'''$("btnAlbum").addEventListener("click", () => { SFX.init(); openAlbum(); });
/* V%d: Squad File – Karriere-Seite + Monster Cards */
const MC_NAME = { norm: "Grunt", fast: "Scout", heavy: "Brute", munch: "Muncher", runner: "Sprinter", kiefer: "The Jaw", bomber: "Bomber", volt: "Sparky", jaguar: "Jaguar", mummy: "Mummy", tiger: "Tiger", bear: "Bear" };
const MC_TIER = [100, 1000, 5000], MC_TN = ["BRONZE", "SILVER", "GOLD"];
function openSquad() {
  try { if (MC.dirty) mcSave(); } catch (e) {}
  let L = {}; try { L = JSON.parse(localStorage.getItem("capy-life") || "{}") || {}; } catch (e) {}
  const st = starsAll(), stars = Object.values(st).reduce((a, b) => a + (+b || 0), 0), places = Object.keys(st).length, med = Object.keys(ALB.got || {}).length;
  const f = n => (n || 0).toLocaleString("en-US"), mins = Math.round((L.t || 0) / 60), tm = mins >= 60 ? `${Math.floor(mins / 60)} h ${mins %% 60} min` : `${mins} min`;
  const box = (v, l) => `<div><b>${v}</b><small>${l}</small></div>`;
  let h = `<div class="albSec">CAREER</div><div class="sqStats">` + box(f(L.k), "monsters splatted") + box(f(L.l), "lines cleared") + box(f(L.w), "waves cleared") + box(f(L.r), "runs") + box(tm, "time on duty") + box(`${stars} ★`, "stars · " + places + " of 30 places") + box(`${med} / 81`, "medals") + box(f(Math.max(0, ...Object.keys(st).map(Number)) * 5 + (places ? 5 : 0)), "best wave reached") + `</div>`;
  const kinds = Object.keys(MC_NAME).filter(k => MON_SPR_SRC[k]); let got = 0;
  const cards = kinds.map(k => { const n = MC.n[k] || 0, t = MC_TIER.filter(x => n >= x).length; if (t) got += t; const next = MC_TIER[t];
    return `<div class="mcCard ${n ? "t" + t : "off"}">${t ? `<em>${MC_TN[t - 1]}</em>` : ""}<img src="${MON_SPR_SRC[k]}" alt=""><i>${n ? MC_NAME[k] : "???"}</i><small>${f(n)}${next ? " / " + f(next) : " · max"}</small></div>`; }).join("");
  h += `<div class="albSec">MONSTER CARDS<span>${got} / ${kinds.length * 3}</span></div><div class="mcGrid">${cards}</div>`;
  $("sqBody").innerHTML = h; $("ovSquad").hidden = false; try { snd("uiTap"); } catch (e) {}
}
$("btnSquad").addEventListener("click", () => { SFX.init(); openSquad(); });
$("sqX").addEventListener("click", () => { $("ovSquad").hidden = true; });
$("ovSquad").addEventListener("click", e => { if (e.target.id === "ovSquad") $("ovSquad").hidden = true; });''' % NEW)
# MC-Speicher früh definieren (vor killMilestones-Nutzung): direkt nach ALB
rep('''const ALB = (() => {''', '''const MC = (() => { let a = {}; try { a = JSON.parse(localStorage.getItem("capy-mcards") || "{}") || {}; } catch (e) {} return { n: a, dirty: false }; })();   /* V%d */
function mcSave() { try { localStorage.setItem("capy-mcards", JSON.stringify(MC.n)); MC.dirty = false; } catch (e) {} }
setInterval(() => { if (MC.dirty) mcSave(); }, 3000); addEventListener("pagehide", () => { if (MC.dirty) mcSave(); });
const ALB = (() => {''' % NEW)
rep('body:has(#ovAlbum:not([hidden])) #btnOffline,', 'body:has(#ovAlbum:not([hidden])) #btnOffline,body:has(#ovSquad:not([hidden])):has(#sqBody):has(#sqX) #btnOffline,')
rep('body:has(#ovAlbum:not([hidden])) #btnMap,', 'body:has(#ovAlbum:not([hidden])) #btnMap,body:has(#ovSquad:not([hidden])):has(#sqBody):has(#sqX) #btnMap,')
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
