"""Coupled safe-singleton/bundle response to the V4.6 bundle exchange.

This wrapper preserves outer_bundle_exchange.py as the earlier admissible
trial and implements a strictly better complete response on constrained Q.
Normal execution is read-only; --write updates only this certificate.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verifier'))
import outer_bundle_exchange as previous

v3, p = previous.v3, previous.p
A,a,b,d,q = previous.A,previous.a,previous.b,previous.d,previous.q


def changed_menu(opponent):
    if max(opponent) <= d:
        return None
    inner = previous.strip.previous.old.screening_menu(
        opponent,previous.strip.previous.old.CANDIDATE_THETA)
    if inner is None:
        return None
    prices,priority,branch = inner
    total = sum(opponent)
    if total <= prices[3]:
        return None
    t = max(opponent)
    k = t-q
    high = 1 if opponent[0] > opponent[1] else 2
    low = 3-high
    updated = list(prices)
    updated[low] = v3.asquad(total-k)
    updated[3] = v3.asquad(total)
    return tuple(updated),priority


def mechanism(profile):
    profile = tuple(map(F,profile))
    before = previous.mechanism(profile)
    inner = changed_menu(profile[:2])
    if inner is None:
        return before
    prices,priority = inner
    values = [v3.base.value(profile[2:],m)-prices[m] for m in range(4)]
    maximum = max(values)
    chosen = next(m for m in priority if values[m] == maximum)
    allocation = tuple(F(bool(chosen&(1<<j))) for j in (0,1))
    assert all(before['allocations'][0][j]+allocation[j] <= 1 for j in (0,1))
    row = dict(before)
    row.update(allocations=(before['allocations'][0],allocation),
               payments=(before['payments'][0],prices[chosen]),
               utilities=(before['utilities'][0],maximum),
               reoptimized_bundle_mask=chosen)
    return row


def calculate():
    add,mul,scale,Q,X = previous.add,previous.mul,previous.scale,previous.Q,previous.X
    k = add(X,Q(-q))
    C0 = add(Q(F(5,6)),scale(mul(k,k),F(3,4)))
    h = add(Q(b),scale(C0,-1))
    cost_poly = scale(mul(mul(h,h),h),F(-2,3))
    prim = previous.primitive(cost_poly)
    coupled_cost = previous.pair_difference(
        previous.evaluate_quadratic(prim,q,F(1,15),23),
        previous.evaluate_quadratic(prim,d,F(),23))
    before = previous.calculate()
    old_cost = tuple(map(F,before['bidder_two_constrained_cost_pair']))
    extra = previous.pair_difference(coupled_cost,old_cost)
    lo,hi = previous.exact_interval((extra[0],F(),extra[1]))
    assert F(30246,10**11) < lo < hi < F(30247,10**11)
    old_gain = tuple(map(F,before['gain_coefficients']))
    full_gain = (old_gain[0]+extra[0],old_gain[1],old_gain[2]+extra[1])
    flo,fhi = previous.exact_interval(full_gain)
    assert F(37741,10**10)<flo<fhi<F(37742,10**10)
    polygon_checks = 0
    for t in (F(501,1000),F(51,100),F(53,100),F(54,100)):
        kt,Ct = t-q,p.value(C0,t)
        for total in ((Ct+b)/2,b):
            B0 = Ct-kt
            assert d < B0 <= total-kt < A
            original = p.polygon_revenue([(F(),F(),F()),(F(1),F(),A),
                                         (F(),F(1),B0),(F(1),F(1),Ct)])[0]
            new = p.polygon_revenue([(F(),F(),F()),(F(1),F(),A),
                                    (F(),F(1),total-kt),(F(1),F(1),total)])[0]
            assert new-original == -(total-Ct)**2
            old_response = p.polygon_revenue([(F(),F(),F()),(F(1),F(),A),
                                             (F(),F(1),B0),(F(1),F(1),total)])[0]
            assert new > old_response
            polygon_checks += 1
    return dict(extra_gain_pair=list(map(str,extra)),extra_gain_field='sqrt(23)',
                extra_gain_interval=list(map(str,(lo,hi))),
                constrained_cost_pair=list(map(str,coupled_cost)),
                constrained_cost_field='sqrt(23)',
                constrained_integrand={str(j):str(z) for j,z in sorted(cost_poly.items())},
                full_bundle_exchange_gain_coefficients=list(map(str,full_gain)),
                full_bundle_exchange_gain_basis=['1','sqrt(2)','sqrt(23)'],
                full_bundle_exchange_gain_interval=list(map(str,(flo,fhi))),
                exact_continuous_polygon_checks=polygon_checks,
                scope='exact additional gain over outer_bundle_exchange; whole changed conditional menus included')


def verify():
    checks = 0
    for t in (F(501,1000),F(51,100),F(53,100),F(54,100)):
        k = t-q
        C0 = F(5,6)+F(3,4)*k*k
        for total in (C0,(C0+b)/2,b):
            rho = total-t
            assert F(0)<rho<t
            for own in ((F(0),F(0)),(F(1),F(1)),(F(1,2),total-F(1,2)),
                        (F(1,2),total-F(1,2)-F(1,10000)),
                        (k,F(1)),(k-F(1,10000),F(1)),
                        (F(0),total-k),(F(0),C0-k),
                        (F(2,5),F(1,2)),(A,total-A)):
                for profile in ((t,rho)+own,(rho,t)+tuple(reversed(own))):
                    mechanism(profile)
                    checks += 1
    # The existing strict-transfer witness remains the same actual transfer.
    witness = (F(9,20),F(9,20),F(11,25),F(11,25))
    assert mechanism(witness)['allocations'] == ((1,1),(0,0))
    # Anchored capacity traces for the possible full inner certificate.
    occupied = 0
    for t in (F(51,100),F(53,100),F(54,100)):
        k = t-q
        C0 = F(5,6)+F(3,4)*k*k
        total = (C0+b)/2
        rho = total-t
        for x in (F(0),F(1,4),F(1,2)):
            assert mechanism((t,rho,x,F(0)))['allocations'][0][0] == 1
            occupied += 1
        for y in (F(0),(total-F(1,2))/2,total-F(1,2)-F(1,10000)):
            assert mechanism((t,rho,F(1,2),y))['allocations'][0][1] == 1
            occupied += 1
        for x in (F(0),k/2,k-F(1,10000)):
            assert mechanism((t,rho,x,F(1)))['allocations'][0][0] == 1
            occupied += 1
    data = dict(status='OUTER_BUNDLE_REOPTIMIZED_EXACT_PASS',
                scope='complete pointwise feasible coupled conditional response; exact strict gain',
                revenue=calculate(), pointwise_cases=checks,occupied_trace_cases=occupied,
                proof='research_log/outer_bundle_reoptimized.md',
                predecessor='verifier/outer_bundle_exchange.py')
    path = ROOT/'certificate'/'outer_bundle_reoptimized.json'
    if '--write' in sys.argv:
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads(path.read_text(encoding='utf-8')) == data
    print(data['status'])
    print('extra_gain_display',float(F(data['revenue']['extra_gain_interval'][0])))
    print('full_bundle_gain_display',float(F(data['revenue']['full_bundle_exchange_gain_interval'][0])))
    print('pointwise_checks',checks+occupied)
    return data


if __name__ == '__main__':
    verify()
