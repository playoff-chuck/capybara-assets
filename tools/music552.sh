#!/bin/sh
# V552: Musik schlanker und Android-sicher – Südamerika-Stücke 96 kHz → 44,1 kHz, Nuts-Stücke 131 → 96 kbit/s (AAC, faststart)
# Aufruf im Repo-Wurzelverzeichnis: sh tools/music552.sh
set -e
cd site/music
for f in airport_bossa andes_lounge copacabana_sunset samba_lounge rumba_lounge lounge_disco jungle_downtempo chill_disco_rio nz_grumblefang nz_anthem nz_skullgrog nz_gorkazar nz_frostgnaw; do
  ffmpeg -nostdin -loglevel error -y -i "$f.mp4" -vn -map_metadata -1 -c:a aac -b:a 96k -ar 44100 -ac 2 -movflags +faststart "/tmp/$f.552.mp4"
  mv "/tmp/$f.552.mp4" "$f.mp4"
done
echo done
