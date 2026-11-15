import time, json, urllib.request, importlib, sys
sys.path.insert(0,'/root'); import gtok
P="capybara-514506-d7d2e"; B="test-lab-t2mdnq3n89654-w4dkfin5kuzdc"
data=open('/srv/twa/app/app-release-signed.apk','rb').read()
for i in range(30):
    importlib.reload(gtok)
    try:
        urllib.request.urlopen(urllib.request.Request(f"https://storage.googleapis.com/upload/storage/v1/b/{B}/o?uploadType=media&name=app/capy-1.0.2.apk",data=data,headers={'Authorization':'Bearer '+gtok.TOK,'Content-Type':'application/vnd.android.package-archive'},method="POST"),timeout=120)
        print(time.strftime('%H:%M'),"upload ok",flush=True); break
    except Exception as e:
        print(time.strftime('%H:%M'),"upload",getattr(e,'code',e),flush=True); time.sleep(60)
else: sys.exit(1)
devs=[("F01L","27"),("a10","29"),("aruba","30"),("TECNO-BF6","31"),("a12","31")]
body={"projectId":P,"testSpecification":{"testTimeout":"300s","androidRoboTest":{"appApk":{"gcsPath":f"gs://{B}/app/capy-1.0.2.apk"}}},
 "environmentMatrix":{"androidDeviceList":{"androidDevices":[{"androidModelId":m,"androidVersionId":v,"locale":"en","orientation":"portrait"} for m,v in devs]}},
 "resultStorage":{"googleCloudStorage":{"gcsPath":f"gs://{B}/results/1.0.2/"},"toolResultsHistory":{"projectId":P}},"flakyTestAttempts":0}
s,b=gtok.call("POST",f"https://testing.googleapis.com/v1/projects/{P}/testMatrices",body,qp=P)
print("matrix",s,b[:800],flush=True); open('/root/testlab_last.json','w').write(b)
