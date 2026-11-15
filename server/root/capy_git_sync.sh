#!/bin/bash
# Sichert Server-Code (ohne Secrets/Daten) laufend nach GitHub (capybara-assets/server/).
set -e
R=/srv/capy-assets; cd $R
export GIT_SSH_COMMAND="ssh -i /root/.ssh/capy_deploy"
git pull -q --rebase origin main || true
mkdir -p server/api server/root server/caddy
cp /srv/capy-api/app.py /srv/capy-api/csfilter.py server/api/
for f in capy_patch_deploy.sh capy_drive.py capy_daily_stats.py capy_cleanup.py capy_tg.py capy_git_sync.sh backup_ru.sh deploy_ru.sh gtok.py play_release.py testlab_daily.py testlab_run.py testlab_web.py autoplay_check.py rec_plane.py setup.sh; do [ -f /root/$f ] && cp /root/$f server/root/; done
[ -f /etc/caddy/Caddyfile ] && cp /etc/caddy/Caddyfile server/caddy/
crontab -l > server/root/crontab.txt 2>/dev/null || true
# Secret-Sperre: bei Verdacht nichts committen
if grep -rEn --exclude=capy_git_sync.sh "(ghp_|github_pat_|sk-[A-Za-z0-9]{20}|AIza[0-9A-Za-z_-]{30}|-----BEGIN [A-Z ]*PRIVATE KEY|[0-9]{8,10}:AA[0-9A-Za-z_-]{30})" server/ ; then echo "SECRET-VERDACHT – abgebrochen"; git checkout -- server 2>/dev/null; git clean -fdq server; exit 1; fi
git add -A server
git diff --cached --quiet && { echo "nichts neu"; exit 0; }
git -c user.name="capy-server" -c user.email="capy-server@localhost" commit -qm "Server-Sicherung $(date -u +%F\ %H:%M)"
git push -q origin main && echo "gepusht"
