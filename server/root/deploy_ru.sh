#!/bin/sh
# Spiel + Datenschutz auf den russischen Server (Timeweb Nowosibirsk, capybarasquad.ru) spiegeln. Nach jedem Deploy laufen lassen.
set -e
E="ssh -i /root/.ssh/ru_server -o BatchMode=yes"
rsync -a --delete -e "$E" --exclude logos /srv/site/www/ root@177.177.219.65:/srv/site/www/
rsync -a -e "$E" /srv/site/privacy_ru/ root@177.177.219.65:/srv/site/privacy/   # RU-Fassung (152-ФЗ), Martin 11.11.
rsync -a -e "$E" /srv/capy-api/app.py /srv/capy-api/csfilter.py root@177.177.219.65:/srv/capy-api/
$E root@177.177.219.65 'systemctl restart capy-api'
echo "RU synced $(date -u +%FT%TZ)"
