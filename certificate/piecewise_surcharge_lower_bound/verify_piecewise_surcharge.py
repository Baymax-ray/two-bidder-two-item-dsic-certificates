#!/usr/bin/env python3
"""Exact symbolic verifier for the piecewise common-surcharge mechanism."""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import sys


def clean(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def add(p, q):
    n = max(len(p), len(q))
    return clean(
        (p[k] if k < len(p) else Q(0))
        + (q[k] if k < len(q) else Q(0))
        for k in range(n)
    )


def neg(p):
    return tuple(-x for x in p)


def sub(p, q):
    return add(p, neg(q))


def scale(p, c):
    return clean(c * x for x in p)


def mul(p, q):
    out = [Q(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return clean(out)


def evaluate(p, t):
    total = Q(0)
    for coefficient in reversed(p):
        total = total * t + coefficient
    return total


def integrate(p, lo, hi):
    return sum(
        coefficient * (hi ** (k + 1) - lo ** (k + 1)) / Q(k + 1)
        for k, coefficient in enumerate(p)
    )


ONE = (Q(1),)
T = (Q(0), Q(1))


def menu_revenue(a, b, c):
    """Revenue polynomial for 0 <= a,b <= c <= 1 and c <= a+b."""
    item_1 = mul(mul(a, sub(ONE, a)), sub(c, a))
    item_2 = mul(mul(b, sub(ONE, b)), sub(c, b))
    rectangle = mul(add(sub(ONE, c), b), add(sub(ONE, c), a))
    triangle = scale(mul(sub(add(a, b), c), sub(add(a, b), c)), Q(1, 2))
    bundle = mul(c, sub(rectangle, triangle))
    return add(add(item_1, item_2), bundle)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest().upper()


def verify_base_dependency(manifest):
    dependency = manifest["base_certificate"]
    base_dir = (Path(__file__).resolve().parent / dependency["directory"]).resolve()
    for name, key in (
        ("manifest.json", "manifest_sha256"),
        ("verify_ama.py", "verifier_sha256"),
        ("verification_output.txt", "output_sha256"),
    ):
        path = base_dir / name
        assert path.is_file(), f"missing base dependency: {path}"
        assert file_sha256(path) == dependency[key], f"base hash mismatch: {name}"
    return json.loads((base_dir / "manifest.json").read_text(encoding="utf-8"))


def check_price_regime(prices, fee, lo, hi):
    for t in (lo, (lo + hi) / 2, hi):
        pa, pb, pc = (evaluate(p, t) + fee for p in prices)
        assert Q(0) <= pa <= pc <= Q(1)
        assert Q(0) <= pb <= pc
        assert pc <= pa + pb


def reconstruct_base_prices(q1, q2, a, b, s):
    h = max(Q(0), q1 - a, q2 - a, q1 + q2 - b)
    return (
        h + min(a, s - q2),
        h + min(a, s - q1),
        h + b,
        h,
    )


def check_chamber_vertices(chamber, lo, hi, a, b, s):
    d = s - a
    c = b - a
    if chamber == "zero_pivot_one_high_triangle":
        for t in (lo, hi):
            for rho in (Q(0), b - t):
                pa, pb, pc, h = reconstruct_base_prices(rho, t, a, b, s)
                assert h == 0
                assert (pa, pb, pc) == (s - t, a, b)
                pa, pb, pc, h = reconstruct_base_prices(t, rho, a, b, s)
                assert h == 0
                assert (pa, pb, pc) == (a, s - t, b)
    elif chamber == "singleton_pivot_rectangle":
        for t in (lo, hi):
            for rho in (Q(0), c):
                pa, pb, pc, h = reconstruct_base_prices(t, rho, a, b, s)
                assert h == t - a
                assert (pa, pb, pc) == (t, d, t + c)
                pa, pb, pc, h = reconstruct_base_prices(rho, t, a, b, s)
                assert h == t - a
                assert (pa, pb, pc) == (d, t, t + c)
    else:
        raise AssertionError(f"unknown chamber: {chamber}")


def main():
    manifest = json.loads(Path(__file__).with_name("manifest.json").read_text(encoding="utf-8"))
    assert manifest["scope"] == "primal_lower_bound_only"
    base_manifest = verify_base_dependency(manifest)
    parameters = base_manifest["parameters"]
    a = Q(parameters["single_item_cost_a"])
    b = Q(parameters["same_bidder_bundle_cost_b"])
    s = Q(parameters["split_allocation_cost_s"])
    assert (a, b, s) == (Q(159, 250), Q(91, 100), Q(1137, 1000))
    d = s - a
    c = b - a

    mechanism = manifest["mechanism"]
    factor = int(mechanism["orientation_count"]) * int(mechanism["symmetric_bidder_count"])
    assert factor == 4
    assert mechanism["applies_to"] == "all nonempty options"

    zero_prices = (sub((s,), T), (a,), (b,))
    singleton_prices = (T, (d,), add(T, (c,)))
    zero_base = menu_revenue(*zero_prices)
    singleton_base = menu_revenue(*singleton_prices)

    zero_gain = Q(0)
    singleton_gain = Q(0)
    previous_hi = {"zero_pivot_one_high_triangle": None, "singleton_pivot_rectangle": None}
    printed = []
    for band in mechanism["bands"]:
        chamber = band["chamber"]
        lo, hi = map(Q, band["high_interval"])
        fee = Q(band["fee"])
        assert lo < hi and fee > 0
        prior = previous_hi[chamber]
        assert prior is None or lo == prior, f"noncontiguous bands in {chamber}"
        previous_hi[chamber] = hi
        check_chamber_vertices(chamber, lo, hi, a, b, s)

        if chamber == "zero_pivot_one_high_triangle":
            assert d < lo < hi <= a
            assert Q(0) < b - hi <= b - lo < d
            prices = zero_prices
            delta = sub(
                menu_revenue(*(add(p, (fee,)) for p in prices)),
                zero_base,
            )
            check_price_regime(prices, fee, lo, hi)
            canonical_gain = integrate(mul((b, Q(-1)), delta), lo, hi)
            total_gain = factor * canonical_gain
            zero_gain += total_gain
        elif chamber == "singleton_pivot_rectangle":
            assert a <= lo < hi
            assert hi + c + fee <= 1
            assert c < d
            prices = singleton_prices
            delta = sub(
                menu_revenue(*(add(p, (fee,)) for p in prices)),
                singleton_base,
            )
            check_price_regime(prices, fee, lo, hi)
            canonical_gain = c * integrate(delta, lo, hi)
            total_gain = factor * canonical_gain
            singleton_gain += total_gain
        else:
            raise AssertionError(f"unknown chamber: {chamber}")

        assert total_gain == Q(band["expected_total_gain"]), f"gain mismatch: {band['id']}"
        assert total_gain > 0
        printed.append((band["id"], lo, hi, fee, total_gain))

    expected = manifest["expected"]
    assert zero_gain == Q(expected["zero_pivot_total_gain"])
    assert singleton_gain == Q(expected["singleton_pivot_total_gain"])
    total_gain = zero_gain + singleton_gain
    assert total_gain == Q(expected["total_revenue_gain_over_base"])

    base_revenue = Q(base_manifest["expected"]["expected_revenue"])
    assert base_revenue == Q(manifest["base_certificate"]["expected_revenue"])
    final_revenue = base_revenue + total_gain
    previous = Q(expected["previous_certified_lower_bound"])
    assert final_revenue == Q(expected["final_expected_revenue"])
    assert final_revenue - previous == Q(expected["strict_improvement_over_previous"])
    assert final_revenue > previous

    print("PIECEWISE-SURCHARGE LOWER-BOUND CERTIFICATE: PASS")
    print("base certificate hashes: PASS")
    print("base conditional menus reconstructed at every band vertex: PASS")
    print(f"parameters: a={a}, b={b}, s={s}, d=s-a={d}, c=b-a={c}")
    for band_id, lo, hi, fee, gain in printed:
        print(f"{band_id}: t=[{lo},{hi}], fee={fee}, exact symmetric gain={gain}")
    print(f"zero-pivot exact gain: {zero_gain}")
    print(f"singleton-pivot exact gain: {singleton_gain}")
    print(f"total exact gain over affine base: {total_gain}")
    print(f"exact expected revenue: {final_revenue}")
    print(f"strict improvement over previous lower: {final_revenue - previous}")
    print(f"decimal expected revenue: {float(final_revenue):.15f}")
    print("scope: exact feasible/DSIC/ex-post-IR primal lower bound only; no optimality claim")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, ValueError, OSError) as exc:
        print(f"PIECEWISE-SURCHARGE LOWER-BOUND CERTIFICATE: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)

