"""Independent exact arithmetic checks and complete replay of the support splice."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import comb,prod
import importlib.util,json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
def run(write=False):
    path=ROOT/'verifier/global_duality.py'
    spec=importlib.util.spec_from_file_location('upper_splice_primary',path)
    g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    reference=g.verify(False)
    boxes=g.opponent_boxes(reference['opponent_partition_t'],reference['opponent_partition_r'])
    degree=max(max(e) for chart in (0,1) for item in (0,1)
               for e in g.average_poly(boxes[0],chart,item))
    moments=0
    for n in (1,2,8,128):
        values=g.interval_moments(n,degree)
        for k,(lo,hi) in enumerate(values):
            for j in range(n):
                a,b=F(j,n),F(j+1,n)
                exact=(b**(k+1)-a**(k+1))/(k+1)
                assert F.from_float(float(lo[j]))<=exact<=F.from_float(float(hi[j]))
                moments+=1
    kinds=('zero','middle_band','high_low','high_band')
    coefficients=0
    for item in (0,1):
        for kind in kinds:
            for coefficient in g.polynomial(item,kind).values():
                lo,hi=g.enclosure(coefficient)
                assert F.from_float(float(lo))<=coefficient<=F.from_float(float(hi))
                coefficients+=1
    definitions=g.roots(boxes)
    controls=0
    selected=list(range(6))+list(range(len(definitions)-6,len(definitions)))
    for root in selected:
        box,item,kind=definitions[root]
        p=g.polynomial(item,kind)
        degrees=tuple(max(e[j] for e in p) for j in range(4))
        upper=g.bernstein_upper(p,box)
        indices={tuple(0 for _ in range(4)),degrees,tuple(n//2 for n in degrees)}
        for j in range(4):
            indices.add(tuple(degrees[k] if j==k else 0 for k in range(4)))
            indices.add(tuple(0 if j==k else degrees[k] for k in range(4)))
        for index in indices:
            factors=[]
            for axis in range(4):
                lo,hi=box[axis];width=hi-lo
                factors.append({k:sum((F(comb(k,j)*comb(index[axis],j),comb(degrees[axis],j))
                                        *lo**(k-j)*width**j
                                        for j in range(min(index[axis],k)+1)),F())
                                for k in range(degrees[axis]+1)})
            exact=sum((coefficient*prod(factors[j][e[j]] for j in range(4))
                       for e,coefficient in p.items()),F())
            assert exact<=F.from_float(float(upper[index]))
            controls+=1
    gain=4*(F(reference['averaged_old_positive_part_lower'])
            -F(reference['one_oriented_opponent_area'])*F(reference['single_buyer_revenue_upper'])
            -F(reference['opposing_price_excess_upper']))
    assert gain==F(reference['global_gain_lower'])>0
    sources=[path,ROOT/'certificate/global_duality.json',ROOT/'research_log/global_duality.md',g.ARCH]
    out=dict(status='GLOBAL_SUPPORT_SPLICE_INDEPENDENT_AUDIT_PASS',
             scope='Full primary continuous-cell replay plus independent exact arithmetic comparisons; written source-aware identities reviewed separately.',
             primary_root_count=reference['penalty_roots'],primary_leaf_count=reference['penalty_leaves'],
             exact_monomial_integral_comparisons=moments,
             rational_coefficient_enclosure_comparisons=coefficients,
             selected_exact_Bernstein_control_comparisons=controls,
             selected_Bernstein_roots=len(selected),
             exact_global_gain_lower=str(gain),
             sources={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):
                      hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})
    output=ROOT/'discovery/upper_splice_audit.json'
    if write:output.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(output.read_text())==out
    print(out['status']);print(moments,coefficients,controls)
    return out
if __name__=='__main__':
    if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
    run('--write' in sys.argv)
