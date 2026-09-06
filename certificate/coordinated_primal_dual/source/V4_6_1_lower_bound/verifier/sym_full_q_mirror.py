"""Symmetric full-Q mirror with complete jointly feasible menu-maximizing ties."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O')
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V4_6/verifier'))
import outer_bundle_reoptimized as pre
import price_joint_revenue as corner
import free_bidder_one as ff
sys.path.insert(0,str(ROOT.parent/'V4_02/verifier'))
import split_cost_revenue as split
old=pre.previous.strip.previous.old
v3=old.v3
A,a,b,d,q=F(2,3),F(159,250),F(91,100),F(1,2),F(113,500)
B0=v3.Quad(F(4,3),-F(1,3),2)

def in_Q(w):return max(w)<=A and sum(w)<=b

def menu(w):
    if in_Q(w):
        t=max(w)
        if t<=d:
            C=max(B0,v3.asquad(sum(w)));prices=(0,A,A,C);priority=(0,1,2,3)
        else:
            k=t-q;C=max(F(5,6)+F(3,4)*k*k,sum(w));high=1 if w[0]>w[1] else 2;low=3-high
            prices=[0,0,0,C];prices[high]=A;prices[low]=C-k;priority=(0,low,high,3)
        return [(tuple(F(bool(mask&(1<<j))) for j in (0,1)),v3.asquad(prices[mask])) for mask in priority]
    if pre.previous.strip.in_extended_region(w):
        return [(row[0],v3.asquad(row[1])) for row in pre.previous.strip.previous.menu(w)]
    prices=old.retained_menu(w,old.CANDIDATE_THETA)
    return [(tuple(F(bool(mask&(1<<j))) for j in (0,1)),prices[mask]) for mask in range(4)]

def mechanism(profile):
    v,w=tuple(map(F,profile[:2])),tuple(map(F,profile[2:]));types=(v,w)
    menus=(menu(w),menu(v));vals=[];maximizers=[]
    for own,rows in zip(types,menus):
        values=[sum((x*z for x,z in zip(own,al)),F())-p for al,p in rows];best=max(values)
        vals.append(best);maximizers.append([j for j,z in enumerate(values) if z==best])
    pair=next(((j,k) for j,k in product(*maximizers)
               if all(menus[0][j][0][ell]+menus[1][k][0][ell]<=1 for ell in (0,1))),None)
    assert pair is not None,'All-real existence theorem must hold at every report'
    rows=[menus[i][pair[i]] for i in (0,1)]
    return dict(allocations=tuple(row[0] for row in rows),payments=tuple(row[1] for row in rows),
                utilities=tuple(vals),menu_indices=pair)

def calculate():
    I=split.I
    def pair(x,rad):return I(F(x[0]))+F(x[1])*split.old.sqrt_interval(rad)
    source=json.loads((ROOT.parent/'V4/certificate/free_capacity_fibers.json').read_text(encoding='utf-8'))['strict_revenue_gain']
    d0=pair((source['rational'],source['sqrt2_coefficient']),2)+old.frozen.revenue_enclosure()[0]
    theta=split.S_NEW-split.s0;m=split.moments()
    iq=split.pair_interval(split.inner_Q(split.S_NEW))-split.pair_interval(split.inner_Q(split.s0))
    retained=I(split.base_Q(split.S_NEW)-split.base_Q(split.s0))-3*theta*m['Q1']+F(3,2)*theta**2*m['Q0']
    f=ff.calculate()['gain_pair'];g=pre.previous.calculate();coupled=pre.calculate()['constrained_cost_pair']
    one=pair(g['bidder_one_gain_pair'],2)
    two=pair(g['bidder_two_free_cost_pair'],2)+pair(coupled,23)
    delta=d0+iq-retained-pair(f,2)-one+two
    # Corner J is completely evaluated by its predecessor. Read its certified
    # rational enclosure; the symbolic exact J remains the named expression.
    final=json.loads((ROOT.parent/'V4_6/certificate/consolidated_bounds.json').read_text(encoding='utf-8'))
    joint=I(*map(F,corner.calculate()['increment_interval']))
    baseline=I(*map(F,final['revenue_rational_interval']))
    net=delta-joint
    assert net.lo>0
    return delta,dict(net_gain_over_V4_6=split.old.rounded_interval(net,30),
                     total_revenue_interval=split.old.rounded_interval(baseline+net,30),old_Q_gap=split.old.rounded_interval(d0,30),inner_split_change=split.old.rounded_interval(iq,30),
                     retained_Q_split_change=split.old.rounded_interval(retained,30),
                     reverse_Q_gain=split.old.rounded_interval(delta,30),
                     exact_formula='D0 + (IQ(s)-IQ(s0)) - (BQ(s)-BQ(s0)-3theta*M1Q+3theta^2*M0Q/2) - F_gain - G1_gain + G2_free_cost + G2_coupled_cost',
                     revenue_formula='R_V4.6 - J + reverse_Q_gain',
                     caveat='J is deliberately removed; old corner region is restored before complete symmetric Q screening')

def verify():
    delta,revenue=calculate();assert delta.lo>F(2523,10**8)
    cases=0
    own=[(F(),F()),(F(1),F(1)),(F(1,2),F()),(F(51,100),F(1,10)),(F(3,5),F(3,10)),
         (F(13,20),F(1,4)),(A,b-A),(F(7,10),F(1,10)),(F(7,10),F(137,500)),
         (F(11,25),F(11,25)),(F(1,2),F(39,100)),(F(1,3),A)]
    for v,w in product(own,repeat=2):
        m=mechanism(v+w);assert all(u>=0 for u in m['utilities']);cases+=1
    ties=0
    for t in (F(51,100),F(3,5),A):
        for rho in (F(),(b-t)/2,b-t):
            w=(t,rho);k=t-q
            C=max(F(5,6)+F(3,4)*k*k,sum(w))
            for v in ((k,F(1)),(k-F(1,10000),F(1)),(k+F(1,10000),F(1)),(A,F()),
                      (F(1,2),C-F(1,2)),(F(1,2),C-F(1,2)-F(1,10000))):
                for profile in (v+w,w+v,tuple(reversed(v))+tuple(reversed(w))):
                    mechanism(profile);ties+=1
    data=dict(status='SYM_FULL_Q_MIRROR_EXACT_PASS',scope='complete pointwise symmetric menu mechanism; full inner Q screening; no global optimum',
              revenue=revenue,pointwise_cases=cases,boundary_cases=ties,
              proof='research_log/sym_full_q_mirror.md')
    p=ROOT/'certificate/sym_full_q_mirror.json'
    if '--write' in sys.argv:p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(p.read_text(encoding='utf-8'))==data
    print(data['status']);print('conditional_Q_gain',float(delta.lo));return data
if __name__=='__main__':verify()
