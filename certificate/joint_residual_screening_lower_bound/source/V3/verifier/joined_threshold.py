"""Exact algebraic/logarithmic revenue for the V3 joined-threshold candidate.

The real mechanism is specified in research_log/joined_threshold_candidate.md.
This module evaluates every rational report exactly, including rational ties.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import baseline_mechanism as base
from stationary_s import P, T, revenue, gradient, nonnegative, require, prices_for_t, cutoff

a,b,c,d=base.A,base.B,base.C,base.D
q=d-c
K=F(2,3)+c*c
r0=b*b-K
r1=F(4,3)*c-F(2,9)
h=b-q

class Quad:
    """r+s sqrt(w), with exact comparisons inside one quadratic field."""
    def __init__(self,r=0,s=0,w=0):
        self.r,self.s,self.w=F(r),F(s),F(w)
        if self.s==0 or self.w==0:
            self.s,self.w=F(),F()
    def __add__(self,z):
        z=z if isinstance(z,Quad) else Quad(z)
        require(self.w==z.w or not self.s or not z.s,'common quadratic field')
        return Quad(self.r+z.r,self.s+z.s,self.w or z.w)
    __radd__=__add__
    def __neg__(self): return Quad(-self.r,-self.s,self.w)
    def __sub__(self,z): return self+-asquad(z)
    def __rsub__(self,z): return asquad(z)+-self
    def sign(self):
        r,s,w=self.r,self.s,self.w
        if not s:return (r>0)-(r<0)
        if not r:return (s>0)-(s<0)
        if r>0 and s>0:return 1
        if r<0 and s<0:return -1
        z=r*r-s*s*w
        return ((z>0)-(z<0))*(1 if r>0 else -1)
    def __eq__(self,z): return (self-asquad(z)).sign()==0
    def __lt__(self,z): return (self-asquad(z)).sign()<0
    def __le__(self,z): return (self-asquad(z)).sign()<=0
    def __gt__(self,z): return (self-asquad(z)).sign()>0
    def __ge__(self,z): return (self-asquad(z)).sign()>=0
    def __repr__(self):return str(self.r) if not self.s else f'({self.r})+({self.s})sqrt({self.w})'


def asquad(x):return x if isinstance(x,Quad) else Quad(x)


def menu(qtype):
    t,rho=max(qtype),min(qtype)
    if not (d<=t<=1 and 0<=rho<=b-min(t,a)):
        return None
    k=t-q
    if t<=a and k*k<=r0:
        prices=(a,b-k,b)
        branch='base'
    elif t<=a and k*k<r1:
        root=Quad(0,1,K+k*k)
        prices=(root-c,root-k,root)
        branch='square_root'
    elif t<=F(2,3):
        C=F(5,6)+F(3,4)*k*k
        prices=(F(2,3),C-k,C)
        branch='quadratic'
    else:
        prices,_,_=prices_for_t(t)
        branch='affine' if t<cutoff else 'base'
    low_mask=1 if qtype[0]<qtype[1] else 2
    high_mask=3-low_mask
    p=[Quad()]*4
    p[high_mask],p[low_mask],p[3]=map(asquad,prices)
    return tuple(p),branch


def mechanism(profile,modified_bidders=(0,1)):
    inherited=base.mechanism(profile)
    types=(inherited['profile'][:2],inherited['profile'][2:])
    masks=list(inherited['masks'])
    payments=list(map(asquad,inherited['payments']))
    utilities=list(map(asquad,inherited['utilities']))
    menus=[tuple(map(asquad,m['prices'])) for m in inherited['menus']]
    branches=['inherited','inherited']
    for i in modified_bidders:
        own,opp=types[i],types[1-i]
        m=menu(opp)
        if m is None:continue
        prices,branches[i]=m
        old=inherited['base_masks'][i]
        u=[base.value(own,j)-prices[j] for j in range(4)]
        top=max(u)
        if top==0:selected=0
        elif u[old]==top:selected=old
        else:
            choices=[j for j in range(4) if j & ~old==0 and u[j]==top]
            require(bool(choices),'base-subset maximizer')
            selected=min(choices)
        masks[i],payments[i],utilities[i],menus[i]=selected,prices[selected],top,prices
        require(selected & ~old==0,'containment in shared base')
    require(masks[0] & masks[1]==0,'pointwise capacity')
    return dict(profile=inherited['profile'],masks=tuple(masks),payments=tuple(payments),
                utilities=tuple(utilities),menus=tuple(menus),branches=tuple(branches))

class I:
    """Closed rational interval; used for certified constants, never mechanism decisions."""
    def __init__(self,lo=0,hi=None):
        if isinstance(lo,I):self.lo,self.hi=lo.lo,lo.hi;return
        self.lo,self.hi=F(lo),F(lo if hi is None else hi)
        require(self.lo<=self.hi,'interval order')
    def __add__(self,x):
        x=I(x);return I(self.lo+x.lo,self.hi+x.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,x):return self+-I(x)
    def __rsub__(self,x):return I(x)+-self
    def __mul__(self,x):
        x=I(x);p=[a*b for a in (self.lo,self.hi) for b in (x.lo,x.hi)]
        return I(min(p),max(p))
    __rmul__=__mul__
    def __truediv__(self,x):
        x=I(x);require(x.lo*x.hi>0,'nonzero interval divisor')
        return self*I(1/x.hi,1/x.lo)
    def __pow__(self,n):
        z=I(1)
        for _ in range(n):z=z*self
        return z


def sqrt_interval(x,digits=45):
    x=F(x);den=10**digits
    n=isqrt(x.numerator*den*den//x.denominator)
    require(F(n,den)**2<=x<=F(n+1,den)**2,'square root enclosure')
    return I(F(n,den),F(n+1,den))


def log_interval(x,n=18):
    x=I(x)
    require(x.lo>=1,'positive log-series argument')
    z=(x-1)/(x+1)
    require(z.lo>=0 and z.hi<F(1,4),'atanh-series convergence')
    part=I()
    for j in range(n):part=part+F(2,2*j+1)*z**(2*j+1)
    tail=F(2,2*n+1)*z.hi**(2*n+1)/(1-z.hi*z.hi)
    return I(part.lo,part.hi+tail)


def evaluate(poly,x):
    ans=I()
    for co in reversed(P(poly).c):ans=ans*x+co
    return ans


def primitive(poly):return P((0,)+tuple(v/F(i+1) for i,v in enumerate(P(poly).c)))


def integrate_interval(poly,lo,hi):
    p=primitive(poly)
    return evaluate(p,I(hi))-evaluate(p,I(lo))


def rounded_interval(x,digits=18):
    den=10**digits
    low=x.lo.numerator*den//x.lo.denominator
    high=-((-x.hi.numerator*den)//x.hi.denominator)
    require(F(low,den)<=x.lo<=x.hi<=F(high,den),'rounded enclosure')
    return [str(F(low,den)),str(F(high,den))]


def calculate():
    k0,k1=sqrt_interval(r0),sqrt_interval(r1)
    C0,C1=b,c+F(2,3)
    # J(k)=int (k^2+K)^(3/2) dk. Its root values are rational at both endpoints.
    Jdifference=(k1*(2*r1+5*K)*C1-k0*(2*r0+5*K)*C0)*F(1,8)
    logratio=log_interval((k1+C1)/(k0+C0))
    Jdifference=Jdifference+F(3,8)*K*K*logratio
    # Exact improvement of the square-root branch over the affine base.
    integrand_poly=(h-T)*(-F(3,2)*b*(T*T+K)+F(1,2)*b**3)
    zrootgain=4*(h*Jdifference-F(C1**5-C0**5,5)+
                  integrate_interval(integrand_poly,k0,k1))
    # Plateau branch through the Z/S pivot, with Z opponent width b-t.
    k=T-q
    C=P(F(5,6))+F(3,4)*k*k
    plateau=(P(F(2,3)),C-k,C)
    baseZ=(P(a),P(b)-k,P(b))
    zpolynomial=4*(b-T)*(revenue(*plateau)-revenue(*baseZ))
    zgain=zrootgain+integrate_interval(zpolynomial,k1+q,I(a))
    # S region: polynomial formulas independently constructed in stationary_s.
    import stationary_s
    sdata=stationary_s.calculate()
    sgain=F(sdata['new_S_gain_over_base'])
    priorZ=sum((F(row['expected_gain']) for row in base.DATA['common_rows'] if row['id'].startswith('Z')),F())
    priorS=F(sdata['inherited_S_common_gain'])+F(sdata['inherited_S_item_gain'])
    old=F('83962078694672281756033/96000000000000000000000')
    R=I(old-priorZ-priorS+sgain)+zgain
    gain=R-old
    upper=F('3715139591287203/4194304000000000')
    require(gain.lo>0,'strict exact gain')
    # Algebraic gluing, checked without approximations.
    require(K+r0==b*b,'square-root starts at zero fee')
    require(K+r1==(c+F(2,3))**2,'root-to-plateau prices')
    require(F(5,6)+F(3,4)*r1==c+F(2,3),'plateau common price at junction')
    require(F(1,6)-c+F(3,4)*r1==0,'selective fee begins at zero')
    require(d*d<1 and 0<r0<r1<(a-q)**2,'strict transition order')
    require(a<F(2,3)<cutoff<1,'S transition order')
    require(evaluate(zpolynomial,I(a)).lo>=0,'plateau endpoint gain')
    return dict(scope='explicit pointwise feasible DSIC mechanism; lower bound only',
                constants={'a':str(a),'b':str(b),'c':str(c),'d':str(d),'q':str(q),
                           'K':str(K),'k0_squared':str(r0),'k1_squared':str(r1),'t3':str(cutoff)},
                exact_revenue_expression='L - inherited_Z_gain - inherited_S_gain + new_S_gain + 4*[h*(J(k1)-J(k0))-(C1^5-C0^5)/5+integral_(k0,k1) (h-k)*(-3*b*(k^2+K)/2+b^3/2) dk] + integral_(q+k1,a) Z_polynomial(t) dt',
                J='k*(2*k^2+5*K)*sqrt(k^2+K)/8 + 3*K^2*log(k+sqrt(k^2+K))/8',
                inherited_Z_gain=str(priorZ),inherited_S_gain=str(priorS),new_S_gain=str(sgain),
                Z_polynomial=[str(z) for z in zpolynomial.c],
                root_polynomial=[str(z) for z in integrand_poly.c],
                revenue_interval=rounded_interval(R),gain_interval=rounded_interval(gain),
                upper_gap_interval=rounded_interval(I(upper)-R),
                t0_interval=rounded_interval(k0+q),t1_interval=rounded_interval(k1+q),
                t2=str(F(2,3)),t3=str(cutoff),
                log_ratio_interval=rounded_interval(logratio),
                sqrt_digits=45,log_series_terms=18)


if __name__=='__main__':
    data=calculate()
    path=Path(__file__).parents[1]/'certificate'/'joined_threshold.json'
    if '--write' in sys.argv:path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:require(json.loads(path.read_text(encoding='utf-8'))==data,'exact revenue certificate replay')
    for key in ('revenue_interval','gain_interval','upper_gap_interval','t0_interval','t1_interval'):
        print(key,data[key],[float(F(x)) for x in data[key]])
    print('PASS exact interval/log remainder, symbolic transition identities, strict gain')
