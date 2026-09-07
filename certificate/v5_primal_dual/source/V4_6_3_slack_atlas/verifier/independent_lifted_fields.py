"""Independent exact reconstruction of every lifted radial field.

No archived polynomial operations or competitor builder is imported during
construction. Coefficientwise source comparison is a separate replay step.
"""
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict
from itertools import product
from hashlib import sha256
import json,sys,importlib.util
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O')
ROOT=Path(__file__).resolve().parents[1]
ARCH=ROOT.parents[3]/'research/closed/two-bidder-two-item-dsic-certificates/certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound'

def corrections():
    source=json.loads((ARCH/'manifest.json').read_text(encoding='utf-8'))
    result=[defaultdict(F),defaultdict(F)]
    for exponent,coefficient in zip(source['basis_order'],source['theta']):
        exponent=tuple(exponent);coefficient=F(coefficient)
        reflected=exponent[1],exponent[0],exponent[3],exponent[2]
        assert exponent<reflected
        for ex,co in ((exponent,coefficient),(reflected,-coefficient)):
            # Expand x(1-x)y(1-y), then differentiate the individual term.
            for dx,dy in product((1,2),repeat=2):
                ep=(ex[0]+dx,ex[1]+dy,ex[2],ex[3]);cp=co*((-1)**(dx+dy))
                for item,axis,sign in ((0,1,1),(1,0,-1)):
                    ee=list(ep);ee[axis]-=1
                    result[item][tuple(ee)]+=cp*ep[axis]*sign
    return tuple({ex:co for ex,co in pp.items() if co} for pp in result),source

def fields(charts):
    """Return [bidder][physical item] polynomials for s1*s2*phi_ij."""
    correction,_=corrections();out=[[defaultdict(F) for _ in (0,1)] for _ in (0,1)]
    for bidder,item in product((0,1),repeat=2):
        for ep,cp in correction[item].items():
            physical=ep if bidder==0 else (ep[2],ep[3],ep[0],ep[1])
            radial=(physical[0]+physical[1]+1,physical[1-charts[0]],
                    physical[2]+physical[3]+1,physical[3-charts[1]])
            out[bidder][item][radial]+=cp
        ratio=0 if item==charts[bidder] else 1
        if bidder==0:
            out[bidder][item][(2,ratio,1,0)]+=F(3,2)
            out[bidder][item][(0,ratio,1,0)]-=F(1,2)
        else:
            out[bidder][item][(1,0,2,ratio)]+=F(3,2)
            out[bidder][item][(1,0,0,ratio)]-=F(1,2)
    return tuple(tuple({ee:cc for ee,cc in p.items() if cc} for p in ps) for ps in out)

def polynomial_integral(poly,bounds):
    value=F()
    for powers,coefficient in poly.items():
        term=coefficient
        for power,(lo,hi) in zip(powers,bounds):term*=(hi**(power+1)-lo**(power+1))/(power+1)
        value+=term
    return value

def evaluate(poly,point):
    value=F()
    for powers,coefficient in poly.items():
        term=coefficient
        for power,x in zip(powers,point):term*=x**power
        value+=term
    return value

def verify():
    sys.path.insert(0,str(ARCH))
    spec=importlib.util.spec_from_file_location('reference_radial_fields',ARCH/'verify_stream_dual.py')
    source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
    manifest,theta,basis=source.load_manifest()
    counts={};integrals={};comparisons=0
    for charts in product((0,1),repeat=2):
        independent=fields(charts)
        for item in (0,1):
            cc=charts if item==0 else tuple(1-x for x in charts)
            reference=source.competitors(theta,basis,*cc)
            for bidder in (0,1):
                assert independent[bidder][item]==reference[bidder],(charts,bidder,item)
                comparisons+=1
        key=''.join(map(str,charts));counts[key]=[[len(p) for p in row] for row in independent]
        bounds=((F(43,100),F(1)),(F(),F(1)),(F(43,100),F(1)),(F(),F(1)))
        integrals[key]=[[str(polynomial_integral(p,bounds)) for p in row] for row in independent]
    out=dict(status='INDEPENDENT_LIFTED_FIELD_IDENTITY_PASS',polynomial_identities=comparisons,
             meaning='Exact polynomial identity for sr*phi_ij on all four radial charts and both physical items; signed integrals are not nonnegative mechanism slacks',
             monomial_counts=counts,signed_integrals_outside_low_square=integrals,
             stream_manifest_sha256=sha256((ARCH/'manifest.json').read_bytes()).hexdigest(),
             independence='Direct monomial boundary expansion and term differentiation; no archived polynomial helpers used until coefficientwise comparison')
    target=ROOT/'certificate/independent_lifted_fields.json'
    if '--write' in sys.argv:target.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(target.read_text(encoding='utf-8'))==out
    print(out['status']);print('exact_polynomial_identities',comparisons)
    return out
if __name__=='__main__':verify()
