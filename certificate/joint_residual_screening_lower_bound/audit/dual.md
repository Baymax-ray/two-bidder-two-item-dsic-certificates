# Independent audit of the V4.6 conditional capacity certificates

Outcome: **PASS for the stated conditional theorems, with one nonblocking null-face wording erratum.** No matching unrestricted two-bidder auction upper certificate follows. No source or archive file was changed by this audit.

This audit independently reconstructs the proof identities and their signs, checks the actual occupied traces and final coverage exclusions, and supplies fresh exact computations. Existing finite-menu examples, manifest matches, and pre-existing PASS messages were not used as substitutes for the continuum argument. The inherited unrestricted upper certificate was not re-executed here. This report does not establish literature priority.

## 1. Scope and source identity

The main sources are `V4_6/research_log/inner_lottery_certificate.md`, `inner_diagonal_capacity.md`, `conditional_coverage.md`, `outer_capacity_junctions.md`, `outer_lottery_strip.md`, `outer_bundle_reoptimized.md`, and `free_bidder_one.md`, together with the final mechanism and its wrappers. The V4.5 simultaneous-lottery proof and V4.02 Q certificate interface were read to check inherited interfaces. Hashes of the four principal proof/implementation sources are recorded in `fresh_exact_dual_checks.json`.

The results concern a **fixed actual residual** and every complete randomized DSIC/IR competitor feasible under that residual. The certificates contain genuine singular report-line prices. Therefore residual functions are pointwise objects, for example bounded Borel maps into `[0,1]^2`; the support pairing must not be interpreted on `L-infinity` equivalence classes modulo two-dimensional null sets.

## 2. Arbitrary competitors, selected subgradients, and measurability

Fix an opponent report. Pointwise DSIC yields

`u(v) >= u(w) + a(w) dot (v-w)`

for every two own reports. Hence `u` is convex, each selected allocation belongs to its subdifferential, and `0 <= a_j <= 1` makes `u` coordinatewise nondecreasing and Lipschitz. There is no finite-menu or deterministic-range restriction in this deduction.

On every fixed horizontal report line, the selected tangential allocation `a_1` is nondecreasing in the horizontal variable and agrees almost everywhere on that line with the derivative of the convex utility trace. The analogous statement holds for vertical `a_2`. Consequently the line envelopes used in both certificates are identities for the actual selected allocations, even when a line is a null event under the original type distribution. No claim that arbitrary normal subgradient components are derivatives of a line trace is needed.

The payment identity is `p = x a_1 + y a_2 - u`. Integration by parts on the square gives

`R = integral u(1,y) dy + integral u(x,1) dx - 3 integral u`.

This formula does not impose `u(0,0)=0`, nonnegative payments, or an outside option actually attained at the origin. Pointwise IR supplies only `u >= 0`. Both proofs correctly retain the resulting nonzero-origin utility slack.

The Borel competitor version is immediate. The same two conditional arguments also apply to Lebesgue-measurable selected mechanisms: on an own-type fiber, allocations equal the gradient outside the convex utility's two-dimensional null nondifferentiability set, and the tangential allocations on each priced line are monotone. Thus the volume and the specific line integrals used here are defined. For jointly Lebesgue-measurable mechanisms with integrable payments, Fubini passes valid sectionwise revenue inequalities to total revenue for almost every opponent. This argument neither constructs a pointwise Borel representative nor licenses arbitrary singular kernels acting on merely joint-Lebesgue selections.

## 3. Lottery certificate: independent derivation

Use the source notation `A=2/3`, `q=113/500`, `c=137/500`, `alpha=3t-2`, `L=delta+alpha/2`, `Y=c+L`, `j=1-t/2`, and `k=t-q`. The exact relations `beta L=alpha/2`, `C-Y=j`, and `B=C-k` are consistent. The factorization `delta=9(T-t)(U-t)/16` proves positivity on the prescribed open interval. The threshold orders in the note follow, in particular `k<j<A<t`, `Y<B<A`, and `L<=q`.

Integrate horizontally on `G={x>z(y)}` and vertically on `H={x<A,y>e(x)}`. For example,

`3 integral_G (x-z(y)) a_1 = 3 integral (1-z(y)) g(y) dy - 3 integral_G u`.

The analogous vertical identity gives exactly the displayed volume densities and trace coefficients. Expanding the integral of the top coefficient `f` and substituting `delta` yields zero as a polynomial identity. Since `f<=0` below `A` and `f=1` above `A`, its negative cumulative integral `F` is nonnegative. Integration by parts gives `integral f h = integral F a_1(x,1) dx`, with the stated positive sign.

For the right trace, the coefficient on the lottery interval is `alpha-3 beta z`. Its first moment is zero. A convex hinge at position `s` has coefficient

`integral_s^L (alpha-3 beta z)(z-s) dz = - beta s(L-s)^2/2`.

Thus the trace gap is the sum of the nonnegative below-c monotonicity term and the nonnegative integral against the trace's second-derivative measure. This covers arbitrary convex nonlinear changes of the trace and arbitrary allocation probabilities, rather than only the displayed lottery family. Endpoint slope jumps cause no missing term: the affine part uses the right derivative at `c`, while the hinge weight vanishes at the relevant interval endpoints.

On the actual line `y=c`, monotonicity of `a_1` gives

`M = t/(t-A) integral_A^t a_1 - integral_0^t a_1 >= 0`.

The line-price pairing is exactly

`integral w a_1 = lambda[g(c)-u(0,c)] + lambda M`.

Combining this with the volume and trace identities yields the source gap with the correct signs:

`<pi,r>-R = <pi,r-a> + T_g + lambda M + 3 integral_D0 u - lambda u(0,c)`.

The rectangle `K=[0,k] x [c,B]` is contained in `D0`. On it monotonicity gives `u>=u(0,c)`, while IR gives `u>=0` everywhere else. The independent exact bound

`3|K|-lambda >= q(1-3q/2) > 0`

therefore proves the final slack is nonnegative. No normalization or positive sink density at every report was silently imposed. The line-price coefficient remains bounded as `t` approaches `A` because `lambda=3(t-A)(c+L/4)` cancels the apparent denominator.

At the candidate, the right trace is constant below `c` and affine on `(c,Y)`, the horizontal line allocation is zero below `t`, and utility vanishes on `D0` almost everywhere. All non-capacity slacks vanish. The volume supports charge marginals allocated with probability one. The top line needs only residual zero for `x<k`; the `y=c` line needs only residual zero for `A<x<t`. At their remaining positive-price portions the candidate allocates one, and feasibility forces residual one. This establishes full conditional optimality under precisely candidate feasibility plus H1/H2, with no hidden assumption of globally free second-item capacity.

## 4. Nonblocking source wording erratum

The lottery note defines `D0` as the complement of strict sets `G` and `H`, then says that `u*=0 on D0`. Literally this is false on some partition faces.

An exact witness is

`t=7/10, (x,y)=(2/3,1), u*(x,y)=62347/93750 > 0`.

Here `x=A` belongs to neither `G` nor `H`, hence the point belongs to the stated `D0`. The entire issue is confined to two-dimensional null faces. The correct statement needed by the proof is **`u*=0 almost everywhere on D0`**, or one can assign the partition faces explicitly. No capacity-line equality, pointwise mechanism definition, or revenue integral needs to be changed. The original source is preserved; the promoted exposition should use the corrected wording.

## 5. Diagonal and constrained-Q certificates

For the generalized candidate `(A,B,C)` with `k=C-B`, `B<=A`, and

`m=2C-5/3-3k^2/2 >= 0`,

the same envelope partition gives top coefficient `f=3B-2` below `k`, `f=3C-3x-2` on `(k,A)`, and `f=1` above `A`. Its total mass is `m` and it is nonpositive below `A`.

Subtracting an anchor of mass `m` at `x=1/2` gives

`F_m(x)=integral_x^1 f - m 1_{x<1/2} >= 0`.

The positive jump of this density at `1/2` has the stated integration-by-parts effect:

`integral f h = m h(1/2) + integral F_m a_1(x,1) dx`.

It is not an unaccounted atom of the capacity-price measure. Expand the anchor utility along the bottom horizontal segment and the vertical segment at `x=1/2`. This produces exactly the bottom and vertical line prices in the note. Direct area integration gives

`3|D0| = m+1`.

Consequently `3 integral_D0 u - m u(0,0) >= u(0,0) >= 0`, and the asserted exact gap follows for arbitrary randomized competitors. At the candidate the sink is zero. The priced volume regions and the positive-candidate parts of the top/vertical lines saturate by feasibility. The remaining required capacity-zero pieces are exactly the occupied traces stated in the note.

In the symmetric case `B=A, C=z`, the mass is `1/3-(3/2)(4/3-z)^2`, nonnegative on the prescribed interval starting at `b0`. The top density vanishes below `k`, so no extra top-hole hypothesis is needed there. In the coupled constrained case `B=C-k`, `C0=5/6+3k^2/4`, the mass is `2(C-C0)`. Its extra positive top density below `k` makes the retained top capacity-zero condition essential; the source explicitly verifies it.

The case `m=0` also explains the retained Q support. It removes the new bottom and vertical anchor prices and recovers the previous top/volume certificate. The symmetric SJA boundary likewise has `m=0`. No passage to a randomization-restricted class is involved in either limiting case.

## 6. Actual residuals and final conditional coverage

On Eplus before the corner release, both occupied traces follow from actual complete menu prices. On `(x,1)`, the other bidder's high price is `1/2` when `x<=c` and `x+q` otherwise, both below its high value `t` for `x<k`. On `(x,c)`, `A<x<t`, its high price is exactly `x`, its utility is strictly positive, and the retained face rule prevents a splice from changing that allocation. The free and bundle-exchange regions miss these report lines. Candidate feasibility supplies all remaining saturation conditions.

For reopened Q, the bottom and vertical occupied pieces are actual strict bundle purchases under the closed F rule or the G bundle rule. In the constrained case reopening forces `1/2<t<q+sqrt(23)/15<a`, so both own singleton values are below the relevant singleton prices and cannot displace those bundles. The top row is retained and gives the required exact scarce-item occupation below `k`.

The final coverage exclusions are sufficient:

- Bidder 1's Eplus menu remains unchanged outside its opponent rectangle S. Its residual changes from the opposing lottery cut only at own reports in W, which meet neither orientation of the priced top and `c` lines. Feasibility maintains saturation on the volume supports.
- For bidder 2, the changed candidate menus are covered by the excluded high-coordinate band. A release of the physical `y=c` occupied trace requires a former high-singleton utility `t-x` in `(0,epsilon]`, with `x` in the horizontal range of S. Hence `t` lies in `[0.7-4 epsilon,0.71+epsilon]`. The conservative stated exclusion covers this whole range, including endpoints and opponents outside W. The opposite physical orientation is safely overexcluded.
- For a fixed Q report, the entry fee can release only the physical safe-of-S item. A positive purchase implies that this is the scarce item in the Q alignment and that its own scarce coordinate is below `k`. The scarce volume density vanishes there, the priced top/bottom edges are absent, and the vertical anchor charges the other marginal. The final lottery-price change is indexed by W, disjoint from Q. Therefore Q saturation survives.
- F menus are unchanged. Reports in F remain globally empty under the later contractions and the small lottery cut, so both F conditional residuals remain full.

These conclusions retain full conditional optimality on the stated surviving regions and make no equality claim on excluded Eplus fibers.

## 7. Safe value-functional corollaries and limits

For pointwise bounded residuals, `V(r)` is concave. Given two admissible mechanisms, a fixed exogenous coin with probability `theta` mixes their allocations and expected payments, preserves every pointwise DSIC/IR inequality and Borel/integrability condition, and is feasible under `theta r1+(1-theta)r2`. Apply this to epsilon-optimal mechanisms and let epsilon tend to zero. There is no need to assume an optimizer exists.

The matching conditional measure therefore gives the valid global affine support

`V(r) <= V(r*) + <pi,r-r*>`.

This does not establish differentiability, a unique supporting measure, existence of a jointly measurable selection of fiber optimizers, or dual attainment for the original auction. An own-report-dependent mixing weight must not be used to prove concavity because it can break DSIC. A fixed scalar mixing proof also works for globally defined conditional-bidder functions; any stronger simultaneous auction claim needs both bidders' constraints checked.

The singular measures need not support the other bidder. In particular, an own-report line can become an opponent-null set for the other conditional optimization. Thus these certificates cannot simply be assembled into a matching unrestricted auction upper proof. The final auction gap being below `0.01` is a numerical-bound milestone, not an equality or optimality theorem. Calling the certificates newly verified V4.6 contributions is justified; a literature-first claim requires a separate literature audit.

## 8. Fresh verification and trust boundary

`fresh_exact_dual_checks.py` uses only the Python standard library, imports no primary or predecessor verifier, and independently performs rational polynomial arithmetic and integrals. It verifies five symbolic factor/mass/area identities and twelve exact gap calculations on smooth convex utilities with continuous allocation ranges. One family has positive origin utility and subsidy payments. Both lottery and diagonal decompositions match exactly and all individual slacks are nonnegative. The exact null-face witness is also checked. Result: `FRESH_INDEPENDENT_DUAL_ALGEBRA_PASS`.

`fresh_final_residual_checks.py` constructs fresh exact report cases against the final mechanism, with bytecode writes disabled. It checks 109 retained Eplus fibers, 545 occupied Eplus trace reports, 436 candidate report choices, and 44 occupied Q trace reports, including both item orientations and points at or immediately outside the final conservative exclusion boundaries. Result: `FRESH_FINAL_RESIDUAL_COVERAGE_REGRESSIONS_PASS`.

Both scripts default to read-only recomputation and comparison with their stored JSON. Run `python -X utf8 -B SCRIPT.py`; add `--write` only to regenerate that script's audit JSON. Each was run with `--write` and then in default mode after this packaging change; both modes passed, the JSON content was preserved, and default execution preserved each JSON file's modification time. The mathematics and recorded source hashes are unchanged.

These fresh scripts and their JSON outputs are in this audit directory. They support the formulas and implementation correspondence but do not replace the analytic proof above. The final mechanism's complete primal feasibility and exact whole-auction revenue are separate audit obligations. No proof-assistant formalization, full predecessor upper replay, or literature-priority certification was performed by this sub-audit.
