import json, urllib.request, sys, time
sys.path.insert(0,'/root'); import gtok
P="capybara-514506-d7d2e"; B="capy-testlab-514506"
apk='/srv/testapp/app/build/outputs/apk/debug/app-debug.apk'
name="app/capy-webtest-4.apk"
req=urllib.request.Request(f"https://storage.googleapis.com/upload/storage/v1/b/{B}/o?uploadType=media&name={name}",data=open(apk,'rb').read(),headers={'Authorization':'Bearer '+gtok.TOK,'Content-Type':'application/vnd.android.package-archive','x-goog-user-project':P},method="POST")
print("upload",urllib.request.urlopen(req,timeout=120).status)
devs=[("RE58C2","35")]
ts=time.strftime('%m%d%H%M')
body={"projectId":P,"testSpecification":{"testTimeout":"300s","androidTestLoop":{"appApk":{"gcsPath":f"gs://{B}/{name}"}}},
 "environmentMatrix":{"androidDeviceList":{"androidDevices":[{"androidModelId":m,"androidVersionId":v,"locale":"ru","orientation":"portrait"} for m,v in devs]}},
 "resultStorage":{"googleCloudStorage":{"gcsPath":f"gs://{B}/results/webtest-{ts}/"},"toolResultsHistory":{"projectId":P}},"flakyTestAttempts":0}
s,b=gtok.call("POST",f"https://testing.googleapis.com/v1/projects/{P}/testMatrices",body,qp=P)
print("matrix",s,b[:600]); open('/root/testlab_web_last.json','w').write(b)
