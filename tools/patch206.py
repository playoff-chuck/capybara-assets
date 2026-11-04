"""V206: Turm-Fenster – alle Waffen-Boxen gleich hoch, vor und nach dem Kauf (feste Höhe, Werte einzeilig,
Upgrade-Knopf feste Breite); «(▲+x height)» kurz als «▲+x»."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V205";', 'const GAME_VER = "V206";')
rep('` <span style="color:#f0b323">(▲+${heightBonus(t).toFixed(1)} height)</span>`', '` <span style="color:#f0b323" title="height bonus">▲+${heightBonus(t).toFixed(1)}</span>`')
css = '''<style id="v206">
#sheet .slot{height:76px!important;min-height:76px!important;max-height:76px!important;box-sizing:border-box!important;overflow:hidden!important;align-content:center}
#sheet .slot .wline{min-width:0;gap:8px!important;align-items:center!important}
#sheet .slot .wline>div{min-width:0;flex:1 1 auto}
#sheet .slot .wname{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;line-height:1.1!important}
#sheet .slot .wstat{white-space:normal!important;overflow:hidden;display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;font-size:12.5px!important;line-height:1.25!important}
#sheet .slot .wline>button{flex:0 0 118px!important;width:118px!important;min-width:118px!important;max-width:118px!important;height:40px!important;padding:0 6px!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#sheet .slot .slotRow{align-self:center}
#sheet .slot .slotRow button{height:56px!important;min-height:56px!important;max-height:56px!important;overflow:hidden}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
