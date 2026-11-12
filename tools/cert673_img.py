# V673: Diplom-Bilder – zweiten Strich + Stempel aus dem Papier entfernen, Stempel als eigenes Bild (stamp_us/ru.webp)
from PIL import Image; import numpy as np, cv2
def save_stamp(a, bg, m, box, name, ink=None):
    x0,y0,x1,y1 = box; A=a[y0:y1,x0:x1].astype(float); B=bg[y0:y1,x0:x1].astype(float)
    dark=(B.mean(2)-A.mean(2)).clip(0); dark[dark<6]=0; dark[m[y0:y1,x0:x1]==0]=0
    if ink is None: ink=A[dark>dark.max()*0.6].mean(0)
    al=(dark/(B.mean(2)-np.mean(ink)).clip(20)).clip(0,1)
    Image.fromarray(np.dstack([np.broadcast_to(np.array(ink),A.shape).astype(np.uint8),(al*255).astype(np.uint8)]),'RGBA').save(f'site/img/{name}',lossless=True)
# US
a=np.asarray(Image.open('site/img/cert_us.webp').convert('RGB')).copy(); g=a.astype(int).sum(2)
m=np.zeros(a.shape[:2],np.uint8); m[690:806,488:608]=(g[690:806,488:608]<700)*255; m[825:834,465:626]=255
m=cv2.dilate(m,np.ones((5,5),np.uint8)); bg=cv2.inpaint(a[:,:,::-1].copy(),m,7,cv2.INPAINT_TELEA)[:,:,::-1]
m2=m.copy(); m2[825:834,465:626]=0
save_stamp(a,bg,m2,(488,690,608,806),'stamp_us.webp'); Image.fromarray(bg).save('site/img/cert_us.webp',quality=90,method=6)
# RU
a=np.asarray(Image.open('site/img/cert_ru.webp').convert('RGB')).copy()
m=np.zeros(a.shape[:2],np.uint8); cv2.ellipse(m,(529,774),(84,83),0,0,360,255,-1)
bg=cv2.inpaint(a[:,:,::-1].copy(),m,9,cv2.INPAINT_TELEA)[:,:,::-1]
save_stamp(a,bg,m,(445,690,614,858),'stamp_ru.webp'); Image.fromarray(bg).save('site/img/cert_ru.webp',quality=90,method=6)
print("img ok")
