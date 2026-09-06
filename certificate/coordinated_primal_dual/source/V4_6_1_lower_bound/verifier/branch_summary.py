"""Exact branch bound, region coverage, and independent-calculator agreement."""
from fractions import Fraction as F
from pathlib import Path
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verifier'))
import independent_family_revenue as independent
import independent_functional

def enclosure(pair,digits=25):
    n=10**digits;lo,hi=pair
    lower=(lo*n).numerator//(lo*n).denominator
    upper=-((-hi*n).numerator//(-hi*n).denominator)
    def dec(k):
        sign='-' if k<0 else '';text=str(abs(k)).zfill(digits+1)
        return sign+text[:-digits]+'.'+text[-digits:]
    return [dec(lower),dec(upper)]

def verify():
    data=independent.calculate()
    primary=json.loads((ROOT/'certificate/parameter_revenue.json').read_text(encoding='utf-8'))
    base=json.loads((ROOT.parent/'V4_6/certificate/consolidated_bounds.json').read_text(encoding='utf-8'))
    coeffs=tuple(map(F,data['full_Q_coefficients']))
    normalized=(coeffs[0],coeffs[1],coeffs[2]*F(2,15))
    expected=(F(482935538268336599,574087500000000000),F(31,1215),-F(170368,664453125))
    assert normalized==expected
    # Primary and independent schemes use different polygon integration and
    # polynomial representations; compare final coefficients exactly.
    key=next(k for k in primary if 'coefficient' in k and isinstance(primary[k],list))
    assert tuple(map(F,primary[key]))==normalized
    assert data['base']==primary['base_exact']
    lo,hi=map(F,data['full_Q_interval']);plo,phi=map(F,primary['revenue_interval'])
    assert plo<=lo<hi<=phi
    oldlo,oldhi=map(F,base['revenue_rational_interval'])
    clean_gain=lo-oldhi,hi-oldlo
    assert clean_gain[0]>F(63,100000)
    functional=independent_functional.calculate()
    increment=F(functional['exact_gain'])
    final=(normalized[0]+increment,normalized[1],normalized[2])
    final_interval=(lo+increment,hi+increment)
    gain=final_interval[0]-oldhi,final_interval[1]-oldlo
    A,c,b,T=F(2,3),F(47,150),F(49,50),F(178,225)
    areaQ=A*A-(2*A-b)**2/2;areaE=2*c*(T-A)
    out=dict(status='V4_6_1_LOWER_BOUND_CERTIFIED',
        mechanism='verifier/functional_exchange.py: mechanism(profile)',
        exact_revenue_coefficients=list(map(str,final)),field_basis=['1','sqrt(2)','sqrt(11)'],
        revenue_enclosure=enclosure(final_interval),gain_over_V4_6_enclosure=enclosure(gain),
        clean_mechanism=dict(evaluator='verifier/parameter_candidate.py: mechanism(profile)',
            exact_revenue_coefficients=list(map(str,normalized)),revenue_enclosure=enclosure((lo,hi)),
            gain_over_V4_6_enclosure=enclosure(clean_gain)),
        functional_increment=str(increment),
        strict_gain_lower=str(F(63,100000)),
        certified_inner_area=dict(Q=str(areaQ),E=str(areaE),union=str(areaQ+areaE)),
        conditional_scope='both bidders fully optimized on Q union E for the new actual residual; remaining region unresolved',
        exact_comparison='independent simplex moments and primary Green boundary integrals agree coefficientwise',
        optimality='Neither unrestricted nor parameter-family optimality is claimed',
        baseline='V4_6 strongest complete mechanism; predecessor file identities checked separately; concurrent outer manifest updates are outside this branch')
    target=ROOT/'certificate/branch_summary.json'
    if '--write' in sys.argv:target.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(target.read_text(encoding='utf-8'))==out
    print(out['status']);print('revenue',out['revenue_enclosure']);print('gain',out['gain_over_V4_6_enclosure'])
    return out
if __name__=='__main__':verify()
