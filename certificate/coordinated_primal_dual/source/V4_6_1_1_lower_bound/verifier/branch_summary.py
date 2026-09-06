"""Read-only reconciliation of exact revenue, parameters and screening areas."""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import json,sys
import refined_candidate as m

ROOT=Path(__file__).resolve().parents[1]

def verify():
    read=lambda name:json.loads((ROOT/'certificate'/name).read_text(encoding='utf-8'))
    revenue=read('refined_revenue.json');audit=read('refined_revenue_audit.json')
    structure=read('refined_structure_audit.json');wing=read('residual_wing_screening.json')
    coefficients=tuple(map(F,revenue['coefficients']))
    independent=list(map(F,audit['exact_revenue_coefficients_basis_1_sqrt2_sqrt_radicand']))
    assert F(audit['radicand'])==F(493894,1500**2)
    independent[2]/=1500
    assert tuple(independent)==coefficients
    assert revenue['functional_increment']==audit['exact_gain_over_clean']
    for name in ('a','b','c','s','q','A','d','u','slope','jump'):
        assert F(audit['parameters'][name])==getattr(m,name)
    assert structure['extra_floor_slack']==audit['extra_capacity_max_slack']=='37/5000000'
    source_hash=sha256((ROOT/'verifier/refined_candidate.py').read_bytes()).hexdigest()
    assert wing['actual_residual']['source_sha256']==source_hash
    assert m.A<m.b<2*m.A and m.T<1-m.q and m.u<=2*m.c
    areas={'Q':m.A**2-(2*m.A-m.b)**2/2,
           'E':2*m.c*(m.T-m.A),'W':2*m.q*(1-m.q-m.u)}
    assert areas['W']==F(wing['actual_residual']['wing_area'])
    areas['union']=sum(areas.values(),F())
    assert 0<areas['union']<1
    out=dict(status='V4_6_1_1_LOWER_BOUND_CERTIFIED',
        mechanism='verifier/refined_candidate.py: mechanism(profile)',
        mechanism_source_sha256=source_hash,field_basis=revenue['field_basis'],
        exact_revenue_coefficients=revenue['coefficients'],
        revenue_enclosure=revenue['revenue_enclosure'],
        gain_over_V4_6_1_enclosure=revenue['gain_over_V4_6_1_enclosure'],
        strict_gain_lower=revenue['strict_gain_lower'],
        exact_comparison='Independent continuous integrations agree coefficientwise after exact radical conversion',
        certified_conditional_area={key:str(value) for key,value in areas.items()},
        conditional_scope='Both bidders, actual residual, full randomized DSIC/IR conditional optimum on disjoint Q, E and W; area is in opponent-report space',
        unresolved_area=str(1-areas['union']),
        screening_does_not_add_revenue=True,
        optimality='No unrestricted auction optimum, common global capacity support, or final parameter-family optimum claimed',
        baseline='V4_6_1_lower_bound; its saved 52-file manifest is verified separately')
    path=ROOT/'certificate/branch_summary.json'
    if '--write' in sys.argv:path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:assert read('branch_summary.json')==out
    print(out['status']);print('independent_coefficients_agree',True)
    print('conditional_areas',out['certified_conditional_area'])
    return out

if __name__=='__main__':
    if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
    verify()
