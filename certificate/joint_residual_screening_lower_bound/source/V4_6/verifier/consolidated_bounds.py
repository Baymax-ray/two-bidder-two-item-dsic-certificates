"""Exact phase ledger, independent radical/log evaluation, read-only replay."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verifier'))
import independent_revenue as audit
UPPER=F(3715139591287203,4194304000000000)

def log_bounds(ratio):
    # Independent fixed 64-term expansion with explicit geometric tail.
    z=(ratio-1)/(ratio+1)
    assert abs(z)<F(1,2)
    term=z
    total=F()
    for n in range(64):
        total+=2*term/F(2*n+1)
        term*=z*z
    error=2*abs(term)/(129*(1-z*z))
    return total-error,total+error

def outward(pair,digits=22):
    lo,hi=pair
    n=10**digits
    a=(lo*n).numerator//(lo*n).denominator
    b=-((-hi*n).numerator//(-hi*n).denominator)
    def decimal(integer):
        sign='-' if integer<0 else ''
        text=str(abs(integer)).zfill(digits+1)
        return sign+text[:-digits]+'.'+text[-digits:]
    return [decimal(a),decimal(b)]

def verify():
    main=audit.calculate()
    refined=tuple(map(F,main['refined_reference_revenue_interval']))
    joint=json.loads((ROOT/'certificate'/'price_joint_revenue.json').read_text(encoding='utf-8'))
    joint_lo=joint_hi=F(joint['rational_constant'])
    for term in joint['logarithms']:
        a,b=log_bounds(F(term['ratio']))
        c=F(term['coefficient'])
        joint_lo+=c*(a if c>=0 else b)
        joint_hi+=c*(b if c>=0 else a)
    saved_lo,saved_hi=map(F,joint['increment_interval'])
    assert saved_lo<=joint_lo<=joint_hi<=saved_hi
    lower=F(joint['independent_gain_lower'])
    assert joint_lo>lower>0
    total=(refined[0]+joint_lo,refined[1]+joint_hi)
    assert total[1]<UPPER
    addition=tuple(map(F,main['refined_addition_coefficients']))
    gain_lo,gain_hi=audit.interval(addition)
    gain=(gain_lo+joint_lo,gain_hi+joint_hi)
    gap=(UPPER-total[1],UPPER-total[0])
    data=dict(status='V4_6_EXACT_BOUNDS_LEDGER_PASS_NOT_CLOSED',
        strongest_mechanism='verifier/price_joint_reallocation.py: mechanism(profile)',
        exact_expression='R_V4.5 + a0 + a2*sqrt(2) + a23*sqrt(23) + j0 + sum(jq*log(q))',
        algebraic_addition_coefficients=main['refined_addition_coefficients'],
        algebraic_basis=['1','sqrt(2)','sqrt(23)'],
        joint_rational_constant=joint['rational_constant'],joint_logarithms=joint['logarithms'],
        revenue_rational_interval=[str(F(v)) for v in outward(total,35)],revenue_decimal_enclosure=outward(total),
        refined_reference_decimal_enclosure=outward(refined),
        exact_joint_increment_decimal_enclosure=outward((joint_lo,joint_hi),35),
        joint_independent_rational_lower=str(lower),
        gain_over_V4_5_decimal_enclosure=outward(gain),
        inherited_unrestricted_upper=str(UPPER),upper_decimal_enclosure=outward((UPPER,UPPER)),
        remaining_gap_decimal_enclosure=outward(gap),
        prior_revenue_dependency='V4_5/certificate/independent_lottery.json and its frozen exact V4.02 formula',
        upper_status='inherited certificate identity preserved; full upper proof not re-executed this phase',
        conditional_scope='full randomized inner certificates; no common full-auction matching support',
        conclusion='strict lower improvement; unrestricted optimal revenue and attainment unresolved')
    path=ROOT/'certificate'/'consolidated_bounds.json'
    if '--write' in sys.argv:
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads(path.read_text(encoding='utf-8'))==data
    print(data['status'])
    print('revenue_enclosure',data['revenue_decimal_enclosure'])
    print('gain_over_V4_5',data['gain_over_V4_5_decimal_enclosure'])
    print('remaining_gap',data['remaining_gap_decimal_enclosure'])
    return data

if __name__=='__main__':
    verify()
