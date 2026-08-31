#!/usr/bin/env python3
"""Primary exact verifier for the combined surcharge lower certificate."""

from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path


HERE = Path(__file__).resolve().parent


def clean(poly):
    return {key: value for key, value in poly.items() if value}


def constant(value):
    value = Q(value)
    return {} if value == 0 else {(0, 0): value}


def add(left, right):
    result = dict(left)
    for key, value in right.items():
        result[key] = result.get(key, Q(0)) + value
    return clean(result)


def scale(poly, scalar):
    return clean({key: Q(scalar) * value for key, value in poly.items()})


def subtract(left, right):
    return add(left, scale(right, -1))


def multiply(left, right):
    result = {}
    for (i, j), value in left.items():
        for (k, ell), other in right.items():
            key = (i + k, j + ell)
            result[key] = result.get(key, Q(0)) + value * other
    return clean(result)


ONE = constant(1)
U = {(1, 0): Q(1)}
RHO = {(0, 1): Q(1)}


def menu_revenue(a, b, c):
    first = multiply(multiply(a, subtract(ONE, a)), subtract(c, a))
    second = multiply(multiply(b, subtract(ONE, b)), subtract(c, b))
    rectangle = multiply(add(subtract(ONE, c), b), add(subtract(ONE, c), a))
    excess = subtract(add(a, b), c)
    triangle = scale(multiply(excess, excess), Q(1, 2))
    return add(add(first, second), multiply(c, subtract(rectangle, triangle)))


def univariate_add(left, right):
    result = dict(left)
    for degree, value in right.items():
        result[degree] = result.get(degree, Q(0)) + value
    return {degree: value for degree, value in result.items() if value}


def univariate_multiply(left, right):
    result = {}
    for i, value in left.items():
        for j, other in right.items():
            result[i + j] = result.get(i + j, Q(0)) + value * other
    return {degree: value for degree, value in result.items() if value}


def univariate_power(poly, exponent):
    result = {0: Q(1)}
    for _ in range(exponent):
        result = univariate_multiply(result, poly)
    return result


def integrate_cell(poly, u_lo, u_hi, alpha, beta, c, k):
    lower = {0: c - alpha * k, 1: alpha}
    upper = {0: c - beta * k, 1: beta}
    integrated = {}
    for (u_degree, rho_degree), coefficient in poly.items():
        exponent = rho_degree + 1
        difference = univariate_add(
            univariate_power(upper, exponent),
            {degree: -value for degree, value in univariate_power(lower, exponent).items()},
        )
        for degree, value in difference.items():
            target = u_degree + degree
            integrated[target] = integrated.get(target, Q(0)) + (
                coefficient * value / exponent
            )
    return sum(
        coefficient
        * (u_hi ** (degree + 1) - u_lo ** (degree + 1))
        / (degree + 1)
        for degree, coefficient in integrated.items()
    )


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest().upper()


def check_package(reference, directory, entries):
    for name, key in entries:
        assert file_hash(directory / name) == reference[key]


def reconstruct_prices(q1, q2, a, b, s):
    pivot = max(Q(0), q1 - a, q2 - a, q1 + q2 - b)
    return (
        pivot + min(a, s - q2),
        pivot + min(a, s - q1),
        pivot + b,
        pivot,
    )


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
    assert (a, b, s) == (Q(159, 250), Q(91, 100), Q(1137, 1000))
    c = b - a
    d = s - a
    e = s - b
    k = c + d

    mechanism = manifest["mechanism"]
    assert mechanism["applies_to"] == "all nonempty options"
    assert mechanism["zero_utility_rule"] == "opt out"
    assert mechanism["nonempty_tie_rule"] == (
        "inherit the base smallest-outcome-id bundle"
    )
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
    constants = extension["constants"]
    assert (c, d, e, k) == tuple(
        Q(constants[name]) for name in ("c", "d", "e", "k")
    )
    assert k == Q(31, 40)
    assert extension["canonical_region"] == (
        "91/100 <= u <= 1 and c <= rho <= u-d"
    )
    assert extension["base_prices"] == "(A,B,C)=(u-c,rho+e,u)"
    assert extension["jacobian_in_u_r"] == "u-k"
    assert int(extension["sum_band_count"]) == 18
    assert int(extension["normalized_rho_strip_count"]) == 8

    predecessor_chambers = predecessor["mechanism"]["chambers"]
    assert predecessor_chambers == {
        "zero_pivot_one_high_triangle": "0 <= rho <= b-t",
        "singleton_pivot_rectangle": "0 <= rho <= b-a",
    }
    # Each tuple is the exact affine form (constant, t coefficient,
    # rho coefficient).  A predecessor Z interior makes u-b<0, whereas a
    # bundle-cell interior makes the identical form positive.  Likewise an S
    # interior makes rho-c<0 and a bundle-cell interior makes it positive.
    u_minus_b = (-b, Q(1), Q(1))
    rho_minus_c = (-c, Q(0), Q(1))
    predecessor_separators = set()
    for predecessor_row in predecessor["mechanism"]["rows"]:
        chamber = predecessor_row["chamber"]
        if chamber == "zero_pivot_one_high_triangle":
            assert predecessor_chambers[chamber] == "0 <= rho <= b-t"
            z_constraint = (-b, Q(1), Q(1))  # rho-(b-t) <= 0
            assert z_constraint == u_minus_b
            predecessor_separators.add("u=b")
        elif chamber == "singleton_pivot_rectangle":
            assert predecessor_chambers[chamber] == "0 <= rho <= b-a"
            s_constraint = (-(b - a), Q(0), Q(1))  # rho-(b-a) <= 0
            assert s_constraint == rho_minus_c
            predecessor_separators.add("rho=c")
        else:
            raise AssertionError(chamber)
    assert predecessor_separators == {"u=b", "rho=c"}

    base_prices = (subtract(U, constant(c)), add(RHO, constant(e)), U)
    base_revenue_poly = menu_revenue(*base_prices)
    seen_cells = set()
    total = Q(0)
    printed = []
    rows = extension["rows"]
    assert len(rows) == int(extension["positive_fee_cell_count"]) == 41
    for row in rows:
        prefix, strip_text = row["id"].split(".")
        band = int(prefix[1:])
        strip = int(strip_text)
        assert 1 <= band <= 18 and 1 <= strip <= 8
        assert (band, strip) not in seen_cells
        seen_cells.add((band, strip))

        u_lo, u_hi = map(Q, row["sum_interval"])
        alpha, beta = map(Q, row["normalized_rho_interval"])
        assert (u_lo, u_hi) == (
            b + Q(band - 1, 200),
            b + Q(band, 200),
        )
        assert (alpha, beta) == (Q(strip - 1, 8), Q(strip, 8))
        # Hence every bundle-cell interior has u>b and r>0, so rho>c.
        # It can meet a predecessor Z or S cell only on u=b or rho=c.
        assert b <= u_lo < u_hi
        assert Q(0) <= alpha < beta
        fee = Q(row["fee"])
        assert fee > 0
        assert fee <= 1 - u_hi

        for u in (u_lo, u_hi):
            width = u - k
            assert width > 0
            for r in (alpha, beta):
                rho = c + r * width
                t = u - rho
                assert b <= u <= 1
                assert c <= rho <= u - d
                assert Q(0) <= rho <= t <= 1
                direct = reconstruct_prices(t, rho, a, b, s)
                assert direct == (u - c, rho + e, u, u - b)
                pa, pb, pc = (direct[index] + fee for index in range(3))
                assert Q(0) <= pb <= pa <= pc <= 1
                assert pc <= pa + pb

        shifted = tuple(add(price, constant(fee)) for price in base_prices)
        delta = subtract(menu_revenue(*shifted), base_revenue_poly)
        gain = factor * integrate_cell(delta, u_lo, u_hi, alpha, beta, c, k)
        assert gain == Q(row["expected_gain"])
        assert gain > 0
        total += gain
        printed.append((row["id"], u_lo, u_hi, alpha, beta, fee, gain))

    expected = manifest["expected"]
    assert total == Q(expected["bundle_pivot_extension_gain"])
    predecessor_revenue = Q(predecessor_reference["expected_revenue"])
    assert predecessor_revenue == Q(expected["predecessor_revenue"])
    assert predecessor_revenue == Q(predecessor["expected"]["final_expected_revenue"])
    predecessor_gain = Q(predecessor["expected"]["total_revenue_gain_over_base"])
    assert predecessor_gain == Q(expected["predecessor_surcharge_gain"])
    base_revenue = Q(base["expected"]["expected_revenue"])
    assert base_revenue == Q(expected["base_revenue"])
    final_revenue = predecessor_revenue + total
    assert final_revenue == Q(expected["final_expected_revenue"])
    assert final_revenue - base_revenue == Q(expected["total_revenue_gain_over_base"])
    assert total == Q(expected["strict_improvement_over_predecessor"])
    ten_band_revenue = Q(
        predecessor["predecessor_certificate"]["expected_revenue"]
    )
    assert final_revenue - ten_band_revenue == Q(
        expected["strict_improvement_over_ten_band_lower"]
    )
    assert upper == Q(expected["current_exact_upper"])
    assert upper - final_revenue == Q(expected["remaining_exact_gap"])

    print("COMBINED TWENTY-BAND + BUNDLE-PIVOT LOWER CERTIFICATE: PASS")
    print("affine-base, predecessor, and current-upper dependency hashes: PASS")
    print("bundle-pivot chamber reconstruction and price regimes: PASS")
    print("Jacobian u-k and factor 2 item orientations x 2 bidders: PASS")
    print("Z/B separation by u=b and S/B separation by rho=c: PASS")
    print("shared boundaries assigned to predecessor by ordered rule: PASS")
    for row_id, lo, hi, alpha, beta, fee, gain in printed:
        print(
            f"{row_id}: u=[{lo},{hi}], r=[{alpha},{beta}], "
            f"fee={fee}, exact gain={gain}"
        )
    print(f"bundle-pivot extension gain: {total}")
    print(f"certified exact expected revenue: {final_revenue}")
    print(f"strict improvement over predecessor: {total}")
    print(f"remaining exact gap to current upper: {upper - final_revenue}")
    print("scope: exact deterministic DSIC/ex-post-IR primal lower bound; no optimality claim")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, ValueError, OSError) as error:
        print(
            f"COMBINED TWENTY-BAND + BUNDLE-PIVOT LOWER CERTIFICATE: FAIL: {error}",
            file=sys.stderr,
        )
        raise SystemExit(1)
