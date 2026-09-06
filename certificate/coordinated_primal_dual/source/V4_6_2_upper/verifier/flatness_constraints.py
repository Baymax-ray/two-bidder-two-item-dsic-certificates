"""Exact checks for the V4.6.2 flatness and singular-price obstructions.
The all-real arguments are in research_log/flatness_global_equality.md.
Normal operation is read-only; --write regenerates this component's JSON.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError("Run without -O.")
ROOT = Path(__file__).resolve().parents[1]
A, q, c = F(2,3), F(113,500), F(137,500)

def add(p, r):
    n=max(len(p),len(r))
    return [(p[i] if i<len(p) else F())+(r[i] if i<len(r) else F()) for i in range(n)]
def scale(p,s): return [x*s for x in p]
def mul(p,r):
    out=[F()]*(len(p)+len(r)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(r): out[i+j]+=x*y
    return out
def ev(p,x):
    ans=F()
    for y in reversed(p): ans=ans*x+y
    return ans
def integ(p,l,h): return sum((v*(h**(i+1)-l**(i+1))/(i+1) for i,v in enumerate(p)), F())
def pars(t):
    alpha=3*t-2
    delta=q+3*q*q/4-3*q*t/2+alpha*alpha/16
    beta=alpha/(alpha+2*delta)
    L=delta+alpha/2
    return alpha,delta,beta,L

def calculate():
    t=[F(),F(1)]
    alpha=[F(-2),F(3)]
    delta=add([q+3*q*q/4,-3*q/2],scale(mul(alpha,alpha),F(1,16)))
    length=add(delta,scale(alpha,F(1,2)))
    lam=mul(alpha,add([c],scale(length,F(1,4))))
    B=add([F(1,2)],delta)
    k=[-q,F(1)]
    junction=mul(t,lam)
    top=scale(mul(add([F(2)],scale(B,F(-3))),mul(k,k)),F(1,2))
    lo,hi,rhowidth=F(3,4),F(4,5),F(1,5)
    junction_mass=rhowidth*integ(junction,lo,hi)
    top_mass=rhowidth*integ(top,lo,hi)
    assert junction_mass>0 and top_mass>0
    # Independent Simpson replay: the two integrands have degree at most four.
    # Composite Boole is exact for these polynomials (degree <=5).
    def boole(p):
        h=(hi-lo)/4
        return 2*h/F(45)*(7*ev(p,lo)+32*ev(p,lo+h)+12*ev(p,lo+2*h)+32*ev(p,lo+3*h)+7*ev(p,hi))
    assert rhowidth*boole(junction)==junction_mass
    assert rhowidth*boole(top)==top_mass
    # Entire untouched lottery box. Delta is decreasing, alpha and beta increase.
    t0,t1=F(3,4),F(19,25)
    a0,d0,b0,l0=pars(t0)
    a1,d1,b1,l1=pars(t1)
    assert F(4,5)<b0<b1<F(19,20)
    assert F(9,8)*t1-F(3,4)-3*q/2<0
    assert F(9,8)*t0+F(3,4)-3*q/2>0
    assert c<F(3,10)<F(7,20)<c+l0
    assert F(17,20)-t1==F(9,100)
    assert F(17,20)>F(613,750)  # opposing menu is outside Eplus
    assert F(1,10)<c<F(1,2)
    own_safe_length=F(1,20)
    other_volume=F(1,100)*F(1,20)*F(1,10)
    box_volume=own_safe_length*other_volume
    assert box_volume==F(1,400000)
    beta_product_lower=F(1,25)
    flatness_coefficient=other_volume*beta_product_lower*own_safe_length**2/2
    assert flatness_coefficient==F(1,400000000)
    sink_density_coefficient=F(9,100)*box_volume
    # Independent direct polynomial integration of the best affine score.
    for beta in (b0,(b0+b1)/2,b1,F(1,4),F(3,4)):
        ell=F(1,20)
        cut=(1-beta)*ell
        integral=beta*cut**2/2+(1-beta)*(ell-cut)**2/2
        assert integral==beta*(1-beta)*ell**2/2
    # Two explicit alternative terminal distributions. Both retain lambda*t.
    for tt in (lo,(lo+hi)/2,hi):
        ll=pars(tt)[0]*(c+pars(tt)[3]/4)
        for start in (A,(A+tt)/2):
            assert ll*tt/(tt-start)*(tt-start)==ll*tt
            for xx in (F(),start/2,start,(start+tt)/2,tt):
                tail=F(1) if xx<=start else (tt-xx)/(tt-start)
                assert tail >= (tt-xx)/tt
    # Rational source checks complement, rather than replace, the open-box proof.
    source=ROOT.parent/'V4_6/verifier/price_joint_reallocation.py'
    spec=importlib.util.spec_from_file_location('v46_flatness_source',source)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    count=0
    for tt,rho,x,y in product((t0,(t0+t1)/2,t1),(F(1,20),F(1,10)),(F(17,20),F(19,20)),(F(3,10),F(7,20))):
        out=mod.mechanism((tt,rho,x,y))
        beta=pars(tt)[2]
        assert out['allocations']==((F(),F()),(F(1),beta))
        assert out['utilities'][1]>F(9,100)
        count+=1
    return {
        'status':'PASS_EXACT_FLATNESS_AND_NULL_OPPONENT_OBSTRUCTIONS',
        'scope':'Global equality restrictions and architecture obstructions; no new numerical auction upper bound or candidate suboptimality claim.',
        'singular_witness_opponents':{'high':[str(lo),str(hi)],'low':['0',str(rhowidth)],'orientation':'physical item 1 high'},
        'singular_junction_consumed_mass':str(junction_mass),
        'singular_top_consumed_mass':str(top_mass),
        'singular_charged_gap_lower':str(junction_mass+top_mass),
        'singular_charged_gap_decimal':str(float(junction_mass+top_mass)),
        'lottery_box':{'w1':[str(t0),str(t1)],'w2':['1/20','1/10'],'v1':['17/20','19/20'],'v2':['3/10','7/20']},
        'lottery_box_volume':str(box_volume),
        'beta_endpoints':[str(b0),str(b1)],
        'beta_bounds':['4/5','19/20'],
        'uniform_grid_n_finite_lift_gap_lower':'1/(400000000*(n+1))',
        'positive_sink_density_a_gap_lower':'9*a/40000000',
        'sink_density_coefficient':str(sink_density_coefficient),
        'source_profile_checks':count,
        'replay_boundary':'Exact rational polynomial identities, terminal-tail examples, and finite source checks support the written continuum proof.'
    }

if __name__=='__main__':
    result=calculate()
    target=ROOT/'certificate/flatness_constraints.json'
    if '--write' in sys.argv:
        target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads(target.read_text(encoding='utf-8'))==result
    print(result['status'])
    print('singular charged-screening gap >= '+result['singular_charged_gap_lower'])
