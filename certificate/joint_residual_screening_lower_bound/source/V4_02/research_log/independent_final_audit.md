# Independent final mechanism and derivation audit

Audit date: 2026-09-05. This bounded audit was performed independently of the candidate author while another investigator checked the numerical revenue integrals. It is not peer review or formal verification.

## Verdict

The split-cost continuation has a complete pointwise DSIC/IR and joint-capacity proof. Its theta=0 member recovers the frozen V3.1 allocation, payment, utility, and conditional-menu rules, including the meaningful boundary ties. The Q replacement is justified at the changed residual by the existing full randomized inner certificate. The global revenue decomposition and the frozen-increment correction formula are consistent with this actual mechanism. No blocking mathematical gap was found in these claims.

The candidate is a new feasible lower construction. Neither optimality over the split-cost family nor unrestricted auction optimality follows from this audit or is asserted by the reviewed derivation. The independent numerical-integration audit is responsible for the final enclosure and strict aggregate gain.

## Files and checks

Read `verifier/split_cost_candidate.py`, `research_log/split_cost_independent_audit.md`, `verifier/split_cost_revenue.py`, and `research_log/split_cost_revenue_derivation.md`. Checked the relevant frozen implementation in `V3_1/verifier/constrained_candidate.py` and the theorem/scope in `V3_1/research_log/constrained_screening.md` and `closed_region_independent_audit.md`. The candidate-owned files were not modified.

Read-only execution of `split_cost_candidate.py` passed: its 103 bounded exact checks include theta=0 comparisons, changed free/constrained boundaries, top-edge ties, the strict reallocation witness, and the slanted-prism vertices. These finite checks supplement the analytic proof; they do not prove continuum feasibility by themselves. The aggregate revenue replay was deliberately left to its separate auditor.

## 1. Recovery at theta=0 is pointwise, not merely in revenue

The retained increment is defined by the complete frozen V3 menu minus its original base menu, at the same opponent report. At theta=0, adding it to the new base reproduces the exact original menu, including the closed joined chamber and the inherited first-match boundaries. The common new base then has exactly the old costs, outcome order, and selected joint maximizer.

The direct maximizing-subset tie rule agrees with the frozen staged rule. If a common-fee stage previously selected empty, later nonnegative increases cannot create a positive alternative; both rules choose empty. Otherwise its predecessor is the same projected base mask, and both choose that mask when it maximizes, or the smallest maximizing subset. This includes positive base ties and zero-utility rejection.

Outside Q, the V4 free-fiber replacement is absent because its support is a subset of Q. Hence the frozen V3.1 rule there is the retained V3 rule. Inside Q, the new screening rule at theta=0 uses the same closed test, the same split at t=d, identical SJA prices and priority on free fibers, and identical scarce/safe menu and priority on constrained fibers. In particular t=d is explicitly free; it is not assigned by continuity from t>d. At t=2/3 and sum(w)=b the same closed-Q convention applies. Branch labels in diagnostic dictionaries need not coincide, but the mathematical mechanism does.

## 2. Frozen increments remain valid relative to the new base

The frozen increment has zero empty price, nonnegative singleton increments, and bundle increment equal to their maximum. This is the portable common-fee plus one-item-surcharge structure proved for V3. It does not require the nonlinear final menu itself to be an affine maximizer.

For every |theta|<=1/1000 the new base has strict discount at least q'=s'-b>0, since b<s'<2a. The generic maximizing-subset lemma therefore applies to its actual selected mask at every report. Both bidders' retained choices are subsets of the same new shared allocation, so they are jointly feasible. No containment in the old shared allocation is claimed or needed.

The final prices depend only on the opponent. Selecting menu maximizers proves DSIC for every own report and misreport. Empty gives IR; the positive price floors give normalization at zero. Finite mask choices with explicit priorities and the Borel frozen increments give a Borel mechanism. Selected payments are between zero and the selected value, hence bounded by two.

The pointwise mechanism proof admits both signs of theta in the stated interval. The exact aggregate revenue calculation is restricted to theta in [-1/1000,0], and the concrete reported candidate uses theta=-1/1000. These scopes should remain distinct.

## 3. Actual new residual and complete Q splice

For t<=d', all bidder-1 singleton prices are at least d' and its bundle price is at least b. Since w belongs to Q, all its utilities are nonpositive, and null-first selection makes it empty for every bidder-2 report. This includes t=d' and sum(w)=b, so the SJA replacement has genuinely full capacity there.

For d'<t<=2/3, the low coordinate is strictly less than d' because rho<=b-t<b-d'<d'. Bidder 1 can receive only its high-coordinate item or nothing. Its low singleton is unaffordable; its bundle cannot have positive utility. The second item is therefore fully available to bidder 2 everywhere on the fiber.

The candidate scarce singleton is safe because x>=2/3>=t and the new base price paid by bidder 1 is at least x (or x+q'). A candidate bundle is safe by x>=k and x+y>=C. If y>d', its base price is at least x+q'>=t. If y<=d' and t<=a, its price is at least a>=t. In the remaining case, the price is at least C-c, and the uniform strict margin

`C(t-q')-c-t >= 9247/250000 >0`

has its asserted minimum at t=2/3, theta=1/1000. Equality cases where a lower bound is only t give zero utility to bidder 1 and are handled by its null-first rule. Thus even the boundary maximizers are safe; the explicit safe-singleton priority additionally avoids allocating the scarce item at the internal x=k tie.

The same full-inner certificate applies through feasibility and support saturation. On x>2/3 the actual scarce residual is one. On the top edge y=1, frozen increments vanish and the scarce price is exactly d' for x<=c and x+q' for x>c; thus the residual is zero for x<k and one for x>=k, including the explicit zero-utility tie. The safe item has capacity one everywhere. The candidate saturates these positive-measure supports and has zero utility on D_0.

This uses the general V3.1 gap identity, not the stronger diagnostic hypothesis that all interior holes lie in x<=k. That stronger assertion is neither needed nor generally available for t>a. The parameter c<k<=2/3-(q-1/1000) lies strictly inside the certificate's proved range [(2-sqrt(2))/3,2/3]. Accordingly the Q inner-optimality claim covers the full randomized DSIC/IR inner class at the actual changed residual. It does not cover the retained bidder-2 rule outside Q or establish a common full-auction upper certificate.

## 4. Global revenue accounting and boundary movements

Before the Q splice, both bidders use the same new-base-plus-frozen-increment rule. Their expected revenues are equal by bidder symmetry outside the null tie sets. Therefore

`R(s)=2 r_base(s)+2 F_all(s)+I_Q(s)-B_Q(s)-F_Q(s)`

is the correct replacement accounting. It includes the changed bidder-1 revenue; it does not attach a new inner value to an unchanged outer term.

All positive-measure frozen-increment supports have exactly one opponent coordinate above d_s and the other below it over the revenue parameter interval. Thus only the aligned low-item singleton price B changes by theta there. The support menus remain in the strict discounted topology with A,B<1, although C can exceed one. The elementary cubic change in G as B moves is correct.

For increments (alpha,beta,beta), adding the increments preserves the base gap C-B at a fixed s. At the original parameter the common gap is t-q0; at parameter s0+theta both the retained and base gaps are t-q0-theta. Their revenue-correction difference is exactly

`beta[-3(t-q0)theta+3theta^2/2]`.

The four global/Q moments therefore have the stated coefficients and signs. Their factor two counts item orientations; the later factor two in 2F_all counts bidders. The bundle-box Jacobian is L(z), and t-q0=z-d0-eta L(z), giving the displayed moment formulas. A finite rational comparison of the 41 source rectangles found no pair with positive-area overlap. Their intersection with Q is only the boundary sum=b, so omitting them from the Q moments is correct for revenue while preserving the original first-match pointwise rule.

The formula for B_Q includes its moving threshold t=d_s. The formula for I_Q includes both the changing free-area term and the moving lower limit of the constrained integral. In particular the free value at t=d_s is not replaced by the limit V_c from the constrained side. The derivative's corresponding boundary term uses the difference between these values. Thus this potentially material boundary movement has not been dropped.

The affine-base derivative and change polynomial were independently derived in `base_split_cost.md` and handle high-price menus as well as the proper-menu region. The final gain is a finite-step integral for theta=-1/1000, rather than an inference from the sign of an infinitesimal derivative. Its numerical evaluation is outside this audit's assigned scope.

## 5. Strict reallocation and claim boundaries

The slanted-prism argument is valid on the complete real prism, not just its checked vertices. Its independent coordinates have determinant-one conversion to reports. The old split-versus-bundle score difference is -h, while the new difference is epsilon-h. Both have a strict sign throughout the prism. Frozen increments vanish there, bidder 1 obtains utility epsilon-h>=epsilon/4 after the change, and bidder 2 switches strictly from bundle to its safe singleton because x lies strictly between its old and new scarce thresholds. This proves a positive-volume change outside the old base allocation's containment set. It alone does not determine the aggregate revenue sign; the global accounting above does that separately.

The reviewed texts explicitly do not claim the new split cost is optimal even within its own family, do not claim all residual fibers are solved, and do not claim a matching upper bound for the unrestricted randomized auction. These restrictions are mathematically necessary.

## Minor editorial corrections reported to the root

1. In the revenue derivation, the phrase that C-B=t-q0 is unchanged should specify that it is preserved by adding frozen increments at s0. As s changes, both gaps equal t-q0-theta. The displayed correction formula is already correct.
2. The revenue derivation referred to `split_cost_candidate.md`, whereas the available complete mechanism proof is `split_cost_independent_audit.md`. The final document should link to the actual proof file or supply the named alias.

Both corrections were subsequently applied by the root investigator and independently re-read in the final revenue derivation: the parameter dependence of C-B is now explicit and the proof link names the existing audit file. Neither item changed the mechanism or algebra. No unresolved blocking issue remains from this bounded proof audit, subject to the stated scope and the separately assigned revenue-enclosure verification.
