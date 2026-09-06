# Exact geometry audit of the joined-threshold candidate

Status: frozen for independent audit; `JOINED_GEOMETRY_EXACT_PASS`.

This bounded audit checks the representation obstruction and actual surviving labels of the candidate specified in `joined_threshold_candidate.md` and evaluated in `verifier/joined_threshold.py`. It does not re-audit its revenue formula or assert global optimality. The complete menu and shared-base containment proofs in the candidate and inherited-mechanism records are the all-type feasibility and DSIC dependencies. No source-classification theorem is imported.

## 1. An exact obstruction to a common convex potential

Let M modify both bidders as in the candidate. Consider the interior rational profiles

`v=(3211/5000,1/100,539/1000,1/100)`,

`v'=(257/400,1/100,541/1000,1/100)`.

The masks selected by M are respectively `(1,0)` and `(0,0)`, with all individual menu maximizers strict. Here mask 1 means item 1, and the pair lists bidder 1 then bidder 2.

For both profiles bidder 1 is on the square-root branch. Write `k=y1-q`, `W=K+k^2`, with `q=227/1000`, `c=137/500`, `K=2/3+c^2`. Its three nonempty utilities are

`x1+c-sqrt(W)`, `x2+k-sqrt(W)`, `x1+x2-sqrt(W)`.

At v, `W=125863/150000` and `(x1+c)^2-W=25183/75000000>0`; the first utility is positive and strictly largest. At v', `W=315127/375000` and `(x1+c)^2-W=-4397/12000000<0`; all three utilities are negative. The opposite bidder is on the quadratic branch and strictly chooses empty at both profiles. These claims use exact rational squaring of positive quantities, rather than decimal evaluations of radicals.

For any fixed weights `w1,w2>0`, the weighted joint allocation's monotonicity expression is

`sum_i wi*(A_i(v)-A_i(v')) dot (v_i-v_i') = -3*w1/10000 < 0`.

Subgradients of one convex potential must be monotone. Thus no common convex potential can have the weighted joint allocation as a selected subgradient on the full cube. In particular, the allocation cannot be represented as a maximizer of fixed joint affine scores with positive bidder weights. This does not contradict either bidder's conditional convex utility, which depends on the opponent's fixed report. The obstruction is to a shared potential, not to DSIC. Payments cannot alter the displayed allocation obstruction.

## 2. The nonlinear surface is an actual local entry panel

An algebraic boundary point makes the row-change issue explicit. Put

`t=27/50`, `ell=1/100`, `k=t-q=313/1000`,

`R=sqrt(503827/600000)=sqrt(K+k^2)`,

`x=(R-c,ell)`, `y=(t,ell)`.

The exact inequalities `r0<k^2<r1<(a-q)^2` and `b^2<R^2<(c+2/3)^2` imply that bidder 1 is strictly inside the square-root branch, `a<R-c<2/3`, and bidder 2 is strictly inside the quadratic branch. Both opponent chambers have strict positive slack. Thus all relevant menu formulas are continuous on a full open neighborhood of this profile.

Bidder 1 has prices `(0,R-c,R-k,R)`. Its empty and item-1 utilities are both zero. Its other utilities obey

`u_01=ell+k-R < ell+k-b = -587/1000`,

`u_11=ell-c=-33/125`.

For bidder 2 write `z=x1-q`. Its prices are

`A2=2/3`, `B2=5/6-z+3z^2/4`, `C2=5/6+3z^2/4`.

The identity `B2=1/2+3(z-2/3)^2/4` gives the exact bounds

`u_10=t-2/3=-19/150`,

`u_01=ell-B2<=-49/100`,

`u_11=t+ell-C2<=-17/60`.

Consequently bidder 2 uniquely chooses empty throughout a sufficiently small open neighborhood. The shared affine base uniquely selects `(1,0)` at the boundary point: its winning score is `R-b>0`, and all other nonempty outcome scores are strictly negative. This base choice persists locally.

The only actual final labels near the point are therefore `(0,0)` and `(1,0)`. They are separated by

`x1=sqrt(K+(y1-q)^2)-c`.

On the equality itself the prescribed zero-utility rule chooses empty. On either strict side the allocation is forced by strict menu maximization. The other coordinates can vary in open intervals, so this is a regular joint panel in the interior four-dimensional cube, not merely a one-dimensional drawing.

The normal into bidder-1 entry and the allocation jumps are

`n=(1,0,-k/R,0)`, `d1=(1,0)`, `d2=(0,0)`.

The normal has a nonzero opponent block, but that bidder's row is unchanged. This is exactly the zero-row degeneracy in the bilateral normal lemma. Its curved threshold has first derivative `k/R>0` and second derivative `K/R^3>0`. No complementary item transfer or both-row-change diagonal is exposed on this panel, so the corresponding local affine-rigidity hypotheses are absent here. Nothing in this argument says such panels are absent elsewhere in the mechanism. Any other panel where both rows change remains subject to the bilateral normal and junction constraints.

## 3. The asymmetric pair is distinct on an open set

Let M1 replace only bidder 1's inherited menu, and M2 replace only bidder 2's inherited menu. Every retained inherited selection and every replaced selection remains a subset of the same globally feasible base selection. Hence either asymmetric choice inherits pointwise joint feasibility. Its menus depend only on the opponent and its stated tie rule chooses a maximizer, so the all-type DSIC, normalized IR and measurability arguments apply unchanged.

At the rational profile

`p=(677/1000,1/100,649/1000,1/100)`

the masks are `M1(p)=(1,0)` and `M2(p)=(0,0)`. In M1, bidder 1's winning item-1 utility is `31/3000>0`, and all its other nonempty utilities are negative. Bidder 2 strictly chooses empty. In M2 both bidders strictly choose empty; bidder 1's item-1 utility is `-237/25000` and bidder 2's is `-7/250`. All menu prices and utility differences are recorded exactly in the certificate.

The inherited rows used here are S1.2 and S3.2, with strict high-coordinate inequalities

`643/1000 < 649/1000 < 13/20`,

`269/400 < 677/1000 < 17/25`.

The new branches are also interior: the first high coordinate is on the affine branch, the second on the quadratic branch. Both low coordinates are strictly below c. Thus no table boundary passes through the profile; the strict allocation difference persists on an open set and has positive measure.

## 4. Precise exposed-representative interpretation

Each of M1 and M2 is a deterministic representative of the original normalized pointwise DSIC/IR feasible set. For either one's binary allocation field `A*`, define bounded measurable coefficients

`c_ij(v)=+1` if `A*_ij(v)=1`, and `-1` otherwise.

The continuous linear functional on the L1 allocation/payment space is

`L(A,p)=integral_[0,1]^4 sum_ij c_ij(v)*A_ij(v) dv`.

For every feasible expected allocation field A, each coordinate belongs to [0,1], and

`L(A*,p*)-L(A,p)=integral sum_ij |A*_ij(v)-A_ij(v)| dv >= 0`.

Equality holds exactly when the allocation fields agree almost everywhere. Thus the deterministic field is exposed in the a.e. quotient, including against randomized competitors. The functional need not be a revenue functional.

Normalized DSIC payments are unique almost everywhere once the allocation is fixed almost everywhere. Indeed, Fubini gives equality of own allocation gradients almost everywhere on almost every opponent slice. Bounded allocations make each DSIC utility Lipschitz and convex on that slice. Equal gradients imply utilities differing by a constant; normalization at zero fixes that constant. The payment identity then gives equality almost everywhere. Hence the normalized allocation/payment pair is exposed in this same quotient. The fixed tie rules specify pointwise representatives; an integral functional cannot uniquely expose choices at null boundary sets. The distinct open-set witness in Section 3 ensures M1 and M2 are different quotient classes.

## 5. Replay and scope

`verifier/joined_geometry.py` checks the exact radical inequalities, strict menu winners, weighted monotonicity coefficient, local utility margins, asymmetric menus and table interiors, and agreement with the supplied exact rational mechanism evaluator. It reads `certificate/joined_geometry.json` and writes nothing. The analytic neighborhood and exposed-representative proofs are given above; finitely many checked reports are not used to claim full-cube IC or global classification.
