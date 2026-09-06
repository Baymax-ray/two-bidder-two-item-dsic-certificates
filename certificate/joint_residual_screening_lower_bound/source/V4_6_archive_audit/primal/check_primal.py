"""Independent V4.6 menu-membership and hostile-boundary regression.

Run without -O: python -B -X utf8 .../primal/check_primal.py
No files are written. This is bounded implementation evidence, not a
continuum proof. The accompanying audit.md supplies the all-real argument.
The retained predecessor menu/Quad scalar arithmetic are explicit shared
dependencies; the final-menu assembler below does not call V4.6 menu helpers.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random
import sys

assert __debug__ and not sys.flags.optimize
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'V4_6' / 'verifier'))
import price_joint_reallocation as production

old = production.baseline.previous.strip.previous.old
Qd = old.v3.Quad
a, b, c, d, q = F(159,250), F(91,100), F(137,500), F(1,2), F(113,500)
A, T, U, e = F(2,3), F(613,750), F(839,750), F(9,10000)
b0 = Qd(F(4,3), -F(1,3), 2)


def in_e(v):
    return A < max(v) < T and min(v) < c


def in_f(v):
    return max(v) <= d and sum(v) <= b0


def in_g(v):
    return max(v) <= d and b0 < sum(v) < b


def in_q(v):
    return max(v) <= A and sum(v) <= b


def lottery(v, cut=False):
    t = max(v)
    delta = F(9,16)*(T-t)*(U-t)
    beta = (3*t-2)/(3*t-2+2*delta)
    rows = [((F(),F()),F()), ((F(),F(1)),d+delta),
            ((F(1),F()),t), ((F(1),F(1)),t+c+delta),
            ((F(1),beta),t+beta*c-(e if cut else F()))]
    if v[0] < v[1]:
        rows = [(tuple(reversed(x)),p) for x,p in rows]
    return rows


def deterministic(prices):
    return [(tuple(F(bool(m & (1 << j))) for j in (0,1)),p)
            for m,p in enumerate(prices)]


def independent_menu(bidder, v):
    """Single formula for each final row, independent of wrapper sequencing."""
    if bidder == 0 and in_f(v):
        menu = deterministic((0,A,A,b0))
    elif bidder == 0 and in_g(v):
        menu = deterministic((0,a,a,sum(v)))
    elif bidder == 1 and F(7,10) <= v[0] <= F(71,100) and 0 <= v[1] <= F(1,5):
        menu = lottery(v, cut=True)
    elif in_e(v):
        menu = lottery(v)
    elif bidder == 1 and in_q(v):
        t,z = max(v),sum(v)
        if t <= d:
            menu = deterministic((0,A,A,max(b0,z)))
        else:
            k = t-q
            C = max(F(5,6)+F(3,4)*k*k,z)
            prices = [F(),A,A,C]
            prices[2 if v[0] > v[1] else 1] = C-k
            menu = deterministic(prices)
    else:
        menu = deterministic(old.retained_menu(v, -F(1,1000)))
    if bidder == 0 and F(7,10)-4*e <= v[0] <= F(71,100) and c-2*e <= v[1] <= c+4*e:
        menu = [(x,p+e if x != (0,0) else p) for x,p in menu]
    return menu


def value(v,x):
    return sum((z*w for z,w in zip(v,x)),F())


def check(profile):
    row = production.mechanism(profile)
    for i in (0,1):
        own,opp = profile[2*i:2*i+2], profile[2*(1-i):2*(1-i)+2]
        menu = independent_menu(i,opp)
        x,p,u = row['allocations'][i], row['payments'][i], row['utilities'][i]
        assert any(x == xx and p == pp for xx,pp in menu), (profile,i,'menu membership')
        assert u == value(own,x)-p == max(value(own,xx)-pp for xx,pp in menu), (profile,i,'maximization')
        assert u >= 0 and p >= 0 and all(0 <= z <= 1 for z in x)
        if u == 0:
            assert x == (0,0) and p == 0, (profile,i,'empty at zero')
    assert all(sum(x[j] for x in row['allocations']) <= 1 for j in (0,1))


def main():
    profiles = set()
    def add(p):
        p = tuple(map(F,p))
        if all(0 <= x <= 1 for x in p):
            profiles.add(p)
    # Full-square extremes, all new region cuts, and inherited shared ties.
    points = {(F(),F()),(F(1),F(1)),(d,d),(a,c),(A,b-A),(T,c),
              (F(43,100),F(43,100)),(F(431,1000),F(431,1000)),
              (F(45,100),F(45,100)),(d,b-d),(F(7,10),F(1,5)),
              (F(71,100),F(1,5)),(F(7,10)-4*e,c-2*e),
              (F(71,100),c+4*e),(F(7,10),c),
              (F(7,10),c-F(1,10**6)),(F(7,10),c+F(1,10**6)),
              (F(1),F()),(d,F()),(A,F()),(T,F())}
    points |= {tuple(reversed(x)) for x in points}
    for w,v in product(points, repeat=2):
        add(w+v)
    # Fresh rational random profiles; this is regression only.
    rng = random.Random(460906)
    for _ in range(700):
        add(F(rng.randrange(10001),10000) for _ in range(4))
    # Exact lottery indifference lines, fee faces, and their two sides.
    h = F(1,10**7)
    for t,rho in product((F(7,10),F(141,200),F(71,100)), (F(),F(1,5))):
        delta = F(9,16)*(T-t)*(U-t)
        beta = (3*t-2)/(3*t-2+2*delta)
        Y = c+delta/(1-beta)
        ys = (c-2*e,c-e/beta,c,c+4*e,Y+e/(1-beta),d+delta,F(1))
        for y in ys:
            for x in (t,t-e,t-beta*(y-c)-e,F(7,10)-4*e,F(71,100)):
                for shift in (-h,F(),h):
                    add((t,rho,x+shift,y))
    # Q bundle/singleton ties and old-to-new C0 junctions, both orientations.
    for t in (d,F(501,1000),F(51,100),F(53,100),F(54,100),a,A):
        k = t-q
        C0 = F(5,6)+F(3,4)*k*k
        for z in (C0-h,C0,C0+h,b-h,b):
            rho = z-t
            for own in ((0,0),(k,1),(A,z-A),(d,z-d),(z/2,z/2),(1,1)):
                p = (t,rho)+tuple(map(F,own))
                add(p)
                add((rho,t,p[3],p[2]))
    counts = {'profiles':0,'final_fee_profiles':0,'final_cut_profiles':0,
              'fee_and_cut_profiles':0}
    for p in sorted(profiles):
        check(p)
        counts['profiles'] += 1
        fee = F(7,10)-4*e <= p[2] <= F(71,100) and c-2*e <= p[3] <= c+4*e
        cut = F(7,10) <= p[0] <= F(71,100) and p[1] <= F(1,5)
        counts['final_fee_profiles'] += fee
        counts['final_cut_profiles'] += cut
        counts['fee_and_cut_profiles'] += fee and cut
    # Check inherited price bounds at the literal tariff endpoints.
    opponent_reports = set(points)
    table = old.base.DATA
    for row in table['bundle_rows']:
        for z,r in product(map(F,row['sum_interval']), map(F,row['normalized_rho_interval'])):
            low = c+r*(z-c-F(501,1000))
            opponent_reports.add((z-low,low))
            opponent_reports.add((low,z-low))
    for row in table['common_rows']:
        for t in map(F,row['high_interval']):
            for low in (F(),c,min(c,b-t)):
                opponent_reports.add((t,low))
                opponent_reports.add((low,t))
    for v in sorted(opponent_reports):
        inc = old.increments(v)
        p = old.retained_menu(v,-F(1,1000))
        assert inc[0] == 0 and min(inc[1:3]) >= 0 and inc[3] == max(inc[1:3])
        assert min(p[1:3]) >= d and p[3] >= b
        assert p[3]-p[1] >= c and p[3]-p[2] >= c
        assert old.base_menu(v,-F(1,1000))[1]+old.base_menu(v,-F(1,1000))[2]-old.base_menu(v,-F(1,1000))[3] >= q
    counts['tariff_endpoint_reports'] = len(opponent_reports)
    print(json.dumps({'status':'INDEPENDENT_PRIMAL_REGRESSION_PASS',
                      'arithmetic':'Fraction and exact quadratic comparisons',
                      'counts':counts,
                      'scope':'bounded source/menu audit; continuum proof is in audit.md'},indent=2))


if __name__ == '__main__':
    main()
