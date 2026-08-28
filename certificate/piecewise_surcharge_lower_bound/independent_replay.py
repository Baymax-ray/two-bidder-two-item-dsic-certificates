#!/usr/bin/env python3
"""Independent exact replay using scalar formulas and Boole quadrature.

This script does not import the symbolic verifier.  Boole's five-point rule is
exact here because each scalar menu-revenue difference is a polynomial of
degree at most three in t, and the triangular cross-section adds at most one
degree.
"""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import sys


def menu_revenue(a, b, c):
    return (
        a * (1 - a) * (c - a)
        + b * (1 - b) * (c - b)
        + c * ((1 - c + b) * (1 - c + a) - (a + b - c) ** 2 / 2)
    )


def boole(f, lo, hi):
    h = (hi - lo) / 4
    values = [f(lo + k * h) for k in range(5)]
    weights = (7, 32, 12, 32, 7)
    return 2 * h * sum((Q(w) * y for w, y in zip(weights, values)), Q(0)) / 45


def fifth_forward_difference(f, lo, hi):
    h = (hi - lo) / 5
    row = [f(lo + k * h) for k in range(6)]
    while len(row) > 1:
        row = [row[k + 1] - row[k] for k in range(len(row) - 1)]
    return row[0]


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest().upper()


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    dependency = manifest["base_certificate"]
    base_dir = (root / dependency["directory"]).resolve()
    for name, key in (
        ("manifest.json", "manifest_sha256"),
        ("verify_ama.py", "verifier_sha256"),
        ("verification_output.txt", "output_sha256"),
    ):
        assert file_sha256(base_dir / name) == dependency[key]
    base_manifest = json.loads((base_dir / "manifest.json").read_text(encoding="utf-8"))

    parameters = base_manifest["parameters"]
    a = Q(parameters["single_item_cost_a"])
    b = Q(parameters["same_bidder_bundle_cost_b"])
    s = Q(parameters["split_allocation_cost_s"])
    d = s - a
    c = b - a
    factor = (
        int(manifest["mechanism"]["orientation_count"])
        * int(manifest["mechanism"]["symmetric_bidder_count"])
    )
    assert factor == 4

    totals = {
        "zero_pivot_one_high_triangle": Q(0),
        "singleton_pivot_rectangle": Q(0),
    }
    rows = []
    for band in manifest["mechanism"]["bands"]:
        chamber = band["chamber"]
        lo, hi = map(Q, band["high_interval"])
        fee = Q(band["fee"])
        if chamber == "zero_pivot_one_high_triangle":
            def integrand(t):
                base = menu_revenue(s - t, a, b)
                raised = menu_revenue(s - t + fee, a + fee, b + fee)
                return (b - t) * (raised - base)
        elif chamber == "singleton_pivot_rectangle":
            def integrand(t):
                base = menu_revenue(t, d, t + c)
                raised = menu_revenue(t + fee, d + fee, t + c + fee)
                return c * (raised - base)
        else:
            raise AssertionError(f"unknown chamber: {chamber}")

        assert fifth_forward_difference(integrand, lo, hi) == 0
        total_gain = factor * boole(integrand, lo, hi)
        assert total_gain == Q(band["expected_total_gain"])
        totals[chamber] += total_gain
        rows.append((band["id"], total_gain))

    expected = manifest["expected"]
    assert totals["zero_pivot_one_high_triangle"] == Q(expected["zero_pivot_total_gain"])
    assert totals["singleton_pivot_rectangle"] == Q(expected["singleton_pivot_total_gain"])
    gain = sum(totals.values(), Q(0))
    assert gain == Q(expected["total_revenue_gain_over_base"])
    base = Q(base_manifest["expected"]["expected_revenue"])
    final = base + gain
    previous = Q(expected["previous_certified_lower_bound"])
    assert final == Q(expected["final_expected_revenue"])
    assert final - previous == Q(expected["strict_improvement_over_previous"])

    print("INDEPENDENT PIECEWISE-SURCHARGE REPLAY: PASS")
    print("method: scalar exact arithmetic + fifth-difference degree checks + exact Boole quadrature")
    print("base certificate hashes: PASS")
    for band_id, total_gain in rows:
        print(f"{band_id}: exact symmetric gain={total_gain}")
    print(f"zero-pivot exact gain: {totals['zero_pivot_one_high_triangle']}")
    print(f"singleton-pivot exact gain: {totals['singleton_pivot_rectangle']}")
    print(f"total exact gain over affine base: {gain}")
    print(f"exact expected revenue: {final}")
    print(f"strict improvement over previous lower: {final - previous}")
    print("scope: independent exact replay of a primal lower mechanism only")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, ValueError, OSError) as exc:
        print(f"INDEPENDENT PIECEWISE-SURCHARGE REPLAY: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)

