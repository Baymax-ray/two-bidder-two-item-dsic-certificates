"""Exact finite replays for the all-randomized inner theorem in the note.

No finite-type approximation is used. Polygon examples independently replay
the continuum integration identity; the written argument handles all menus.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent/'V4_5'/'verifier'))
import residual_lottery as old

P, X = old.P, old.X
A, q, c = old.A, old.q, old.c
ALPHA = 3*X-2
LL = old.DELTA+F(1, 2)*ALPHA
YY = c+LL
JJ = 1-F(1, 2)*X
KK = X-q
BB = F(1, 2)+old.DELTA
CC = X+c+old.DELTA
LAM = ALPHA*(c+F(1, 4)*LL)
VALUE = c*X*(1-X)+F(1, 4)*(X-q)
VALUE += (X+c)*((F(3, 2)-c-X)*(1-c)-q*q/2)+old.DELTA**2


def integral(poly, lo, hi):
    return P(poly).integral(lo, hi)


def clip(poly, aa, bb, cc):
    """Closed rational half-plane aa*x+bb*y+cc >= 0."""
    out = []
    if not poly:
        return out
    for p, r in zip(poly, poly[1:]+poly[:1]):
        fp = aa*p[0]+bb*p[1]+cc
        fr = aa*r[0]+bb*r[1]+cc
        if fp >= 0:
            out.append(p)
        if (fp > 0 and fr < 0) or (fp < 0 and fr > 0):
            ratio = fp/(fp-fr)
            out.append(tuple(p[i]+ratio*(r[i]-p[i]) for i in range(2)))
    return out


SQUARE = [(F(0), F(0)), (F(1), F(0)), (F(1), F(1)), (F(0), F(1))]


def region(*planes):
    poly = SQUARE[:]
    for plane in planes:
        poly = clip(poly, *map(F, plane))
    return poly


def moments(poly):
    """Area and first x/y moments by exact oriented polygon formulas."""
    area = mx = my = F(0)
    for p, r in zip(poly, poly[1:]+poly[:1]):
        cross = p[0]*r[1]-r[0]*p[1]
        area += cross/2
        mx += (p[0]+r[0])*cross/6
        my += (p[1]+r[1])*cross/6
    assert area >= 0
    return area, mx, my


def affine_integral(poly, ax=0, ay=0, const=0):
    area, mx, my = moments(poly)
    return ax*mx+ay*my+const*area


def cells(menu):
    result = []
    for ix, (ax, ay, price) in enumerate(menu):
        poly = SQUARE[:]
        for jx, (bx, by, other) in enumerate(menu):
            if jx == ix:
                continue
            if ax == bx and ay == by and price == other and jx < ix:
                poly = []
                break
            poly = clip(poly, ax-bx, ay-by, other-price)
        result.append(poly)
    assert sum(moments(poly)[0] for poly in result) == 1
    return result


def intersection(poly, planes):
    for plane in planes:
        poly = clip(poly, *plane)
    return poly


def line_pieces(menu, fixed, horizontal=True):
    """All exact utility cells on a fixed horizontal or vertical line."""
    breaks = {F(0), F(1)}
    affine = [(ax if horizontal else ay,
               (ay if horizontal else ax)*fixed-p) for ax, ay, p in menu]
    for m, b0 in affine:
        for n, b1 in affine:
            if m != n:
                z = (b1-b0)/(m-n)
                if 0 < z < 1:
                    breaks.add(z)
    breaks = sorted(breaks)
    pieces = []
    for lo, hi in zip(breaks, breaks[1:]):
        midpoint = (lo+hi)/2
        vals = [m*midpoint+b0 for m, b0 in affine]
        ix = vals.index(max(vals))
        pieces.append((lo, hi, ix, P((affine[ix][1], affine[ix][0]))))
    return pieces


def piece_integral(pieces, weight, lo=F(0), hi=F(1), allocation=False, menu=None):
    total = F(0)
    for left, right, ix, utility in pieces:
        low, high = max(left, lo), min(right, hi)
        if low < high:
            integrand = weight*menu[ix][0] if allocation else weight*utility
            total += integral(integrand, low, high)
    return total


def candidate(t):
    delta, beta = old.menu_parameters(t)
    B, C = F(1, 2)+delta, t+c+delta
    return [(F(0), F(0), F(0)), (F(0), F(1), B),
            (F(1), F(0), t), (F(1), F(1), C),
            (F(1), beta, t+beta*c)]


def payment_cut_identity(t):
    delta, beta = old.menu_parameters(t)
    al, L = 3*t-2, delta+(3*t-2)/2
    Y, C, H = c+L, t+c+delta, c+delta
    price = P(t+beta*c)-X
    lower = P(c)-1/beta*X
    upper = P(Y)+1/(1-beta)*X
    new = price*((1-price)*(upper-lower)+beta*F(1, 2)*(upper**2-lower**2))
    displaced = t*(1-t)*(H-lower)
    displaced += C*((1-C)*(upper-H)+F(1, 2)*(upper**2-H**2))
    full = new-displaced
    variation = full-full(0)
    closed = al*L/4*X-al/(4*beta*(1-beta))*X**2
    closed -= 1/(2*beta*(1-beta)**2)*X**3
    assert (variation-closed).zero()
    # Independent exact hinge-polynomial identity used in the trace proof.
    kernel = al*L*L/2-al*L*X-beta*L**3+F(3, 2)*beta*L*L*X
    kernel -= -al/2*X**2+beta/2*X**3
    assert (kernel+beta/2*X*(L-X)**2).zero()
    return dict(t=str(t), variation_coefficients=list(map(str, variation.c)))


def replay_menu(t, menu):
    delta, beta = old.menu_parameters(t)
    al, k, j = 3*t-2, t-q, 1-t/2
    B, C, L = F(1, 2)+delta, t+c+delta, delta+(3*t-2)/2
    Y, lam = c+L, (3*t-2)*(c+L/4)
    assert 0 < k < j < A < t < 1 and c < Y < B < A
    assert beta*L == al/2 and C-Y == j
    f0, fm, fh = 3*B-2, P((3*C-2, -3)), 3*Y-2
    F0 = P((0, -f0))
    Fm = P(-f0*k)+P((0, 3*C-2, -F(3, 2)))(k) - P((0, 3*C-2, -F(3, 2)))
    Fj = Fm(j)
    Fh = P(Fj+fh*j)-fh*X
    Ftop = [(F(0), k, F0), (k, j, Fm), (j, A, Fh), (A, F(1), 1-X)]
    assert F0(k) == Fm(k) and Fm(j) == Fh(j) and Fh(A) == 1-A
    assert all(Fpoly(left) >= 0 and Fpoly(right) >= 0 for left, right, Fpoly in Ftop)
    # Six rectangular/polygonal integration pieces; all inequalities closed.
    G = [([(0, -1, c), (1, 0, -t)], (3, 0, -3*t)),
         ([(0, 1, -c), (0, -1, Y), (1, beta, -t-beta*c)], (3, 3*beta, -3*(t+beta*c))),
         ([(0, 1, -Y), (1, 0, -A)], (3, 0, -3*A))]
    H = [([(1, 0, 0), (-1, 0, k), (0, 1, -B)], (0, 3, -3*B)),
         ([(1, 0, -k), (-1, 0, j), (1, 1, -C)], (3, 3, -3*C)),
         ([(1, 0, -j), (-1, 0, A), (0, 1, -Y)], (0, 3, -3*Y))]
    polys = cells(menu)
    revenue = sum(p*moments(poly)[0] for (_, _, p), poly in zip(menu, polys))
    total_u = sum(affine_integral(poly, ax, ay, -p) for (ax, ay, p), poly in zip(menu, polys))
    gh_u = price_vol = F(0)
    for component, alloc_index in ((G, 0), (H, 1)):
        for planes, density in component:
            for row, poly in zip(menu, polys):
                cut = intersection(poly, planes)
                gh_u += affine_integral(cut, row[0], row[1], -row[2])
                price_vol += row[alloc_index]*affine_integral(cut, *density)
    D0_u = total_u-gh_u
    right = line_pieces(menu, F(1), horizontal=False)
    top = line_pieces(menu, F(1))
    corner = line_pieces(menu, c)
    sg = piece_integral(right, P(al), F(0), c)
    sg += piece_integral(right, P((al+3*beta*c, -3*beta)), c, Y)
    gc = max(ax+ay*c-p for ax, ay, p in menu)
    uc = max(ay*c-p for ax, ay, p in menu)
    Tg = lam*gc-sg
    Ma = t/(t-A)*piece_integral(corner, P(1), A, t, True, menu)
    Ma -= piece_integral(corner, P(1), F(0), t, True, menu)
    Su = 3*D0_u-lam*uc
    top_price = sum(piece_integral(top, weight, left, right0, True, menu)
                    for left, right0, weight in Ftop)
    line_price = 3*t*(c+L/4)*piece_integral(corner, P(1), A, t, True, menu)
    line_price += lam*piece_integral(corner, P(1), t, F(1), True, menu)
    pi_a = price_vol+top_price+line_price
    assert pi_a-revenue == Tg+lam*Ma+Su
    assert min(Tg, Ma, Su) >= 0
    return dict(t=str(t), revenue=str(revenue), priced_allocation=str(pi_a),
                trace_slack=str(Tg), monotonicity_slack=str(Ma),
                sink_slack=str(Su), options=len(menu))


def verify():
    assert (old.DELTA-F(9, 16)*(old.T-X)*(old.U-X)).zero()
    assert (CC-YY-JJ).zero() and (BB-CC+KK).zero()
    integral_f = (3*BB-2)*KK+(3*CC-2)*(JJ-KK)-F(3, 2)*(JJ**2-KK**2)
    integral_f += (3*YY-2)*(A-JJ)+(1-A)
    assert integral_f.zero()
    assert LL(old.T) == q
    assert (LL.derivative()-(F(9, 8)*X+F(3, 4)-F(3, 2)*q)).zero()
    margin = 3*(A-q)*q-2*q*(c+q/4)
    assert margin == q*(1-F(3, 2)*q) > 0
    examples = []
    payment_cuts = []
    for t in (F(67, 100), F(7, 10), F(3, 4), F(4, 5)):
        payment_cuts.append(payment_cut_identity(t))
        own = replay_menu(t, candidate(t))
        assert own['revenue'] == own['priced_allocation']
        assert F(own['revenue']) == VALUE(t)
        examples.append(dict(label='candidate', **own))
        for label, menu in (
            ('empty', [(F(0), F(0), F(0))]),
            ('low_price_deterministic', [(F(0), F(0), F(0)), (F(1), F(0), F(1, 3)), (F(0), F(1), F(2, 5)), (F(1), F(1), F(3, 5))]),
            ('both_marginals_interior', [(F(0), F(0), F(0)), (F(2, 5), F(3, 5), F(1, 5)), (F(3, 4), F(1, 3), F(2, 5)), (F(1), F(1), F(4, 5))]),
            ('first_probability_below_one', candidate(t)+[(F(3, 5), F(1), F(11, 20)), (F(4, 5), F(1, 5), F(9, 20))])):
            examples.append(dict(label=label, **replay_menu(t, menu)))
    actual_checks = 0
    for t in (F(67, 100), F(7, 10), F(4, 5)):
        k = t-q
        for rho in (F(0), (old.b-t)/2, old.b-t):
            for x in (F(0), c, (c+k)/2, k-F(1, 100000)):
                row = old.mechanism((t, rho, x, F(1)))
                assert row['allocations'][0][0] == 1
                actual_checks += 1
            for x in ((2*A+t)/3, (A+t)/2, (A+2*t)/3):
                row = old.mechanism((t, rho, x, c))
                assert row['allocations'][0][0] == 1
                actual_checks += 1
    data = dict(status='INNER_LOTTERY_FULL_RANDOMIZED_CERTIFICATE_PASS',
                scope='global capacity-support identity; full randomized inner optimality under candidate feasibility and H1/H2; no common auction support claimed',
                polynomial_equal_area_identity=True,
                uniform_sink_margin=str(margin),
                conditional_value_coefficients=list(map(str, VALUE.c)),
                exact_polygon_gap_examples=examples,
                exact_payment_cut_polynomial_identities=payment_cuts,
                actual_residual_boundary_checks=actual_checks,
                trusted_continuum_proof='research_log/inner_lottery_certificate.md')
    destination = ROOT/'certificate'/'inner_lottery_certificate.json'
    if '--write' in sys.argv:
        destination.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    else:
        assert json.loads(destination.read_text(encoding='utf-8')) == data
    print(data['status'])
    print('exact_polygon_gap_examples', len(examples))
    print('actual_residual_boundary_checks', actual_checks)
    return data


if __name__ == '__main__':
    verify()

