#!/usr/bin/env python3
"""Replay the eight-row gain, sharing the sealed predecessor revenue."""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def bind(reference, entries):
    folder = (HERE / reference["directory"]).resolve()
    for name, field in entries:
        need(digest(folder / name) == reference[field],
             f"dependency digest mismatch: {folder.name}/{name}")
    return folder


def clip(polygon, plane):
    aa, bb, cc = plane

    def value(point):
        return aa * point[0] + bb * point[1] + cc

    if not polygon:
        return []
    result = []
    previous = polygon[-1]
    previous_value = value(previous)
    for point in polygon:
        point_value = value(point)
        if (previous_value >= 0) != (point_value >= 0):
            ratio = previous_value / (previous_value - point_value)
            result.append((previous[0] + ratio * (point[0] - previous[0]),
                           previous[1] + ratio * (point[1] - previous[1])))
        if point_value >= 0:
            result.append(point)
        previous, previous_value = point, point_value
    return result


def area(polygon):
    if len(polygon) < 3:
        return Q(0)
    twice = sum(polygon[index][0] * polygon[(index + 1) % len(polygon)][1]
                - polygon[index][1] * polygon[(index + 1) % len(polygon)][0]
                for index in range(len(polygon)))
    return abs(twice) / 2


def demand_revenue(prices):
    a, b, c = prices
    options = (
        (Q(0), Q(0), Q(0), Q(0)),
        (Q(1), Q(0), -a, a),
        (Q(0), Q(1), -b, b),
        (Q(1), Q(1), -c, c),
    )
    square = [(Q(0), Q(0)), (Q(1), Q(0)),
              (Q(1), Q(1)), (Q(0), Q(1))]
    payment = Q(0)
    for chosen in options:
        cell = square
        for other in options:
            cell = clip(cell, (chosen[0] - other[0],
                               chosen[1] - other[1],
                               chosen[2] - other[2]))
        payment += chosen[3] * area(cell)
    return payment


def differences(values):
    return [right - left for left, right in zip(values, values[1:])]


def exact_boole(function, lower, upper, degree, label):
    # Polynomiality follows from the menu formula and whole-row price regime.
    # Finite differences only test consistency with the stated degree.
    fine_step = (upper - lower) / 8
    fine_values = [function(lower + index * fine_step) for index in range(9)]
    remainder = fine_values
    for _ in range(degree + 1):
        remainder = differences(remainder)
    need(all(value == 0 for value in remainder),
         f"finite-difference consistency check failed: {label}")
    values = fine_values[::2]
    step = (upper - lower) / 4
    return (Q(2) * step / 45
            * (7 * values[0] + 32 * values[1] + 12 * values[2]
               + 32 * values[3] + 7 * values[4]))


def check_prices(prices, label):
    a, b, c = prices
    need(Q(0) <= a <= c <= 1, f"A/C price regime failed: {label}")
    need(Q(0) <= b <= c <= a + b,
         f"B/subadditivity regime failed: {label}")


def main():
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    need(manifest["scope"] == "primal_lower_bound_only", "wrong scope")
    need(manifest["status"] == "SEALED", "manifest is not sealed")
    mechanism = manifest["mechanism"]
    need(mechanism["zero_utility_rule"]
         == "if the maximum utility is zero, choose the empty outcome",
         "zero-utility rule mismatch")
    need(mechanism["tie_rule"]
         == ("at positive maximum utility, retain the predecessor-selected "
             "outcome whenever it remains maximizing; otherwise choose the "
             "maximizing itemwise subset of that predecessor outcome with "
             "smallest outcome id under the predecessor's fixed outcome order"),
         "positive-utility tie rule mismatch")
    need(mechanism["ordered_rule"]
         == ("evaluate the hash-bound immediate predecessor first; if its first "
             "matching twenty-band row is S5.1 or S5.2, then apply the unique "
             "listed item row with t in (lower,upper]; otherwise retain the "
             "predecessor menu unchanged"), "top ordered rule mismatch")
    need(mechanism["shared_boundary_rule"]
         == ("the predecessor tests all twenty-band rows before bundle-pivot "
             "rows, so rho=c belongs to the S row (and its item surcharge when "
             "applicable); bundle-pivot positive-measure support has rho>c"),
         "rho=c boundary rule mismatch")

    immediate_ref = manifest["immediate_predecessor"]
    immediate_folder = bind(immediate_ref, (
        ("manifest.json", "manifest_sha256"),
        ("README.md", "readme_sha256"),
        ("verify_combined_surcharge.py", "verifier_sha256"),
        ("verification_output.txt", "verification_output_sha256"),
        ("independent_replay.py", "independent_replay_sha256"),
        ("independent_replay_output.txt", "independent_replay_output_sha256"),
        ("SHA256SUMS.txt", "sha256s_sha256"),
    ))
    common_ref = manifest["common_predecessor"]
    common_folder = bind(common_ref, (
        ("manifest.json", "manifest_sha256"),
        ("README.md", "readme_sha256"),
        ("verify_twenty_band_surcharge.py", "verifier_sha256"),
        ("verification_output.txt", "verification_output_sha256"),
        ("independent_replay.py", "independent_replay_sha256"),
        ("independent_replay_output.txt", "independent_replay_output_sha256"),
        ("SHA256SUMS.txt", "sha256s_sha256"),
    ))
    upper_ref = manifest["upper_reference"]
    upper_folder = bind(upper_ref, (
        ("manifest.json", "manifest_sha256"),
        ("README.md", "readme_sha256"),
        ("dual_polynomials.py", "dual_polynomials_sha256"),
        ("verify_stream_dual.py", "verifier_sha256"),
        ("verification_output.txt", "verification_output_sha256"),
        ("independent_replay.py", "independent_replay_sha256"),
        ("independent_replay_output.txt", "independent_replay_output_sha256"),
        ("SHA256SUMS.txt", "sha256s_sha256"),
    ))

    immediate = json.loads((immediate_folder / "manifest.json").read_text(encoding="utf-8"))
    common = json.loads((common_folder / "manifest.json").read_text(encoding="utf-8"))
    upper = json.loads((upper_folder / "manifest.json").read_text(encoding="utf-8"))
    need(Q(immediate["expected"]["final_expected_revenue"])
         == Q(immediate_ref["expected_revenue"]), "predecessor revenue mismatch")
    need(immediate["status"] == "SEALED" and common["status"] == "SEALED"
         and upper["expected"]["status"] == "SEALED",
         "a dependency is not sealed")
    need(immediate["predecessor_certificate"]["manifest_sha256"]
         == common_ref["manifest_sha256"], "common crosslink mismatch")
    need(immediate["upper_reference"]["manifest_sha256"]
         == upper_ref["manifest_sha256"], "upper crosslink mismatch")
    need(Q(upper["expected"]["promoted"]["upper_fraction"])
         == Q(upper_ref["expected_upper_bound"]), "upper value mismatch")

    item = mechanism["item_containment"]
    a, b, s = Q(159, 250), Q(91, 100), Q(1137, 1000)
    c, d = b - a, s - a
    need(Q(item["constants"]["c"]) == c
         and Q(item["constants"]["d"]) == d, "constant mismatch")
    need(item["low_interval"] == "0 <= rho <= 137/500",
         "item support mismatch")
    need(item["row_endpoint_rule"]
         == ("each listed high interval is (lower,upper]; no item surcharge "
             "is applied at t=139/200"), "item endpoint rule mismatch")
    need(immediate["mechanism"]["ordered_rule"]
         == ("test the predecessor twenty-band rows first, then the bundle-pivot "
             "extension rows in listed order; the first matching closed row "
             "supplies the fee; otherwise the fee is zero"),
         "predecessor priority mismatch")
    bundle = immediate["mechanism"]["bundle_pivot_extension"]
    need(Q(bundle["constants"]["c"]) == c, "bundle boundary mismatch")
    need(bundle["canonical_region"]
         == "91/100 <= u <= 1 and c <= rho <= u-d",
         "bundle canonical region mismatch")
    need(common["mechanism"]["chambers"]["singleton_pivot_rectangle"]
         == "0 <= rho <= b-a", "common S chamber mismatch")
    common_rows = {row["id"]: row for row in common["mechanism"]["rows"]}
    item_ids = [row["id"] for row in item["rows"]]
    need(len(item_ids) == 8 and len(set(item_ids)) == 8,
         "item row count or uniqueness mismatch")
    need(all(row["left_endpoint_open"] is True for row in item["rows"]),
         "left-endpoint convention mismatch")

    factor = Q(item["orientation_count"] * item["symmetric_bidder_count"])
    need(factor == 4, "symmetry factor mismatch")
    grouped = {}
    total = Q(0)
    reports = []
    for row in item["rows"]:
        parent = common_rows[row["parent"]]
        need(parent["chamber"] == "singleton_pivot_rectangle",
             f"non-S parent: {row['id']}")
        fee = Q(row["common_fee"])
        need(fee == Q(parent["fee"]), f"fee crosslink: {row['id']}")
        lower, upper_t = map(Q, row["high_interval"])
        parent_lower, parent_upper = map(Q, parent["high_interval"])
        need(parent_lower <= lower < upper_t <= parent_upper,
             f"row outside parent: {row['id']}")
        grouped.setdefault(row["parent"], []).append((lower, upper_t))
        delta = Q(row["item_surcharge"])
        slack = d - c + fee
        need(Q(0) < delta < slack, f"deletion margin: {row['id']}")

        # The sampled endpoints check all affine price inequalities over the
        # entire row. The analytic menu formula is then cubic in t, within
        # Boole's exactness range; the stronger degree-one test is diagnostic.
        def integrand(t):
            before = (d + fee, t + fee, t + c + fee)
            after = (before[0] + delta, before[1], before[2] + delta)
            check_prices(before, row["id"] + "/before")
            check_prices(after, row["id"] + "/after")
            return factor * c * (demand_revenue(after)
                                 - demand_revenue(before))

        gain = exact_boole(integrand, lower, upper_t, 1, row["id"])
        need(gain == Q(row["expected_gain"]),
             f"polygon gain mismatch: {row['id']}")
        total += gain
        reports.append((row["id"], gain))

    for parent_id, intervals in grouped.items():
        intervals.sort()
        parent_lower, parent_upper = map(Q, common_rows[parent_id]["high_interval"])
        need(intervals[0][0] == parent_lower
             and intervals[-1][1] == parent_upper,
             f"coverage endpoints: {parent_id}")
        need(all(left[1] == right[0]
                 for left, right in zip(intervals, intervals[1:])),
             f"coverage adjacency: {parent_id}")

    expected = manifest["expected"]
    need(total == Q(expected["item_containment_gain"]), "item total mismatch")
    predecessor = Q(immediate_ref["expected_revenue"])
    final = predecessor + total
    need(final == Q(expected["final_expected_revenue"]), "final mismatch")
    need(final - Q(common_ref["expected_revenue"])
         == Q(expected["combined_extension_gain_over_twenty_band"]),
         "combined extension mismatch")
    exact_upper = Q(upper_ref["expected_upper_bound"])
    need(exact_upper - final == Q(expected["remaining_exact_gap"]),
         "remaining gap mismatch")

    print("FINAL COMBINED NON-IMPORTING DEMAND-POLYGON REPLAY: PASS")
    print("implementation: exact rational polygon clipping and Boole quadrature; finite differences are consistency checks")
    print("sealed bundle predecessor, twenty-band predecessor, and upper hashes: PASS")
    print("deterministic tie rule, half-open item rows, and rho=c priority: PASS")
    for row_id, gain in reports:
        print(f"{row_id}: exact polygon gain={gain}")
    print(f"item-containment exact gain: {total}")
    print(f"predecessor exact revenue: {predecessor}")
    print(f"certified exact expected revenue: {final}")
    print(f"remaining exact gap to current upper: {exact_upper - final}")
    print("scope: independent eight-row gain replay with shared predecessor revenue; no global-optimality claim")


if __name__ == "__main__":
    try:
        main()
    except (OSError, KeyError, TypeError, ValueError, RuntimeError,
            json.JSONDecodeError) as error:
        print(f"FINAL COMBINED NON-IMPORTING DEMAND-POLYGON REPLAY: FAIL: {error}",
              file=sys.stderr)
        raise SystemExit(1)
