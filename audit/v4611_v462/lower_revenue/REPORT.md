# Fresh independent revenue audit: V4.6.1.1 and V4.6.2 pairing

Date: 2026-09-06. Scope: exact continuous revenue and cross-branch arithmetic. This is a technical audit, not a Nature-style referee report.

**Verdict: no blocking revenue or arithmetic defect found.** The selected V4.6.1.1 mechanism has the stated exact revenue. Its gain over the frozen V4.6.1 value is strictly greater than 17/2000000. Paired with the exact V4.6.2 upper endpoint, the certified interval width is below 0.01. The structural validity of the complete mechanism and the unrestricted validity of the upper certificate require the separate structural and upper audits; this report does not replace them.

## Exact result

The third reconstruction returns, coefficient by coefficient,

\[
R=\frac{35791404252341621852527735747861637}
{42525000000000000000000000000000000}
+\frac{31}{1215}\sqrt2
-\frac{15059524650320123}{8305664062500000000000}\sqrt{493894}.
\]

Strict rational radical enclosures give

\[
0.876464164471798049944906113027<R<
0.876464164471798049944906113028.
\]

The exact V4.6.2 ledger endpoint is reconciled independently as its depth-20 anchor minus its frozen conditional-support subtraction minus 81/10^10. Thus

\[
0.006458888786918919315720686827<U_{4.6.2}-R<
0.006458888786918919315720686828<0.01.
\]

Moreover,

\[
0.992684652685100617902519468374<R/U_{4.6.2}<
0.992684652685100617902519468375.
\]

Provided the separate primal and upper proofs hold, this proves the mechanism obtains **more than 99.2684% of unrestricted optimal revenue**. This percentage uses R/U, not an estimate of OPT. The displayed gap is the width of a certified enclosing interval; it is not a claim that OPT equals the upper endpoint or that the mechanism's actual regret equals that width.

The gain over V4.6.1 lies strictly between
0.000008550635472197798753464735 and
0.000008550635472197798753464736. The V4.6.2 report's comparison to V4.6.1 is a historical cross-branch comparison; promotion of V4.6.1.1 must use the new width above.

## Fresh independent reconstruction

[third_revenue_and_pairing.py](third_revenue_and_pairing.py) imports only the Python standard library. It does not import either selected source calculator, the inherited polynomial helpers, or the candidate implementation. It constructs the exact parameters and continuum integrals before reading the frozen coefficients for comparison. Its default invocation is read-only; `--write` creates the adjacent audit JSON.

The reconstruction uses its own rational bivariate polynomial class, its own affine clipping, and **vertical slicing** of polygons. On each interval between consecutive vertex abscissae, it integrates between the two affine boundary edges. This differs from the source root's simplex moments and the source auditor's Green boundary method.

The following components were independently reconstructed:

1. The entire ordered opponent triangle for the unmodified base menu. Generic pivot comparisons, the two minimum-price switches, and the singleton-price-one boundaries produce nine positive-area polygons. Their areas sum exactly to 1/2. Relevant proper-menu topology inequalities are checked on every polygon vertex. The integrated base revenue is exactly 33016262254015350834722212412993/37968750000000000000000000000000; the factor four counts both bidders and both item orientations.
2. The constrained Q menu, including its complete inverse plateau, sloped inverse segment, unchanged segment, bundle-price clipping and safe-price cap. The code checks the uncapped quadratic identity and the cap identity as exact bivariate polynomial equalities. The positive-length opponent interval mapped to k=c is integrated explicitly; it is not discarded as an inverse-coordinate null set.
3. Free Q with its algebraic bundle floor. The low-square sum density and the sqrt(2) endpoint are integrated in an exact quadratic field.
4. The E lottery gain and the negative E/base correction on A<t<a. The latter is explicitly checked to be negative; omitting it would overstate revenue.
5. Both base-fee strips. The ordinary bundle-pivot strips and the extra zero-pivot strip caused by a>A are integrated directly over freshly clipped two-dimensional polygons. Polynomial identities verify the full safe-plus-bundle price change, including the high-singleton-unaffordable topology, instead of treating a virtual-value derivative as the finite change.

The resulting three radical coefficients agree exactly with both frozen computations, using sqrt(246947/1125000)=sqrt(493894)/1500. Twenty-seven freshly constructed own-type menu polygon integrations also pass: 19 E lottery fibers and eight Q cap/no-cap fibers. These finite checks support the derived identities; the continuum calculation is not a type-grid estimate.

Tie-breaking does not modify the revenue integral: different options have different allocation vectors, and their affine utility ties have zero own-type area for each nondegenerate conditional menu. Exceptional opponent faces also have zero opponent area. This observation concerns the integral only. The independent structural proof must still justify DSIC, IR, joint feasibility and the complete tie rule on every report.

## Fresh replay results and source anchors

All three selected read-only source replays returned exit code zero:

- `V4_6_1_1_lower_bound/verifier/refined_revenue.py` (`verify`, line 16): `REFINED_EXACT_CONTINUUM_REVENUE_PASS`.
- `V4_6_1_1_lower_bound/verifier/refined_revenue_audit.py` (`calculate`, line 103): `REFINED_CONTINUOUS_REVENUE_AUDIT_PASS`; 45 source-auditor conditional polygon checks.
- `V4_6_1_1_lower_bound/verifier/branch_summary.py`: `V4_6_1_1_LOWER_BOUND_CERTIFIED`; coefficient and parameter reconciliation.

[fresh_replay_record.json](fresh_replay_record.json) records commands, return codes, Python version, source hashes and before/after equality for the original Python inventory. Adjacent `*_fresh.txt` files capture output. [third_revenue_run.json](third_revenue_run.json) seals the fresh checker source and its read-only run. [third_revenue_and_pairing.json](third_revenue_and_pairing.json) contains exact component values, bound comparisons and input identities.

The source derivation reviewed is `V4_6_1_1_lower_bound/research_log/refined_revenue_audit.md`: constants at line 27; extra C-bound redundancy at line 63; complete base partition at line 94; cap at line 135; inverse plateau at line 174; negative E correction at line 230; extra base strip at line 251; final coefficient identity at line 295. The source root's independent variation assembly is `verifier/constant_kernel.py`, `clean` at line 26 and `affine_gain` at line 85.

## Independence and claim boundaries

This is a new computational reconstruction of the stated mathematical decomposition, not a proof-assistant formalization or an independent foundational derivation of the auction model. The small polynomials and screening identities were inspected mathematically, then encoded separately. Trusted execution includes Python's exact integers and `fractions.Fraction`; integer-square-root brackets and all comparison directions are explicitly checked. There is no optimizer, floating quadrature, numerical tolerance, or search-based selection in the fresh proof computation.

The old V4.6.1 revenue coefficients are read from their frozen ledger for the strict-improvement comparison. The full inherited V4.6.1 replay is coordinated separately. Upper arithmetic is freshly reconciled, but the upper measure's validity and its large continuous integration are audited by the independent upper worker. No new source or archive file was modified by this worker; all writes are confined to this fresh audit directory.

Revenue improvements from alternative candidates in V4.6.1.1 must not be added to this selected total. Conditional screening certificates contribute no extra revenue. The safe cap and inverse plateau are useful admissible mechanisms, but neither this audit nor their restricted variation equations imply unrestricted stationarity or optimality. A global matching mechanism/upper certificate remains open.
