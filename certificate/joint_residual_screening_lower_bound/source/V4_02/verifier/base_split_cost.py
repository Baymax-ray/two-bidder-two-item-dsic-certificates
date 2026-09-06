"""Exact per-bidder affine-base split-cost derivative on [1.136,1.137]."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
A=F(159,250)
B=F(91,100)
C=B-A
S0=F(1137,1000)
LOW=S0-F(1,1000)


def require(test,message):
    if not test: raise RuntimeError(message)


def trim(p):
    p=list(map(F,p))
    while len(p)>1 and not p[-1]:p.pop()
    return tuple(p)


def add(*ps):
    n=max(map(len,ps))
    return trim(sum((p[j] if j<len(p) else F() for p in ps),F()) for j in range(n))


def scale(p,c):return trim(x*F(c) for x in p)


def mul(p,r):
    out=[F()]*(len(p)+len(r)-1)
    for j,x in enumerate(p):
        for k,y in enumerate(r):out[j+k]+=x*y
    return trim(out)


def power(p,n):
    out=(F(1),)
    for _ in range(n):out=mul(out,p)
    return out


def value(p,x):
    out=F()
    for y in reversed(p):out=out*x+y
    return out


def derivative(p):return trim((j*p[j] for j in range(1,len(p))) or [F()])


def shifted(p,x):
    return trim(sum((p[i]*comb(i,j)*x**(i-j) for i in range(j,len(p))),F()) for j in range(len(p)))


def bernstein(p,lo,hi):
    n=len(p)-1
    v=[sum((p[i]*comb(i,k)*lo**(i-k)*(hi-lo)**k for i in range(k,n+1)),F()) for k in range(n+1)]
    return [sum((v[k]*F(comb(j,k),comb(n,k)) for k in range(j+1)),F()) for j in range(n+1)]


def formula_polynomial():
    h=(1+B,F(-1))
    z=(A+B,F(-1))
    h2,z2=power(h,2),power(z,2)
    first=mul(add(scale(h2,F(3,2)),scale(h,-1)),add(h2,(-C*C,)))
    return add(first,scale(add(power(z,4),(-C**4,)),F(-1,4)),
               scale(power(z,3),-C),scale(z,C**3),
               scale(add(h2,scale(z2,-1)),F(-3,2)*C*C))


DERIVATIVE=(F(39760023849,3906250000),-F(48411347,1953125),F(221343,10000),-F(216,25),F(5,4))
CHANGE=(F(),F(173733429,4000000000000),-F(612392179,2000000000),F(314537,400000),-F(591,800),F(1,4))


def per_bidder_change(theta):
    theta=F(theta)
    require(-F(1,1000)<=theta<=0,'split-cost parameter interval')
    return value(CHANGE,theta)


def total_change(theta):return 2*per_bidder_change(theta)


def calculate():
    require(formula_polynomial()==DERIVATIVE,'closed integral/quartic polynomial identity')
    local=shifted(DERIVATIVE,S0)
    require(derivative(CHANGE)==local,'exact primitive in theta')
    for s in (LOW,S0):
        d,q=s-A,s-B
        h=1-q
        require(0<C<d<A<1 and q>0 and h<1 and h>B-d>C,'parameter chamber')
        require(h-(B-d)==1-A,'moving bundle lower limit stays below cap')
    dpoly=derivative(DERIVATIVE)
    require(max(bernstein(dpoly,LOW,S0))<0,'whole-interval decreasing derivative')
    lower,upper=value(DERIVATIVE,S0),value(DERIVATIVE,LOW)
    require(lower==F(173733429,4000000000000)>0,'derivative at original split cost')
    require(upper==F(514209,781250000),'derivative at lower endpoint')
    require(all(x*((-1)**j)<0 for j,x in enumerate(CHANGE) if j),'base loss for every negative theta')
    path=ROOT.parent/'V3/certificate/baseline_mechanism.json'
    base=json.loads(path.read_text(encoding='utf-8'))
    calibration=F(base['expected']['base'])
    return {
        'scope':'affine-base term only; per-bidder revenue derivative, not the full changed mechanism',
        'interval':[str(LOW),str(S0)],
        'per_bidder_derivative_coefficients':[str(x) for x in DERIVATIVE],
        'per_bidder_change_theta_coefficients':[str(x) for x in CHANGE],
        'total_change_theta_coefficients':[str(2*x) for x in CHANGE],
        'per_bidder_derivative_bounds':[str(lower),str(upper)],
        'derivative_decreasing_Bernstein':[str(x) for x in bernstein(dpoly,LOW,S0)],
        'total_base_revenue_at_s0':str(calibration),
        'calibration_input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'total_base_change_at_lower_endpoint':str(total_change(LOW-S0)),
        'conclusion':'the base term loses for every s in [1.136,1.137); other correction terms must be included separately',
    }


if __name__=='__main__':
    data=calculate()
    path=ROOT/'certificate/base_split_cost.json'
    if '--write' in sys.argv:
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:require(json.loads(path.read_text(encoding='utf-8'))==data,'exact certificate replay')
    print('D1(s0)',data['per_bidder_derivative_bounds'][0])
    print('per-bidder theta coefficients',data['per_bidder_change_theta_coefficients'])
    print('PASS exact full affine-base split-cost derivative and change polynomial')
