#!/bin/bash
# Megatest-Ablauf (Martin 12.11. 23:29 MV): Leistung → P1 W1-30 → P2 W31-60 → P3 W61-90 → P4 W91-150 → P5 Nuts L1-15 → P6 Nuts L16-30 → Gesamtbericht.
# Je Phase 3 Spuren parallel. Fertige Läufe (Datei done) werden beim Neustart übersprungen. Nach 02:05 UTC keine neuen Läufe.
cd /root/megatest; export SITE=/root/megatest/site; R=/root/megatest/runs; mkdir -p $R; ST=$R/status.txt
DEAD=$(date -u -d 'tomorrow 02:05' +%s); [ $(date -u +%H) -lt 12 ] && DEAD=$(date -u -d 'today 02:05' +%s)
log(){ echo "$(date -u +%H:%M) $*" >> $ST; }
run(){ # name gruppe sprache von bis nuts(-) tmax
  local n=$1; [ -f $R/$n/done ] && return
  if [ $(date -u +%s) -gt $DEAD ]; then log "übersprungen $n (Zeit)"; return; fi
  log "start $n"; local NZ=$6; [ "$NZ" = "-" ] && NZ=""
  NUTS=$NZ TMAX=$7 python3 megatest.py $2 $4 $5 $R/$n $3 > $R/$n.log 2>&1
  mkdir -p $R/$n; touch $R/$n/done; log "fertig $n: $(tail -n 1 $R/$n.log | cut -c1-120)"; }
phase(){ local p=$1; shift; [ -f $R/$p.done ] && return; log "PHASE $p START"
  for track in "$@"; do ( IFS=';'; for spec in $track; do IFS=' '; run $spec; done ) & done; wait
  python3 report.py $p >> $ST 2>&1; touch $R/$p.done; log "PHASE $p FERTIG"; }
[ -f perf.json ] || { log "Leistungsprobe START"; python3 perfprobe.py $SITE perf.json > $R/perf.log 2>&1; log "Leistungsprobe fertig"; }
[ -f static.json ] || python3 static_checks.py $SITE static.json > $R/static.log 2>&1
phase p1 "p1_G3_en 3 en 1 30 - 35" "p1_G1_ru 1 ru 1 30 - 35" "p1_G5_es 5 es 1 30 - 35"
phase p2 "p2_G3_en 3 en 31 60 - 40" "p2_G1_ru 1 ru 31 60 - 40" "p2_G6_pt 6 pt 31 60 - 40"
phase p3 "p3_G3_en 3 en 61 90 - 45" "p3_G1_ru 1 ru 61 90 - 45" "p3_G7_ru 7 ru 61 90 - 45"
phase p4 "p4_G3_en 3 en 91 150 - 80" "p4_G1_ru 1 ru 91 150 - 80" "p4_G2_es 2 es 91 150 - 80"
phase p5 "p5_G3_en_c0 3 en 1 15 0 25;p5_G3_en_c1 3 en 1 15 1 25" "p5_G1_ru_c2 1 ru 1 15 2 25;p5_G1_ru_c3 1 ru 1 15 3 25" "p5_G4_pt_c4 4 pt 1 15 4 25"
phase p6 "p6_G3_en_c0 3 en 16 30 0 25;p6_G3_en_c1 3 en 16 30 1 25" "p6_G1_ru_c2 1 ru 16 30 2 25;p6_G1_ru_c3 1 ru 16 30 3 25" "p6_G4_pt_c4 4 pt 16 30 4 25"
python3 report.py all >> $ST 2>&1; log "ALLE FERTIG"
