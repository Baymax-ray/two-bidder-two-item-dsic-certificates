"""Fail-closed manifest verifier for the adaptive degree-4 certificate."""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

import adaptive_certify as cert
import numpy as np

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
    partition = manifest["partition"]
    require(partition["adaptive_extra_depth"] == 1,
            "unsupported adaptive depth")
    theta, basis, _ = cert.load_frozen()
    max_degree = 0
    root_max = 0
    for c1 in range(2):
        for c2 in range(2):
            first, second = cert.higher.competitors(theta, basis, c1, c2)
            difference = cert.dp.add(first, cert.dp.scale(second, -1))
            for polynomial in (first, second, difference):
                degrees = tuple(max((e[j] for e in polynomial), default=0)
                                for j in range(4))
                max_degree = max(max_degree, *degrees)
                controls = cert.verify.fixed_controls(
                    polynomial, manifest["fixed_point_scale"])
                root_max = max(root_max, abs(int(controls.min())),
                               abs(int(controls.max())))
    arithmetic = manifest["arithmetic_audit"]
    radius = arithmetic["initial_rounding_error_units"] + (
        partition["base_depth"] + partition["adaptive_extra_depth"]
    ) * max_degree
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
    report = cert.run(
        partition["base_depth"], partition["adaptive_extra_depth"],
        manifest["fixed_point_scale"], write_outputs=False, emit=False,
        include_runtime=False)
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
    require(actual == expected, f"certificate mismatch: {actual} != {expected}")
    require("runtime_seconds" not in report, "runtime leaked into proof transcript")
    require(type(int(report["accumulator"])) is int,
            "accumulator is not a Python integer")
    upper = Q(report["accumulator"]) * 2 / (
        manifest["fixed_point_scale"] * (1 << report["common_final_depth"])
    )
    require(upper == Q(report["upper_fraction"]), "upper fraction mismatch")
    require(upper < Q(manifest["target"]), "target comparison failed")
    replay = manifest["precision_replay"]
    replay_report = json.loads((HERE / "proof_transcript_s100000000.json").read_text(
        encoding="utf-8"))
    require(replay_report["scale"] == replay["fixed_point_scale"],
            "sensitivity scale mismatch")
    require(replay_report["accumulator"] == replay["accumulator"],
            "sensitivity accumulator mismatch")
    require(replay_report["upper_fraction"] == replay["upper_fraction"],
            "sensitivity upper mismatch")
    require(Q(replay_report["upper_fraction"]) < Q(manifest["target"]),
            "sensitivity target comparison failed")
    verification = {
        "status": "PASS",
        "candidate_sha256": digest(candidate),
        "accumulator": report["accumulator"],
        "upper_fraction": str(upper),
        "target": manifest["target"],
        "strict_margin": str(Q(manifest["target"]) - upper),
        "precision_replay_upper": replay["upper_fraction"]
    }
    text = json.dumps(verification, indent=2)
    print(text)


if __name__ == "__main__":
    main()
