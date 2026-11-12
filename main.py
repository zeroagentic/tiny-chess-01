V={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':0,'.':0};CAP=18000
DR={'N':(-33,-31,-18,-14,14,18,31,33),'B':(-17,-15,15,17),'R':(-16,-1,1,16)};DR['Q']=DR['K']=DR['B']+DR['R']
class TO(Exception):pass
def P(fen):
 b=['.']*128;pt=fen.split()
 r=f=0
 for ch in pt[0]:
  if ch=='/':r+=1;f=0
  elif ch.isdigit():f+=int(ch)
  else:b[r*16+f]=ch;f+=1
 ep=-1 if pt[3:4]in(['-'],[]) else (8-int(pt[3][1]))*16+ord(pt[3][0])-97
 return [b,len(pt)<2 or pt[1]=='w',(pt[2:]+[''])[0],ep]
def atk(b,sq,byw):
 for d in (15,17):
  j=sq+d if byw else sq-d
  if not j&0x88 and b[j]==('P' if byw else 'p'):return 1
 for u,ds in DR.items():
  ps={'B':'BQ','R':'RQ'}.get(u,u);sl=u not in 'NK'
  for d in ds:
   j=sq+d
   while not j&0x88:
    p=b[j]
    if p!='.':
     if p.isupper()==byw and p.upper() in ps:return 1
     break
    if not sl:break
    j+=d
 return 0
def kgm(s):return s[0].index('k' if s[1] else 'K')
def gen(s):
 b,w,c,ep=s;ms=[]
 for i,p in enumerate(b):
  if p=='.' or i&0x88 or p.isupper()!=w:continue
  u=p.upper()
  if u=='P':
   d=-16 if w else 16;tg=[]
   if b[i+d]=='.':
    tg.append(i+d)
    if (i//16==(6 if w else 1)) and b[i+2*d]=='.':ms.append((i,i+2*d,''))
   for df in (-1,1):
    t=i+d+df
    if not t&0x88 and (b[t]!='.' and b[t].isupper()!=w or t==ep):tg.append(t)
   for t in tg:
    if t<16 or t>=112:
     for q in 'QRBN':ms.append((i,t,q if w else q.lower()))
    else:ms.append((i,t,''))
  else:
   for d in DR[u]:
    j=i+d
    while not j&0x88:
     q=b[j]
     if q=='.':ms.append((i,j,''))
     else:
      if q.isupper()!=w:ms.append((i,j,''))
      break
     if u in 'NK':break
     j+=d
 K='K' if w else 'k';ks=116 if w else 4
 if b[ks]==K:
  rt=('K','Q') if w else ('k','q')
  for r_,sg in((rt[0],1),(rt[1],-1)):
   if r_ in c and all(b[ks+k*sg]=='.' for k in ((1,2) if sg>0 else (1,2,3))) and not any(atk(b,ks+k*sg,not w) for k in (0,1,2)):ms.append((ks,ks+2*sg,''))
 return ms
def mk(s,m):
 b=s[0];fr,to,pr=m;p=b[fr]
 if p in 'Pp' and to==s[3] and b[to]=='.' and fr%16!=to%16:b[to+(16 if s[1] else -16)]='.'
 b[to]=pr if pr else p;b[fr]='.'
 if p in 'Kk' and abs(to-fr)==2:
  rf,rt=(fr+3,fr+1) if to>fr else (fr-4,fr-1);b[rt]=b[rf];b[rf]='.'
 s[3]=(fr+to)//2 if p.upper()=='P' and abs(to-fr)==32 else -1
 RM={116:'KQ',4:'kq',119:'K',112:'Q',7:'k',0:'q'}
 for ch in RM.get(fr,'')+RM.get(to,''):s[2]=s[2].replace(ch,'')
 s[1]=not s[1]
def cp(s):return s[0][:],s[1],s[2],s[3]
def un(s,u):s[0][:],s[1],s[2],s[3]=u
def ev(s):
 b,w=s[0],s[1];sc=0
 for i,p in enumerate(b):
  if p=='.' or i&0x88:continue
  u=p.upper();v=V[u]
  if u=='N':v+=(min(i%16,7-i%16)+min(i//16,7-i//16))*6-12
  sc+=v if p.isupper() else -v
 return sc if w else -sc
nd=0;BM=[None]
def sr(s,d,al,be,ply):
 global nd;nd+=1
 if nd>CAP:raise TO
 if d<=0:
  al=max(al,ev(s))
  if al>=be:return be
  for m in [m for m in gen(s) if s[0][m[1]]!='.' or m[2]]:
   u=cp(s);mk(s,m)
   if atk(s[0],kgm(s),s[1]):un(s,u);continue
   sc=-sr(s,-1,-be,-al,ply+1);un(s,u)
   if sc>=be:return be
   al=max(al,sc)
  return al
 ms=gen(s)
 ms.sort(key=lambda m:-V[s[0][m[1]].upper()])
 best=-999999;bm=None
 for m in ms:
  u=cp(s);mk(s,m)
  if atk(s[0],kgm(s),s[1]):un(s,u);continue
  sc=-sr(s,d-1,-be,-al,ply+1);un(s,u)
  if sc>best:best,bm=sc,m
  al=max(al,sc)
  if al>=be:break
 if bm is None:return -100000+ply if atk(s[0],s[0].index(('k','K')[s[1]]),not s[1]) else 0
 if ply==0:BM[0]=bm
 return best
def muci(m):
 f=lambda i:chr(97+i%16)+str(8-i//16)
 return f(m[0])+f(m[1])+(m[2].lower() if m[2] else '')
def best(s):
 global nd;nd=0;bm=None;d=1
 while d<13:
  try:sr(s,d,-999999,999999,0)
  except TO:break
  bm=BM[0] or bm
  d+=1
 return bm
def run():
 import json as J,os,urllib.request as U
 url=os.getenv('MAKEFUN_ENV_URL')
 def post(p,b):
  return J.loads(U.urlopen(U.Request(url+p,data=J.dumps(b).encode())).read())
 while (g:=post('/game',{})).get('status')!='done':
  while g.get('status')=='your_move':
   m=best(P(g['fen']));u=muci(m) if m else '0000'
   if u not in g.get('legal_moves',[u]):u=sorted(g['legal_moves'])[0]
   g=post('/move',{'game':g['game'],'move':u})
if __name__=='__main__':run()
