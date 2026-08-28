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
UPPER = Fraction(18588262788621, 20971520000000)
LOWER = Fraction(26237753173862063, 30000000000000000)
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
    stream = ROOT / "certificate" / "continuous_stream_degree4_nonuniform_upper_bound"

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
            and str(LOWER) in output,
            "active lower verifier did not report the release endpoint")

    output = run_checked(
        "independent piecewise-surcharge replay",
        [python, "-B", "independent_replay.py"],
        surcharge,
        recorder,
    )
    require("INDEPENDENT PIECEWISE-SURCHARGE REPLAY: PASS" in output
            and str(LOWER) in output,
            "independent lower replay did not report the release endpoint")

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
    require('"coverage_units": 16777216' in output,
            "independent full coverage mismatch")


def check_text_consistency(recorder: Recorder) -> None:
    manuscript = (ROOT / "manuscript" / "manuscript.tex").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    upper_manifest = json.loads(
        (ROOT / "certificate" / "continuous_stream_degree4_nonuniform_upper_bound" / "manifest.json")
        .read_text(encoding="utf-8")
    )
    lower_manifest = json.loads(
        (ROOT / "certificate" / "piecewise_surcharge_lower_bound" / "manifest.json")
        .read_text(encoding="utf-8")
    )
    require(Fraction(upper_manifest["expected"]["upper_bound"]) == UPPER,
            "upper manifest differs from release theorem")
    require(Fraction(lower_manifest["expected"]["final_expected_revenue"]) == LOWER,
            "lower manifest differs from release theorem")
    for text, label in ((manuscript, "manuscript"), (readme, "README")):
        require("18588262788621" in text and "20971520000000" in text,
                f"upper endpoint missing from {label}")
        require("26237753173862063" in text and "30000000000000000" in text,
                f"lower endpoint missing from {label}")
        require(text.count(AI_DECLARATION) == 1,
                f"AI declaration must occur exactly once in {label}")
        require(AUTHOR_EMAIL in text and AUTHOR_ORCID in text,
                f"author metadata missing from {label}")
    require("0.88722066443341350555419921875" not in manuscript,
            "superseded active upper decimal remains in manuscript")
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
