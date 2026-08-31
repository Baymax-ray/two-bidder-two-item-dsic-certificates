#!/usr/bin/env python3
"""Independent scalar/quadrature replay of the combined lower certificate."""

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
    values = [function(lo + index * step) for index in range(5)]
    weights = (7, 32, 12, 32, 7)
    return 2 * step * sum(
        (Q(weight) * value for weight, value in zip(weights, values)), Q(0)
    ) / 45


def forward_difference(function, lo, hi, order):
    step = (hi - lo) / order
    row = [function(lo + index * step) for index in range(order + 1)]
    for _ in range(order):
        row = [row[index + 1] - row[index] for index in range(len(row) - 1)]
    return row[0]


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest().upper()


def check_package(reference, directory, entries):
    for name, key in entries:
        assert file_hash(directory / name) == reference[key]


def main():
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["certificate"] == (
        "combined_twenty_band_and_bundle_pivot_common_entry_"
        "surcharge_lower_bound"
    )
    assert manifest["scope"] == "primal_lower_bound_only"
    assert manifest["status"] == "SEALED"

    predecessor_reference = manifest["predecessor_certificate"]
    predecessor_dir = (HERE / predecessor_reference["directory"]).resolve()
    check_package(
        predecessor_reference,
        predecessor_dir,
        (
            ("manifest.json", "manifest_sha256"),
            ("verify_twenty_band_surcharge.py", "verifier_sha256"),
            ("verification_output.txt", "verification_output_sha256"),
            ("independent_replay.py", "independent_replay_sha256"),
            ("independent_replay_output.txt", "independent_replay_output_sha256"),
            ("SHA256SUMS.txt", "sha256s_sha256"),
        ),
    )
    predecessor = json.loads(
        (predecessor_dir / "manifest.json").read_text(encoding="utf-8")
    )

    base_reference = manifest["base_certificate"]
    assert base_reference == predecessor["base_certificate"]
    base_dir = (HERE / base_reference["directory"]).resolve()
    check_package(
        base_reference,
        base_dir,
        (
            ("manifest.json", "manifest_sha256"),
            ("verify_ama.py", "verifier_sha256"),
            ("verification_output.txt", "output_sha256"),
        ),
    )
    base = json.loads((base_dir / "manifest.json").read_text(encoding="utf-8"))

    upper_reference = manifest["upper_reference"]
    upper_dir = (HERE / upper_reference["directory"]).resolve()
    check_package(
        upper_reference,
        upper_dir,
        (
            ("manifest.json", "manifest_sha256"),
            ("verify_stream_dual.py", "verifier_sha256"),
            ("verification_output.txt", "verification_output_sha256"),
            ("independent_replay.py", "independent_replay_sha256"),
            ("independent_replay_output.txt", "independent_replay_output_sha256"),
            ("SHA256SUMS.txt", "sha256s_sha256"),
        ),
    )
    upper_manifest = json.loads(
        (upper_dir / "manifest.json").read_text(encoding="utf-8")
    )
    upper = Q(upper_manifest["expected"]["promoted"]["upper_fraction"])
    assert upper == Q(upper_reference["expected_upper_bound"])

    parameters = base["parameters"]
    a = Q(parameters["single_item_cost_a"])
    b = Q(parameters["same_bidder_bundle_cost_b"])
    s = Q(parameters["split_allocation_cost_s"])
    c = b - a
    d = s - a
    e = s - b
    k = c + d
    assert (a, b, s, c, d, e, k) == (
        Q(159, 250),
        Q(91, 100),
        Q(1137, 1000),
        Q(137, 500),
        Q(501, 1000),
        Q(227, 1000),
        Q(31, 40),
    )

    mechanism = manifest["mechanism"]
    assert mechanism["applies_to"] == "all nonempty options"
    assert mechanism["zero_utility_rule"] == "opt out"
    assert mechanism["ordered_rule"] == (
        "test the predecessor twenty-band rows first, then the bundle-pivot "
        "extension rows in listed order; the first matching closed row "
        "supplies the fee; otherwise the fee is zero"
    )
    factor = int(mechanism["orientation_count"]) * int(
        mechanism["symmetric_bidder_count"]
    )
    assert factor == 4
    extension = mechanism["bundle_pivot_extension"]
    assert extension["canonical_region"] == (
        "91/100 <= u <= 1 and c <= rho <= u-d"
    )
    assert extension["base_prices"] == "(A,B,C)=(u-c,rho+e,u)"
    assert extension["jacobian_in_u_r"] == "u-k"
    rows = extension["rows"]
    assert len(rows) == int(extension["positive_fee_cell_count"]) == 41

    seen_cells = set()
    total = Q(0)
    printed = []
    for row in rows:
        prefix, strip_text = row["id"].split(".")
        band = int(prefix[1:])
        strip = int(strip_text)
        assert 1 <= band <= 18 and 1 <= strip <= 8
        assert (band, strip) not in seen_cells
        seen_cells.add((band, strip))

        u_lo, u_hi = map(Q, row["sum_interval"])
        r_lo, r_hi = map(Q, row["normalized_rho_interval"])
        assert (u_lo, u_hi) == (
            b + Q(band - 1, 200),
            b + Q(band, 200),
        )
        assert (r_lo, r_hi) == (Q(strip - 1, 8), Q(strip, 8))
        fee = Q(row["fee"])
        assert Q(0) < fee <= 1 - u_hi

        def integrand(u, r):
            width = u - k
            rho = c + r * width
            prices = (u - c, rho + e, u)
            shifted = tuple(price + fee for price in prices)
            return factor * width * (
                scalar_menu_revenue(*shifted) - scalar_menu_revenue(*prices)
            )

        for u in (u_lo, (u_lo + u_hi) / 2, u_hi):
            assert forward_difference(
                lambda r: integrand(u, r), r_lo, r_hi, 4
            ) == 0
        for r in (r_lo, (r_lo + r_hi) / 2, r_hi):
            assert forward_difference(
                lambda u: integrand(u, r), u_lo, u_hi, 5
            ) == 0

        for u in (u_lo, u_hi):
            for r in (r_lo, r_hi):
                width = u - k
                rho = c + r * width
                t = u - rho
                pivot = max(Q(0), t - a, rho - a, u - b)
                direct = (
                    pivot + min(a, s - rho),
                    pivot + min(a, s - t),
                    pivot + b,
                    pivot,
                )
                assert c <= rho <= u - d
                assert rho <= t
                assert direct == (u - c, rho + e, u, u - b)
                pa, pb, pc = (direct[index] + fee for index in range(3))
                assert Q(0) <= pb <= pa <= pc <= 1
                assert pc <= pa + pb

        gain = boole(
            lambda u: boole(
                lambda r: integrand(u, r), r_lo, r_hi
            ),
            u_lo,
            u_hi,
        )
        assert gain == Q(row["expected_gain"])
        assert gain > 0
        total += gain
        printed.append((row["id"], gain))

    expected = manifest["expected"]
    assert total == Q(expected["bundle_pivot_extension_gain"])
    predecessor_revenue = Q(predecessor_reference["expected_revenue"])
    assert predecessor_revenue == Q(expected["predecessor_revenue"])
    base_revenue = Q(base["expected"]["expected_revenue"])
    assert base_revenue == Q(expected["base_revenue"])
    final_revenue = predecessor_revenue + total
    assert final_revenue == Q(expected["final_expected_revenue"])
    assert final_revenue - base_revenue == Q(expected["total_revenue_gain_over_base"])
    assert total == Q(expected["strict_improvement_over_predecessor"])
    assert upper == Q(expected["current_exact_upper"])
    assert upper - final_revenue == Q(expected["remaining_exact_gap"])

    print("INDEPENDENT COMBINED SURCHARGE LOWER-CERTIFICATE REPLAY: PASS")
    print("method: scalar Fraction arithmetic and tensor exact Boole quadrature")
    print("affine-base, predecessor, and current-upper dependency hashes: PASS")
    print("degree <=4 in u and <=3 in r, with Jacobian u-k: PASS")
    print("bundle-pivot chamber and deletion-compatible price regimes: PASS")
    for row_id, gain in printed:
        print(f"{row_id}: exact symmetric gain={gain}")
    print(f"bundle-pivot extension gain: {total}")
    print(f"certified exact expected revenue: {final_revenue}")
    print(f"strict improvement over predecessor: {total}")
    print(f"remaining exact gap to current upper: {upper - final_revenue}")
    print("scope: independent exact primal replay; no global-optimality claim")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, ValueError, OSError) as error:
        print(
            f"INDEPENDENT COMBINED SURCHARGE LOWER-CERTIFICATE REPLAY: FAIL: {error}",
            file=sys.stderr,
        )
        raise SystemExit(1)
