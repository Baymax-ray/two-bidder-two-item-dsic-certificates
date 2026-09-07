"""Global reserve rebasing: complete exact-report mechanism and revenue ledger.

The all-real DSIC/IR/feasibility proof is in research_log/primal_global.md.
Finite checks here test its implementation, not the universal quantifiers.
Run primal_face_integrals.py separately to replay the face integrations.
"""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from itertools import product
import importlib.util,json,random,sys

if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT.parent/'V4_6_1_1_lower_bound/verifier/refined_candidate.py'
spec=importlib.util.spec_from_file_location('v5_preserved_primal',SOURCE)
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
tau=F(1,100);scale=1-tau

def times(v,c):
    v=source.qd.asquad(v)
    return source.qd.Quad(c*v.r,c*v.s,v.w)

def transform(v):return max((F(v)-tau)/scale,F())

def mechanism(profile):
    v=tuple(map(F,profile));assert len(v)==4 and all(0<=z<=1 for z in v)
    z=tuple(map(transform,v));old=source.mechanism(z)
    allocations=old['allocations']
    assert all(v[2*i+j]>tau or allocations[i][j]==0 for i in (0,1) for j in (0,1))
    payments=tuple(times(old['payments'][i],scale)+tau*sum(allocations[i]) for i in (0,1))
    utilities=tuple(times(old['utilities'][i],scale) for i in (0,1))
    for i in (0,1):
        value=sum((v[2*i+j]*allocations[i][j] for j in (0,1)),F())
        assert value-payments[i]==utilities[i] and utilities[i]>=0 and payments[i]>=0
    assert all(sum(allocations[i][j] for i in (0,1))<=1 for j in (0,1))
    return dict(profile=v,transformed=z,allocations=allocations,payments=payments,
                utilities=utilities,source_selected=old['selected'],source_branches=old['branches'])

def plus(*terms):return [sum((x[k] for x in terms),F()) for k in (0,1)]
def multiple(interval,a):
    q=[a*x for x in interval]
    return q if a>=0 else q[::-1]

def revenue_ledger(faces):
    m={k:list(map(F,v)) for k,v in faces['moment_enclosures'].items()}
    R=[m['R4'],multiple(m['R3'],4),multiple(plus(m['RSJA'],m['Rsame'],m['Rcross']),2),multiple(m['Rone'],4),[F(),F()]]
    N=[m['N4'],multiple(m['N3'],4),multiple(plus(m['NSJA'],m['Nsame'],m['Ncross']),2),multiple(m['N_one'],4),[F(),F()]]
    terms=[multiple(R[k],tau**k*scale**(5-k)) for k in range(5)]
    terms +=[multiple(N[k],tau**(k+1)*scale**(4-k)) for k in range(5)]
    revenue=plus(*terms)
    gain=plus(multiple(R[0],scale**5-1),*terms[1:5],*terms[5:])
    derivative=plus(m['N4'],multiple(m['R3'],4),multiple(m['R4'],-5))
    assert gain[0]>F(3,62500)>0 and derivative[0]>F(3,250)
    return dict(tau=str(tau),scale=str(scale),group_R=[[str(x) for x in a] for a in R],
                group_N=[[str(x) for x in a] for a in N],
                revenue_enclosure=list(map(str,revenue)),gain_enclosure=list(map(str,gain)),
                first_derivative_enclosure=list(map(str,derivative)),
                display_revenue=list(map(float,revenue)),display_gain=list(map(float,gain)),
                display_first_derivative=list(map(float,derivative)),
                clean_strict_gain_lower_bound=str(F(3,62500)))

def witness():
    v=(F(1577,2000),F(123,200),F(3,5),F(4,5));radius=F(1,10000)
    q=source.q
    # On the whole box all transformed coordinates exceed1/2, their sums
    # exceed b, and the base fee vanishes. Thus C_i=sum(v_-i) and the
    # respective singleton surcharges are q and scale*q exactly.
    assert min(v)-radius>tau+scale/2
    assert min(v[0]+v[1],v[2]+v[3])-2*radius>2*tau+scale*source.b
    assert min(v)-radius>source.u
    # Full affine own-option utility lists in this fixed high-sum chart.
    def values(pt,i,surcharge):
        x,y=pt[2*i:2*i+2];w,z=pt[2*(1-i):2*(1-i)+2]
        return (F(),x-w-surcharge,y-z-surcharge,x+y-w-z)
    margins=[]
    for signs in product((-1,1),repeat=4):
        pt=tuple(x+sg*radius for x,sg in zip(v,signs))
        old=source.mechanism(pt);new=mechanism(pt)
        assert old['allocations']==((F(1),F(1)),(F(),F()))
        assert new['allocations']==((F(1),F()),(F(),F(1)))
        for i,selected in ((0,3),(1,0)):
            uu=values(pt,i,q);margins +=[uu[selected]-u for j,u in enumerate(uu) if j!=selected]
        for i,selected in ((0,1),(1,2)):
            uu=values(pt,i,scale*q);margins +=[uu[selected]-u for j,u in enumerate(uu) if j!=selected]
    assert min(margins)>0
    # All these differences are affine on the box, so corner checks prove
    # the same strict choices at every real point of the whole box.
    return dict(center=list(map(str,v)),radius=str(radius),volume=str((2*radius)**4),
                strict_margin=str(min(margins)),region='base/base, both high-sum branches',
                old_allocation=[[1,1],[0,0]],new_allocation=[[1,0],[0,1]],
                proof='All option-utility differences affine on whole box;16 exact vertices checked.')

def implementation_checks():
    rng=random.Random(5001);count=deviations=zero_checks=0
    nodes=(F(),tau/2,tau,tau+F(1,10000),tau+scale*source.A,F(1))
    for v in product(nodes,repeat=4):mechanism(v);count+=1
    for _ in range(250):
        v=tuple(F(rng.randrange(10001),10000) for _ in range(4));truth=mechanism(v);count+=1
        for i in (0,1):
            report=list(v);report[2*i:2*i+2]=[F(rng.randrange(10001),10000) for _ in (0,1)]
            alt=mechanism(report)
            deviation=sum((v[2*i+j]*alt['allocations'][i][j] for j in (0,1)),F())-alt['payments'][i]
            assert truth['utilities'][i]>=deviation;deviations+=1
        for axis in range(4):
            z=list(v);z[axis]=F();out=source.mechanism(z)
            assert out['allocations'][axis//2][axis%2]==0;zero_checks+=1
    # Constants used by the all-real zero-valued-item lemma.
    de=F(9,16)*(source.T-source.A)*(source.U-source.A)
    assert source.B0-source.A>0
    assert F(5,6)+F(3,4)*source.c**2-source.A>0
    assert source.A-source.q-de>0
    return dict(profile_checks=count,random_two_way_deviation_checks=deviations,
                zero_valued_item_sample_checks=zero_checks,
                zero_item_E_margin_lower_bound=str(source.A-source.q-de),
                scope='Bounded implementation checks; universal claims follow from the written convex-composition proof.')

def calculate():
    path=ROOT/'certificate/primal_face_integrals.json'
    faces=json.loads(path.read_text(encoding='utf-8'))
    assert faces['status']=='EXACT_SOURCE_FACE_MOMENTS_PASS'
    assert faces['source_primal_sha256']==sha256(SOURCE.read_bytes()).hexdigest()
    return dict(status='COMPLETE_GLOBAL_PRIMAL_IMPROVEMENT_PASS',construction='coordinatewise reserve rebasing',
                ledger=revenue_ledger(faces),ownership_switch=witness(),checks=implementation_checks(),
                face_certificate_sha256=sha256(path.read_bytes()).hexdigest(),
                source_primal_sha256=sha256(SOURCE.read_bytes()).hexdigest(),
                tie_rule='At transformed profile use the frozen lexicographically first feasible maximizing pair; empty at zero utility.',
                claim_boundary='Strict lower-bound improvement for unrestricted randomized DSIC/IR problem; global optimum remains open.')

if __name__=='__main__':
    out=calculate();path=ROOT/'certificate/primal_global.json'
    if '--write' in sys.argv:path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text(encoding='utf-8'))==out
    print(out['status']);print('revenue',out['ledger']['display_revenue']);print('gain',out['ledger']['display_gain'])
