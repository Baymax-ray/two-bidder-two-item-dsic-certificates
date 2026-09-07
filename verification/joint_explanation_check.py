"""Read-only author check: independent rational polygons and residue integration.

No source imports, numerical optimizer, writes, or finite-grid theorem claims.
Run with python -B -X utf8 joint_explanation_check.py (without -O).
"""
from fractions import Fraction as F
from math import factorial
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without optimized Python.')
e, c, q = F(9, 10000), F(137, 500), F(113, 500)
lo, hi, x0 = F(7, 10), F(71, 100), F(1741, 2500)


def trim(p):
    p = list(map(F, p))
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(p, r):
    return trim([(p[i] if i < len(p) else 0) +
                 (r[i] if i < len(r) else 0)
                 for i in range(max(len(p), len(r)))])


def sc(p, v):
    return trim([a*v for a in p])


def mul(p, r):
    result = [F()] * (len(p)+len(r)-1)
    for i, a in enumerate(p):
        for j, b in enumerate(r):
            result[i+j] += a*b
    return trim(result)


def val(p, t):
    return sum((a*t**i for i, a in enumerate(p)), F())


def derivative(p):
    return trim([i*p[i] for i in range(1, len(p))] or [0])


def integral(p, a, b):
    return sum((v*(b**(i+1)-a**(i+1))/F(i+1)
                for i, v in enumerate(p)), F())


def div(p, d):
    p, d = trim(p), trim(d)
    quotient = [F()] * max(1, len(p)-len(d)+1)
    while p != [0] and len(p) >= len(d):
        k, z = len(p)-len(d), p[-1]/d[-1]
        quotient[k] += z
        p = add(p, [F()]*k + sc(d, -z))
    return trim(quotient), trim(p)


def clip(poly, a, b, d):
    out = []
    for p, r in zip(poly, poly[1:]+poly[:1]):
        fp, fr = a*p[0]+b*p[1]+d, a*r[0]+b*r[1]+d
        if fp >= 0:
            out.append(p)
        if fp*fr < 0:
            u = fp/(fp-fr)
            out.append((p[0]+u*(r[0]-p[0]), p[1]+u*(r[1]-p[1])))
    return out


def area(poly):
    return sum((p[0]*r[1]-p[1]*r[0]
                for p, r in zip(poly, poly[1:]+poly[:1])), F())/2


def menu_revenue(menu):
    areas = []
    for ax, ay, price in menu:
        poly = [(F(0), F(0)), (F(1), F(0)), (F(1), F(1)), (F(0), F(1))]
        for bx, by, other in menu:
            poly = clip(poly, ax-bx, ay-by, other-price)
        areas.append(area(poly))
    assert sum(areas) == 1
    return sum((p*a for (_, _, p), a in zip(menu, areas)), F()), areas[0]


alpha = [-F(2), F(3)]
delta = add(add([q+3*q*q/4], [0, -3*q/2]), sc(mul(alpha, alpha), F(1, 16)))
length = add(delta, sc(alpha, F(1, 2)))
bundle = add([c, F(1)], delta)
lam = mul(alpha, add([c], sc(length, F(1, 4))))

# The continuum polygon derivation is in the companion Markdown. These exact
# full-menu integrations are independent examples, including the C > 1 row.
for t in (x0, lo, (lo+hi)/2, hi):
    al, de, L, C, la = (val(p, t) for p in (alpha, delta, length, bundle, lam))
    beta, B = al/(al+2*de), F(1, 2)+de
    menu = [(F(0), F(0), F(0)), (F(0), F(1), B),
            (F(1), F(0), t), (F(1), F(1), C),
            (F(1), beta, t+beta*c)]
    revenue, D = menu_revenue(menu)
    assert D == (1+la)/3
    for h in (F(), e/2, e):
        shifted = [menu[0]] + [(a, b, p+h) for a, b, p in menu[1:]]
        new_revenue, new_D = menu_revenue(shifted)
        assert new_D == D+C*h+h*h/2
        assert new_revenue-revenue == -la*h-F(3, 2)*C*h*h-h**3/2
        assert min(1-t-h, 1-B-h) > 0
    cut = menu[:-1]+[(F(1), beta, t+beta*c-e)]
    new_revenue, unused = menu_revenue(cut)
    gain = al*L*e/4-al*e*e/(4*beta*(1-beta))-e**3/(2*beta*(1-beta)**2)
    assert new_revenue-revenue == gain
    if t == lo:
        assert de == F(1727, 62500) and C == F(31301, 31250) > 1
        assert -la*e-F(3, 2)*C*e*e-e**3/2 == -F(1381203369, 50000000000000)
        print('row_delta', de, 'row_C', C, 'row_D', D)
        print('row_fee_change', -la*e-F(3, 2)*C*e*e-e**3/2)

# Independent J1 integration. Upper-strip polynomials are integrated using
# triangle monomial moments, rather than the source's moving-boundary method.
below = 2*e*integral(add(add(sc(lam, -e), sc(bundle, -F(3, 2)*e*e)), [-e**3/2]), x0, hi)


def polynomial_product(p, r):
    out = {}
    for (i, j), a in p.items():
        for (k, l), b in r.items():
            out[i+k, j+l] = out.get((i+k, j+l), F())+a*b
    return out


def polynomial_power(p, n):
    result = {(0, 0): F(1)}
    for unused in range(n):
        result = polynomial_product(result, p)
    return result


def triangle_moment(vertices, i, j):
    p, r, s = vertices
    det = (r[0]-p[0])*(s[1]-p[1])-(s[0]-p[0])*(r[1]-p[1])
    xp = {(0, 0): p[0], (1, 0): r[0]-p[0], (0, 1): s[0]-p[0]}
    yp = {(0, 0): p[1], (1, 0): r[1]-p[1], (0, 1): s[1]-p[1]}
    transformed = polynomial_product(polynomial_power(xp, i), polynomial_power(yp, j))
    return det*sum((v*F(factorial(k)*factorial(l), factorial(k+l+2))
                    for (k, l), v in transformed.items()), F())


def integrate_cell(poly, lower, upper):
    z1 = 4*e
    vertices = [(val(lower, 0), F()), (val(upper, 0), F()),
                (val(upper, z1), z1), (val(lower, z1), z1)]
    return sum((v*(triangle_moment(vertices[:3], i, j)+
                    triangle_moment([vertices[0], vertices[2], vertices[3]], i, j))
                for (i, j), v in poly.items()), F())


upper_parts = []
for lower, upper, f in (([x0], [F(701, 1000), -1], F(7, 2000)),
                         ([F(701, 1000), -1], [F(353, 500), -1], F(7, 10000)),
                         ([F(353, 500), -1], [hi], F())):
    # AB-(A+B-C)^2/2, expanded in the opponent coordinates x,z.
    D = {(1, 0): F(1, 2)+f, (1, 1): F(1),
         (0, 0): f*(F(1, 2)+f)-(q+f)**2/2,
         (0, 1): F(1, 2)+f-q, (0, 2): F(1, 2)}
    p = {mon: -3*e*v for mon, v in D.items()}
    p[0, 0] += e-F(3, 2)*(c+f)*e*e-e**3/2
    p[1, 0] -= F(3, 2)*e*e
    p[0, 1] -= F(3, 2)*e*e
    upper_parts.append(integrate_cell(p, lower, upper))
assert below == -F(92624010033429, 125000000000000000000000)
assert upper_parts == [F(3161434941, 25000000000000000000),
                       F(15610239, 62500000000000000),
                       F(838578339, 5000000000000000000)]
J1 = below+sum(upper_parts)
assert J1 == -F(24631898853429, 125000000000000000000000) < 0

# Integrate J2 by direct residues at the rational poles. In particular,
# double-pole coefficients use local values/derivatives, not a fitted system.
den = mul(alpha, mul(delta, delta))
num = add(add(sc(mul(mul(alpha, length), den), e/4),
                  sc(mul(mul(length, length), mul(alpha, delta)), -e*e/2)),
          sc(mul(mul(length, length), length), -e**3))
quotient, remainder = div(num, den)
constant, logs, reconstruct = integral(quotient, lo, hi), {}, mul(quotient, den)
for pole, multiplicity in ((F(2, 3), 1), (F(613, 750), 2), (F(839, 750), 2)):
    factor = [-pole, F(1)]
    cofactor, residual = div(den, factor)
    assert residual == [0]
    if multiplicity == 1:
        simple = val(num, pole)/val(cofactor, pole)
    else:
        local_den, residual = div(cofactor, factor)
        assert residual == [0]
        double = val(num, pole)/val(local_den, pole)
        simple = (val(derivative(num), pole)*val(local_den, pole)-
                  val(num, pole)*val(derivative(local_den), pole))/val(local_den, pole)**2
        constant += double*(1/(lo-pole)-1/(hi-pole))
        reconstruct = add(reconstruct, sc(local_den, double))
    ratio = (hi-pole)/(lo-pole)
    logs[ratio] = simple/5
    reconstruct = add(reconstruct, sc(cofactor, simple))
assert reconstruct == num
constant /= 5
assert constant == F(1110803432734877157, 1363542488000000000000000000)
assert logs == {F(13, 10): -F(9308601, 5000000000000000000),
                F(161, 176): F(6248637, 282500000000000),
                F(613, 628): -F(61575471, 282500000000000)}
J2_lower = J2_upper = constant
for ratio, coefficient in logs.items():
    z = (ratio-1)/(ratio+1)
    center = 2*sum((z**(2*k+1)/F(2*k+1) for k in range(40)), F())
    error = 2*abs(z)**81/(81*(1-z*z))
    J2_lower += coefficient*center-abs(coefficient)*error
    J2_upper += coefficient*center+abs(coefficient)*error
assert J2_lower > 0
assert J1+J2_lower > F(26902077489, 12500000000000000000) > 0
print('J1', J1)
print('J2_rational_part', constant)
print('J2_logs', {str(r): str(v) for r, v in logs.items()})
for label, lower, upper in (('J2', J2_lower, J2_upper), ('J', J2_lower+J1, J2_upper+J1)):
    scale = 10**45
    lower = F((lower*scale).__floor__(), scale)
    upper = F((upper*scale).__ceil__(), scale)
    print(label+'_outward_interval', str(lower), str(upper))
print('JOINT_EXPLANATION_INDEPENDENT_EXACT_PASS')
