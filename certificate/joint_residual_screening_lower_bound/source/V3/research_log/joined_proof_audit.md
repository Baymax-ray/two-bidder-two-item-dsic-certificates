# Hostile proof audit: joined-threshold mechanism and certificate interface

Audit date: 2026-09-05. This is an independent bounded analytic audit by the V3 admissible-variations investigator. It is not peer review or a formal proof check. The candidate construction files were read without modifying them.

## Material reviewed and scope

Reviewed `research_log/joined_threshold_candidate.md`, `verifier/joined_threshold.py`, and their mechanism dependencies `verifier/baseline_mechanism.py`, `verifier/stationary_s.py`, and `certificate/baseline_mechanism.json`. Subsequently reviewed `research_log/candidate_certificate.md` for signs, binding-constraint support, and the local/global distinction.

This audit addresses complete pointwise implementation, exceptional reports and ties, the proper-menu domain when the bundle price exceeds one, the four local contraction directions, and the weak-duality identity. It deliberately does not rerun or duplicate the separately assigned numerical revenue-enclosure audit.

## Verdict on the mechanism proof: PASS

No blocking all-report DSIC, IR, or capacity gap was found. The proof rests on itemwise containment in a shared feasible base, not on an inferred common potential for the final mechanism.

1. **The base menus match the common joint maximizer.** Conditioning on a bidder's empty mask gives opponent welfare offset H. Conditioning on item 1 gives the better of leaving the opponent empty at cost a or allocating item 2 to it at joint cost s; the resulting price is `H+min(a,s-w2)`. The other singleton is symmetric, and the bundle price is H+b. Thus the projection of the same globally selected outcome is a utility maximizer for each bidder. The nine listed mask pairs are pairwise item-disjoint.

2. **The base is subadditive on every opponent report.** The three cases determined by whether zero, one, or two coordinates exceed d give lower discount margins `2a-b`, `s-b`, and `2(s-b)`. Their minimum is the positive rational `s-b=227/1000`. Every nonempty base price is at least `s-1=137/1000`.

3. **All inherited changes are contractions.** A finite read of the certificate found 20 common-fee rows, 41 bundle-pivot fee rows, and eight selective rows. Their minimum fees/surcharges are respectively `233/50000`, `7/10000`, and `133/12500`, all strictly positive. Common fees preserve the ranking of all nonempty masks and otherwise select empty. A selective item surcharge then lies in the proved four-option contraction cone. First-match boundary rules remain Borel and do not change this containment argument. The staged inherited tie algorithm is consistent with the direct shared-base rule: if the common stage selects empty, later positive price changes still select empty; otherwise the predecessor remains the projected base mask.

4. **The replacement chamber is unambiguous, including its boundary.** From `t>=d` and `rho<=b-d<d`, the high coordinate is unique. The closed chamber, its square-root transition comparisons, and the explicit branch formulas cover every real opponent report. At t=a the two base expressions coincide, and the final quadratic price formula is identical on both sides. All stated adjacent branch prices agree at their exact algebraic or rational transition.

5. **The replacement is a contraction of the same base.** In aligned coordinates its increments are `(f,f+delta,f+delta)`. The transition formulas imply f,delta>=0 on their respective branches. Lowering an inherited fee is therefore safe here because the final choice contracts the base, not because it contracts the inherited choice. Both bidders may be changed at once: their selected masks remain subsets of a single jointly feasible pair of base masks.

6. **The tie proof is complete.** If an old singleton is optimal, subadditivity makes the other singleton's utility nonpositive, and the surcharge inequality prevents the bundle from strictly overtaking the retained singleton. Hence a maximizing subset exists even at old positive ties. Choosing empty at zero utility is also a maximizer. The old bundle permits every new mask. This proves the three-step selection rule for every own report, every opponent report, and every chamber boundary, including outer faces and corners. Finite priority gives a Borel selection.

7. **DSIC and IR follow pointwise from the final menus.** Every final price depends only on the opponent, and the chosen own mask maximizes the final menu utility. The usual taxation inequality therefore holds against every own misreport. Empty gives IR. Positive nonempty prices force empty at zero own type. Selected payments lie in [0,2], ensuring integrability. Discontinuities of prices in the opponent parameter do not harm this own-report argument.

8. **The exact evaluator has the stated, narrower computational scope.** The mathematical definition covers real reports. The Python evaluator first converts reports to exact fractions and evaluates the only irrational branch in one quadratic field per conditional menu. Utility comparisons within that menu share the same radicand, and its exact sign rule is valid for the positive radicands used. The code does not purport to enumerate every real report or every algebraic tie. The all-real claim comes from the proof above.

## Proper-menu domain and four-ray conditions: PASS, with an endpoint precision correction

The area formula requires `0<A,B<1` and `max(A,B)<C<A+B`; it does not require C<=1. The singleton regions are rectangles of areas `(1-A)(C-A)` and `(1-B)(C-B)`. The bundle region is the upper-right rectangle with side lengths `1-C+B` and `1-C+A`, minus the triangle of leg `A+B-C`. That triangle fits precisely because A,B<=1. Thus crossing C=1 creates no omitted cell or sign change.

On the replacement, `C-A=c+delta>0` and `C-B=k>0`; the discount is the base discount plus f. A<1 for t<1. B is at most a<2/3: it decreases on the square-root branch because `d(C-k)/dk=k/C-1<0`, decreases on the quadratic branch because `3k/2-1<0`, decreases on the affine branch, and is constant after that. These establish the strict topology throughout d<=t<1.

The four extreme rays are correctly identified. The already independently checked polynomial identities give the common-fee cubic and item-surcharge quadratic. Before the first transition, beta<=0 and both singleton gradients are nonnegative. On the square-root branch beta=0 with both singleton gradients nonnegative. On the plateau G_A=Gamma=0 and G_B>0. On the affine branch G_A<0, Gamma=0, G_B>0. Thereafter G_A<=0, Gamma<=0, G_B>0. These identities imply all four directional derivatives are nonpositive.

**Precision item reported to the root investigator:** at t=1, A=1. Increasing A then crosses a menu topology, so the derivative of the polynomial continuation in A is not necessarily the actual right derivative. Continuity of revenue at A=1 does not justify continuing its gradient. The correct claim is the four-ray statement for `d<=t<1`, hence almost everywhere in the opponent chamber; the endpoint retains the full pointwise feasibility/DSIC proof and the continuous revenue value. The root investigator acknowledged this correction. It does not affect the mechanism or its revenue integral.

The construction is stationary only for these specified conditional price directions on the replaced chamber. The manuscript correctly leaves other globally admissible changes, lotteries, and unchanged opponent regions unresolved. No proof of unrestricted optimality is supplied or inferred.

## Candidate-specific weak certificate: algebra and support PASS

The signed-measure definitions expand with the correct signs. In the proposed gap identity, the alpha/beta utility terms cancel, the allocation moment terms cancel, the capacity-allocation terms cancel, and the remaining expression is `sum_j mu_j(Z)-Rev`, minus the normalization pairing, which is zero. Nonnegativity of all four remaining terms gives weak duality for the stated normalized Borel class. Finite measure mass and bounded normalized utilities/allocations justify all pairings, including singular measures on ties. No dual attainment assertion is needed.

For a selected report r with mask S, `u(r)=ell_S(r)`, so its exact IC slack against true type v is `u(v)-ell_S(v)`. Consequently the tight set is exactly the union of `A_S x E_S` on each opponent fiber. The distinction between closed active cells A_S and actually selected-report cells E_S is essential and handled correctly. All five proper-menu contact panels and the two price-cycle identities check directly. Under strict discount there is no exposed singleton/singleton panel.

A matching sum of nonnegative gap terms can vanish only when each measure gives full mass to its stated zero set. This supports the candidate-specific restrictions on lambda, sigma, mu, and tau. They are zero-set assertions in the actual Borel representative; they are not assertions about topological support inferred from an almost-everywhere allocation. The local polar decompositions also expand exactly and have the correct nonpositive signs on their corresponding branches. As with the gradient statement, they should be scoped to t<1.

**Full-class scope item reported to the root investigator:** the weak identity is explicitly stated for Borel mechanisms. If the original admissible class includes merely completed-Lebesgue measurable representatives, normalization alone does not make singular multiplier pairings well-defined on all such representatives. To extend the upper-bound conclusion to that larger class, explicitly invoke the preserved pointwise Borel-repair/attainment theorem equating revenue suprema, or otherwise prove that reduction. If Borel measurability is already part of the formal original class, no additional reduction is needed. This is a scope dependency of the prospective certificate, not a defect of the Borel candidate construction. No actual matching upper certificate has been claimed.

## Residual obligations

The numerical revenue expression and enclosure belong to the independent revenue audit. The two precision/scope items above should be reflected in the final text. The weak multiplier system itself remains unconstructed; the polar for four conditional price directions cannot replace it. Subject to those stated boundaries, this audit found a complete feasible DSIC candidate proof and a correctly signed candidate-specific certificate interface.
