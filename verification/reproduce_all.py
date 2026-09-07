#!/usr/bin/env python3
"""Run every publication-facing certificate and a clean manuscript build."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY_UPPER = Fraction(3715139591287203, 4194304000000000)
PREDECESSOR_MANIFEST = json.loads((ROOT / "certificate/coordinated_primal_dual/manifest.json").read_text(encoding="utf-8"))
PREDECESSOR_UPPER = Fraction(PREDECESSOR_MANIFEST["upper"])
V5_PACKAGE = ROOT / "certificate/v5_primal_dual"
V5_MANIFEST = json.loads((V5_PACKAGE / "manifest.json").read_text(encoding="utf-8"))
RESERVE_PACKAGE = ROOT / "certificate/reserve_parameter"
ACTIVE_MANIFEST = json.loads((RESERVE_PACKAGE / "manifest.json").read_text(encoding="utf-8"))
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
    environment={key:value for key,value in os.environ.items()
                 if not key.upper().startswith("PYTHON")}
    environment["PYTHONNOUSERSITE"]="1"
    if Path(command[0]).resolve()==Path(sys.executable).resolve():
        command=[command[0], "-E", "-s", *command[1:]]
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
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
        "historical piecewise-surcharge lower certificate",
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
            "retained deterministic lower verifier did not report its endpoint")

    output = run_checked(
        "independent retained deterministic lower replay",
        [python, "-B", "-X", "utf8", "-I", "independent_replay.py"],
        final_lower,
        recorder,
    )
    require("FINAL COMBINED NON-IMPORTING DEMAND-POLYGON REPLAY: PASS" in output
            and str(LOWER) in output,
            "independent retained deterministic replay did not report its endpoint")

    joint = ROOT / "certificate" / "joint_residual_screening_lower_bound"
    output = run_checked(
        "historical joint residual-screening lower certificate and fresh audits",
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
        ROOT / "verification",
        recorder,
    )
    require("JOINT_EXPLANATION_INDEPENDENT_EXACT_PASS" in output,
            "post-review revenue derivation failed")

    paired = ROOT / "certificate/coordinated_primal_dual"
    output = run_checked(
        "predecessor coordinated primal-dual certificate and both full upper traversals",
        [python, "-B", "-X", "utf8", "verify_coordinated.py"], paired, recorder)
    require("COORDINATED_PRIMAL_DUAL_CERTIFICATE_PASS 46" in output
            and str(PREDECESSOR_UPPER) in output and "STRICT_GAP_LT_1_100_PASS" in output,
            "coordinated replay did not certify its predecessor endpoints")

    output = run_checked(
        "inherited full upper and intermediate reserve component at tau=1/100",
        [python, "-B", "-X", "utf8", "verify_v5.py"], V5_PACKAGE, recorder)
    require("V5_PORTABLE_CERTIFICATE_PASS" in output and str(UPPER) in output,
            "portable V5 replay did not certify the active exact upper endpoint")

    for line in output.splitlines():
        if line.startswith(("RUNTIME_IDENTITY ", "COMPONENT_SCOPE ")):
            recorder.say(line)

    output = run_checked(
        "selected reserve parameter and exact family certificate",
        [python, "-B", "-X", "utf8", "verify_reserve.py"], RESERVE_PACKAGE, recorder)
    require("EXACT_RESERVE_PARAMETER_CERTIFICATE_PASS" in output,
            "reserve parameter certificate failed")
    output = run_checked(
        "rational reserve implementation boundary checks",
        [python, "-B", "-X", "utf8", "check_implementation.py"], RESERVE_PACKAGE, recorder)
    require("RESERVE_IMPLEMENTATION_CHECK_PASS" in output,
            "reserve implementation checks failed")


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
            "historical deterministic lower manifest mismatch")
    joint_manifest = json.loads(
        (ROOT / "certificate" / "joint_residual_screening_lower_bound" / "manifest.json")
        .read_text(encoding="utf-8")
    )
    require(Fraction(joint_manifest["lower_floor"]) == JOINT_FLOOR,
            "historical joint lower floor mismatch")
    require(Fraction(joint_manifest["upper"]) == LEGACY_UPPER,
            "historical joint upper manifest mismatch")
    require(UPPER - LOWER_FLOOR < Fraction(1, 100),
            "exact endpoints do not certify a gap below 0.01")
    require(Fraction(ACTIVE_MANIFEST["guarantee"]) == Fraction(993384, 1000000)
            and LOWER_FLOOR / UPPER > Fraction(993384, 1000000),
            "exact endpoints do not certify the stated 99.3384% guarantee")
    v5_sources = V5_PACKAGE / "source"
    phase = json.loads((v5_sources / "V5_gap_closure/certificate/phase_ledger.json")
                       .read_text(encoding="utf-8"))
    component_sources = {
        "numerical_remainder_lower": ("V4_6_3_slack_atlas/certificate/numerical_remainder.json", "total_E", "lower"),
        "master_gain_lower": ("V4_8A_frozen_primal/certificate/master_certificate.json", "exact_total_gain_lower"),
        "splice_gain_lower": ("V5_gap_closure/certificate/global_duality.json", "global_gain_lower"),
        "BB_gain": ("V5_gap_closure/certificate/bb_global.json", "exact_upper_decrease"),
    }
    components = {key: Fraction(value) for key, value in ACTIVE_MANIFEST["upper_components"].items()}
    require(set(components) == {"predecessor_upper", *component_sources},
            "V5 upper assembly has missing or unexpected components")
    require(components["predecessor_upper"] == PREDECESSOR_UPPER,
            "V5 upper assembly does not start from the coordinated predecessor")
    for key, (relative, *fields) in component_sources.items():
        value = json.loads((v5_sources / relative).read_text(encoding="utf-8"))
        for field in fields:
            value = value[field]
        require(components[key] == Fraction(value), f"V5 assembly source mismatch: {key}")
    require(UPPER == components["predecessor_upper"]
            - sum((components[key] for key in component_sources), Fraction())
            == Fraction(phase["new_exact_upper"]),
            "V5 exact upper assembly differs from the accepted certificate")
    exact_lower = Fraction(ACTIVE_MANIFEST["revenue_enclosure"][0])
    exact_higher = Fraction(ACTIVE_MANIFEST["revenue_enclosure"][1])
    require(LOWER_FLOOR <= exact_lower <= exact_higher
            <= Fraction(ACTIVE_MANIFEST["lower_enclosure"][1]) < UPPER,
            "V5 manifest revenue enclosure does not contain the exact certificate")
    require(Fraction(ACTIVE_MANIFEST["upper_enclosure"][0]) <= UPPER
            <= Fraction(ACTIVE_MANIFEST["upper_enclosure"][1]),
            "V5 displayed upper enclosure is not outward rounded")
    require(Fraction(ACTIVE_MANIFEST["gap_enclosure"][0]) <= UPPER - exact_higher
            <= UPPER - exact_lower <= Fraction(ACTIVE_MANIFEST["gap_enclosure"][1]),
            "V5 displayed gap enclosure is not outward rounded")
    for text, label in ((manuscript, "manuscript"), (readme, "README")):
        require("99.3384" in text,
                f"certified revenue guarantee missing from {label}")
        require(all(endpoint in text for endpoint in ACTIVE_MANIFEST["lower_enclosure"]),
                f"active V5 revenue enclosure missing from {label}")
        require(ACTIVE_MANIFEST["upper_enclosure"][1] in text,
                f"active V5 upper endpoint missing from {label}")
        require(all(endpoint in text for endpoint in ACTIVE_MANIFEST["gap_enclosure"]),
                f"active V5 gap enclosure missing from {label}")
        require("open" in text.lower() and "matching" in text.lower(),
                f"open optimum and matching-certificate scope missing from {label}")
        require(text.count(AI_DECLARATION) == 1,
                f"AI declaration must occur exactly once in {label}")
        require("The author retains responsibility" in text
                and "numerical search outputs were not treated as proofs" in text,
                f"expanded AI-use scope and responsibility missing from {label}")
        require(REPOSITORY_URL in text,
                f"public repository URL missing from {label}")
        require(AUTHOR_EMAIL in text and AUTHOR_ORCID in text,
                f"author metadata missing from {label}")
    require("certificate/v5_primal_dual" in readme,
            "active V5 certificate path missing from README")
    require("certificate/coordinated_primal_dual" in readme,
            "coordinated dependency path missing from README")
    require("certificate/joint_residual_screening_lower_bound" in readme,
            "joint dependency path missing from README")
    require("1445765276937161827" not in manuscript
            and "1445765276937161827" not in readme,
            "superseded exact gap remains active in publication text")
    require("0.8919" in manuscript and "0.876" in manuscript,
            "external benchmark values missing from manuscript")
    predecessor = json.loads((ROOT / "certificate/coordinated_primal_dual/manifest.json").read_text(encoding="utf-8"))
    require(predecessor == PREDECESSOR_MANIFEST, "predecessor manifest changed during replay")
    active = json.loads((RESERVE_PACKAGE / "manifest.json").read_text(encoding="utf-8"))
    require(active == ACTIVE_MANIFEST, "active manifest changed during replay")
    require(predecessor["revenue_coefficients"][0].split("/")[0] in manuscript,
            "retained predecessor algebraic revenue missing from manuscript")
    import re
    labels = re.findall(r"\\label\{([^}]+)\}", manuscript)
    references = re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", manuscript)
    require(len(labels) == len(set(labels)), "duplicate manuscript label")
    require(set(references) <= set(labels),
            "unresolved manuscript reference: " + str(sorted(set(references)-set(labels))))
    require(not re.search(r"\bV[345](?:[._]\d+)*\b|historical|predecessor", manuscript),
            "development chronology remains in manuscript")
    require(all(r"\label{" + name + "}" in manuscript for name in
                ("app:compatibility", "app:stream", "app:integration")),
            "final proof appendix missing")
    from hashlib import sha256
    require(sha256((RESERVE_PACKAGE / "manifest.json").read_bytes()).hexdigest()
            in manuscript.replace("\\\\", "").replace("\n", ""),
            "final parameter manifest identity missing from manuscript")
    guide=(ROOT / "verification/README.md").read_text(encoding="utf-8")
    require("99.3384%" in guide and "83/10000" in guide
            and "99.2684" not in guide and "active coordinated" not in guide,
            "verification guide does not identify the final result")
    recorder.say("PASS theorem, README, manifest, and declaration consistency")


def compile_manuscript(recorder: Recorder) -> None:
    pdflatex = shutil.which("pdflatex")
    bibtex = shutil.which("bibtex")
    tectonic = shutil.which("tectonic")
    require((pdflatex is not None and bibtex is not None) or tectonic is not None,
            "pdflatex and bibtex, or tectonic, must be available on PATH")
    source = ROOT / "manuscript"
    with tempfile.TemporaryDirectory(prefix="dsic-preprint-") as temporary:
        build = Path(temporary)
        for tex in source.glob("*.tex"):
            shutil.copy2(tex, build / tex.name)
        shutil.copy2(source / "references.bib", build / "references.bib")
        if pdflatex is not None and bibtex is not None:
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
        else:
            run_checked("Tectonic manuscript build",
                        [tectonic, "--keep-logs", "--keep-intermediates",
                         "--outdir", str(build), "manuscript.tex"], build, recorder)
            final_output = (build / "manuscript.log").read_text(encoding="utf-8", errors="replace")
        require("Label(s) may have changed" not in final_output
                and "undefined references" not in final_output
                and "undefined citations" not in final_output,
                "manuscript references did not stabilize")
        pdf = build / "manuscript.pdf"
        require(pdf.is_file() and pdf.stat().st_size > 10_000,
                "clean manuscript PDF was not produced")
    recorder.say("PASS clean temporary-directory manuscript compilation")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transcript", type=Path)
    parser.add_argument("--checks", choices=("all", "math", "release"), default="all",
                        help="Separate mathematical replay from release consistency")
    arguments = parser.parse_args()
    recorder = Recorder()
    try:
        require(sys.version_info >= (3, 10), "Python 3.10 or newer is required")
        require(sys.flags.optimize == 0, "optimized Python mode is not supported")
        if arguments.checks in ("all", "math"):
            run_checked("portable-runner path and import-isolation tests",
                        [sys.executable, "-B", "-X", "utf8",
                         "verification/test_portable_runner.py"], ROOT, recorder)
        if arguments.checks in ("all", "release"):
            recorder.say("RELEASE_PREFLIGHT_START")
            check_text_consistency(recorder)
            compile_manuscript(recorder)
        if arguments.checks in ("all", "math"):
            recorder.say("MATHEMATICAL_REPLAY_START")
            check_certificates(recorder)
            recorder.say("MATHEMATICAL_REPRODUCTION_PASS")
        if arguments.checks in ("all", "release"):
            run_checked("root SHA-256 manifest",
                        [sys.executable, "-B", "verification/verify_hashes.py"],
                        ROOT, recorder)
            recorder.say("RELEASE_CONSISTENCY_PASS")
        if arguments.checks == "all":
            recorder.say("PUBLICATION_REPRODUCTION_PASS "
                         f"lower_floor={LOWER_FLOOR} upper={UPPER} "
                         "mathematics=PASS release=PASS")
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
