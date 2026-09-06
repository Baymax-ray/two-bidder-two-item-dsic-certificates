# Mirror the full Q response with compatible joint ties

This intermediate trial returns to the fully evaluated V4.6 mechanism immediately
before the corner release (`outer_bundle_reoptimized`). It deliberately removes
the exact corner increment J, then replaces **both** bidders' menus on
Q={max(w)<=A, sum(w)<=b}, A=2/3, b=91/100, by the same full Q response.
It is separate from the literal strongest-baseline symmetrization experiment
in `sym_rescreen.md`. The later parameterized symmetric construction uses this
compatibility principle but does not inherit the frozen constants.

For opponent w, t=max(w), use empty and the two singleton/bundle options:

* t<=1/2: singleton prices A,A; bundle C=max(b0,sum(w)), b0=(4-sqrt(2))/3.
* 1/2<t<=A: k=t-q, q=113/500; scarce singleton A, safe singleton
  B=C-k, bundle C=max(5/6+3k^2/4,sum(w)). Scarce means the opponent's high item.

These replace the old position-1 menu on all Q; position 2 already had exactly
these menus. Outside Q, both menu correspondences are retained from the
pre-corner predecessor: Eplus has its five-option lottery and the other rows
have the retained V4.02/V3 menus.

## Complete tie architecture

At each report profile form the two finite sets of utility-maximizing menu
options, keeping empty available at zero. Select the lexicographically first
pair whose marginal allocations sum to at most one for each physical item.
The menu orders are empty, safe, scarce, bundle on constrained Q; empty,
item 1, item 2, bundle on free Q and retained rows; and the predecessor Eplus
order on lottery rows. The Python implementation enumerates at most 25 pairs.

This is an exact pointwise definition, not an after-the-fact deletion of an
allocation. We now prove the feasible pair always exists. A chosen menu
maximizer remains DSIC even if the choice among ties depends on both reports:
all available outcomes give the same utility at that report. Empty gives IR.
The finite menus and feasibility inequalities are Borel, so the lexicographic
selection is measurable. Their bounded prices imply integrability.

If neither report lies in Q, the predecessor's feasible pair uses exactly the
same menus and proves existence. If only one report lies in Q, either the
original or bidder-swapped pre-corner mechanism provides a feasible pair using
exactly the two desired menus. This step is about existence of a jointly
compatible pair, not equality of the two predecessors' asymmetric tie choices.

If both reports lie in Q, scarce singleton utility is nonpositive because
its price is A and all own coordinates are at most A. An empty-first maximizer
never selects it at zero utility. Safe singleton prices exceed 1/2, whereas
any own low coordinate is at most b/2<1/2. Thus a singleton, if selected, is
the own high item and can arise only when the two reports have opposite high
orientations. Two such singleton outcomes concern different physical items.

The only remaining conflicts involve a bundle. Two positive-utility bundles
are impossible since every bundle price is at least the opponent's sum:
they would require simultaneously sum(v)>sum(w) and sum(w)>sum(v).
For opposite high orientations, suppose v wins a bundle against w and w wins
its safe singleton against v. The bundle-versus-safe comparison at v gives

v_low>k(w)=w_high-q,

where a tie selects the safe item first. The singleton purchase at w gives

w_high>B(v)=C(v)-v_high+q >= v_low+q,

because C(v)>=sum(v). These strict inequalities contradict each other.
If one report has maximum at most 1/2, its opponent's free-Q singleton prices
are A, so the putative safe singleton has nonpositive utility; the same conflict
cannot arise. On all zero-utility or equality faces choose empty/safe as above.
This proves pointwise feasibility on the whole continuous domain and establishes
the lexicographic pair's existence, including exceptional reports.

## Full inner scope

The unchanged/free Q certificates and the raised diagonal Q certificates
continue to apply. Candidate feasibility was proved jointly above. Their
required occupied top traces are outside Q and retain strict predecessor
purchases. The diagonal bottom and x=1/2 traces now sell a strict bundle through
the mirrored Q menu because its price is below the fixed opponent's sum.
At b0 the diagonal charge vanishes, as in V4.6. Positive measures ignore isolated
line endpoints, while the mechanism still specifies them pointwise. Therefore
both bidders' Q menus solve their full randomized inner problems against the
new residual. No statement is made about optimality of all outside-Q fibers
or about a common unrestricted auction certificate.

## Exact conditional gap accounting

Let D0 be the exact V4 free-fiber gain plus the V3.1 constrained-fiber gain;
it equals the position-2 screening advantage over the symmetric V3 menu on Q
at the old split s0=1137/1000. All terms below are the explicit finite
algebraic/logarithmic expressions in the named predecessor verifiers, not
floating values.

Let s=142/125, theta=s-s0=-1/1000. In V4.02 notation, IQ(s) is the exact
full-screened Q revenue, BQ(s) the base-menu Q revenue, and M0Q,M1Q the frozen
joined-surcharge Q moments. The retained Q menu change is exactly

RetDelta = BQ(s)-BQ(s0)-3theta*M1Q+(3/2)theta^2*M0Q.

Let F_gain be the V4.6 free bidder-1 gain, G1_gain its bundle-exchange
bidder-1 gain, and G2_free_cost/G2_coupled_cost the two complete bidder-2
conditional costs in the bundle exchange with its coupled singleton response.
The exact remaining Q conditional advantage is

D = D0 + IQ(s)-IQ(s0) - RetDelta - F_gain - G1_gain
    + G2_free_cost + G2_coupled_cost.

The frozen V3 joined region on Q depends only on t, so its moments cover the
entire old Q surcharge contribution. F and G are the only subsequent changed
position-1 Q menus; the two G2 terms are the only changed position-2 Q menus.
Eplus and the final corner modifications have opponent maximum greater than A.
This proves the accounting identity without assuming a sampled revenue map.

Independent rational antiderivatives, square-root bounds, and logarithmic-series
bounds in the existing exact functions give

0.00002523224869194826477063167 < D
  < 0.000025232248691948264770631671.

The mechanism's exact revenue is R_V4.6-J+D, and its net gain is about
0.0000252283325640061. The certificate contains rational enclosures for D,
the net gain, and total revenue. Menu tie choices change revenue only on
conditional affine tie lines, hence on a four-dimensional null set by Fubini.
The exact continuous menu integrals therefore apply to the declared joint tie
rule. The bounded rational regressions supplement the all-real argument above.
