# Independent structural audit of V4.6.1.1

Audit date: 2026-09-06. This is a technical audit of the selected mechanism and its conditional screening statements, separate from the later simulated reviewer round. No source mechanism, source certificate, or publication file was modified. There is **no blocking mathematical defect found in the audited claims**. Promotion is justified with the claim boundaries below; global auction optimality is not among those claims.

## 1. Audit boundary and fresh evidence

The audited definition is `V4_6_1_1_lower_bound/verifier/refined_candidate.py` (lines 15–67), together with its all-real specification and proof in `research_log/refined_structure_audit.md` (lines 13–330). The proof of conditional Q/E optimality is at lines 332–474; W is in `research_log/residual_wing_screening.md` (Sections 1–3). Earlier mathematical definitions were inspected in `V4_6/research_log/inner_diagonal_capacity.md` and `inner_lottery_certificate.md`. Source audit conclusions were not used as premises: the compatibility arguments, parameter signs, envelope identities, and required actual occupation were reconstructed below.

Fresh read-only execution, using Python 3.10.16 without optimization or bytecode writes, completed successfully:

| Operation | This audit's result |
|---|---|
| `V4_6_1_1_lower_bound/verifier/run_all.py` | Exit 0; 14 current mathematical entries plus 12 V4.6.1 mathematical entries, and the documented provenance checks |
| Current `verify_manifest.py` | Exit 0; all 53 stable files match the complete manifest |
| Current `artifact_audit.py` | Exit 0; 17 JSON files, 12 Markdown files, and 33 local links checked |
| Independent new Fraction polynomial checker | 22 exact checks pass; imports no project module |
| Before/after current source identity | Every current source file, including its SHA256SUMS file, is unchanged |

The command records, full output, and source hashes are `full_replay_run.json`, `run_all.py.log`, `verify_manifest.py.log`, `artifact_audit.py.log`, and `source_identity.json` alongside this report. `independent_structure_identities.py/.json` records a separate exact reconstruction. The new checker initially attempted to use SymPy, which was unavailable; its final version uses only Python standard-library Fraction arithmetic and an independently written polynomial representation. The failed environment probe did not affect source artifacts or results.

The full replay includes the selected mechanism's 8,961 bounded profile checks and 16 reallocation-box corners, the separately reconstructed 2,209 profile pairs, and W's 168 menu-integral identities plus 12,220 actual profile checks. These counts are implementation evidence. They are **not** the justification for continuum DSIC or for arbitrary randomized conditional competitors. Those conclusions use the all-real arguments examined below. No proof-assistant formalization was run or claimed. The separate revenue auditor is responsible for the total revenue formula and independent continuum integration; this report does not replace that obligation.

## 2. Complete joint mechanism: reconstruction and audit

The parameters are exact: A=2/3, d=1/2, c=157/500, q=93/500, a=A+q²/2, b=a+c, s=a+d, and g(r)=(4/5)(3421/10000-r) on the closed interval [c,3421/10000], zero elsewhere. The jump at c is positive. Its generalized inverse has the plateau k(t)=c for d<t<=h(c). The valid implications are x<k(t) => h(x)<t and x>=k(t) => h(x)>=t; h(k(t))=t is false inside that plateau. The code and proof use the implications, with the jump face included in g's support.

The three opponent-menu regions partition every report: closed Q, open E, and the remaining base rows. Q's cap is a part of the selected mechanism, not an optional correction. The selection rule first keeps only the empty option if the maximal utility is zero, otherwise keeps every maximizer, and then takes the first feasible pair in the stated finite joint order. This gives a well-defined Borel mechanism once nonempty feasible argmax products are proved. The six menu-region combinations satisfy that requirement:

- **Base/base.** The uncharged prices are pivot-normalized menus of the common nine-outcome feasible affine allocation. The discount P_scarce+P_safe-P_bundle has lower bounds a-c, q, and 2q in the zero-, one-, and two-high-coordinate tariff regimes. All are strictly positive. Consequently an old safe maximizer cannot switch to a positive scarce singleton after both safe and bundle prices rise by the same nonnegative fee; the bundle comparison remains unchanged. Every old maximizer has a new maximizing subset. Applying this to a common feasible old pair proves base/base feasibility, including positive ties. Merely increasing prices would not have supplied this argument.
- **Q/base.** A base buyer whose own report lies in Q can only buy its high item positively. With the other low coordinate y<=d its high price is at least max(x,x+y-c), while any opposing Q allocation consuming that item forces x>=A or x+y>=C>=t+c. With y>d, a positive base purchase forces x<t-q<d<y, so the surcharge applies to that same physical item and its price is at least h(x). The Q bundle's scarce upgrade is C-B>=k(t); the inverse implication then excludes conflicting positive purchases. The cap only increases this upgrade threshold.
- **Q/Q.** Positive singleton prices exceed d, while a constrained Q type's low value is below d. Hence positive singleton allocations can only be disjoint high items under opposite orientations. Two positive bundles contradict the two sum-price inequalities. A bundle/safe conflict would require both y>B>=h(rho) and rho>=k(y), which is impossible. Strict positivity makes this exclusion valid at the other bidder's indifference face. Free-Q singletons cannot be positive for another Q-free type.
- **E/base.** An own E type's low singleton is unaffordable and its bundle is dominated by its high singleton because its low value is below c. For any opposing E option consuming that high good, IR and the bundle/lottery comparisons imply the old base high tariff is at least the own E high value. The uncharged pair is therefore compatible; the proven base maximizing-subset property allows the actual fee.
- **E/Q.** The old reserve-a=A argument would fail here. The replacement bound on the Q type's E-lottery utility is A-t+beta(a-A). The exact ratio (t-A)/beta=t-A+2delta/3 is strictly increasing on the open E interval, with infimum q²/2=a-A. Thus the lottery is strictly excluded even at the selected allowance equality. The E bundle is also strictly excluded because delta(A)=3q²/4>q²/2 and t-A+delta is increasing. Only the safe singleton remains; its reverse Q upgrade k(y)>=c excludes conflict with the E low value rho<c. Strict k(y)>c is unnecessary and would be false on the plateau.
- **E/E.** With the same orientation, low value below c makes the bundle and lottery dominated by the scarce singleton, which only the higher high report can obtain with positive utility. Equal high reports have zero utility and use empty. With opposite orientations, scarce and upgrade thresholds exclude the other physical good, leaving disjoint own high items.

The key all-real Q compatibility margins were independently recovered as exact rationals: B0(A-q)-h(b-A)=37/5000000, the minimum derivative in the remaining fee-support subinterval is 79/1000, and B0(c)-d-g(c)=212401/3000000. Thus the extra floor k+h(rho) is redundant throughout Q. No assumption C<1 is needed; C0(k)>1 occurs legitimately near t=A.

Every selected outcome remains a maximizer of the same fixed-opponent menu; report-dependent joint tie selection therefore preserves **pointwise DSIC** for every true report and deviation. Empty establishes pointwise IR. Finite Borel comparisons establish measurability. Selected payments are nonnegative and bounded by allocated value <=2. Fractional marginals can be realized by disjoint item-wise intervals under uniform randomness, giving samplewise feasibility and the stated expected utility. The result is DSIC in expected utility, not a claim of universal truthfulness for each random seed.

## 3. Full randomized conditional screening on Q

The prior diagonal/coupled identities extend to the current parameter range because their actual algebraic hypotheses remain true, not because the older theorem's written z<=0.91 limit was ignored. This audit separately integrated the top coefficient for arbitrary k,C and obtained

m = 2(C-5/6-3k²/4),   3|D0|-m=1.

For an uncapped row, c<=k<=A-q<d, B=C-k<=A and C>=C0(k); hence the top coefficient is nonpositive below A, the anchored cumulative price is nonnegative, and the utility sink is nonnegative even for unnormalized u(0,0)>=0. This derivation allows C>1 when it occurs. When m>0, necessarily C=z<=b<1, which is the separate condition needed for the Q-free anchor reports; no anchor is incorrectly extended using C0(k)>1.

Actual top occupation for x<k follows from the reverse base price max(d,h(x))<t and strict purchase of the high item. If m>0, the reverse Q-free bundle is strictly cheaper than z on the bottom and vertical anchors, so the opponent occupies both items there. At the cap, C=z>b0 and the symmetric theorem applies with k'=C-A<d and nonnegative m'; its price vanishes below k', so no nonexistent enlarged top hole is assumed. Q-free C=b0 has m=0 and the full-capacity SJA certificate; C>b0 has the same strict anchors. This establishes arbitrary randomized conditional optimality on all closed Q fibers, for either bidder, under the actual frozen opposite allocation.

## 4. E's incentive-derived junction trace

The original literal junction-capacity statement is false after raising a above A. It is correctly repaired in the current source; it must not be reinstated in the manuscript. At an interior x in (A,t), actual residual capacity at (x,c) can be positive, and the replay explicitly retains a vacant-face example.

The relevant fact is stronger about *feasible IC allocations*: the actual residual scarce capacity is zero throughout the open rectangle A<x<t, 0<y<c, because the reverse E menu sells the opponent its high singleton strictly. Every feasible competitor therefore has zero selected scarce allocation in that rectangle. The two horizontal DSIC inequalities make its utility constant along each horizontal line. Bounded allocations imply Lipschitz continuity, so the constancy extends to y=c. At an interior x on that trace, comparison with a point on either side forces **the selected** scarce marginal to zero, including exceptional selected subgradients.

The inherited E envelope and convex-trace identity were checked with the new parameters. The zero-top-mass polynomial is identically zero; the strict sink lower bound is q(1-3q/2)>0. The remaining actual top hole holds despite the new jump because h(u)<A<t. The priced junction segment A<x<t contributes zero for every actual-residual competitor by the IC trace argument. The other volume and singular prices are saturated by the candidate; all utility slacks vanish at it. This gives a tight **actual-residual** conditional upper bound over arbitrary randomized DSIC/IR competitors.

Deleting the zero junction pairing does not make the remaining measure a support valid for arbitrary new residuals. The allocation-zero inference used the specific adjacent open rectangle, which a joint deformation may release. Q's explicit nonnegative measure supplies an arbitrary-residual support in its own conditional setting; E's repaired statement has the narrower actual-residual scope just described.

## 5. W: an independent derivation and applicability check

Write p=min(rho+q,1), k=t+rho-p, and W={t>=1-q, t+rho>=1+u}. On W, rho>=u>c, the fee is zero, the scarce singleton is unaffordable, and the only useful options are safe at p and bundle at k+p. The source's actual occupation proof was checked separately in every reverse base, Q and E row, including cap rows, surcharge orientations, p=1, equality t=1-q and equality z=1+u. Its strict comparisons show first-item occupation on x<k and inside the no-sale region; the left-edge trace has second-item occupation. It does not assume both items are occupied throughout the entire no-sale region.

For any feasible DSIC competitor those capacities imply u=u0 on D0={y<p,x+y<k+p}, and u(x,y)=u(0,y) on the strip x<k. Average the horizontal and vertical envelope identities, then distribute the left-edge rent across that strip. This independently yields

R+u0 = integral_G [((3x-1)a1+(3y-1)a2)/2]
       + integral_H [(((3k+1)y-k-1)/(2k))a2],

where G={x>k,x+y>k+p} and H={x<k,y>p}. The coefficient signs follow from k>=1/3, k+p>=4/3 and (3k+1)p>=k+1. At the selected constants the last inequality has the exact uniform numerator margin 18601/5000000>0. The candidate saturates the nonnegative coefficients, giving the full randomized conditional optimum.

Besides recovering the candidate integral, the new independent polynomial checker verifies this identity for the nonlinear convex utility u=(u*)²/4. Its allocations vary continuously over positive cells, so this check is not confined to finite allocation ranges. This is an additional exact sanity check; the general envelope proof, rather than any finite list of test utilities, supplies the arbitrary-competitor theorem.

The region areas independently recompute to |Q|=1746937679191/4500000000000, |E|=4867/62500 and |W|=438867/2500000. Their disjoint union is 2887322279191/4500000000000 = 0.64162717315355... of each bidder's opponent square. These are measures of conditionally certified subproblems, not a percentage of the auction revenue gap eliminated or proof of joint optimality. W's displayed density alone is not an arbitrary-residual support, because its derivation eliminates utility using these particular capacity-zero sets.

## 6. Publication implications and remaining scope

The following theoretical contributions are supported by this audit and can be emphasized without an optimal-auction claim:

1. A complete compatible-menu construction with an upward exchange-threshold jump and a positive-measure generalized-inverse plateau; the reallocation witness strictly changes ownership beyond predecessor containment.
2. An exact link between the profitable whole-menu safe-price cap and restoration of the Q envelope sign needed for full randomized conditional screening.
3. An IC-derived boundary allocation constraint despite positive physical residual capacity on that very boundary, which repairs the E inner certificate after the reserve increases.
4. A strip-and-left-trace rent identity supporting full randomized screening on a substantially larger high-value wing, without finite-menu assumptions for competitors.
5. A quantitative actual-residual zero-gap map showing precisely where further gains must change the opposite allocation, rather than merely refine one fixed conditional menu.

These are mathematical contributions relative to the explicitly inspected predecessor constructions. This audit did not perform a literature-priority search; it does not establish a claim of being the first such method in the literature. It also does not establish a common global capacity-price/incentive-flow certificate, an unrestricted optimal mechanism, uniqueness, parameter optimality, a finite-menu classification, or existence of a finite-menu optimizer.

No mathematical erratum requiring a source change was identified. The existing source already includes the necessary plateau, cap, reserve, exceptional-trace and actual-residual qualifications. The manuscript update should preserve them. An inherited replay marker such as `FULL_CONTINUUM_AUDIT_PASS` is not a formal-verification claim: prose should identify the written continuum proof and the finite exact implementation checks separately.
