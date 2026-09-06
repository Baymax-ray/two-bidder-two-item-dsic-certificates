"""Pointwise rational evaluator for a split-cost continuation of frozen V3.1.

The continuum proof is research_log/split_cost_independent_audit.md.
This script does not calculate or certify the sign of aggregate revenue change.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V3_1'/'verifier'))
import constrained_candidate as frozen

v3=frozen.v3
base=v3.base
A,B,S=base.A,base.B,base.S
TWO_THIRDS=F(2,3)
THETA_LIMIT=F(1,1000)
CANDIDATE_THETA=-THETA_LIMIT
CANDIDATE_SPLIT=S+CANDIDATE_THETA
assert CANDIDATE_SPLIT==F(142,125)


def check_theta(theta):
    theta=F(theta)
    assert -THETA_LIMIT<=theta<=THETA_LIMIT
    return theta


def base_menu(opponent,theta=F(0)):
    theta=check_theta(theta)
    opponent=tuple(map(F,opponent))
    assert len(opponent)==2 and all(0<=value<=1 for value in opponent)
    pivot=base.pivot(opponent)
    split=S+theta
    prices=(F(0),pivot+min(A,split-opponent[1]),
            pivot+min(A,split-opponent[0]),pivot+B)
    assert prices[1]+prices[2]-prices[3]>=split-B>0
    return prices


def increments(opponent):
    """Frozen V3 full menu minus the frozen original shared-base menu."""
    opponent=tuple(map(F,opponent))
    joined=v3.menu(opponent)
    prices=joined[0] if joined is not None else base.menu(opponent)['prices']
    original_base=base.base_menu(opponent)
    delta=tuple(v3.asquad(price)-old_price for price,old_price in zip(prices,original_base))
    assert delta[0]==0
    assert min(delta[1],delta[2])>=0
    assert delta[3]==max(delta[1],delta[2])
    return delta


def retained_menu(opponent,theta=F(0)):
    return tuple(price+extra for price,extra in zip(base_menu(opponent,theta),increments(opponent)))


def screening_menu(opponent,theta=F(0)):
    """Return the full certified inner menu on fixed Q, else None."""
    theta=check_theta(theta)
    opponent=tuple(map(F,opponent))
    if not frozen.in_solved_region(opponent):
        return None
    split=S+theta
    d_new,q_new=split-A,split-B
    t=max(opponent)
    if t<=d_new:
        return frozen.free.SJA_PRICES,(0,1,2,3),'free_inner'
    high_mask=1 if opponent[0]>opponent[1] else 2
    low_mask=3-high_mask
    k=t-q_new
    C=TWO_THIRDS+F(1,6)+F(3,4)*k*k
    prices=[v3.Quad() for _ in range(4)]
    prices[high_mask]=v3.asquad(TWO_THIRDS)
    prices[low_mask]=v3.asquad(C-k)
    prices[3]=v3.asquad(C)
    return tuple(prices),(0,low_mask,high_mask,3),'constrained_inner'


def mechanism(profile,theta=F(0)):
    theta=check_theta(theta)
    profile=tuple(map(F,profile))
    assert len(profile)==4 and all(0<=value<=1 for value in profile)
    types=(profile[:2],profile[2:])
    costs=(F(0),A,A,B,A,A,B,S+theta,S+theta)
    scores=[base.value(types[0],masks[0])+base.value(types[1],masks[1])-cost
            for masks,cost in zip(base.OUTCOMES,costs)]
    maximum=max(scores)
    base_id=next(index for index,score in enumerate(scores) if score==maximum)
    shared=base.OUTCOMES[base_id]
    masks,payments,utilities,menus,branches=[],[],[],[],[]
    for bidder in range(2):
        own,opponent=types[bidder],types[1-bidder]
        menu=retained_menu(opponent,theta)
        values=[base.value(own,j)-menu[j] for j in range(4)]
        best=max(values)
        previous=shared[bidder]
        if best==0:
            selected=0
        elif values[previous]==best:
            selected=previous
        else:
            candidates=[j for j in range(4) if j & ~previous==0 and values[j]==best]
            assert candidates,'New-base subset maximizer must exist.'
            selected=min(candidates)
        assert selected & ~previous==0
        masks.append(selected)
        payments.append(menu[selected])
        utilities.append(best)
        menus.append(menu)
        branches.append('retained_increment')
    inner=screening_menu(types[0],theta)
    if inner is not None:
        menu,priority,branch=inner
        values=[base.value(types[1],j)-menu[j] for j in range(4)]
        best=max(values)
        selected=next(j for j in priority if values[j]==best)
        masks[1],payments[1],utilities[1]=selected,menu[selected],best
        menus[1],branches[1]=menu,branch
    assert not masks[0]&masks[1]
    assert all(value>=0 for value in utilities)
    return dict(profile=profile,theta=theta,base_id=base_id,base_masks=shared,
                masks=tuple(masks),payments=tuple(payments),utilities=tuple(utilities),
                menus=tuple(menus),branches=tuple(branches))


def candidate(profile):
    """The concrete V4.02 trial, with split cost 142/125."""
    return mechanism(profile,CANDIDATE_THETA)


def verify():
    assert B<S-THETA_LIMIT<S+THETA_LIMIT<2*A
    assert 2*(S-THETA_LIMIT-A)>B
    assert S+THETA_LIMIT-A<A
    k=TWO_THIRDS-(S+THETA_LIMIT-B)
    slack=F(5,6)+F(3,4)*k*k-base.C-TWO_THIRDS
    assert slack==F(9247,250000)>0
    cases=[(0,0,0,0),(1,1,1,1),(0,F(3,5),1,F(7,20)),
           (F(51,100),F(1,100),F(3,10),F(3,5)),
           (F(3,5),F(1,100),F(3,5),F(1,2)),
           (F(7,10),F(1,10),F(2,5),F(4,5)),
           (F(1,2),F(1,2),F(3,5),F(2,5)),
           (F(2,3),B-F(2,3),F(1,3),1)]
    checks=0
    for profile in cases:
        original=frozen.mechanism(profile)
        current=mechanism(profile)
        for field in ('masks','payments','utilities','menus'):
            assert current[field]==original[field],field
        checks+=1
    for theta in (-THETA_LIMIT,F(0),THETA_LIMIT):
        d_new,q_new=S+theta-A,S+theta-B
        for profile in cases:
            mechanism(profile,theta)
            checks+=1
        for t in (d_new,F(3,5),TWO_THIRDS):
            for rho in (F(0),B-t):
                if rho>t:
                    continue
                k=t-q_new
                for x in (k-F(1,10000),k,k+F(1,10000)):
                    current=mechanism((rho,t,1,x),theta)
                    if t>d_new:
                        assert (current['masks'][0]==0)==(x>=k)
                    else:
                        assert current['masks'][0]==0
                    checks+=1
        for x in (0,base.C,F(7,20),F(1)):
            for report in ((F(1),F(x)),(F(x),F(1))):
                assert all(value==0 for value in increments(report))
    theta=-THETA_LIMIT
    witness=(F(1,100),F(3,5),F(1),F(373,1000)-theta/2)
    original,current=frozen.mechanism(witness),mechanism(witness,theta)
    assert original['masks']==(0,3) and current['masks']==(2,1)
    assert base.mechanism(witness)['base_masks']==(0,3)
    assert current['payments'][0]==F(1199,2000)
    assert current['utilities'][0]==F(1,2000)
    # A slanted prism: v2=t-q+h, with independent coordinates rho,t,v1,h.
    epsilon=-CANDIDATE_THETA
    prism=((F(1,200),F(3,200)),(F(119,200),F(121,200)),
           (F(99,100),F(1)),(epsilon/4,3*epsilon/4))
    volume=F(1)
    for low,high in prism:
        volume*=high-low
    assert volume==F(1,2000000000)
    assert prism[0][1]+prism[1][1]<B
    assert prism[1][1]<TWO_THIRDS
    xmin=prism[1][0]-base.S+B+prism[3][0]
    xmax=prism[1][1]-base.S+B+prism[3][1]
    assert xmin>base.C and prism[2][0]+xmin>1
    assert xmax<TWO_THIRDS
    assert prism[0][1]<prism[2][0]+xmin-base.C
    for rho,t,y,h in product(*prism):
        x=t-(S-B)+h
        profile=(rho,t,y,x)
        old_row,new_row=frozen.mechanism(profile),candidate(profile)
        assert base.mechanism(profile)['base_masks']==(0,3)
        assert old_row['masks']==(0,3) and new_row['masks']==(2,1)
        assert new_row['payments'][0]==t+h-epsilon
        assert new_row['utilities'][0]==epsilon-h
        assert all(value==0 for value in increments((y,x)))
        checks+=1
    print('SPLIT_COST_CANDIDATE_POINTWISE_EXACT_PASS')
    print('uniform_inner_slack',slack)
    print('bounded_checks',checks+1)
    print('witness',tuple(map(str,witness)))
    print('old_masks',original['masks'],'new_masks',current['masks'])
    print('strict_transfer_prism_volume',volume)
    print('candidate_split_cost',CANDIDATE_SPLIT)
    print('scope no aggregate revenue sign certified by this replay')


if __name__=='__main__':
    verify()
