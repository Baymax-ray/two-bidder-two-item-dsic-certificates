# V4.8A: frozen-primal continuous stress master

The V4.6.1.1 mechanism, all conditional menus, its pointwise joint tie completion and its exact revenue are immutable. This note concerns only upper certificates. The baseline is the V4.6.2 common capacity price, including its conditional splice on W=[0,43/100]^2, all four old two-way flows, and the origin IR sink. The V4.7 endpoint rectangles are reserved for the separately integrated first-event weights.

## 1. Columns and exact incumbent complementarity

A column has one fixed bidder, two own endpoint centers A and B, a common own-offset rectangle K, a common opponent rectangle J, d=A-B, and amplitude lambda>=0. Its virtual correction is

    delta_phi(v;w)=lambda*d*(1_(A+K)(v)-1_(B+K)(v))*1_J(w).

Whole-box utility inequalities must place both endpoint boxes in the closure of the SAME incumbent own-affine menu cell. The resulting incumbent own allocations agree almost everywhere in offset and opponent report. The frozen pointwise tie rule remains in effect on null option interfaces; its selected allocation need not be constant there. All active menu branches, cell faces and capacity conditions used to prove the almost-everywhere assertion are checked over continuous boxes. Opposing-bidder allocations need not be identical. A column can connect different semantic profile regions while staying in one complete affine cell of the corrected bidder's conditional utility.

For every DSIC utility and its selected allocation, adding the two truthful IC inequalities gives

    K_column=lambda*integral_(K x J)
        d.[x(A+s;w)-x(B+s;w)] >=0.

For the incumbent this is exactly zero. Finite nonnegative sums, with arbitrary overlap, remain nonnegative and complementary. No numerical master constraint is substituted for this continuum property.

When both components of d are nonzero, the column is also the divergence of the continuous Lipschitz rank-one PSD field

    M(v;w)=lambda*dd^T*integral_0^1 1_K(v-B-td)dt *1_J(w),
    delta_phi=-div_v M.

Its compact support and regularity make the continuous-field/Hessian-measure pairing well defined. This is the SAME incentive term K_column, not an additional independent gain.

Axis-aligned d is legitimate in the integrated IC representation. Its rectangular corridor can have a transverse jump, so an arbitrary product of that field with a singular Hessian is not asserted. Own-coordinate positive mollification gives continuous PSD approximants, and the endpoint corrections converge in L1. If the endpoint boxes have uniform interior margins in the same affine menu cell, sufficiently small mollifications remain complementary. Alternatively the displayed IC integral directly proves the limiting virtual inequality without any Hessian product. The implemented certificate must say which representation is used.

The corridor may cross the own-report W square or the larger common no-sale set D. This does not introduce a boundary term merely because a semantic label changes inside the corridor. The opponent must remain outside W, and the endpoint corrections must leave the conditional splice intact. On profiles with an opponent in W, the inherited universal conditional support remains in use. Old cycle endpoints must either be excluded or included in the exact common endpoint partition.

## 2. Joint endpoint partition and whole-cell regret bounds

Take the common refinement of all endpoint boxes and the physical radial charts, together with any inherited support boundaries. On each positive-volume cell C, every column's physical virtual correction is constant, so the total shift to item j and option k is

    delta_(C,j,k)=sum_l A_(C,j,k,l)*lambda_l.

Option k=0 means unsold and has delta=0; k=1,2 are bidders. Coincident endpoints are added in this one matrix. They are not assigned disjoint gains. Distinct cells may touch on null faces, using a consistent half-open/Borel membership convention; the actual incumbent and its ties do not change.

Let phi_k be the baseline virtual values at a profile in C, including zero. For every k choose a rational L_(C,j,k) such that

    0<=L_(C,j,k)<=max_l phi_l-phi_k throughout C.

One convenient certificate is

    L_k=max(0,max_l lower_bound_C(phi_l-phi_k)).

The lower bounds use exact rational or directed polynomial/interval arithmetic after clearing strictly positive radial denominators. This does not require a fictitious unique old winner on every cell. For at least one option L_k=0, since a pointwise old maximizer has zero regret. The construction must independently check every claimed bound.

The full continuous envelope change then obeys pointwise

    max_k(phi_k+delta_k)-max_k phi_k
        <= max_k(delta_k-L_k).

Thus the convex piecewise-linear function on the right is a lifted continuous majorant of the true envelope change. Its validity allows winner changes inside C. A finite type-grid optimum is not used anywhere in this inequality.

## 3. Master and certified extraction

The joint master is

    minimize sum_(C,j) volume(C)*theta_(C,j)
    subject to theta_(C,j)>=sum_l A_(C,j,k,l)*lambda_l-L_(C,j,k)
               for every C,j,k,
               lambda_l>=0.

Theta is allowed to be negative. The zero-amplitude point has objective zero. Shared endpoint corrections are summed before taking the maximum, so their interactions and winner switches are covered.

A floating LP solution is discovery only. For acceptance, round nonnegative amplitudes to explicitly stored rational values and recompute every theta as the exact rational maximum of its three right sides. The negative of the resulting objective is a certified continuous gain G_master whenever positive. Neither numerical solver optimality nor a dual LP certificate is needed for this upper-bound validity. A finite-master optimality claim would require its own exact primal-dual check and would remain restricted to the chosen majorant and columns.

For pricing, a dual master weight y_(C,j,k)>=0 obeys sum_k y_(C,j,k)=volume(C). A candidate column's reduced cost is sum A*y. A negative value identifies an improving column for that master. The separation search can use these weights, current virtual-winner differences and atlas priorities to propose pairs. Whole-box menu and field verification is required before insertion. Failure to find another column is neither a proof of full separation nor evidence that the incumbent is suboptimal.

## 4. Whole-auction upper and all remainder terms

Let phi_new be the aggregate corrected field. Define the common capacity price as its nonnegative virtual maximum outside the inherited splice, retaining the old conditional price on the splice. Pointwise nonnegativity and itemwise dominance hold by definition. The inherited conditional identity plus the nonnegative column IC terms proves

    H_1(Pi_new)=H_2(Pi_new)=0,
    OPT<=integral sum_j Pi_new,j.

The empty mechanism attains the charged value zero. This is a bound on arbitrary jointly measurable randomized pointwise-DSIC/IR mechanisms with bounded marginal allocations, not on the incumbent's finite menu.

For every feasible mechanism, the exact identity contains conditional-screening, priced-capacity, virtual-allocation, inherited IC/IR and new column-IC terms. For the frozen incumbent, screening and origin IR are zero, old weighted IC remains 9/7812500000, and all new column terms vanish. Only its capacity/virtual slack changes.

Write G_event_true for the exact first-event gain, enclosed by [G_event_lo,G_event_hi], and G_master_true for the actual aggregate master decrease. Reserved endpoint disjointness gives

    integral Pi_new = integral Pi_old-G_event_true-G_master_true,
    G_master_true>=G_master.

If U_old has inherited remainder E_old, the certified endpoint

    U_new=U_old-G_event_lo-G_master

has exact surplus

    E_old+(G_event_true-G_event_lo)+(G_master_true-G_master).

The event-integration enclosure and master-majorant slack must be recorded separately from inherited E. If an existing atlas lower enclosure E_lo is reused, subtract it separately and replace E_old by E_old-E_lo in this formula. Such a subtraction is inherited numerical-remainder recovery, not evidence that new PSD stresses repair allocation disagreement.

No certificate here asserts that a finite stress library is complete. The independent affine-cell flux obstruction is a different, basis-independent argument, with explicitly stated support and trace hypotheses. It must not be replaced by numerical nonfinding.
