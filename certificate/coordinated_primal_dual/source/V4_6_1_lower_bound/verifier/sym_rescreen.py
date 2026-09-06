"""Exact V4.6 bidder-symmetry and unrestricted G-fiber rescreen experiment."""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import json,sys
if not __debug__ or sys.flags.optimize: raise RuntimeError("Run without -O")
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V4_6/verifier'))
import price_joint_reallocation as old
import inner_diagonal_capacity as inner
v3=old.baseline.v3
A,a,b,c,d,q=F(2,3),F(159,250),F(91,100),F(137,500),F(1,2),F(113,500)
B0=v3.Quad(F(4,3),-F(1,3),2)

def scale(x,z):
    if isinstance(z,v3.Quad): return v3.Quad(x*z.r,x*z.s,z.w)
    return x*z

def in_G(w): return max(w)<=d and B0<sum(w)<b

def symmetrized(profile):
    v,w=tuple(map(F,profile[:2])),tuple(map(F,profile[2:]))
    l,r=old.mechanism(v+w),old.mechanism(w+v)
    return dict(allocations=tuple(tuple((l['allocations'][i][j]+r['allocations'][1-i][j])/2 for j in (0,1)) for i in (0,1)),
                payments=tuple(scale(F(1,2),l['payments'][i]+r['payments'][1-i]) for i in (0,1)),
                utilities=tuple(scale(F(1,2),l['utilities'][i]+r['utilities'][1-i]) for i in (0,1)))

def mechanism(profile):
    v,w=tuple(map(F,profile[:2])),tuple(map(F,profile[2:]))
    row=symmetrized(v+w)
    if not in_G(w): return row
    prices=(F(),A,A,sum(w)); vals=[v3.base.value(v,m)-p for m,p in enumerate(prices)]
    best=max(vals); chosen=next(m for m,u in enumerate(vals) if u==best)
    row['allocations']=(tuple(F(bool(chosen&(1<<j))) for j in (0,1)),row['allocations'][1])
    row['payments']=(prices[chosen],row['payments'][1]);row['utilities']=(best,row['utilities'][1])
    assert all(sum(z[j] for z in row['allocations'])<=1 for j in (0,1))
    return row

def pair_add(x,y): return x[0]+y[0],x[1]+y[1]
def pair_mul(x,y): return x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def pair_scale(a,x):return a*x[0],a*x[1]
def evaluate(poly,z):
    ans=(F(),F());power=(F(1),F())
    for co in poly:
        ans=pair_add(ans,pair_scale(co,power));power=pair_mul(power,z)
    return ans

def pair_interval(x):
    n=10**55;m=isqrt(2*n*n);assert m*m<2*n*n<(m+1)**2
    r,s=x;lo,hi=F(m,n),F(m+1,n)
    return (r+s*lo,r+s*hi) if s>=0 else (r+s*hi,r+s*lo)

def calculate():
    h=A-a
    # Half the all-real conditional value gap, weighted by exact G cross-section 1-z.
    gap=[h*h*(-2+2*h)/2,3*h*h/2]
    density=[gap[0],gap[1]-gap[0],-gap[1]]
    primitive=[F()]+[z/F(j+1) for j,z in enumerate(density)]
    gain=pair_add(evaluate(primitive,(b,F())),pair_scale(-1,evaluate(primitive,(F(4,3),-F(1,3)))))
    lo,hi=pair_interval(gain);assert lo>0
    checks=0
    own=((F(),F()),(F(1),F(1)),(a,F(1,5)),(A,F(1,5)),(F(13,20),F(1,10)),
         (F(1,2),F(39,100)),(F(51,100),F(38,100)),(F(7,10),c),(F(7,10),c-F(1,1000)))
    opponents=((F(11,25),F(11,25)),(F(1,2),F(37,100)),(F(9,20),F(9,20)))
    for w in opponents:
        assert in_G(w)
        s=sum(w)
        assert inner.revenue(A,A,s)-inner.revenue(a,a,s)==h*h*(3*s-2+2*h)
        inner.replay(A,s,inner.candidate(A,s))
        for v in own:
            for profile in (v+w,tuple(reversed(v))+tuple(reversed(w))):
                before=symmetrized(profile);after=mechanism(profile)
                assert after['allocations'][1]==before['allocations'][1]
                assert after['payments'][1]==before['payments'][1]
                checks+=1
        for v in ((F(1,4),F()),(F(1,2),(s-F(1,2))/2)):
            before=symmetrized(v+w)
            assert before['allocations'][1]==(1,1)
            checks+=1
    witness=(F(13,20),F(1,10),F(11,25),F(11,25))
    bef,aft=symmetrized(witness),mechanism(witness)
    assert bef['allocations'][0]==(F(1,2),0) and aft['allocations'][0]==(0,0)
    return dict(status='SYM_G_FULL_RANDOMIZED_RESCREEN_PASS',
      scope='literal bidder-symmetrization of strongest V4.6; bidder 2 held pointwise fixed; full inner optimum on G only',
      exact_gain_pair=list(map(str,gain)),field='sqrt(2)',gain_interval=list(map(str,(lo,hi))),
      conditional_gap='(2/3-a)^2*(3*z-2+2*(2/3-a))/2',
      proof='research_log/sym_rescreen.md',pointwise_checks=checks,
      witness=dict(profile=list(map(str,witness)),old=[[str(z) for z in x] for x in bef['allocations']],new=[[str(z) for z in x] for x in aft['allocations']]))
if __name__=='__main__':
    data=calculate();p=ROOT/'certificate/sym_rescreen.json'
    if '--write' in sys.argv:p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(p.read_text(encoding='utf-8'))==data
    print(data['status']);print('gain',float(F(data['gain_interval'][0])));print('pair',data['exact_gain_pair'])
