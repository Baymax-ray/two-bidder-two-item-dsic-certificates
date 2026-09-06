"""Exact global gap replays for symmetric and constrained reopened Q.

Written all-real theorem: research_log/inner_diagonal_capacity.md.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'verifier'))
import inner_lottery_certificate as geometry
import outer_bundle_exchange as actual

P, X, A = geometry.P, geometry.X, F(2, 3)


def revenue(a, b, c):
    return (a*(1-a)*(c-a)+b*(1-b)*(c-b)
            +c*((1-c+b)*(1-c+a)-F(1, 2)*(a+b-c)**2))


def candidate(B, C):
    return [(F(), F(), F()), (F(1), F(), A),
            (F(), F(1), B), (F(1), F(1), C)]


def replay(B, C, menu):
    k = C-B
    assert 0 < k < F(1, 2) < A and B <= A
    m = 2*C-F(5, 3)-F(3, 2)*k*k
    assert m > 0
    f0 = 3*B-2
    low = -f0*X
    mid = P(-f0*k)-(3*C-2)*(X-k)+F(3, 2)*(X**2-k*k)
    top_weights = [(F(), k, low), (k, F(1, 2), mid),
                   (F(1, 2), A, mid+m), (A, F(1), 1-X)]
    assert low(k) == mid(k) and mid(A)+m == 1-A
    assert low(0) == 0 and f0 <= 0
    G = [([(1, 0, -A)], (3, 0, -3*A))]
    H = [([(-1, 0, k), (0, 1, -B)], (0, 3, -3*B)),
         ([(1, 0, -k), (-1, 0, A), (1, 1, -C)], (3, 3, -3*C))]
    polys = geometry.cells(menu)
    R = sum(p*geometry.moments(poly)[0] for (_, _, p), poly in zip(menu, polys))
    int_u = sum(geometry.affine_integral(poly, a, b, -p)
                for (a, b, p), poly in zip(menu, polys))
    price_vol = gh_u = F()
    for component, index in ((G, 0), (H, 1)):
        for planes, density in component:
            for row, poly in zip(menu, polys):
                cut = geometry.intersection(poly, planes)
                price_vol += row[index]*geometry.affine_integral(cut, *density)
                gh_u += geometry.affine_integral(cut, row[0], row[1], -row[2])
    D0_u = int_u-gh_u
    top = geometry.line_pieces(menu, F(1))
    bottom = geometry.line_pieces(menu, F())
    vertical = geometry.line_pieces(menu, F(1, 2), horizontal=False)
    price_top = sum(geometry.piece_integral(top, weight, lo, hi, True, menu)
                    for lo, hi, weight in top_weights)
    price_bottom = m*geometry.piece_integral(bottom, P(1), F(), F(1, 2), True, menu)
    # The generic line integrator's allocation slot is x; rotate rows for
    # the vertical-line safe-item price without changing utility pieces.
    rotated_menu = [(b, a, p) for a, b, p in menu]
    price_vertical = m*geometry.piece_integral(vertical, P(1), F(), F(1), True, rotated_menu)
    u00 = max(-p for _, _, p in menu)
    sink = 3*D0_u-m*u00
    pi_a = price_vol+price_top+price_bottom+price_vertical
    assert pi_a-R == sink >= 0
    return dict(B=str(B), C=str(C), k=str(k), mass=str(m),
                revenue=str(R), priced_allocation=str(pi_a), sink=str(sink), options=len(menu))


def verify():
    # General equal-area and anchor-mass identity, as an actual polynomial.
    for k in (F(1, 5), F(7, 25), F(3, 10)):
        C, B = X, X-k
        mass = 2*C-F(5, 3)-F(3, 2)*k*k
        area_D0 = B*k+C*(A-k)-F(1, 2)*(A*A-k*k)
        assert (3*area_D0-mass-1).zero()
        value = revenue(A, A, C)
        assert (value-(F(1, 2)*C**3-2*C**2+F(7, 3)*C-F(8, 27))).zero()
    params = [(A, z, 'symmetric') for z in (F(87, 100), F(89, 100), F(91, 100))]
    for t in (F(51, 100), F(53, 100), F(54, 100)):
        k = t-actual.q
        C0 = F(5, 6)+F(3, 4)*k*k
        assert C0 < actual.b
        C = (C0+actual.b)/2
        params.append((C-k, C, 'constrained'))
    examples = []
    for B, C, label in params:
        own = replay(B, C, candidate(B, C))
        assert own['revenue'] == own['priced_allocation']
        assert F(own['revenue']) == revenue(A, B, C)
        examples.append(dict(label=label+'_candidate', **own))
        for name, menu in (
            ('empty', [(F(), F(), F())]),
            ('interior_lotteries', [(F(), F(), F()), (F(2, 5), F(3, 5), F(1, 5)),
                                   (F(3, 4), F(1, 3), F(2, 5)), (F(1), F(1), F(4, 5))]),
            ('cheap_deterministic', [(F(), F(), F()), (F(1), F(), F(1, 3)),
                                     (F(), F(1), F(2, 5)), (F(1), F(1), F(3, 5))])):
            examples.append(dict(label=label+'_'+name, **replay(B, C, menu)))
    checks = 0
    for B, C, label in params:
        own = (F(1, 2), C-F(1, 2)) if label == 'symmetric' else (C-B+actual.q, B-actual.q)
        assert sum(own) == C
        for x in (F(), F(1, 4), F(1, 2)):
            row = actual.mechanism(own+(x, F()))
            assert row['allocations'][0][0] == 1
            checks += 1
        for y in (F(), (C-F(1, 2))/2, C-F(1, 2)-F(1, 100000)):
            row = actual.mechanism(own+(F(1, 2), y))
            assert row['allocations'][0][1] == 1
            checks += 1
        if label == 'constrained':
            k = C-B
            for x in (F(), k/2, k-F(1, 100000)):
                row = actual.mechanism(own+(x, F(1)))
                assert row['allocations'][0][0] == 1
                checks += 1
    data = dict(status='INNER_DIAGONAL_AND_CONSTRAINED_Q_FULL_CERTIFICATE_PASS',
                scope='full randomized global inner support for symmetric and coupled raised-Q menus; no common auction certificate',
                exact_polygon_gap_examples=examples, actual_occupied_trace_checks=checks,
                proof='research_log/inner_diagonal_capacity.md')
    path = ROOT/'certificate'/'inner_diagonal_capacity.json'
    if '--write' in sys.argv:
        path.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    else:
        assert json.loads(path.read_text(encoding='utf-8')) == data
    print(data['status'])
    print('exact_polygon_gap_examples', len(examples))
    print('actual_occupied_trace_checks', checks)
    return data


if __name__ == '__main__':
    verify()
