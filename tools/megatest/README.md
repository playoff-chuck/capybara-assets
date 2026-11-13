# Mega-Check (Megatest) – Stand 13.11.2026

Vollständige Beschreibung im Projekt: «Capybara – Mega-Check (konsolidiert, 13.11.2026)».

Arbeitsordner auf dem Server: /root/megatest (Kopie des Spiels in ./site, Ergebnisse in ./runs).
Start: `systemd-run --unit=megatest --property=MemoryMax=3300M --property=OOMScoreAdjust=500 /root/megatest/megatest.sh`
Einzellauf: `NUTS= TMAX=35 python3 megatest.py <Gruppe 1-7> <von> <bis> <Ausgabeordner> <Sprache>`
Bericht: `python3 report.py all` → runs/report_all.md

Bekannte Bot-Fehler (vor dem nächsten Lauf beheben): Projektdokument, Abschnitt «Bot-Korrekturen».
