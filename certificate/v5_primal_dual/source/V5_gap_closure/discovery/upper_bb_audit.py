"""Independent algebra/source audit of the BB translated-IC branch.

Does not turn a floating search result into a certificate. The selected-cell
primary verifier must still replay all accepted continuous endpoint boxes.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import prod
import importlib.util,json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def evaluate(p,z):return sum((c*prod(x**n for x,n in zip(z,e)) for e,c in p.items()),F())

def run(write=False):
    old=load('upper_bb_original',BASE/'V4_7/verifier/psd_polynomials.py')
    data=json.loads((ROOT/'discovery/bb_centered_fields.json').read_text())
    centers=[tuple(map(F,c)) for c in data['centers']]
    half=tuple(map(F,data['halfwidths']))
    assert centers==[(F(23,40),F(3,5),F(91,100),F(13,40)),
                     (F(29,40),F(23,40),F(91,100),F(13,40))]
    assert half==(F(3,40),F(3,20),F(9,100),F(13,40))
    assert tuple(b-a for a,b in zip(*centers))==(F(3,20),-F(1,40),F(),F())
    original=[old.CORR[0],old.CORR[1],old.p.swap_bidders(old.CORR[0]),old.p.swap_bidders(old.CORR[1])]
    coefficients=0
    for site,center in enumerate(centers):
        for k,p in enumerate(original):
            # Independent binomial expansion, not the discovery Horner shift.
            q=old.p.centered(p,center)
            q={e:c*prod(h**n for h,n in zip(half,e)) for e,c in q.items()}
            stored={tuple(e):F(c) for e,c in data['corrections'][site][k]}
            assert q==stored
            coefficients+=len(q)
    primary=load('upper_bb_interval_primary',ROOT/'discovery/bb_translation_intervals.py')
    scalar_cases=0;positive=0
    for gaps in product((F(-1),F(),F(1)),repeat=4):
        for caps in product((F(),F(2)),repeat=4):
            g1,g2,h1,h2=gaps
            lam=max(F(),min(-40*g2,-F(20,3)*h1,40*h2)) if g1<=0 else F()
            for scale in (F(1,2),F(1)):
                ll=scale*lam
                own=[c+g for c,g in zip(caps,gaps)]
                new=[own[0]-F(3,20)*ll,own[1]+F(1,40)*ll,
                     own[2]+F(3,20)*ll,own[3]-F(1,40)*ll]
                before=sum((max(c,a) for c,a in zip(caps,own)),F())
                after=sum((max(c,a) for c,a in zip(caps,new)),F())
                assert before-after==ll/40
                scalar_cases+=1;positive+=int(ll>0)
    point_checks=0
    for u in product((F(-1),F(),F(1)),repeat=4):
        box=tuple((int(x*primary.S),)*2 for x in u)
        for site,center in enumerate(centers):
            z=tuple(c+h*x for c,h,x in zip(center,half,u))
            interval=primary.fields(box,site)
            for k,p in enumerate(original):
                ownmax=max(z[2*(k//2):2*(k//2)+2])
                exact=z[k]*(F(3,2)-F(1,2)/ownmax**2)+evaluate(p,z)
                assert F(interval[k][0],primary.S)<=exact<=F(interval[k][1],primary.S)
                point_checks+=1
    endpoints=(-2*primary.S,-primary.S//2,0,primary.S//3,2*primary.S)
    intervals=[(a,b) for a in endpoints for b in endpoints if a<=b]
    multiplication_checks=0
    for a,b in product(intervals,repeat=2):
        got=primary.mul(a,b)
        values=[F(x*y,primary.S**2) for x in a for y in b]
        assert F(got[0],primary.S)<=min(values)<=max(values)<=F(got[1],primary.S)
        multiplication_checks+=1
    sources=[ROOT/'discovery/bb_centered_fields.json',ROOT/'discovery/bb_translation_intervals.py',
             ROOT/'discovery/bb_center_fields.py',old.p.ARCH/'manifest.json']
    out=dict(status='BB_FULL_ENVELOPE_ALGEBRA_AND_SOURCE_AUDIT_PASS',
             scope='Independent source reconstruction and exact algebra; selected continuous positive cells need separate full replay.',
             reconstructed_exact_polynomial_coefficients=coefficients,
             scalar_first_event_cases=scalar_cases,positive_scalar_cases=positive,
             exact_radial_chart_point_checks=point_checks,
             interval_multiplication_cases=multiplication_checks,
             single_copy_gain='lambda/40',four_copy_gain='lambda/10',
             incumbent_IC_slack='Nonnegative and retained; not asserted zero.',
             sources={str(p.relative_to(BASE)) if p.is_relative_to(BASE) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})
    path=ROOT/'discovery/upper_bb_audit.json'
    if write:path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text())==out
    print(out['status']);print(coefficients,scalar_cases,point_checks,multiplication_checks)
    return out
if __name__=='__main__':
    if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
    run('--write' in sys.argv)
