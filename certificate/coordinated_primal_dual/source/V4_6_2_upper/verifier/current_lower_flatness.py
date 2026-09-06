"""Strict final-dual gap against the selected V4.6.1 lower mechanism.

The all-real selection proof is research_log/current_lower_flatness.md.
Normal invocation is read-only; --write saves only this new certificate.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from hashlib import sha256
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verifier'))
import sparse_cycle as p
LOWER=ROOT.parent/'V4_6_1_lower_bound'
sys.path.insert(0,str(LOWER/'verifier'))
import functional_exchange as selected

def numerator():
    manifest=json.loads((p.ARCH/'manifest.json').read_text(encoding='utf-8'))
    terms={}
    for e,c in zip(manifest['basis_order'],manifest['theta']):
        e=tuple(e);es=e[1],e[0],e[3],e[2]
        terms=p.add(terms,{e:F(c),es:-F(c)})
    x,y,z,w=[p.var(j) for j in range(4)]
    stream=p.mul(x,p.add(p.ONE,p.scale(x,-1)),y,p.add(p.ONE,p.scale(y,-1)),terms)
    correction=p.swap_bidders(p.scale(p.der(stream,0),-1))
    x2,z2=p.mul(x,x),p.mul(z,z)
    denominator=p.scale(p.mul(x2,z2),2)
    return p.add(p.mul(p.add(p.scale(z2,3),p.scale(p.ONE,-1)),w,x2),p.mul(denominator,correction))

def parameters(t):
    A,c,T,U=F(2,3),F(47,150),F(178,225),F(26,25)
    delta=F(9,16)*(T-t)*(U-t)
    alpha=3*t-2
    return delta,alpha/(alpha+2*delta),delta+alpha/2

def verify():
    center=(F(151,200),F(3,40),F(9,10),F(63,200))
    half=(F(1,10000),)*4
    t0,rho0,x0,y0=[a-h for a,h in zip(center,half)]
    t1,rho1,x1,y1=[a+h for a,h in zip(center,half)]
    A,c,b,s,q,T,U=F(2,3),F(47,150),F(49,50),F(7,6),F(14,75),F(178,225),F(26,25)
    assert (selected.A,selected.c,selected.b,selected.q)==(A,c,b,q)
    assert (selected.base.T,selected.base.U)==(T,U)
    # Entire first opponent row lies in E, with physical item 1 scarce.
    assert A<t0<t1<T and rho1<c and rho1<t0
    d0,beta0,L0=parameters(t0);d1,beta1,L1=parameters(t1)
    assert F(9,16)*(2*t1-T-U)<0  # delta decreases
    assert F(3,2)+F(9,16)*(2*t0-T-U)>0  # L increases
    assert F(9,10)<beta0<beta1<F(49,50)
    # Unique lottery winner on the complete all-real box.
    assert c<y0<y1<c+L0
    assert x0>t1
    assert x0-t1+F(1,2)-y1>0  # lottery beats safe even without positive beta term
    # Opposing bidder has the base row, outside both functional strips.
    assert x0>T and x0>y1 and y0>c
    assert y1<selected.L and rho1<selected.L
    assert min(x0,t0)>selected.U+q
    assert s-y1>A and s-x0<A
    # H=x+y-b, prices P1=x+y-c, P2=y+q, C=x+y.
    assert x0+y0-c>t1
    assert y0+q>rho1
    assert x0+y0>t1+rho1
    assert max(center[:2])-half[0]>F(43,100)
    assert max(center[2:])-half[2]>F(43,100)
    cycles=json.loads((ROOT/'certificate/sparse_cycle.json').read_text(encoding='utf-8'))
    cycle_half=tuple(map(F,cycles['halfwidths']))
    for raw in cycles['orbit_centers']:
        other=tuple(map(F,raw))
        assert any(abs(a-b)>h+k for a,b,h,k in zip(center,other,half,cycle_half))
    # All-real selections above; source checks include every corner and center.
    profiles=[tuple(a+sign*h for a,sign,h in zip(center,signs,half)) for signs in product((-1,1),repeat=4)]
    profiles.append(center)
    for profile in profiles:
        row=selected.mechanism(profile)
        beta=parameters(profile[0])[1]
        assert row['branches']==('base','E_lottery')
        assert row['selected']==('base_0','lottery')
        assert row['allocations']==((F(),F()),(F(1),beta))
        assert row['utilities'][1]>0
    lo,hi=p.bound(p.centered(numerator(),center),half)
    assert hi<0
    denominator_upper=2*(center[0]+half[0])**2*(center[2]+half[2])**2
    absolute=-hi/denominator_upper
    volume=F(1)
    for h in half:volume*=2*h
    assert volume==F(1,625000000000000)
    gap=absolute*volume/50
    result={
        'status':'CURRENT_V4_6_1_LOWER_STRICT_DUAL_GAP_PASS',
        'selected_lower':'V4_6_1_lower_bound/verifier/functional_exchange.py:mechanism',
        'center':list(map(str,center)),'halfwidths':list(map(str,half)),
        'all_real_allocations':['bidder1 empty','bidder2 (1,beta(t))'],
        'branches':['base','E_lottery'],
        'beta_endpoint_values':list(map(str,(beta0,beta1))),
        'beta_bounds':['9/10','49/50'],
        'functional_tent_disjoint':True,'conditional_support_square_disjoint':True,
        'cycle_rectangles_disjoint':len(cycles['orbit_centers']),
        'virtual_numerator_interval':list(map(str,(lo,hi))),
        'virtual_absolute_lower':str(absolute),'box_volume':str(volume),
        'safe_slack_coefficient':'1/50',
        'exact_capacity_plus_virtual_slack_lower':str(gap),
        'source_profile_checks':len(profiles),
        'source_sha256':{f:sha256((LOWER/'verifier'/f).read_bytes()).hexdigest() for f in ('parameter_candidate.py','functional_exchange.py')},
        'scope':'This specific final common dual cannot match the selected V4.6.1 lower mechanism; no suboptimality or optimality claim about that lower mechanism.',
        'proof':'research_log/current_lower_flatness.md'
    }
    target=ROOT/'certificate/current_lower_flatness.json'
    if '--write' in sys.argv:target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(target.read_text(encoding='utf-8'))==result
    print(result['status']);print('positive_slack_lower',float(gap));print('source_checks',len(profiles))
    return result
if __name__=='__main__':verify()
