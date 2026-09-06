# V4.6.2 verification record

The exact upper ledger certifies `OPT <= 882923053259/1000000000000` for the full continuous randomized DSIC/IR problem. This claim uses the written continuum arguments plus the exact arithmetic replays below. It is not a proof-assistant formalization and does not certify an optimal mechanism.

## Executed mathematics

| Check | Actual execution and scope |
|---|---|
| Primary continuous majorant | Full four-chart run through depth 20; 1,351,220 nodes, 475,257 unresolved leaves, 200,355 fixed-winner nodes; all five upper bounds and coverages saved. Approximately 206 seconds. |
| Independent continuous majorant | Separate full four-chart run, approximately 211 seconds; exactly the same five accumulators, coverages, node counts, and maximum directed error 157. The independent result pins the primary certificate's SHA-256. |
| Opponent-uniform sign | Exact Bernstein signs for both own radial charts, first at side 2/5, then at side 43/100. The latter uses nine leaves with maximum depth six. Simultaneous item symmetry covers both marginals. |
| Invalid larger sign square | Exact rational counterexample at own report (1/2,1/2), opponent (1,1/2), proving a virtual value above 1/40. |
| Conditional global support | Inherited constrained-screening and capacity-support identities replayed; new full polynomial integration and corrected radial-cell reduction replayed through n=1024. |
| Independent conditional audit | All averaged-field coefficients reconstructed by exact symbolic differentiation and tensor Boole integration; 20,968 exact menu-corner comparisons, 30 independent monomial cell integrals, and the crossing-cell regression. |
| Alternative lottery support | Exact polynomial identities and positive margins for line-to-volume price redistribution; the all-real convexity and support arguments are in the written proof. |
| Sparse long-range cycles | Exact polynomial reconstruction and strict whole-box comparisons before/after the correction, four symmetry images, all 28 box separations, and disjointness from side-43/100 replacement regions. |
| Independent cycle audit | Four independent numerator reconstructions, 16 strict whole-box inequalities, 256 rational endpoint checks, all separations, and the exact four-image gain. Endpoint checks supplement rather than replace the whole-box proof. |
| Lottery equality diagnostics | Inherited profile reconstruction plus all-real open-region derivation; separate exact subbox bound proves the final field is nonzero where matching requires zero. |
| Combined ledger | Same-stream dependency and amplitude checks, all sixteen strict rational decreases, directed decimal endpoint, unchanged lower enclosure, and remaining-gap enclosure. |

The full primary and independent integrations were performed separately during this phase. The final aggregate invocation used `--skip-deep`: it reran the other exact checks and explicitly did **not** rerun either deep tree. Its output is [final_replay.txt](research_log/final_replay.txt). This distinction is intentional; saved hashes alone would not establish a fresh deep replay.

The independent majorant imports the canonical archive's independent polynomial builder and midpoint subdivision. It imports neither this phase's primary majorant implementation nor the archive's primary `verify_stream_dual.py`. It implements its own common-degree conversion, directed errors, coefficientwise maximum, traversal, and accumulators. Both implementations still depend on Python, NumPy's bounded integer operations, the stated exact coefficient data, and the written analytic identity.

The conditional classifier initially accepted some total-value-above-price cells crossing the singleton/bundle threshold. Root review found this error before release. The criterion now requires both relevant lower bounds, and every subtraction in the final ledger was recomputed. The superseded larger subtraction is not a certificate used in this release. See [independent_conditional_audit.md](research_log/independent_conditional_audit.md).

The cross-branch update additionally executed five read-only V4.6.1 checks: primary and independent rebuilt revenue, the functional exchange, independent functional revenue, and branch summary. All passed. Actual command output and the bounded complete-mechanism proof review are in [current_lower_crosscheck.md](research_log/current_lower_crosscheck.md). The 7201 rational profile checks supplement its continuum proof. A new exact comparison independently encloses both square roots and the combined gap. The new current_lower_flatness.py proves strict all-real lottery selection on a separate box, checks 17 source profiles, excludes both branches' functional modifications, and certifies a negative safe field there. Its generation and normal replay passed. These are separate additions; the original full-depth upper integration was unchanged.

## Commands and execution boundary

From `output/output/two_bidder_two_item_full_dsic_exact_auction`:

```powershell
python -B -X utf8 V4_6_2_upper/verifier/run_all.py
python -B -X utf8 V4_6_2_upper/verifier/verify_manifest.py
```

The first command includes both complete deep integrations. Add `--skip-deep` only to request the shorter, explicitly labeled replay. Default mathematical verifiers are read-only; certificate creation requires their explicit `--write` option. Assertion-based verifiers reject optimized Python; the independent integration's `-O` rejection was also checked. Do not run with `python -O`.

The canonical 32 stream coefficients are in
`research/closed/two-bidder-two-item-dsic-certificates/certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound/manifest.json`.
Its SHA-256 is
`65040d3569530e81c2c026a351c6b9fab84c4f556ebe95425ec6abf433d287a4`.
Primary and independent certificates record their further code dependencies. The final endpoint uses a new verified continuous integration, not the old numerical upper as an unexamined premise. The old upper is used for historical comparison and an earlier entry in the ledger.

Floating amplitude and cycle searches are retained as discovery records. Their solver values do not enter the theorem. Rationalized witnesses enter only after separate exact continuous checks. There is no finite type-grid implementation or finite-menu completeness assumption in this upper-bound proof.

The frozen ledger takes its lower endpoint from the existing V4.6 exact revenue certificate. This branch rechecked the conditional identities and allocation profiles needed by the upper argument, but did not rerun the entire V4.6 lower-mechanism package. A separate current_bound_comparison.py verifies the stronger parallel V4.6.1 revenue expression and the current combined gap by exact rational and integer-square-root arithmetic. Its result is separate from the unchanged upper ledger; lower-feasibility and revenue cross-checks are recorded in research_log/current_lower_crosscheck.md. Final read-only review by the three participating mathematical branches found no blocking issue in the combined proof, corrected support subtraction, endpoint arithmetic, and stated flow scope.

## Preservation and manifests

Before this branch, the outer manifest listed 993 identities; all matched at the initial check. Another 383 files already existed under `V4_6_archive_audit` but were absent from that manifest. Therefore the initial complete-coverage check failed, although every listed identity passed. Both original inventories and the original navigation bytes were saved in this branch's `certificate` directory before work.

At final comparison, all **993 originally listed identities remain unchanged**, using the saved original navigation bytes for `CURRENT_PHASE.md`. Of the 383 initially unlisted archive-audit files, 376 are unchanged and seven changed during the run: `validate_release.py`, the compiled manuscript PDF, its main build log, and four pass logs. Their before/after hashes and observed modification times are in [predecessor_final_comparison.json](certificate/predecessor_final_comparison.json). This branch's commands and agents did not run that archive's LaTeX build or reproducer; the originating writer has not been independently identified. The current files were left in place. We do **not** claim preservation of all 1,376 observed identities.

The first aggregate replay exited on that strict preservation comparison after all mathematical checks had passed. The comparison utility now separately requires the 993 research identities to be unchanged and the seven observed archive changes to match the explicit drift record. It prints both counts. `preserve_previous.py --strict` retains the all-files-unchanged condition and therefore reports these seven differences. The replay was then repeated with this explicitly bounded preservation check.

Only the outer phase-navigation file and outer manifest are updated for this release, in addition to new files inside `V4_6_2_upper`. The old navigation and manifest remain saved. Files from the parallel V4.6.1 lower branch and further archive QA also appeared after the initial inventory. They were not created by this upper branch. The final outer manifest includes those files and the pre-existing archive-audit material at their current observed identities; inclusion does not claim that its results were rerun or reviewed here. The branch manifest and the outer stable-file manifest check safe paths, complete coverage, and file identity, excluding only the verifier's documented build/cache paths.

Hashes establish identity and coverage. They do not replace the mathematical replays or establish the truth of unrelated archive claims.
