#!/bin/bash
# Aufruf: capy_patch_deploy.sh NNN "Commit-Text" [erwarteter sha16]
set -e
N=$1; MSG=$2; EXP=$3
cd /srv/capy-assets
export GIT_SSH_COMMAND="ssh -i /root/.ssh/capy_deploy"
cp tools/patch$N.py /tmp/p$N.py
git fetch -q && git reset -q --hard origin/main
cp /tmp/p$N.py tools/patch$N.py
python3 tools/patch$N.py site/index.html site/index.html
SHA=$(sha256sum site/index.html | cut -c1-16); echo "sha $SHA"
if [ -n "$EXP" ] && [ "$EXP" != "$SHA" ]; then echo "SHA ABWEICHUNG"; git checkout -q site/index.html; exit 1; fi
python3 tools/make_offline.py site >/dev/null
git add -A tools/patch$N.py tools/lang$N.py site 2>/dev/null || git add -A tools/patch$N.py site
git commit -qm "$MSG

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_019cECXEjT3HZuLYxLFQjn5E"
git push -q
rsync -a --exclude logos site/ /srv/site/www/
bash /root/deploy_ru.sh >/dev/null
sleep 1
echo "com $(curl -s https://playcapybarasquad.com/index.html | grep -o 'GAME_VER = "[^"]*"')"
echo "ru  $(curl -s https://capybarasquad.ru/index.html | grep -o 'GAME_VER = "[^"]*"')"
