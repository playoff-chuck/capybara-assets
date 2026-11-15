import base64,json,time,urllib.request,urllib.parse
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
def token(scope="https://www.googleapis.com/auth/cloud-platform"):
    SA=json.load(open('/srv/capy-api/secret/play-sa.json'))
    b64=lambda b: base64.urlsafe_b64encode(b).rstrip(b"=")
    now=int(time.time())
    h=b64(json.dumps({"alg":"RS256","typ":"JWT"}).encode()); c=b64(json.dumps({"iss":SA["client_email"],"scope":scope,"aud":SA["token_uri"],"iat":now,"exp":now+3000}).encode())
    k=serialization.load_pem_private_key(SA["private_key"].encode(),None)
    sig=b64(k.sign(h+b"."+c,padding.PKCS1v15(),hashes.SHA256()))
    d=urllib.parse.urlencode({"grant_type":"urn:ietf:params:oauth:grant-type:jwt-bearer","assertion":(h+b"."+c+b"."+sig).decode()}).encode()
    return json.load(urllib.request.urlopen(urllib.request.Request(SA["token_uri"],d)))["access_token"]
def call(method,url,body=None,qp=None):
    h={'Authorization':'Bearer '+TOK,'Content-Type':'application/json'}
    if qp: h['x-goog-user-project']=qp
    try:
        r=urllib.request.urlopen(urllib.request.Request(url,data=json.dumps(body).encode() if body is not None else None,headers=h,method=method),timeout=60); return r.status, r.read().decode()
    except Exception as e: return getattr(e,'code',0), (e.read().decode() if hasattr(e,'read') else str(e))
TOK=token()
