# Independent final report and claim-scope audit

Audit date: 2026-09-06. Audited documents: `REPORT.md`, `README.md`,
`certificate/branch_summary.json`, and `research_log/conditional_gap_map.md`.
The replay log and final branch manifest are issued separately by the root
verifier; this note does not certify files that had not yet been generated.

**Verdict: the mathematical headline, mechanism scope, and comparison narrative
are consistent with the branch evidence. One live-preservation defect was found
and corrected explicitly, as described below. No auction-optimality claim is
justified or made.**

## 1. Exact strongest mechanism and revenue

The final selected evaluator is `verifier/functional_exchange.py`, at the
specified epsilon=1/1000 and tent support [.32,.33,.34]. The three-region
`parameter_candidate.py` is its exact predecessor, not a second additive
improvement to be counted elsewhere. The headline coefficients are

309078860435260513361/367416000000000000000,
31/1215, and -170368/664453125

in the basis (1,sqrt(2),sqrt(11)). Their enclosure and gain over the full
V4.6 baseline match `branch_summary.py`, freshly replayed read-only during
this audit. The displayed lower and upper endpoints are outward bounds, not
floating optimizer values. I also independently checked with `Fraction` that
its rational coefficient equals the clean mechanism's coefficient plus
68161978301/216000000000000000, and that all three final coefficients match
`independent_functional.json` exactly. The independent base partition contains
exactly the nine positive-area cells claimed in the report.

The low-square, symmetrization, and full-Q-mirror trials are explicitly treated
as alternative mechanisms. The report correctly adds only the functional
increment to the selected clean three-region candidate. Its fixed-baseline
mirror comparison subtracts the old corner correction before adding its own
Q menu revenue difference. No overlapping gain is stacked twice.

## 2. Complete pointwise mechanism and tie rule

The report states the clean Q, E, and remaining base menus, every constant,
the continuous tent, its inverse image knots, both coordinated price changes,
and the complete joint tie rule. These agree with the two published evaluators.
The inverse formulas agree at the tent endpoints and middle image knot. Q is
closed; E is open in the two stated inequalities; all other reports use the
base rule. Zero utility selects empty. Otherwise a finite lexicographic search
selects a jointly feasible pair among full menu maximizers.

Existence of that pair is supported by the all-real Q-Q/Q-base audit and the
independent E/base and E/E arguments, then by the functional audit. Crucially,
the safe/bundle surcharge uses the actual discounted-tariff contraction lemma;
the report does not infer contraction merely from nonnegative price changes.
The extra maximum is uniformly slack by the exact 14/1875 bound, so the revenue
calculation does not omit a newly binding region. The proof uses the complete
menu and all tied alternatives, not a discretized allocation table.

The DSIC statement is correctly pointwise in every own true report, deviation,
and opponent report, in expected utility. Any feasible maximizing-pair choice
still attains the same complete conditional menu value. Empty gives IR, the
finite Borel formulas give measurability, and per-item disjoint intervals realize
feasible allocation marginals. No universal-truthfulness claim is made.

## 3. Conditional versus global claims

The exact old low-square gap entries have a feasible replacement and an actual
fixed-residual diagonal support. The strongest-baseline symmetrization experiment
literally holds bidder 2 pointwise fixed and fully optimizes bidder 1 on G.
The report correctly observes that its optimizer avoids the intermediate
one-half-capacity set, so this is not evidence for essential randomization.
The coordinated full-Q mirror is not mislabeled as a baseline fixed-residual
inner gap on every Q fiber; both sides' exceptional tie selections can change.

For the selected clean and functional mechanisms, the claimed zero inner gap
on both bidders' Q and E fibers is supported by the new parameter hypotheses
and actual occupied traces. In particular, the functional Q top trace has
price max(1/2,h(x))<t for x<h^{-1}(t); reopened Q bottom and vertical anchors
remain in unchanged free-Q rows. E's junction has low coordinate c outside the
tent support, and its changed top prices are below A<t. Candidate feasibility
therefore allows the inherited full randomized conditional supports to saturate.
Their competitors are unrestricted randomized DSIC/IR conditional mechanisms,
not just the displayed menus or finite grids.

The report's area 62101/135000 is the two-dimensional opponent-region area
|Q union E|. It is explicitly not interpreted as a fraction of four-dimensional
profiles or as a percentage of the global optimum. The remaining base fibers
and all outer optimality questions remain unresolved. Neither parameter-family
optimality nor a matching global upper certificate is claimed. Finite rational
profile checks are consistently identified as implementation evidence additional
to the written continuum inequalities and exact integrals.

## 4. Preservation defect found and resolved

A fresh replay of the originally written `preserve_baseline.py` failed at the
live outer `CURRENT_PHASE.md`. Independent hashing of all 993 saved manifest
records found **992 unchanged live files and only CURRENT_PHASE.md changed**.
Its original digest exactly matches the branch's archived
`certificate/pre_V4_6_1_CURRENT_PHASE.md`. The outer SHA256SUMS also differs
from the starting snapshot. These changes occurred concurrently outside this
branch's ownership; this lower branch did not write either outer file.

With root authorization, I changed only the branch's `preserve_baseline.py`
and `certificate/baseline_identity.json`: 992 identities are checked against
their current original paths, and the original navigation identity is checked
against its saved snapshot. Live navigation and outer-manifest drift are
reported separately. The earlier all-993-live success remains explicitly
historical, rather than being relabeled as a current result.

The corrected read-only replay passed with the precise output:

V4_6_1_BASELINE_PRESERVATION_PASS 992 unchanged live identities + 1 matching archived navigation identity
live_navigation_matches_start_snapshot False
outer_manifest_matches_start_snapshot False

Consequently a final verification summary must use that qualified preservation
statement. It must not claim that all 993 original live paths are unchanged.
The audited REPORT and README already avoid that false numeric statement and
correctly describe branch-only manifest ownership. Hash preservation verifies
file identities, not a new execution of a predecessor upper-bound proof.

## Audit execution boundary

Fresh commands: `branch_summary.py` and the corrected `preserve_baseline.py`.
Additional independent checks: all 993 starting-record hashes, archived navigation
digest equality, exact coefficient addition, final coefficient identity, and
independent base-cell count. Written proofs reviewed: the low-square and symmetry
notes, rebuilt parameter region proof and independent Q audit, functional exchange
proof, and functional residual-gap audit. The full branch runner and final manifest
verification are separate, later execution records; their counts are not invented
or anticipated in this audit.
