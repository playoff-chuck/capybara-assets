"""V293 (Martin 17:47): Sidewinder ohne 180°-Flip. Neue Regel: jede Sidewinder-Welle dreht nur einmal um 90°, abwechselnd
−90° (1., 3., …) und +90° (2., 4., …). Das Paket am Wellenende dreht entsprechend zurück und ist beschriftet mit der Gegenrichtung
(nach −90° → «+90° PACKAGE», nach +90° → «−90° PACKAGE»). Zähler S.rotN wird gespeichert."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V292";', 'const GAME_VER = "V293";')
rep('S.rotT = S.rotT || 0; if (!S.rotMode) setRotMode(1);',
    'S.rotT = S.rotT || 0; if (!S.rotMode) { if (S.rotNW !== S.wave) { S.rotNW = S.wave; S.rotN = (S.rotN || 0) + 1; } setRotMode(S.rotN % 2 === 0 ? 2 : 1); }   /* V293: abwechselnd −90° / +90° */')
rep('if (S.rotMode === 1 && (S.rotT >= ROT_FLIP_AT / specK() || (S.toSpawn === 0 && S.rotT >= 20))) {',
    'if (false && S.rotMode === 1 && (S.rotT >= ROT_FLIP_AT / specK() || (S.toSpawn === 0 && S.rotT >= 20))) {   /* V293: kein 180°-Flip mehr */')
rep('const t = m === 1 ? "WORLD TILT −90°" : "FLIPPED · +90°";', 'const t = m === 1 ? "WORLD TILT −90°" : "WORLD TILT +90°";')
rep('if (rp) { S.rotDone = S.wave; title = "−90° PACKAGE · WORLD RESTORED"; loot = [["rot", "Tilt", "−90°"], ...(loot || []).slice(0, 2)];',
    'const rpBack = S.rotMode === 2 ? "−90°" : "+90°";\n  if (rp) { S.rotDone = S.wave; title = `${rpBack} PACKAGE · WORLD RESTORED`; loot = [[rpBack === "+90°" ? "rotp" : "rot", "Tilt", rpBack], ...(loot || []).slice(0, 2)];')
rep('rp ? "−90° PACKAGE"', 'rp ? `${rpBack} PACKAGE`')
rep('const SAVE_KEYS = ["ordDue",', 'const SAVE_KEYS = ["rotN", "rotNW", "ordDue",')
js = r'''
  /* V293: Paket-Symbol +90° */
  try { if (typeof LOOT_ICON !== "undefined" && LOOT_ICON.rot && !LOOT_ICON.rotp) LOOT_ICON.rotp = LOOT_ICON.rot.replace("−90", "+90").replace('<path d="M7 4a7 7 0 0 1 11 2"', '<path transform="matrix(-1 0 0 1 24 0)" d="M7 4a7 7 0 0 1 11 2"').replace('<path d="M19 2v4h-4"', '<path transform="matrix(-1 0 0 1 24 0)" d="M19 2v4h-4"'); } catch (e) {}
'''
i = s.rindex('})();\n</script>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
