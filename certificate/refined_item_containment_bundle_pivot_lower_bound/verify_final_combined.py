#!/usr/bin/env python3
"""Exact symbolic verifier for the final combined primal lower bound."""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def verify_hashes(reference, entries):
    directory = (HERE / reference["directory"]).resolve()
    for filename, key in entries:
        require(digest(directory / filename) == reference[key],
                f"dependency hash mismatch: {directory.name}/{filename}")
    return directory


def trim(poly):
    values = list(poly)
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def add(left, right):
    size = max(len(left), len(right))
    return trim(tuple((left[k] if k < len(left) else Q(0))
                      + (right[k] if k < len(right) else Q(0))
                      for k in range(size)))


def subtract(left, right):
    size = max(len(left), len(right))
    return trim(tuple((left[k] if k < len(left) else Q(0))
                      - (right[k] if k < len(right) else Q(0))
                      for k in range(size)))


def multiply(left, right):
    answer = [Q(0)] * (len(left) + len(right) - 1)
    for i, first in enumerate(left):
        for j, second in enumerate(right):
            answer[i + j] += first * second
    return trim(tuple(answer))


def scale(poly, scalar):
    return trim(tuple(scalar * value for value in poly))


def evaluate(poly, point):
    result = Q(0)
    for coefficient in reversed(poly):
        result = result * point + coefficient
    return result


def integrate(poly, lower, upper):
    return sum(coefficient * (upper ** (degree + 1)
                              - lower ** (degree + 1)) / Q(degree + 1)
               for degree, coefficient in enumerate(poly))


ONE = (Q(1),)
T = (Q(0), Q(1))


def menu_revenue(a, b, c):
    """Expected payment of menu (0,A,B,C) in the checked price regime."""
    first = multiply(multiply(a, subtract(ONE, a)), subtract(c, a))
    second = multiply(multiply(b, subtract(ONE, b)), subtract(c, b))
    rectangle = multiply(add(subtract(ONE, c), b),
                         add(subtract(ONE, c), a))
    excess = subtract(add(a, b), c)
    triangle = scale(multiply(excess, excess), Q(1, 2))
    return add(add(first, second),
               multiply(c, subtract(rectangle, triangle)))


def check_regime(prices, lower, upper, label):
    for point in (lower, (lower + upper) / 2, upper):
        a, b, c = (evaluate(poly, point) for poly in prices)
        require(Q(0) <= a <= c <= 1, f"A/C price regime failed: {label}")
        require(Q(0) <= b <= c <= a + b,
                f"B/subadditivity regime failed: {label}")


def main():
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    require(manifest["scope"] == "primal_lower_bound_only", "wrong scope")
    require(manifest["status"] == "SEALED", "manifest is not sealed")
    require(manifest["mechanism"]["zero_utility_rule"]
            == "if the maximum utility is zero, choose the empty outcome",
            "zero-utility tie rule is not deterministic")
    require(manifest["mechanism"]["tie_rule"]
            == ("at positive maximum utility, retain the predecessor-selected "
                "outcome whenever it remains maximizing; otherwise choose the "
                "maximizing itemwise subset of that predecessor outcome with "
                "smallest outcome id under the predecessor's fixed outcome order"),
            "positive-utility tie rule is not deterministic")
    require(manifest["mechanism"]["ordered_rule"]
            == ("evaluate the hash-bound immediate predecessor first; if its first "
                "matching twenty-band row is S5.1 or S5.2, then apply the unique "
                "listed item row with t in (lower,upper]; otherwise retain the "
                "predecessor menu unchanged"),
            "top-level ordered rule mismatch")
    require(manifest["mechanism"]["shared_boundary_rule"]
            == ("the predecessor tests all twenty-band rows before bundle-pivot "
                "rows, so rho=c belongs to the S row (and its item surcharge when "
                "applicable); bundle-pivot positive-measure support has rho>c"),
            "rho=c boundary rule mismatch")

    immediate_ref = manifest["immediate_predecessor"]
    immediate_dir = verify_hashes(immediate_ref, (
        ("manifest.json", "manifest_sha256"),
        ("README.md", "readme_sha256"),
        ("verify_combined_surcharge.py", "verifier_sha256"),
        ("verification_output.txt", "verification_output_sha256"),
        ("independent_replay.py", "independent_replay_sha256"),
        ("independent_replay_output.txt", "independent_replay_output_sha256"),
        ("SHA256SUMS.txt", "sha256s_sha256"),
    ))
    common_ref = manifest["common_predecessor"]
    common_dir = verify_hashes(common_ref, (
        ("manifest.json", "manifest_sha256"),
        ("README.md", "readme_sha256"),
        ("verify_twenty_band_surcharge.py", "verifier_sha256"),
        ("verification_output.txt", "verification_output_sha256"),
        ("independent_replay.py", "independent_replay_sha256"),
        ("independent_replay_output.txt", "independent_replay_output_sha256"),
        ("SHA256SUMS.txt", "sha256s_sha256"),
    ))
    upper_ref = manifest["upper_reference"]
    upper_dir = verify_hashes(upper_ref, (
        ("manifest.json", "manifest_sha256"),
        ("README.md", "readme_sha256"),
        ("dual_polynomials.py", "dual_polynomials_sha256"),
        ("verify_stream_dual.py", "verifier_sha256"),
        ("verification_output.txt", "verification_output_sha256"),
        ("independent_replay.py", "independent_replay_sha256"),
        ("independent_replay_output.txt", "independent_replay_output_sha256"),
        ("SHA256SUMS.txt", "sha256s_sha256"),
    ))

    immediate = json.loads((immediate_dir / "manifest.json").read_text(encoding="utf-8"))
    common = json.loads((common_dir / "manifest.json").read_text(encoding="utf-8"))
    upper_manifest = json.loads((upper_dir / "manifest.json").read_text(encoding="utf-8"))
    require(immediate["status"] == "SEALED", "immediate predecessor is not sealed")
    require(common["status"] == "SEALED", "common predecessor is not sealed")
    require(upper_manifest["expected"]["status"] == "SEALED",
            "upper reference is not sealed")
    require(Q(immediate["expected"]["final_expected_revenue"])
            == Q(immediate_ref["expected_revenue"]),
            "immediate predecessor revenue mismatch")
    require(Q(common["expected"]["final_expected_revenue"])
            == Q(common_ref["expected_revenue"]),
            "common predecessor revenue mismatch")
    require(Q(upper_manifest["expected"]["promoted"]["upper_fraction"])
            == Q(upper_ref["expected_upper_bound"]),
            "upper-bound value mismatch")
    require(immediate["predecessor_certificate"]["manifest_sha256"]
            == common_ref["manifest_sha256"],
            "immediate/common predecessor crosslink mismatch")
    require(Q(immediate["predecessor_certificate"]["expected_revenue"])
            == Q(common_ref["expected_revenue"]),
            "immediate/common revenue crosslink mismatch")
    require(immediate["upper_reference"]["manifest_sha256"]
            == upper_ref["manifest_sha256"],
            "immediate/upper crosslink mismatch")

    item = manifest["mechanism"]["item_containment"]
    a, b, s = Q(159, 250), Q(91, 100), Q(1137, 1000)
    c, d = b - a, s - a
    require(Q(item["constants"]["c"]) == c
            and Q(item["constants"]["d"]) == d,
            "item constants mismatch")
    require(item["orientation_count"] * item["symmetric_bidder_count"] == 4,
            "wrong item symmetry factor")
    require(item["low_interval"] == "0 <= rho <= 137/500",
            "item low-coordinate support mismatch")
    require(item["row_endpoint_rule"]
            == ("each listed high interval is (lower,upper]; no item surcharge "
                "is applied at t=139/200"),
            "item endpoint rule mismatch")
    require(common["mechanism"]["chambers"]["singleton_pivot_rectangle"]
            == "0 <= rho <= b-a", "common S chamber mismatch")
    bundle = immediate["mechanism"]["bundle_pivot_extension"]
    require(Q(bundle["constants"]["c"]) == c,
            "bundle-pivot boundary mismatch")
    require(immediate["mechanism"]["ordered_rule"]
            == ("test the predecessor twenty-band rows first, then the "
                "bundle-pivot extension rows in listed order; the first matching "
                "closed row supplies the fee; otherwise the fee is zero"),
            "predecessor/bundle ordering mismatch")
    require(bundle["canonical_region"]
            == "91/100 <= u <= 1 and c <= rho <= u-d",
            "bundle-pivot canonical region mismatch")

    common_rows = {row["id"]: row for row in common["mechanism"]["rows"]}
    item_ids = [row["id"] for row in item["rows"]]
    require(len(item_ids) == 8 and len(set(item_ids)) == 8,
            "item row count or uniqueness mismatch")
    require(all(row["left_endpoint_open"] is True for row in item["rows"]),
            "item left-endpoint convention mismatch")
    require(set(row["parent"] for row in item["rows"])
            == {"S5.1", "S5.2"}, "unexpected item parents")
    grouped = {}
    item_gain = Q(0)
    reports = []
    factor = Q(item["orientation_count"] * item["symmetric_bidder_count"])
    for row in item["rows"]:
        parent = common_rows[row["parent"]]
        require(parent["chamber"] == "singleton_pivot_rectangle",
                f"non-S parent: {row['id']}")
        fee = Q(row["common_fee"])
        require(fee == Q(parent["fee"]), f"common-fee crosslink: {row['id']}")
        lower, upper = map(Q, row["high_interval"])
        parent_lower, parent_upper = map(Q, parent["high_interval"])
        require(parent_lower <= lower < upper <= parent_upper,
                f"row outside parent: {row['id']}")
        grouped.setdefault(row["parent"], []).append((lower, upper))

        delta = Q(row["item_surcharge"])
        slack = d - c + fee
        require(Q(0) < delta < slack,
                f"strict deletion margin failed: {row['id']}")
        before = ((d + fee,), add(T, (fee,)), add(T, (c + fee,)))
        after = ((d + fee + delta,), add(T, (fee,)),
                 add(T, (c + fee + delta,)))
        check_regime(before, lower, upper, row["id"] + "/before")
        check_regime(after, lower, upper, row["id"] + "/after")
        difference = subtract(menu_revenue(*after), menu_revenue(*before))
        require(len(difference) <= 2,
                f"item conditional gain is not affine: {row['id']}")
        gain = factor * c * integrate(difference, lower, upper)
        require(gain == Q(row["expected_gain"]),
                f"item exact gain mismatch: {row['id']}")
        item_gain += gain
        cap_margin = 1 - evaluate(after[2], upper)
        reports.append((row["id"], lower, upper, fee, delta,
                        slack - delta, cap_margin, gain))

    for parent_id, intervals in grouped.items():
        intervals.sort()
        parent_lower, parent_upper = map(Q, common_rows[parent_id]["high_interval"])
        require(intervals[0][0] == parent_lower
                and intervals[-1][1] == parent_upper,
                f"coverage endpoints failed: {parent_id}")
        require(all(left[1] == right[0]
                    for left, right in zip(intervals, intervals[1:])),
                f"coverage gap or overlap: {parent_id}")

    expected = manifest["expected"]
    require(item_gain == Q(expected["item_containment_gain"]),
            "item total mismatch")
    predecessor = Q(immediate_ref["expected_revenue"])
    final = predecessor + item_gain
    require(predecessor == Q(expected["predecessor_revenue"]),
            "expected predecessor mismatch")
    require(final == Q(expected["final_expected_revenue"]),
            "final expected revenue mismatch")
    require(final - predecessor
            == Q(expected["strict_improvement_over_predecessor"]),
            "strict improvement mismatch")
    require(final - Q(common_ref["expected_revenue"])
            == Q(expected["combined_extension_gain_over_twenty_band"]),
            "combined extension mismatch")
    current_upper = Q(upper_ref["expected_upper_bound"])
    require(current_upper == Q(expected["current_exact_upper"]),
            "expected upper mismatch")
    require(current_upper - final == Q(expected["remaining_exact_gap"]),
            "remaining gap mismatch")

    print("FINAL BUNDLE-PIVOT + ITEM-CONTAINMENT LOWER CERTIFICATE: PASS")
    print("sealed bundle predecessor, twenty-band predecessor, and upper hashes: PASS")
    print("deterministic zero/tie rules and rho=c predecessor priority: PASS")
    print("eight item rows, price regimes, deletion slack, and coverage: PASS")
    for values in reports:
        row_id, lower, upper, fee, delta, deletion_margin, cap_margin, gain = values
        print(f"{row_id}: t=({lower},{upper}], common={fee}, item={delta}, "
              f"deletion_margin={deletion_margin}, cap_margin={cap_margin}, gain={gain}")
    print(f"item-containment exact gain: {item_gain}")
    print(f"predecessor exact revenue: {predecessor}")
    print(f"certified exact expected revenue: {final}")
    print(f"strict improvement over predecessor: {final - predecessor}")
    print(f"remaining exact gap to current upper: {current_upper - final}")
    print("scope: exact deterministic DSIC/ex-post-IR primal lower bound; no optimality claim")


if __name__ == "__main__":
    try:
        main()
    except (OSError, KeyError, TypeError, ValueError, RuntimeError,
            json.JSONDecodeError) as error:
        print(f"FINAL BUNDLE-PIVOT + ITEM-CONTAINMENT LOWER CERTIFICATE: FAIL: {error}",
              file=sys.stderr)
        raise SystemExit(1)
