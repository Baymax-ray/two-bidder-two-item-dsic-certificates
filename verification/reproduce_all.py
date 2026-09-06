#!/usr/bin/env python3
"""Run every publication-facing certificate and a clean manuscript build."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY_UPPER = Fraction(3715139591287203, 4194304000000000)
ACTIVE_MANIFEST = json.loads((ROOT / "certificate/coordinated_primal_dual/manifest.json").read_text(encoding="utf-8"))
UPPER = Fraction(ACTIVE_MANIFEST["upper"])
LOWER = Fraction(83962078694672281756033, 96000000000000000000000)
TEN_BAND_LOWER = Fraction(26237753173862063, 30000000000000000)
TWENTY_BAND_LOWER = Fraction(2623779309282875420759, 3000000000000000000000)
BUNDLE_PIVOT_LOWER = Fraction(83961603016753854879913, 96000000000000000000000)
JOINT_FLOOR = Fraction(437909927074211227673, 500000000000000000000)
LOWER_FLOOR = Fraction(ACTIVE_MANIFEST["lower_enclosure"][0])
AI_DECLARATION = "This manuscript was developed with the assistance of OpenAI GPT-5.6 Sol and OpenAI Codex."
AUTHOR_EMAIL = "baymin@bu.edu"
AUTHOR_ORCID = "0009-0006-9100-0445"
REPOSITORY_URL = "https://github.com/Baymax-ray/two-bidder-two-item-dsic-certificates"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


class Recorder:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def say(self, message: str) -> None:
        self.lines.append(message)
        print(message, flush=True)

    def write(self, path: Path) -> None:
        allowed = (ROOT / "verification" / "generated").resolve()
        resolved = path.resolve()
        require(allowed == resolved.parent or allowed in resolved.parents,
                "transcript path must be under verification/generated")
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text("\n".join(self.lines) + "\n", encoding="utf-8", newline="\n")


def run_checked(label: str, command: list[str], cwd: Path, recorder: Recorder) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"{label} failed with exit code {completed.returncode}\n{completed.stdout}"
        )
    recorder.say(f"PASS {label}")
    return completed.stdout


def check_certificates(recorder: Recorder) -> None:
    python = sys.executable
    ama = ROOT / "certificate" / "ama_lower_bound"
    predecessor_surcharge = ROOT / "certificate" / "menu_surcharge_lower_bound"
    surcharge = ROOT / "certificate" / "piecewise_surcharge_lower_bound"
    twenty_band = ROOT / "certificate" / "piecewise_surcharge_twenty_band_lower_bound"
    bundle_pivot = ROOT / "certificate" / "piecewise_surcharge_bundle_pivot_lower_bound"
    final_lower = ROOT / "certificate" / "refined_item_containment_bundle_pivot_lower_bound"
    stream = ROOT / "certificate" / "continuous_stream_degree4_two_level_nonuniform_upper_bound"

    output = run_checked(
        "exact base lower certificate",
        [python, "-B", "verify_ama.py"],
        ama,
        recorder,
    )
    require(str(Fraction(26232089810531183, 30000000000000000)) in output,
            "base lower endpoint missing from verifier output")

    output = run_checked(
        "predecessor surcharge lower certificate",
        [python, "-B", "verify_surcharge.py"],
        predecessor_surcharge,
        recorder,
    )
    require("26232788323031183/30000000000000000" in output,
            "predecessor lower endpoint missing from verifier output")

    output = run_checked(
        "active piecewise-surcharge lower certificate",
        [python, "-B", "verify_piecewise_surcharge.py"],
        surcharge,
        recorder,
    )
    require("PIECEWISE-SURCHARGE LOWER-BOUND CERTIFICATE: PASS" in output
            and str(TEN_BAND_LOWER) in output,
            "ten-band lower verifier did not report its sealed endpoint")

    output = run_checked(
        "independent piecewise-surcharge replay",
        [python, "-B", "independent_replay.py"],
        surcharge,
        recorder,
    )
    require("INDEPENDENT PIECEWISE-SURCHARGE REPLAY: PASS" in output
            and str(TEN_BAND_LOWER) in output,
            "independent ten-band replay did not report its sealed endpoint")

    output = run_checked(
        "twenty-band lower certificate",
        [python, "-B", "-X", "utf8", "verify_twenty_band_surcharge.py"],
        twenty_band,
        recorder,
    )
    require("TWENTY-BAND RATIONAL SURCHARGE LOWER CERTIFICATE: PASS" in output
            and str(TWENTY_BAND_LOWER) in output,
            "twenty-band lower verifier did not report its sealed endpoint")

    output = run_checked(
        "independent twenty-band lower replay",
        [python, "-B", "-X", "utf8", "independent_replay.py"],
        twenty_band,
        recorder,
    )
    require("INDEPENDENT TWENTY-BAND LOWER-CERTIFICATE REPLAY: PASS" in output
            and str(TWENTY_BAND_LOWER) in output,
            "independent twenty-band replay did not report its sealed endpoint")

    output = run_checked(
        "bundle-pivot lower certificate",
        [python, "-B", "-X", "utf8", "verify_combined_surcharge.py"],
        bundle_pivot,
        recorder,
    )
    require("COMBINED TWENTY-BAND + BUNDLE-PIVOT LOWER CERTIFICATE: PASS" in output
            and str(BUNDLE_PIVOT_LOWER) in output,
            "bundle-pivot lower verifier did not report its sealed endpoint")

    output = run_checked(
        "independent bundle-pivot lower replay",
        [python, "-B", "-X", "utf8", "independent_replay.py"],
        bundle_pivot,
        recorder,
    )
    require("INDEPENDENT COMBINED SURCHARGE LOWER-CERTIFICATE REPLAY: PASS" in output
            and str(BUNDLE_PIVOT_LOWER) in output,
            "independent bundle-pivot replay did not report its sealed endpoint")

    output = run_checked(
        "retained deterministic item-containment lower certificate",
        [python, "-B", "-X", "utf8", "-I", "verify_final_combined.py"],
        final_lower,
        recorder,
    )
    require("FINAL BUNDLE-PIVOT + ITEM-CONTAINMENT LOWER CERTIFICATE: PASS" in output
            and str(LOWER) in output,
            "active lower verifier did not report the release endpoint")

    output = run_checked(
        "independent retained deterministic lower replay",
        [python, "-B", "-X", "utf8", "-I", "independent_replay.py"],
        final_lower,
        recorder,
    )
    require("FINAL COMBINED NON-IMPORTING DEMAND-POLYGON REPLAY: PASS" in output
            and str(LOWER) in output,
            "independent active lower replay did not report the release endpoint")

    joint = ROOT / "certificate" / "joint_residual_screening_lower_bound"
    output = run_checked(
        "active joint residual-screening lower certificate and fresh audits",
        [python, "-B", "-X", "utf8", "verify_joint_residual.py"],
        joint,
        recorder,
    )
    require("JOINT_RESIDUAL_SCREENING_CERTIFICATE_PASS" in output
            and str(JOINT_FLOOR) in output
            and "STRICT_GAP_LT_1_100_PASS" in output,
            "joint lower verifier did not certify the release enclosure")

    output = run_checked(
        "post-review independent joint revenue explanation",
        [python, "-B", "-X", "utf8", "joint_explanation_check.py"],
        ROOT / "audit" / "nature_review_v46",
        recorder,
    )
    require("JOINT_EXPLANATION_INDEPENDENT_EXACT_PASS" in output,
            "post-review revenue derivation failed")

    paired = ROOT / "certificate/coordinated_primal_dual"
    output = run_checked(
        "active coordinated primal-dual certificate and both full upper traversals",
        [python, "-B", "-X", "utf8", "verify_coordinated.py"], paired, recorder)
    require("COORDINATED_PRIMAL_DUAL_CERTIFICATE_PASS 46" in output
            and str(UPPER) in output and "STRICT_GAP_LT_1_100_PASS" in output,
            "active coordinated replay did not certify current endpoints")


def check_text_consistency(recorder: Recorder) -> None:
    manuscript = "\n".join(p.read_text(encoding="utf-8")
                           for p in sorted((ROOT / "manuscript").glob("*.tex")))
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    upper_manifest = json.loads(
        (ROOT / "certificate" / "continuous_stream_degree4_two_level_nonuniform_upper_bound" / "manifest.json")
        .read_text(encoding="utf-8")
    )
    lower_manifest = json.loads(
        (ROOT / "certificate" / "refined_item_containment_bundle_pivot_lower_bound" / "manifest.json")
        .read_text(encoding="utf-8")
    )
    require(Fraction(upper_manifest["expected"]["promoted"]["upper_fraction"]) == LEGACY_UPPER,
            "historical upper manifest mismatch")
    require(Fraction(lower_manifest["expected"]["final_expected_revenue"]) == LOWER,
            "lower manifest differs from release theorem")
    joint_manifest = json.loads(
        (ROOT / "certificate" / "joint_residual_screening_lower_bound" / "manifest.json")
        .read_text(encoding="utf-8")
    )
    require(Fraction(joint_manifest["lower_floor"]) == JOINT_FLOOR,
            "historical joint lower floor mismatch")
    require(Fraction(joint_manifest["upper"]) == LEGACY_UPPER,
            "joint manifest upper differs from release theorem")
    require(UPPER - LOWER_FLOOR < Fraction(1, 100),
            "exact endpoints do not certify a gap below 0.01")
    require(LOWER_FLOOR / UPPER > Fraction(992684, 1000000),
            "exact endpoints do not certify the stated 99.2684% guarantee")
    for text, label in ((manuscript, "manuscript"), (readme, "README")):
        require("99.2684" in text,
                f"certified revenue guarantee missing from {label}")
        require("3715139591287203" in text and "4194304000000000" in text,
                f"upper endpoint missing from {label}")
        require("83962078694672281756033" in text
                and "96000000000000000000000" in text,
                f"lower endpoint missing from {label}")
        require("0.876464164471798049944906113027" in text
                and "0.876464164471798049944906113028" in text,
                f"new exact revenue enclosure missing from {label}")
        require("0.006458888786918919315720686828" in text,
                f"remaining gap enclosure missing from {label}")
        require(text.count(AI_DECLARATION) == 1,
                f"AI declaration must occur exactly once in {label}")
        require("The author retains responsibility" in text
                and "numerical search outputs were not treated as proofs" in text,
                f"expanded AI-use scope and responsibility missing from {label}")
        require(REPOSITORY_URL in text,
                f"public repository URL missing from {label}")
        require(AUTHOR_EMAIL in text and AUTHOR_ORCID in text,
                f"author metadata missing from {label}")
    require("certificate/coordinated_primal_dual" in readme,
            "active upper certificate path missing from README")
    require("certificate/joint_residual_screening_lower_bound" in readme,
            "active lower certificate path missing from README")
    require("1445765276937161827" not in manuscript
            and "1445765276937161827" not in readme,
            "superseded exact gap remains active in publication text")
    require("0.8919" in manuscript and "0.876" in manuscript,
            "external benchmark values missing from manuscript")
    run_checked("immutable self-review evidence packet",
                [sys.executable, "-B", "audit/nature_review_v46/verify_review_snapshot.py"],
                ROOT, recorder)
    run_checked("immutable coordinated self-review evidence packet",
                [sys.executable, "-B", "audit/nature_review_v4611_v462/verify_review_snapshot.py"],
                ROOT, recorder)
    active = json.loads((ROOT / "certificate/coordinated_primal_dual/manifest.json").read_text(encoding="utf-8"))
    require(active == ACTIVE_MANIFEST, "active manifest changed during replay")
    require(active["revenue_coefficients"][0].split("/")[0] in manuscript,
            "active algebraic revenue missing from manuscript")
    recorder.say("PASS theorem, README, manifest, and declaration consistency")


def compile_manuscript(recorder: Recorder) -> None:
    pdflatex = shutil.which("pdflatex")
    bibtex = shutil.which("bibtex")
    require(pdflatex is not None, "pdflatex is required")
    require(bibtex is not None, "bibtex is required")
    source = ROOT / "manuscript"
    with tempfile.TemporaryDirectory(prefix="dsic-preprint-") as temporary:
        build = Path(temporary)
        for tex in source.glob("*.tex"):
            shutil.copy2(tex, build / tex.name)
        shutil.copy2(source / "references.bib", build / "references.bib")
        latex = [
            pdflatex,
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            "manuscript.tex",
        ]
        run_checked("LaTeX pass 1", latex, build, recorder)
        run_checked("BibTeX", [bibtex, "manuscript"], build, recorder)
        run_checked("LaTeX pass 2", latex, build, recorder)
        final_output = run_checked("LaTeX pass 3", latex, build, recorder)
        if "Label(s) may have changed" in final_output:
            final_output = run_checked("LaTeX cross-reference pass", latex, build, recorder)
        require("Label(s) may have changed" not in final_output
                and "undefined references" not in final_output,
                "manuscript references did not stabilize")
        pdf = build / "manuscript.pdf"
        require(pdf.is_file() and pdf.stat().st_size > 10_000,
                "clean manuscript PDF was not produced")
    recorder.say("PASS clean temporary-directory manuscript compilation")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transcript", type=Path)
    arguments = parser.parse_args()
    recorder = Recorder()
    try:
        require(sys.version_info >= (3, 10), "Python 3.10 or newer is required")
        require(sys.flags.optimize == 0, "optimized Python mode is not supported")
        check_certificates(recorder)
        check_text_consistency(recorder)
        compile_manuscript(recorder)
        run_checked(
            "root SHA-256 manifest",
            [sys.executable, "-B", "verification/verify_hashes.py"],
            ROOT,
            recorder,
        )
        recorder.say(
            "PUBLICATION_REPRODUCTION_PASS "
            f"lower_floor={LOWER_FLOOR} upper={UPPER} formal=PASS independent=PASS "
            "paper=compiled hashes=verified"
        )
        if arguments.transcript is not None:
            recorder.write(arguments.transcript)
        return 0
    except (OSError, RuntimeError) as error:
        recorder.say(f"PUBLICATION_REPRODUCTION_FAILED {error}")
        if arguments.transcript is not None:
            recorder.write(arguments.transcript)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
