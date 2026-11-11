#!/usr/bin/env python3
# V618 (Martin 11.11. 12:45–12:50):
# 1) Begrüßung «Willkommen in Südamerika» (Spruch welcome, Martins Stimme) fehlte beim ersten Anflug – im Kurs (TUT.on) waren nur Lob-Sprüche erlaubt. welcome jetzt erlaubt.
# 2) Diplom-Tusch ohne Rauschen (Rausch-Becken und Rausch-Pauken entfernt, bis die Suno-Fanfare kommt).
# 3) Musik: bei allem, was das Spiel anhält (Tipps, Kurs-/General-Karten, Meldungen, Pause), 2 s ganz ausblenden; nach OK in 1,5 s wieder einblenden, Stück läuft weiter. Diplom ausgenommen.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V617";', 'const GAME_VER = "V618";')
rep('window.__tutKeys = new Set(TUT_PRAISE);', 'window.__tutKeys = new Set(TUT_PRAISE); window.__tutKeys.add("welcome");   /* V618: Begrüßung Südamerika im Kurs */')
rep('  for (let i = 0; i < 10; i++) noise(t0 + i * 0.045, 0.09, 0.22 + i * 0.03, "lowpass", 180);   /* Pauken-Wirbel */\n', '')
rep('  noise(t0 + 0.96, 1.6, 0.35, "highpass", 5000); noise(t0 + 0.96, 0.35, 0.6, "lowpass", 120);   /* Becken + Pauke */\n', '')
# Musik ausblenden/einblenden
rep('!S.mapShow && !S.tiltCard && !S.coachHold);', '!S.mapShow && !S.tiltCard && !window.__tutSumOpen && !window.__certFade);   /* V618: auch bei Kurs-/General-Karten ausblenden */')
rep('if (pz) { tpFade(0.0001, 1.5); setTimeout(() => { if (TP.paused) TP.el.pause(); }, 1600); } else { const p = TP.el.play(); if (p && p.catch) p.catch(() => {}); tpFade(0.5, 0.6); } return; }',
    'if (pz) { tpFade(0.0001, 2); setTimeout(() => { if (TP.paused) TP.el.pause(); }, 2100); } else { const p = TP.el.play(); if (p && p.catch) p.catch(() => {}); tpFade(0.5, 1.5); } return; }   /* V618: 2 s aus, 1,5 s ein */')
rep('bus.gain.exponentialRampToValueAtTime(pz ? 0.0001 : LVL * sonarLvl, ac.currentTime + (pz ? 1.5 : 0.25));',
    'bus.gain.exponentialRampToValueAtTime(pz ? 0.0001 : LVL * sonarLvl, ac.currentTime + (pz ? 2 : 1.5));   /* V618 */')
open(p, "w", encoding="utf-8").write(s)
print("ok V618")
