#!/usr/bin/env python3
# V407 (t12 Nr. 1 + 8): Squad Level 1–50 + Titel. XP aus der Karriere (capy-life): 1 je Splat, 10 je Reihe, 50 je Welle.
# Keine Belohnungen (kein Balancing-Eingriff). Anzeige: Hauptmenü unter dem Claim, Squad File (Level, XP-Balken, nächster Titel),
# Meldung «SQUAD LEVEL n!» beim Aufstieg. Titel: Rookie (1–9) · Splat Pro (10–19) · Ring Keeper (20–34) · World Squad (35–50).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V406";', 'const GAME_VER = "V407";')
CSS = """.sqLvl{position:fixed;left:max(12px,env(safe-area-inset-left,0px));bottom:calc(env(safe-area-inset-bottom,0px) + 18px);z-index:5;pointer-events:none;font-family:var(--f-display);font-size:clamp(10px,3vw,12px);letter-spacing:.08em;color:var(--sand);text-shadow:0 2px 0 #0b0e07,0 0 8px rgba(0,0,0,.7);line-height:1.25;max-width:52vw}.sqLvl b{color:#ffd36a}.sqLvl:empty{display:none}
.sqLv{background:rgba(0,0,0,.25);border:2px solid var(--ink);border-radius:12px;padding:8px 10px;margin:0 0 8px;text-align:center}.sqLv b{display:block;font-family:var(--f-display);font-size:22px;letter-spacing:.06em;color:#ffd36a}.sqLv i{display:block;font-style:normal;font-family:var(--f-display);font-size:13px;letter-spacing:.1em;color:var(--sand)}
.sqBar{height:10px;border-radius:6px;background:rgba(0,0,0,.4);border:1.5px solid var(--ink);overflow:hidden;margin:6px 0 4px}.sqBar span{display:block;height:100%;background:linear-gradient(90deg,#9cf0ff,#ffd36a);border-radius:6px}.sqLv small{display:block;font-size:11px;opacity:.85}
</style>"""
rep(".signRule b{color:#ffd36a}\n</style>", ".signRule b{color:#ffd36a}\n" + CSS)
rep('<div class="tagline claim"><span>Stack \'em.</span><span class="hot">Splat \'em.</span></div></div>',
    '<div class="tagline claim"><span>Stack \'em.</span><span class="hot">Splat \'em.</span></div><div class="sqLvl" id="sqLvl"></div></div>')
JS = r'''
/* V407: Squad Level + Titel (t12 Nr. 1 + 8) – XP aus der Karriere, keine Belohnungen */
const SQ_TITLE = [[35, "World Squad"], [20, "Ring Keeper"], [10, "Splat Pro"], [1, "Rookie"]];
function sqLife() { try { return JSON.parse(localStorage.getItem("capy-life") || "{}") || {}; } catch (e) { return {}; } }
function sqXP(L) { L = L || sqLife(); return (L.k || 0) + 10 * (L.l || 0) + 50 * (L.w || 0); }
function sqNeed(n) { return 40 * (n - 1) * (n - 1); }   /* XP gesamt für Level n (2 → 40, 10 → 3 240, 50 → 96 040) */
function sqLevel(xp) { if (xp == null) xp = sqXP(); let n = 1; while (n < 50 && xp >= sqNeed(n + 1)) n++; return n; }
function sqTitle(n) { return (SQ_TITLE.find(t => n >= t[0]) || SQ_TITLE[3])[1]; }
function sqNextTitle(n) { const t = SQ_TITLE.slice().reverse().find(t => t[0] > n); return t ? { at: t[0], name: t[1] } : null; }
function sqHtml() { const xp = sqXP(), n = sqLevel(xp), f = v => v.toLocaleString("en-US");
  const a = sqNeed(n), b = n < 50 ? sqNeed(n + 1) : a, p = n < 50 ? Math.round(100 * (xp - a) / Math.max(1, b - a)) : 100, nt = sqNextTitle(n);
  return `<div class="sqLv"><b>SQUAD LEVEL ${n}</b><i>${sqTitle(n).toUpperCase()}</i><div class="sqBar"><span style="width:${Math.max(2, Math.min(100, p))}%"></span></div><small>${n < 50 ? `${f(xp)} / ${f(b)} XP${nt ? ` · ${nt.name} at level ${nt.at}` : ""}` : `${f(xp)} XP · max level`}</small></div>`; }
function sqMenu() { try { const el = $("sqLvl"); if (!el) return; const n = sqLevel(), nick = LS.get("tarnturm-nick") || ""; el.innerHTML = `${nick ? nick.toUpperCase() + "<br>" : ""}<b>LVL ${n}</b> · ${sqTitle(n).toUpperCase()}`; } catch (e) {} }
window.__sq = { xp: () => sqXP(), lv: () => sqLevel(), open: () => openSquad() };   /* Test-Haken */
sqMenu(); setInterval(() => { try { if (!$("startMain").hidden) sqMenu(); } catch (e) {} }, 1500);
setInterval(() => { try { if (!S || !S.started || S.over || S.testRun) return; const n = sqLevel(), was = +LS.get("capy-sqlvl") || 0;
  if (!was) { LS.set("capy-sqlvl", n); return; } if (n <= was) return; if (S.inWave || uiWinOpen() || frozen()) return;
  LS.set("capy-sqlvl", n); toast(`SQUAD LEVEL ${n}!${n === 10 || n === 20 || n === 35 ? " · " + sqTitle(n).toUpperCase() : ""}`, "SQUAD", 2400); snd("powerup"); } catch (e) {} }, 3000);
'''
rep('/* V395: ein Auszeichnungs-Icon – Pokal öffnet Medaillen, Reiter zu Hall of fame und Squad */', JS + '/* V395: ein Auszeichnungs-Icon – Pokal öffnet Medaillen, Reiter zu Hall of fame und Squad */')
rep('let h = `<div class="albSec">CAREER</div>', 'let h = sqHtml() + `<div class="albSec">CAREER</div>')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
