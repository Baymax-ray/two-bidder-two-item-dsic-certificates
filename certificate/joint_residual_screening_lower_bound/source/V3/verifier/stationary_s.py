"""Exact V3 S-chamber candidate; standard-library polynomial revenue replay.

No floating optimizer or type grid enters the construction or proof.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import baseline_mechanism as base

class P:
    def __init__(self, x=0):
        if isinstance(x, P):
            self.c = x.c
            return
        c = tuple(map(F, x)) if isinstance(x, (list, tuple)) else (F(x),)
        while len(c) > 1 and c[-1] == 0:
            c = c[:-1]
        self.c = c
    def __add__(self, b):
        b = P(b)
        return P(tuple((self.c[i] if i < len(self.c) else 0) +
                       (b.c[i] if i < len(b.c) else 0)
                       for i in range(max(len(self.c), len(b.c)))))
    __radd__ = __add__
    def __neg__(self):
        return P(tuple(-a for a in self.c))
    def __sub__(self, b):
        return self + -P(b)
    def __rsub__(self, b):
        return P(b) + -self
    def __mul__(self, b):
        b = P(b)
        c = [F()] * (len(self.c) + len(b.c) - 1)
        for i, a in enumerate(self.c):
            for j, d in enumerate(b.c):
                c[i+j] += a*d
        return P(c)
    __rmul__ = __mul__
    def __pow__(self, n):
        answer = P(1)
        for _ in range(n):
            answer = answer*self
        return answer
    def __call__(self, t):
        z = F()
        for a in reversed(self.c):
            z = z*t+a
        return z
    def integral(self, lo, hi):
        return sum((a*(hi**(i+1)-lo**(i+1))/F(i+1)
                    for i, a in enumerate(self.c)), F())
    def derivative(self):
        return P(tuple(i*a for i, a in enumerate(self.c) if i) or (0,))
    def zero(self):
        return self.c == (0,)


def require(test, message):
    if not test:
        raise RuntimeError(message)


def revenue(A, B, C):
    return (A*(1-A)*(C-A) + B*(1-B)*(C-B) +
            C*((1-C+B)*(1-C+A) - F(1, 2)*(A+B-C)**2))


def gradient(A, B, C):
    return ((C-A)*(2-3*A), (C-B)*(2-3*B),
            1-4*C+2*(A+B)+F(3, 2)*C*C-F(3, 2)*(A*A+B*B))


def bernstein(poly, lo, hi):
    from math import comb
    p = P(poly)
    n = len(p.c)-1
    power = [sum((p.c[i]*comb(i,k)*lo**(i-k)*(hi-lo)**k
                  for i in range(k,n+1)), F()) for k in range(n+1)]
    return [sum((power[k]*F(comb(j,k),comb(n,k)) for k in range(j+1)), F())
            for j in range(n+1)]


def nonnegative(poly, lo, hi, label):
    b = bernstein(poly, lo, hi)
    require(min(b) >= 0, 'Bernstein sign: '+label)
    return str(min(b))


T = P((0, 1))
a, c, d = base.A, base.C, base.D
q = d-c
switch = F(2, 3)
cutoff = (F(1, 2)-c+F(3, 4)*q*q)/(F(3, 2)*q)
f1 = switch-T
delta1 = F(1, 6)-c+F(3, 4)*(T-q)**2
f2 = P()
delta2 = F(1, 2)-c+F(3, 4)*q*q-F(3, 2)*q*T
SEGMENTS = [(a,switch,f1,delta1),(switch,cutoff,f2,delta2),
            (cutoff,F(1),P(),P())]


def prices_for_t(t):
    t = F(t)
    require(a <= t <= 1, 'S high coordinate')
    if t <= switch:
        fee, delta = f1(t), delta1(t)
    elif t <= cutoff:
        fee, delta = F(), delta2(t)
    else:
        fee, delta = F(), F()
    return (t+fee, d+fee+delta, t+c+fee+delta), fee, delta


def mechanism(profile, modified_bidders=(0,1)):
    """Complete mechanism including exceptional reports and ties.

    S interior in high coordinate is modified; t=a retains the baseline.
    At low=c modification is explicit, regardless of table priority.
    This changes only null boundaries relative to the integrated formula.
    """
    result = base.mechanism(profile)
    types = (result['profile'][:2], result['profile'][2:])
    masks, payments, utilities = list(result['masks']), list(result['payments']), list(result['utilities'])
    menus = [x['prices'] for x in result['menus']]
    for i in modified_bidders:
        own, opp = types[i], types[1-i]
        t, rho = max(opp), min(opp)
        if not (a < t <= 1 and 0 <= rho <= c):
            continue
        prices, fee, delta = prices_for_t(t)
        low_mask = 1 if opp[0] < opp[1] else 2
        high_mask = 3-low_mask
        menu = [F()]*4
        menu[high_mask], menu[low_mask], menu[3] = prices
        old = result['base_masks'][i]
        vals = [base.value(own,m)-menu[m] for m in range(4)]
        best = max(vals)
        if best == 0:
            selected = 0
        elif vals[old] == best:
            selected = old
        else:
            choices = [m for m in range(4) if m & ~old == 0 and vals[m] == best]
            require(bool(choices), 'base-subset menu maximizer')
            selected = min(choices)
        masks[i], payments[i], utilities[i], menus[i] = selected,menu[selected],best,tuple(menu)
        require(selected & ~old == 0, 'item containment')
    require(masks[0] & masks[1] == 0, 'joint capacity')
    return dict(profile=result['profile'],masks=tuple(masks),payments=tuple(payments),
                utilities=tuple(utilities),menus=tuple(menus),base_masks=result['base_masks'])


def calculate():
    checks, new_gain = [], F()
    old = revenue(T,P(d),T+c)
    for index,(lo,hi,fee,delta) in enumerate(SEGMENTS):
        A,B,C = T+fee,d+fee+delta,T+c+fee+delta
        signs={}
        for label,p in [('fee',fee),('delta',delta),('A',A),('B',B),('1-A',1-A),
                        ('1-B',1-B),('C-A',C-A),('C-B',C-B),('A+B-C',A+B-C)]:
            signs[label]=nonnegative(p,lo,hi,label)
        gA,gB,gC=gradient(A,B,C)
        for label,p in [('bundle',gC),('high_item',gA+gC),('low_item',gB+gC),('common',gA+gB+gC)]:
            signs['negative_'+label]=nonnegative(-p,lo,hi,label)
        if index == 0:
            require(gA.zero() and (gB+gC).zero(), 'first stationary identities')
        elif index == 1:
            require((gB+gC).zero(), 'second stationary identity')
        gain=4*c*(revenue(A,B,C)-old).integral(lo,hi)
        new_gain += gain
        checks.append(dict(interval=[str(lo),str(hi)],fee=[str(x) for x in fee.c],
                           delta=[str(x) for x in delta.c],signs=signs,base_gain=str(gain)))
    require(f1(switch)==0 and delta1(switch)==delta2(switch), 'first junction')
    require(delta2(cutoff)==0, 'second junction')
    scommon=sum((F(r['expected_gain']) for r in base.DATA['common_rows'] if r['id'].startswith('S')),F())
    item_sum=sum((F(r['expected_gain']) for r in base.DATA['item_rows']),F())
    inherited=F('83962078694672281756033/96000000000000000000000')
    gain=new_gain-scommon-item_sum
    require(gain>0,'strict improvement over strongest baseline')
    upper=F('3715139591287203/4194304000000000')
    return dict(scope='exact feasible lower bound; no unrestricted optimality claim',
                switch=str(switch),cutoff=str(cutoff),segments=checks,
                new_S_gain_over_base=str(new_gain),inherited_S_common_gain=str(scommon),
                inherited_S_item_gain=str(item_sum),gain_over_inherited=str(gain),
                inherited_lower=str(inherited),new_lower=str(inherited+gain),
                inherited_upper=str(upper),remaining_gap=str(upper-inherited-gain))


if __name__=='__main__':
    data=calculate()
    target=Path(__file__).parents[1]/'certificate'/'stationary_s.json'
    if '--write' in sys.argv:
        target.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:
        require(json.loads(target.read_text(encoding='utf-8'))==data,'certificate exact replay')
    for k in ('cutoff','gain_over_inherited','new_lower','remaining_gap'):
        print(k,data[k],float(F(data[k])))
    print('PASS exact piecewise polynomial integrals, cone signs, junctions, and strict gain')
