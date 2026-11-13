/* Megatest: zusätzliche Live-Prüfungen (Kriterienkatalog 12.11.2026). Läuft neben CHECK aus testbot.py. */
(() => {
  const S0 = () => window.__TT && window.__TT.S, g = id => document.getElementById(id);
  let k = 0, mOpen = {}, mT = {}, hkW = {}, lastOffClose = -1e9, lastAdClose = -1e9, evs = [], idle = 0, idleW = -1, low = 0, bubV = null, posBase = {}, posBad = {}, contChk = {}, says = [], fontsDone = false, inWSince = 0;
  const LANG = window.__LANG || 'en';
  const hookSay = () => { try { const X = window.__TT && window.__TT.SFX; if (!X || X.__mt) return; const o = X.say; X.__mt = 1;
      X.say = function (key) { try { const t = performance.now(), S = S0(); says.push({ t, key: String(key) }); says = says.filter(s => t - s.t < 20000);
        const nonJoy = says.filter(s => !/^(nailedit|boomshaka|hellyeah|phenomenal|outstanding|spectacular)$/.test(s.key));
        if (nonJoy.length >= 3) window.__ADD('A16', 'say@' + (S ? S.wave : 0), `${nonJoy.length} Sprüche in 20 s: ${nonJoy.map(s => s.key).join(', ')}`, { shot: 0 });
        const joy = says.filter(s => t - s.t < 5000 && /^(nailedit|boomshaka|hellyeah|phenomenal|outstanding|spectacular)$/.test(s.key)); if (joy.length >= 2) window.__ADD('A15', 'joy@' + (S ? S.wave : 0), 'Mehrere Jubelsprüche nach Boss-Hack: ' + joy.map(s => s.key).join(', '), { shot: 0 }); } catch (e) {}
        return o.apply(this, arguments); }; } catch (e) {} };
  const ownText = e => [...e.childNodes].some(c => c.nodeType === 3 && c.textContent.trim().length > 1);
  setInterval(() => { try {
    const add = window.__ADD, vis = window.__VIS, R = window.__R, inter = window.__INTER, MOD = window.__MODAL || [], S = S0(); if (!add || !S || !S.started) return; k++; hookSay();
    const now = performance.now(), W = S.wave | 0, nuts = !!S.nuts, open = MOD.filter(id => vis(g(id))), mapUp = document.body.classList.contains('mapUp');
    /* Fenster-Zeitachse: D2 (Anzeigen ≥ 45 s), D3, D4, E5 */
    for (const id of MOD) { const o = open.includes(id);
      if (o && !mOpen[id]) { mT[id] = now; evs.push({ id, t: now, w: W }); evs = evs.slice(-8);
        if (id === 'ovAd' && now - lastAdClose < 45000) add('D2', 'ad45@' + W, `Anzeige nur ${((now - lastAdClose) / 1000).toFixed(1)} s nach der letzten Anzeige`);
        if (id === 'ovHackAd') { hkW[W] = (hkW[W] || 0) + 1; if (hkW[W] > 1) add('D3', 'hk2@' + W, `Zweites Boss-Hack-Angebot in Welle ${W}`); }
        const ch = evs.filter(e => now - e.t < 12000); if (ch.length >= 3 && new Set(ch.map(e => e.id)).size >= 3) add('D4', ch.map(e => e.id).join('>'), 'Fensterkette: ' + ch.map(e => e.id).join(' → ')); }
      if (!o && mOpen[id]) { if (id === 'ovAd') lastAdClose = now; }
      mOpen[id] = o;
      if (o && now - (mT[id] || now) > 3500 && k % 4 === 0) { const bs = [...g(id).querySelectorAll('button')].filter(b => vis(b)); if (bs.length && bs.every(b => b.disabled)) add('E5', id, `${id}: nach 3,5 s alle Knöpfe gesperrt`); } }
    /* D8: Spiel läuft hinter einem Pflichtfenster weiter */
    const stopIds = open.filter(id => !['ovMap'].includes(id));
    if (stopIds.length && S.inWave && !S.paused && !S.duel) { inWSince += 500; if (inWSince > 2500) add('D8', stopIds.join('+'), `Welle läuft hinter Fenster ${stopIds.join(', ')} weiter`); } else inWSince = 0;
    /* D19: Welle startet nicht (Pause ohne Fenster > 25 s) */
    if (!S.inWave && !open.length && !S.paused && !mapUp && !S.over && !S.duel) { idle += 500; if (idle > 25000 && idleW !== W) { idleW = W; add('D19', 'idle@' + W, `Nach Welle ${W} startet die nächste Welle nicht (> 25 s ohne Fenster)`); } } else idle = 0;
    /* D14: neuer Kontinent → Feld leer, keine Türme */
    if (!nuts && [31, 61, 91, 121].includes(W) && S.inWave && !contChk[W]) { contChk[W] = 1; const nT = S.towers && (S.towers.size != null ? S.towers.size : S.towers.length); if (nT > 0) add('D14', 'cont@' + W, `Neuer Kontinent W${W}: noch ${nT} Türme auf dem Feld`); }
    /* D16/D17/B6 */
    const pill = g('hackPill');
    if (vis(pill) && (open.includes('ovHackAd') || open.includes('ovHack'))) add('B6', 'pill', 'Boss-Signal-Pille über offener Boss-Hack-Anzeige');
    if (W >= 150 && !nuts && vis(pill)) add('D16', 'pill150', 'Boss-Signal nach W150');
    if (nuts) { for (const id of ['ovHackAd', 'ovAd', 'ovCoachAd', 'ovBandit']) if (open.includes(id)) add('D17', id, `Nuts: ${id} erscheint (soll gesperrt sein)`); if (vis(pill)) add('D17', 'pill', 'Nuts: Boss-Signal sichtbar'); }
    /* B5: Wellennummer unter Sprechblase */
    const wn = g('waveNum'); if (vis(wn)) for (const id of ['buddy', 'coach']) { const b = g(id); if (vis(b) && !(id === 'buddy' && !b.classList.contains('on')) && inter(R(b), R(wn))) add('B5', id, `Wellennummer unter ${id}`); }
    /* C5: Boss-Hack-Fenster im Bild */
    const hk = g('ovHack'); if (vis(hk)) for (const c of hk.children) if (vis(c)) { const r = R(c); if (r.top < -2 || r.bottom > innerHeight + 2 || r.left < -2 || r.right > innerWidth + 2) add('C5', c.id || c.className, `Boss-Hack-Teil ${c.id || c.className} ragt aus dem Bildschirm`); }
    /* A7/A8: Musikpegel */
    try { if (typeof TP !== 'undefined' && TP.el && !TP.el.paused && !mapUp && !window.__tpHush && !S.duel && typeof TP_VOL === 'function') { const v = TP.el.volume, t = TP_VOL();
        if (t > 0.05 && v < 0.4 * t) { if (++low === 14) add('A7', 'mus@' + W, `Musik seit 7 s auf ${(v / t * 100).toFixed(0)} % des Sollpegels`, { shot: 0 }); } else low = 0;
        const bd = g('buddy'), on = bd && bd.classList.contains('on'); if (on && bubV == null) bubV = v; if (on && bubV > 0.05 && v < bubV * 0.7) add('A8', 'bub@' + W, `Musik sinkt während Sprechblase ${bubV.toFixed(2)}→${v.toFixed(2)}`, { shot: 0 }); if (!on) bubV = null; } } catch (e) {}
    /* E3: Anzeigen oben bleiben stehen */
    if (!open.length && !mapUp && k > 40) for (const id of ['waveNum']) { const e = g(id); if (!vis(e)) continue; const r = R(e), key = id + innerWidth;
      if (!posBase[key]) posBase[key] = [r.left, r.top]; const d = Math.hypot(r.left - posBase[key][0], r.top - posBase[key][1]);
      posBad[key] = d > 6 ? (posBad[key] || 0) + 1 : 0; if (posBad[key] === 6) add('E3', id, `${id} verschiebt sich um ${d.toFixed(0)} px`); }
    /* langsamere Prüfungen */
    if (k % 8 === 0) {
      /* E2: Knöpfe groß genug */
      for (const b of document.querySelectorAll('.deck button')) if (vis(b) && R(b).height < 30) add('E2', b.id || b.className, `Knopf ${b.id || b.className} nur ${R(b).height.toFixed(0)} px hoch`);
      /* C13/C10/C14: Texte in offenen Fenstern */
      const roots = open.map(g).filter(Boolean); if (vis(g('buddy'))) roots.push(g('buddy'));
      for (const r0 of roots) for (const e of r0.querySelectorAll('*')) { if (!ownText(e) || !vis(e)) continue; const fs = parseFloat(getComputedStyle(e).fontSize), tx = (e.innerText || '').trim().slice(0, 50);
        if (fs < 11 && tx.length > 2) add('C13', tx, `Schrift ${fs.toFixed(1)} px: «${tx}»`);
        if (LANG === 'ru') { if (/золота|ЗОЛОТО/.test(tx)) add('C10', 'gold:' + tx, `RU «золото» statt Münze: «${tx}»`); if (W >= 31 && /напарник/.test(tx)) add('C10', 'np:' + tx, `Anrede «напарник» ab W31: «${tx}»`); if (W >= 61 && /дружище/.test(tx)) add('C10', 'dr:' + tx, `Anrede «дружище» ab W61: «${tx}»`); } }
      if (/tetris|tetromino/i.test(document.body.innerText || '')) add('C14', 'tetris', 'Text «Tetris/Tetromino» sichtbar');
      /* B10: Ortsschilder auf der Karte */
      if (mapUp) { const L = [...g('ovMap').querySelectorAll('*')].filter(e => ownText(e) && vis(e)).map(e => [e, R(e)]);
        for (let i = 0; i < L.length; i++) for (let j = i + 1; j < L.length; j++) { const a = L[i][1], b = L[j][1]; const ix = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)), iy = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
          if (ix * iy > 0.3 * Math.min(a.width * a.height, b.width * b.height) && !L[i][0].contains(L[j][0]) && !L[j][0].contains(L[i][0])) add('B10', (L[i][0].innerText + '|' + L[j][0].innerText).slice(0, 60), `Karte: «${L[i][0].innerText.slice(0, 25)}» überdeckt «${L[j][0].innerText.slice(0, 25)}»`); } }
      /* B14: Diplom im Rahmen */
      const pp = document.querySelector('.ctPaper'); if (vis(pp)) { const P = R(pp); for (const c of pp.querySelectorAll('*')) if (vis(c)) { const r = R(c); if (r.left < P.left - 2 || r.right > P.right + 2 || r.top < P.top - 2 || r.bottom > P.bottom + 2) add('B14', c.className || c.tagName, `Diplom: ${c.className || c.tagName} ragt aus dem Papier`); } }
      /* B8: etwas liegt über der Game-over-Karte */
      const ov = g('ovOver'); if (vis(ov)) { const box = R(ov.firstElementChild || ov), z = +getComputedStyle(ov).zIndex || 0;
        for (const e of document.querySelectorAll('body *')) { if (ov.contains(e) || !ownText(e) || !vis(e)) continue; const cs = getComputedStyle(e); if (cs.position !== 'fixed' && cs.position !== 'absolute') continue; let zz = +cs.zIndex; if (isNaN(zz)) zz = 0; if (zz > z && inter(R(e), box)) add('B8', (e.id || e.className || '') + '', `Über Game-over liegt: «${(e.innerText || '').slice(0, 40)}»`); } }
    }
    if (k % 20 === 0) {
      /* B16: kaputte Bilder */
      for (const im of document.images) if (im.getAttribute('src') && vis(im) && im.complete && im.naturalWidth === 0) add('B16', (im.getAttribute('src') || '').slice(0, 60), `Bild lädt nicht: ${im.getAttribute('src')}`);
      /* B19: Spielfeld nicht fast schwarz */
      if (!open.length && !mapUp && S.inWave) { try { const cv = document.querySelector('#board canvas') || g('board'); const c2 = cv && cv.getContext && cv.getContext('2d'); if (c2) { const w = cv.width, h = cv.height, d = c2.getImageData(w * 0.3 | 0, h * 0.2 | 0, w * 0.4 | 0, h * 0.3 | 0).data; let s = 0, n = 0; for (let i = 0; i < d.length; i += 64) { s += 0.3 * d[i] + 0.59 * d[i + 1] + 0.11 * d[i + 2]; n++; } if (n && s / n < 22) add('B19', 'dark@' + W, `Spielfeld fast schwarz (Helligkeit ${(s / n).toFixed(0)})`); } } catch (e) {} }
      /* C12: Schriften geladen */
      if (!fontsDone && k > 40) { fontsDone = true; try { const smp = { ru: 'БОСС', es: 'ñÑ¡¿', pt: 'çãõ', en: 'BOSS' }[LANG] || 'BOSS'; for (const f of ['Bangers', '"Baloo 2"']) if (!document.fonts.check(`20px ${f}`, smp)) add('C12', f, `Schrift ${f} für «${smp}» nicht geladen (Ersatzschrift)`, { shot: 0 }); } catch (e) {} }
    }
  } catch (e) {} }, 500);
})();
/* Megatest C10 (Martin 13.11. 00:39 MV): RU-Anrede ab W31 «дружище», ab W61 «друг» – alle sichtbaren Texte UND gesprochene Clips */
(() => { if ((window.__LANG || 'en') !== 'ru') return; let seenV = 0;
  setInterval(() => { try { const add = window.__ADD, S = window.__TT && window.__TT.S; if (!add || !S || !S.started) return; const W = S.wave | 0; if (W < 31) return;
    const RX = W >= 61 ? /[Нн]апарник|[Дд]ружище/ : /[Нн]апарник/;
    const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: n => RX.test(n.data) ? 1 : 3 }); let n;
    while ((n = tw.nextNode())) { const e = n.parentElement; if (!e || ['SCRIPT', 'STYLE'].includes(e.nodeName)) continue; const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
      if (r.width < 2 || r.height < 2 || cs.visibility === 'hidden' || cs.display === 'none') continue;
      add('C10', 'txt:' + n.data.trim().slice(0, 40), `Anrede falsch (W${W}): «${n.data.trim().slice(0, 70)}»`); }
    const L = window.__voiceLog || [], VT = window.__VOICE_TEXT || {};
    for (const v of L.slice(seenV)) { const k = String(v.k), t = String(VT[k] || '');
      if (!/__d[rg]$/.test(k) && /напарник/i.test(t)) add('C10', 'say:' + k, `Gesprochen «напарник» ab W31 (Clip ${k}): «${t.slice(0, 60)}»`, { shot: 0 });
      if (W >= 61 && /__dr$/.test(k)) add('C10', 'say:' + k, `Gesprochen «дружище» ab W61 (Clip ${k})`, { shot: 0 }); }
    seenV = L.length; } catch (e) {} }, 2000); })();
