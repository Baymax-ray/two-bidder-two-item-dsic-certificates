"""Independent V3.1 revenue replay using dictionary polynomials and a binomial tail.

Does not call constrained_candidate.revenue_enclosure or the primary logarithm
routine. Frozen V3 replay is explicitly run without --write, even when this
new verifier is writing its own certificate.
"""
if not __debug__:
    raise RuntimeError("Run without -O")

import contextlib
from fractions import Fraction as F
import io
import json
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]


def require(test, message):
    if not test:
        raise RuntimeError(message)


def certificate():
    old_script = ROOT.parent / "V3" / "verifier" / "joined_independent.py"
    arguments = sys.argv
    try:
        sys.argv = [str(old_script)]  # Protect every frozen V3 file from --write.
        with contextlib.redirect_stdout(io.StringIO()):
            old = runpy.run_path(str(old_script))
    finally:
        sys.argv = arguments
    cp, add, scale = old["cp"], old["add"], old["scale"]
    mul, power, menu_revenue = old["mul"], old["power"], old["menu_revenue"]
    interval_add, interval_neg = old["interval_add"], old["interval_neg"]
    interval_mul, interval_integral = old["interval_mul"], old["interval_integral"]
    a, b, d, q = F(159, 250), F(91, 100), F(501, 1000), F(227, 1000)
    T = {1: F(1)}
    k = add(T, cp(-q))
    C = add(cp(F(5, 6)), scale(power(k, 2), F(3, 4)))
    candidate_prices = (cp(F(2, 3)), add(C, scale(k, -1)), C)
    old_base_prices = (cp(a), add(cp(b), scale(k, -1)), cp(b))
    difference = add(menu_revenue(*candidate_prices), scale(menu_revenue(*old_base_prices), -1))
    integrand = scale(mul(add(cp(b), scale(T, -1)), difference), 2)
    t1 = (q + old["k1"][0], q + old["k1"][1])
    polynomial_gain = interval_integral(integrand, (d, d), t1)
    old_root_half = interval_mul((F(1, 2), F(1, 2)), old["Zroot"])
    gain = interval_add(polynomial_gain, interval_neg(old_root_half))
    require(gain[0] > F(2153805511902915333, 10**23), "strict independently integrated improvement")

    # Independently recover V4's exact free-fiber increment with a dyadic
    # sqrt(1/2) bracket, without reading its published total as an input.
    free_area = d*d - (2*d-b)**2/2
    old_single = menu_revenue(cp(a), cp(a), cp(b))
    require(old_single == {0: F(136719583, 250000000)}, "old single-buyer integral")
    root_half = old["sqrt_bracket"](F(1, 2))
    sqrt_two = (2*root_half[0], 2*root_half[1])
    delta_rational = free_area * (F(4, 9) - old_single[0])
    delta_radical = free_area * F(2, 27)
    delta = interval_add((delta_rational, delta_rational),
                         interval_mul((delta_radical, delta_radical), sqrt_two))
    free_revenue = interval_add(old["total"], delta)
    total = interval_add(free_revenue, gain)

    # The solved opponent sets are disjoint up to omitted boundary lines.
    constrained_area = 2*(b*(F(2, 3)-d) - (F(4, 9)-d*d)/2)
    solved_area = free_area + constrained_area
    require(solved_area == F(63871, 180000), "exact solved opponent area")
    require(solved_area == F(4, 9)-(F(4, 3)-b)**2/2, "closed Q area by direct polygon formula")
    # The exact bidder-2 screening value on the complete solved set Q.
    constrained_value_integrand = scale(mul(add(cp(b), scale(T, -1)),
                                            menu_revenue(*candidate_prices)), 2)
    constrained_value = old["integral"](constrained_value_integrand, d, F(2, 3))
    solved_value_rational = free_area*F(4, 9) + constrained_value
    solved_value_radical = free_area*F(2, 27)
    require(solved_value_rational == F(3270005919999123155413, 19440000000000000000000),
            "exact rational part of bidder 2 solved-region value")
    require(solved_value_radical == F(246769, 13500000), "exact radical part of solved-region value")
    published = json.loads((ROOT / "certificate" / "constrained_candidate.json").read_text(encoding="utf-8"))
    for key, calculated in [("gain_rational_interval", gain), ("revenue_rational_interval", total)]:
        enclosure = tuple(map(F, published[key]))
        require(enclosure[0] <= calculated[0] <= calculated[1] <= enclosure[1],
                "independent enclosure contained in primary published enclosure")
    coefficients = [str(integrand.get(j, F())) for j in range(max(integrand)+1)]
    require(coefficients == published["integrand_coefficients"], "independent polynomial coefficients")
    require(str(solved_area) == published["solved_opponent_region_area"], "published solved area")
    require(published["exact_bidder2_value_on_solved_region"] ==
            {"rational": str(solved_value_rational), "sqrt2_coefficient": str(solved_value_radical)},
            "published fully optimized regional inner value")
    return {
        "scope": "independent exact revenue and area audit, no outer optimality claim",
        "method": "dictionary rational polynomials, dyadic square-root brackets, inherited independent binomial remainder; no primary logarithm evaluation",
        "old_root_gain_subtraction": "one half of V3 Zroot: one changed bidder, both item orientations",
        "integrand_coefficients": coefficients,
        "polynomial_part_interval": old["rounded"](polynomial_gain),
        "subtracted_root_half_interval": old["rounded"](old_root_half),
        "independent_gain_interval": old["rounded"](gain),
        "independent_free_V4_revenue_interval": old["rounded"](free_revenue),
        "independent_total_revenue_interval": old["rounded"](total),
        "free_opponent_area": str(free_area),
        "constrained_opponent_area": str(constrained_area),
        "solved_opponent_area": str(solved_area),
        "bidder_2_value_on_closed_Q": {"rational": str(solved_value_rational),
                                        "sqrt2_coefficient": str(solved_value_radical)},
        "sqrt_bracket_bits": 160,
        "binomial_order": old["order"],
        "frozen_V3_replay_write_disabled": True,
    }


if __name__ == "__main__":
    data = certificate()
    destination = ROOT / "certificate" / "independent_revenue.json"
    if "--write" in sys.argv:
        destination.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    else:
        require(json.loads(destination.read_text(encoding="utf-8")) == data, "saved independent replay")
    print("PASS independent_revenue: exact gain, old-root factor, V4 baseline and solved area")
