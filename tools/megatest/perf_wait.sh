#!/bin/bash
# Leistungsprobe erst, wenn der Megatest fertig ist (oder spätestens 01:35 UTC), damit FPS nicht durch parallele Bots verfälscht werden.
cd /root/megatest
END=$(date -u -d 'today 01:35' +%s); [ $(date -u +%H) -ge 12 ] && END=$(date -u -d 'tomorrow 01:35' +%s)
while systemctl is-active --quiet megatest && [ $(date -u +%s) -lt $END ]; do sleep 60; done
echo "$(date -u +%H:%M) Leistungsprobe (2) START" >> runs/status.txt
python3 perfprobe.py /root/megatest/site perf.json > runs/perf2.log 2>&1
echo "$(date -u +%H:%M) Leistungsprobe (2) fertig" >> runs/status.txt
python3 report.py all >> runs/status.txt 2>&1
