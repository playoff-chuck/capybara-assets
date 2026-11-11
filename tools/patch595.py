#!/usr/bin/env python3
# V595 (Martin 11.11.): (1) Nach der Urkunde nur der 10T-Airdrop – 60 s Ruhe ab Schließen der Urkunde: keine Rosie/Blue-Figur
# (buddyHelp, z. B. «HEADS UP! TEN TONS!»), Orden-Fenster (albTry) warten bis danach (Orden bleibt erhalten), Meldungen (msgPush) entfallen.
# (2) Unkraut-Warnung Variante C: einmalige Neuheiten-Karte beim ersten Unkraut (hint «weedintro»), Spiel steht wie bei anderen NEW-Karten.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V594";', 'const GAME_VER = "V595";')
# 1) Ruhefenster nach der Urkunde
rep('''function buddyHelp(kind) { try { window.__msnEv && window.__msnEv("use_" + kind); } catch (e) {}
  try { if ((typeof TUT !== "undefined" && TUT.on) || window.__tutSumPend || window.__tutSumNow || window.__tutSumOpen) return; } catch (e) {}''',
    '''function certQuiet() { return performance.now() - (window.__certQuietT || -1e9) < 60000; }   /* V595: 60 s nach der Urkunde nur der 10T-Airdrop */
function buddyHelp(kind) { try { window.__msnEv && window.__msnEv("use_" + kind); } catch (e) {}
  try { if ((typeof TUT !== "undefined" && TUT.on) || window.__tutSumPend || window.__tutSumNow || window.__tutSumOpen || certQuiet()) return; } catch (e) {}''')
rep('''function msgPush(m) {
''', '''function msgPush(m) {
  try { if (certQuiet()) return; } catch (e) {}   /* V595 */
''')
rep('''function albTry() {
''', '''window.__TQ = () => ({ certQuiet, msgPush, buddyHelp, hint, n: () => MSGQ.length, q: () => MSGQ.map(m => m.title) });   /* V595: Test-Zugang */
function albTry() {
  try { if (albQ.length && certQuiet()) { clearTimeout(window.__albT); window.__albT = setTimeout(albTry, 2000); return; } } catch (e) {}   /* V595: Orden erst nach der Ruhe */
''')
rep('''window.__tutSumOpen = false; try { S.coachHold = false; snd("uiTap"); } catch (e) {} window.__evtLast = performance.now(); }''',
    '''window.__tutSumOpen = false; window.__certQuietT = performance.now(); try { S.coachHold = false; snd("uiTap"); } catch (e) {} window.__evtLast = performance.now(); }''')
# 2) Unkraut-Vorstellung (einmal je Gerät)
rep('''    snd("siren"); { const nm = k === "weed" && D.weeds.length > 1 ? NAMES.weed5 : NAMES[k]; announce(nm[0], nm[1], "ALERT", 2400); }
''', '''    snd("siren"); { const nm = k === "weed" && D.weeds.length > 1 ? NAMES.weed5 : NAMES[k]; announce(nm[0], nm[1], "ALERT", 2400); }
    if (k === "weed") setTimeout(() => { try { hint("weedintro", "WEEDS!", "🌱 → ⬆ → ✂ Weeds grow toward the ring. If one reaches it, the field is lost. Cut it with a Sniper strike or Tesla storm!", "board"); } catch (e) {} }, 2600);   /* V595: Unkraut-Vorstellung (Variante C) */
''')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
