"""Complete localized non-affine exchange trials over frozen V4.02.

Continuum claims are proved in research_log/functional_exchange.md.
The finite rational replay supplements that proof; it is not a type grid.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json
import sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE.parent/'V4_02'/'verifier'))
import split_cost_candidate as old
base=old.base
q=old.CANDIDATE_SPLIT-old.B
d=old.CANDIDATE_SPLIT-old.A
L,M,U=F(29,100),F(17,50),F(39,100)
HEIGHT=F(1,1000)
NODES=(L,M,U)

def bump(y,height=HEIGHT):
    y,height=F(y),F(height)
    assert 0<=height<=HEIGHT
    if y<=L or y>=U:return F(0)
    return height*(y-L)/(M-L) if y<=M else height*(U-y)/(U-M)

def h(y,mode='up',height=HEIGHT):
    assert mode in ('up','down')
    return F(y)+q+(1 if mode=='up' else -1)*bump(y,height)

def inverse(t,mode='up',height=HEIGHT):
    """Use the affine continuation h(y)=y+q outside [L,U], on all R."""
    t=F(t)
    if t<=L+q or t>=U+q:return t-q
    for lo,hi in zip(NODES,NODES[1:]):
        hlo,hhi=h(lo,mode,height),h(hi,mode,height)
        if hlo<=t<=hhi:return lo+(t-hlo)*(hi-lo)/(hhi-hlo)
    raise AssertionError('Increasing affine-piece inverse covers the image.')

def choose(own,menu,old_mask,mode):
    us=[base.value(own,j)-menu[j] for j in range(4)]
    top=max(us)
    if top==0:mask=0
    elif us[old_mask]==top:mask=old_mask
    elif mode=='drop':
        choices=[j for j in range(4) if j & ~old_mask==0 and us[j]==top]
        assert choices
        mask=min(choices)
    else:
        assert us[2]==top
        mask=2
    return mask,menu[mask],top

def mechanism(profile,mode='up',height=HEIGHT):
    profile=tuple(map(F,profile))
    baseline=old.candidate(profile)
    w,v=profile[:2],profile[2:]
    menus=[list(p) for p in baseline['menus']]
    e=bump(v[1],height)
    if mode=='up':
        menus[0][2]+=e;menus[0][3]+=e
    elif mode=='down':menus[0][2]-=e
    else:raise ValueError(mode)
    row1=choose(w,menus[0],baseline['masks'][0], 'drop' if mode=='up' else 'new_singleton')
    in_Q=old.frozen.in_solved_region(w)
    if in_Q and w[1]>d:
        k=inverse(w[1],mode,height)
        C=F(5,6)+F(3,4)*k*k
        menus[1]=list(map(old.v3.asquad,(0,C-k,F(2,3),C)))
        us=[base.value(v,j)-menus[1][j] for j in range(4)]
        top=max(us)
        mask=next(j for j in (0,1,2,3) if us[j]==top)
        row2=(mask,menus[1][mask],top)
    elif not in_Q and mode=='down':
        eta=inverse(w[1],mode,height)-(w[1]-q)
        assert eta>=0
        menus[1][2]+=eta;menus[1][3]+=eta
        row2=choose(v,menus[1],baseline['masks'][1],'drop')
    else:
        row2=(baseline['masks'][1],baseline['payments'][1],baseline['utilities'][1])
    masks=(row1[0],row2[0])
    assert not masks[0]&masks[1]
    assert row1[2]>=0 and row2[2]>=0
    return dict(profile=profile,mode=mode,height=F(height),menus=tuple(map(tuple,menus)),
                masks=masks,payments=(row1[1],row2[1]),utilities=(row1[2],row2[2]),
                baseline_masks=baseline['masks'])

def verify():
    assert base.C<L<M<U<old.A-q<d
    assert old.A-HEIGHT>U+q+HEIGHT
    assert HEIGHT<min(M-L,U-M)
    assert old.B-(L+q)<d
    checks=inverse_checks=0
    for mode in ('up','down'):
        for height in (F(0),HEIGHT/2,HEIGHT):
            for y in (F(-1),F(0),L,(L+M)/2,M,(M+U)/2,U,F(1),F(2)):
                assert inverse(h(y,mode,height),mode,height)==y
                inverse_checks+=1
            for y in (L,(L+M)/2,M,(M+U)/2,U):
                t=h(y,mode,height)
                for r in (F(0),old.B-t,F(2,3),F(1)):
                    for x in (F(0),d,old.A,F(1)):
                        for z in (y-F(1,100000),y,y+F(1,100000)):
                            mechanism((r,t,x,z),mode,height)
                            checks+=1
            for profile in ((0,0,0,0),(1,1,1,1),(0,d,1,base.C),
                            (0,F(3,5),1,F(7,20)),(old.B/2,old.B/2,1,1)):
                mechanism(profile,mode,height);checks+=1
    # At zero amplitude the complete menus, selected masks and payments agree.
    for profile in ((0,0,0,0),(1,1,1,1),(0,F(3,5),1,F(7,20)),
                    (F(3,10),F(3,5),F(7,10),F(2,5)),(old.B/2,old.B/2,1,1)):
        b0=old.candidate(profile)
        for mode in ('up','down'):
            n0=mechanism(profile,mode,F(0))
            for key in ('menus','masks','payments','utilities'):
                assert n0[key]==b0[key],key
            checks+=1
    # Strict inverse-threshold transfer at a non-affine tent peak.
    witness=(F(1,100),M+q+HEIGHT/2,F(1),M)
    b0=old.candidate(witness)
    up=mechanism(witness,'up')
    assert b0['masks']==(2,1) and up['masks']==(0,3)
    witness_down=(F(1,100),M+q-HEIGHT/2,F(1),M)
    b1=old.candidate(witness_down)
    down=mechanism(witness_down,'down')
    assert b1['masks']==(0,3) and down['masks']==(2,1)
    return dict(scope='exact bounded replay plus separately written all-real proof; no aggregate revenue claim',
                inverse_checks=inverse_checks,pointwise_checks=checks,
                h_nodes=list(map(str,NODES)),height=str(HEIGHT),q=str(q),
                witness_up=list(map(str,witness)),old_up=b0['masks'],new_up=up['masks'],
                witness_down=list(map(str,witness_down)),old_down=b1['masks'],new_down=down['masks'],
                exact_full_inner_region='Q remains certified for both trial modes at actual changed residual',
                global_optimality_claim=False)

if __name__=='__main__':
    data=verify()
    # JSON normalization makes tuple-valued payloads canonical.
    data=json.loads(json.dumps(data))
    path=HERE/'certificate'/'functional_exchange.json'
    if '--write' in sys.argv:path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text(encoding='utf-8'))==data
    print('FUNCTIONAL_EXCHANGE_POINTWISE_EXACT_PASS',data['pointwise_checks'],data['inverse_checks'])
