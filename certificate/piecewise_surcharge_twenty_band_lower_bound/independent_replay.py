#!/usr/bin/env python3
"""Independent exact scalar replay of the sealed twenty-band certificate."""

from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path


HERE = Path(__file__).resolve().parent


def scalar_menu_revenue(a, b, c):
    return (
        a * (1 - a) * (c - a)
        + b * (1 - b) * (c - b)
        + c * ((1 - c + b) * (1 - c + a) - (a + b - c) ** 2 / 2)
    )


def boole(function, lo, hi):
    step = (hi - lo) / 4
    values = [function(lo + k * step) for k in range(5)]
    return (
        2 * step
        * sum((Q(weight) * value for weight, value in zip(
            (7, 32, 12, 32, 7), values
        )), Q(0))
        / 45
    )


def fifth_difference(function, lo, hi):
    step = (hi - lo) / 5
    row = [function(lo + k * step) for k in range(6)]
    while len(row) > 1:
        row = [row[k + 1] - row[k] for k in range(len(row) - 1)]
    return row[0]


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest().upper()


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
    base_manifest = json.loads(
        (base_dir / "manifest.json").read_text(encoding="utf-8")
    )

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
    printed = []
    rows = manifest["mechanism"]["rows"]
    assert len(rows) == 20

    predecessor_bands = {
        band["id"]: band for band in predecessor["mechanism"]["bands"]
    }
    grouped = {}
    for row in rows:
        grouped.setdefault(row["parent"], []).append(row)
    assert set(grouped) == set(predecessor_bands)
    for parent_id, halves in grouped.items():
        assert len(halves) == 2
        parent = predecessor_bands[parent_id]
        parent_lo, parent_hi = map(Q, parent["high_interval"])
        midpoint = (parent_lo + parent_hi) / 2
        endpoints = tuple(
            point
            for half in halves
            for point in map(Q, half["high_interval"])
        )
        assert endpoints == (parent_lo, midpoint, midpoint, parent_hi)
        assert halves[0]["chamber"] == halves[1]["chamber"] == parent["chamber"]

    for row in rows:
        chamber = row["chamber"]
        lo, hi = map(Q, row["high_interval"])
        fee = Q(row["fee"])
        assert fee > 0
        if chamber == "zero_pivot_one_high_triangle":
            assert d < lo < hi <= a
            assert Q(0) < b - hi <= b - lo < d
            for t in (lo, hi):
                raised_prices = (s - t + fee, a + fee, b + fee)
                pa, pb, pc = raised_prices
                assert Q(0) <= pa <= pc <= 1
                assert Q(0) <= pb <= pc <= pa + pb

            def integrand(t):
                base = scalar_menu_revenue(s - t, a, b)
                raised = scalar_menu_revenue(s - t + fee, a + fee, b + fee)
                return (b - t) * (raised - base)
        elif chamber == "singleton_pivot_rectangle":
            assert a <= lo < hi
            assert c < d
            for t in (lo, hi):
                raised_prices = (t + fee, d + fee, t + c + fee)
                pa, pb, pc = raised_prices
                assert Q(0) <= pa <= pc <= 1
                assert Q(0) <= pb <= pc <= pa + pb

            def integrand(t):
                base = scalar_menu_revenue(t, d, t + c)
                raised = scalar_menu_revenue(t + fee, d + fee, t + c + fee)
                return c * (raised - base)
        else:
            raise AssertionError(chamber)

        assert fifth_difference(integrand, lo, hi) == 0
        gain = factor * boole(integrand, lo, hi)
        assert gain == Q(row["expected_gain"])
        totals[chamber] += gain
        printed.append((row["id"], gain))

    expected = manifest["expected"]
    total = sum(totals.values(), Q(0))
    assert totals["zero_pivot_one_high_triangle"] == Q(
        expected["zero_pivot_total_gain"]
    )
    assert totals["singleton_pivot_rectangle"] == Q(
        expected["singleton_pivot_total_gain"]
    )
    assert total == Q(expected["total_revenue_gain_over_base"])
    predecessor_gain = Q(
        predecessor["expected"]["total_revenue_gain_over_base"]
    )
    assert predecessor_gain == Q(expected["predecessor_surcharge_gain"])
    assert total - predecessor_gain == Q(
        expected["strict_improvement_over_predecessor"]
    )
    base_revenue = Q(base_manifest["expected"]["expected_revenue"])
    assert base_revenue == Q(expected["base_revenue"])
    final = base_revenue + total
    predecessor_revenue = Q(predecessor_reference["expected_revenue"])
    assert predecessor_revenue == Q(predecessor["expected"]["final_expected_revenue"])
    assert final == Q(expected["final_expected_revenue"])
    assert final - predecessor_revenue == Q(
        expected["strict_improvement_over_predecessor"]
    )
    assert upper == Q(expected["current_exact_upper"])
    assert upper - final == Q(expected["remaining_exact_gap"])

    print("INDEPENDENT TWENTY-BAND LOWER-CERTIFICATE REPLAY: PASS")
    print("method: scalar Fraction arithmetic, degree check, exact Boole quadrature")
    print("affine-base, predecessor, and current-upper dependency hashes: PASS")
    for row_id, gain in printed:
        print(f"{row_id}: exact symmetric gain={gain}")
    print(f"zero-pivot gain: {totals['zero_pivot_one_high_triangle']}")
    print(f"singleton-pivot gain: {totals['singleton_pivot_rectangle']}")
    print(f"total surcharge gain: {total}")
    print(f"certified exact expected revenue: {final}")
    print(f"strict improvement over predecessor: {final - predecessor_revenue}")
    print(f"remaining exact gap to current upper: {upper - final}")
    print("scope: independent exact primal replay; no global-optimality claim")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, ValueError, OSError) as error:
        print(
            f"INDEPENDENT TWENTY-BAND LOWER-CERTIFICATE REPLAY: FAIL: {error}",
            file=sys.stderr,
        )
        raise SystemExit(1)
