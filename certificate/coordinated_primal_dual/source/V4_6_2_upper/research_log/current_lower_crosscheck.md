# Bounded read-only cross-check of the concurrent lower branch

All five requested default replays passed with exit code 0. Commands used `python -B -X utf8`, without `--write` or optimization. The exact stdout is in [current_lower_crosscheck.txt](current_lower_crosscheck.txt). No command in this audit wrote to the lower branch or ran its full predecessor archive.

The inspected selected mechanism is `V4_6_1_lower_bound/verifier/functional_exchange.py:mechanism(profile)`. Its stored exact revenue is

\[
R=\frac{309078860435260513361}{367416000000000000000}
+\frac{31}{1215}\sqrt2-\frac{170368}{664453125}\sqrt{11},
\]

with enclosure
`[0.8764556138363258521461526, 0.8764556138363258521461527]`.
The functional increment over the rebuilt three-region mechanism is exactly
`68161978301/216000000000000000 > 0`.

## What was checked

- `parameter_revenue.py`: PASS, exact rebuilt revenue and rational base contribution.
- `independent_family_revenue.py`: PASS, independent continuum revenue reconstruction with nine base integration cells.
- `functional_exchange.py`: PASS, exact positive functional increment, sufficient-constraint margin, inverse-map identities, monotonicity, and 7201 pointwise profile checks.
- `independent_functional.py`: PASS, independent direct Q Jacobian expansion and reconstruction of base price-shift derivatives; all rational coefficients agree.
- `branch_summary.py`: PASS, selected exact revenue, enclosures, and comparison to the stored V4.6 construction revenue.

Read the full `parameter_rebuilt_family.md` and `functional_exchange.md` proofs, plus the complete menu/selection implementations in `parameter_candidate.py` and `functional_exchange.py` and the independent functional revenue code. No blocking inconsistency was found in this bounded source review.

The continuum validity argument is substantive: the three exhaustive menu regions Q, E, and affine base are defined at every report; the proof covers all region pairs and excludes item conflicts through explicit threshold inequalities. The joint tie rule first rejects zero utility, then chooses the first feasible pair among complete menu maximizers. The case proof supplies existence of that pair; no optimizer or missing selection oracle enters the mathematical definition.

For the tent deformation, the written proof uses an increasing, explicitly invertible h; adds the compatibility condition C >= k+h(rho) to Q; proves the changed discounted base menu contracts; and checks Q/Q, Q/base, E/Q, and E/base compatibility. Its exact positive slack 14/1875 > 1/1000 shows the extra maximum does not introduce an unaccounted revenue region for this particular tent. The paired menu changes, rather than pointwise virtual-value choices, are integrated in the accepted revenue formula.

Every fixed-opponent selected outcome remains a maximizer of a fixed complete menu, so the taxation argument is pointwise DSIC in expected utility. Empty provides IR at every report profile under the allocation-probability utility convention used by this project. Finite Borel region/argmax/feasibility predicates give a measurable complete rule; the per-item interval realization provides samplewise allocation feasibility. The code is an exact rational-report evaluator; the all-real extension is supplied by the displayed formulas and written proof, not by the 7201 checks.

## Limits of this cross-check

This is a bounded current-branch source/replay audit, not a new formal proof or full independent replay of every inherited dependency. The primary and independent revenue replays were actually run, but the rational profile checks do not establish all-real DSIC/IR or feasibility by enumeration; those rest on the inspected continuum arguments. The summary's stronger full conditional-screening claim on Q union E was not separately replayed in this request. Neither restricted-family nor unrestricted optimality is established. The global upper branch remains separately certified and does not depend on choosing this particular lower mechanism.
