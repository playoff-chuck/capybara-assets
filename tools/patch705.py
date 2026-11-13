# V705 (Martin 13.11. 23:41): Die ersten zwei Boss-Hacks ohne Einsatz nur für echte Neulinge.
# Wer schon einmal über Welle 12 hinaus gespielt hat (capy-maxw / Bestwert), bekommt auch nach einem
# Neustart, Speicher-Reset oder auf dem anderen Server (.ru/.com) sofort das Einsatz-Fenster.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep('GAME_VER = "V704"', 'GAME_VER = "V705"')
rep('const first = () => { try { return (LS.get("capy-hk-first") !== "1" && !S.testRun) || (S.testRun && S.testKind === "tips"); } catch (e) { return false; } };',
    'const hkExp = () => { try { const gb = k => { try { return typeof getBest === "function" ? (+getBest(k) || 0) : 0; } catch (e) { return 0; } }; return Math.max(+localStorage.getItem("capy-maxw") || 0, gb("chill"), gb("pro")) >= 13; } catch (e) { return false; } };   /* V705 */\n'
    '  const first = () => { try { return (LS.get("capy-hk-first") !== "1" && !hkExp() && !S.testRun) || (S.testRun && S.testKind === "tips"); } catch (e) { return false; } };')
rep('if (c0 == null) c0 = LS.get("capy-hk-first") === "1" ? 2 : 0; hn = (+c0 || 0) + 1;',
    'if (c0 == null) c0 = LS.get("capy-hk-first") === "1" ? 2 : 0; if (hkExp()) c0 = Math.max(+c0 || 0, 2); hn = (+c0 || 0) + 1;')
open(dst, "w", encoding="utf8").write(s)
print("ok V705")
