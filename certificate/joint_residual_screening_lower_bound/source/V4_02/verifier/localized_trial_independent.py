"""Independent exact smoke replay of the localized joint-fee trial.

Continuum arguments are in research_log/localized_trial_independent.md.
No aggregate revenue or optimality outside the displayed fibers is claimed.
"""
from fractions import Fraction as F
from pathlib import Path
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V3_1'/'verifier'))
import constrained_candidate as old

K0,K1=F(17,50),F(39,100)
Q,B=F(227,1000),F(91,100)


def C(z):
    return F(5,6)+F(3,4)*z*z


def fee_support(v,epsilon):
    y,x=v
    return K0-epsilon<=x<=K1 and y>=C(x-epsilon)-x


def target(w):
    rho,t=w
    return Q+K0<=t<=Q+K1 and 0<=rho<=B-t


def mechanism(profile,epsilon):
    epsilon=F(epsilon)
    assert 0<epsilon<=F(1,200)
    profile=tuple(map(F,profile))
    w,v=profile[:2],profile[2:]
    inherited=old.mechanism(profile)
    masks,payments=list(inherited['masks']),list(inherited['payments'])
    if fee_support(v,epsilon):
        if inherited['utilities'][0]>epsilon:
            payments[0]=payments[0]+epsilon
        else:
            masks[0],payments[0]=0,old.v3.Quad()
    if target(w):
        k=w[1]-Q-epsilon
        price=(F(0),C(k)-k,F(2,3),C(k))
        utility=[old.v3.base.value(v,j)-price[j] for j in range(4)]
        maximum=max(utility)
        masks[1]=next(j for j in (0,1,2,3) if utility[j]==maximum)
        payments[1]=old.v3.asquad(price[masks[1]])
    assert not masks[0]&masks[1]
    return dict(masks=tuple(masks),payments=tuple(payments),
                old=inherited,fee=fee_support(v,epsilon),target=target(w))


def verify():
    assert K0-F(2,200)>0
    assert K0-F(1,200)>F(137,500)
    assert C(K0-F(1,200))>B
    assert Q+K1<F(159,250)
    checks=0
    for epsilon in (F(1,1000),F(1,200)):
        for k in (K0,F(73,200),K1):
            t=Q+k
            for rho in (F(0),B-t):
                for x in (k-epsilon-F(1,4000),k-epsilon,
                          k-epsilon+F(1,4000),k,k+F(1,4000)):
                    result=mechanism((rho,t,1,x),epsilon)
                    assert result['masks'][0] in (0,2)
                    assert (result['masks'][0]==0)==(x>=k-epsilon)
                    checks+=1
        k=F(73,200)
        witness=(F(1,100),Q+k,F(1),k-epsilon/2)
        result=mechanism(witness,epsilon)
        assert result['old']['masks']==(2,1)
        assert result['masks']==(0,3)
        assert result['fee'] and result['target']
        assert result['old']['utilities'][0]==epsilon/2
        checks+=1
        # Outside the closed target, bidder 2 remains exactly the old bidder.
        for t in (Q+K0-F(1,10000),Q+K1+F(1,10000)):
            result=mechanism((F(1,100),t,F(1),K0),epsilon)
            assert not result['target']
            assert result['masks'][1]==result['old']['masks'][1]
            assert result['payments'][1]==result['old']['payments'][1]
            checks+=1
    print('LOCALIZED_TRIAL_INDEPENDENT_EXACT_PASS')
    print('bounded_checks',checks)
    print('scope no total revenue assertion')


if __name__=='__main__':
    verify()
