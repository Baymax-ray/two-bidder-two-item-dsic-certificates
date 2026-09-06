"""Exact comparison with the independently developed V4.6.1 lower branch.

This arithmetic check does not itself prove that the lower mechanism is
feasible; that proof and its independent replays live in the lower branch.
"""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
from hashlib import sha256
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]

def decimal_enclosure(lo,hi,places=25):
    s=10**places
    a=lo.numerator*s//lo.denominator
    b=-((-hi.numerator*s)//hi.denominator)
    def fmt(x):return str(x//s)+'.'+str(x%s).zfill(places)
    return [fmt(a),fmt(b)]

def verify():
    source=ROOT.parent/'V4_6_1_lower_bound/certificate/branch_summary.json'
    data=json.loads(source.read_text(encoding='utf-8'))
    assert data['status']=='V4_6_1_LOWER_BOUND_CERTIFIED'
    coeff=tuple(map(F,data['exact_revenue_coefficients']))
    assert coeff==(F(309078860435260513361,367416000000000000000),
                   F(31,1215),-F(170368,664453125))
    lo=hi=coeff[0];s=10**45
    for k,c in zip((2,11),coeff[1:]):
        n=isqrt(k*s*s);assert n*n<k*s*s<(n+1)*(n+1)
        bounds=(F(n,s),F(n+1,s))
        if c<0:bounds=bounds[::-1]
        lo+=c*bounds[0];hi+=c*bounds[1]
    oldlo,oldhi=map(F,data['revenue_enclosure'])
    assert oldlo<=lo<=hi<=oldhi
    ledger=json.loads((ROOT/'certificate/upper_ledger.json').read_text())
    upper=F(ledger['final_upper'])
    assert F(ledger['lower_revenue_decimal_enclosure'][1])<lo<hi<upper
    result={'status':'EXACT_CROSS_BRANCH_BOUND_COMPARISON_PASS',
        'lower_source':'V4_6_1_lower_bound/certificate/branch_summary.json',
        'lower_source_sha256':sha256(source.read_bytes()).hexdigest(),
        'exact_lower_coefficients_basis_1_sqrt2_sqrt11':list(map(str,coeff)),
        'lower_revenue_enclosure':decimal_enclosure(lo,hi),
        'unchanged_exact_upper':str(upper),
        'upper_enclosure':decimal_enclosure(upper,upper),
        'remaining_gap_enclosure':decimal_enclosure(upper-hi,upper-lo),
        'scope':'Exact arithmetic comparison. Lower feasibility uses its separate complete mechanism proof and replays; the upper certificate does not depend on any lower candidate.'}
    target=ROOT/'certificate/current_bound_comparison.json'
    if '--write' in sys.argv:target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(target.read_text(encoding='utf-8'))==result
    print(result['status']);print('current_lower',result['lower_revenue_enclosure'])
    print('current_gap',result['remaining_gap_enclosure'])
    return result
if __name__=='__main__':verify()
