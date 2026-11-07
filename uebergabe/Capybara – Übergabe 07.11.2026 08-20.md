# Capybara – Übergabe 07.11.2026 08:20 (MVT)

## Status
Live V363. Seite 200, caddy/capy-api/splatmcp aktiv.
Link: https://playcapybarasquad.com

## Fertig seit letzter Übergabe
- V363: Lucky Supply bis Welle 60 um 30 % seltener (Abstand 7–10 statt 5–7 Wellen; ab Welle 60 unverändert; erster Lucky und Rettungs-Lucky unverändert). tools/patch363.py.
- Hinweis: beim ersten V363-Commit auf dem Server waren ungetrackte Dateien (gen_loop/, pro/night_v178.log, review/thief_walk/…, voice/…) mitcommittet → sofort per force-with-lease durch sauberen Commit 04b231c ersetzt. Dateien liegen weiter ungetrackt in /srv/capy-assets. Künftig NICHT `git add -A`, sondern nur `git add site tools/patchNNN.py`.

## Offen Claude (Martins Meldungen 07.11. 08:17–08:18, noch nicht umgesetzt)
1. **Musik weg (höchste Priorität, Martin: «war oft weg beim Test, bitte checken»)**: nach Lautstärke-Regeln keine Musik mehr, auch nach mehreren Neustarts; im Spiel mehrfach weg (Level 9, 13, …). Ursache klären.
   Erste Befunde im Code (Suno-Player TP, Abschnitt «Musik: Suno-Stücke»):
   - tpStop() setzt TP.stopping und pausiert per setTimeout das Audio-Element; tpPlay() setzt TP.stopping nicht zurück → kommt start/menu kurz nach stop, wird das neue Stück gleich wieder pausiert, TP.key bleibt gesetzt.
   - Neustart per Tipp greift nur bei `SFX.music.playing < 1`; mit gesetztem TP.key ist playing ≥ 1 → hängendes, pausiertes Element wird nie neu gestartet. Fix-Idee: in tpPlay TP.stopping=false; Wächter: TP.key && !TP.paused && el.paused → play().
   - Lautstärke: TP_VOL = vol² · ch("m")² …; Werte in localStorage tarnturm-vol / tarnturm-ch / tarnturm-mute / tarnturm-music. Prüfen, ob Regler (Pause-Menü pVol, data-ch="all|m|f|v", Kopf-Regler #vol) 0 oder Mute speichert, das nach Neustart bleibt.
2. Flugzeug: erste Sequenz läuft zweimal – bei ALLEN Flügen prüfen.
3. Flugzeug nach Afrika fliegt falschen Punkt an.
4. Während Tutorial / Ideengeber das Spiel im Hintergrund anhalten.
5. Pokal im Hauptmenü: das Fenster, das sich öffnet, stimmt nicht (prüfen und richten; Regel: nichts darf sich verschieben).
6. Zu Martins Stimme immer nur Blue zeigen, nie Rosie (derzeit «meine Stimme + Rosie»).
7. Prüfen, ob die neuen Rosie-/Blue-Meldungen andere Meldungen verdrängen.
8. **Konsolidiere alle Regeln und Abläufe**: Übergaben, «Ablauf-Regeln Fenster & Anzeigen», alle «Entscheidungen …», «Tarnturm – Spielregeln & Entscheidungen», /neu-Arbeitsregeln → ein Dokument «Capybara – Regelwerk», ohne Widersprüche, neueste Entscheidung gilt, Alt-Dateien als überholt markieren. V363 (Lucky seltener) mit aufnehmen.

## Offen Martin
- nichts Neues

## Arbeitsweise
- Nach Skill /neu (Repo playoff-chuck/capybara-assets, Patch-Ablauf, Playwright 412×915, Splat_Server).
- Commit auf dem Server nur gezielt: `git add site tools/patchNNN.py` (kein `git add -A`).
