# V5: a complete global primal improvement by reserve rebasing

The construction below improves the frozen V4.6.1.1 mechanism over the **full four-dimensional profile distribution**. For the explicit choice `tau=1/100`, exact face integration and rational enclosure give

\[
0.87651220877675 < R_{\tau} < 0.87651222602760,
\]

where the displayed decimals are outward summaries of the rational endpoints in `certificate/primal_global.json`. Its revenue gain over the frozen mechanism is strictly greater than

\[
\frac3{62500}=0.000048.
\]

The more precise gain enclosure is approximately `[0.0000480443049596593, 0.0000480615557971841]`. This is a new complete lower bound, not an optimality claim. The old mechanism and every predecessor file remain unchanged. The first derivative calculation is a globally admissible variation; it does not maximize a virtual value pointwise or assert stationarity under unrestricted variations.

## 1. Complete mechanism, including all exceptional reports

Write the frozen complete mechanism as `(x^0,p^0,u^0)`, with own utilities normalized to zero at the origin. Its exact implementation is `V4_6_1_1_lower_bound/verifier/refined_candidate.py`. Its existing all-real feasibility and full-menu DSIC proof is a dependency; the new proof below gives a transformation of that complete mechanism, rather than selecting independently incompatible maximizing options.

For `0<=tau<1`, put `s=1-tau` and

\[
T(v)=\max\{(v-\tau)/s,0\},\qquad z_{ij}=T(v_{ij}).
\]

Define at **every real profile** in `[0,1]^4`

\[
x_i^{\tau}(v)=x_i^0(z),\qquad
p_i^{\tau}(v)=s p_i^0(z)+\tau\sum_{j=1}^2x_{ij}^0(z).
\tag{1}
\]

The source tie rule is retained exactly at the transformed profile: each bidder selects empty if the maximum menu utility is zero; otherwise use the lexicographically first jointly feasible pair among the two complete sets of maximizing options. Thus reporting a clipping threshold, lying on a menu interface, equal opponent coordinates, and endpoints of the unit square all have a specified outcome. No tie is decided by a floating tolerance.

Allocations in (1) are expected allocations. For a concrete randomized realization, on each item independently select bidder1 with probability `x_1j`, bidder2 with probability `x_2j`, and leave the remaining probability unsold. Charge each bidder its deterministic expected payment in (1). This realizes the same additive expected utilities and satisfies ex post item feasibility in every random outcome. All functions are Borel measurable. The source includes its genuine lottery menu, which (1) retains at transformed reports.

### Zero-valued-item lemma for the source

For every real source profile, including ties,

\[
z_{ij}=0\quad\Longrightarrow\quad x_{ij}^0(z)=0.
\tag{2}
\]

Here are the branchwise reasons; they concern the entire source menu, so the final feasible-pair selection cannot invalidate them. Let `A=2/3`, `d=1/2`, `c=157/500`, `q=d-c`, `B0=(4-sqrt(2))/3`, and `K(k)=5/6+3k^2/4`. Every singleton has strictly positive price.

* In the free Q menu, the bundle price is at least `B0`; comparison with the complementary singleton requires each bundle coordinate to be at least `B0-A>0`.
* In constrained Q, the prices are scarce `A`, safe `B=min(A,C-k)`, bundle `C`, where `k>=c` and `C>=K(k)`. A winning bundle requires scarce value at least `C-B>=k>=c`, and safe value at least `C-A>=K(c)-A>0`.
* In the base menu, each bundle-minus-complementary-singleton price is at least `b-a=c>0`. Indeed the common `H` cancels; the safe fee either cancels or increases that marginal price. Each singleton price is at least `d`: `H>=w_j-a` and the minimum in the singleton formula give this directly.
* In E, the prices are scarce `t`, safe `d+delta`, bundle `t+c+delta`, and lottery `(1,beta)` at price `t+beta*c`, in scarce/safe coordinates. Here `A<t<T`, `0<beta<1`, and `delta(t)=9(T-t)(U-t)/16`. Bundle marginal prices are positive. A lottery with positive safe component must beat the scarce singleton, requiring safe value at least `c>0`. To allocate its scarce component, it must beat both empty and the safe singleton. For safe value below `d+delta`, the empty comparison, and for safe value above it, the safe comparison, imply scarce value at least `t-beta(q+delta)`. This is at least `A-q-delta(A)>0`, since `delta` decreases on `[A,T]`. The exact positive rational lower bound is replayed in `primal_global.py`.

At a weak equality in these comparisons the lower bound on the corresponding value is still strictly positive. Hence (2) is pointwise, including source ties. No stronger invariance of a positive-width low-value strip is needed.

### Universal DSIC, IR and feasibility proof

Fix an arbitrary opposing report `w`. Set

\[
U(v;w)=s\,u^0(T(v);T(w)).
\]

The source utility is convex and coordinatewise nondecreasing. The map `T` is convex and nondecreasing. More explicitly, at any own report `r`, choose the subgradient of `T` to be `D_j(r)=0` if `r_j<=tau`, and `1/s` if `r_j>tau`. For every true type `v`, source DSIC gives

\[
u^0(T(v))\ge u^0(T(r))+x^0(T(r))\cdot[T(v)-T(r)].
\]

Coordinatewise convexity of `T`, and nonnegativity of `x^0`, imply

\[
U(v)\ge U(r)+\sum_j sD_j(r)x_j^0(T(r))(v_j-r_j).
\]

By (2), `sD_j(r)x_j^0(T(r))=x_j^0(T(r))`, including `r_j=tau`. Also every allocated coordinate has `v_j=tau+sT(v_j)`, so (1) gives exactly `v.x^tau-p^tau=U(v)`. The displayed subgradient inequality proves **all-pairs dominant-strategy IC** on the full continuous report space. IR follows from source IR. Since `U(0)=0`, the subgradient inequality with true type0 also yields nonnegative payments; IR bounds payments above by value. Source joint feasibility at `z` gives `x_1j^tau+x_2j^tau<=1` pointwise. This establishes all required mechanism properties, rather than testing them on a type grid.

## 2. A positive-volume base/base ownership change

This variation is not a contraction of the old allocation at the original profile. Consider

\[
v=(1577/2000,123/200),\qquad w=(3/5,4/5).
\]

On the entire closed four-dimensional box of radius `1/10000` about this profile, the old and transformed source reports lie in the high-sum base/base branches and all coordinates exceed the relevant safe-fee thresholds. The old conditional menu has singleton prices `w_j+q` and bundle price `w_1+w_2`. The new menu has singleton prices `w_j+s q` and the **same** bundle price `w_1+w_2`.

The old allocation on this whole box is bidder1 bundle, bidder2 empty. The new allocation is item1 to bidder1 and item2 to bidder2. All option-utility differences are affine within the box; exact checks at its16 vertices give a strictly positive minimum gap, recorded in `ownership_switch` in the certificate. Thus the ownership change holds on a positive-volume set, not only at sampled points. The global revenue calculation next includes this change **and every other induced switch and rent change**; this local witness alone is not used to infer a net gain.

## 3. Exact full-distribution revenue identity

For a uniform original coordinate, `Z=T(V)` has distribution

\[
\tau\delta_0+s\,\operatorname{Unif}[0,1].
\]

The four transformed coordinates remain independent. For `S` a subset of the four coordinates, let `R_S` and `N_S` be the integrals of source total payments and total expected allocated-item count when coordinates in `S` are fixed at0 and all other coordinates are uniform. Expanding the product mixture and using (1) gives the exact identity

\[
R_\tau=\sum_{S\subseteq\{1,2,3,4\}}
\tau^{|S|}s^{4-|S|}\bigl(s R_S+\tau N_S\bigr).
\tag{3}
\]

There is no unintegrated correction for switches: they are already present in the pushforward distribution and the source-face integrals. Formula (3) is a degree5 polynomial in `tau` with exact face-moment coefficients. It characterizes the revenue of the complete family, not just a restricted boundary calculation.

Bidder/item symmetries reduce the16 source faces to the following groups. Write `R4,N4` for the full four-free-coordinate moments, `R3,N3` for any one-zero-coordinate face, `RSJA,NSJA` for two zeros belonging to the same bidder, `Rsame,Nsame` for two zeros in the same physical item, `Rcross,Ncross` for diagonally opposite zeros, and `Rone,N_one` for three zeros. The group sums by number of zero coordinates are

\[
\begin{aligned}
\mathcal R&=(R4,4R3,2(RSJA+Rsame+Rcross),4Rone,0),\\
\mathcal N&=(N4,4N3,2(NSJA+Nsame+Ncross),4N_{one},0).
\end{aligned}
\]

The source tie selection need not be symmetric at every boundary profile. It is symmetric almost everywhere on each relevant face: zero-valued coordinates never receive allocation by (2), and menu ties affecting any positive free coordinate occur on finitely many affine own-type interfaces, a null set. If a bidder has no free coordinates, the zero-utility rule selects empty. This suffices for the face-moment symmetries.

In particular the exact global derivative at the frozen source is

\[
R'_0=N4+4R3-5R4
\in[0.0120503811119742,0.0120521625636254].
\tag{4}
\]

It is strictly positive. This supplies a global necessary optimality test that the old mechanism fails. The selected finite step `tau=.01` is verified directly by (3), rather than relying only on the derivative. No claim is made that this step optimizes the rebasing family.

## 4. Source-face integration and all numerical remainder

`primal_face_integrals.py` performs rational polynomial integration over ordered opponent types `(t,rho)`, `0<=rho<=t<=1`. Only narrow one-dimensional intervals containing unresolved branch crossings are enclosed. The generated certificate lists296 resolved intervals and15 unresolved strips. The source `B0` is bracketed by rationals at width `10^-15`; this approximation is separately bounded below. These are continuous integral enclosures, not optimization on a finite type grid.

### Conditional deterministic-menu formulas

For empty/scarce/safe/bundle prices `(0,P,B,C)`, replace the singletons by `min(P,1),min(B,1)`, without changing utility on the square. In every used branch the resulting prices satisfy

\[
0\le P,B\le1,\qquad \max(P,B)\le C\le P+B.
\]

Put `k=C-B`, `ell=C-P`, `Delta=P+B-C`. The scarce, safe, and bundle allocation areas are

\[
(1-P)\ell,\quad(1-B)k,\quad
(1-k)(1-\ell)-\tfrac12\Delta^2.
\]

Thus `Rcond` is the price-weighted sum of these areas and

\[
Ncond=2-2C+C^2+(P+B)(1-C).
\tag{5}
\]

The formulas remain valid when the bundle price exceeds1. Clipping singleton prices above1 affects neither the value function nor any relevant integral.

### Exact E-lottery corrections

Relative to the deterministic E menu with prices `P=t`, `B=d+delta`, `C=t+c+delta`, let `alpha=3t-2` and `beta=alpha/(alpha+2delta)`. The lottery contributes exactly

\[
\Delta Ncond=\alpha\delta/4,\qquad
\Delta Rcond=\alpha^2\delta/8.
\tag{6}
\]

For completeness, write the own safe coordinate as `c+r`. The lottery changes utility only for `0<r<L=delta/(1-beta)=alpha/2+delta`. On this strip the safe singleton has negative utility, because `L<q+delta`; the two scarce-coordinate cutoffs are `a=t-beta r` and `b=t-max(0,r-delta)`. Their difference is triangular. The integral of its utility increase on the own `x=1` edge is `alpha delta/4`; the other three square edges do not change. Its utility-volume increase is `(1-t)alpha delta/4+alpha^2 delta/24`. The identities `N=boundary flux of u` and `R=top-edge integral of u-3 integral u` give (6). This accounts for the lottery regions exactly; no deterministic substitute is used.

### Reduction of the face moments

Let `P(t,rho),B(t,rho)` denote clipped scarce/safe singleton prices. With `G=P(1-P)+B(1-B)` and `S=2-P-B`, the exact reductions are

\[
\begin{aligned}
N4&=4\iint_{0\le\rho\le t\le1}Ncond(t,\rho),\\
R3&=\int_0^1Rcond(t,0)\,dt+\iint G(t,\rho),\\
N3&=\int_0^1Ncond(t,0)\,dt+\iint S(t,\rho),\\
Rcross&=2\int_0^1B(t,0)(1-B(t,0))\,dt,\\
Ncross&=2\int_0^1(1-B(t,0))\,dt.
\end{aligned}
\tag{7}
\]

In a one-zero face, the full two-coordinate bidder contributes the first line integral; the other bidder has just one valued item, with its corresponding singleton critical price. Its two physical opponent orientations give the triangle integrands `G` and `S`. A bundle cannot improve on that singleton when its other coordinate is zero, by the positive marginal-price lemma. On cross faces the only sale threshold is the safe singleton price. The remaining elementary moments are

\[
RSJA=(12+2\sqrt2)/27,\quad NSJA=(8+2\sqrt2)/9,
\]
\[
Rsame=31/81,\quad Nsame=5/9,\quad Rone=2/9,\quad N_{one}=1/3.
\]

The same-item face is a two-bidder second-price auction with reserve `A`; the one-free-coordinate face has posted price `A`. `R4` is the inherited exact V4.6.1.1 revenue enclosure, source-hashed in the certificate.

### Branch coverage and rigorous enclosure

The source Q exchange term is redundant by the inherited exact Q activity proof: `C=max(K(k),t+rho)` in constrained Q. The inverse has its constant, fast, and tail branches; all are retained. Ordered-opponent integration uses rational `t` cuts at `0,d,d+jump,u+q,A,a,T,1-q,1` and polynomial `rho` cuts at

`0,t,c,u,d,1-q,b-t,1+c-t`,

plus `B0-t` for free Q or `K(k)-t` and `A+k-t` for constrained Q. These include Q/base and E/base selection, the fee, `H` and singleton-minimum changes, the Q floor/sum and cap changes, and singleton clipping. The one-dimensional `rho=0` integrals use the corresponding complete branch list.

For each accepted `t` interval, adjacent cut differences have nonnegative exact interval bounds obtained by centering their polynomial coefficients. Their certified order fixes all branch choices on every resulting vertical region. Rational polynomial integration then evaluates (5)--(7) exactly. If this order is unresolved after the prescribed bisections, the **entire** opponent triangle strip is bounded using `0<=Ncond<=2`, `0<=G<=1/2`, `0<=S<=2`; its exact area is recorded. No profile or remainder is dropped.

Finally `bh=861928812542301/10^15` satisfies `bh<B0<bh+10^-15`, certified by squared rational comparisons. Replacing only `B0` changes every conditional utility by at most this width. For an own face with `m<=2` free coordinates, utility integration by parts bounds its revenue difference by `(2m+1)10^-15<=5*10^-15` and its allocated-count difference by `2m*10^-15<=4*10^-15`. Coordinates fixed at zero have zero allocation by (2), also for the rationalized menus. Across both bidders this gives `10*10^-15` and `8*10^-15`. Every recorded face enclosure includes the more conservative `10^-12` error allowance. Rationalized menus are only an integration device; no claim that they independently form a new complete feasible auction is required.

All coefficients in (3) are nonnegative at the selected `tau`. For the gain relative to `R4`, its coefficient is `s^5-1<0`, so the lower gain endpoint uses the **upper** `R4` endpoint. `primal_global.py` performs this interval arithmetic explicitly. The approximately `1.73*10^-8` width of the final revenue enclosure is much smaller than the certified positive gain.

## 5. Replay, discovery history and claim boundary

Run, from the auction workspace, with bytecode disabled:

```
python -B -X utf8 V5_gap_closure/verifier/primal_face_integrals.py
python -B -X utf8 V5_gap_closure/verifier/primal_global.py
```

Both are read-only replays by default and reject optimized `-O` execution. The first recomputes all face enclosures; the second source-checks that certificate, evaluates (3)--(4), and checks the exact-report implementation on clipping/source boundary nodes and random deviations. The all-real conclusions come from the proofs above and inherited source mechanism, not those finite checks. Certificate hashes establish dependency identity, not an independent proof on their own.

The earlier files in `discovery/primal_*` contain broad floating transport probes and provisional face estimates. Their sampling errors were larger than the improvement at issue, so early negative estimates were inconclusive. They are retained as discovery evidence only and are not used by either proof replay. The final construction is a fixed finite global deformation and a complete exact menu mechanism; it does not require enlarging a type grid or solving a finite menu classification.

This branch has achieved a new strict complete lower bound, a global derivative that diagnoses a missing direction of the frozen mechanism, and explicit base/base ownership changes. It has not identified an unrestricted optimizer, matched the upper bound, or characterized all admissible deformations. The common-support problem and the full randomized-DSIC gap remain open.
