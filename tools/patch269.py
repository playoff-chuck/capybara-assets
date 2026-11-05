"""V269 (Martin 05.11. 15:23): General-Statistiken. Alle 5–6 Wellen spricht der General beim Wellen-Ende statt seines
üblichen Spruchs eine Statistik (30 verschiedene, ohne Wiederholung bis alle durch sind), z. B. «95 % make it this far»,
«Faster than 72 % of all players», «1,000 monsters down – career total». Vergleichswerte vorerst aus unseren
Simulationen (v6, 4000 Läufe) bzw. Schätzwerten; Karriere-Zähler (Monster, Zeilen, Spielzeit, Läufe) lokal auf dem Gerät."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V268";', 'const GAME_VER = "V269";')
rep('function genWaveMsg(title, loot) { const say = FP_SAY[(S.fpI = ((S.fpI || 0) + 1 + Math.floor(Math.random() * 9)) % FP_SAY.length)];',
    'function genWaveMsg(title, loot) { let say = FP_SAY[(S.fpI = ((S.fpI || 0) + 1 + Math.floor(Math.random() * 9)) % FP_SAY.length)]; try { const st = window.__genStat && window.__genStat(); if (st) say = st; } catch (e) {}')
js = r'''
  /* V269: General-Statistiken alle 5–6 Wellen (Vergleich vorerst aus Simulation v6 / Schätzwerten) */
  try { (() => {
    const REACH = [100,99,98,97,96,96,96,96,96,96,96,96,96,96,96,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,94,94,94,94,94,94,94,94,94,93,93,93,93,92,92,91,91,91,91,90,90,90,89,88,87,87,86,86];
    const reach = w => REACH[Math.max(1, Math.min(150, w)) - 1];
    const expK = w => { try { return Math.min(limits(w).monsters, G.waveBase + G.wavePer * w) * (w >= 21 ? 0.55 : 1) * 0.95; } catch (e) { return 10; } };
    try { if (typeof SAVE_KEYS !== "undefined") ["statNext", "statSeen", "lifeK", "lifeL", "lifeT", "lifeRun"].forEach(k => { if (!SAVE_KEYS.includes(k)) SAVE_KEYS.push(k); }); } catch (e) {}
    const Phi = z => 1 / (1 + Math.exp(-1.702 * z));
    const pc = (x, med, sig, better = 1) => { if (!(x > 0) || !(med > 0)) return null; const z = Math.log(x / med) / sig * better; return Math.max(3, Math.min(97, Math.round(Phi(z) * 100))); };
    const fmt = n => Math.round(n).toLocaleString("en-US");
    const life = () => { try { return JSON.parse(localStorage.getItem("capy-life") || "{}"); } catch (e) { return {}; } };
    function track() { const L = life(); L.k = (L.k || 0) + (S.kills || 0) - (S.lifeK || 0); L.l = (L.l || 0) + (S.lines || 0) - (S.lifeL || 0); L.t = (L.t || 0) + (S.playT || 0) - (S.lifeT || 0);
      if (!S.lifeRun) { S.lifeRun = 1; L.r = (L.r || 0) + 1; } L.w = (L.w || 0) + 1; S.lifeK = S.kills || 0; S.lifeL = S.lines || 0; S.lifeT = S.playT || 0; try { localStorage.setItem("capy-life", JSON.stringify(L)); } catch (e) {} return L; }
    const CONT = ["South America", "Africa", "Asia", "Europe", "North America"];
    const STATS = [
      w => `${reach(w)}% of all players make it this far!`,
      w => w <= 140 ? `Only ${reach(w + 10)}% reach wave ${w + 10}. Be one of them!` : null,
      w => { const p = pc(S.playT / w, 42, 0.25, -1); return p && p >= 50 ? `You're faster than ${p}% of all players!` : null; },
      w => (S.kills || 0) >= 20 ? `${fmt(S.kills)} monsters splatted this run!` : null,
      w => { const p = pc((S.lines || 0) / w, 1.4, 0.4); return p && p >= 50 ? `More lines than ${p}% of players at wave ${w}!` : null; },
      (w, L) => (L.k || 0) >= 100 ? `Career total: ${fmt(L.k)} monsters down!` : null,
      (w, L) => (L.l || 0) >= 50 ? `Career total: ${fmt(L.l)} lines sunk!` : null,
      (w, L) => (L.t || 0) >= 600 ? `${Math.floor(L.t / 3600)}h ${Math.floor(L.t % 3600 / 60)}m with the squad so far!` : null,
      (w, L) => (L.r || 0) >= 2 ? `Run number ${L.r} – real veteran material!` : null,
      w => { const n = S.towers ? S.towers.size : 0; if (!n) return null; const p = pc((S.kills || 0) / n / w, expK(w) / Math.min(8, 1 + w / 6), 0.45); return p && p >= 50 ? `Your towers hit harder than ${p}% of squads!` : null; },
      w => { const lost = Math.max(0, (G.lives || 15) - (S.lives || 0)), med = 0.5 + w / 25, p = Math.max(3, Math.min(97, Math.round(Phi((med - lost) / (1 + w / 30)) * 100))); return p >= 50 ? `Fewer leaks than ${p}% of players!` : null; },
      w => (S.lives || 0) > 0 ? `${S.lives} lives left – keep the ring tight!` : null,
      w => { const b = getBest(MODE); return b > w ? `Your best is wave ${b}. ${b - w} to go!` : null; },
      w => { const b = getBest(MODE); return b && w > b ? `New personal best – wave ${w}!` : null; },
      w => { const m = (S.playT || 0) / 60; if (m < 2) return null; const k = (S.kills || 0) / m, p = pc(k, expK(w) / 0.7, 0.35); return p && p >= 50 ? `${k.toFixed(1)} monsters a minute – top ${100 - p}%!` : null; },
      w => `Wave ${w} of 150 – ${Math.round(w / 1.5)}% of the world tour done!`,
      w => { const c = Math.min(5, Math.floor((w - 1) / 30) + 1); return c >= 2 ? `${c} of 5 continents reached!` : null; },
      w => { const n = S.towersBuilt || 0; if (!n) return null; const p = pc(n, Math.min(8, 1 + w / 6), 0.4); return p && p >= 50 ? `You build faster than ${p}% of players!` : null; },
      w => (S.medals || 0) >= 1 ? `${S.medals} medal${S.medals > 1 ? "s" : ""} – more than ${pc(S.medals + 0.5, 1.6, 0.6) || 50}% at this wave!` : null,
      w => { const a = (S.playT || 0) / w; return a > 5 ? `Your average wave: ${Math.round(a)} s. Squad average: 42 s.` : null; },
      w => (S.lines || 0) >= 5 ? `${fmt(S.lines)} lines this run – ${((S.lines || 0) / w).toFixed(1)} per wave!` : null,
      w => w <= 140 ? `The next 10 waves? ${Math.round(reach(w + 10) / reach(w) * 100)}% of squads survive them.` : null,
      w => w >= 5 ? `${Math.floor(w / 5)} places cleared on the map!` : null,
      w => { const n = S.towers ? S.towers.size : 0, a = Math.round(Math.min(8, 1 + w / 6)); return n ? `${n} tower${n > 1 ? "s" : ""} guard the ring – squad average here: ${a}.` : null; },
      w => w >= 75 ? `Past halfway! ${reach(75)}% made it to wave 75.` : null,
      w => { const a = pc(S.playT / w, 42, 0.25, -1) || 50, b = pc((S.lines || 0) / w, 1.4, 0.4) || 50, p = Math.round((a + b) / 2); return p >= 60 ? `Top ${100 - p}% overall – the General is impressed!` : null; },
      w => (S.kills || 0) >= 30 && S.playT > 60 ? `One splat every ${(S.playT / S.kills).toFixed(1)} seconds!` : null,
      w => { const c = Math.floor((w - 1) / 30); if (c >= 4) return null; const nx = (c + 1) * 30 + 1; return nx - w <= 12 ? `${reach(nx)}% of squads make it to ${CONT[c + 1]}.` : null; },
      w => `Only ${reach(150)}% finish all 150 waves. Will you?`,
      (w, L) => (L.w || 0) >= 20 ? `${fmt(L.w)} waves cleared in your career!` : null,
    ];
    window.__genStat = () => { if (!S || S.nuts || S.testRun0) return null; const L = track(), w = S.wave || 1;
      if (!S.statNext) S.statNext = w + 4 + Math.floor(Math.random() * 2);   // erste Statistik nach Welle 5–6
      if (w < S.statNext) return null;
      S.statNext = w + 5 + Math.floor(Math.random() * 2);
      let seen = S.statSeen || []; if (seen.length >= STATS.length - 3) seen = [];
      const order = STATS.map((f, i) => i).filter(i => !seen.includes(i)).sort(() => Math.random() - 0.5);
      for (const i of order) { let t = null; try { t = STATS[i](w, L); } catch (e) {} if (t) { seen.push(i); S.statSeen = seen; return t; } }
      return null; };
    window.__TT && (window.__TT.announce = announce); window.__TT && (window.__TT.stats = { list: () => { const L = life(), w = S.wave || 1; return STATS.map((f, i) => { try { return i + ": " + f(w, L); } catch (e) { return i + ": ERR " + e.message; } }); } });
  })(); } catch (e) { console.error("genStat", e); }
'''
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
