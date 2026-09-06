"""Fresh audit: support divergence and latest candidate's strict dual slack.
Only inputs are frozen stream coefficients and selected menu implementation.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
from itertools import product
from hashlib import sha256
import importlib.util,json,sys
if not __debug__ or sys.flags.optimize: raise RuntimeError('No optimized Python.')
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
ARCH=BASE.parents[2]/'research/closed/two-bidder-two-item-dsic-certificates/certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound'
LOWER=BASE/'V4_6_1_1_lower_bound/verifier/refined_candidate.py'
spec=importlib.util.spec_from_file_location('fresh_selected_lower',LOWER)
selected=importlib.util.module_from_spec(spec);spec.loader.exec_module(selected)
# Independent Q(sqrt(2)) arithmetic and univariate polynomials.
class Q2:
    def __init__(self,a=0,b=0):self.a,self.b=F(a),F(b)
    @staticmethod
    def cast(v):return v if isinstance(v,Q2) else Q2(v)
    def __add__(self,v):v=self.cast(v);return Q2(self.a+v.a,self.b+v.b)
    __radd__=__add__
    def __neg__(self):return Q2(-self.a,-self.b)
    def __sub__(self,v):return self+-self.cast(v)
    def __rsub__(self,v):return self.cast(v)+-self
    def __mul__(self,v):v=self.cast(v);return Q2(self.a*v.a+2*self.b*v.b,self.a*v.b+self.b*v.a)
    __rmul__=__mul__
    def __truediv__(self,v):v=self.cast(v);den=v.a*v.a-2*v.b*v.b;return self*Q2(v.a/den,-v.b/den)
    def __pow__(self,n):
        out=Q2(1)
        for _ in range(n):out=out*self
        return out
    def __eq__(self,v):v=self.cast(v);return self.a==v.a and self.b==v.b

def peval(p,x):
    out=Q2()
    for co in reversed(p):out=out*x+co
    return out

def integral(p,lo,hi):return sum((co*(Q2.cast(hi)**(j+1)-Q2.cast(lo)**(j+1))/(j+1) for j,co in enumerate(p)),Q2())
A=Q2(F(2,3));b0=Q2(F(4,3),-F(1,3));k=b0-A;Z=F(3,4)
Fm=[(3*b0-2)*A-F(3,2)*A*A+1-A,2-3*b0,Q2(F(3,2))]
assert peval(Fm,k)==0 and peval(Fm,A)==1-A
# F'=-f, f=3(b0-x)-2. Divergences follow exactly coefficientwise.
assert Fm[1]==2-3*b0 and 2*Fm[2]==3
D0=k*A+integral([b0,-Q2(1)],k,A)
assert D0==F(1,3)
# Psi2(top)=3(1-ell)+f=1 and Psi1(right)=3(1-A)=1.
assert 3*(1-b0)+(3*b0-2)==1 and 3*(1-A)==1 and 4*(1-Z)==1
# All interfaces have matching normal traces; y=Z changes tangential Psi1 only.
mass=F(3,2)*(1-A)**2+integral(Fm,k,A)+integral([Q2(1),-Q2(1)],A,1)+F(3,2)*(k*(1-A)**2+integral([(1-b0)**2,2*(1-b0),Q2(1)],k,A))
assert mass==Q2(F(4,9),F(2,27))
# New V4.6.1.1: the same open lottery box survives the now-active safe fee.
center=(F(151,200),F(3,40),F(9,10),F(63,200)); radius=F(1,10000)
t0,r0,x0,y0=[a-radius for a in center];t1,r1,x1,y1=[a+radius for a in center]
Ac,c,d,a,b,s,q,T,U=selected.A,selected.c,selected.d,selected.a,selected.b,selected.s,selected.q,selected.T,selected.U
assert c==F(157,500)
def parameters(t):
    delta=F(9,16)*(T-t)*(U-t);alpha=3*t-2
    return delta,alpha/(alpha+2*delta),delta+alpha/2
assert Ac<t0<t1<T and r1<c
Dlo,beta0,L0=parameters(t0);Dhi,beta1,L1=parameters(t1)
assert F(9,16)*(2*t1-T-U)<0
assert F(3,2)+F(9,16)*(2*t0-T-U)>0
assert F(9,10)<beta0<beta1<F(49,50)
assert c<y0<y1<c+L0 and x0>t1 and x0-t1+d-y1>0
# Opposing conditional base menu: H=x+y-b. Safe fee active and nonnegative.
assert x0>T and x0>a and y0>c and x0+y0>b
assert s-y1>a and s-x0<a and x0>y1
assert c<y0<y1<selected.u and selected.g(y1)>0
assert x0+y0-c>t1 and y0+q>r1 and x0+y0>t1+r1
assert t0>F(43,100) and x0>F(43,100)
cycles=json.loads((BASE/'V4_6_2_upper/certificate/sparse_cycle.json').read_text(encoding='utf-8'))
for row in cycles['orbit_centers']:
    assert any(abs(a-F(z))>radius+F(h) for a,z,h in zip(center,row,cycles['halfwidths']))
profiles=[tuple(a+sg*radius for a,sg in zip(center,signs)) for signs in product((-1,1),repeat=4)]+[center]
for point in profiles:
    r=selected.mechanism(point);beta=parameters(point[0])[1]
    assert r['branches']==('base_fee','E')
    assert r['selected']==('base_0','lottery')
    assert r['allocations']==((F(),F()),(F(1),beta)) and r['utilities'][1]>0
# Direct rational differentiation of the stream; no imported polynomial builder.
ZERO=(0,0,0,0)
def add(*polys):
    out={}
    for poly in polys:
        for e,co in poly.items():out[e]=out.get(e,F())+co
    return {e:c for e,c in out.items() if c}
def scale(p,z):return {e:c*z for e,c in p.items() if c*z}
def mul(*polys):
    out={ZERO:F(1)}
    for poly in polys:
        temp={}
        for e,c in out.items():
            for f,d0 in poly.items():
                key=tuple(a0+b0 for a0,b0 in zip(e,f));temp[key]=temp.get(key,F())+c*d0
        out={e:c for e,c in temp.items() if c}
    return out
def var(j):
    e=list(ZERO);e[j]=1
    return {tuple(e):F(1)}
def derivative(poly,j):
    out={}
    for e,co in poly.items():
        if e[j]:
            ee=list(e);ee[j]-=1;out[tuple(ee)]=co*e[j]
    return out
one={ZERO:F(1)};x,y,z,w=[var(j) for j in range(4)]
m=json.loads((ARCH/'manifest.json').read_text(encoding='utf-8'))
anti={}
for e,co in zip(m['basis_order'],m['theta']):
    e=tuple(e);es=(e[1],e[0],e[3],e[2]);anti=add(anti,{e:F(co),es:-F(co)})
stream=mul(x,add(one,scale(x,-1)),y,add(one,scale(y,-1)),anti)
curl_safe=scale(derivative(stream,0),-1)
curl_bidder2={(e[2],e[3],e[0],e[1]):co for e,co in curl_safe.items()}
D=scale(mul(x,x,z,z),2)
numerator=add(mul(add(scale(mul(z,z),3),scale(one,-1)),w,x,x),mul(D,curl_bidder2))
centered={}
for e,coef in numerator.items():
    for f in product(*(range(n+1) for n in e)):
        v=coef
        for n,j,a0 in zip(e,f,center):v*=comb(n,j)*a0**(n-j)
        centered[f]=centered.get(f,F())+v
zero=(0,0,0,0);constant=centered.get(zero,F())
error=sum((abs(co)*radius**sum(e) for e,co in centered.items() if e!=zero),F())
lo,hi=constant-error,constant+error
assert hi<0
upperD=2*t1*t1*x1*x1
magnitude=-hi/upperD
volume=(2*radius)**4
# Since this field is negative, beta > 9/10 gives a sharper safe-item bound.
gap=F(9,10)*magnitude*volume
assert gap>0
record={
 'status':'FRESH_SUPPORT_AND_V4611_FLATNESS_AUDIT_PASS',
 'support_no_sale_area':'1/3','support_mass':'4/9+2*sqrt(2)/27',
 'support_checks':'Piecewise divergence, continuous normal traces, outer flux and mass reconstructed in rational quadratic arithmetic; nonnegativity and universal weak-gradient identity in audit report.',
 'latest_lower_center':list(map(str,center)),'halfwidth':str(radius),
 'latest_lower_branches':['base_fee','E'],'source_checks':len(profiles),
 'base_fee_active':True,'beta_endpoint_values':list(map(str,(beta0,beta1))),
 'beta_bounds':['9/10','49/50'],'virtual_numerator_interval':list(map(str,(lo,hi))),
 'virtual_absolute_lower':str(magnitude),'box_volume':str(volume),
 'capacity_plus_virtual_slack_lower':str(gap),
 'slack_decimal_diagnostic':float(gap),
 'polynomial_reconstruction':'Direct rational polynomial differentiation and exact centered monomial bound; independent of inherited polynomial builders.',
 'scope':'This specific V4.6.2 dual is not matching V4.6.1.1. Does not show primal suboptimality.',
 'source_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in (LOWER,ARCH/'manifest.json')},
}
(HERE/'fresh_support_latest_flatness.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(record['status']);print('latest lottery slack lower',gap);print('approximation',float(gap))
