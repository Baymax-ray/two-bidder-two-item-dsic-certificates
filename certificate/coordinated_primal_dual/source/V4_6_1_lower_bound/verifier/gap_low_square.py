"""Exact low-square conditional-gap elimination above the V4.6 baseline.

Normal execution is read-only. --write writes only this branch certificate.
The all-real proof is research_log/gap_low_square.md.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError("Run without -O.")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V4_6'/'verifier'))
import price_joint_reallocation as baseline
import outer_bundle_exchange as p

v3 = p.v3
A, a, b, c = F(2,3), F(159,250), F(91,100), F(137,500)
B0, ZMAX = p.B0, A+c


def in_region(opponent):
    return max(opponent) <= F(1,2) and B0 < sum(opponent) <= ZMAX


def mechanism(profile):
    profile = tuple(map(F,profile))
    assert len(profile) == 4 and all(0 <= z <= 1 for z in profile)
    row = dict(baseline.mechanism(profile))
    allocations = list(row['allocations'])
    payments, utilities = list(row['payments']), list(row['utilities'])
    selected = [None,None]
    for bidder in (0,1):
        own = profile[2*bidder:2*bidder+2]
        opponent = profile[2*(1-bidder):2*(1-bidder)+2]
        if not in_region(opponent):
            continue
        prices = tuple(map(v3.asquad,(0,A,A,sum(opponent))))
        values = [v3.base.value(own,mask)-prices[mask] for mask in range(4)]
        best = max(values)
        mask = next(j for j,value in enumerate(values) if value == best)
        allocations[bidder] = tuple(F(bool(mask&(1<<j))) for j in (0,1))
        payments[bidder], utilities[bidder], selected[bidder] = prices[mask],best,mask
    assert all(allocations[0][j]+allocations[1][j] <= 1 for j in (0,1))
    assert all(u >= 0 for u in utilities)
    row.update(allocations=tuple(allocations),payments=tuple(payments),
               utilities=tuple(utilities),gap_low_square_masks=tuple(selected))
    return row


def gap(z, bidder):
    """Exact conditional value minus the actual V4.6 conditional revenue."""
    z = F(z)
    assert B0 < z <= ZMAX and bidder in (0,1)
    if z <= b and bidder == 1:
        return F()
    old_single = a if z <= b else z-c
    distance = A-old_single
    return 3*distance*distance*(z-A)+2*distance**3


def calculate():
    X,Q,add,mul,scale = p.X,p.Q,p.add,p.mul,p.scale
    weight = add(Q(1),scale(X,-1))
    low = mul(weight,add(p.revenue_poly(Q(A),Q(A),X),
                        scale(p.revenue_poly(Q(a),Q(a),X),-1)))
    upper_price = add(X,Q(-c))
    high = mul(weight,add(p.revenue_poly(Q(A),Q(A),X),
                         scale(p.revenue_poly(upper_price,upper_price,X),-1)))
    low_pair = p.integral_from_b0(low)
    primitive = p.primitive(high)
    high_value = p.p.value(primitive,ZMAX)-p.p.value(primitive,b)
    coefficients = low_pair[0]+2*high_value, low_pair[1]
    assert low_pair == (F(30892611299,75937500000000),-F(180389,632812500))
    assert high_value == F(2999883353,4746093750000000)
    lo,hi = p.exact_interval((coefficients[0],coefficients[1],F()))
    assert F(49458,10**10) < lo < hi < F(49460,10**10)
    polygon_checks = 0
    for z in (F(87,100),F(9,10),b,F(92,100),F(93,100),ZMAX):
        for bidder in (0,1):
            old_single = A if bidder == 1 and z <= b else a if z <= b else z-c
            old_menu = [(F(),F(),F()),(F(1),F(),old_single),
                        (F(),F(1),old_single),(F(1),F(1),z)]
            new_menu = [(F(),F(),F()),(F(1),F(),A),
                        (F(),F(1),A),(F(1),F(1),z)]
            assert p.p.polygon_revenue(new_menu)[0]-p.p.polygon_revenue(old_menu)[0] == gap(z,bidder)
            polygon_checks += 1
    # The diagonal-hole support extends without a hypothesis change up to ZMAX.
    kmax = ZMAX-A
    assert 0 < kmax < F(1,2) < A
    # m(z)=1/3-3/2(4/3-z)^2 is nonnegative on [b0,ZMAX].
    assert B0 < ZMAX < F(4,3)
    assert F(1,3)-F(3,2)*(F(4,3)-ZMAX)**2 > 0
    return dict(field_basis=['1','sqrt(2)'],gain_coefficients=list(map(str,coefficients)),
                exact_gain_interval=list(map(str,(lo,hi))),
                bidder_one_below_b_pair=list(map(str,low_pair)),
                each_bidder_above_b_gain=str(high_value),
                integrated_polynomial_below_b={str(j):str(v) for j,v in sorted(low.items())},
                integrated_polynomial_above_b={str(j):str(v) for j,v in sorted(high.items())},
                polygon_checks=polygon_checks,
                conditional_gap='3*(2/3-P)^2*(z-2/3)+2*(2/3-P)^3',
                old_singleton='P=a for bidder1 z<=b; P=A for bidder2 z<=b; P=z-c for both z>b',
                full_inner_scope='Both bidders: opponent max<=1/2 and sum<=1411/1500 after replacement, including inherited F')


def verify():
    cases = 0
    own_points = ((F(),F()),(F(1),F(1)),(a,F()),(A,F()),
                  (A,F(1,5)),(F(7,10),c),(F(1,2),F(2,5)),
                  (F(7,10),F(1,10)),(F(1,10),F(7,10)))
    for z in (F(87,100),F(9,10),b,F(92,100),F(93,100),ZMAX):
        for opponent in ((F(1,2),z-F(1,2)),(z/2,z/2)):
            for own in own_points+((z/2,z/2),(A,z-A),(z-A,A)):
                for profile in (own+opponent,opponent+own):
                    mechanism(profile)
                    cases += 1
    # Exact occupied traces used by the complete randomized upper support.
    trace_cases = 0
    for z in (F(87,100),b,F(92,100),ZMAX):
        fixed = F(1,2),z-F(1,2)
        for own in ((F(1,4),F()),(F(1,2),(z-F(1,2))/2),
                    (F(1,2),z-F(1,2)-F(1,10000))):
            for profile,bidder in ((own+fixed,0),(fixed+own,1)):
                row = mechanism(profile)
                assert row['allocations'][1-bidder] == (1,1)
                trace_cases += 1
    # Actual complete menus on the whole Gplus square never make low types
    # choose a singleton or lottery. Named exact regressions augment the proof.
    all_or_none = 0
    opponents = ((F(),F()),(A,c),(F(7,10),F(1,10)),
                 (F(7,10),c),(F(1),F()),(F(1,2),F(1,2)),
                 (F(7,10),c-F(1,10000)))
    for own,opponent in product(((F(1,2),F(1,2)),(F(49,100),F(49,100)),
                                 (F(1,2),F(2,5)),(F(1,2),F())),opponents):
        for profile,bidder in ((own+opponent,0),(opponent+own,1)):
            assert baseline.mechanism(profile)['allocations'][bidder] in ((0,0),(1,1))
            all_or_none += 1
    data = dict(status='GAP_LOW_SQUARE_EXACT_PASS',revenue=calculate(),
                pointwise_cases=cases,occupied_trace_cases=trace_cases,
                all_or_none_cases=all_or_none,
                proof='research_log/gap_low_square.md',
                baseline='V4_6/verifier/price_joint_reallocation.py',
                scope='Exact whole-menu improvement and full randomized conditional gap elimination; no full auction upper bound')
    path = ROOT/'certificate/gap_low_square.json'
    if '--write' in sys.argv:
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads(path.read_text(encoding='utf-8')) == data
    print(data['status'])
    print('gain_display',float(F(data['revenue']['exact_gain_interval'][0])))
    print('exact_cases',cases+trace_cases+all_or_none)
    return data

if __name__ == '__main__':
    verify()
