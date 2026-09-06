"""Exact boundary-payment sign for the V3.1 origin-compression direction."""
from fractions import Fraction as F
from pathlib import Path
from math import comb
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
AUCTION = ROOT.parent


def require(test, message):
    if not test:
        raise RuntimeError(message)


class P:
    def __init__(self, x=0):
        if isinstance(x, P):
            self.c = x.c
        else:
            c = tuple(map(F, x)) if isinstance(x, (tuple, list)) else (F(x),)
            while len(c) > 1 and c[-1] == 0:
                c = c[:-1]
            self.c = c
    def __add__(self, other):
        other = P(other)
        n = max(len(self.c), len(other.c))
        return P(tuple((self.c[j] if j < len(self.c) else 0) +
                       (other.c[j] if j < len(other.c) else 0) for j in range(n)))
    __radd__ = __add__
    def __neg__(self): return P(tuple(-x for x in self.c))
    def __sub__(self, other): return self + -P(other)
    def __rsub__(self, other): return P(other) + -self
    def __mul__(self, other):
        other = P(other)
        out = [F()] * (len(self.c)+len(other.c)-1)
        for j, x in enumerate(self.c):
            for k, y in enumerate(other.c): out[j+k] += x*y
        return P(out)
    __rmul__ = __mul__
    def __pow__(self, n):
        out = P(1)
        for _ in range(n): out = out*self
        return out
    def integral(self, lo, hi):
        return sum((x*(hi**(j+1)-lo**(j+1))/F(j+1) for j,x in enumerate(self.c)), F())


def nonnegative(poly, lo, hi):
    p = P(poly)
    n = len(p.c)-1
    power = [sum((p.c[i]*comb(i,k)*lo**(i-k)*(hi-lo)**k
                  for i in range(k,n+1)), F()) for k in range(n+1)]
    bern = [sum((power[k]*F(comb(j,k),comb(n,k)) for k in range(j+1)), F())
            for j in range(n+1)]
    require(min(bern)>=0, 'whole-interval polynomial sign')


def calculate():
    inputs = {
        'base': AUCTION/'V3/certificate/baseline_mechanism.json',
        'V3': AUCTION/'V3/certificate/joined_threshold.json',
        'V3_1': AUCTION/'V3_1/certificate/independent_revenue.json',
    }
    data = {k: json.loads(p.read_text(encoding='utf-8')) for k,p in inputs.items()}
    a,b,c,d,q = F(159,250),F(91,100),F(137,500),F(501,1000),F(227,1000)
    h = 1-q
    require(c==b-a and q==d-c, 'constant identities')
    T = P((0,1))
    Q = lambda z: z*(1-z)+h*q*(1-z)+(z+h)*q*q*F(1,2)
    S2 = 2*(c*Q(d)+Q(T+q).integral(c,h)+
            ((1+T)*(1-T)**2*F(1,2)).integral(h,F(1)))
    EC = b+c*(1-a)**2+(1-c)**2*(1-a)+(2*a-b)**3/F(6)
    Eg2 = c*c*d+(h**3-c**3)/F(3)
    primitive = lambda z: z*z*F(1,2)-z**3*F(1,3)+c*c*z
    J1 = (primitive(1+T)-primitive(1+c)).integral(c,d)
    J2 = (-(1-h**3)/3+(1-h*h)/2+q**3)*(1-d)-q*(1+q)*(1-d*d)/2
    S1base = 2*(EC-Eg2+J1+J2)
    require(S2==F(5509643569103,12000000000000), 'S2 exact integral')
    require(S1base==F(3453946410567,2000000000000), 'base S1 exact integral')
    cutoff = (F(1,2)-c+F(3,4)*q*q)/(F(3,2)*q)
    segments = [(a,F(2,3),F(2,3)-T,F(1,6)-c+F(3,4)*(T-q)**2),
                (F(2,3),cutoff,P(),F(1,2)-c+F(3,4)*q*q-F(3,2)*q*T)]
    gains = []
    for lo,hi,fee,delta in segments:
        nonnegative(fee,lo,hi)
        nonnegative(delta,lo,hi)
        nonnegative(1-c-delta,lo,hi)
        gains.append(2*c*(2*fee+2*(1-c)*delta-delta*delta).integral(lo,hi))
    Sgain = sum(gains,F())
    require(Sgain==F(2064375095897180100457,735480000000000000000000), 'joined S edge integral')
    # The omitted Z terms are nonnegative on their analytic branches.
    r0 = b*b-F(2,3)-c*c
    r1 = F(4,3)*c-F(2,9)
    require(c*c<r0<r1<(a-q)**2, 'Z branch ordering and k>c')
    require(F(3,2)*(F(2,3)-q)<1, 'plateau low price decreases')
    require(F(1,6)-c+F(3,4)*r1==0, 'Z surcharge starts nonnegative')
    rows = data['base']['bundle_rows']
    fees = [F(row['fee']) for row in rows]
    require(len(rows)==41 and min(fees)>=0, 'nonnegative inherited bundle fees')
    require(a+1-b+max(fees)<1, 'bundle-fee singleton topology')
    require(all(row['id'].startswith(('Z','S')) for row in data['base']['common_rows']), 'all common rows covered')
    require(all(row['parent'].startswith('S') for row in data['base']['item_rows']), 'all selective rows covered')
    S1lo = S1base+Sgain
    R3hi = F(data['V3']['revenue_interval'][1])
    R31hi = F(data['V3_1']['independent_total_revenue_interval'][1])
    derivative_lo = S1lo+S2-R3hi/2-2*R31hi
    require(derivative_lo>F(1,1000), 'strict positive left derivative')
    return {
        'scope':'near-identity origin compression loses; no statement for all lambda<1',
        'method':'exact polynomial integrals and nonnegative omitted terms; no grid',
        'input_sha256':{k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in inputs.items()},
        'S2':str(S2),'EC_base':str(EC),'Eg2_base':str(Eg2),
        'edge_correction_1':str(J1),'edge_correction_2':str(J2),
        'S1_base':str(S1base),'S_edge_segments':[str(x) for x in gains],
        'S_edge_gain':str(Sgain),'S1_lower':str(S1lo),
        'omitted_terms':'nonnegative joined Z edge gain and nonnegative inherited bundle-fee edge gains',
        'bundle_fee_singleton_upper':str(a+1-b+max(fees)),
        'R_V3_upper_dependency':str(R3hi),'R_V3_1_upper_dependency':str(R31hi),
        'derivative_lower':str(derivative_lo),'strict_comparison':'derivative_lower > 1/1000 > 0',
    }


if __name__=='__main__':
    result=calculate()
    target=ROOT/'certificate/compression_boundary_sign.json'
    if '--write' in sys.argv:
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    else:
        require(json.loads(target.read_text(encoding='utf-8'))==result,'exact certificate replay')
    for key in ('S2','S1_base','S_edge_gain','S1_lower','derivative_lower'):
        print(key,result[key])
    print('PASS exact boundary-payment sign; no finite-type approximation')
