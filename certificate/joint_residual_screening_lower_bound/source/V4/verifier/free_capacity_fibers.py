"""Exact V4 full-capacity inner fibers and a pointwise feasible escape from V3.

The all-real proof is in research_log/free_capacity_fibers.md. Rational-report
evaluation uses V3's exact quadratic comparisons, not floating decisions.
Run --write once to write the certificate; normal execution replays it.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / "V3" / "verifier"))
import joined_threshold as v3

A, B, D = F(159, 250), F(91, 100), F(501, 1000)
SJA_SINGLE = v3.Quad(F(2, 3))
SJA_BUNDLE = v3.Quad(F(4, 3), -F(1, 3), 2)
SJA_PRICES = (v3.Quad(), SJA_SINGLE, SJA_SINGLE, SJA_BUNDLE)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def in_free_fiber(w):
    return all(0 <= z < D for z in w) and sum(w) < B


def mechanism(profile):
    """Keep bidder 1 V3; optimize bidder 2 completely on the free fibers."""
    profile = tuple(map(F, profile))
    result = v3.mechanism(profile)
    if not in_free_fiber(profile[:2]):
        return result
    require(result["masks"][0] == 0, "bidder 1 must be empty on every free fiber")
    z = profile[2:]
    utilities = [v3.base.value(z, mask) - SJA_PRICES[mask] for mask in range(4)]
    maximum = max(utilities)
    selected = min(mask for mask, utility in enumerate(utilities) if utility == maximum)
    changed = dict(result)
    changed["masks"] = (0, selected)
    changed["payments"] = (result["payments"][0], SJA_PRICES[selected])
    changed["utilities"] = (result["utilities"][0], maximum)
    changed["menus"] = (result["menus"][0], SJA_PRICES)
    changed["branches"] = (result["branches"][0], "full_capacity_SJA")
    require(maximum >= 0, "IR")
    require(changed["masks"][0] & changed["masks"][1] == 0, "item capacity")
    return changed


# Independent arithmetic in Q(sqrt(2)); pairs store rational coefficients.
def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def neg(x):
    return -x[0], -x[1]


def sub(x, y):
    return add(x, neg(y))


def mul(x, y):
    return x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def scale(c, x):
    return c * x[0], c * x[1]


def rational(c):
    return F(c), F()


def revenue(a, b):
    one = rational(1)
    single_area = mul(sub(one, a), sub(b, a))
    rect_side = add(sub(one, b), a)
    corner_side = sub(scale(2, a), b)
    bundle_area = sub(mul(rect_side, rect_side), scale(F(1, 2), mul(corner_side, corner_side)))
    return add(scale(2, mul(a, single_area)), mul(b, bundle_area))


def interval(pair, digits=40):
    denominator = 10 ** digits
    low_num = isqrt(2 * denominator * denominator)
    require(low_num * low_num < 2 * denominator * denominator < (low_num + 1) ** 2,
            "strict rational sqrt(2) enclosure")
    low, high = F(low_num, denominator), F(low_num + 1, denominator)
    a, b = pair
    return (a + b * low, a + b * high) if b >= 0 else (a + b * high, a + b * low)


def encode_pair(pair):
    return {"rational": str(pair[0]), "sqrt2_coefficient": str(pair[1])}


def certificate():
    require(v3.a == A and v3.b == B and v3.d == D, "frozen V3 constants")
    require(0 < 2 * D - B < D < A < 1, "free-fiber polygon topology")
    # Every old common fee row starts strictly above D; bundle rows require
    # sum >= B. V3's new chamber also starts at high >= D.
    require(all(F(row["high_interval"][0]) > D for row in v3.base.DATA["common_rows"]),
            "old common rows absent on E")
    # Global base singleton lower bound: for t <= D the min is A; for
    # t >= D use H >= t-A to obtain S-A = D. Bundle price >= B.
    require(v3.base.S - A == D and A > D, "global base-price lower bound")
    area = D * D - (2 * D - B) ** 2 / 2
    require(area == F(246769, 1000000), "exact polygon area")
    old = revenue(rational(A), rational(B))
    single = revenue(rational(F(2, 3)), (F(4, 3), -F(1, 3)))
    require(old == (F(136719583, 250000000), F()), "old menu exact revenue")
    require(single == (F(4, 9), F(2, 27)), "SJA exact revenue")
    gain = scale(area, sub(single, old))
    expected_gain = (-F(56874392995943, 2250000000000000), F(246769, 13500000))
    require(gain == expected_gain, "exact integrated gain")
    gain_interval = interval(gain)
    require(gain_interval[0] > F(573163599821354970, 10 ** 21), "strict positive revenue gain")

    witness = (F(1, 10), F(1, 10), F(9, 20), F(9, 20))
    before = v3.mechanism(witness)
    after = mechanism(witness)
    base = v3.base.mechanism(witness)
    require(base["base_masks"] == (0, 0), "shared base strictly empty at witness")
    require(before["masks"] == (0, 0) and after["masks"] == (0, 3), "escape from containment")
    require(SJA_BUNDLE < F(9, 10) < B and F(9, 20) < A, "strict witness inequalities")
    # A rational positive-volume box preserves the strict witness allocation:
    # bidder 1 coordinates in [0.09,0.11], bidder 2 in [0.44,0.45].
    require(2 * F(11, 100) < B and F(11, 100) < D, "whole box in E")
    require(SJA_BUNDLE < F(22, 25) and 2 * F(9, 20) < B, "bundle entry on whole box")
    require(F(9, 20) < A and F(11, 100) + F(9, 20) < v3.base.S,
            "all nonempty shared-base outcomes strictly lose on whole box")

    # Exact smoke checks include zero types, an axis, and rational boundaries
    # of E. The universal DSIC/feasibility proof is analytic, not this sample.
    examples = [witness, (0, 0, 0, 0), (0, 0, F(2, 3), 0),
                (D, 0, F(9, 20), F(9, 20)),
                (F(91, 200), F(91, 200), 1, 1),
                (0, F(1, 10), 1, 0), (F(1, 10), F(1, 10), 1, 1)]
    for profile in examples:
        old_result, new_result = v3.mechanism(profile), mechanism(profile)
        require(new_result["masks"][0] == old_result["masks"][0], "bidder 1 unchanged")
        require(new_result["payments"][0] == old_result["payments"][0], "bidder 1 payment unchanged")
        if not in_free_fiber(profile[:2]):
            require(new_result == old_result, "outside E unchanged, including E boundary")

    return {
        "scope": "exact optimum of the full-capacity inner fibers only; unrestricted auction optimum unresolved",
        "free_fiber": "0<=w1<501/1000, 0<=w2<501/1000, w1+w2<91/100",
        "free_fiber_area": str(area),
        "old_conditional_revenue": encode_pair(old),
        "optimal_conditional_revenue": encode_pair(single),
        "strict_revenue_gain": encode_pair(gain),
        "gain_rational_interval": list(map(str, gain_interval)),
        "witness_profile": list(map(str, witness)),
        "witness_base_masks": list(base["base_masks"]),
        "witness_V3_masks": list(before["masks"]),
        "witness_V4_masks": list(after["masks"]),
        "witness_new_bundle_price": encode_pair((F(4, 3), -F(1, 3))),
        "positive_volume_escape_box": ["[9/100,11/100]^2", "[11/25,9/20]^2"],
        "pointwise_smoke_checks": len(examples),
        "theorem_dependency": "Giannakopoulos--Koutsoupias arXiv:1404.2329v4 Theorem 2, randomized single-buyer class",
    }


if __name__ == "__main__":
    result = certificate()
    destination = ROOT / "certificate" / "free_capacity_fibers.json"
    if "--write" in sys.argv:
        destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    else:
        require(json.loads(destination.read_text(encoding="utf-8")) == result,
                "saved exact certificate replay")
    print("PASS free_capacity_fibers: exact inner optimum, strict gain, pointwise splice and containment escape")
