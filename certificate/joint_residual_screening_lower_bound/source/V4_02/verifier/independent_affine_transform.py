"""Bounded exact checks for a global affine report transform of frozen V3.1.

The all-report proof is independent_affine_transform.md. These finite checks
are implementation diagnostics, not the DSIC/capacity proof or revenue bound.
"""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError("Run without -O.")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / 'V3_1' / 'verifier'))
import constrained_candidate as frozen


def transform(profile, lam=F(1), delta=F(0)):
    lam, delta = F(lam), F(delta)
    assert 0 < lam <= 1 and delta >= 0
    w, v = tuple(map(F, profile[:2])), tuple(map(F, profile[2:]))
    assert all(0 <= value <= 1 for value in w+v)
    compressed = tuple(max(F(0), lam*value-delta) for value in w)
    old = frozen.mechanism(compressed+v)
    mask1, mask2 = old['masks']
    assert not mask1 & mask2
    for item in range(2):
        if compressed[item] == 0:
            assert not mask1 & (1 << item)
    # Frozen Quad supports exact comparisons but not division; all examples
    # with an irrational payment use its explicit rational-field coefficients.
    payment_old = old['payments'][0]
    payment1 = frozen.v3.Quad((payment_old.r+delta*mask1.bit_count())/lam,
                             payment_old.s/lam, payment_old.w)
    utility1 = frozen.v3.base.value(w,mask1)-payment1
    expected = old['utilities'][0]
    expected = frozen.v3.Quad(expected.r/lam, expected.s/lam, expected.w)
    assert utility1 == expected and utility1 >= 0
    return dict(masks=old['masks'], payments=(payment1,old['payments'][1]),
                compressed=compressed, inner_certified=frozen.in_solved_region(compressed))


def verify():
    delta = F(53,1000)
    profile = (F(0),F(3,5),F(1),F(7,20))
    old, new = frozen.mechanism(profile), transform(profile,delta=delta)
    assert old['masks']==(2,1) and new['masks']==(0,3)
    assert new['payments'][0]==0 and new['payments'][1]==F(3413,3750)
    assert new['compressed']==(0,F(547,1000)) and new['inner_certified']
    assert new['compressed'][1]-F(227,1000)==F(8,25)

    box=((F(1,200),F(3,200)),(F(119,200),F(121,200)),
         (F(99,100),F(1)),(F(17,50),F(9,25)))
    volume=F(1)
    for lo,hi in box:
        volume*=hi-lo
    assert volume==F(1,50000000)
    assert box[0][1]<delta
    assert box[1][0]-delta>F(501,1000)
    assert box[1][1]-delta<F(2,3)
    assert box[1][1]-delta<box[3][0]+F(227,1000)
    assert box[3][0]-(box[1][1]-delta-F(227,1000))==F(3,200)
    upper_k=box[1][1]-delta-F(227,1000)
    upper_C=F(5,6)+F(3,4)*upper_k**2
    assert upper_C<1 and box[2][0]+box[3][0]>upper_C
    assert box[2][0]>upper_C-F(2,3)
    for point in product(*box):
        old,new=frozen.mechanism(point),transform(point,delta=delta)
        assert old['masks']==(2,1) and new['masks']==(0,3)
        assert new['inner_certified']

    checks=0
    for lam,fee in ((F(1),F(0)),(F(99,100),F(0)),(F(1),delta),(F(99,100),delta)):
        clipped=fee/lam
        profiles=[(0,0,0,0),(1,1,1,1),profile,
                  (clipped,F(3,5),F(1),F(7,20)),
                  (F(3,5),clipped,F(7,20),F(1)),
                  (F(51,100),F(1,100),F(3,10),F(3,5))]
        for example in profiles:
            transform(example,lam,fee)
            checks+=1
    print('INDEPENDENT_AFFINE_TRANSFORM_EXACT_PASS')
    print('strict_transfer_box_volume',volume)
    print('bounded_profile_checks',checks+16)
    print('scope no total revenue improvement certified')


if __name__=='__main__':
    verify()
