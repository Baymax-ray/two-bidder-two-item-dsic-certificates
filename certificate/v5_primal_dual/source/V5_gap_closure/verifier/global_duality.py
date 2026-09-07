"""Continuous global SJA support splice, with outward interval integrals.

The candidate support is chosen analytically. This verifier bounds complete
conditional revenue integrals, not finite type-grid mechanisms. IEEE binary64
basic operations are enclosed by nextafter after EVERY operation; final sums
are rational dyadic integers. Polynomial inputs are exact Fractions.
"""
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import spec_from_file_location, module_from_spec
from math import comb, isqrt, prod
from pathlib import Path
import heapq
import json
import sys
import numpy as np

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent
spec = spec_from_file_location('global_splice_exact_polynomials', BASE/'V4_7/verifier/psd_polynomials.py')
old = module_from_spec(spec)
spec.loader.exec_module(old)
CORR = old.CORR
ARCH = old.p.ARCH/'manifest.json'
ZERO = (0, 0, 0, 0)
A, WL, WH, RH = F(2, 3), F(43, 100), F(1, 2), F(7, 20)
KUP = F(195263, 10**6)
Z = F(3, 4)
DOWN, UP = -np.inf, np.inf
DYADIC = 2**40


def enclosure(q):
    q = F(q)
    f = float(q)
    exact = F.from_float(f)
    return (f if exact <= q else np.nextafter(f, DOWN),
            f if exact >= q else np.nextafter(f, UP))


def ia(a, b):
    return np.nextafter(a[0]+b[0], DOWN), np.nextafter(a[1]+b[1], UP)


def im(a, b):
    corners = (a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1])
    return np.nextafter(np.minimum.reduce(corners), DOWN), np.nextafter(np.maximum.reduce(corners), UP)


def isum_floor(values, upward=False, scale=DYADIC):
    vals = np.maximum(values, 0)
    assert np.all(np.isfinite(vals))
    assert float(np.max(vals, initial=0))*len(vals.ravel())*scale < 2**62
    rounded = (np.ceil if upward else np.floor)(vals*scale).astype(np.int64)
    # Multiplication by a power of two is exact here; integers are below 2^53.
    assert np.max(rounded, initial=0) < 2**53
    assert int(np.max(rounded, initial=0))*rounded.size < 2**63
    return F(int(rounded.sum(dtype=np.int64)), scale)


def interval_moments(n, degree):
    assert n > 0 and n & (n-1) == 0
    x = np.arange(n+1, dtype=np.float64)/n
    power = (np.ones_like(x), np.ones_like(x))
    moments = []
    for k in range(1, degree+2):
        power = im(power, (x, x))
        lo = np.nextafter(power[0][1:]-power[1][:-1], DOWN)
        hi = np.nextafter(power[1][1:]-power[0][:-1], UP)
        moments.append((np.maximum(0, np.nextafter(lo/k, DOWN)),
                        np.nextafter(hi/k, UP)))
    return moments


def positive_integral_lower(poly, n):
    degrees = [max(e[j] for e in poly) for j in (0, 1)]
    mx, my = [interval_moments(n, degree) for degree in degrees]
    acc = (np.zeros((n, n)), np.zeros((n, n)))
    for (i, j), coefficient in sorted(poly.items()):
        weight = im((mx[i][0][:, None], mx[i][1][:, None]),
                    (my[j][0][None, :], my[j][1][None, :]))
        acc = ia(acc, im(enclosure(coefficient), weight))
    return isum_floor(acc[0], scale=2**44)


def average_poly(box, ownmax, item):
    moments = []
    for axis in (0, 1):
        lo, hi = box[axis]
        moments.append({k: (hi**(k+1)-lo**(k+1))/((k+1)*(hi-lo)) for k in range(6)})
    out = {(2, int(item != ownmax)): F(3, 2),
           (0, int(item != ownmax)): -F(1, 2)}
    for (x, y, t, r), coefficient in CORR[item].items():
        power = (x+y+1, y if ownmax == 0 else x)
        out[power] = out.get(power, F())+coefficient*moments[0][t]*moments[1][r]
    return {e: c for e, c in out.items() if c}


def opponent_boxes(nt, nr):
    return [((WL+(WH-WL)*i/nt, WL+(WH-WL)*(i+1)/nt),
             (RH*j/nr, RH*(j+1)/nr)) for i in range(nt) for j in range(nr)]


def baseline_lower(boxes, n):
    total = F()
    for idx, box in enumerate(boxes):
        volume = prod(hi-lo for lo, hi in box)
        subtotal = sum((positive_integral_lower(average_poly(box, chart, item), n)
                        for chart in (0, 1) for item in (0, 1)), F())
        total += volume*subtotal
    return total


def polynomial(item, psi_kind):
    out = {}
    def add(e, v):
        out[e] = out.get(e, F())+v
        if not out[e]:
            del out[e]
    if item == 0:
        add((3, 0, 0, 0), F(3)); add((1, 0, 0, 0), -F(1))
    else:
        add((2, 1, 0, 0), F(3)); add((0, 1, 0, 0), -F(1))
    for e, coefficient in CORR[item].items():
        add((e[0]+2, e[1], e[2], e[3]), 2*coefficient)
    psi = {
        'zero': {},
        'middle_band': {0: 6*KUP*KUP, 1: -12*KUP, 2: F(6)},
        'high_low': {0: -F(2), 1: F(3)},
        'high_band': {0: F(2), 1: -F(1)},
    }[psi_kind]
    for exponent, coefficient in psi.items():
        add((2, 0, exponent, 0), -2*coefficient)
    return out


def roots(boxes):
    pieces = [((F(), A), (F(), Z), 'zero'),
              ((F(), KUP), (Z, F(1)), 'zero'),
              ((KUP, A), (Z, F(1)), 'middle_band'),
              ((A, F(1)), (F(), Z), 'high_low'),
              ((A, F(1)), (Z, F(1)), 'high_band')]
    out = []
    for box in boxes:
        for xx, yy, kind in pieces:
            out.append((box+(xx, yy), 0, kind))
        out.append((box+((F(), F(1)), (F(), F(1))), 1, 'zero'))
    return out


def bernstein_upper(poly, box):
    degrees = tuple(max(e[j] for e in poly) for j in range(4))
    shape = tuple(d+1 for d in degrees)
    values = (np.zeros(shape), np.zeros(shape))
    for e, coefficient in poly.items():
        lo, hi = enclosure(coefficient)
        values[0][e] = lo; values[1][e] = hi
    for axis, degree in enumerate(degrees):
        lower, upper = (np.moveaxis(v, axis, 0) for v in values)
        result = (np.zeros_like(lower), np.zeros_like(upper))
        lo, hi = box[axis]
        width = hi-lo
        for i in range(degree+1):
            acc = (np.zeros(lower.shape[1:]), np.zeros(lower.shape[1:]))
            for k in range(degree+1):
                m = sum((F(comb(k, j)*comb(i, j), comb(degree, j))*lo**(k-j)*width**j
                         for j in range(min(i, k)+1)), F())
                if m:
                    acc = ia(acc, im(enclosure(m), (lower[k], upper[k])))
            result[0][i], result[1][i] = acc
        values = tuple(np.moveaxis(v, 0, axis) for v in result)
    assert np.all(values[0] <= values[1])
    return values[1]


def split_controls(values, axis):
    points = np.moveaxis(values, axis, 0)
    degree = len(points)-1
    left, right = np.empty_like(points), np.empty_like(points)
    left[0], right[degree] = points[0], points[-1]
    work = points.copy()
    for step in range(1, degree+1):
        work = np.nextafter(np.nextafter(work[:-1]+work[1:], UP)/2, UP)
        left[step], right[degree-step] = work[0], work[-1]
    return np.moveaxis(left, 0, axis), np.moveaxis(right, 0, axis)


def node_bound(values, box):
    if np.max(values) <= 0:
        return F()
    mass = isum_floor(values, upward=True)/values.size
    return mass*prod(hi-lo for lo, hi in box)/(2*box[0][0]**2)


def cut_box(box, axis):
    midpoint = sum(box[axis])/2
    left, right = list(box), list(box)
    left[axis] = (box[axis][0], midpoint)
    right[axis] = (midpoint, box[axis][1])
    return tuple(left), tuple(right)


def penalty_bound(boxes, max_splits, saved=None):
    definitions = roots(boxes)
    initial = [bernstein_upper(polynomial(item, kind), box) for box, item, kind in definitions]
    if saved is not None:
        total = F(); leaves = 0
        for root_id, ((box, item, kind), coeff) in enumerate(zip(definitions, initial)):
            splits = saved[root_id]
            visited = set()
            def visit(values, region, path):
                nonlocal total, leaves
                if path not in splits:
                    total += node_bound(values, region); leaves += 1
                    return
                visited.add(path)
                axis = splits[path]
                assert 0 <= axis < 4 and values.shape[axis] > 1
                children = split_controls(values, axis)
                regions = cut_box(region, axis)
                for side in (0, 1):
                    visit(children[side], regions[side], path+str(side))
            visit(coeff, box, '')
            assert visited == set(splits)
        return total, saved, leaves
    serial = 0
    heap = []
    split_records = [{} for _ in definitions]
    total = F()
    def insert(values, box, root_id, path):
        nonlocal serial, total
        bound = node_bound(values, box)
        total += bound
        if bound and np.min(values) < 0:
            heapq.heappush(heap, (-float(bound), serial, values, box, root_id, path, bound))
            serial += 1
    for root_id, ((box, item, kind), values) in enumerate(zip(definitions, initial)):
        insert(values, box, root_id, '')
    used = 0
    for used in range(max_splits):
        if not heap:
            break
        _, _, values, box, root_id, path, previous = heapq.heappop(heap)
        variations = [float(np.mean(np.abs(np.diff(values, axis=axis))))*(values.shape[axis]-1)
                      if values.shape[axis] > 1 else -1 for axis in range(4)]
        axis = int(np.argmax(variations))
        split_records[root_id][path] = axis
        total -= previous
        children = split_controls(values, axis)
        child_boxes = cut_box(box, axis)
        for side in (0, 1):
            insert(children[side], child_boxes[side], root_id, path+str(side))
        if (used+1) % 2000 == 0:
            print('penalty splits', used+1, 'certified upper', float(total), flush=True)
    split_count = sum(map(len, split_records))
    return total, split_records, len(definitions)+split_count


def verify(write=False, max_splits=12000, nt=7, nr=7, grid=128):
    assert np.finfo(np.float64).nmant == 52 and np.finfo(np.float64).eps == 2**-52
    assert np.nextafter(np.float64(1), UP) == 1+2**-52
    # KUP>(2-sqrt2)/3 and .85<B0 follow from exact squared comparisons.
    assert 0 < 2-3*KUP and (2-3*KUP)**2 < 2
    assert WH+RH == F(17, 20) and F(29, 20)**2 > 2
    assert WL < WH <= F(1, 2) and RH < WL
    # Item covariance supplies the equal contribution of the swapped J.
    assert {(e[1], e[0], e[3], e[2]): c for e, c in CORR[0].items()} == CORR[1]
    # |D0|=A^2-(2A-B0)^2/2, and (2A-B0)^2=2/9.
    assert A*A-F(2, 9)/2 == F(1, 3)
    target = ROOT/'certificate/global_duality.json'
    if not write:
        reference = json.loads(target.read_text(encoding='utf-8'))
        nt, nr, grid = reference['opponent_partition_t'], reference['opponent_partition_r'], reference['radial_grid']
    boxes = opponent_boxes(nt, nr)
    lower = baseline_lower(boxes, grid)
    print('averaged old positive-part lower', float(lower), flush=True)
    previous = None if write else reference['penalty_split_trees']
    penalty, partition, leaves = penalty_bound(boxes, max_splits, previous)
    denominator = 10**50
    square_lower = isqrt(2*denominator*denominator)
    root2_upper = F(square_lower+1, denominator)
    R0_upper = F(4, 9)+2*root2_upper/27
    area = (WH-WL)*RH
    gain = 4*(lower-area*R0_upper-penalty)
    print('net global gain lower', float(gain), 'penalty upper', float(penalty), flush=True)
    out = {'status': 'CONTINUOUS_GLOBAL_SUPPORT_SPLICE_PASS' if gain > 0 else 'ENCLOSURE_NOT_YET_POSITIVE',
           'global_gain_lower': str(gain), 'global_gain_lower_display': float(gain),
           'averaged_old_positive_part_lower': str(lower), 'opposing_price_excess_upper': str(penalty),
           'single_buyer_revenue_upper': str(R0_upper), 'one_oriented_opponent_area': str(area),
           'opponent_partition_t': nt, 'opponent_partition_r': nr, 'radial_grid': grid,
           'penalty_roots': len(roots(boxes)), 'penalty_leaves': leaves,
           'penalty_split_trees': partition,
           'support_domain': 'W union ((43/100,1/2] x [0,7/20]) union its item swap',
           'support_orientation': 'Inherited orientation on W; orient SJA support by high opponent item on the two added rectangles.',
           'screening_class': 'All randomized pointwise DSIC/IR mechanisms; complete conditional support identities.',
           'interval_arithmetic': 'Binary64 basic arithmetic with outward nextafter at every operation; rational input enclosures and dyadic integer final sums.',
           'stream_manifest_sha256': sha256(ARCH.read_bytes()).hexdigest(),
           'source_polynomial_sha256': sha256((BASE/'V4_7/verifier/psd_polynomials.py').read_bytes()).hexdigest(),
           'conditional_support_proof_sha256': sha256((BASE/'V4_6_2_upper/research_log/conditional_global_splice.md').read_bytes()).hexdigest(),
           'conditional_support_certificate_sha256': sha256((BASE/'V4_6_2_upper/certificate/conditional_global_splice.json').read_bytes()).hexdigest(),
           'no_sale_area': '1/3',
           'overlap_accounting': 'JxJ superadditivity; low-W intersections retained conservatively; inherited QQ first-event improvement must not be subtracted again.',
           'mechanism_changed': False}
    if write:
        target.write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')
    else:
        assert out == reference
        assert gain > 0
    return out


if __name__ == '__main__':
    splits = int(sys.argv[sys.argv.index('--splits')+1]) if '--splits' in sys.argv else 12000
    verify('--write' in sys.argv, max_splits=splits)
