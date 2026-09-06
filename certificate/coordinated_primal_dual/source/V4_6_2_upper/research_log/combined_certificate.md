# The final global capacity measure and complete gap identity

Let W=[0,43/100]^2 and let Psi be the nonnegative, absolutely continuous
single-buyer support in conditional_global_splice.md. It has zero density
on W, total mass R0=4/9+2sqrt(2)/27, and the universal identity
`<Psi,a>-R=3 integral_D0 u` for every complete randomized DSIC/IR utility.

Let phi_i be the frozen rational stream field. Add the four disjoint
long-range cycles in sparse_cycle.md to obtain phi'_i. Their support is
disjoint from all profiles on which either bidder reports in W.
Define the final common capacity density in physical item coordinates by

    Pi'_j(w,v) = 0                         if w,v both belong to W;
                 Psi_j(v)                if w in W, v outside W;
                 Psi_j(w)                if v in W, w outside W;
                 max(0,phi'_1j,phi'_2j)   if both are outside W.

This specifies a finite nonnegative Borel measure on the whole continuous
report space. At the radial origin the fields may be defined as zero;
the identities retain the appropriate IR sink at the zero type. The
positive parts are integrable. All added nonlocal flows are finite and
nonnegative and leave opponent reports fixed.

For each bidder i, split its conditional menus according to whether its
opponent belongs to W. On that opponent region use the universal Psi
screening inequality. Outside it use the exact stream envelope plus the
actual added two-way IC inequalities. Whenever the bidder's own report
is in W, its old virtual values are nonpositive and there is no cycle
correction. On the remaining profiles Pi' dominates its modified field.
It follows for every jointly measurable full randomized DSIC/IR mechanism
for that bidder, with only marginal allocation bounds, that

    R_i - <Pi',a_i> <= 0.

The globally empty mechanism attains zero. Hence the unrestricted charged
screening values are exactly

    H_1(Pi') = H_2(Pi') = 0,
    OPT <= integral sum_j Pi'_j.

Solving these charged values is not a claim that empty is a good auction:
it leaves all positively priced capacity unused. Equality of the whole
auction bound still requires simultaneous capacity and incentive equality.
No exchange of an uncountable supremum and a measurable integral is used.

## Four mechanism slacks

Let O_i denote the opponent-in-W region. For every complete feasible
auction with utilities u_i and actual selected allocations a_i, define

    S_screen = sum_i 3 integral_{O_i} integral_{D0} u_i;
    S_capacity = sum_j integral Pi'_j (1-a_1j-a_2j);
    S_virtual = sum_ij integral_{O_i complement} (Pi'_j-phi'_ij) a_ij;
    S_IC = sum_i integral_{O_i complement} u_i(0;opponent)
             + sum_over_added_edges integral weighted truthful IC residual.

The last term uses the actual finite two-way flows from sparse_cycle.md.
Their source-target mass balances, so no extra sink is introduced. The
existing origin sink is separately visible; there is no positive interior
sink hidden at a type with positive information rents. All four slacks
are nonnegative, and exactly

    integral Pi' - (R1+R2)
       = S_screen + S_capacity + S_virtual + S_IC.

The screening theorem's internal IR and trace terms belong to S_screen.
They are not counted again as separated-report IC slack. The four-way
identity applies to the entire original randomized pointwise class.

## Certified numerical envelope and its remaining remainders

Let B denote the exact integral of the original stream's virtual maximum,
B20 its independently replayed depth20 upper, and D the exact total
reduction from the two conditional-support replacements. Let d1024 be
the corrected exact lower bound on D. The cycle reduction g=81/10^10 is
an exact change of the continuous maximum, because all affected winners
remain strict throughout their complete profile boxes. Therefore

    integral Pi' = B - D - g;
    U_final = B20 - d1024 - g.

The remaining certification remainder is explicitly

    E = (B20-B) + (D-d1024) >= 0.

The first term is the Bernstein envelope and directed-rounding remainder.
The second consists of omitted nonnegative SJA-boundary-cell slack and
the nonnegative gap in the cellwise Jensen inequalities. Neither is a
mechanism incentive slack. If an exactly four-category decomposition of
the reported numerical gap is desired, define
`S_virtual_certified = S_virtual + E`; then

    U_final-(R1+R2)
      = S_screen + S_capacity + S_virtual_certified + S_IC.

This accounts for every term rather than silently labeling integration
error as complementary slackness. The 16-stage ledger records rational
upper bounds, not an assertion that this fixed architecture converges to
OPT.

## A verified obstruction remaining on the lower candidate

The V4.6 auction has bidder 1 empty and bidder 2 allocation (1,beta),
4/5<beta<19/20, on the open box stated in flatness_global_equality.md.
That box is untouched by the conditional splice and the added cycles.
Thus Pi' there is the original virtual maximum. For the safe item,

    capacity slack + virtual slack
       = Pi'_safe - beta*phi_2safe >= |phi_2safe|/20.

The replay remaining_lottery_slack.py independently reconstructs the
rational numerator of phi_2safe and proves its absolute value is bounded
strictly away from zero on a rational subbox centered at
`(151/200,3/40,9/10,13/40)`, halfwidth `1/10000`. The numerator's whole-box
Taylor bound, positive denominator, subbox inclusion, and disjointness
from all eight cycle rectangles are exact. It consequently gives a strict
rational lower bound on S_capacity+S_virtual for the final dual versus
V4.6. This does not prove the V4.6 mechanism suboptimal; it proves this
specific final dual is not matching.

The broader analytic obstruction explains why merely optimizing a finite
polynomial curl cannot make the required zero plateau: the field is
analytic on each open radial chart and retains a noncancelable radial
pole. Any exact common certificate matching the current lottery region
must change that local dual representation or the primal allocation.

## Cross-check against the parallel V4.6.1 candidate

The stronger selected lower mechanism also has a verified positive lottery-region gap for this same final dual. See [current_lower_flatness.md](current_lower_flatness.md) for the complete all-real selections on a separate box, its disjointness from both branches' functional changes, and an exact negative safe-field bound. This diagnostic changes neither Pi prime nor the upper ledger. The current combined endpoint comparison is stored separately in certificate/current_bound_comparison.json.
