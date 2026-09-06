"""Exact rational-plus-log revenue increment of the joint corner trial.

All polynomial arithmetic, partial fractions, and logarithm bounds use
Fractions. Normal replay is read-only; --write creates this certificate.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'verifier'))
import price_joint_reallocation as trial

e, lo, hi = trial.EPS, trial.J0, trial.J1
c, q, d = trial.c, trial.q, F(1, 2)


def trim(p):
    p = list(map(F, p))
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p


def add(p, r):
    return trim([(p[j] if j < len(p) else F())+
                 (r[j] if j < len(r) else F())
                 for j in range(max(len(p), len(r)))])


def scale(p, z):
    return trim([z*x for x in p])


def mul(p, r):
    out = [F()]*(len(p)+len(r)-1)
    for j, a in enumerate(p):
        for k, b in enumerate(r):
            out[j+k] += a*b
    return trim(out)


def power(p, n):
    out = [F(1)]
    for unused in range(n):
        out = mul(out, p)
    return out


def divide(p, r):
    p, r = trim(p), trim(r)
    out = [F()]*max(1, len(p)-len(r)+1)
    while p != [F()] and len(p) >= len(r):
        shift = len(p)-len(r)
        z = p[-1]/r[-1]
        out[shift] += z
        p = add(p, [F()]*shift+scale(r, -z))
    return trim(out), trim(p)


def integral(p, a, b):
    return sum((z*(b**(j+1)-a**(j+1))/F(j+1)
                for j, z in enumerate(p)), F())


def solve(matrix, rhs):
    n = len(rhs)
    rows = [list(row)+[rhs[j]] for j, row in enumerate(matrix)]
    for j in range(n):
        pivot = next(k for k in range(j, n) if rows[k][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        z = rows[j][j]
        rows[j] = [v/z for v in rows[j]]
        for k in range(n):
            if k != j:
                z = rows[k][j]
                rows[k] = [a-z*b for a, b in zip(rows[k], rows[j])]
    return [rows[j][-1] for j in range(n)]


def rational_integral(num, den, poles):
    """Return exact rational constant and coefficients of positive log ratios."""
    quotient, remainder = divide(num, den)
    basis, labels = [], []
    for pole, order in poles:
        for degree in range(1, order+1):
            term, rest = divide(den, power([-pole, F(1)], degree))
            assert rest == [F()]
            basis.append(term)
            labels.append((pole, degree))
    n = len(den)-1
    assert len(basis) == n
    matrix = [[p[j] if j < len(p) else F() for p in basis] for j in range(n)]
    coeffs = solve(matrix, remainder+[F()]*(n-len(remainder)))
    reconstructed = [F()]
    for coef, pol in zip(coeffs, basis):
        reconstructed = add(reconstructed, scale(pol, coef))
    assert reconstructed == trim(remainder)  # exact polynomial identity
    constant, logs = integral(quotient, lo, hi), {}
    for coef, (pole, degree) in zip(coeffs, labels):
        if degree == 1:
            ratio = (hi-pole)/(lo-pole)
            assert ratio > 0
            logs[ratio] = logs.get(ratio, F())+coef
        else:
            constant += coef*((hi-pole)**(1-degree)-(lo-pole)**(1-degree))/F(1-degree)
    return constant, logs


def log_interval(ratio, terms=40):
    z = (ratio-1)/(ratio+1)
    assert abs(z) < 1
    center = 2*sum((z**(2*j+1)/F(2*j+1) for j in range(terms)), F())
    radius = 2*abs(z)**(2*terms+1)/(F(2*terms+1)*(1-z*z))
    return center-radius, center+radius


def biadd(p, r):
    out = dict(p)
    for mon, z in r.items():
        out[mon] = out.get(mon, F())+z
    return {mon: z for mon, z in out.items() if z}


def bisc(p, z):
    return {mon: value*z for mon, value in p.items() if value*z}


def bimul(p, r):
    out = {}
    for (i, j), a in p.items():
        for (k, l), b in r.items():
            key = (i+k, j+l)
            out[key] = out.get(key, F())+a*b
    return {mon: z for mon, z in out.items() if z}


def cell_integral(poly, lower_x, upper_x, zmax):
    """Integrate x then z; each x limit is an affine polynomial in z."""
    result = [F()]
    for (i, j), value in poly.items():
        upper, lower = power(upper_x, i+1), power(lower_x, i+1)
        term = scale(add(upper, scale(lower, -1)), value/F(i+1))
        result = add(result, [F()]*j+term)
    return integral(result, F(), zmax)


def fee_revenue(delta, alpha, length):
    x0, x1, zmax = lo-4*e, hi, 4*e
    lam = mul(alpha, add([c], scale(length, F(1, 4))))
    bundle = add([c, F(1)], delta)
    below_poly = add(add(scale(lam, -e), scale(bundle, -F(3, 2)*e*e)), [-e**3/2])
    below = 2*e*integral(below_poly, x0, x1)
    # Literal frozen fee-row identities, not a guessed continuous tariff.
    rows = trial.old.old.v3.base.DATA['bundle_rows']
    selected = {row['id']: row for row in rows if row['id'] in ('B13.1', 'B14.1')}
    assert selected['B13.1']['sum_interval'] == ['97/100', '39/40']
    assert selected['B14.1']['sum_interval'] == ['39/40', '49/50']
    assert all(row['normalized_rho_interval'] == ['0', '1/8'] for row in selected.values())
    f13, f14 = F(selected['B13.1']['fee']), F(selected['B14.1']['fee'])
    assert f13 == F(7, 2000) and f14 == F(7, 10000)
    assert F(97, 100) < x0+c < F(39, 40) < F(49, 50) < hi+c < 1-zmax
    frozen_d = trial.old.old.v3.base.D
    assert frozen_d == F(501, 1000)
    assert zmax/(x0-frozen_d) < F(1, 8)
    # No further row with a zero lower-rho endpoint meets sum > 49/50.
    assert not any(F(row['sum_interval'][1]) > F(49, 50)
                   and F(row['sum_interval'][0]) < hi+c+zmax
                   and F(row['normalized_rho_interval'][0]) == 0 for row in rows)
    cells = [([x0], [F(39, 40)-c, -F(1)], f13),
             ([F(39, 40)-c, -F(1)], [F(49, 50)-c, -F(1)], f14),
             ([F(49, 50)-c, -F(1)], [x1], F())]
    one, x, z = {(0, 0): F(1)}, {(1, 0): F(1)}, {(0, 1): F(1)}
    above, pieces = F(), []
    for lower, upper, fee in cells:
        ap = biadd(biadd(x, z), bisc(one, fee))
        bp = biadd(z, bisc(one, d+fee))
        cp = biadd(biadd(x, z), bisc(one, c+fee))
        overlap = biadd(z, bisc(one, q+fee))
        no_sale = biadd(bimul(ap, bp), bisc(bimul(overlap, overlap), -F(1, 2)))
        change = biadd(biadd(bisc(biadd(one, bisc(no_sale, -3)), e),
                             bisc(cp, -F(3, 2)*e*e)), bisc(one, -e**3/2))
        value = cell_integral(change, lower, upper, zmax)
        pieces.append(dict(fee=str(fee), value=str(value)))
        above += value
    return below+above, dict(below_c=str(below), above_c=str(above), above_pieces=pieces)


def calculate():
    delta = list(trial.old.DELTA.c)
    alpha = [-F(2), F(3)]
    length = add(delta, scale(alpha, F(1, 2)))
    A, T, U = F(2, 3), trial.old.T, trial.old.U
    assert delta == scale(mul([-T, F(1)], [-U, F(1)]), F(9, 16))
    constant = e*integral(mul(alpha, length), lo, hi)/4
    logs = {}
    r2, l2 = rational_integral(power(length, 2), scale(delta, 2), [(T, 1), (U, 1)])
    r3, l3 = rational_integral(power(length, 3), mul(alpha, power(delta, 2)),
                               [(A, 1), (T, 2), (U, 2)])
    constant -= e*e*r2+e**3*r3
    for source, factor in ((l2, -e*e), (l3, -e**3)):
        for ratio, coeff in source.items():
            logs[ratio] = logs.get(ratio, F())+factor*coeff
    constant *= trial.RHO
    logs = {ratio: coeff*trial.RHO for ratio, coeff in logs.items()}
    fee, detail = fee_revenue(delta, alpha, length)
    second_constant = constant
    constant += fee
    low, high = constant, constant
    for ratio, coefficient in logs.items():
        a, b = log_interval(ratio)
        low += coefficient*(a if coefficient >= 0 else b)
        high += coefficient*(b if coefficient >= 0 else a)
    independent_bound = F(trial.calculate()['total_gain_lower'])
    assert low > independent_bound > 0 and high-low < F(1, 10**65)
    # Outward decimal enclosures are rational integers, not float formatting.
    scale_decimal = 10**45
    floor = (low*scale_decimal).numerator//(low*scale_decimal).denominator
    ceil = -((-high*scale_decimal).numerator//(-high*scale_decimal).denominator)
    return dict(status='PRICE_JOINT_REVENUE_EXACT_PASS',
                scope='exact rational-plus-log joint increment, all affected full menus included',
                rational_constant=str(constant),
                logarithms=[dict(ratio=str(ratio), coefficient=str(coeff))
                            for ratio, coeff in sorted(logs.items())],
                increment_interval=[str(F(floor,scale_decimal)),str(F(ceil,scale_decimal))],
                second_bidder_rational_part=str(second_constant),
                first_bidder_exact_increment=str(fee), entry_fee_parts=detail,
                independent_gain_lower=str(independent_bound),
                logarithm_terms=40,
                evaluation_boundary='exact polynomial identities and rational log series; no floating solver')


if __name__ == '__main__':
    data = calculate()
    path = ROOT/'certificate'/'price_joint_revenue.json'
    if '--write' in sys.argv:
        path.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    else:
        assert json.loads(path.read_text(encoding='utf-8')) == data
    print(data['status'])
    print('increment_interval', data['increment_interval'])
    print('first_bidder_exact_increment', data['first_bidder_exact_increment'])
