"""Exact small witnesses for joint threshold and junction propagation.

This is not a revenue improvement or a full type-grid verification.
General pointwise claims are proved in research_log/joint_compatibility.md.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

if not __debug__:
    raise RuntimeError('Run without -O')

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / 'V3_1/verifier'))
import constrained_candidate as current


def evaluate():
    w, v = (F(3,4), F(7,10)), (F(1), F(7,20))
    before = current.mechanism(w+v)
    assert before['masks'] == (2,1)
    expected = ((0,F(269,250),F(577,1000),F(27,20)),
                (0,F(977,1000),F(927,1000),F(29,20)))
    assert before['menus'] == expected
    shift = F(53,1000)
    new_prices = list(before['menus'][0])
    new_prices[2] += shift
    utilities = [current.v3.base.value(w,k)-new_prices[k] for k in range(4)]
    assert utilities == [0,-F(163,500),F(7,100),F(1,10)]
    assert utilities[3] > max(utilities[:3])
    assert 3 & before['masks'][1] == 1
    old_junction = F(27,20)-F(577,1000)
    new_junction = old_junction-shift
    assert old_junction == F(773,1000)
    assert new_junction == F(18,25) < w[0] < old_junction

    target_w = (F(0),F(3,5))
    lam, q = F(547,600), F(227,1000)
    source_w = tuple(lam*z for z in target_w)
    source = current.mechanism(source_w+v)
    original = current.mechanism(target_w+v)
    assert original['masks'] == (2,1)
    assert source['masks'] == (0,3)
    assert source['payments'] == (0,F(3413,3750))
    target_threshold = lam*target_w[1]-q
    assert target_threshold == F(8,25)
    assert (target_threshold+q)/lam == target_w[1]

    feasible_mask_pairs = [(i,j) for i in range(4) for j in range(4) if i&j == 0]
    assert len(feasible_mask_pairs) == 9
    return {
        'status': 'JOINT_GEOMETRY_EXACT_PASS',
        'scope': 'Exact witnesses and affine inverse identity; no expected-revenue improvement asserted',
        'singleton_shift_profile': list(map(str,w+v)),
        'old_masks': list(before['masks']),
        'old_menus': [list(map(str,p)) for p in before['menus']],
        'singleton2_price_shift': str(shift),
        'shifted_first_utilities': list(map(str,utilities)),
        'incompatible_graft_masks': [3,1],
        'item2_to_bundle_junction': [str(old_junction),str(new_junction)],
        'compression_lambda': str(lam),
        'compression_profile': list(map(str,target_w+v)),
        'compression_source_profile': list(map(str,source_w+v)),
        'compression_old_masks': list(original['masks']),
        'compression_new_masks': list(source['masks']),
        'compression_second_payment': str(source['payments'][1]),
        'compression_target_threshold': str(target_threshold),
        'feasible_deterministic_joint_mask_pairs': [list(pair) for pair in feasible_mask_pairs],
        'not_claimed': ['Improved expected revenue', 'All-report numerical verification',
                        'Actual GemNet model reconstructed', 'Finite-menu optimality for original problem']
    }


if __name__ == '__main__':
    result = evaluate()
    target = ROOT/'certificate/joint_geometry.json'
    if '--write' in sys.argv:
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads(target.read_text(encoding='utf-8')) == result
    print(result['status'])
