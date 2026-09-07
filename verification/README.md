# Reproducing the current revenue bracket

The final mechanism uses `tau=83/10000`. The authoritative mathematical record
is [reserve_parameter/manifest.json](../certificate/reserve_parameter/manifest.json),
with revenue in `[0.876514341027067549900397423113,
0.876514355424052828335888359874]`, unrestricted upper below
`0.882351585488796576205586892264`, gap below `0.005837245`, and a guarantee
strictly above **99.3384%** of unrestricted randomized DSIC optimal revenue.
The exact revenue is the manuscript's sixteen-face integral, not an endpoint
of its numerical enclosure. The unrestricted optimum and a matching mechanism
remain open.

## Entry points

From the publication-package root, use Python 3.10 or newer with NumPy.

```
python -E -s -B -X utf8 verification/reproduce_all.py
```

The default runs both mathematics and release consistency. `--checks math`
runs the mathematical dependency chain; `--checks release` checks the current
text and manifests, builds a clean temporary PDF and checks full SHA-256
coverage. In the default mode, text and TeX preflight precede long mathematics.
Optional transcripts must be placed under `verification/generated/`, which
is temporary and excluded from the release manifest.

The mathematical chain retains the base and intermediate exact certificates,
the coordinated component's 46 explicit entrypoints, the portable upper and
face-moment component's thirteen replays plus exact assembly, and the final
reserve arithmetic and rational-report implementation checks. Old directory
names identify dependencies, not the current headline. In particular,
`certificate/v5_primal_dual/verify_v5.py` reports the intermediate `tau=1/100`
lower alongside the still-current upper. Continue through the final reserve
checker to obtain the paper's selected mechanism and final revenue enclosure.

The original research workspace is unnecessary. Portable wrappers stage the
frozen inputs in disposable directories and check their hashes before and
after replay. `source_bindings.json` distinguishes mathematical inputs,
independent checks, source/accounting provenance and unused candidates.
Retained nonexecuted candidates do not establish any deduction in the final upper.

## Scope and trust

The seed revenue has independent full reconstructions. The stream majorant
has two complete implementations. The conditional subtraction has one full
1024-partition accumulation, independent coefficient reconstruction and bounded
cross-checks. The shared-cell master system has a separate complete replay.
The opposing-excess tree has a full directed-arithmetic replay and bounded
independent cross-checks, not a second complete independently implemented tree.
See the manuscript's reproducibility section for the precise independence levels.

Runtime identity and actual imported module paths are emitted during the portable
replay. Child Python processes ignore ambient Python overrides and user-site
imports; installed interpreter and library code remain trusted. Proof kernels
use assertions. `-O`, `-OO` and nonzero `PYTHONOPTIMIZE` are unsupported and
explicitly rejected at the entrypoints. Path and environment regression checks
are in `test_portable_runner.py`.

`joint_explanation_check.py` preserves the separate rational polygon and fee
identity check formerly stored with internal review notes. The three current
mathematical packages already contain their independent source checks; duplicate
audit copies and historical reviewer snapshots are not runtime dependencies.

## Release files

`make_hashes.py` writes the root manifest and `verify_hashes.py` requires exact
stable-file coverage. The current build, runtime and replay receipts in this
directory are verification evidence. `reproduction_all.txt` records the full
reader-copy run; `reproduction_release.txt` records the final-directory checks. Hash agreement establishes identity,
not mathematical validity. The all-report proofs remain in the manuscript
and the included analytic sources.

`tools/build_paper.py` and `tools/render_paper.py` retain the configured local
TinyTeX and Poppler build/QA helpers. They write temporary material beneath
`generated/`; the portable publication runner supports the environment described
in [ENVIRONMENT.md](../ENVIRONMENT.md). Old review reports and transient authoring
outputs are not part of the reader-facing reproduction chain.
