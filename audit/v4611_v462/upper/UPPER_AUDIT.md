# Independent technical audit of the V4.6.2 unrestricted upper certificate

Date: 2026-09-06. This is an author-side mathematical audit, not a Nature reviewer report and not a proof-assistant formalization. Original research and archive files were read only. All newly generated evidence is in this directory.

**Determination: no blocking defect found in the final V4.6.2 upper endpoint or its unrestricted randomized-DSIC scope.** Promotion is supported by the fresh full replays, the continuum derivations reviewed below, and explicitly identified dependencies. The exact optimum remains open. The bound is independent of which feasible lower mechanism is used for comparison.

## Endpoint and actual new execution

Let `B20=231831916327659047/262144000000000000`, let `Delta1024` be the final exact `delta` in the frozen conditional-global-splice certificate, and let `g=81/10000000000`. The promoted endpoint is exactly `U=B20-Delta1024-g`. Its full rational is in `fresh_endpoint.json`, independently recomputed here from the component certificates and compared with the ledger.

The independently directed enclosures are

- `0.882923053258716969260626799854 < U < 0.882923053258716969260626799855`;
- the selected V4.6.1.1 expression lies between `0.876464164471798049944906113027` and `0.876464164471798049944906113028`;
- `0.006458888786918919315720686827 < U-R < 0.006458888786918919315720686828 < 0.01`;
- the feasible mechanism therefore achieves more than `0.992684652685` of optimum, **conditional on the separate lower feasibility/revenue audit**. This file audits that lower expression arithmetically, not its entire mechanism.

| Fresh command, with Python `-B -X utf8` | Outcome | Execution boundary |
|---|---|---|
| `V4_6_2_upper/flow_majorant.py` | PASS, 272.141 seconds | Complete four-chart depth-20 traversal; 1,351,220 nodes, all five accumulators and coverages match |
| `V4_6_2_upper/verifier/independent_majorant.py` | PASS, 259.750 seconds | Separate complete four-chart traversal, own degree conversion/traversal, independent archive polynomial and subdivision routines |
| `V4_6_2_upper/verifier/run_all.py --skip-deep` | PASS, 34.125 seconds | All 16 named nondeep subprocesses rerun; did not repeat either deep traversal |
| `V4_6_2_upper/verifier/verify_manifest.py` | PASS | Exactly 62 stable source-branch files, full listed coverage and hashes |
| `upper/fresh_support_latest_flatness.py` | PASS | New rational-quadratic support calculations and all-real latest-candidate slack diagnosis, described below |

The two full tree traversals are **freshly executed in this audit**, not inferred from saved PASS outputs or hashes. Logs and execution records are `primary_stdout.txt/primary_run.json`, `independent_stdout.txt/independent_run.json`, and `nondeep_stdout.txt/nondeep_run.json`. The run wrapper seals all V4.6.2 Python/JSON inputs plus the frozen inherited stream archive before and after execution; all sealed identities remained unchanged. The successful nondeep preservation checker acknowledges its historical seven-file drift record. It does not claim those old audit files were unchanged in the earlier research phase.

`B20` uses accumulator `463663832655318094`, coverage `4194304`, 200,355 fixed-winner nodes, 475,257 unresolved leaves, and maximum one-sided integer error 157. Final component accumulation uses Python integers. The independent replay imports neither the phase's primary majorant nor the archive's primary verifier; it does share the inherited independent polynomial/subdivision implementation and the same 32 exact coefficients. These dependency and independence limits must remain visible.

## Continuum weak duality and all-class quantifiers

A complete conditional DSIC mechanism supplies a convex utility with selected allocations as bounded subgradients; its gradient agrees with those allocations almost everywhere. IR gives a nonnegative zero-type utility, with no normalization to zero assumed for competitors. Integrating the radial envelope yields the field

`phi^0_j(v)=v_j(3/2-1/(2 max(v)^2))`

and the identity `R_i=integral phi_i.a_i - integral u_i(0;opponent)`. The polynomial curl comes from `x(1-x)y(1-y)P`; it has zero divergence and zero normal flux. Integration against the weak gradient of every convex Lipschitz conditional utility is zero. The origin singularity is integrable. These facts justify the revenue identity for nonlinear utilities and arbitrary allocation ranges. Pointwise capacity then bounds revenue by the integrated itemwise maximum. Neither pointwise virtual maximization nor finite menu completeness is assumed implementable.

For the reported model, mechanisms remain complete, jointly measurable, pointwise DSIC/IR and pointwise feasible, with integrable payments. Continuum identities hold on almost-everywhere gradients; competitors retain their actual selected allocations at exceptional reports. This is compatible with pointwise feasibility, which is stronger than what the absolutely continuous final price needs. General *singular* interfaces must additionally retain the stated Borel residuals, measurable kernels and well-defined pairings with actual selections. A Lebesgue equivalence class of residual capacities is insufficient for those separate interfaces. The numerical final price is absolutely continuous and avoids this issue.

## Independently reconstructed full-capacity support

The support used by the splice can be checked directly without taking the inherited screening theorem as an unexplained numerical premise. Put `A=2/3`, `b0=(4-sqrt(2))/3`, `k=b0-A`, `Z=3/4`, `ell=A` for `x<k` and `ell=b0-x` for `k<x<A`. Write

`f=3ell-2` below A, `f=1` above A, `F(x)=integral_x^1 f`, `H(y)=4(y-Z)_+`.

On the three x intervals, `F` equals 0, `(3b0-2)(A-x)-3(A^2-x^2)/2+1-A`, and `1-x`. The fresh exact checker establishes the endpoint matches, `F'=-f`, `area(D0)=1/3`, and the total price mass `4/9+2sqrt(2)/27` using independent rational-quadratic arithmetic.

The densities are

`Psi1=3(x-A)_+ + 4F(x) 1[y>Z]`,

`Psi2=3(y-ell(x))_+ 1[x<A] + f(x)H(y)`.

They have divergence 0 in D0 and 3 outside D0. Internal interfaces have continuous normal traces: the jump of Psi1 at y=Z is tangential; Psi2 is continuous there; the remaining piecewise thresholds match. Top/right normal fluxes are 1, bottom/left fluxes 0. Therefore weak integration by parts, compared with `R=top(u)+right(u)-3 integral u`, gives the universal exact identity

`<Psi,a>-R = 3 integral_D0 u >= 0`.

Nonnegativity is also direct. `F>=0`, while above Z the potentially negative f term in Psi2 combines as `(1-H)3(y-ell)+H(3y-2)`, with both summands nonnegative. Below Z its remaining term is manifestly nonnegative. This derivation includes arbitrary nonnegative utility offsets because `3 area(D0)=1`; no hidden zero-origin assumption occurs.

The support vanishes on the own-report square W=[0,.43]^2. The freshly replayed rational Bernstein sign certificate establishes both inherited own virtual values nonpositive on W for every opposing report. The chart denominator is positive away from the origin; zero-coordinate faces use the explicit coordinate factor. Item and bidder transformations are justified by the frozen polynomial symmetries.

## Why the common price is valid and why the improvements add

The final price is 0 on W×W, Psi of the high-report bidder on exactly-one-in-W regions, and the corrected virtual maximum when both are outside W. For each bidder, the choice of using Psi versus the stream inequality depends only on its opponent report. Thus complete conditional menus are compared; no own-type patch of an incentive inequality and no interchange of supremum and integration is being used. In the complementary region where that bidder's own report belongs to W, its virtual values are nonpositive and the common price is nonnegative. Consequently both unrestricted charged values satisfy `H_i(Pi')<=0`, and the empty mechanism attains zero.

This is a valid exact common support with `H_1=H_2=0`; it is **not** a matching auction certificate. The empty mechanism leaves all positive-priced capacity unused.

For the conditional reduction, the old and new prices are zero on W×W. The two bidder replacements therefore add without double subtraction. Evaluating the stream identity on the fixed single-buyer optimal menu turns the exact saving into integrated nonnegative virtual-allocation slack. Opponent polynomial coordinates are integrated exactly; the remaining rectangles belong to an *integral certificate*, not a finite type grid. On each certified allocation-constant rectangle Jensen's positive-part bound supplies a rational nonnegative contribution. Omitted boundary cells can only weaken the reduction. The corrected bundle classifier requires both minimum sum above b0 **and** minimum low coordinate above k. The earlier too-permissive classifier is not used. Full n=1024 reconstruction and the independent coefficient/corner/cell-integral audit passed freshly.

The four translated two-way IC cycles are nonnegative finite measures on actual pairs of reports of one bidder, keeping the opponent fixed. The sum of the two true IC residuals is `d.(a(A+s)-a(B+s))>=0`. Equal shapes and opposing directions cancel source/target mass, so the modification introduces no interior sink. It shifts the field by +epsilon*d and -epsilon*d in the respective boxes. Whole-box strict winner inequalities, rather than sample winners, make the envelope change exactly `-81/10^10` over the four disjoint symmetry images. Exact separations exclude every conditional replacement region. Their addition to the same amplitude-one stream is therefore justified.

All sixteen decreasing ledger endpoints are valid, but their finite decrease is not evidence of convergence to optimum. The final gap identity separates screening, capacity, virtual-allocation and true IC/origin-IR slack. It must retain the independent nonnegative numerical remainder `E=(B20-B)+(D-Delta1024)`; otherwise an equality assertion would silently omit certification error. The published combined proof states this correctly.

## New diagnosis for the actual V4.6.1.1 candidate

The frozen V4.6.2 notes diagnose V4.6 and V4.6.1. Their claim that the lower functional fee is absent **does not carry over** to V4.6.1.1. A fresh check here supplies the needed new argument rather than relabeling the old evidence.

Use the closed profile box centered at `(t,rho,x,y)=(151/200,3/40,9/10,63/200)`, with halfwidth 1/10000 and positive interior volume `1/625000000000000`. The selected new mechanism has `c=157/500`, changed `a,b,s,T,U`, and fee `g(y)>0` throughout this box.

For bidder 2, `A<t<T` and `rho<c`, so its menu is E with

`delta=9(T-t)(U-t)/16`, `alpha=3t-2`, `beta=alpha/(alpha+2delta)`, `L=delta+alpha/2`.

On the t interval, delta decreases and beta and L increase. Rational endpoint bounds give `.9<beta<.98`, `c<y<c+L`, `x>t`, and `x-t+1/2-y>0`. Thus lottery utility `x-t+beta(y-c)` is strictly positive; it strictly beats the scarce singleton by `beta(y-c)`, the bundle by `(1-beta)(c+L-y)`, and the safe singleton by more than `x-t+1/2-y`. These are all-real strict comparisons, including every closed face of the box.

Bidder 1 sees the base-fee menu since `x>T`. Here `H=x+y-b`, `s-y>a`, and `s-x<a`. Its nonempty prices simplify to

`P1=x+y-c`, `P2=y+q+g(y)`, `C=x+y+g(y)`.

The first exceeds t, the second exceeds rho already before the positive fee, and the third exceeds t+rho already before the fee. Empty is therefore the unique maximizing choice. The actual joint allocation is `(empty,(1,beta))` on the whole box. The exact selected implementation additionally agrees at all 16 corners and the center; those 17 profiles supplement the inequalities.

This box is outside both W regions and all eight upper cycle boxes. A new direct rational polynomial reconstruction, using only the 32 frozen coefficients and no inherited polynomial builder, expands the bidder-2 safe numerator at the box center. The absolute nonconstant-monomial bound proves its upper bound strictly negative. Division by the positive denominator upper bound supplies `m>0` with `phi_22<=-m` everywhere. The local safe capacity-plus-virtual slack is `Pi'_2-beta*phi_22 >= .9m`. Integration yields the explicit strictly positive rational in `fresh_support_latest_flatness.json`, approximately `1.7037945963617297e-17`.

Thus the **actual V4.6.1.1** candidate is not matched by this particular final dual. This proves neither a new admissible primal improvement nor primal suboptimality. Its purpose is an equality diagnosis. The positive lottery allocation and unused safe capacity also force any matching density certificate to have an open zero-price/zero-winning-field plateau there. The finite polynomial-curl family cannot have that plateau: its field is analytic on a connected radial chart, while a noncancelable radial pole prevents it from vanishing identically. This excludes exact matching by that specified analytic family, not arbitrary nonsmooth or singular measures and not asymptotic approximation.

## Promotion limits and corrections to make in the archive

1. Promote the new unrestricted U together with the separately audited latest R and the gap near .00645889. Preserve the frozen upper ledger's old lower comparisons as historical.
2. Include the common-price construction, zero charged optima and exact certification remainder, rather than announcing only a numerical bound.
3. Cite the new latest-lottery diagnosis when discussing V4.6.1.1. State that its fee is active and nevertheless empty remains strict. Do not claim the old functional-disjointness proof applies unchanged.
4. Keep the alternative singular lottery support and null-opponent-charge lemma as diagnostic results. They contribute **zero** to the reported endpoint; no nonexistence of all singular common supports is proved. General singular pairings require well-defined selected allocations on the charged sets.
5. No optimal mechanism, exact optimum, attainment, uniqueness, finite-menu completeness, unrestricted stationarity, or convergence theorem is established. No new exhaustive priority audit of the literature was performed by this technical audit.
6. A prototype of the additional fresh checker initially attempted an unavailable symbolic package. It was replaced by self-contained Fraction/quadratic and polynomial arithmetic; the final successful executable requires no such package. The two original full traversals require NumPy. This setup issue did not alter any source certificate or mathematical endpoint.

Trusted boundary: Python exact integers/Fraction, bounded NumPy integer operations and their overflow guards for the traversals, fixed coefficient data, the explicitly reconstructed polynomial calculations, and the written convexity, weak integration-by-parts, measurability and full conditional-menu arguments. Fresh numerical/profile replay is supplementary to those all-real arguments.
