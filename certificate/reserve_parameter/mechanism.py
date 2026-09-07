"""Final exact rational-report mechanism. All-real definition is in the paper."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util,sys

if sys.flags.optimize:
    raise RuntimeError('Run without optimized Python mode')
TAU=F(83,10000)
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'certificate/joint_residual_screening_lower_bound/source/V3/verifier'))
path=ROOT/'certificate/coordinated_primal_dual/source/V4_6_1_1_lower_bound/verifier/refined_candidate.py'
spec=importlib.util.spec_from_file_location('reserve_seed',path)
seed=importlib.util.module_from_spec(spec)
spec.loader.exec_module(seed)

def scale_quad(value,factor):
    value=seed.qd.asquad(value)
    return seed.qd.Quad(factor*value.r,factor*value.s,value.w)

def mechanism(profile):
    v=tuple(map(F,profile))
    if len(v)!=4 or not all(0<=x<=1 for x in v):
        raise ValueError('Expected four rational reports in [0,1]')
    scale=1-TAU
    transformed=tuple(max((x-TAU)/scale,F()) for x in v)
    base=seed.mechanism(transformed)
    allocations=base['allocations']
    payments=tuple(scale_quad(base['payments'][i],scale)+TAU*sum(allocations[i]) for i in (0,1))
    utilities=tuple(scale_quad(base['utilities'][i],scale) for i in (0,1))
    assert all(v[2*i+j]>TAU or allocations[i][j]==0 for i in (0,1) for j in (0,1))
    assert all(sum(allocations[i][j] for i in (0,1))<=1 for j in (0,1))
    for i in (0,1):
        value=sum((v[2*i+j]*allocations[i][j] for j in (0,1)),F())
        assert value-payments[i]==utilities[i] and utilities[i]>=0 and payments[i]>=0
    return dict(profile=v,transformed=transformed,allocations=allocations,
                payments=payments,utilities=utilities,selected=base['selected'],branches=base['branches'])
