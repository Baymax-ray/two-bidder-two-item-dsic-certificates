"""Independent audit of the joined V3 candidate.

The new integral is reconstructed with rational polynomial arithmetic and a
binomial remainder bound, without importing either candidate calculate().
Candidate mechanism() is called only for exact implementation/tie checks.
Default replay reads its own certificate; --write creates that V3 certificate.
"""
if not __debug__:
    raise RuntimeError("Run without -O: exact certification uses assertions.")

import contextlib
from fractions import Fraction as F
import io
import json
from pathlib import Path
import runpy
import sys

HERE = Path(__file__).resolve().parent
V3 = HERE.parent
with contextlib.redirect_stdout(io.StringIO()):
    inherited = runpy.run_path(str(HERE / "baseline_replay.py"))
base_value, bundle_value = inherited["base"], inherited["bundle_gain"]
old_value = inherited["total"]
a, b, c, d = F(159, 250), F(91, 100), F(137, 500), F(501, 1000)
q = d - c
K = F(2, 3) + c * c
r0, r1 = b * b - K, F(4, 3) * c - F(2, 9)
switch = F(2, 3)
cutoff = (F(1, 2) - c + F(3, 4) * q * q) / (F(3, 2) * q)


def cp(x):
    return {} if x == 0 else {0: F(x)}


def add(*ps):
    out = {}
    for p in ps:
        for j, value in p.items():
            out[j] = out.get(j, F()) + value
    return {j: value for j, value in out.items() if value}


def scale(p, value):
    return {j: x * value for j, x in p.items() if x * value}


def mul(p, z):
    out = {}
    for i, x in p.items():
        for j, y in z.items():
            out[i + j] = out.get(i + j, F()) + x * y
    return {j: value for j, value in out.items() if value}


def power(p, n):
    out = cp(1)
    for _ in range(n):
        out = mul(out, p)
    return out


def integral(p, left, right):
    return sum(value * (right ** (j + 1) - left ** (j + 1)) / (j + 1)
               for j, value in p.items())


def menu_revenue(A, B, C):
    one = cp(1)
    first = mul(mul(A, add(one, scale(A, -1))), add(C, scale(A, -1)))
    second = mul(mul(B, add(one, scale(B, -1))), add(C, scale(B, -1)))
    rectangle = mul(add(one, scale(C, -1), B), add(one, scale(C, -1), A))
    triangle = scale(power(add(A, B, scale(C, -1)), 2), F(1, 2))
    return add(first, second, mul(C, add(rectangle, scale(triangle, -1))))


def interval_add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def interval_neg(x):
    return (-x[1], -x[0])


def interval_mul(x, y):
    values = [a * b for a in x for b in y]
    return (min(values), max(values))


def interval_eval(p, interval):
    out = (F(), F())
    for j in range(max(p, default=0), -1, -1):
        out = interval_add(interval_mul(out, interval), (p.get(j, F()),) * 2)
    return out


def interval_integral(p, left, right):
    primitive = {j + 1: value / (j + 1) for j, value in p.items()}
    return interval_add(interval_eval(primitive, right), interval_neg(interval_eval(primitive, left)))


def sqrt_bracket(value, bits=160):
    """Dyadic bisection, separate from the candidate's decimal isqrt bounds."""
    left, right = F(), F(1)
    assert 0 < value < 1
    for _ in range(bits):
        middle = (left + right) / 2
        if middle * middle <= value:
            left = middle
        else:
            right = middle
    assert left * left <= value <= right * right
    return (left, right)


def rounded(interval, digits=24):
    den = 10 ** digits
    left = interval[0].numerator * den // interval[0].denominator
    right = -((-interval[1].numerator * den) // interval[1].denominator)
    out = (F(left, den), F(right, den))
    assert out[0] <= interval[0] <= interval[1] <= out[1]
    return [str(x) for x in out]


# S integral: independently expand the two nonzero polynomial segments.
T = {1: F(1)}
k = add(T, cp(-q))
plateau_C = add(cp(F(5, 6)), scale(power(k, 2), F(3, 4)))
plateau = (cp(switch), add(plateau_C, scale(k, -1)), plateau_C)
base_S = (T, cp(d), add(T, cp(c)))
delta2 = add(cp(F(1, 2) - c + F(3, 4) * q * q), scale(T, -F(3, 2) * q))
affine = (T, add(cp(d), delta2), add(T, cp(c), delta2))
S1 = add(menu_revenue(*plateau), scale(menu_revenue(*base_S), -1))
S2 = add(menu_revenue(*affine), scale(menu_revenue(*base_S), -1))
new_S = 4 * c * (integral(S1, a, switch) + integral(S2, switch, cutoff))
assert new_S == F(json.loads((V3 / "certificate" / "stationary_s.json").read_text())["new_S_gain_over_base"])

# Real-domain, general cone, and revenue-chamber checks.
assert 0 < c < d < a < switch < cutoff < 1
assert 0 < r0 < r1 < (a - q) ** 2
assert K + r0 == b * b
assert K + r1 == (c + switch) ** 2
assert F(5, 6) + F(3, 4) * r1 == c + switch
assert F(1, 6) - c + F(3, 4) * r1 == 0
assert 2 * c * (a - q) < F(2, 3)
delta_at_switch = F(1, 2) - c + F(3, 4) * q * q - F(3, 2) * q * switch
assert delta_at_switch > 0 and d + delta_at_switch < 1
assert F(1, 2) - c + F(3, 4) * q * q - F(3, 2) * q * cutoff == 0

# Z square-root branch. Expand (K+k^2)^(3/2) about (93/100)^2.
# Uniform absolute tail uses decreasing binomial-coefficient magnitudes.
k0, k1 = sqrt_bracket(r0), sqrt_bracket(r1)
center_root = F(93, 100)
center = center_root * center_root
eta = F(1, 20)
zleft = (K + k0[0] ** 2 - center) / center
zright = (K + k1[1] ** 2 - center) / center
assert -eta <= zleft <= zright <= eta < 1
X = {1: F(1)}
zpoly = add(cp((K - center) / center), scale(power(X, 2), 1 / center))
order = 24
coefficient, series = F(1), cp(1)
for n in range(1, order + 1):
    coefficient *= (F(3, 2) - (n - 1)) / n
    series = add(series, scale(power(zpoly, n), coefficient))
next_coefficient = coefficient * (F(3, 2) - order) / (order + 1)
uniform_error = (center_root ** 3 * abs(next_coefficient)
                 * eta ** (order + 1) / (1 - eta))
root_cubed_polynomial = scale(series, center_root ** 3)
base_subtraction = add(scale(add(power(X, 2), cp(K)), -F(3, 2) * b), cp(b ** 3 / 2))
width = add(cp(b - q), scale(X, -1))
root_integrand = scale(mul(width, add(root_cubed_polynomial, base_subtraction)), 4)
Zroot = interval_integral(root_integrand, k0, k1)
weight_integral_upper = 4 * integral(width, k0[0], k1[1])
assert weight_integral_upper > 0 and b - q > k1[1]
error = uniform_error * weight_integral_upper
Zroot = (Zroot[0] - error, Zroot[1] + error)

# Remaining Z plateau, using width b-t and its exact polynomial primitive.
base_Z = (cp(a), add(cp(b), scale(k, -1)), cp(b))
Zp = scale(mul(add(cp(b), scale(T, -1)),
               add(menu_revenue(*plateau), scale(menu_revenue(*base_Z), -1))), 4)
t1 = (q + k1[0], q + k1[1])
Zplateau = interval_integral(Zp, t1, (a, a))
new_Z = interval_add(Zroot, Zplateau)
constant = base_value + bundle_value + new_S
total = interval_add((constant, constant), new_Z)
gain = (total[0] - old_value, total[1] - old_value)
assert gain[0] > 0

# Independent retained-part accounting equals subtraction from the old L.
removed = inherited["common_z"] + inherited["common_s"] + inherited["item_gain"]
assert old_value - removed == base_value + bundle_value
published = json.loads((V3 / "certificate" / "joined_threshold.json").read_text())
published_interval = tuple(map(F, published["revenue_interval"]))
assert published_interval[0] <= total[0] <= total[1] <= published_interval[1]

# Exact rational implementation/tie checks. No candidate calculate() is called.
candidate = runpy.run_path(str(HERE / "joined_threshold.py"))
mechanism, candidate_menu = candidate["mechanism"], candidate["menu"]
base_mechanism = inherited["mechanism"]
checks = []

def record(profile, expected_first_mask=None):
    result = mechanism(profile)
    original = base_mechanism(profile)
    assert result["masks"][0] & result["masks"][1] == 0
    assert result["utilities"][0] >= 0 and result["utilities"][1] >= 0
    for i in range(2):
        own = tuple(map(F, profile[2 * i:2 * i + 2]))
        prices = result["menus"][i]
        utilities = [sum((own[j] for j in range(2) if mask & (1 << j)), F())
                     - prices[mask] for mask in range(4)]
        selected = result["masks"][i]
        assert result["utilities"][i] == utilities[selected] == max(utilities)
        assert result["payments"][i] == prices[selected]
        assert selected & ~original["base_masks"][i] == 0
        if max(utilities) == 0:
            assert selected == 0 and result["payments"][i] == 0
    if expected_first_mask is not None:
        assert result["masks"][0] == expected_first_mask
    checks.append({"profile": [str(F(x)) for x in profile],
                   "masks": list(result["masks"]), "branches": list(result["branches"])})
    return result

opponent = (F(11, 20), F(1, 10))
assert candidate_menu(opponent)[1] == "square_root"
high_tie = record((F(3, 4), c) + opponent, 1)
high_prices = high_tie["menus"][0]
assert F(3, 4) - high_prices[1] == F(3, 4) + c - high_prices[3] > 0
low_tie = record((opponent[0] - q, F(3, 4)) + opponent, 3)
low_prices = low_tie["menus"][0]
assert F(3, 4) - low_prices[2] == opponent[0] - q + F(3, 4) - low_prices[3] > 0

# Rational parametrization makes the nominal square root exactly rational.
low_price = F(3, 5)
height = (low_price + K / low_price) / 2
kk = (K / low_price - low_price) / 2
assert height * height == K + kk * kk and r0 < kk * kk < r1
opponent_rational_root = (q + kk, F(1, 10))
zero_tie = record((height - c, c / 2) + opponent_rational_root, 0)
assert height - c - zero_tie["menus"][0][1] == 0

for high in (d, F(31, 50), a, F(13, 20), switch, F(7, 10), cutoff, F(9, 10)):
    record((F(3, 4), F(2, 5), high, F(1, 10)))
    record((0, 0, high, c), 0)
record((1, 1, 1, 1))

# A strictly interior retained bundle-pivot opponent report.
opponent_retained = (F(49, 80), F(3, 10))
assert candidate_menu(opponent_retained) is None
profile = (F(7, 10), F(7, 10)) + opponent_retained
modified, original = mechanism(profile), base_mechanism(profile)
assert modified["masks"][0] == original["masks"][0]
assert modified["payments"][0] == original["payments"][0]

result = {
    "scope": "Independent feasible-mechanism and revenue audit; no unrestricted optimality claim",
    "method": "rational polynomial integration with binomial tail; no log-series import and no candidate calculate() call",
    "base_value": str(base_value), "retained_bundle_gain": str(bundle_value),
    "removed_baseline_gain": str(removed), "new_S_gain": str(new_S),
    "new_Z_root_interval": rounded(Zroot), "new_Z_plateau_interval": rounded(Zplateau),
    "revenue_interval": rounded(total), "gain_interval": rounded(gain),
    "candidate_published_interval": published["revenue_interval"],
    "sqrt_bracket_bits": 160, "binomial_order": order,
    "binomial_center_root": str(center_root), "uniform_relative_argument_bound": str(eta),
    "uniform_root_cube_error_bound": str(uniform_error),
    "t0_interval": rounded((q + k0[0], q + k0[1])), "t1_interval": rounded(t1),
    "general_cone": "alpha,beta,gamma>=0 and gamma>=max(alpha,beta), with base subadditivity and zero-price opt-out",
    "archived_delta_guard_required": False,
    "rational_profile_checks": checks
}
target = V3 / "certificate" / "joined_independent.json"
if "--write" in sys.argv:
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
else:
    assert json.loads(target.read_text(encoding="utf-8")) == result
print("JOINED_INDEPENDENT_POLYNOMIAL_BINOMIAL_ENCLOSURE_PASS")
print("JOINED_INDEPENDENT_RETAINED_BASE_AND_BUNDLE_ACCOUNTING_PASS")
print("JOINED_EXACT_RATIONAL_TIE_AND_CAPACITY_CHECKS_PASS", len(checks))
print("revenue_interval", result["revenue_interval"])
print("gain_interval", result["gain_interval"])
print("The analytic cone proof covers all real reports; finite checks audit only the implementation.")
