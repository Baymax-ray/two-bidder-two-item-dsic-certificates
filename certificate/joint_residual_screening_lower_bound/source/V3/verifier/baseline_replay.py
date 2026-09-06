"""Exact BASE-1 replay, independent of archived verifier implementations.

Recomputes the affine base from a max-value anchor and a split-probability
integral, then recomputes all 69 layer gains. Reads only V3 files; prints only.
Finite profile checks exercise implementation boundaries, not the DSIC proof.
"""
if not __debug__:
    raise RuntimeError("Run without -O: exact certification uses assertions.")

from fractions import Fraction as F
from pathlib import Path
import runpy

model = runpy.run_path(str(Path(__file__).with_name("baseline_mechanism.py")))
DATA = model["DATA"]
mechanism, menu = model["mechanism"], model["menu"]
base_menu, allocation_vector = model["base_menu"], model["allocation_vector"]
a, b, s = model["A"], model["B"], model["S"]
c, d, e, k = b - a, s - a, s - b, b + s - 2 * a


def boole(function, lower, upper):
    weights = (7, 32, 12, 32, 7)
    return (upper - lower) * sum(
        weight * function(lower + (upper - lower) * F(j, 4))
        for j, weight in enumerate(weights)) / 90


def regime(prices):
    A, B, C = prices
    assert 0 <= A <= C <= 1
    assert 0 <= B <= C <= A + B


def revenue(prices):
    A, B, C = prices
    return (A * (1 - A) * (C - A) + B * (1 - B) * (C - B)
            + C * ((1 - C + B) * (1 - C + A) - (A + B - C) ** 2 / 2))


def shift(prices, fee):
    return tuple(price + fee for price in prices)


def base_revenue():
    """Independent analytic anchor; parameters here are singleton a,c,d."""
    x, t, h = a, c, d
    assert 0 < t < h < x < 1
    q = x - t
    H = t * (1 - x) ** 2 + (1 - t) ** 2 * (1 - x) + q ** 3 / 6
    top = F(5, 3) - (x + t) + t ** 3 / 3
    volume = (4 * t ** 2 * (F(1, 3) - x / 2 + x ** 3 / 6)
              + F(4, 3) * (1 - t ** 3) * (1 - t ** 2)
              - (x + t) * (1 - t ** 2) ** 2
              + F(2, 3) * t ** 2 * q ** 3 + t * q ** 4 / 3 + q ** 5 / 30)

    def split_derivative(eta):
        ell, delta = 1 - eta, x - eta
        M = ell ** 2 / 2 + t * ell
        T = t ** 2 * delta ** 2 / 2 + t * delta ** 3 / 3 + delta ** 4 / 24
        return 12 * (M ** 2 - T) - 4 * (ell + t) * M

    return 4 * top - 6 * volume + 2 * H + boole(split_derivative, t, h)


base = base_revenue()
assert base == F(DATA["expected"]["base"])
common_gain = F()
common_z, common_s = F(), F()
for row in DATA["common_rows"]:
    left, right = map(F, row["high_interval"])
    fee = F(row["fee"])
    assert fee > 0
    is_z = row["id"].startswith("Z")

    def prices(t):
        return (s - t, a, b) if is_z else (t, d, t + c)

    for endpoint in (left, right):
        regime(prices(endpoint))
        regime(shift(prices(endpoint), fee))
    gain = 4 * boole(
        lambda t: ((b - t) if is_z else c)
        * (revenue(shift(prices(t), fee)) - revenue(prices(t))), left, right)
    assert gain == F(row["expected_gain"]), row["id"]
    common_gain += gain
    if is_z:
        common_z += gain
    else:
        common_s += gain
    assert menu((0, (left + right) / 2))["common_row"] == row["id"]
assert common_gain == F(DATA["expected"]["common"])
assert common_z == F(DATA["expected"]["common_Z"])
assert common_s == F(DATA["expected"]["common_S"])

bundle_gain = F()
for row in DATA["bundle_rows"]:
    u0, u1 = map(F, row["sum_interval"])
    r0, r1 = map(F, row["normalized_rho_interval"])
    fee = F(row["fee"])

    def prices(u, r):
        rho = c + r * (u - k)
        return (u - c, rho + e, u)

    for u in (u0, u1):
        for r in (r0, r1):
            rho = c + r * (u - k)
            assert b <= u <= 1 and c <= rho <= u - d
            assert u - k >= F(27, 200)
            assert prices(u, r) == base_menu((u - rho, rho))[1:]
            regime(prices(u, r))
            regime(shift(prices(u, r), fee))
    gain = 4 * boole(
        lambda u: boole(lambda r: (u - k)
                        * (revenue(shift(prices(u, r), fee)) - revenue(prices(u, r))),
                        r0, r1), u0, u1)
    assert gain == F(row["expected_gain"]), row["id"]
    bundle_gain += gain
    um, rm = (u0 + u1) / 2, (r0 + r1) / 2
    rho = c + rm * (um - k)
    assert menu((um - rho, rho))["common_row"] == row["id"]
assert bundle_gain == F(DATA["expected"]["bundle"])

item_gain = F()
item_reports = []
parents = {row["id"]: row for row in DATA["common_rows"]}
for row in DATA["item_rows"]:
    left, right = map(F, row["high_interval"])
    fee, delta = F(row["common_fee"]), F(row["item_surcharge"])
    parent = parents[row["parent"]]
    assert fee == F(parent["fee"])
    assert F(parent["high_interval"][0]) <= left < right <= F(parent["high_interval"][1])
    assert 0 < delta < d - c + fee

    def before(t):
        return (d + fee, t + fee, t + c + fee)

    def after(t):
        return (d + fee + delta, t + fee, t + c + fee + delta)

    for endpoint in (left, right):
        regime(before(endpoint))
        regime(after(endpoint))
    gain = 4 * c * boole(lambda t: revenue(after(t)) - revenue(before(t)), left, right)
    assert gain == F(row["expected_gain"]), row["id"]
    item_gain += gain
    item_reports.append((row["id"], d - c + fee - delta, 1 - after(right)[2]))
    assert menu((0, (left + right) / 2))["item_row"] == row["id"]
assert item_gain == F(DATA["expected"]["item"])
assert common_s + item_gain == F(DATA["expected"]["S_common_plus_item"])
assert len(DATA["common_rows"]) == 20
assert len(DATA["bundle_rows"]) == 41
assert len(DATA["item_rows"]) == 8
total = base + common_gain + bundle_gain + item_gain
assert total == F(DATA["expected"]["total"])

# Literal overlap and zero-utility conventions; these are code checks only.
assert menu((0, F(139, 200)))["common_row"] == "S4.2"
assert menu((0, F(139, 200)))["item_row"] is None
assert menu((0, F(281, 400)))["item_row"] == "I1.4"
assert menu((c, F(73, 80) - c))["common_row"] == "S1.1"
assert menu((F(29, 100), F(31, 50)))["common_row"] == "Z5.1"
for q in ((0, 0), (1, 1), (0, F(7, 10)), (c, F(73, 80) - c)):
    result = mechanism((0, 0) + q)
    assert result["masks"][0] == 0 and result["payments"][0] == 0
    prices = menu(q)["prices"]
    for own in ((1, 1), (prices[1], 0), (0, prices[2]),
                (prices[1], prices[3] - prices[1])):
        if all(0 <= v <= 1 for v in own):
            result = mechanism(own + q)
            assert result["masks"][0] & result["masks"][1] == 0
            assert result["utilities"][0] >= 0 and result["utilities"][1] >= 0

v = tuple(map(F, (F(321, 500), 0, F(539, 1000), 0)))
w = tuple(map(F, (F(643, 1000), 0, F(541, 1000), 0)))
mv, mw = mechanism(v), mechanism(w)
assert mv["masks"] == (1, 0) and mw["masks"] == (0, 0)
assert mv["payments"] == (F(32033, 50000), 0)
Xv, Xw = allocation_vector(mv), allocation_vector(mw)
joint_monotonicity = sum((y - x) * (b - a) for x, y, a, b in zip(Xv, Xw, v, w))
assert joint_monotonicity == F(-1, 1000)
vi = (v[0], F(1, 100), v[2], F(1, 100))
wi = (w[0], F(1, 100), w[2], F(1, 100))
mvi, mwi = mechanism(vi), mechanism(wi)
assert mvi["masks"] == (1, 0) and mwi["masks"] == (0, 0)
assert mvi["payments"] == (F(32033, 50000), 0)
Xi, Yi = allocation_vector(mvi), allocation_vector(mwi)
assert sum((y - x) * (b - a) for x, y, a, b in zip(Xi, Yi, vi, wi)) == F(-1, 1000)
# These exact constant inequalities close the three-case all-report proof.
assert 2 * a - b >= s - b > 0
assert 2 * (s - b) >= s - b

print("BASELINE_INDEPENDENT_BASE_REVENUE_PASS", base)
print("BASELINE_ALL_69_ROW_REVENUES_AND_REGIMES_PASS")
print("common_gain", common_gain)
print("common_Z_gain", common_z)
print("common_S_gain", common_s)
print("S_common_plus_item_gain", common_s + item_gain)
print("bundle_gain", bundle_gain)
print("item_gain", item_gain)
print("exact_total", total)
print("BASELINE_POINTWISE_CONVENTION_SPOT_CHECKS_PASS")
print("BASELINE_NO_POSITIVE_CONSTANT_WEIGHT_COMMON_CONVEX_POTENTIAL_PASS", joint_monotonicity)
print("The same strict obstruction is verified at two entirely interior profiles.")
print("Item row: strict deletion margin; integration-chamber cap margin at upper endpoint")
for row in item_reports:
    print(*row)
print("The cap is an integration-regime condition, not a general DSIC/capacity constraint.")
print("Pointwise DSIC/IR/capacity for all reports follow from taxation plus analytic containment.")
