#!/usr/bin/env python3
"""Google Play: App-Bundle in einen Test-Track hochladen (Dienstkonto aus /srv/capy-api/secret/play-sa.json).
  python3 /root/play_release.py check                 -> Zugang prüfen, Tracks auflisten
  python3 /root/play_release.py promote VC TRACK     -> vorhandene Version in Track (z. B. alpha)
  python3 /root/play_release.py upload AAB [TRACK]     -> hochladen + veröffentlichen (TRACK: internal|alpha, Standard internal)
Schlüssel wird nie ausgegeben.
"""
import base64, json, sys, time, urllib.request, urllib.parse
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
PKG = "com.playcapybarasquad.app"
SA = json.load(open("/srv/capy-api/secret/play-sa.json"))
API = "https://androidpublisher.googleapis.com/androidpublisher/v3/applications/" + PKG
UP = "https://androidpublisher.googleapis.com/upload/androidpublisher/v3/applications/" + PKG
def b64(b): return base64.urlsafe_b64encode(b).rstrip(b"=")
def token():
    now = int(time.time())
    h = b64(json.dumps({"alg": "RS256", "typ": "JWT"}).encode()); c = b64(json.dumps({"iss": SA["client_email"], "scope": "https://www.googleapis.com/auth/androidpublisher", "aud": SA["token_uri"], "iat": now, "exp": now + 3000}).encode())
    k = serialization.load_pem_private_key(SA["private_key"].encode(), None)
    sig = b64(k.sign(h + b"." + c, padding.PKCS1v15(), hashes.SHA256()))
    d = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": (h + b"." + c + b"." + sig).decode()}).encode()
    return json.load(urllib.request.urlopen(urllib.request.Request(SA["token_uri"], d)))["access_token"]
TOK = None
def call(method, url, body=None, ctype="application/json", raw=None):
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data, method=method, headers={"Authorization": "Bearer " + TOK, "Content-Type": ctype})
    try: return json.load(urllib.request.urlopen(r, timeout=300))
    except urllib.error.HTTPError as e: print("HTTP", e.code, e.read().decode()[:600]); sys.exit(1)
a = sys.argv[1:]
TOK = token()
ed = call("POST", API + "/edits", {})["id"]
if a[0] == "check":
    print("Zugang ok:", SA["client_email"])
    for t in call("GET", API + f"/edits/{ed}/tracks").get("tracks", []):
        print(t["track"], [(r.get("name"), r.get("versionCodes"), r.get("status")) for r in t.get("releases", [])])
    call("DELETE", API + f"/edits/{ed}") if False else None
elif a[0] == "promote":   # vorhandene Version (versionCode) in anderen Track: promote VC TRACK
    vc, track = a[1], a[2]
    call("PUT", API + f"/edits/{ed}/tracks/{track}", {"track": track, "releases": [{"versionCodes": [str(vc)], "status": "completed"}]})
    print("commit", call("POST", API + f"/edits/{ed}:commit").get("id")); print("fertig: Track", track, "versionCode", vc)
elif a[0] == "upload":
    aab, track = a[1], (a[2] if len(a) > 2 else "internal")
    b = call("POST", UP + f"/edits/{ed}/bundles?uploadType=media", raw=open(aab, "rb").read(), ctype="application/octet-stream")
    vc = b["versionCode"]; print("hochgeladen versionCode", vc)
    call("PUT", API + f"/edits/{ed}/tracks/{track}", {"track": track, "releases": [{"versionCodes": [str(vc)], "status": "completed"}]})
    print("commit", call("POST", API + f"/edits/{ed}:commit").get("id")); print("fertig: Track", track)
