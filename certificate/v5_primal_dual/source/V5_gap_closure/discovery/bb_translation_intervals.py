# Integer outward interval discovery for the complete translated-IC objective.
from pathlib import Path
from fractions import Fraction as F
from heapq import heappush,heappop
import json,time,sys
ROOT=Path(__file__).resolve().parents[1]
S=1<<60
def const(q):
    q=F(q)*S
    return q.numerator//q.denominator,-((-q.numerator)//q.denominator)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    if a[0]>=0 and b[0]>=0:v,w=a[0]*b[0],a[1]*b[1]
    elif a[1]<=0 and b[0]>=0:v,w=a[0]*b[1],a[1]*b[0]
    elif b[1]<=0 and a[0]>=0:v,w=a[1]*b[0],a[0]*b[1]
    else:
        z=[a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1]];v,w=min(z),max(z)
    return v//S,-((-w)//S)
def inv(a):
    assert a[0]>0
    return S*S//a[1],-((-S*S)//a[0])
def tree(poly,axis=0):
    if axis==4:return const(poly.get((0,0,0,0),F()))
    deg=max((e[axis] for e in poly),default=0)
    nodes=[]
    for n in range(deg,-1,-1):
        pp={}
        for e,c in poly.items():
            if e[axis]==n:
                key=list(e);key[axis]=0;pp[tuple(key)]=c
        nodes.append(tree(pp,axis+1))
    return tuple(nodes)
def ev(tr,box,axis=0):
    if axis==4:return tr
    v=ev(tr[0],box,axis+1)
    for branch in tr[1:]:v=add(mul(v,box[axis]),ev(branch,box,axis+1))
    return v
data=json.loads((ROOT/'discovery/bb_centered_fields.json').read_text())
TREES=[[tree({tuple(e):F(c) for e,c in p}) for p in row] for row in data['corrections']]
CENTERS=[[const(c) for c in cc] for cc in data['centers']]
HALFS=[const(h) for h in data['halfwidths']]
ONEHALF=const(F(1,2));THREEHALF=const(F(3,2))
VOL=F(3,20)*F(3,10)*F(9,50)*F(13,20)
def fields(box,site):
    coord=[add(CENTERS[site][j],mul(HALFS[j],box[j])) for j in range(4)]
    base=[]
    for b in range(2):
        xx,yy=coord[2*b:2*b+2]
        m=max(xx[0],yy[0]),max(xx[1],yy[1])
        factor=sub(THREEHALF,mul(ONEHALF,inv(mul(m,m))))
        base.extend([mul(xx,factor),mul(yy,factor)])
    return [add(base[k],ev(TREES[site][k],box)) for k in range(4)]

# Full-field Taylor enclosures preserve cancellation between radial and curl derivatives.
POLYS=[[{tuple(e):F(c) for e,c in p} for p in row] for row in data['corrections']]
def derivative(p,j):
    out={}
    for e,c in p.items():
        if e[j]:
            ee=list(e);ee[j]-=1;out[tuple(ee)]=c*e[j]
    return out
DERTREES=[[[tree(derivative(p,j)) for j in range(4)] for p in row] for row in POLYS]
HESS=[]
for row in POLYS:
    mats=[]
    for p in row:
        mat=[]
        for j in range(4):
            mat.append([const(sum((abs(c) for c in derivative(derivative(p,j),k).values()),F()))[1] for k in range(4)])
        mats.append(mat)
    HESS.append(mats)
FC=[[F(c) for c in row] for row in data['centers']]
FH=[F(h) for h in data['halfwidths']]
BASEH={}
for site in range(2):
 for k in range(4):
  bidder=k//2
  for chart in range(2):
   axis=2*bidder+chart
   mlo=FC[site][axis]-FH[axis]
   if mlo<=0:
    assert axis==3 and FC[site][2]-FH[2]>FC[site][3]+FH[3]
    continue
   xmax=FC[site][k]+FH[k]
   hh=[[F() for j in range(4)] for i in range(4)]
   if k==axis:hh[axis][axis]=1/mlo**3
   else:
    hh[k][axis]=hh[axis][k]=1/mlo**3
    hh[axis][axis]=3*xmax/mlo**4
   BASEH[site,k,chart]=[[const(hh[i][j]*FH[i]*FH[j])[1] for j in range(4)] for i in range(4)]
def fields(box,site):
    mid=tuple(((a+b)//2,(a+b)//2) for a,b in box)
    half=[(b-a)//2 for a,b in box]
    coord=[add(CENTERS[site][j],mul(HALFS[j],mid[j])) for j in range(4)]
    whole=[add(CENTERS[site][j],mul(HALFS[j],box[j])) for j in range(4)]
    out=[]
    for k in range(4):
        cp=ev(TREES[site][k],mid)
        grads=[ev(tr,mid) for tr in DERTREES[site][k]]
        bb=2*(k//2)
        charts=[0] if whole[bb][0]>=whole[bb+1][1] else [1] if whole[bb+1][0]>=whole[bb][1] else [0,1]
        ranges=[]
        for chart in charts:
            axis=bb+chart
            inverse=inv(coord[axis])
            cube=mul(mul(inverse,inverse),inverse)
            factor=sub(THREEHALF,mul(ONEHALF,mul(inverse,inverse)))
            val=add(mul(coord[k],factor),cp)
            dg=list(grads)
            dg[k]=add(dg[k],mul(HALFS[k],factor))
            dg[axis]=add(dg[axis],mul(HALFS[axis],mul(coord[k],cube)))
            radius=0
            for j in range(4):
                radius+=-((-max(abs(dg[j][0]),abs(dg[j][1]))*half[j])//S)
                for l in range(4):
                    hbound=HESS[site][k][j][l]+BASEH[site,k,chart][j][l]
                    radius+=-((-hbound*half[j]*half[l])//(2*S*S))
            ranges.append((val[0]-radius,val[1]+radius))
        out.append((min(a for a,b in ranges),max(b for a,b in ranges)))
    return out

def density(box):
    a=fields(box,0);b=fields(box,1)
    # a/b order: own1, own2, opposing1, opposing2.
    lo=min(40*(max(0,a[3][0])-a[1][1]),
           (20*(max(0,b[2][0])-b[0][1]))//3,
           40*(b[1][0]-max(0,b[3][1])))
    hi=min(40*(max(0,a[3][1])-a[1][0]),
           -((-20*(max(0,b[2][1])-b[0][0]))//3),
           40*(b[1][1]-max(0,b[3][0])))
    if a[0][1]>max(0,a[2][0]):lo=0
    if a[0][0]>max(0,a[2][1]):hi=0
    return max(0,lo),max(0,hi)
def main(limit):
    start=time.perf_counter();serial=0
    box=tuple([(-S,S)]*4);lo,hi=density(box)
    # Entries: priority, serial, normalized box, lambda lower/upper, path.
    heap=[(-float(VOL*F(hi-lo,S)/10),serial,box,lo,hi,'')]
    total=F(lo,S)*VOL/10;upper=F(hi,S)*VOL/10
    count=1
    weights=[F(3,20),F(3,10),F(9,50),F(13,80)]
    while len(heap)<limit and heap and -heap[0][0]>1e-12:
        _,_,box,lo,hi,path=heappop(heap)
        vol=VOL
        for aa,bb in box:vol*=F(bb-aa,2*S)
        total-=vol*F(lo,S)/10;upper-=vol*F(hi,S)/10
        axis=max(range(4),key=lambda j:(box[j][1]-box[j][0])*weights[j])
        mid=sum(box[axis])//2
        for bit in [0,1]:
            child=list(box);child[axis]=(box[axis][0],mid) if bit==0 else (mid,box[axis][1]);child=tuple(child)
            ll,hh=density(child);ll=max(ll,lo);hh=min(hh,hi)
            assert 0<=ll<=hh,(ll,hh)
            serial+=1;count+=1
            total+=vol*F(ll,S)/20;upper+=vol*F(hh,S)/20
            heappush(heap,(-float(vol*F(hh-ll,S)/20),serial,child,ll,hh,path+str(axis)+str(bit)))
        if count%2000==1:print('cells',count,'gain',float(total),'ceiling',float(upper),'seconds',round(time.perf_counter()-start,1),flush=True)
    leaves=[dict(path=path,lambda_floor=str(lo),lambda_ceiling=str(hi)) for _,_,box,lo,hi,path in heap]
    out=dict(status='EXACT_INTERVAL_DISCOVERY_PENDING_INDEPENDENT_REPLAY',scale=str(S),root_volume=str(VOL),
             lower=str(total),upper=str(upper),display=[float(total),float(upper)],leaves=leaves,
             evaluations=count,seconds=time.perf_counter()-start)
    (ROOT/'discovery/bb_translation_intervals.json').write_text(json.dumps(out,indent=2)+'\n')
    print('DONE',len(leaves),float(total),float(upper),out['seconds'])
if __name__=='__main__':main(int(sys.argv[1]) if len(sys.argv)>1 else 8192)
