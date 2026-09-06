"""Exact global revenue change: joint split-cost change plus inner reoptimization.

Frozen V3 menu increments are held as opponent functions; the feasible base
changes jointly. This is a candidate calculation, not a full optimality proof.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V3/verifier'))
import joined_threshold as old
from compression_boundary_sign import P
import base_split_cost as exact_base

T=P((0,1))
a,b,c,d,q=old.a,old.b,old.c,old.d,old.q
s0=old.base.S
S_NEW=F(142,125)
A=F(2,3)
I=old.I

def intv(poly,lo,hi):
    return old.integrate_interval(old.P(P(poly).c),lo,hi)

def integral(poly,lo,hi):
    return P(poly).integral(F(lo),F(hi))

def G(A,B,C):
    return A*(1-A)*(C-A)+B*(1-B)*(C-B)+C*((1-C+B)*(1-C+A)-(A+B-C)**2*F(1,2))

def base_Q(s):
    dd=s-a
    free=dd*dd-(2*dd-b)**2/2
    return (free*G(a,a,b)+2*integral((b-T)*G(P(a),s-T,P(b)),dd,a)
            +2*integral((b-T)*G(T,P(dd),T+c),a,A))

def base_Q_derivative(s):
    dd=s-a
    return (2*integral((b-T)*(b-s+T)*(2-3*(s-T)),dd,a)
            +2*integral((b-T)*(T+c-dd)*(2-3*dd),a,A))

def inner_Q(s):
    dd,qq=s-a,s-b
    free=dd*dd-(2*dd-b)**2/2
    k=T-qq
    R=P(F(59,108))+F(1,4)*k*k-k**3+F(9,16)*k**4
    # pair rational + coefficient*sqrt(2)
    return (free*F(4,9)+2*integral((b-T)*R,dd,A),free*F(2,27))

def pair_interval(pair):
    return I(pair[0])+pair[1]*old.sqrt_interval(2)

def moments():
    k0,k1=old.sqrt_interval(old.r0),old.sqrt_interval(old.r1)
    K,h=old.K,b-q
    C0,C1=b,c+A
    log=old.log_interval((k1+C1)/(k0+C0))
    J0=(k1*C1-k0*C0+K*log)/2
    J1=I((C1**3-C0**3)/3)
    J2=(k1*(2*old.r1+K)*C1-k0*(2*old.r0+K)*C0-K*K*log)/8
    root0=2*(h*J0-J1-b*(h*(k1-k0)-(k1**2-k0**2)/2))
    root1=2*(h*J1-J2-b*(h*(k1**2-k0**2)/2-(k1**3-k0**3)/3))
    all0,all1,Q0,Q1=root0,root1,root0,root1
    k=T-q
    C=P(F(5,6))+F(3,4)*k*k
    # Identical widths below a, then all-fiber and Q widths differ.
    lo=k1+q
    inc=C-b
    add0=intv(2*(b-T)*inc,lo,a)
    add1=intv(2*(b-T)*k*inc,lo,a)
    all0,all1,Q0,Q1=all0+add0,all1+add1,Q0+add0,Q1+add1
    inc=C-T-c
    all0=all0+integral(2*c*inc,a,A)
    all1=all1+integral(2*c*k*inc,a,A)
    Q0=Q0+integral(2*(b-T)*inc,a,A)
    Q1=Q1+integral(2*(b-T)*k*inc,a,A)
    cut=F(1058587,1362000)
    inc=P(F(1,2)-c+F(3,4)*q*q)-F(3,2)*q*T
    all0=all0+integral(2*c*inc,A,cut)
    all1=all1+integral(2*c*k*inc,A,cut)
    # Bundle-fee boxes: z=high+low, eta=(low-c)/(z-c-d).
    bundle0=bundle1=F()
    L=T-c-d
    for row in old.base.DATA['bundle_rows']:
        zl,zh=map(F,row['sum_interval'])
        el,eh=map(F,row['normalized_rho_interval'])
        fee=F(row['fee'])
        bundle0+=integral(2*fee*(eh-el)*L,zl,zh)
        bundle1+=integral(2*fee*((eh-el)*(T-d)*L-F(1,2)*(eh*eh-el*el)*L*L),zl,zh)
    all0,all1=all0+bundle0,all1+bundle1
    return dict(all0=all0,all1=all1,Q0=Q0,Q1=Q1,
                root0=root0,root1=root1,bundle0=I(bundle0),bundle1=I(bundle1))

BASE_D=P((F(39760023849,3906250000),-F(48411347,1953125),
          F(221343,10000),-F(216,25),F(5,4)))

def calculate():
    theta=S_NEW-s0
    assert theta==-F(1,1000)
    assert S_NEW-a>=F(1,2) and S_NEW-b>0
    m=moments()
    assert BASE_D.c==exact_base.DERIVATIVE
    base_delta=2*integral(BASE_D,s0,S_NEW)
    assert base_delta==exact_base.total_change(theta)
    fee_delta=-3*theta*(2*m['all1']-m['Q1'])+F(3,2)*theta*theta*(2*m['all0']-m['Q0'])
    IQ0,IQ1=inner_Q(s0),inner_Q(S_NEW)
    inner_delta=pair_interval((IQ1[0]-IQ0[0],IQ1[1]-IQ0[1]))
    baseQ_delta=base_Q(S_NEW)-base_Q(s0)
    gain=I(base_delta-baseQ_delta)+fee_delta+inner_delta
    source=json.loads((ROOT.parent/'V3_1/certificate/constrained_candidate.json').read_text(encoding='utf-8'))
    prior=I(*map(F,source['revenue_rational_interval']))
    revenue=prior+gain
    k=T-q
    Rp=F(1,2)*k-3*k*k+F(9,4)*k**3
    Rc=F(59,108)+c*c/4-c**3+F(9,16)*c**4
    inner_derivative=pair_interval((2*(b-d)*(F(4,9)-Rc)-2*integral((b-T)*Rp,d,A),2*(b-d)*F(2,27)))
    Dbase=sum((co*s0**j for j,co in enumerate(BASE_D.c)),F())
    derivative=2*Dbase-base_Q_derivative(s0)+inner_derivative-3*(2*m['all1']-m['Q1'])
    assert derivative.hi < -F(6,1000)
    assert gain.lo>0
    return {
        'scope':'exact revenue of an explicit feasible candidate; no unrestricted optimality claim',
        'split_cost_old':str(s0),'split_cost_new':str(S_NEW),'theta':str(theta),
        'formula':'DeltaR=2 integral_s0^s Dbase(u)du - (B_Q(s)-B_Q(s0)) + (I_Q(s)-I_Q(s0)) -3 theta (2 M1-M1_Q) +3 theta^2 (2 M0-M0_Q)/2',
        'base_derivative_polynomial':list(map(str,BASE_D.c)),
        'moment_intervals':{key:old.rounded_interval(value,30) for key,value in m.items()},
        'base_total_delta':str(base_delta),'base_Q_delta':str(baseQ_delta),
        'inner_Q_old_pair':list(map(str,IQ0)),'inner_Q_new_pair':list(map(str,IQ1)),
        'fee_delta_interval':old.rounded_interval(fee_delta,30),
        'inner_delta_interval':old.rounded_interval(inner_delta,30),
        'derivative_at_origin_interval':old.rounded_interval(derivative,24),
        'gain_rational_interval':old.rounded_interval(gain,24),
        'revenue_rational_interval':old.rounded_interval(revenue,24),
        'not_claimed':['optimal split cost','full residual screening outside Q','matching full randomized DSIC upper bound']
    }

if __name__=='__main__':
    if sys.flags.optimize: raise SystemExit('Run without -O')
    data=calculate()
    dest=ROOT/'certificate/split_cost_revenue.json'
    if '--write' in sys.argv:dest.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else: assert json.loads(dest.read_text(encoding='utf-8'))==data
    for key in ('derivative_at_origin_interval','gain_rational_interval','revenue_rational_interval'):
        print(key,data[key],[float(F(z)) for z in data[key]])
    print('SPLIT_COST_EXACT_REVENUE_PASS')
