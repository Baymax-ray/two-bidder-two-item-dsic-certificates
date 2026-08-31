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
UPPER = Fraction(3715139591287203, 4194304000000000)
LOWER = Fraction(83962078694672281756033, 96000000000000000000000)
TEN_BAND_LOWER = Fraction(26237753173862063, 30000000000000000)
TWENTY_BAND_LOWER = Fraction(2623779309282875420759, 3000000000000000000000)
BUNDLE_PIVOT_LOWER = Fraction(83961603016753854879913, 96000000000000000000000)
AI_DECLARATION = "This manuscript was completed with the assistance of OpenAI GPT-5.6 Sol."
AUTHOR_EMAIL = "baymin@bu.edu"
AUTHOR_ORCID = "0009-0006-9100-0445"


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
        "active bundle-pivot plus item-containment lower certificate",
        [python, "-B", "-X", "utf8", "-I", "verify_final_combined.py"],
        final_lower,
        recorder,
    )
    require("FINAL BUNDLE-PIVOT + ITEM-CONTAINMENT LOWER CERTIFICATE: PASS" in output
            and str(LOWER) in output,
            "active lower verifier did not report the release endpoint")

    output = run_checked(
        "independent active lower replay",
        [python, "-B", "-X", "utf8", "-I", "independent_replay.py"],
        final_lower,
        recorder,
    )
    require("FINAL COMBINED NON-IMPORTING DEMAND-POLYGON REPLAY: PASS" in output
            and str(LOWER) in output,
            "independent active lower replay did not report the release endpoint")

    output = run_checked(
        "formal nonuniform upper certificate",
        [python, "-B", "verify_stream_dual.py"],
        stream,
        recorder,
    )
    require('"status": "PASS"' in output and str(UPPER) in output,
            "formal upper replay did not report the release endpoint")

    output = run_checked(
        "independent nonuniform upper replay",
        [python, "-B", "independent_replay.py"],
        stream,
        recorder,
    )
    require('"status": "PASS"' in output and str(UPPER) in output,
            "independent full replay did not report the release endpoint")
    require('"coverage_units": 33554432' in output,
            "independent full coverage mismatch")


def check_text_consistency(recorder: Recorder) -> None:
    manuscript = (ROOT / "manuscript" / "manuscript.tex").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    upper_manifest = json.loads(
        (ROOT / "certificate" / "continuous_stream_degree4_two_level_nonuniform_upper_bound" / "manifest.json")
        .read_text(encoding="utf-8")
    )
    lower_manifest = json.loads(
        (ROOT / "certificate" / "refined_item_containment_bundle_pivot_lower_bound" / "manifest.json")
        .read_text(encoding="utf-8")
    )
    require(Fraction(upper_manifest["expected"]["promoted"]["upper_fraction"]) == UPPER,
            "upper manifest differs from release theorem")
    require(Fraction(lower_manifest["expected"]["final_expected_revenue"]) == LOWER,
            "lower manifest differs from release theorem")
    for text, label in ((manuscript, "manuscript"), (readme, "README")):
        require("3715139591287203" in text and "4194304000000000" in text,
                f"upper endpoint missing from {label}")
        require("83962078694672281756033" in text
                and "96000000000000000000000" in text,
                f"lower endpoint missing from {label}")
        require("34262987107793868572569" in text
                and "3072000000000000000000000" in text,
                f"remaining exact gap missing from {label}")
        require(text.count(AI_DECLARATION) == 1,
                f"AI declaration must occur exactly once in {label}")
        require(AUTHOR_EMAIL in text and AUTHOR_ORCID in text,
                f"author metadata missing from {label}")
    require("certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound" in readme,
            "active upper certificate path missing from README")
    require("certificate/refined_item_containment_bundle_pivot_lower_bound" in readme,
            "active lower certificate path missing from README")
    require("1445765276937161827" not in manuscript
            and "1445765276937161827" not in readme,
            "superseded exact gap remains active in publication text")
    require("0.8919" in manuscript and "0.876" in manuscript,
            "external benchmark values missing from manuscript")
    recorder.say("PASS theorem, README, manifest, and declaration consistency")


def compile_manuscript(recorder: Recorder) -> None:
    pdflatex = shutil.which("pdflatex")
    bibtex = shutil.which("bibtex")
    require(pdflatex is not None, "pdflatex is required")
    require(bibtex is not None, "bibtex is required")
    source = ROOT / "manuscript"
    with tempfile.TemporaryDirectory(prefix="dsic-preprint-") as temporary:
        build = Path(temporary)
        shutil.copy2(source / "manuscript.tex", build / "manuscript.tex")
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
        run_checked("LaTeX pass 3", latex, build, recorder)
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
            f"lower={LOWER} upper={UPPER} formal=PASS independent=PASS "
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
