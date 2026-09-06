"""Independent rational-polynomial structure checks with no project imports.

Includes an infinite-allocation-range convex utility family. These exact
identities support, but do not formalize, the accompanying all-real proof.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Assertions required')
N=5
class P:
 def __init__(self,terms=0):
  self.terms={m:F(c) for m,c in terms.items() if c} if isinstance(terms,dict) else ({(0,)*N:F(terms)} if terms else {})
 @staticmethod
 def var(i):
  m=[0]*N;m[i]=1;return P({tuple(m):1})
 def __add__(self,r):
  r=poly(r);d=dict(self.terms)
  for m,c in r.terms.items():d[m]=d.get(m,F())+c
  return P(d)
 __radd__=__add__
 def __neg__(self):return P({m:-c for m,c in self.terms.items()})
 def __sub__(self,r):return self+-poly(r)
 def __rsub__(self,r):return poly(r)+-self
 def __mul__(self,r):
  d={}
  for m,c in self.terms.items():
   for n,e in poly(r).terms.items():
    k=tuple(a+b for a,b in zip(m,n));d[k]=d.get(k,F())+c*e
  return P(d)
 __rmul__=__mul__
 def __truediv__(self,r):return self*F(1,r)
 def __pow__(self,n):
  assert isinstance(n,int) and n>=0
  out=P(1)
  for _ in range(n):out=out*self
  return out
 def substitute(self,i,value):
  out=P()
  for m,c in self.terms.items():
   n=list(m);n[i]=0;out+=P({tuple(n):c})*poly(value)**m[i]
  return out
 def integral(self,i,lo,hi):
  out={}
  for m,c in self.terms.items():
   n=list(m);n[i]+=1;out[tuple(n)]=c/n[i]
  prim=P(out);return prim.substitute(i,hi)-prim.substitute(i,lo)
 def constant(self):
  assert all(not any(m) for m in self.terms);return self.terms.get((0,)*N,F())
 def serialized(self):return {','.join(map(str,m)):str(c) for m,c in sorted(self.terms.items())}
def poly(v):return v if isinstance(v,P) else P(v)
x,y,k,p,C=[P.var(i) for i in range(N)]
A=F(2,3);d=F(1,2);c=F(157,500);q=d-c;nu=q*q/2;a=A+nu;b=a+c;U=F(5,3)-2*c;T=1-2*c/3;u=F(3421,10000);eta=F(4,5)
K=A-q;rho=b-A;g=lambda r:eta*(u-r)
B0=lambda z:F(5,6)+F(3,4)*z*z-z
checks={}
def exact(name,expr,expected=0):
 pp=poly(expr)-expected;assert not pp.terms,(name,pp.serialized())
 checks[name]=poly(expr).serialized()
exact('new_reserve',a,F(1025947,1500000))
exact('Q_floor_margin',B0(K)-(rho+q+g(rho)),F(37,5000000))
exact('Q_floor_derivative_minimum',eta-F(3,2)*K,F(79,1000))
exact('Q_upgrade_margin_at_c',B0(c)-d-g(c),F(212401,3000000))
assert B0(K)>d and B0(c)<A and K<d
mass=(3*(C-k)-2)*k+(3*C-3*x-2).integral(0,k,A)+1-A
area=k*(C-k)+(C-x).integral(0,k,A)
exact('Q_general_mass',mass,2*(C-(F(5,6)+F(3,4)*k*k)))
exact('Q_general_sink',3*area-mass,1)
# Use variable x for t in the independent E polynomial reconstruction.
t=x;delta=F(9,16)*(T-t)*(U-t);alpha=3*t-2;L=delta+alpha/2;j=1-t/2;z=t+c+delta
exact('E_zero_top_mass',3*(A*z-A*j+j*j/2-(t-q)**2/2)-1)
exact('E_allowance_endpoint',(t-A+2*delta/3).substitute(0,A),nu)
allowance_der=lambda t0:1+F(3,8)*(2*t0-T-U)
assert allowance_der(A)>0 and allowance_der(T)>0
checks['E_allowance_derivative_endpoints']=[str(allowance_der(A)),str(allowance_der(T))]
exact('E_delta_at_A',delta.substitute(0,A),3*q*q/4)
exact('E_delta_at_T',delta.substitute(0,T))
assert (1-T/2)-(T-q)==0 and (1-A/2)-(A-q)>0 and q*(1-F(3,2)*q)>0
checks['E_sink_margin']=str(q*(1-F(3,2)*q))
# W: integrate geometry anew; no candidate or polygon helper imported.
z=k+p
WG=lambda f:poly(f).integral(1,z-x,1).integral(0,k,1)
# H price divides by k; cancel it with the horizontal integral length k.
HP=lambda multiplier:(((3*k+1)*y-k-1)*multiplier/2).integral(1,p,1)
price_g=(3*x-1)/2+(3*y-1)/2
value=p*k*(1-p)+(k+p)*((1-k)*(1-p)+(1-k)**2/2)
exact('W_candidate_price_identity',WG(price_g)+HP(P(1)),value)
# u=(u_star)^2/4 gives a continuum of allocations, all bounded by u_star's.
vg=x+y-z;vh=y-p
rev=WG((x+y)*vg/2-vg*vg/4)+((y*vh/2-vh*vh/4)*k).integral(1,p,1)
priced=WG(price_g*vg/2)+HP(vh/2)
exact('W_nonlinear_convex_utility_identity',rev-priced)
checks['W_nonlinear_revenue']=rev.serialized()
exact('W_uniform_sign_margin',(4-3*q)*(u+q)-(2-q),F(18601,5000000))
areaQ=A*A-(2*A-b)**2/2;areaE=2*c*(T-A);areaW=2*q*(1-q-u)
exact('Q_area',areaQ,F(1746937679191,4500000000000))
exact('E_area',areaE,F(4867,62500))
exact('W_area',areaW,F(438867,2500000))
exact('certified_area',areaQ+areaE+areaW,F(2887322279191,4500000000000))
assert a-c>q>0
checks['tariff_discount_bounds']={'both_below_d':str(a-c),'one_above_d':str(q),'both_above_d':str(2*q)}
J=g(c)
assert a+J<1-q and u+q<1-q and b+J<1+u and T<1-q
assert max(F(5,6)+F(3,4)*K*K,b+J)<1+u
assert F(5,6)+F(3,4)*K*K-A<1-q
checks['wing_price_margins']={key:str(v) for key,v in {'reserve':1-q-a-J,'fee':1-q-u-q,'bundle':1+u-b-J,'Q_upgrade':1-q-(F(5,6)+F(3,4)*K*K-A)}.items()}
OUT=Path(__file__).resolve().parent
out={'status':'INDEPENDENT_STRUCTURE_IDENTITIES_PASS','check_count':len(checks),'checks':checks,'independence':'Independent Fraction polynomial reconstruction, no project code imported; does not formalize all-real case analysis.'}
target=OUT/'independent_structure_identities.json'
if '--write' in sys.argv:
 target.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
else:
 assert json.loads(target.read_text(encoding='utf-8'))==out
print(out['status'],len(checks))
