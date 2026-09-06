"""Exact selected revenue and comparison with the preserved V4.6.1 bound."""
from pathlib import Path
from fractions import Fraction as F
import json,sys
import constant_kernel as k
import refined_candidate as candidate
ROOT=Path(__file__).resolve().parents[1]

def enclosure(interval,digits=30):
    n=10**digits;lo,hi=interval
    def render(x):
        sign='-' if x<0 else '';s=str(abs(x)).zfill(digits+1)
        return sign+s[:-digits]+'.'+s[-digits:]
    return [render((lo*n).numerator//(lo*n).denominator),render(-((-hi*n).numerator//(-hi*n).denominator))]

def verify():
    a,c,sl,u=candidate.a,candidate.c,candidate.slope,candidate.u
    assert k.affine_hypotheses(a,c,sl,u)
    clean=k.clean(a,c);increment=k.affine_gain(a,c,sl,u)
    assert clean['D']==F(246947,1125000)
    coeffs=(clean['coefficients'][0]+increment,clean['coefficients'][1],clean['coefficients'][2]/1500)
    interval=k.p.bound(coeffs,(F(2),F(493894)))
    old=json.loads((ROOT.parent/'V4_6_1_lower_bound/certificate/branch_summary.json').read_text(encoding='utf-8'))
    old_coeff=tuple(map(F,old['exact_revenue_coefficients']))
    old_interval=k.p.bound(old_coeff,(F(2),F(11)))
    difference=(interval[0]-old_interval[1],interval[1]-old_interval[0])
    assert difference[0]>F(85,10000000)
    out=dict(status='REFINED_EXACT_CONTINUUM_REVENUE_PASS',field_basis=['1','sqrt(2)','sqrt(493894)'],
        coefficients=list(map(str,coeffs)),revenue_interval=list(map(str,interval)),revenue_enclosure=enclosure(interval),
        gain_over_V4_6_1_enclosure=enclosure(difference),strict_gain_lower='17/2000000',
        clean_capped_coefficients_basis_1_sqrt2_sqrtD=list(map(str,clean['coefficients'])),D=str(clean['D']),
        functional_increment=str(increment),clean_components={name:[str(x) for x in clean[name]] if isinstance(clean[name],tuple) else str(clean[name]) for name in ('base','high','lottery','low','cut','clipping')},
        positive_base_cells=len(clean['base_cells']),base_cell_data=clean['base_cells'],
        mechanism='verifier/refined_candidate.py: mechanism(profile)',
        scope='Exact continuum lower bound for the complete selected candidate; no family or unrestricted optimum assertion')
    path=ROOT/'certificate/refined_revenue.json'
    if '--write' in sys.argv:path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text(encoding='utf-8'))==out
    print(out['status']);print('revenue',out['revenue_enclosure']);print('gain',out['gain_over_V4_6_1_enclosure'])
    return out
if __name__=='__main__':
    if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
    verify()
