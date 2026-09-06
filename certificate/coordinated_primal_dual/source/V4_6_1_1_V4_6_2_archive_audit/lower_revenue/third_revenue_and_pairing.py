"""Fresh archive audit: direct continuum integration, no source-calculator imports.
Standard-library rational polynomials; base polygons integrated by vertical slices.
Run without -O. Default is read-only; --write records adjacent fresh audit JSON.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json,sys,hashlib
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
class Poly:
 def __init__(self,x=0):
  self.p=x.p.copy() if isinstance(x,Poly) else ({k:F(v) for k,v in x.items() if v} if isinstance(x,dict) else ({(0,0):F(x)} if x else {}))
 def __add__(self,x):
  p=self.p.copy()
  for k,v in Poly(x).p.items():p[k]=p.get(k,F())+v
  return Poly(p)
 __radd__=__add__
 def __neg__(self):return Poly({k:-v for k,v in self.p.items()})
 def __sub__(self,x):return self+-Poly(x)
 def __rsub__(self,x):return Poly(x)+-self
 def __mul__(self,x):
  p={}
  for (i,j),v in self.p.items():
   for (a,b),w in Poly(x).p.items():p[i+a,j+b]=p.get((i+a,j+b),F())+v*w
  return Poly(p)
 __rmul__=__mul__
 def __truediv__(self,x):return self* (1/F(x))
 def __pow__(self,n):
  assert n>=0
  ans=Poly(1)
  for _ in range(n):ans*=self
  return ans
 def at(self,x,y=0):return sum((v*x**i*y**j for (i,j),v in self.p.items()),F())
 def integ(self,l,h):
  assert all(j==0 for i,j in self.p)
  return sum((v*(h**(i+1)-l**(i+1))/F(i+1) for (i,j),v in self.p.items()),F())
 def substitute_y(self,z):return sum((v*X**i*z**j for (i,j),v in self.p.items()),Poly())
X=Poly({(1,0):1});Y=Poly({(0,1):1})
def G(A,B,C):return A*(1-A)*(C-A)+B*(1-B)*(C-B)+C*((1-C+B)*(1-C+A)-(A+B-C)**2/2)
def clip(vertices,plane):
 ans=[]
 for p,q in zip(vertices,vertices[1:]+vertices[:1]):
  f,g=plane.at(*p),plane.at(*q)
  if f>=0:ans.append(p)
  if (f<0<g) or (g<0<f):ans.append(tuple((p[i]*g-q[i]*f)/(g-f) for i in (0,1)))
 return ans

def slices(p,poly):
 """Integrate by vertical slices, not Green or simplex-moment helper code."""
 if len(poly)<3:return F()
 ans=F();xs=sorted(set(x for x,y in poly))
 for l,h in zip(xs,xs[1:]):
  mid=(l+h)/2;edges=[]
  for (x,y),(a,b) in zip(poly,poly[1:]+poly[:1]):
   if min(x,a)<mid<max(x,a):edges.append(Poly(y)+(X-x)*(b-y)/(a-x))
  if not edges:continue
  assert len(edges)==2
  lo,hi=sorted(edges,key=lambda z:z.at(mid))
  inner=sum((v*X**i*(hi**(j+1)-lo**(j+1))/F(j+1) for (i,j),v in Poly(p).p.items()),Poly())
  ans+=inner.integ(l,h)
 return ans
A=F(2,3);d=F(1,2);c=F(157,500);q=d-c;a=A+q*q/2;b=a+c;s=a+d
lam=F(4,5);end=F(3421,10000);jump=lam*(end-c);m=b-A;ka=A-q
T=1-F(2,3)*c;U=F(5,3)-2*c;D=F(4,3)*(b-F(5,6))
def base():
 total=area=F();cells=[]
 pivots=[Poly(0),X-a,X+Y-b]
 for i,H in enumerate(pivots):
  for hi in (False,True):
   for lo in (False,True):
    pa=H+(s-Y if lo else a);pb=H+(s-X if hi else a);pc=H+b
    for status in range(3):
     poly=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1))]
     cond=[H-J for J in pivots]+[X-d if hi else d-X,Y-d if lo else d-Y]
     cond+= [1-pa,1-pb] if status==0 else ([pa-1,1-pb] if status==1 else [pa-1,pb-1])
     for plane in cond:
      poly=clip(poly,plane)
      if not poly:break
     ar=slices(1,poly)
     if ar==0:continue
     assert ar>0
     for xy in poly:
      ap,bp,cp=(z.at(*xy) for z in (pa,pb,pc))
      assert 0<=bp<=ap and max(ap,bp)<=cp<=ap+bp and 0<=cp-ap<=1 and 0<=cp-bp<=1
     if status==0:rev=G(pa,pb,pc)
     elif status==1:
      k=pc-pb
      rev=pb*k*(1-pb)+pc*((1-k)*(1-pb)+(1-k)**2/2)
     else:rev=pc*(2-pc)**2/2
     rr=slices(rev,poly);area+=ar;total+=rr
     cells.append(dict(pivot=i,hi=hi,lo=lo,status=status,area=str(ar),integral=str(rr)))
 assert area==F(1,2) and len(cells)==9
 return 4*total,cells

def add(v,w):return tuple(x+y for x,y in zip(v,w))
def scale(v,s):return tuple(x*s for x in v)
def mul(v,w,D):return(v[0]*w[0]+D*v[1]*w[1],v[0]*w[1]+v[1]*w[0])
def fi(poly,left,right,rad):
 def at(x):
  ans=(F(),F());powx=(F(1),F())
  # Power by iteration; independent of source primitive/Horner implementation.
  for degree in range(max((i for i,j in poly.p),default=0)+2):
   if degree:ans=add(ans,scale(powx,poly.p.get((degree-1,0),F())/degree))
   powx=mul(powx,x,rad)
  return ans
 assert all(j==0 for i,j in poly.p)
 return add(at(right),scale(at(left),-1))
def own_menu(rows):
 total=area=F()
 for ax,ay,payment in rows:
  polygon=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]
  for bx,by,pay in rows:
   polygon=clip(polygon,(ax-bx)*X+(ay-by)*Y+pay-payment)
   if not polygon:break
  ar=slices(1,polygon);area+=ar;total+=payment*ar
 assert area==1
 return total

def direct():
 rb,cells=base();C0=Poly(F(5,6))+F(3,4)*X**2
 # Integrate entire capped menu over rho for each inverse branch.
 I=G(A,C0-X,C0);J=X*(m-X)**3/2+(m-X)**4/8
 assert (G(A,Y-X,Y)-(I-(Y-C0)**2)).p=={}
 eta=Y-X-A
 assert (G(A,A,Y)-G(A,Y-X,Y)-F(3,2)*X*eta**2-eta**3/2).p=={}
 assert I.p==(Poly(F(59,108))+X**2/4-X**3+F(9,16)*X**4).p
 assert C0.at(end)<b and c<m<end and end**2<D<ka**2
 h=(1-lam)*X+q+lam*end
 plateau=(b*jump-((d+jump)**2-d*d)/2)*I.at(c)-jump*(b-C0.at(c))**3/3+jump*J.at(c)
 sloped=(1-lam)*((b-h)*I-(b-C0)**3/3).integ(c,end)+(1-lam)*J.integ(c,m)
 remainder=((b-q-X)*I).integ(end,ka)
 cutoff=scale(fi((b-C0)**3,(end,F()),(F(),F(1)),D),-F(1,3))
 old=( (b-X)*G(a,s-X,b)).integ(d,A)
 qpiece=scale(add((plateau+sloped+remainder-old,F()),cutoff),4)
 # Free-Q: area with bundle floor b0 plus remaining sum fibres.
 b0=(F(4,3),-F(1,3));RF=(F(4,9),F(2,27));free_area=(F(1,12),F(1,9))
 qfree=scale(add(mul(free_area,RF,F(2)),fi((1-X)*G(A,A,X),b0,(b,F()),F(2))),2)
 qfree=add(qfree,(-2*(F(1,4)-(1-b)**2/2)*G(a,a,b),F()))
 # Lottery and base correction where reserve exceeds A.
 delta=F(9,16)*(T-X)*(U-X)
 e_lottery=4*c*(delta**2).integ(A,T)
 e_correction=4*c*(G(X,d,X+c)-G(a,s-X,b)).integ(A,a)
 assert e_correction<0
 # Base fee: integrate affine t/rho domains directly by vertical slicing.
 gg=lam*(end-Y)
 pa=X+Y-c;pb=Y+q;pc=X+Y
 gamma1=1-2*pc+2*pa+F(3,2)*(pc-pb)**2-F(3,2)*pa**2
 gamma2=F(3,2)-2*pc+F(3,2)*(pc-pb)**2
 assert (G(pa,pb+gg,pc+gg)-G(pa,pb,pc)-gamma1*gg+gg**2).p=={}
 def high(B,C):
  k=C-B
  return B*k*(1-B)+C*((1-k)*(1-B)+(1-k)**2/2)
 assert (high(pb+gg,pc+gg)-high(pb,pc)-gamma2*gg+gg**2).p=={}
 def fee_integral(planes,gamma):
  vertices=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]
  for plane in planes:vertices=clip(vertices,plane)
  return slices(gamma*gg-gg**2,vertices)
 basic=[Y-c,end-Y,X+Y-b]
 main=4*(fee_integral(basic+[1-pa],gamma1)+fee_integral(basic+[pa-1],gamma2))
 gamma0=1-2*b+2*a+F(3,2)*(X-q)**2-F(3,2)*a*a
 assert (G(a,s-X+gg,b+gg)-G(a,s-X,b)-gamma0*gg+gg**2).p=={}
 extra=4*fee_integral([Y-c,m-Y,X-A,b-X-Y],gamma0)
 coeff=(rb+qpiece[0]+qfree[0]+e_lottery+e_correction+main+extra,qfree[1],qpiece[1]/1500)
 assert D==F(493894,1500**2)
 checks=0
 for j in range(1,20):
  t=A+(T-A)*F(j,20);de=F(9,16)*(T-t)*(U-t);beta=(3*t-2)/(3*t-2+2*de)
  assert own_menu([(0,0,F()),(0,1,d+de),(1,0,t),(1,1,t+c+de),(1,beta,t+beta*c)])==G(t,d,t+c)+de*de
  checks+=1
 for k in (c,m,end,ka):
  for C in (C0.at(k),max(C0.at(k),b)):
   B=min(A,C-k)
   assert own_menu([(0,0,F()),(1,0,A),(0,1,B),(1,1,C)])==G(A,B,C)
   checks+=1
 return coeff,dict(own_menu_polygon_checks=checks,base=str(rb),base_cells=cells,q_constrained=list(map(str,qpiece)),q_free=list(map(str,qfree)),E_lottery=str(e_lottery),E_reserve_correction=str(e_correction),base_fee_main=str(main),base_fee_additional_strip=str(extra))
def sqrt_bounds(n,digits=90):
 scale=10**digits;floor=isqrt(n*scale*scale)
 assert floor*floor<n*scale*scale<(floor+1)**2
 return F(floor,scale),F(floor+1,scale)
def bound(coeffs,rad):
 lo=hi=coeffs[0]
 for co,r in zip(coeffs[1:],rad):
  a,b=sqrt_bounds(r)
  lo+=co*(a if co>0 else b);hi+=co*(b if co>0 else a)
 return lo,hi
def decimals(iv,digits=30):
 scale=10**digits
 lo=(iv[0]*scale).numerator//(iv[0]*scale).denominator
 hi=-((-iv[1]*scale).numerator//(-iv[1]*scale).denominator)
 def fmt(v):
  sign='-' if v<0 else '';z=str(abs(v)).zfill(digits+1)
  return sign+z[:-digits]+'.'+z[-digits:]
 return[fmt(lo),fmt(hi)]
def run():
 assert __debug__ and not sys.flags.optimize
 coeff,parts=direct()
 frozen=ROOT/'V4_6_1_1_lower_bound/certificate/refined_revenue.json';source=json.loads(frozen.read_text(encoding='utf-8'))
 assert coeff==tuple(map(F,source['coefficients']))
 # Source is read only AFTER independent coefficients were constructed.
 iv=bound(coeff,(2,493894))
 oldfile=ROOT/'V4_6_1_lower_bound/certificate/branch_summary.json';old=json.loads(oldfile.read_text(encoding='utf-8'))
 oldiv=bound(tuple(map(F,old['exact_revenue_coefficients'])),(2,11))
 inc=(iv[0]-oldiv[1],iv[1]-oldiv[0]);assert inc[0]>F(17,2000000)
 upperfile=ROOT/'V4_6_2_upper/certificate/upper_ledger.json';up=json.loads(upperfile.read_text(encoding='utf-8'))
 U=F(up['anchor_upper'])-F(up['exact_common_support_subtraction'])-F(81,10**10)
 assert U==F(up['final_upper'])<F(up['simple_rational_upper'])
 gap=(U-iv[1],U-iv[0]);ratio=(iv[0]/U,iv[1]/U)
 assert gap[0]>0 and gap[1]<F(1,100)
 assert ratio[0]>F(992684,1000000)
 summary=dict(status='FRESH_THIRD_CONTINUUM_REVENUE_AND_PAIRING_PASS',basis=['1','sqrt(2)','sqrt(493894)'],coefficients=list(map(str,coeff)),revenue=decimals(iv),gain_vs_V461=decimals(inc),new_upper=decimals((U,U)),gap=decimals(gap),ratio_lower_over_upper=decimals(ratio),ratio_guarantee='992684/1000000',gap_ceiling='1/100',components=parts,dependencies='Python standard library only; no imports from proof packages',arithmetic_scope='Revenue independently reintegrated; upper formula reconciled but upper validity separately audited',source_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (frozen,oldfile,upperfile)})
 path=OUT/'third_revenue_and_pairing.json'
 if '--write' in sys.argv:path.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
 else:assert json.loads(path.read_text(encoding='utf-8'))==summary
 print(summary['status'])
 for name in ('revenue','gain_vs_V461','new_upper','gap','ratio_lower_over_upper'):print(name,summary[name])
if __name__=='__main__':run()
