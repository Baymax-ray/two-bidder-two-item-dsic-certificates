# Verification record — V4.6.1 lower-bound branch

The final combined exact replay completed with **exit code 0** and
`V4_6_1_EXACT_REPLAY_PASS mathematical_replays=12`.
Its output is preserved in [final_replay.txt](research_log/final_replay.txt).

## Reproduce

From the auction package directory
`output/output/two_bidder_two_item_full_dsic_exact_auction`:

```powershell
python -B -X utf8 V4_6_1_lower_bound/verifier/run_all.py
python -B -X utf8 V4_6_1_lower_bound/verifier/verify_manifest.py
```

The default commands are read-only. Use Python 3.10 or newer, without
`-O`, `-OO`, or `PYTHONOPTIMIZE`. Exact replay requires only the Python
standard library and the preserved project proof/calculation modules.
The two floating discovery scripts are deliberately excluded from the
replay and are not evidence for the lower bound.

## Completed mathematical checks

| Check | Result and scope |
|---|---|
| Rebuilt candidate evaluator | 6,676 exact rational profile checks; all-real validity proved separately |
| Primary continuous revenue | Exact rational polygon integration and radical endpoint evaluation passed |
| Independent continuous revenue | Nine base cells have ordered area exactly 1/2; independently reconstructed coefficients agree exactly |
| Low-square gap replacement | 368 exact cases plus continuum area and support identities passed |
| Symmetrization and full one-bidder re-screening | Exact gap expression, fixed-residual description, and conditional support replay passed |
| Full-Q mirror experiment | Exact complete-menu gain over strongest V4.6 passed; not stacked with the selected construction |
| Independent rebuilt-menu interaction audit | 31,684 pairs from 178 types, including 1,796 positive-argmax tie profiles; source comparisons passed |
| Independent Q/Q and Q/base proof audit | Parameter hypotheses and pointwise compatibility checks passed |
| Functional exchange | Exact finite quadratic gain and neighboring negative derivative bound passed; 7,201 rational profiles checked |
| Independent functional revenue | Direct Q Jacobian expansion and base price-shift reconstruction agree on all four component coefficients |
| Independent functional pointwise/residual audit | 119,019 pairs at three epsilon values, 108 occupied traces, independent inverse interpolation, menus, and source comparisons passed |
| Consolidated branch ledger | Exact clean/final coefficients, strict V4.6 improvement, and certified Q/E area passed |

Counts in different rows overlap and are not a count of distinct profiles.
They are bounded implementation tests, **not** a replacement for the
all-real proofs. Pointwise DSIC follows from complete menu maximization;
the six region-pair arguments prove nonempty compatible maximizing sets
at all real profiles, including exceptional reports and ties. Borel
selection and bounded payments establish the required measurability and
integrability.

The primary and independent revenue calculators use different polynomial
representations and integration formulas. The independent clean calculator
imports no other project calculator; the independent functional calculator
uses that independent polynomial kernel, not the primary functional code.
Agreement is coefficientwise exact, not decimal agreement.

The Q/E screening statements reuse the predecessor's continuum capacity
support/slack identities after verifying their new hypotheses and actual
occupied traces. They cover arbitrary randomized conditional DSIC/IR
mechanisms. They do not supply a common global upper certificate for the
new joint allocation. See the independent
[rebuilt audit](research_log/gap_parameter_audit.md),
[Q audit](research_log/sym_parameter_q_audit.md), and
[functional audit](research_log/functional_gap_audit.md).

The final reader-facing claims received a separate
[report audit](research_log/final_report_audit.md).

## Baseline replay and preservation

The V4.6 baseline was freshly replayed during this branch, with exit code 0:
11 V4.6 mathematical replays, 14 inherited replays, and its 945-identity
preservation check passed. That output is preserved in
[baseline_replay.txt](research_log/baseline_replay.txt).
The final branch replay also verifies V4.6's complete 47-file manifest.

The starting outer manifest contained 993 identities. At the initial check,
all 993 live files matched. A concurrent branch subsequently changed the
outer CURRENT_PHASE.md and SHA256SUMS. The final preservation check therefore
verifies **992 unchanged live file identities plus the exact archived
starting CURRENT_PHASE.md identity**. It separately reports the current
navigation/outer-manifest mismatch; those files are not managed by this
lower-bound branch. No predecessor mathematical identity changed.

The starting manifest also omitted 433 pre-existing audit/upper-branch files.
They are explicitly outside this preservation claim. The initial whole-tree
inventory is a provenance snapshot, not a promise that concurrent branches
stay frozen. Details and digests are in
[baseline_identity.json](certificate/baseline_identity.json).

The branch has its own SHA256SUMS, with complete stable-file coverage checked
by the preserved common manifest validator. That check verifies identities,
safe paths, no links or reparse points, no case aliases, and no inventory
drift during verification. As in the parent package, the manifest itself,
Python caches, and designated generated TeX directories are excluded.
A matching hash establishes file identity; it does not independently prove
a mathematical claim.

## Result boundary

The proved result is a complete admissible mechanism with the exact revenue
in [REPORT.md](REPORT.md), and the corresponding strict lower-bound
improvement. Both bidders are fully conditionally optimal on Q and E for
the selected mechanism's actual residual capacity. The remaining base
region, the optimal outer allocation, and the unrestricted auction optimum
remain unresolved. Numerical discovery, one successful tent, and one
rejected tent do not establish family optimality or global stationarity.
