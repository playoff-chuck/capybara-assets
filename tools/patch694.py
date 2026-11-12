# V694 (Martin 13.11. 00:39 MV): RU-Anrede ab W31 «дружище», ab W61 «друг» – überall, geschrieben UND gesprochen.
# 1) capyAddr ersetzt jedes «напарник/Напарник» (nicht nur «, напарник»), ab W61 auch «дружище» → «друг».
# 2) Sicherheitsnetz: alle 2,5 s werden Texte, die schon vor W31/W61 auf dem Bildschirm standen, nachgezogen.
# 3) Sprache: auch Sprüche, die über ihren Satz (statt Schlüssel) aufgerufen werden, nehmen den __dr/__dg-Clip; Protokoll window.__voiceLog.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
rep('''function capyAddr(v) { try { if (I18N.lang !== "ru" || typeof v !== "string" || v.indexOf("напарник") < 0) return v; const TS = window.__TT && window.__TT.S, w = (TS && +TS.wave) || 0; if (w < 31) return v;   /* V639: Anrede nach Welle */
  return v.replace(/, напарник(?=[\\s.,!?–—])/g, w >= 61 ? ", друг" : ", дружище"); } catch (e) { return v; } }''',
'''function capyAddr(v) { try { if (I18N.lang !== "ru" || typeof v !== "string" || !/[Нн]апарник|[Дд]ружище/.test(v)) return v; const TS = window.__TT && window.__TT.S, w = (TS && +TS.wave) || 0; if (w < 31) return v;   /* V639/V694: Anrede nach Welle – überall */
  const to = w >= 61 ? "друг" : "дружище", up = x => x[0].toUpperCase() + x.slice(1);
  let r = v.replace(/(^|[^А-Яа-яЁё])([Нн])апарник(?![А-Яа-яЁё])/g, (m, a, n) => a + (n === "Н" ? up(to) : to));
  if (w >= 61) r = r.replace(/(^|[^А-Яа-яЁё])([Дд])ружище(?![А-Яа-яЁё])/g, (m, a, d) => a + (d === "Д" ? "Друг" : "друг"));
  return r; } catch (e) { return v; } }''')
rep('''    const ck = VOICE[text] ? text : VOICE_BY_TEXT[norm(text)];''',
'''    let ck = VOICE[text] ? text : VOICE_BY_TEXT[norm(text)];
    try { if (ck && window.__sayKey) { const k2 = window.__sayKey(ck); if (k2 !== ck && BUF["v_" + k2] && BUF["v_" + k2].length) ck = k2; } } catch (e) {}   /* V694: Anrede-Clip auch bei Aufruf über den Satz */
    try { if (ck) { const L = window.__voiceLog || (window.__voiceLog = []); L.push({ k: ck, t: performance.now() }); if (L.length > 60) L.shift(); } } catch (e) {}''')
rep('''/* V642: Sicherheitsnetz – nichts wartet länger als 2 Wellen */''',
'''/* V694: Anrede-Sicherheitsnetz – Texte, die vor W31/W61 schon standen, nachziehen */
try { (() => { const RX = /[Нн]апарник|[Дд]ружище/, SKIP = new Set(["SCRIPT", "STYLE", "TEXTAREA", "INPUT"]);
  setInterval(() => { try { if (I18N.lang !== "ru") return; const S = window.__TT && window.__TT.S; if (!S || (S.wave | 0) < 31) return;
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: n => RX.test(n.data) && n.parentNode && !SKIP.has(n.parentNode.nodeName) ? 1 : 3 }); const L = []; let n; while ((n = w.nextNode())) L.push(n);
    for (const t of L) { const v = capyAddr(t.data); if (v !== t.data) t.data = v; } } catch (e) {} }, 2500); })(); } catch (e) { console.error("v694", e); }
/* V642: Sicherheitsnetz – nichts wartet länger als 2 Wellen */''')
rep('$("hkAgain").hidden = !S.testRun && !(HK.coach && coachLeft() > 0);', '$("hkAgain").hidden = !(HK.coach && coachLeft() > 0);   /* V694: kein «Again (test)» mehr */')
rep('#ovHack #hackRes.hkNew .hkRow{padding:0 14px;box-sizing:border-box}', '#ovHack #hackRes.hkNew .hkRow{padding:0 14px;box-sizing:border-box;justify-content:center}#ovHack #hackRes.hkNew .hkRow button{flex:0 1 calc(50% - 4px)!important}#ovHack #hackRes.hkNew.lose #hkBack{background:linear-gradient(180deg,#ffb0da,#f06aac)!important;color:#fff!important}')
rep('const GAME_VER = "V693"', 'const GAME_VER = "V694"')
open(dst, "w", encoding="utf8").write(s); print("ok", len(s))
