"""A complete bundle exchange above the closed full-capacity region F.

The exact aggregate gain includes the full induced bidder-2 screening cost.
Normal execution is read-only; --write writes only this V4.6 certificate.
"""
from fractions import Fraction as F
from itertools import product
from math import comb, isqrt
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'verifier'))
import free_bidder_one as baseline

strip, v3 = baseline.strip, baseline.v3
p = strip.independent
add, mul, scale = p.add, p.mul, p.scale
Q = lambda r: {0:F(r)}
X = {1:F(1)}
A, a, b, d, q = F(2,3), F(159,250), F(91,100), F(1,2), F(113,500)
B0 = baseline.B0


def in_exchange(opponent):
    """Explicitly retain the earlier row at sum=b0 and sum=b."""
    return max(opponent) <= d and B0 < sum(opponent) < b


def mechanism(profile):
    profile = tuple(map(F,profile))
    assert len(profile) == 4 and all(0 <= z <= 1 for z in profile)
    before = baseline.mechanism(profile)
    own, opponent = profile[:2], profile[2:]
    allocations = list(before['allocations'])
    payments, utilities = list(before['payments']), list(before['utilities'])
    changed = [None,None]
    if in_exchange(opponent):
        prices = tuple(map(v3.asquad, (0,a,a,sum(opponent))))
        values = [v3.base.value(own,m)-prices[m] for m in range(4)]
        maximum = max(values)
        chosen = next(m for m,value in enumerate(values) if value == maximum)
        allocations[0] = tuple(F(bool(chosen&(1<<j))) for j in (0,1))
        payments[0], utilities[0], changed[0] = prices[chosen], maximum, chosen
    inner = strip.previous.old.screening_menu(own, strip.previous.old.CANDIDATE_THETA)
    if inner is not None:
        prices, priority, branch = inner
        if prices[3] < sum(own):
            prices = list(prices)
            prices[3] = v3.asquad(sum(own))
            values = [v3.base.value(opponent,m)-prices[m] for m in range(4)]
            maximum = max(values)
            chosen = next(m for m in priority if values[m] == maximum)
            allocations[1] = tuple(F(bool(chosen&(1<<j))) for j in (0,1))
            payments[1], utilities[1], changed[1] = prices[chosen], maximum, chosen
    assert all(allocations[0][j]+allocations[1][j] <= 1 for j in (0,1))
    assert all(value >= 0 for value in utilities)
    assert all(value >= 0 for value in payments)
    return dict(profile=profile, allocations=tuple(allocations),
                payments=tuple(payments), utilities=tuple(utilities),
                bundle_exchange_masks=tuple(changed))


def revenue_poly(ap,bp,cp):
    """Continuous-cell polynomial for 0<=A,B<=C<=A+B and C<=1."""
    first = mul(mul(ap,add(Q(1),scale(ap,-1))),add(cp,scale(ap,-1)))
    second = mul(mul(bp,add(Q(1),scale(bp,-1))),add(cp,scale(bp,-1)))
    rectangle = mul(add(Q(1),scale(cp,-1),bp),add(Q(1),scale(cp,-1),ap))
    cut = add(ap,bp,scale(cp,-1))
    return add(first,second,mul(cp,add(rectangle,scale(mul(cut,cut),F(-1,2)))))


def evaluate_quadratic(poly, r, s, radicand):
    """Evaluate at r+s*sqrt(radicand), returning exact (constant, coefficient)."""
    constant = coefficient = F()
    for degree,value in poly.items():
        for j in range(degree+1):
            term = value*comb(degree,j)*r**(degree-j)*s**j*radicand**(j//2)
            if j % 2:
                coefficient += term
            else:
                constant += term
    return constant, coefficient


def primitive(poly):
    return {j+1:value/F(j+1) for j,value in poly.items()}


def pair_difference(x,y):
    return x[0]-y[0],x[1]-y[1]


def integral_from_b0(poly):
    prim = primitive(poly)
    return pair_difference(evaluate_quadratic(prim,b,F(),2),
                           evaluate_quadratic(prim,F(4,3),-F(1,3),2))


def exact_interval(coefficients,digits=55):
    lo = hi = coefficients[0]
    n = 10**digits
    for coefficient,radicand in zip(coefficients[1:],(2,23)):
        z = isqrt(radicand*n*n)
        assert z*z < radicand*n*n < (z+1)*(z+1)
        lower,upper = F(z,n),F(z+1,n)
        if coefficient < 0:
            lower,upper = upper,lower
        lo += coefficient*lower
        hi += coefficient*upper
    return lo,hi


def calculate():
    # Bidder 1: sum density 1-z in the upper part of [0,1/2]^2.
    g1 = mul(add(Q(1),scale(X,-1)),
             add(revenue_poly(Q(a),Q(a),X),
                 scale(revenue_poly(Q(a),Q(a),Q(b)),-1)))
    gain1 = integral_from_b0(g1)
    assert gain1 == (F(-6270448598899,243000000000000),F(221749217,12150000000))
    # Bidder 2's free Q part: all menus whose sum z exceeds b0 must move.
    integral_free = integral_from_b0(mul(add(Q(1),scale(X,-1)),
                                        revenue_poly(Q(A),Q(A),X)))
    area_hi = evaluate_quadratic({0:F(1,2),1:F(-1),2:F(1,2)},F(4,3),-F(1,3),2)
    area = area_hi[0]-F(1,2)*(1-b)**2, area_hi[1]
    sja = F(4,9),F(2,27)
    original = baseline.mul(area,sja)
    loss_free = pair_difference(integral_free,original)
    assert loss_free == (F(93808494641,12150000000000),-F(13271,2430000))
    # Constrained Q: t in [d,q+sqrt(23)/15], z in [C(t),b].
    k = add(X,Q(-q))
    C = add(Q(F(5,6)),scale(mul(k,k),F(3,4)))
    B = add(C,scale(k,-1))
    h = add(Q(b),scale(C,-1))
    K = add(Q(1+2*A-F(3,2)*A*A),scale(B,2),scale(mul(B,B),F(-3,2)))
    gc = add(K,scale(C,-4),scale(mul(C,C),F(3,2)))
    gcc = add(Q(-4),scale(C,3))
    h2,h3,h4 = mul(h,h),mul(mul(h,h),h),mul(mul(h,h),mul(h,h))
    constrained_poly = scale(add(scale(mul(gc,h2),F(1,2)),
                                 scale(mul(gcc,h3),F(1,6)),scale(h4,F(1,8))),2)
    prim = primitive(constrained_poly)
    loss_constrained = pair_difference(evaluate_quadratic(prim,q,F(1,15),23),
                                       evaluate_quadratic(prim,d,F(),23))
    coefficients = (gain1[0]+loss_free[0]+loss_constrained[0],
                    gain1[1]+loss_free[1],loss_constrained[1])
    lo,hi = exact_interval(coefficients)
    assert F(34716,10**10) < lo < hi < F(34717,10**10)
    # Independent exact continuous polygon checks of all deterministic cells.
    polygon_checks = 0
    for t in (F(501,1000),F(51,100),F(53,100),F(54,100)):
        Ct,Bt = p.value(C,t),p.value(B,t)
        for z in (Ct,(Ct+b)/2,b):
            menu = [(F(),F(),F()),(F(1),F(),A),(F(),F(1),Bt),(F(1),F(1),z)]
            exact = p.polygon_revenue(menu)[0]
            assert exact == p.value(revenue_poly(Q(A),Q(Bt),Q(z)),F())
            delta = z-Ct
            analytic = p.value(gc,t)*delta+F(1,2)*p.value(gcc,t)*delta**2+F(1,2)*delta**3
            assert exact-p.value(revenue_poly(Q(A),Q(Bt),Q(Ct)),F()) == analytic
            polygon_checks += 1
    for z in (F(87,100),F(89,100),b):
        assert B0 < z <= b
        exact = p.polygon_revenue([(F(),F(),F()),(F(1),F(),a),
                                  (F(),F(1),a),(F(1),F(1),z)])[0]
        assert exact == p.value(revenue_poly(Q(a),Q(a),Q(z)),F())
        polygon_checks += 1
    return dict(gain_coefficients=list(map(str,coefficients)),
                field_basis=['1','sqrt(2)','sqrt(23)'],
                exact_gain_interval=list(map(str,(lo,hi))),
                bidder_one_gain_pair=list(map(str,gain1)),
                bidder_two_free_cost_pair=list(map(str,loss_free)),
                bidder_two_constrained_cost_pair=list(map(str,loss_constrained)),
                free_cost_field='sqrt(2)', constrained_cost_field='sqrt(23)',
                constrained_integrand={str(j):str(z) for j,z in sorted(constrained_poly.items())},
                constrained_upper_endpoint='113/500 + sqrt(23)/15',
                exact_continuous_polygon_checks=polygon_checks,
                claim='exact positive complete-menu gain, including both induced bidder-2 costs')


def verify():
    checks = 0
    points = ((F(0),F(0)),(F(1),F(1)),(F(9,20),F(9,20)),
              (F(11,25),F(11,25)),(F(1,2),F(39,100)),
              (F(51,100),F(39,100)),(F(54,100),F(36,100)),
              (F(7,10),F(1,4)),(F(4,5),F(27,100)),
              (F(159,250),F(137,500)),(F(1,2),F(41,100)))
    for own,opp in product(points,repeat=2):
        mechanism(own+opp)
        checks += 1
    # Menu entry ties and equal bundle totals, both orientations.
    for z in (F(87,100),F(89,100),F(9,10)):
        opp = F(1,2),z-F(1,2)
        assert in_exchange(opp)
        for own in ((z/2,z/2),(a,z-a),(z-a,a),(F(1),z-a),(F(1,2),z-F(1,2))):
            for profile in (own+opp,tuple(reversed(own))+tuple(reversed(opp))):
                mechanism(profile)
                checks += 1
    witness = (F(9,20),F(9,20),F(11,25),F(11,25))
    before,after = baseline.mechanism(witness),mechanism(witness)
    assert before['allocations'] == ((0,0),(1,1))
    assert after['allocations'] == ((1,1),(0,0))
    assert after['payments'][0] == F(22,25)
    # An open rational box of strict ownership transfers, checked by endpoint
    # inequalities as well as its 16 vertices; the note proves its interior.
    prism = ((F(449,1000),F(451,1000)),)*2 + ((F(439,1000),F(441,1000)),)*2
    assert F(878,1000)>B0 and F(902,1000)<b
    assert F(898,1000)>F(882,1000)
    for profile in product(*prism):
        assert baseline.mechanism(profile)['allocations'] == ((0,0),(1,1))
        assert mechanism(profile)['allocations'] == ((1,1),(0,0))
        checks += 1
    data = dict(status='OUTER_BUNDLE_EXCHANGE_EXACT_PASS',
                scope='complete pointwise DSIC/IR genuine joint reallocation with exact positive total gain',
                revenue=calculate(), pointwise_checks=checks,
                strict_transfer_box_volume=str(F(1,500)**4),
                witness=dict(profile=list(map(str,witness)),
                             prior_allocations=[[str(z) for z in w] for w in before['allocations']],
                             new_allocations=[[str(z) for z in w] for w in after['allocations']],
                             new_payments=list(map(str,after['payments']))),
                proof='research_log/outer_bundle_exchange.md',
                inner_scope='F and Eplus certificates survive; Q is retained only where sum(w)<=C_Q(w)',
                full_auction_upper='unresolved')
    path = ROOT/'certificate'/'outer_bundle_exchange.json'
    if '--write' in sys.argv:
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads(path.read_text(encoding='utf-8')) == data
    print(data['status'])
    print('gain_coefficients',data['revenue']['gain_coefficients'])
    print('gain_display',float(F(data['revenue']['exact_gain_interval'][0])))
    print('pointwise_checks',checks)
    return data


if __name__ == '__main__':
    verify()
