#!/bin/sh
# Tägliche Sicherung der russischen Spielerdaten auf den Hetzner-Server (14 Tage aufbewahren)
set -e
D=/root/backup_ru; mkdir -p $D
ssh -i /root/.ssh/ru_server -o BatchMode=yes root@177.177.219.65 'sqlite3 /srv/capy-api/data.db ".backup /tmp/ru_backup.db" && gzip -c /tmp/ru_backup.db && rm -f /tmp/ru_backup.db' > $D/data_$(date -u +%F).db.gz
find $D -name 'data_*.db.gz' -mtime +14 -delete
