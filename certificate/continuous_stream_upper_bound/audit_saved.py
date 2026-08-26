"""Fast fail-closed audit of frozen outputs; does not rerun the traversal."""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

import numpy as np
import adaptive_certify as cert

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    candidate = HERE / manifest["candidate_file"]
    require(digest(candidate) == manifest["candidate_sha256"],
            "candidate hash mismatch")
    report = json.loads((HERE / "proof_transcript_s1000000000.json").read_text(
        encoding="utf-8"))
    expected = manifest["expected"]
    stats = report["statistics"]
    actual = {
        "maximum_initial_absolute_control": report["maximum_initial_absolute_control"],
        "accumulator": report["accumulator"],
        "upper_fraction": report["upper_fraction"],
        "base_fixed": stats["base_fixed"],
        "base_unresolved": stats["base_unresolved"],
        "base_refined": stats["base_refined"],
        "base_held": stats["base_held"],
        "adaptive_splits": stats["adaptive_splits"],
        "adaptive_axis_counts": stats["adaptive_axis_counts"],
        "gain_units": stats["gain_units"],
    }
    require(actual == expected, "saved expected fields mismatch")
    denominator = manifest["fixed_point_scale"] * (1 << report["common_final_depth"])
    upper = Q(2 * int(report["accumulator"]), denominator)
    require(upper == Q(report["upper_fraction"]), "saved upper mismatch")
    require(upper < Q(manifest["target"]), "saved target comparison failed")
    replay_expected = manifest["precision_replay"]
    replay = json.loads((HERE / "proof_transcript_s100000000.json").read_text(
        encoding="utf-8"))
    require(replay["scale"] == replay_expected["fixed_point_scale"],
            "sensitivity scale mismatch")
    require(replay["accumulator"] == replay_expected["accumulator"],
            "sensitivity accumulator mismatch")
    require(replay["upper_fraction"] == replay_expected["upper_fraction"],
            "sensitivity upper mismatch")
    require(Q(replay["upper_fraction"]) < Q(manifest["target"]),
            "sensitivity target comparison failed")
    arithmetic = manifest["arithmetic_audit"]
    theta, basis, _ = cert.load_frozen()
    max_degree = root_max = 0
    for c1 in range(2):
        for c2 in range(2):
            first, second = cert.higher.competitors(theta, basis, c1, c2)
            difference = cert.dp.add(first, cert.dp.scale(second, -1))
            for polynomial in (first, second, difference):
                degrees = tuple(max((e[j] for e in polynomial), default=0)
                                for j in range(4))
                max_degree = max(max_degree, *degrees)
                controls = cert.verify.fixed_controls(polynomial,
                                                       manifest["fixed_point_scale"])
                root_max = max(root_max, abs(int(controls.min())),
                               abs(int(controls.max())))
    radius = 1 + 21 * max_degree
    pair_bound = 2 * root_max
    require(max_degree == arithmetic["maximum_axis_degree"], "degree bound mismatch")
    require(radius == arithmetic["maximum_error_units_at_common_depth_21"],
            "error-radius mismatch")
    require(root_max == arithmetic["maximum_initial_absolute_control"],
            "root control bound mismatch")
    require(root_max + radius == arithmetic["maximum_stored_absolute_control_plus_error"],
            "stored control-plus-error bound mismatch")
    require(pair_bound == arithmetic["maximum_int64_pair_sum_or_difference"],
            "pairwise-operation bound mismatch")
    require(pair_bound < np.iinfo(np.int64).max, "int64 pairwise bound exceeded")
    require(type(int(report["accumulator"])) is int,
            "accumulator is not a Python integer")
    require("runtime_seconds" not in report and "runtime_seconds" not in replay,
            "runtime leaked into deterministic transcript")
    for name in ("adaptive_certify.py", "degree4_polynomials.py",
                 "dual_polynomials.py", "fixed_bernstein.py"):
        source = (HERE / name).read_text(encoding="utf-8")
        require("output/" not in source and "scratch/" not in source,
                f"non-self-contained path in {name}")
    result = {
        "status": "PASS_SAVED_AUDIT",
        "candidate_sha256": digest(candidate),
        "upper_fraction": str(upper),
        "target": manifest["target"],
        "strict_margin": str(Q(manifest["target"]) - upper),
        "precision_replay_upper": replay["upper_fraction"],
        "self_contained_source_check": True,
        "int64_and_error_bounds_check": True
    }
    text = json.dumps(result, indent=2)
    (HERE / "saved_audit_output.json").write_text(text, encoding="utf-8")
    (HERE / "saved_audit_output.txt").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
