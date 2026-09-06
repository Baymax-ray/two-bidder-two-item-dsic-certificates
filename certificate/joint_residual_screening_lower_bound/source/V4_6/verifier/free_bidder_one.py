"""Complete reverse free-capacity splice and exact Q(sqrt2) gain."""
from fractions import Fraction as F
from itertools import product
from math import isqrt
from pathlib import Path
import json,sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O')
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verifier'))
import outer_lottery_strip as strip
v3=strip.previous.old.v3
A,B,D=F(159,250),F(91,100),F(1,2)
B0=v3.Quad(F(4,3),-F(1,3),2)
PRICES=(v3.Quad(),v3.Quad(F(2,3)),v3.Quad(F(2,3)),B0)

def in_free(opponent):
    return max(opponent)<=D and sum(opponent)<=B0

def mechanism(profile):
    profile=tuple(map(F,profile))
    before=strip.mechanism(profile)
    if not in_free(profile[2:]):
        return before
    assert before['allocations'][1]==(0,0)
    values=[v3.base.value(profile[:2],m)-p for m,p in enumerate(PRICES)]
    maximum=max(values)
    chosen=next(m for m,val in enumerate(values) if val==maximum)
    row=dict(before)
    row.update(allocations=(tuple(F(bool(chosen&(1<<j))) for j in (0,1)),before['allocations'][1]),
               payments=(PRICES[chosen],before['payments'][1]),
               utilities=(maximum,before['utilities'][1]),free_bidder_one_mask=chosen)
    return row

def mul(x,y): return (x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def scale(z,x): return z*x[0],z*x[1]
def add(x,y): return x[0]+y[0],x[1]+y[1]
def interval(x,digits=50):
    n=10**digits
    m=isqrt(2*n*n)
    assert m*m<2*n*n<(m+1)*(m+1)
    lo,hi=F(m,n),F(m+1,n)
    r,s=x
    return (r+s*lo,r+s*hi) if s>=0 else (r+s*hi,r+s*lo)

def calculate():
    area=(F(1,12),F(1,9))
    revenue_sja=(F(4,9),F(2,27))
    revenue_old=F(136719583,250000000)
    # Separate direct symmetric-menu area formula with pair arithmetic.
    def rev(a,b):
        one=(F(1),F())
        sub=lambda x,y:add(x,scale(-1,y))
        single=mul(sub(one,a),sub(b,a))
        side=add(sub(one,b),a)
        corner=sub(scale(2,a),b)
        bundle=sub(mul(side,side),scale(F(1,2),mul(corner,corner)))
        return add(scale(2,mul(a,single)),mul(b,bundle))
    assert rev((A,F()),(B,F()))==(revenue_old,F())
    assert rev((F(2,3),F()),(F(4,3),-F(1,3)))==revenue_sja
    gain=mul(area,(revenue_sja[0]-revenue_old,revenue_sja[1]))
    assert gain==(F(1925713777,243000000000),-F(11719583,2250000000))
    assert interval(gain)[0]>F(5585,10000000)
    assert B0<B and F(4,5)<B0<1 and D<F(2,3)
    assert all(F(row['high_interval'][0])>v3.d for row in v3.base.DATA['common_rows'])
    q=strip.previous.q
    km=F(2,3)-q
    safe=F(5,6)+F(3,4)*km*km-km
    assert safe>D and F(5,6)+F(3,4)*v3.c*v3.c>B0
    assert F(2,3)+v3.c>B
    count=0
    own_nodes=((F(0),F(0)),(F(1),F(1)),(F(7,10),F(1,4)),
               (F(9,20),F(9,20)),(F(2,3),F(1,5)),(F(1,2),F(2,5)))
    opp_nodes=((F(0),F(0)),(D,F(0)),(F(2,5),F(2,5)),
               (D,F(1,3)),(F(43,100),F(43,100)),(F(1,3),D))
    for own,opp in product(own_nodes,opp_nodes):
        assert in_free(opp)
        old=strip.mechanism(own+opp)
        assert old['allocations'][1]==(0,0)
        assert tuple(strip.previous.old.retained_menu(opp,strip.previous.old.CANDIDATE_THETA))==tuple(map(v3.asquad,(0,A,A,B)))
        mechanism(own+opp)
        mechanism(opp+own)
        count+=2
    # Actual all-empty witnesses for each conditional branch and both rotations.
    branches=((F(0),F(0)),(F(1,2),F(2,5)),(F(3,5),F(1,4)),
              (F(7,10),F(1,4)),(F(4,5),F(27,100)),(F(1),F(0)),(F(1),F(1)))
    for opp,own in product(branches,opp_nodes):
        for profile in (opp+own,tuple(reversed(opp))+tuple(reversed(own))):
            before=strip.mechanism(profile)
            assert before['allocations'][1]==(0,0)
            mechanism(profile)
            count+=1
    # Exact irrational boundary utility, evaluated algebraically rather than rounded.
    corner=(v3.Quad(D),B0-D)
    assert max(v3.base.value(corner,m)-p for m,p in enumerate(PRICES))==0
    witness=(F(9,20),F(9,20),F(1,10),F(1,10))
    before,after=strip.mechanism(witness),mechanism(witness)
    assert before['allocations']==((0,0),(0,0)) and after['allocations']==((1,1),(0,0))
    ext=strip.exact_gain()
    lo,hi=map(F,ext['revenue_interval'])
    gl,gh=interval(gain)
    return dict(scope='full randomized conditional optimum on F; exact feasible lower improvement; no auction optimum',
                area_pair=list(map(str,area)), gain_pair=list(map(str,gain)),
                gain_interval=list(map(str,(gl,gh))),
                total_revenue_interval=list(map(str,(lo+gl,hi+gh))),
                rational_boundary_checks=count,
                witness=dict(profile=list(map(str,witness)),old_allocations=[[str(x) for x in a] for a in before['allocations']],
                             new_allocations=[[str(x) for x in a] for a in after['allocations']],payment=str(after['payments'][0])),
                no_sale_set='max(v)<=1/2 and sum(v)<=(4-sqrt(2))/3, closed boundaries included')
if __name__=='__main__':
    data=calculate()
    path=ROOT/'certificate/free_bidder_one.json'
    if '--write' in sys.argv:path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text(encoding='utf-8'))==data
    print('FREE_BIDDER_ONE_EXACT_PASS')
    print('gain_pair',data['gain_pair'])
    print('gain_display',float(F(data['gain_interval'][0])))
    print('total_display',float(F(data['total_revenue_interval'][0])))
