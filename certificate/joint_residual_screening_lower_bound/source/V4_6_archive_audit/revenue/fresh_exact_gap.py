"""Fresh V4.6 arithmetic audit; standard library only, no project imports.

Reconstructs the algebraic additions by direct final-menu integration and
the joint increment by local pole expansions and complete entry-fee cells.
The historical V4.5 revenue interval is an explicitly retained dependency.
Default execution is read-only; --write writes only this audit's JSON.
"""
from fractions import Fraction as Q
from math import comb, isqrt
from pathlib import Path
import hashlib
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Exact audit requires assertions; do not use -O.')
HERE = Path(__file__).resolve().parent
AUCTION = HERE.parents[1]
V46 = AUCTION / 'V4_6'


class Poly:
    """Sparse rational polynomial in x and z, used for direct cell areas."""
    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.c = dict(value.c)
        elif isinstance(value, dict):
            self.c = {k: Q(v) for k, v in value.items() if v}
        else:
            self.c = {(0, 0): Q(value)} if value else {}

    def __add__(self, other):
        result = dict(self.c)
        for k, v in Poly(other).c.items():
            result[k] = result.get(k, Q()) + v
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.c.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        result = {}
        for (i, j), v in self.c.items():
            for (k, l), w in Poly(other).c.items():
                mon = i+k, j+l
                result[mon] = result.get(mon, Q()) + v*w
        return Poly(result)

    __rmul__ = __mul__

    def __truediv__(self, number):
        return self * (1/Q(number))

    def __pow__(self, exponent):
        result = Poly(1)
        for _ in range(exponent):
            result = result * self
        return result

    def __eq__(self, other):
        return self.c == Poly(other).c

    def substitute(self, axis, value):
        out = Poly()
        for powers, coefficient in self.c.items():
            remaining = list(powers)
            degree = remaining[axis]
            remaining[axis] = 0
            out += Poly({tuple(remaining): coefficient}) * value**degree
        return out

    def integrate(self, axis, lower, upper):
        primitive = {}
        for powers, coefficient in self.c.items():
            increased = list(powers)
            increased[axis] += 1
            primitive[tuple(increased)] = coefficient / increased[axis]
        primitive = Poly(primitive)
        return primitive.substitute(axis, Poly(upper)) - primitive.substitute(axis, Poly(lower))

    def scalar(self):
        assert not (set(self.c) - {(0, 0)})
        return self.c.get((0, 0), Q())


X, Z = Poly({(1, 0): 1}), Poly({(0, 1): 1})


def qmul(u, v, radicand):
    return u[0]*v[0]+radicand*u[1]*v[1], u[0]*v[1]+u[1]*v[0]


def quadratic_eval(polynomial, endpoint, radicand):
    """Independent explicit binomial powers, not the source Horner routine."""
    result = [Q(), Q()]
    for (degree, other), coefficient in polynomial.c.items():
        assert other == 0
        a, b = endpoint
        for j in range(degree+1):
            result[j % 2] += coefficient*comb(degree, j)*a**(degree-j)*b**j*radicand**(j//2)
    return tuple(result)


def field_integral(polynomial, lower, upper, radicand):
    primitive = Poly({(i+1, 0): c/Q(i+1) for (i, j), c in polynomial.c.items() if not j})
    assert all(j == 0 for i, j in polynomial.c)
    high = quadratic_eval(primitive, upper, radicand)
    low = quadratic_eval(primitive, lower, radicand)
    return high[0]-low[0], high[1]-low[1]


def menu_revenue(a, b, bundle):
    """Area of each deterministic winning cell times its literal payment."""
    a, b, bundle = Poly(a), Poly(b), Poly(bundle)
    singleton1 = (1-a)*(bundle-a)
    singleton2 = (1-b)*(bundle-b)
    bundle_area = (1+a-bundle)*(1+b-bundle)-(a+b-bundle)**2/2
    return a*singleton1+b*singleton2+bundle*bundle_area


def algebraic_increment():
    a, b, c, A, q = Q(159, 250), Q(91, 100), Q(137, 500), Q(2, 3), Q(113, 500)
    endpoint = (Q(4, 3), -Q(1, 3))
    old = menu_revenue(a, a, b).scalar()
    free_menu = quadratic_eval(menu_revenue(A, A, X), endpoint, 2)
    free_gain = qmul((Q(1, 12), Q(1, 9)), (free_menu[0]-old, free_menu[1]), 2)
    T, U, split = Q(613, 750), Q(839, 750), Q(1058587, 1362000)
    delta = Q(9, 16)*(T-X)*(U-X)
    delta_old = Q(1, 2)-c+Q(3, 4)*Q(227, 1000)**2-Q(3, 2)*Q(227, 1000)*X
    alpha = 3*X-2
    old_strip = ((delta-delta_old)**2+delta_old*alpha**2/8)*4*(X-a)
    new_strip = delta**2*4*(X-a)
    strip = old_strip.integrate(0, A, split).scalar()+new_strip.integrate(0, split, T).scalar()
    # One integral for the final G menu; a second for its free counterpart.
    g1 = field_integral((1-X)*(menu_revenue(a, a, X)-old), endpoint, (b, Q()), 2)
    free_new = field_integral((1-X)*menu_revenue(A, A, X), endpoint, (b, Q()), 2)
    g_area = field_integral(1-X, endpoint, (b, Q()), 2)
    free_old = qmul(g_area, free_menu, 2)
    g = (g1[0]+free_new[0]-free_old[0], g1[1]+free_new[1]-free_old[1])
    k = X-q
    C = Q(5, 6)+Q(3, 4)*k**2
    B = C-k
    # Integrate the final coupled menu directly against the initial Q menu.
    # This bypasses the source's bundle-change-plus-extra-change addition.
    q_poly = 2*(menu_revenue(A, Z-k, Z)-menu_revenue(A, B, C)).integrate(1, C, b)
    q_cost = field_integral(q_poly, (Q(1, 2), Q()), (q, Q(1, 15)), 23)
    result = (strip+free_gain[0]+g[0]+q_cost[0], free_gain[1]+g[1], q_cost[1])
    return result, dict(strip=str(strip), free=list(map(str, free_gain)), G=list(map(str, g)), final_Q=list(map(str, q_cost)))


def degree(poly):
    assert all(j == 0 for i, j in poly.c)
    return max((i for i, j in poly.c), default=-1)


def divide(numerator, denominator):
    quotient, remainder = Poly(), Poly(numerator)
    den_degree = degree(denominator)
    while degree(remainder) >= den_degree:
        n = degree(remainder)
        term = Poly({(n-den_degree, 0): remainder.c[n, 0]/denominator.c[den_degree, 0]})
        quotient += term
        remainder -= term*denominator
    assert numerator == quotient*denominator+remainder
    return quotient, remainder


def at(poly, value):
    return poly.substitute(0, Poly(value)).scalar()


def derivative(poly):
    return Poly({(i-1, 0): c*i for (i, j), c in poly.c.items() if i})


def rational_integral(numerator, denominator, poles, lo, hi):
    """Residues from local Taylor expansions; no linear system solver."""
    quotient, remainder = divide(numerator, denominator)
    rational = quotient.integrate(0, lo, hi).scalar()
    logs, identity, records = {}, Poly(), []
    for pole, order in poles:
        assert order in (1, 2) and not lo <= pole <= hi
        H, rest = divide(denominator, (X-pole)**order)
        assert rest == 0 and at(H, pole) != 0
        highest = at(remainder, pole)/at(H, pole)
        local = {order: highest}
        if order == 2:
            local[1] = (at(derivative(remainder), pole)*at(H, pole)-at(remainder, pole)*at(derivative(H), pole))/at(H, pole)**2
        for power, coefficient in local.items():
            basis, rest = divide(denominator, (X-pole)**power)
            assert rest == 0
            identity += coefficient*basis
            if power == 1:
                ratio = (hi-pole)/(lo-pole)
                assert ratio > 0
                logs[ratio] = logs.get(ratio, Q())+coefficient
            else:
                rational += coefficient*((hi-pole)**(1-power)-(lo-pole)**(1-power))/Q(1-power)
            records.append(dict(pole=str(pole), power=power, coefficient=str(coefficient)))
    assert identity == remainder
    return rational, logs, records


def joint_increment():
    e, lo, hi, rho, c, d = Q(9, 10000), Q(7, 10), Q(71, 100), Q(1, 5), Q(137, 500), Q(1, 2)
    T, U, A = Q(613, 750), Q(839, 750), Q(2, 3)
    delta, alpha = Q(9, 16)*(T-X)*(U-X), 3*X-2
    L = delta+alpha/2
    r2, l2, audit2 = rational_integral(L**2, 2*delta, [(T, 1), (U, 1)], lo, hi)
    r3, l3, audit3 = rational_integral(L**3, alpha*delta**2, [(A, 1), (T, 2), (U, 2)], lo, hi)
    second_rational = rho*(e*(alpha*L).integrate(0, lo, hi).scalar()/4-e**2*r2-e**3*r3)
    logs = {}
    for table, factor in ((l2, -rho*e**2), (l3, -rho*e**3)):
        for ratio, value in table.items():
            logs[ratio] = logs.get(ratio, Q())+factor*value
    x0, x1 = lo-4*e, hi
    C = X+c+delta
    y0 = c+L
    # Integrate the no-sale polygon vertically. beta*L = alpha/2.
    # Three slices: [0,c], [c,c+L], [c+L,d+delta].
    # The literal low singleton costs d+delta, not d.
    low_price = d+delta
    D0 = X*c+X*L-alpha*L/4+C*(low_price-y0)-(low_price**2-y0**2)/2
    assert 3*D0-1 == alpha*(c+L/4)
    fee_poly = e*(1-3*D0)-Q(3, 2)*C*e**2-e**3/2
    below = 2*e*fee_poly.integrate(0, x0, x1).scalar()
    edges = [Poly(x0), Q(39, 40)-c-Z, Q(49, 50)-c-Z, Poly(x1)]
    pieces = []
    for left, right, f in zip(edges, edges[1:], (Q(7, 2000), Q(7, 10000), Q())):
        ap, bp, cp = X+Z+f, d+Z+f, X+c+Z+f
        # Direct complete before/after menu payments, rather than fee formula.
        change = menu_revenue(ap+e, bp+e, cp+e)-menu_revenue(ap, bp, cp)
        area = ap*bp-(ap+bp-cp)**2/2
        assert change == e*(1-3*area)-Q(3, 2)*cp*e**2-e**3/2
        pieces.append(change.integrate(0, left, right).integrate(1, 0, 4*e).scalar())
    fee = below+sum(pieces, Q())
    return second_rational+fee, logs, dict(second_rational=str(second_rational), fee=str(fee), below=str(below), above_pieces=list(map(str, pieces)), partial_fractions_r2=audit2, partial_fractions_r3=audit3)


def log_interval(ratio, terms=80):
    """One-sided positive series plus explicit tail; invert ratios below 1."""
    if ratio < 1:
        lower, upper = log_interval(1/ratio, terms)
        return -upper, -lower
    z = (ratio-1)/(ratio+1)
    assert 0 <= z < Q(1, 2)
    partial = 2*sum((z**(2*j+1)/Q(2*j+1) for j in range(terms)), Q())
    tail = 2*z**(2*terms+1)/((2*terms+1)*(1-z*z))
    return partial, partial+tail


def radical_interval(coefficients, digits=70):
    lower = upper = coefficients[0]
    denominator = 10**digits
    for coefficient, radicand in zip(coefficients[1:], (2, 23)):
        root = isqrt(radicand*denominator**2)
        assert root**2 < radicand*denominator**2 < (root+1)**2
        a, b = Q(root, denominator), Q(root+1, denominator)
        lower += coefficient*(a if coefficient >= 0 else b)
        upper += coefficient*(b if coefficient >= 0 else a)
    return lower, upper


def decimal_interval(pair, digits=35):
    denominator = 10**digits
    lower, upper = pair
    a = (lower*denominator).numerator//(lower*denominator).denominator
    b = -((-upper*denominator).numerator//(-upper*denominator).denominator)
    def render(integer):
        sign = '-' if integer < 0 else ''
        number = str(abs(integer)).zfill(digits+1)
        return sign+number[:-digits]+'.'+number[-digits:]
    return [render(a), render(b)]


def main():
    source_paths = [AUCTION/'V4_5/certificate/independent_lottery.json', V46/'certificate/consolidated_bounds.json', V46/'certificate/price_joint_revenue.json', AUCTION/'V3/certificate/baseline_mechanism.json']
    baseline, consolidated, joint, tariff = [json.loads(path.read_text(encoding='utf-8')) for path in source_paths]
    # Complete literal tariff-row exclusion, including every nonzero rho low.
    # This checks a condition only implicit in the primary zero-low-row scan.
    e, x0, x1, c, d = Q(9, 10000), Q(1741, 2500), Q(71, 100), Q(137, 500), Q(501, 1000)
    rho_bound = 4*e/(x0-d)
    assert 0 < rho_bound < Q(1, 8)
    selected = {row['id']: row for row in tariff['bundle_rows'] if row['id'] in ('B13.1', 'B14.1')}
    assert selected['B13.1']['sum_interval'] == ['97/100', '39/40']
    assert selected['B14.1']['sum_interval'] == ['39/40', '49/50']
    assert Q(selected['B13.1']['fee']) == Q(7, 2000)
    assert Q(selected['B14.1']['fee']) == Q(7, 10000)
    for row in tariff['bundle_rows']:
        left, right = map(Q, row['sum_interval'])
        down, up = map(Q, row['normalized_rho_interval'])
        if right >= x0+c and left <= x1+c+4*e:
            if down == 0:
                assert row['id'] in selected and up == Q(1, 8)
            else:
                assert down >= Q(1, 8) > rho_bound
    coefficients, algebra_details = algebraic_increment()
    rational, logs, joint_details = joint_increment()
    assert list(map(str, coefficients)) == consolidated['algebraic_addition_coefficients']
    assert str(rational) == joint['rational_constant']
    assert {str(k): str(v) for k, v in logs.items()} == {term['ratio']: term['coefficient'] for term in joint['logarithms']}
    assert joint_details['fee'] == joint['first_bidder_exact_increment']
    assert joint_details['below'] == joint['entry_fee_parts']['below_c']
    assert joint_details['above_pieces'] == [row['value'] for row in joint['entry_fee_parts']['above_pieces']]
    joint_low = joint_high = rational
    for ratio, coefficient in logs.items():
        a, b = log_interval(ratio)
        joint_low += coefficient*(a if coefficient >= 0 else b)
        joint_high += coefficient*(b if coefficient >= 0 else a)
    assert Q(joint['increment_interval'][0]) <= joint_low <= joint_high <= Q(joint['increment_interval'][1])
    assert joint_low > Q(joint['independent_gain_lower']) > 0
    algebra_low, algebra_high = radical_interval(coefficients)
    revenue = (Q(baseline['revenue_interval'][0])+algebra_low+joint_low, Q(baseline['revenue_interval'][1])+algebra_high+joint_high)
    upper = Q(3715139591287203, 4194304000000000)
    assert revenue[1] < upper
    gap = upper-revenue[1], upper-revenue[0]
    # Readable strict certificate, independently rounded down from fresh R.
    simple_lower = Q(8758198541484224553460, 10**22)
    assert simple_lower <= revenue[0]
    margin = Q(1, 100)-(upper-simple_lower)
    assert margin.numerator > 0
    saved = list(map(Q, consolidated['revenue_rational_interval']))
    assert saved[0] <= revenue[0] <= revenue[1] <= saved[1]
    result = dict(status='FRESH_V46_REVENUE_RECONSTRUCTION_AND_STRICT_GAP_PASS',
        boundary='Fresh reconstruction of all V4.6 algebraic and logarithmic additions; V4.5 baseline interval retained. Mechanism all-real proof and inherited upper proof are separate dependencies.',
        source_sha256={str(path.relative_to(AUCTION)).replace('\\', '/'): hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths},
        algebraic_coefficients=list(map(str, coefficients)), algebraic_details=algebra_details,
        joint_rational=str(rational), joint_logs={str(k): str(v) for k, v in sorted(logs.items())}, joint_details=joint_details,
        tariff_source_audit=dict(all_bundle_rows=len(tariff['bundle_rows']), active_zero_rho_rows=sorted(selected), strict_rho_upper=str(rho_bound), other_intersecting_rows_excluded=True),
        log_terms=80, radical_digits=70, joint_decimal_enclosure=decimal_interval((joint_low, joint_high), 50),
        revenue_decimal_enclosure=decimal_interval(revenue), upper=str(upper), gap_decimal_enclosure=decimal_interval(gap),
        strict_certificate=dict(lower=str(simple_lower), lower_decimal='0.8758198541484224553460', upper_minus_lower=str(upper-simple_lower), one_hundredth_minus_gap_upper=str(margin), positive_integer_numerator=margin.numerator, denominator=margin.denominator, conclusion='0 < U-R <= U-L < 1/100'),
        methods=['direct final Q-menu integral in one step', 'binomial quadratic-field endpoint evaluation', 'no-sale polygon vertical slices', 'direct before/after three-price menu integrals', 'local pole Taylor coefficients and full polynomial identity', 'one-sided positive log series with reciprocal reduction', 'integer-square-root radical enclosures', 'exact rational strict threshold comparison'])
    destination = HERE/'fresh_exact_gap.json'
    if '--write' in sys.argv:
        destination.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    else:
        assert json.loads(destination.read_text(encoding='utf-8')) == result
    print(result['status'])
    print('revenue_enclosure', result['revenue_decimal_enclosure'])
    print('gap_enclosure', result['gap_decimal_enclosure'])
    print('positive_threshold_margin', margin)


if __name__ == '__main__':
    main()
