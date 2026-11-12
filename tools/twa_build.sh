#!/bin/bash
# Baut die Play-Store-App (TWA) für playcapybarasquad.com: Upload-Schlüssel (einmalig), Projekt, .aab + .apk
set -e
cd /srv/twa
LOG=/srv/twa/build.log; exec >> $LOG 2>&1; echo "== build $(date)"
export ANDROID_HOME=/srv/twa/android-sdk JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))
mkdir -p ~/.bubblewrap
echo "{\"jdkPath\":\"$JAVA_HOME\",\"androidSdkPath\":\"$ANDROID_HOME\"}" > ~/.bubblewrap/config.json
# 1) Upload-Schlüssel einmalig anlegen (Passwort nur auf dem Server, root-only)
if [ ! -f /etc/splatsquad/twa.pass ]; then umask 077; head -c 24 /dev/urandom | base64 | tr -d '/+=' > /etc/splatsquad/twa.pass; fi
PW=$(cat /etc/splatsquad/twa.pass)
if [ ! -f /srv/twa/upload.jks ]; then
  keytool -genkeypair -v -keystore /srv/twa/upload.jks -alias capyupload -keyalg RSA -keysize 2048 -validity 10000 \
    -storepass "$PW" -keypass "$PW" -dname "CN=Capybara Squad, O=ChuckVC, C=AT"
  chmod 600 /srv/twa/upload.jks
fi
# 2) Projekt erzeugen
GL=$(npm root -g)
cat > gen.js <<'EOF'
const path = require('path');
const core = require(path.join(process.env.GL, '@bubblewrap/cli/node_modules/@bubblewrap/core'));
(async () => {
  const m = await core.TwaManifest.fromWebManifest('https://playcapybarasquad.com/manifest.webmanifest');
  m.packageId = 'com.playcapybarasquad.app';
  m.host = 'playcapybarasquad.com';
  m.name = 'Capybara Squad'; m.launcherName = 'Capybara Squad';
  m.startUrl = '/';
  m.iconUrl = 'https://playcapybarasquad.com/icons/icon-512.png'; m.maskableIconUrl = 'https://playcapybarasquad.com/icons/icon-maskable-512.png';   // V654: aktuelles Logo C1 (Manifest nennt jetzt das freigestellte Splash-Logo)
  m.appVersionCode = parseInt(process.env.VCODE || '1'); m.appVersionName = process.env.VNAME || '1.0.0';
  m.orientation = 'portrait'; m.display = 'standalone';
  m.enableNotifications = false; m.fallbackType = 'customtabs';
  m.signingKey = { path: '/srv/twa/upload.jks', alias: 'capyupload' };
  m.shortcuts = [];
  m.minSdkVersion = 24;
  await m.saveToFile('/srv/twa/twa-manifest.json');
  const g = new core.TwaGenerator();
  await g.createTwaProject('/srv/twa/app', m, new core.ConsoleLog('gen'));
  console.log('PROJECT OK');
})().catch(e => { console.error('GENFAIL', e); process.exit(1); });
EOF
rm -rf /srv/twa/app; mkdir -p /srv/twa/app
GL=$GL node gen.js
python3 /srv/capy-assets/tools/make_splash.py /srv/capy-assets/site /srv/twa/app/app/src/main/res   # V326: Startbild = Titelbild statt Icon
# 3) Bauen
cd /srv/twa/app
cp /srv/twa/twa-manifest.json .
printf "n\n" | BUBBLEWRAP_KEYSTORE_PASSWORD="$PW" BUBBLEWRAP_KEY_PASSWORD="$PW" bubblewrap build --skipPwaValidation --manifest=/srv/twa/app/twa-manifest.json
ls -la /srv/twa/app/*.aab /srv/twa/app/*.apk
# 4) Fingerabdruck für assetlinks.json
keytool -list -v -keystore /srv/twa/upload.jks -alias capyupload -storepass "$PW" | grep "SHA256:"
echo BUILDDONE
