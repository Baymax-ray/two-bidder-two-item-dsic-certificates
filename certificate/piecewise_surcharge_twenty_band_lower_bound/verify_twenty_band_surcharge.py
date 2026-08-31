#!/usr/bin/env python3
"""Primary exact verifier for the sealed twenty-band surcharge certificate."""

from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path


HERE = Path(__file__).resolve().parent


def clean(poly):
    values = list(poly)
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def add(left, right):
    return clean(
        (left[k] if k < len(left) else Q(0))
        + (right[k] if k < len(right) else Q(0))
        for k in range(max(len(left), len(right)))
    )


def scale(poly, scalar):
    return clean(scalar * value for value in poly)


def subtract(left, right):
    return add(left, scale(right, -1))


def multiply(left, right):
    result = [Q(0)] * (len(left) + len(right) - 1)
    for i, value in enumerate(left):
        for j, other in enumerate(right):
            result[i + j] += value * other
    return clean(result)


def evaluate(poly, point):
    result = Q(0)
    for value in reversed(poly):
        result = result * point + value
    return result


def integrate(poly, lo, hi):
    return sum(
        value * (hi ** (degree + 1) - lo ** (degree + 1))
        / Q(degree + 1)
        for degree, value in enumerate(poly)
    )


ONE = (Q(1),)
T = (Q(0), Q(1))


def menu_revenue(a, b, c):
    first = multiply(multiply(a, subtract(ONE, a)), subtract(c, a))
    second = multiply(multiply(b, subtract(ONE, b)), subtract(c, b))
    rectangle = multiply(add(subtract(ONE, c), b), add(subtract(ONE, c), a))
    excess = subtract(add(a, b), c)
    triangle = scale(multiply(excess, excess), Q(1, 2))
    return add(add(first, second), multiply(c, subtract(rectangle, triangle)))


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest().upper()


def reconstruct_prices(q1, q2, a, b, s):
    pivot = max(Q(0), q1 - a, q2 - a, q1 + q2 - b)
    return (
        pivot + min(a, s - q2),
        pivot + min(a, s - q1),
        pivot + b,
        pivot,
    )


def check_chamber(chamber, lo, hi, fee, a, b, s):
    d = s - a
    c = b - a
    if chamber == "zero_pivot_one_high_triangle":
        assert d < lo < hi <= a
        assert Q(0) < b - hi <= b - lo < d
        prices = (subtract((s,), T), (a,), (b,))
        for t in (lo, hi):
            for rho in (Q(0), b - t):
                direct = reconstruct_prices(rho, t, a, b, s)
                assert direct == (s - t, a, b, Q(0))
    elif chamber == "singleton_pivot_rectangle":
        assert a <= lo < hi
        assert hi + c + fee <= 1
        assert c < d
        prices = (T, (d,), add(T, (c,)))
        for t in (lo, hi):
            for rho in (Q(0), c):
                direct = reconstruct_prices(t, rho, a, b, s)
                assert direct == (t, d, t + c, t - a)
    else:
        raise AssertionError(chamber)

    for t in (lo, (lo + hi) / 2, hi):
        pa, pb, pc = (evaluate(price, t) + fee for price in prices)
        assert Q(0) <= pa <= pc <= 1
        assert Q(0) <= pb <= pc
        assert pc <= pa + pb
    return prices


def row_gain(chamber, lo, hi, fee, prices, b, c):
    shifted = tuple(add(price, (fee,)) for price in prices)
    delta = subtract(menu_revenue(*shifted), menu_revenue(*prices))
    weight = (b, Q(-1)) if chamber == "zero_pivot_one_high_triangle" else (c,)
    return 4 * integrate(multiply(weight, delta), lo, hi)


def main():
    manifest = json.loads(
        (HERE / "manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["certificate"] == (
        "twenty_band_piecewise_opponent_dependent_common_entry_"
        "surcharge_lower_bound"
    )
    assert manifest["scope"] == "primal_lower_bound_only"
    assert manifest["status"] == "SEALED"

    predecessor_reference = manifest["predecessor_certificate"]
    predecessor_dir = (HERE / predecessor_reference["directory"]).resolve()
    for name, key in (
        ("manifest.json", "manifest_sha256"),
        ("verify_piecewise_surcharge.py", "verifier_sha256"),
        ("verification_output.txt", "verification_output_sha256"),
        ("independent_replay.py", "independent_replay_sha256"),
        ("independent_replay_output.txt", "independent_replay_output_sha256"),
        ("SHA256SUMS.txt", "sha256s_sha256"),
    ):
        assert file_hash(predecessor_dir / name) == predecessor_reference[key]
    predecessor = json.loads(
        (predecessor_dir / "manifest.json").read_text(encoding="utf-8")
    )

    base_reference = manifest["base_certificate"]
    assert base_reference == predecessor["base_certificate"]
    base_dir = (HERE / base_reference["directory"]).resolve()
    for name, key in (
        ("manifest.json", "manifest_sha256"),
        ("verify_ama.py", "verifier_sha256"),
        ("verification_output.txt", "output_sha256"),
    ):
        assert file_hash(base_dir / name) == base_reference[key]
    base = json.loads((base_dir / "manifest.json").read_text(encoding="utf-8"))

    upper_reference = manifest["upper_reference"]
    upper_dir = (HERE / upper_reference["directory"]).resolve()
    for name, key in (
        ("manifest.json", "manifest_sha256"),
        ("verify_stream_dual.py", "verifier_sha256"),
        ("verification_output.txt", "verification_output_sha256"),
        ("independent_replay.py", "independent_replay_sha256"),
        ("independent_replay_output.txt", "independent_replay_output_sha256"),
        ("SHA256SUMS.txt", "sha256s_sha256"),
    ):
        assert file_hash(upper_dir / name) == upper_reference[key]
    upper_manifest = json.loads(
        (upper_dir / "manifest.json").read_text(encoding="utf-8")
    )
    upper = Q(upper_manifest["expected"]["promoted"]["upper_fraction"])
    assert upper == Q(upper_reference["expected_upper_bound"])

    parameters = base["parameters"]
    a = Q(parameters["single_item_cost_a"])
    b = Q(parameters["same_bidder_bundle_cost_b"])
    s = Q(parameters["split_allocation_cost_s"])
    assert (a, b, s) == (Q(159, 250), Q(91, 100), Q(1137, 1000))
    c = b - a

    mechanism = manifest["mechanism"]
    assert mechanism["applies_to"] == "all nonempty options"
    assert mechanism["zero_utility_rule"] == "opt out"
    assert mechanism["nonempty_tie_rule"] == (
        "inherit the base smallest-outcome-id bundle"
    )
    assert mechanism["region_boundary_rule"] == (
        "test rows in listed order; the first matching closed row supplies "
        "the fee; otherwise the fee is zero"
    )
    assert int(mechanism["orientation_count"]) == 2
    assert int(mechanism["symmetric_bidder_count"]) == 2
    assert mechanism["chambers"] == {
        "zero_pivot_one_high_triangle": "0 <= rho <= b-t",
        "singleton_pivot_rectangle": "0 <= rho <= b-a",
    }
    rows = mechanism["rows"]
    assert len(rows) == 20

    predecessor_bands = {
        band["id"]: band for band in predecessor["mechanism"]["bands"]
    }
    by_parent = {}
    for row in rows:
        by_parent.setdefault(row["parent"], []).append(row)
    assert set(by_parent) == set(predecessor_bands)
    for parent_id, halves in by_parent.items():
        assert len(halves) == 2
        parent = predecessor_bands[parent_id]
        parent_lo, parent_hi = map(Q, parent["high_interval"])
        midpoint = (parent_lo + parent_hi) / 2
        first_lo, first_hi = map(Q, halves[0]["high_interval"])
        second_lo, second_hi = map(Q, halves[1]["high_interval"])
        assert (first_lo, first_hi, second_lo, second_hi) == (
            parent_lo, midpoint, midpoint, parent_hi
        )
        assert halves[0]["chamber"] == halves[1]["chamber"] == parent["chamber"]

    total = Q(0)
    chamber_totals = {
        "zero_pivot_one_high_triangle": Q(0),
        "singleton_pivot_rectangle": Q(0),
    }
    printed = []
    for row in rows:
        chamber = row["chamber"]
        lo, hi = map(Q, row["high_interval"])
        fee = Q(row["fee"])
        assert fee > 0
        prices = check_chamber(chamber, lo, hi, fee, a, b, s)
        gain = row_gain(chamber, lo, hi, fee, prices, b, c)
        assert gain == Q(row["expected_gain"])
        assert gain > 0
        total += gain
        chamber_totals[chamber] += gain
        printed.append((row["id"], lo, hi, fee, gain))

    expected = manifest["expected"]
    assert chamber_totals["zero_pivot_one_high_triangle"] == Q(
        expected["zero_pivot_total_gain"]
    )
    assert chamber_totals["singleton_pivot_rectangle"] == Q(
        expected["singleton_pivot_total_gain"]
    )
    predecessor_gain = Q(
        predecessor["expected"]["total_revenue_gain_over_base"]
    )
    assert predecessor_gain == Q(expected["predecessor_surcharge_gain"])
    assert total == Q(expected["total_revenue_gain_over_base"])
    assert total - predecessor_gain == Q(
        expected["strict_improvement_over_predecessor"]
    )
    assert total > predecessor_gain

    base_revenue = Q(base["expected"]["expected_revenue"])
    assert base_revenue == Q(expected["base_revenue"])
    final_revenue = base_revenue + total
    predecessor_revenue = Q(predecessor_reference["expected_revenue"])
    assert predecessor_revenue == Q(predecessor["expected"]["final_expected_revenue"])
    assert final_revenue == Q(expected["final_expected_revenue"])
    assert final_revenue - predecessor_revenue == Q(
        expected["strict_improvement_over_predecessor"]
    )
    assert upper == Q(expected["current_exact_upper"])
    assert upper - final_revenue == Q(expected["remaining_exact_gap"])

    print("TWENTY-BAND RATIONAL SURCHARGE LOWER CERTIFICATE: PASS")
    print("affine-base, predecessor, and current-upper dependency hashes: PASS")
    print("ten predecessor bands split into twenty exact rational half-bands: PASS")
    print("common nonnegative opponent-only fee on all nonempty options: PASS")
    print("price regimes and deletion-feasibility chamber vertices: PASS")
    for row_id, lo, hi, fee, gain in printed:
        print(f"{row_id}: t=[{lo},{hi}], fee={fee}, exact gain={gain}")
    print(f"zero-pivot gain: {chamber_totals['zero_pivot_one_high_triangle']}")
    print(f"singleton-pivot gain: {chamber_totals['singleton_pivot_rectangle']}")
    print(f"total surcharge gain: {total}")
    print(f"strict gain over predecessor: {total - predecessor_gain}")
    print(f"certified exact expected revenue: {final_revenue}")
    print(f"remaining exact gap to current upper: {upper - final_revenue}")
    print("scope: exact deterministic DSIC/ex-post-IR primal lower bound; no optimality claim")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, ValueError, OSError) as error:
        print(
            f"TWENTY-BAND RATIONAL SURCHARGE LOWER CERTIFICATE: FAIL: {error}",
            file=sys.stderr,
        )
        raise SystemExit(1)
