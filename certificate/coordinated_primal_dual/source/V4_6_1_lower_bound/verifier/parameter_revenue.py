"""Exact continuous revenue for a rebuilt rational parameter family.

No optimizer is called. Fractions, polynomial cells, and certified sqrt/log
series evaluate the explicit continuous integral, including high-price menus.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V3'/'verifier'))
import joined_threshold as tools
from stationary_s import P
I=tools.I
X=P((0,1))
a,c=F(2,3),F(47,150)
b=a+c;d=F(1,2);s=a+d;q=d-c;A=F(2,3)
T=1-2*c/3;U=F(5,3)-2*c;K=F(2,3)+c*c
r0=b*b-K;r1=4*c/3-F(2,9);rb=4*(b-F(5,6))/3

def G(a,b,c):
    return a*(1-a)*(c-a)+b*(1-b)*(c-b)+c*((1-c+b)*(1-c+a)-(a+b-c)**2*F(1,2))

class BP:
    def __init__(self,x=0):
        self.z=x.z.copy() if isinstance(x,BP) else ({k:F(v) for k,v in x.items() if v} if isinstance(x,dict) else ({(0,0):F(x)} if x else {}))
    def __add__(self,x):
        z=self.z.copy()
        for k,v in BP(x).z.items():z[k]=z.get(k,F())+v
        return BP(z)
    __radd__=__add__
    def __neg__(self):return BP({k:-v for k,v in self.z.items()})
    def __sub__(self,x):return self+-BP(x)
    def __rsub__(self,x):return BP(x)+-self
    def __mul__(self,x):
        z={}
        for (i,j),v in self.z.items():
            for (k,l),w in BP(x).z.items():z[i+k,j+l]=z.get((i+k,j+l),F())+v*w
        return BP(z)
    __rmul__=__mul__
    def __truediv__(self,x):return self*(1/F(x))
    def __pow__(self,n):
        z=BP(1)
        for _ in range(n):z=z*self
        return z
    def at(self,x,y):return sum((v*x**i*y**j for (i,j),v in self.z.items()),F())

TT=BP({(1,0):1});RR=BP({(0,1):1})
def clip(poly,f):
    f=BP(f);out=[]
    for i,p in enumerate(poly):
        n=poly[(i+1)%len(poly)];fp=f.at(*p);fn=f.at(*n)
        if fp>=0:out.append(p)
        if (fp<0<fn) or (fn<0<fp):
            z=fp/(fp-fn);out.append((p[0]+z*(n[0]-p[0]),p[1]+z*(n[1]-p[1])))
    return out

def pintegral(f,poly):
    ans=F()
    if not poly:return ans
    for j,p in enumerate(poly):
        n=poly[(j+1)%len(poly)];dx=n[0]-p[0];dy=n[1]-p[1]
        for (i,k),co in BP(f).z.items():
            z=(P((p[0],dx))**(i+1))*(P((p[1],dy))**k)
            ans+=co*dy*z.integral(0,1)/(i+1)
    return ans

def base_integral():
    total=F();areas=F();count=0
    for H,cond in ((BP(0),(a-TT,b-TT-RR)),(TT-a,(TT-a,c-RR)),(TT+RR-b,(TT+RR-b,RR-c))):
        for lo_t in (True,False):
            for lo_r in (True,False):
                pa=H+(a if lo_r else s-RR);pb=H+(a if lo_t else s-TT);pc=H+b
                for status in range(3):
                    poly=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1))]
                    fs=list(cond)+[d-TT if lo_t else TT-d,d-RR if lo_r else RR-d]
                    if status==0:fs += [1-pa,1-pb];rev=G(pa,pb,pc)
                    elif status==1:
                        fs += [pa-1,1-pb];kk=pc-pb
                        rev=pb*kk*(1-pb)+pc*((1-kk)*(1-pb)+(1-kk)**2/2)
                    else:fs += [pb-1,pa-1];rev=pc*(2-pc)**2/2
                    for f in fs:
                        if poly:poly=clip(poly,f)
                    area=pintegral(1,poly)
                    assert area>=0
                    if area:
                        count+=1;areas+=area;total+=pintegral(rev,poly)
    assert areas==F(1,2)
    return 4*total,count

def integral(p,lo,hi):return tools.integrate_interval(P(p),I(lo),I(hi))
def square(x):return tools.sqrt_interval(x,60)
def ratint(p,lo,hi):return P(p).integral(F(lo),F(hi))

def menu_area_replay():
    import parameter_candidate as candidate
    count=0
    for t in (A+F(1,1000),F(7,10),F(3,4),T-F(1,1000)):
        rows,branch=candidate.menu((t,F(1,10)))
        assert branch=='E_lottery'
        ans=F()
        for p,alloc,tag in rows:
            assert not p.s
            poly=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]
            for pp,aa,tt in rows:
                if poly:poly=clip(poly,(alloc[0]-aa[0])*TT+(alloc[1]-aa[1])*RR+pp.r-p.r)
            ans+=p.r*pintegral(1,poly)
        dl=F(9,16)*(T-t)*(U-t)
        assert ans==G(t,d,t+c)+dl*dl
        count+=1
    for t in (F(51,100),F(11,20),F(3,5),A):
        kk=t-q;C0=F(5,6)+F(3,4)*kk*kk
        for zz in (max(C0,t),b):
            if not t<=zz<=b:continue
            pp=(A,max(C0,zz)-kk,max(C0,zz))
            Ri=F(59,108)+kk*kk/4-kk**3+F(9,16)*kk**4
            assert G(*pp)==Ri-max(F(0),zz-C0)**2
            count+=1
    return count

def pair_mul(x,y,D):
    return x[0]*y[0]+D*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def pair_add(x,y):return x[0]+y[0],x[1]+y[1]
def pair_scale(x,v):return v*x[0],v*x[1]
def pair_integral(poly,lo,hi,D):
    coeffs=(F(),)+tuple(co/F(i+1) for i,co in enumerate(P(poly).c))
    def ev(x):
        out=(F(),F())
        for co in reversed(coeffs):out=pair_add(pair_mul(out,x,D),(co,F()))
        return out
    return pair_add(ev(hi),pair_scale(ev(lo),-1))
def radical_expression(base,qhigh,lottery):
    root2b=(F(4,3),-F(1,3));rfree=(F(4,9),F(2,27))
    area=F(1,4)-(1-b)**2/2
    low=pair_scale(pair_add(rfree,(-G(a,a,b),F())),2*area)
    exchange=pair_scale(pair_integral((1-X)*G(P(A),P(A),X),root2b,(b,F()),2),2)
    correction=pair_mul(rfree,pair_integral(1-X,root2b,(b,F()),2),2)
    low=pair_add(low,pair_add(exchange,pair_scale(correction,-2)))
    C0=P(F(5,6))+F(3,4)*(X-q)**2
    assert rb==F(44,225)
    cost=pair_scale(pair_integral((b-C0)**3,(d,F()),(q,F(2,15)),11),-F(4,3))
    coeff=(base+qhigh+lottery+low[0]+cost[0],low[1],cost[1])
    assert coeff==(F(482935538268336599,574087500000000000),F(31,1215),-F(170368,664453125))
    return coeff

def calculate():
    assert r0==r1 and d<q+square(r1).lo<a==A<T<1
    assert 0<c<d<a and b<1 and b>F(4,3)-square(2).lo/3
    assert b<2*d and 0<q<c and q+square(rb).hi<a
    base,cells=base_integral()
    k=X-q;C0=P(F(5,6))+F(3,4)*k*k
    Ri=P(F(59,108))+F(1,4)*k*k-k**3+F(9,16)*k**4
    Bz=G(P(a),P(s)-X,P(b))
    dl=F(9,16)*(T-X)*(U-X)
    qhigh=I(4*ratint((b-X)*(Ri-Bz),d,A))
    lottery=I(4*c*ratint(dl*dl,A,T))
    rt2=square(2);B0=(I(4)-rt2)/3;RF=I(F(4,9))+F(2,27)*rt2
    areaL=F(1,4)-(1-b)**2/2
    qlow=2*areaL*(RF-G(a,a,b))
    exchange=2*integral((1-X)*G(P(A),P(A),X),B0,b)-2*RF*integral(1-X,B0,b)
    cost=-F(4,3)*integral((b-C0)**3,d,q+square(rb))
    revenue=I(base)+qhigh+lottery+qlow+exchange+cost
    before=F('8758198541484224553461/10000000000000000000000')
    assert revenue.lo>before+F(63,100000)
    vals={'base':I(base),'Q_high_replacement':qhigh,'lottery':lottery,'Q_low_free_replacement':qlow,'Q_low_bundle_competition':exchange,'Q_high_bundle_competition':cost}
    data={'status':'PARAMETER_REBUILT_EXACT_REVENUE_PASS','scope':'Exact continuous integral of the fully specified parameter_candidate mechanism; lower bound only',
      'parameters':{key:str(v) for key,v in dict(a=a,b=b,c=c,s=s,d=d,q=q,A=A,T=T,U=U,K=K,r0=r0,r1=r1,rb=rb).items()},
      'radical_coefficients_basis_1_sqrt2_sqrt11':list(map(str,radical_expression(base,qhigh.lo,lottery.lo))),'base_exact':str(base),'base_positive_area_cells':cells,'base_ordered_area':'1/2','independent_menu_area_identities':menu_area_replay(),
      'component_intervals':{key:tools.rounded_interval(val,28) for key,val in vals.items()},
      'revenue_interval':tools.rounded_interval(revenue,28),'gain_over_V4_6_interval':tools.rounded_interval(revenue-before,28),
      'certified_gain_exceeds':'63/100000','formula':'research_log/parameter_rebuilt_family.md',
      'discovery_claim_boundary':'No parameter optimality or unrestricted optimality assertion.'}
    path=ROOT/'certificate/parameter_revenue.json'
    if '--write' in sys.argv:path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text(encoding='utf-8'))==data
    print(data['status']);print('revenue',data['revenue_interval'],[float(F(z)) for z in data['revenue_interval']]);print('base',float(base))
    return data
if __name__=='__main__':
    if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O')
    calculate()
