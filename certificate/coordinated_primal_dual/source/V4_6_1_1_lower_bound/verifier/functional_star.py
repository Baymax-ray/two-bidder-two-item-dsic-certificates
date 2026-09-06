"""Admissible pointwise kernel optimizer with exact algebraic-root decisions.

The implicit inverse is an explicitly isolated simple real polynomial root.
Zero comparisons use exact polynomial gcds; all other comparisons refine
rational enclosures. No floating decision is made.
"""
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
from itertools import product
import json,random,sys
import functional_kernel as K
import functional_jump as jump
P,X,I=K.P,K.X,K.I
ROOT=Path(__file__).resolve().parents[1]
c,q,A,b,d=K.c,K.q,K.A,K.b,K.d

def compose(p,inner):
    out=P(0)
    for co in reversed(P(p).c):out=out*inner+co
    return out

def star_integral(terms=28):
    lo,hi=K.kappa_bracket(140);width=K.V-c
    ap=compose(K.AA,c+width*X);bp=compose(K.BB,c+width*X)
    center=K.ev(K.BB,(c+K.V)/2);ep=1-bp*F(1,center)
    ec=K.bernstein(ep,0,1);rho=max(abs(v) for v in ec);assert rho<F(3,50)
    total=P(1);power=P(1)
    for _ in range(terms):power=power*ep;total=total+power
    integrand=ap*ap*total*F(width,4*center)
    lower=integrand.integral(0,(lo-c)/width);upper=integrand.integral(0,(hi-c)/width)
    tail=rho**(terms+1)/(1-rho)*(K.AA*K.AA).integral(c,K.V)/(4*center)
    assert 0<tail<F(1,10**39)
    return I(lower-tail,upper+tail),{'highest_geometric_power':terms,'summands':terms+1,'rho_bound':str(rho),'remainder_bound':K.old.tools.rounded_interval(I(tail),48)}

def trim(p):
    a=list(P(p).c)
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def rem(a,b):
    a=trim(a);b=trim(b)
    while len(a)>=len(b) and any(a):
        v=a[-1]/b[-1];off=len(a)-len(b)
        for j,z in enumerate(b):a[j+off]-=v*z
        while len(a)>1 and a[-1]==0:a.pop()
    return P(a)

def gcd(a,b):
    a,b=P(a),P(b)
    while any(b.c):
        r=rem(a,b)
        if any(r.c):r=r*F(1,r.c[-1])
        a,b=b,r
    return a*F(1,a.c[-1])

def interval_poly(p,lo,hi):
    out=I();x=I(lo,hi)
    for co in reversed(P(p).c):out=out*x+co
    return out

class Root:
    def __init__(self,t):
        self.t=F(t);self.poly=2*K.BB*(X+q-self.t)+K.AA
        self.lo,self.hi=c,self.t-q;self.signs={}
        assert K.ev(self.poly,self.lo)<0<K.ev(self.poly,self.hi)
    def refine(self):
        mid=(self.lo+self.hi)/2;v=K.ev(self.poly,mid)
        if v<0:self.lo=mid
        elif v>0:self.hi=mid
        else:self.lo=self.hi=mid
    def sign(self,p):
        p=P(p);key=p.c
        if key in self.signs:return self.signs[key]
        if not any(p.c):return 0
        if self.lo==self.hi:
            val=K.ev(p,self.lo);ans=(val>0)-(val<0);self.signs[key]=ans;return ans
        iv=interval_poly(p,self.lo,self.hi)
        if iv.lo>0:self.signs[key]=1;return 1
        if iv.hi<0:self.signs[key]=-1;return -1
        common=gcd(self.poly,p)
        if len(common.c)>1 and K.ev(common,self.lo)*K.ev(common,self.hi)<0:
            self.signs[key]=0;return 0
        while True:
            self.refine()
            if self.lo==self.hi:
                val=K.ev(p,self.lo);ans=(val>0)-(val<0);break
            iv=interval_poly(p,self.lo,self.hi)
            if iv.lo>0:ans=1;break
            if iv.hi<0:ans=-1;break
        self.signs[key]=ans;return ans

class Value:
    def __init__(self,root,p):self.root,self.p=root,P(p)
    def other(self,x):
        if isinstance(x,Value):assert x.root is self.root;return x.p
        return P(F(x))
    def __add__(self,x):return Value(self.root,self.p+self.other(x))
    __radd__=__add__
    def __neg__(self):return Value(self.root,-self.p)
    def __sub__(self,x):return self+-Value(self.root,self.other(x))
    def __rsub__(self,x):return Value(self.root,self.other(x))+-self
    def __mul__(self,x):return Value(self.root,self.p*self.other(x))
    __rmul__=__mul__
    def __eq__(self,x):return self.root.sign(self.p-self.other(x))==0
    def __lt__(self,x):return self.root.sign(self.p-self.other(x))<0
    def __le__(self,x):return self.root.sign(self.p-self.other(x))<=0
    def __gt__(self,x):return self.root.sign(self.p-self.other(x))>0
    def __ge__(self,x):return self.root.sign(self.p-self.other(x))>=0
    def __repr__(self):return 'poly('+','.join(map(str,self.p.c))+'); root_t='+str(self.root.t)

@lru_cache(maxsize=4096)
def inverse_root(t):return Root(t)

def g(x):
    if not c<=x<=K.V:return F()
    val=K.ev(K.AA,x)
    return max(F(),val)/(2*K.ev(K.BB,x))
def h(x):return x+q+g(x)
def hinv(t):
    if t<=d:return t-q
    if t<=h(c):return c
    if t-q>=K.V or K.ev(K.AA,t-q)<=0:return t-q
    return Value(inverse_root(t),X)

def menu(opponent):
    x,y=tuple(opponent);t=max(x,y);rho=min(x,y);zz=x+y
    rows,branch=jump.base.menu(opponent)
    if branch=='Q_constrained':
        k=hinv(t);C0=F(5,6)+F(3,4)*k*k;C=max(C0,zz);B=C-k
        assert B>=h(rho)
        hi=0 if x>y else 1;scarce=tuple(F(j==hi) for j in (0,1));safe=tuple(1-j for j in scarce)
        return ((F(0),(F(0),F(0)),'empty'),(B,safe,'safe'),(A,scarce,'scarce'),(C,(F(1),F(1)),'bundle')),'Q_star'
    if branch=='base' and g(rho)>0:
        low=0 if x<y else 1;safe=tuple(F(j==low) for j in (0,1));fee=g(rho)
        return tuple((p+(fee if alloc==safe or alloc==(1,1) else 0),alloc,tag) for p,alloc,tag in rows),'base_star'
    return rows,branch

def mechanism(profile):return jump.select(profile,menu)

def verify():
    integral,meta=star_integral()
    affine=(K.AA*K.GG-K.BB*K.GG*K.GG).integral(c,K.END)
    assert integral.lo>affine+F(47,10**11)
    assert integral.hi<affine+F(535,10**12)
    clean=I(F(482935538268336599,574087500000000000))+F(31,1215)*K.old.square(2)-F(170368,664453125)*K.old.square(11)
    rv=clean+integral
    previous=clean+F(68161978301,216000000000000000)
    checks=ties=0;rng=random.Random(461112)
    for _ in range(300):mechanism(tuple(F(rng.randrange(1001),1000) for j in range(4)));checks+=1
    for t in (F(523,1000),F(21,40),F(527,1000),F(529,1000)):
        for rho in (F(0),c,c+F(1,1000),K.END,b-t):
            for x,y in product((c,c+F(1,1000),F(13,40),A,F(1)),(c,F(1,2),F(1))):
                mechanism((t,rho,x,y));mechanism((x,y,t,rho));checks+=2
    for x in (c+F(1,1000),F(8,25),F(13,40),F(33,100),F(17,50)):
        t=h(x);k=hinv(t);assert k==x;ties+=1
        for rho in (F(0),c,b-t):
            mechanism((t,rho,x,F(1)));checks+=1
    for t in (d,d+g(c)/2,h(c),h(c)+F(1,1000000)):
        for x in (c-F(1,1000000),c,c+F(1,1000000)):
            mechanism((t,F(1,10),x,F(1)));checks+=1
    data={'status':'FUNCTIONAL_STAR_EXACT_PASS','scope':'Explicit globally feasible analytic candidate; optimum of the named sufficient h family, not the full auction',
      'right_jump_height':str(g(c)),'jump_plateau_t_interval':[str(d),str(h(c))],
      'inverse_polynomial':'2 B(k) (k+q-t)+A(k)=0, unique root in (c,t-q) when not on plateau or unchanged branch',
      'root_decision_method':'rational interval refinement; polynomial gcd detects exact ties; uniqueness follows from certified h monotonicity',
      'exact_revenue':'clean_radical_expression + integral_c^kappa A(x)^2/(4B(x)) dx',
      'integral_interval':K.old.tools.rounded_interval(integral,30),'revenue_interval':K.old.tools.rounded_interval(rv,30),
      'gain_over_V4_6_1_interval':K.old.tools.rounded_interval(rv-previous,30),'advantage_over_affine_interval':K.old.tools.rounded_interval(integral-affine,30),
      'quadrature_certificate':meta,'rational_profile_checks':checks,'exact_algebraic_root_ties':ties,
      'proof':'research_log/functional_jump.md'}
    path=ROOT/'certificate/functional_star.json'
    if '--write' in sys.argv:path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text(encoding='utf-8'))==data
    print(data['status']);print('revenue',data['revenue_interval']);print('gain_over_previous',data['gain_over_V4_6_1_interval']);print('checks',checks,'ties',ties)
    return data
if __name__=='__main__':
    if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O')
    verify()
