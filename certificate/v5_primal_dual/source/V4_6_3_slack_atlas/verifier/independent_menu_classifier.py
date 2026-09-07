"""Rational outer classifier for the frozen V4.6.1.1 mechanism.

classify(bounds, charts): four PHYSICAL-coordinate Fraction interval pairs;
charts gives the high physical item (0 or 1) for each bidder. The actual
cell is assumed to obey those two chart inequalities. Interval products
are outer bounds; exact analytic pairwise differences preserve shared
price cancellation. Weak whole-cell dominance identifies allocations
a.e.; complete pointwise ties remain owned by the frozen mechanism.
"""
from fractions import Fraction as F
from math import isqrt
from itertools import combinations
from pathlib import Path
import sys,json
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O')
ROOT=Path(__file__).resolve().parents[1]
A,d,c=F(2,3),F(1,2),F(157,500)
q=d-c;nu=q*q/2;a=A+nu;b=a+c;s=a+d
eta,end=F(4,5),F(3421,10000)
T=1-2*c/3;U=F(5,3)-2*c
scale=10**50;rt=isqrt(2*scale*scale)

class I:
    __slots__=('lo','hi')
    def __init__(self,lo,hi=None):
        if isinstance(lo,I):self.lo,self.hi=lo.lo,lo.hi;return
        if hi is None and isinstance(lo,(tuple,list)):lo,hi=lo
        self.lo=F(lo);self.hi=F(lo if hi is None else hi)
        assert self.lo<=self.hi
    def __add__(self,o):o=I(o);return I(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,o):return self+-I(o)
    def __rsub__(self,o):return I(o)+-self
    def __mul__(self,o):
        o=I(o);v=(self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi);return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=I(o);assert o.lo>0 or o.hi<0
        return self*I(1/o.hi,1/o.lo)
    def pair(self):return self.lo,self.hi
    def __repr__(self):return f'I({self.lo},{self.hi})'

def imax(*xs):
    xs=[I(x) for x in xs];return I(max(x.lo for x in xs),max(x.hi for x in xs))
def imin(*xs):
    xs=[I(x) for x in xs];return I(min(x.lo for x in xs),min(x.hi for x in xs))
def square(x):
    x=I(x)
    if x.lo>=0:return I(x.lo*x.lo,x.hi*x.hi)
    if x.hi<=0:return I(x.hi*x.hi,x.lo*x.lo)
    return I(0,max(x.lo*x.lo,x.hi*x.hi))
def restrict(x,lo,hi):return I(max(x.lo,F(lo)),min(x.hi,F(hi)))
def exact_g(x):return eta*(end-x) if c<=x<=end else F()
def exact_h(x):return x+q+exact_g(x)
HC,HU=exact_h(c),exact_h(end)
def exact_inverse(t):
    if t<=d:return t-q
    if t<=HC:return c
    if t<HU:return (t-q-eta*end)/(1-eta)
    return t-q
def g_range(x):
    if x.hi<c or x.lo>end:return I(0)
    hi=eta*(end-max(c,x.lo))
    lo=eta*(end-x.hi) if c<=x.lo<=x.hi<=end else F()
    return I(lo,hi)
def h_range(x):return I(exact_h(x.lo),exact_h(x.hi))
def k_range(x):return I(exact_inverse(x.lo),exact_inverse(x.hi))
def increment_range(t):
    pts=[t.lo,t.hi]+[z for z in (d,HC,HU) if t.lo<=z<=t.hi]
    vals=[z-exact_inverse(z) for z in pts];return I(min(vals),max(vals))
def c0_range(k):return F(5,6)+F(3,4)*square(k)
def b0safe_range(k):
    fn=lambda v:F(5,6)+F(3,4)*v*v-v
    assert k.hi<=A
    return I(fn(k.hi),fn(k.lo))
B0=I((4-F(rt+1,scale))/3,(4-F(rt,scale))/3)

def row(tag,alloc,price):return dict(tag=tag,allocation=tuple(map(I,alloc)),price=I(price))
def candidate_branches(opp,hi):
    t,rho=opp[hi],opp[1-hi];z=sum(opp,I(0))
    Q=t.hi<=A and z.hi<=b
    E=t.lo>A and t.hi<T and rho.hi<c
    out=[]
    if t.lo<=d and z.lo<=b:out.append('Q_free')
    if t.hi>d and t.lo<=A and z.lo<=b:out.append('Q_constrained')
    if t.hi>A and t.lo<T and rho.lo<c:out.append('E')
    if not Q and not E:out.append('base')
    return out

def construct(branch,own,opp,hi):
    lo=1-hi;t,rho=opp[hi],opp[lo];z=sum(opp,I(0));vs,vl=own[hi],own[lo]
    units=((1,0),(0,1));empty=(0,0);both=(1,1)
    diffs={};scores={};meta={}
    def pair(k,l,value):diffs[k,l]=value;diffs[l,k]=-value
    if branch=='Q_free':
        C=imax(B0,restrict(z,0,b))
        rows=[row('empty',empty,0),row('item1',units[0],A),row('item2',units[1],A),row('bundle',both,C)]
        scores={'item1':own[0]-A,'item2':own[1]-A,'bundle':sum(own,I(0))-C}
        pair('item1','item2',own[0]-own[1])
        pair('bundle','item1',own[1]-(C-A));pair('bundle','item2',own[0]-(C-A))
    elif branch=='Q_constrained':
        t=restrict(t,d,A);rho=restrict(rho,0,A);z=restrict(z,0,b)
        k=k_range(t);C0=c0_range(k);C=imax(C0,z,k+h_range(rho))
        Braw=imax(b0safe_range(k),rho+increment_range(t),h_range(rho))
        B=imin(A,Braw);upgrade=imax(k,C-A)
        rows=[row('empty',empty,0),row('safe',units[lo],B),row('scarce',units[hi],A),row('bundle',both,C)]
        scores={'safe':vl-B,'scarce':vs-A,'bundle':sum(own,I(0))-C}
        pair('bundle','safe',vs-upgrade);pair('bundle','scarce',vl-(C-A))
        pair('safe','scarce',vl-vs+A-B)
        meta=dict(k=k.pair(),B=B.pair(),C=C.pair(),cap_status='capped' if Braw.lo>=A else 'uncapped' if Braw.hi<=A else 'crossing')
    elif branch=='E':
        t=restrict(t,A,T)
        delta=lambda x:F(9,16)*(T-x)*(U-x)
        beta=lambda x:(3*x-2)/(3*x-2+2*delta(x))
        yf=lambda x:c+delta(x)+(3*x-2)/2
        D=I(delta(t.hi),delta(t.lo));B=d+D
        C=I(t.lo+c+delta(t.lo),t.hi+c+delta(t.hi))
        betaI=I(beta(t.lo),beta(t.hi));Y=I(yf(t.lo),yf(t.hi))
        lp=I(t.lo+c*beta(t.lo),t.hi+c*beta(t.hi))
        lot=[I(1),I(1)];lot[lo]=betaI
        rows=[row('empty',empty,0),row('safe',units[lo],B),row('scarce',units[hi],t),row('bundle',both,C),row('lottery',lot,lp)]
        scores={'safe':vl-B,'scarce':vs-t,'bundle':sum(own,I(0))-C,'lottery':vs-t+betaI*(vl-c)}
        pair('bundle','safe',vs-(t-q));pair('bundle','scarce',vl-c-D)
        pair('safe','scarce',vl-vs+t-B)
        pair('lottery','scarce',betaI*(vl-c))
        pair('lottery','bundle',(1-betaI)*(Y-vl))
        pair('lottery','safe',vs-(t-q)+(1-betaI)*(Y-vl))
        meta=dict(beta=betaI.pair(),Y=Y.pair())
    elif branch=='base':
        x,y=opp;fee=g_range(rho);H=imax(0,x-a,y-a,z-b)
        def singleton(j):
            xx,yy=opp[j],opp[1-j]
            if yy.hi<=d:P=imax(a,xx,yy,xx+yy-c)
            elif yy.lo>=d:P=imax(s-yy,xx+d-yy,d,xx+q)
            else:P=H+imin(a,s-yy)
            return P+fee if j==lo else P
        P=[singleton(0),singleton(1)];C=imax(b,x+c,y+c,z)+fee
        rows=[row('empty',empty,0),row('item1',units[0],P[0]),row('item2',units[1],P[1]),row('bundle',both,C)]
        scores={'item1':own[0]-P[0],'item2':own[1]-P[1],'bundle':sum(own,I(0))-C}
        for j in (0,1):
            increment=imax(c,opp[1-j]-q)+(fee if j==hi else I(0))
            pair('bundle','item'+str(j+1),own[1-j]-increment)
        difference=imin(a,s-opp[1])-imin(a,s-opp[0])+(fee if lo==0 else -fee)
        pair('item1','item2',own[0]-own[1]-difference)
        meta=dict(fee=fee.pair())
    else:raise ValueError(branch)
    scores['empty']=I(0)
    for tag,value in scores.items():
        if tag!='empty':pair(tag,'empty',value)
    tags=[r['tag'] for r in rows]
    assert len(diffs)==len(tags)*(len(tags)-1)
    possible=[tag for tag in tags if not any(diffs[other,tag].lo>0 for other in tags if other!=tag)]
    assert possible,(branch,own,opp,hi,diffs)
    # Distinct allocations tie on null affine own-type sets. Any option
    # weakly dominating throughout the cell gives the actual allocation a.e.
    winners=[tag for tag in tags if all(diffs[tag,other].lo>=0 for other in tags if other!=tag)]
    ae=winners[0] if winners else None
    selected=[r for r in rows if r['tag']==ae] if ae else [r for r in rows if r['tag'] in possible]
    allocation=tuple((min(r['allocation'][j].lo for r in selected),max(r['allocation'][j].hi for r in selected)) for j in (0,1))
    return dict(branch=branch,possible=possible,ae_winner=ae,allocation=allocation,
                regime='lottery' if ae=='lottery' else 'deterministic' if ae else 'unresolved',
                rows=[dict(tag=r['tag'],allocation=[x.pair() for x in r['allocation']],price=r['price'].pair()) for r in rows],
                meta=meta,difference_bounds={key:value.pair() for key,value in diffs.items()})

def classify(bounds,charts):
    assert len(bounds)==4 and len(charts)==2 and all(x in (0,1) for x in charts)
    vals=tuple(map(I,bounds));assert all(0<=v.lo<=v.hi<=1 for v in vals)
    reports=(vals[:2],vals[2:]);sides=[]
    for i in (0,1):
        own,opp=reports[i],reports[1-i];hi=charts[1-i]
        branches=candidate_branches(opp,hi)
        menus=[construct(name,own,opp,hi) for name in branches]
        assert menus
        allocation=tuple((min(m['allocation'][j][0] for m in menus),max(m['allocation'][j][1] for m in menus)) for j in (0,1))
        semantic=set('Q' if name.startswith('Q_') else name for name in branches)
        sides.append(dict(branches=branches,region=next(iter(semantic)) if len(semantic)==1 else None,
                          menus=menus,allocation=allocation,
                          regime=menus[0]['regime'] if len(menus)==1 else 'unresolved'))
    region=tuple(side['region'] for side in sides)
    return dict(bidders=sides,region=region if all(x is not None for x in region) else None,
                allocation=tuple(side['allocation'] for side in sides),
                constant_allocation=all(lo==hi for side in sides for lo,hi in side['allocation']))

if __name__=='__main__':
    sys.path.insert(0,str(ROOT.parent/'V4_6_1_1_lower_bound/verifier'))
    import refined_candidate as frozen
    points=(F(1,10),c,F(315,1000),end,d,HC,HU,A,a,T,F(99,100))
    tested=0;boxes=0;regimes={}
    import random
    rng=random.Random(463)
    profiles=[tuple(F(rng.randrange(1,10000),10000) for _ in range(4)) for _ in range(500)]
    profiles += [(HC,c,F(315,1000),F(99,100)),(A,b-A,c,F(1)),(F(103,200),F(1,10),F(63,200),F(99,100))]
    for profile in profiles:
        charts=tuple(0 if profile[2*i]>profile[2*i+1] else 1 for i in (0,1))
        known=frozen.mechanism(profile)
        for radius in (F(),F(1,100000)):
            intervals=tuple((max(F(),v-radius),min(F(1),v+radius)) for v in profile)
            result=classify(intervals,charts);boxes+=1
            for i in (0,1):
                source,branch=frozen.menu(profile[2*(1-i):2*(1-i)+2])
                branch='Q_constrained' if branch=='Q_capped' else 'base' if branch=='base_fee' else branch
                audited=next(m for m in result['bidders'][i]['menus'] if m['branch']==branch)
                for ni,ri in enumerate(audited['rows']):
                  for nj,rj in enumerate(audited['rows']):
                    if ni==nj:continue
                    exact=sum((profile[2*i+k]*(source[ni][1][k]-source[nj][1][k]) for k in (0,1)),F())-source[ni][0]+source[nj][0]
                    low,high=audited['difference_bounds'][ri['tag'],rj['tag']]
                    assert low<=exact<=high,(profile,radius,branch,ri['tag'],rj['tag'],low,exact,high)
                for j in (0,1):
                    lo,hi=result['allocation'][i][j];val=known['allocations'][i][j]
                    # At exact ties an a.e. winner need not equal selected
                    # pointwise maximizer. Validate possible full argmax rows.
                    if not lo<=val<=hi:
                        rows=[r for m in result['bidders'][i]['menus'] for r in m['rows'] if r['tag'] in m['possible']]
                        assert any(r['allocation'][j][0]<=val<=r['allocation'][j][1] for r in rows),(profile,radius,i,j,result,known)
            tested+=1
            key=str(result['region']);regimes[key]=regimes.get(key,0)+1
    out=dict(status='INDEPENDENT_RATIONAL_MENU_CLASSIFIER_PASS',profile_centers=len(profiles),interval_boxes=boxes,
             exact_center_compatibility_checks=tested,regions=regimes,
             scope='Rational interval enclosure of all possible menu choices; a.e. winner is used only for Lebesgue slack integration, not to replace pointwise mechanism ties')
    path=ROOT/'certificate/independent_menu_classifier.json'
    if '--write' in sys.argv:path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text(encoding='utf-8'))==out
    print(out['status']);print('interval_boxes',boxes)
