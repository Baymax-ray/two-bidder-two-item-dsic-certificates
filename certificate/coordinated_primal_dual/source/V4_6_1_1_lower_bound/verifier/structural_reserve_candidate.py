"""Complete reserve-above-A candidate and exact alternative lower bound."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O')
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verifier'))
import structural_reserve as integral
import structural_split as outside
p=integral.p;v3=p.tools
A=F(2,3);c=F(47,150);d=F(1,2);q=d-c
nu=(1-2*c)**2/8;a=A+nu;b=a+c;s=a+d;T=1-2*c/3;U=F(5,3)-2*c
B0=v3.Quad(F(4,3),-F(1,3),2)

def menu(w,cap_safe=False):
    t,rho=max(w),min(w)
    high=0 if w[0]>w[1] else 1
    scarce=tuple(F(j==high) for j in (0,1));safe=tuple(1-z for z in scarce)
    if t<=A and sum(w)<=b:
        if t<=d:
            C=max(B0,v3.asquad(sum(w)))
            return ((0,(0,0)),(A,(1,0)),(A,(0,1)),(C,(1,1)))
        k=t-q;C=max(F(5,6)+F(3,4)*k*k,sum(w));B=min(A,C-k) if cap_safe else C-k;return ((0,(0,0)),(B,safe),(A,scarce),(C,(1,1)))
    if A<t<T and rho<c:
        dl=F(9,16)*(T-t)*(U-t);alpha=3*t-2;beta=alpha/(alpha+2*dl)
        lot=tuple(F(1) if j==high else beta for j in (0,1))
        return ((0,(0,0)),(d+dl,safe),(t,scarce),(t+c+dl,(1,1)),(t+beta*c,lot))
    H=max(0,w[0]-a,w[1]-a,sum(w)-b)
    return ((0,(0,0)),(H+min(a,s-w[1]),(1,0)),(H+min(a,s-w[0]),(0,1)),(H+b,(1,1)))

def mechanism(profile,cap_safe=False):
    own=(tuple(map(F,profile[:2])),tuple(map(F,profile[2:])))
    menus=[menu(own[1-i],cap_safe) for i in (0,1)];maxs=[];utilities=[]
    for i in (0,1):
        vals=[sum((x*y for x,y in zip(own[i],alloc)),F())-price for price,alloc in menus[i]]
        u=max(vals);utilities.append(u);maxs.append([0] if u==0 else [j for j,v in enumerate(vals) if v==u])
    pair=next(((j,k) for j,k in product(*maxs) if all(menus[0][j][1][ell]+menus[1][k][1][ell]<=1 for ell in (0,1))),None)
    assert pair is not None,'Structural continuous feasibility theorem'
    rows=[menus[i][pair[i]] for i in (0,1)]
    return dict(allocations=tuple(row[1] for row in rows),payments=tuple(row[0] for row in rows),utilities=tuple(utilities))

def exact_revenue():
    X,P=p.X,p.P;k=X-q;C0=P(F(5,6))+F(3,4)*k*k
    Ri=P(F(59,108))+F(1,4)*k*k-k**3+F(9,16)*k**4
    dl=F(9,16)*(T-X)*(U-X);D=4*(b-F(5,6))/3
    rational=outside.outer_base(a,c,d)+4*p.ratint((b-X)*Ri,d,A)+4*c*p.ratint(p.G(X,P(d),X+c)+dl*dl,A,T)
    add,mul,scale=p.pair_add,p.pair_mul,p.pair_scale
    RF=(F(4,9),F(2,27));B0pair=(F(4,3),-F(1,3))
    low=scale(RF,2*(d*d-(2*d-b)**2/2))
    low=add(low,scale(p.pair_integral((1-X)*p.G(P(A),P(A),X),B0pair,(b,F()),2),2))
    low=add(low,scale(mul(RF,p.pair_integral(1-X,B0pair,(b,F()),2),2),-2))
    cost=scale(p.pair_integral((b-C0)**3,(d,F()),(q,F(1)),D),-F(4,3))
    coeff=(rational+low[0]+cost[0],low[1],cost[1])
    value=p.I(coeff[0])+coeff[1]*p.square(2)+coeff[2]*p.square(D)
    old=integral.revenue(a,c)
    assert max(value.lo,old.lo)<min(value.hi,old.hi)
    return coeff,D,value

def verify():
    assert a==F(3848,5625) and 0<c<d<A<a<b<1 and a-A==nu
    assert A-q<d and F(5,6)+F(3,4)*(A-q)**2-(A-q)>d
    assert F(5,6)+F(3,4)*c*c>=d+c
    # The exact minimum guard for excluding E lotteries at Q types.
    dlA=F(3,16)*(1-2*c)**2
    assert nu==2*dlA/3 and F(1,2)+c>0 and F(1,4)+F(3,2)*c>0
    types=((F(),F()),(d,F()),(F(11,25),F(11,25)),(A,b-A),(a,F(1,10)),(F(7,10),c),(F(7,10),c-F(1,10000)),(F(1),F(1)),(A,F()))
    count=0
    for w,v in product(types,repeat=2):mechanism(w+v);count+=1
    for t in (A,A+F(1,100000),a,T-F(1,100000)):
      for r in (F(),c-F(1,100000),c):
       for x in (t-q,A,t):
        for y in (c,d,F(1)):
          mechanism((t,r,x,y));count+=1
    coeff,D,value=exact_revenue()
    baseline=json.loads((ROOT.parent/'V4_6_1_lower_bound/certificate/branch_summary.json').read_text(encoding='utf-8'))
    lo,hi=map(F,baseline['revenue_enclosure']);gain=value-p.I(lo,hi);assert gain.lo>F(5,10**7)
    data=dict(status='STRUCTURAL_RESERVE_ABOVE_A_EXACT_PASS',
      scope='alternative complete feasible mechanism; no full conditional or outer optimizer claim',
      parameters={name:str(z) for name,z in dict(A=A,a=a,c=c,b=b,d=d,q=q,s=s,nu=nu).items()},
      revenue_coefficients=list(map(str,coeff)),basis=['1','sqrt(2)','sqrt('+str(D)+')'],
      revenue_interval=p.tools.rounded_interval(value,30),gain_over_V4_6_1_interval=p.tools.rounded_interval(gain,30),
      pointwise_cases=count,proof='research_log/structural_compatibility.md',
      missing_optimality='E junction support can fail when a>A; actual full-inner optimization not certified')
    target=ROOT/'certificate/structural_reserve_candidate.json'
    if '--write' in sys.argv:target.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(target.read_text(encoding='utf-8'))==data
    print(data['status']);print('revenue',data['revenue_interval']);print('gain',data['gain_over_V4_6_1_interval']);return data
def capped_mechanism(profile):return mechanism(profile,True)

def verify_cap():
    coeff,D,value=exact_revenue();eta=nu
    assert F(5,6)+F(3,4)*(c+eta)**2<A+c
    gain=c*eta**4/2+eta**5/5
    X=p.X
    direct=p.ratint(2*(X-q)*(d+eta-X)**3+F(1,2)*(d+eta-X)**4,d,d+eta)
    assert gain==direct>0
    count=0
    for t in (d,d+eta/2,d+eta):
      for rho in (A-q,(A-q+b-t)/2,b-t):
        if not 0<=rho<=t:continue
        for v in ((F(),F()),(F(1),F(1)),(A,F()),(t-q,F(1)),(F(1,2),t+rho-F(1,2))):
          for profile in ((t,rho)+v,v+(t,rho)):
            capped_mechanism(profile);count+=1
    final=(coeff[0]+gain,coeff[1],coeff[2]);r=value+gain
    data=dict(status='STRUCTURAL_SAFE_CAP_EXACT_PASS',
       scope='complete pointwise feasible safe-price cap; full diagonal support restored on cap rows C=sum(w)',
       incremental_gain=str(gain),uncapped_reference='certificate/structural_reserve_candidate.json',
       revenue_coefficients=list(map(str,final)),basis=['1','sqrt(2)','sqrt('+str(D)+')'],
       revenue_interval=p.tools.rounded_interval(r,30),pointwise_cases=count,
       proof='research_log/structural_compatibility.md Section 9')
    target=ROOT/'certificate/structural_reserve_cap.json'
    if '--write' in sys.argv:target.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(target.read_text(encoding='utf-8'))==data
    print(data['status']);print('cap_gain',gain,float(gain));print('revenue',data['revenue_interval']);return data
if __name__=='__main__':
    if '--cap' in sys.argv:verify_cap()
    else:verify()
