# V3: globally admissible revenue variations

This note gives complete mechanism transformations and necessary revenue tests. It does not assume a common potential, a finite allocation range, or a finite type grid unless a particular subsection says so. It does not identify the unrestricted optimizer. All statements concern the original uniform two-bidder, two-item model, with additive expected utility, pointwise DSIC, and pointwise joint feasibility. The constructions include exceptional reports and ties.

## 1. A universal participation-fee transformation

Write a normalized mechanism's own utility, allocation row, and payment as

`u_i(v,w)=v.x_i(v,w)-p_i(v,w)`, `u_i(0,w)=0`.

For every fixed opponent report, u is convex, nonnegative, and x is a supporting vector at every own report. Fix any bounded Borel function `e_i(w)>=0`. Define

`u_i^e(v,w)=max(u_i(v,w)-e_i(w),0)`.

Retain the original allocation row if `u_i(v,w)>=e_i(w)` and erase it otherwise. On retained reports charge `p_i+e_i`; on erased reports charge zero. At equality this specifies retention, including the case e=0. Apply the transformation to either bidder or both bidders independently.

**Theorem 1.** This is a complete Borel, pointwise DSIC, normalized IR, jointly feasible mechanism. It applies to arbitrary original lotteries, including infinitely many allocation rows.

**Proof.** Above the cutoff, the old supporting inequality supports `u-e`, hence supports `max(u-e,0)` at the selected old row. Below it, zero supports the new utility. At equality both the old row and zero are supporting vectors, so retention is valid. The formula for payment is exactly `v.x^e-u^e`. Normalization follows from e>=0, and nonnegativity gives IR. Every new allocation coordinate is either the old coordinate or zero. Consequently both bidders may be transformed simultaneously without exceeding any old item capacity. The selection and payments are Borel. Payments remain nonnegative and at most 2: on retained reports `p+e=v.x-u+e<=v.x<=2`. This proof uses neither nested original lotteries nor an allocation representation shared between bidders. QED.

The menu interpretation is a common added fee on every nonzero allocation, followed by choosing the zero outside option when all such choices become unattractive. Their relative ranking is unchanged. Convex utility truncation is the formulation that also works without a finite menu.

### Exact revenue identity and the forced moving set

Fix w and suppress the bidder index. Conditional expectation below is over the full own square. For e>=0,

`Delta(e;w)=e Pr[u>=e]-E[p 1_{u<e}]`.                                      (1)

For the uniform square the normalized radial virtual-revenue field is

`c(v)=v(3/2-1/(2 max(v_1,v_2)^2))` for v!=0, and c(0)=0.

The normalized envelope identity gives the equivalent formula

`Delta(e;w)=- integral_{u(v,w)<e} c(v).x(v,w) dv`.                         (2)

Indeed the allocation change is precisely `-x 1_{u<e}` and the radial identity is linear in the allocation. Its coefficients are integrable on the square. Equation (2) integrates over an **entire utility sublevel set**. Selecting just its profiles with negative pointwise virtual revenue generally fails IC.

For a normalized revenue optimum,

`e Pr[u>=e] <= E[p 1_{u<e}]` for all e>=0, for almost every w.             (3)

The qualifier concerns the revenue necessity, not the construction: the construction is pointwise for every w. To prove (3), conditional gains are Borel and continuous in e. Every positive level set of u has area zero: along each ray from zero, convexity and u(0)=0 make a positive level cross at most once. At level zero, x=0 and p=0 almost everywhere on the zero-utility set, by differentiability of a convex function almost everywhere. Dominated convergence now gives continuity, including at zero. If (3) failed on a positive-measure set of opponents, a fixed rational e would give positive gain on such a set; use that fee there and zero elsewhere. This contradicts optimality. It suffices to consider e in [0,2].

This is a candidate-specific separating test. A negative integral in (2) certifies suboptimality by providing a better complete mechanism. Nonnegative integrals for all fees do not certify unrestricted optimality.

### Convex utility thinning adds no new revenue direction beyond these fees

Let h:[0,2]->R be convex and nondecreasing, h(0)=0, with all slopes in [0,1]. Choose a Borel subgradient theta(u) in [0,1], set `U=h(u)`, `X=theta(u)x`, and `P=v.X-U`. The composition supporting inequality proves DSIC. Coordinatewise contraction proves joint feasibility even when both bidders are transformed. This includes new lotteries.

Such an h has a hinge representation

`h(z)=a z + integral_(0,2] (z-e)_+ d mu(e)`, `a>=0`, `a+mu((0,2])<=1`.

Apart from tie sets of zero revenue measure, its revenue is the same mixture of the original mechanism and the fee mechanisms, with the remaining mixture weight on the zero mechanism. Therefore if the original mechanism has nonnegative revenue and every fee test (3) passes, no transformation in this utility-thinning class improves revenue. This limitation of the class is a consequence of the representation, not evidence against more general lotteries.

## 2. Entry-frontier balance for finite menus

Suppose a conditional menu has finitely many nonzero rows r with prices p_r, as well as (0,0). Let D_r be their original choice cells when the zero option is temporarily omitted, with any fixed measurable resolution of ordinary menu ties; the zero option is still available in the actual mechanism. After adding a common fee e, each positive cell is intersected with `v.r>=p_r+e`. At regular levels,

`R'(e)=sum_r |D_r intersect {v.r>=p_r+e}|`

`        -sum_r (p_r+e) H^1(D_r intersect {v.r=p_r+e})/||r||`.             (4)

This is coarea applied to the complete moving entry frontiers. The first term is the extra fee collected from retained types; the second is the payment lost at the entry frontier. Formula (4) holds at almost every e, and at a level where all cell intersections have the ordinary stable geometry. If a level coincides with a positive-length cell interface, use the exact identity (1) or the appropriate one-sided limit, rather than double-counting a shared edge. The mechanism transformation itself remains valid at every e.

Only upward fees are automatically admissible. Equality `R'(0)=0` is not a necessary condition at a general optimum: the valid necessity is `R'(0+)<=0`, when that derivative exists. Decreasing a current fee can admit reports whose allocation conflicts with the other bidder. A two-sided stationarity equation requires a separate all-profile capacity proof for the reverse change.

## 3. Exact fee polynomial for the three-price deterministic menu

Let the current conditional singleton and bundle prices be A,B,C and assume

`0<A,B<1`, `max(A,B)<C<A+B`.

For `0<=e<min(1-A,1-B)`, put D=A+B-C. The selected areas after a common fee are

`a_1(e)=(1-A-e)(C-A)`,

`a_2(e)=(1-B-e)(C-B)`,

`a_12(e)=(1-C+B)(1-C+A)-(D+e)^2/2`.

The bundle area is its upper-right rectangle minus its lower-left entry triangle. The singleton/bundle comparison boundaries remain fixed; all entry boundaries move together. Therefore

`R(e)=(A+e)a_1(e)+(B+e)a_2(e)+(C+e)a_12(e)`

`     =R(0)+beta e-(3C/2)e^2-e^3/2`,                                    (5)

where

`beta=1+(3/2)(A^2+B^2+C^2)-3C(A+B)`.

Thus beta>0 yields an exact, globally feasible improvement for every sufficiently small positive e; beta<=0 excludes improvement by all additional fees within this topology. If beta>0, the stationary fee is

`e_*=-C+sqrt(C^2+2 beta/3)`.

This is the maximizing fee in this interval if it lies inside the interval. It is not necessarily the globally optimal fee after topology changes, and it is not an unrestricted mechanism optimum. The full conditional price functions may depend arbitrarily on the opponent and need not come from a common potential.

## 4. A larger admissible price cone for subadditive four-option menus

The following construction was proposed by the V3 root investigator and independently checked here. Suppose the original conditional menu is exactly the deterministic options empty, item 1, item 2, both, with prices 0,A,B,C and `C<=A+B`. Select any original utility-maximizing option at every report, including all ties. Change the prices by

`dA>=0`, `dB>=0`, `dC>=max(dA,dB)`.

**Theorem 2.** At every report there is a new utility-maximizing option that is an itemwise subset of the original selected option. Choose such an option by a fixed finite priority. The resulting allocation is DSIC for this bidder and is coordinatewise no larger than its original allocation. Hence it preserves joint feasibility while leaving the other bidder unchanged, or while making an independently justified contraction to the other bidder.

**Proof including ties.** If the old choice is empty, all old utilities are nonpositive and the new nonempty prices are no smaller, so empty remains a maximizer. If the old choice is item 1, comparison with the old bundle gives `v_2<=C-A<=B`. Consequently the new item-2 utility is nonpositive. Also the new bundle utility is no larger than the new item-1 utility because its relative price increased by `dC-dA>=0`. Thus a maximum exists among empty and item 1. The item-2 case is symmetric. If the old choice is the bundle, every option is its subset. Selecting a maximizing subset is Borel and satisfies the ordinary menu support inequalities at every report. QED.

The original menu, not the changed menu, must satisfy subadditivity for this proof. The changed menu may cross into a different topology. A blanket assertion that any monotone increase of arbitrary lottery prices contracts allocations would be false; Theorem 2 uses the particular four deterministic options and the displayed inequalities.

The cone has extreme rays `(0,0,1)`, `(1,0,1)`, `(0,1,1)`, `(1,1,1)`. In the strict topology of Section 3, write G(A,B,C)=R(0). Direct area differentiation gives

`G_A=(C-A)(2-3A)`,

`G_B=(C-B)(2-3B)`,

`G_C=1-4C+2(A+B)+(3/2)C^2-(3/2)(A^2+B^2)`.

A revenue optimum having these conditional menus must satisfy, for almost every opponent where the strict topology holds,

`G_C<=0`, `G_A+G_C<=0`, `G_B+G_C<=0`, `G_A+G_B+G_C<=0`.                   (6)

The last expression is beta. The first three can detect improvements that a common entry fee misses. These are one-sided cone conditions. They neither characterize all globally admissible changes nor establish global optimality when they hold.

### The item surcharge has an exact quadratic gain

For the ray `(0,1,1)`, put `Gamma=G_B+G_C`. As long as `0<=delta<1-B`,

`G(A,B+delta,C+delta)-G(A,B,C)=Gamma delta-delta^2`.                       (7)

The second derivative along this ray is identically -2. The proper-discount inequalities persist because C-B and A+B-C are unchanged. No assumption `C+delta<1` is required: the bundle price may cross 1 while the same area formula remains valid. Thus `delta=Gamma/2` is the maximizing surcharge within this regime when Gamma>0 and this value is below 1-B. The ray `(1,0,1)` has the symmetric statement. Equation (7) describes a complete item surcharge and its induced whole-cell movements, including bundle-to-singleton as well as entry movements.

### Independent check of the root investigator's S-chamber construction

Let `a=159/250`, `c=137/500`, `d=501/1000`, `q=d-c=227/1000`. On the S opponent chamber, the proposed feasible base conditional menu is `A=t`, `B=d`, `C=t+c`, with `a<=t<=1`. Set `k=t-q`. For common fee f>=0 and item-2 surcharge delta>=0, the changed prices are

`A=t+f`, `B=d+f+delta`, `C=t+c+f+delta`, with `C-B=k`.

Here

`Gamma=1-2B-2k+2A+(3/2)(k^2-A^2)`.

Interior stationarity in f and delta gives Gamma=0 and `G_A=0`; since C>A, the latter forces A=2/3. The resulting formulas are

* for `a<=t<=2/3`: `f=2/3-t`, `delta=1/6-c+3(t-q)^2/4`;
* for `2/3<=t<=t0`: `f=0`, `delta=1/2-c+3q^2/4-3qt/2`;
* for `t0<=t<=1`: `f=delta=0`,

where `t0=(1/2-c+3q^2/4)/(3q/2)`.

These formulas and their continuity have been independently checked algebraically. Delta is positive on the first interval; on the second it decreases linearly to zero. The largest B is its value at t=a and is less than 11/20. The inequalities `C>A`, `C>B`, and `C<A+B` hold throughout, and A<1 away from the outer endpoint t=1. Therefore crossing C=1 does not invalidate the revenue formula. At t=1 the complete menu construction and subset tie rule remain valid; revenue is obtained by continuity.

The changes relative to the base are `(f,f+delta,f+delta)`, in the cone of Theorem 2. Thus they contract the base allocation pointwise. Replacing a previous mechanism with smaller fees is safe by this proof only if the entire final mechanism, including the unchanged opponent chambers, contracts the same jointly feasible base. It need not contract the previous fee mechanism. This is a required mechanism-specific check for the root package.

These stationarity formulas concern the two-dimensional fee/surcharge family. Their derivation and contraction property do not establish unrestricted optimality or a matching global dual bound.

### Z-to-S active-constraint transition

The root investigator subsequently extended the same construction into the adjacent Z chamber, whose base prices are `A=a=b-c`, `B=b-k`, `C=b`, with `b=91/100` and k=t-q. Define

`k_start=sqrt(b^2-2/3-c^2)`, `k_plateau=sqrt(4c/3-2/9)`.

Their squares are positive and `d<q+k_start<q+k_plateau<a<2/3`. Before k_start no fee or surcharge is used. On `k_start<k<k_plateau`, the common-fee-only stationary solution is

`C_*=sqrt(2/3+k^2+c^2)`, `A=C_*-c`, `B=C_*-k`.

Indeed substituting A=C-c and B=C-k into beta gives `1-3C^2/2+3(c^2+k^2)/2`. At this solution `Gamma=-G_A=-c(2-3A)<0`, so the nonnegative item surcharge is correctly inactive. At k_plateau, A reaches 2/3. The next branch is

`A=2/3`, `B=5/6-k+3k^2/4`, `C=5/6+3k^2/4`.

It has Gamma=G_A=0. In Z it uses `f=2/3-a` and `delta=1/6-c+3k^2/4`; in S it uses `f=2/3-t` and the same delta. Thus there is no price discontinuity at the affine-base pivot t=a. The opponent widths also match: Z has low-coordinate width b-t, which is c at t=a, and S has width c. These formulas identify the transition between active nonnegativity constraints in the admissible cone. They are independently algebraically checked; the root package supplies the complete opponent partition and revenue integration.

All four local cone inequalities (6) hold on these Z/S branches. On the common-only branch beta=0 and both G_A,G_B are positive, so G_C is negative and the individual item-ray derivatives are negative. On the plateau G_A=0 and Gamma=0, while B<2/3 implies G_B>0 and G_C<0. On the subsequent S surcharge branch G_A<0 and Gamma=0; beyond t0 both G_A<0 and Gamma<=0. Before the Z start, beta<=0 and both singleton gradients are positive. This closes the four specified local price directions on these chambers. It does not close other globally admissible directions.

## 5. Binary interfaces: integrate the whole projection fiber

For two fixed feasible joint outcomes A and B, write `d_i=A_i-B_i`, assume both d_i are nonzero, and set `s=d_1.v_1`, `t=d_2.v_2`. On their full scalar ranges choose a continuous nonincreasing threshold phi. Select A exactly when `s>=phi(t)`, and B otherwise. This is a complete mechanism, including a specified tie rule.

For bidder 1 a supporting utility is

`B_1.v_1+(s-phi(t))_+-(-phi(t))_+`.

For bidder 2 the A-region is an upper interval in t at fixed s. Let kappa(s) be its lower endpoint, clipped to the full t-range when that interval is empty or full. Its supporting utility is

`B_2.v_2+(t-kappa(s))_+-(-kappa(s))_+`.

Endpoints may receive either tied row; the stated selection supplies a supporting row there. These separate utilities prove pointwise DSIC and IR. Both possible joint outcomes are feasible. Thus a deformation of phi preserving monotonicity gives a complete globally admissible change, without a common affine envelope.

Let f_i be the pushforward density of the uniform square under `v_i -> d_i.v_i`. Define the integrable projected virtual-revenue density

`m_i(s)=integral_{d_i.v_i=s} c(v_i).d_i / ||d_i|| dH^1(v_i)`.

Then, since a constant allocation has normalized revenue zero,

`R(phi)=integral integral_{s>=phi(t)} K(s,t) ds dt`,

`K(s,t)=m_1(s)f_2(t)+f_1(s)m_2(t)`.

At a perturbation `phi_e=phi+e h`, supported away from the outer projection boundaries and preserving nonincreasingness, assume K is continuous on a neighborhood of the compact graph patch (or that its traces satisfy a justified dominated differentiation rule). Then

`dR(phi_e)/de at 0 = -integral h(t) K(phi(t),t) dt`.                       (8)

One must integrate over each full product of the two perpendicular report fibers before making this comparison. If `phi'` is bounded strictly below zero on the patch, arbitrary smooth compactly supported h of both signs are admissible for sufficiently small e, so stationarity implies `K(phi(t),t)=0` there. At flat segments only monotonicity-preserving directions are allowed and one obtains variational inequalities instead. This is a necessity within the globally binary mechanism class. A patch of a larger mechanism cannot inherit these deformations without checking its other interfaces and junctions.

### Exact nonlinear witness and its improvement

For the V2 nonlinear one-item mechanism `v_11>=h(v_21)`, where `h(y)=y/(2-y)`, both item-2 coordinates are ignored. For any increasing homeomorphism h:[0,1]->[0,1], winner critical payments give

`R(h)=integral_0^1 [2y h(y)-h(y)^2]dy = 1/3-integral_0^1(h(y)-y)^2dy`.

Therefore `h_e=(1-e)h+e id`, 0<=e<=1, is a complete pointwise DSIC/feasible homotopy and

`R(h_e)=1/3-(1-e)^2(25/3-12 log 2)`.

The original revenue is `12 log 2-8`. The strictly positive improvement is analytic, not an inference from absence of a certificate. This witness only concerns the one-item forced-sale binary class and does not compete with the best two-item lower bound.

## 6. Why an isolated local interface displacement may not be admissible

For a fixed opponent, write a finite own-row cell potential as `U(v)=r_C.v-q_C` on each cell. Along an edge between rows r_C,r_D, its intercept is

`h_CD=(r_C-r_D).v=q_C-q_D`.

Any globally implemented deformation with the same rows and adjacency must satisfy `delta h_CD=delta q_C-delta q_D`. Thus the signed intercept changes sum to zero around every adjacency cycle. If all but one edge intercept are fixed, that remaining edge can move only if removing it disconnects the adjacency graph. In particular an edge on a cycle cannot move alone. A bridge is only the absence of this particular obstruction; it does not by itself prove the deformed polygonal slices, joint feasibility, or both bidders' compatibility.

Apply these conditions in every opponent slice for both bidders. Nondegenerate triple junctions from the V2 infrastructure add common tangent-weight ratios at the junction, whereas repeated-row and collinear-row junctions can retain genuine freedom. Local normal compatibility and intercept-cycle identities are necessary infrastructure. A full mechanism construction such as Theorem 1, Theorem 2, or the globally binary threshold construction is what licenses a revenue comparison.

## 7. Exact replay and interpretation

`verifier/variation_verify.py` uses Python standard-library Fraction arithmetic. It verifies the fee cubic and all three price derivatives as multivariate polynomial identities; checks the four cone rays; checks an exact rectangular entry-fee improvement with both signs of pointwise radial virtual revenue on a forced-moving fiber; and checks the nonlinear homotopy integral identity and a strict rational logarithm bound.

The rectangular example gives bidder 1 item 1 at price 1/4 and bidder 2 item 2 at price 1/2. Adding a 1/4 fee to bidder 1 raises total revenue from 7/16 to 1/2, an exact gain 1/16. The erased band is `1/4<=v_11<1/2` times the full v_12 interval. At v_11=3/8, radial item-1 coefficients are -37/48 at v_12=0 and 3/8 at v_12=1; their full-fiber average is -1/4. This directly exhibits why pointwise virtual sorting is the wrong test for this admissible displacement.

The replay checks algebra and stated witnesses. The continuum proofs and all-profile tie constructions are given above. These tests supply explicit improvements or necessary inequalities; none is a matching upper bound for the unrestricted randomized DSIC class. The S and Z formulas were proposed by the root investigator and independently checked here; their full-mechanism application and comparison with the incumbent are documented in the root V3 candidate artifacts.
