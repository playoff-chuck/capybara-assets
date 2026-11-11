#!/bin/bash
# Martin 11.11.2026: Datenbank bleibt in Russland (Backup dort lokal). Nach Finnland (Hetzner) nur CODE/Konfiguration,
# nachts 03:03 MSK. Keine Datenbank, keine personenbezogenen Daten. Neue Fassung nur, wenn sich etwas geändert hat; 30 Fassungen.
set -e
K="-i /root/.ssh/ru_server -o BatchMode=yes -o ConnectTimeout=20"
B=/srv/backup/ru-code; T=$(date +%Y%m%d-%H%M); N=$B/tmp-$T
mkdir -p $N
rsync -a -e "ssh $K" root@177.177.219.65:/srv/capy-api/app.py root@177.177.219.65:/srv/capy-api/csfilter.py $N/ 
rsync -a -e "ssh $K" root@177.177.219.65:/etc/caddy/Caddyfile $N/
rsync -a -e "ssh $K" --include='capy*' --exclude='*' root@177.177.219.65:/etc/systemd/system/ $N/systemd/ || true
rsync -a -e "ssh $K" --include='*.sh' --exclude='*' root@177.177.219.65:/usr/local/bin/ $N/bin/ || true
L=$(ls -1d $B/20* 2>/dev/null | tail -1)
if [ -n "$L" ] && diff -rq $L $N >/dev/null; then rm -rf $N; echo "$T unverändert"; else mv $N $B/$T; echo "$T neue Fassung"; fi
ls -1d $B/20* | head -n -30 | xargs -r rm -rf
