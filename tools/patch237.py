"""V237: Shop: (1) Sprechblase von Major Ledger neu: oben Name links und Gold-Pille rechts, darunter der Spruch
über die volle Breite (immer 2 Zeilen hoch, nichts verschiebt sich). (2) Gesperrte Sachen sagen jetzt, WARUM:
«🔒 WAVE 12» statt «LOCKED»; Waffen zeigen «TAP A TOWER» (Waffen kauft man am Turm), statt grau «ON TOWER»."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V236";', 'const GAME_VER = "V237";')
import re
n = 0
for k in ["snipe", "tesla", "mix", "lock", "chomp", "ton"]:
    a = f'unlocked("{k}") ? "BUY" : "LOCKED"'
    if a in s: s = s.replace(a, f'unlocked("{k}") ? "BUY" : `<i class="lk">🔒 WAVE ${{unlockedAt("{k}")}}</i>`'); n += 1
assert n == 6, n
rep('unlocked(k) ? "ON TOWER" : "LOCKED"', 'unlocked(k) ? "TAP A TOWER" : `<i class="lk">🔒 WAVE ${unlockedAt(k)}</i>`')
rep('<em>${S.gold} gold</em>', '<em><i></i>${S.gold.toLocaleString("en")}</em>')
css = '''<style id="v237">
#sheet .shopItem button:has(.lk) span.lbl,#sheet button:has(.lk) .lbl{display:none!important}
button .lk{font-style:normal;white-space:nowrap}
/* Major Ledger: Kopfzeile Name | Gold, darunter Spruch */
#sheet .ledgerTop{display:flex!important;width:auto!important;box-sizing:border-box!important}
#sheet .ledgerTop .ledgerBubble{display:grid!important;grid-template-columns:1fr auto!important;grid-template-areas:"nm gd" "tx tx"!important;align-items:center!important;gap:3px 10px!important;
  width:100%!important;max-width:none!important;flex:1 1 auto!important;padding:8px 14px 9px!important;box-sizing:border-box!important}
#sheet .ledgerTop .ledgerBubble b{grid-area:nm!important;font:400 15px/1 var(--f-display,"Bangers",sans-serif)!important;letter-spacing:.06em!important;color:#d94c8c!important;margin:0!important;white-space:nowrap}
#sheet .ledgerTop .ledgerBubble em{grid-area:gd!important;justify-self:end!important;margin:0!important;display:inline-flex!important;align-items:center;gap:5px;font:800 15px/1 "Baloo 2",sans-serif!important;font-style:normal!important;color:#3a2414!important;
  background:#ffe9a8;border:2px solid #3a2414;border-radius:999px;padding:3px 10px 2px 4px;box-shadow:0 2px 0 #3a2414;white-space:nowrap}
#sheet .ledgerTop .ledgerBubble em i{width:15px;height:15px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#fff2a8,#f2b51e 55%,#b8800a);border:1.5px solid #3a2414;box-sizing:border-box}
#sheet .ledgerTop .ledgerBubble span{grid-area:tx!important;font:600 13.5px/1.25 "Baloo 2",sans-serif!important;color:#3a2414!important;min-height:2.5em;display:-webkit-box!important;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin:0!important;flex:none!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
