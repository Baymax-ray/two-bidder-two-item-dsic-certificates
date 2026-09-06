# An exact type-dependent residual-screening problem and its global capacity support

This note solves a restricted **residual-capacity instance**, not the original auction. Its support inequality nevertheless ranges over the full two-item randomized DSIC/IR class and over arbitrary pointwise Borel residual capacities. No finite type grid, differentiability of the allocation, or finite-menu hypothesis is used in the upper bound.

## 1. Conventions and a pointwise reduction

Write bidder 2's own type as `(t,z) in [0,1]^2`, uniformly distributed. An additional variable `y in [0,1]^2` can index bidder 1's report; all statements below hold conditionally on `y` and can be integrated over it. Allocations and payments are Borel; DSIC, IR, and capacity inequalities hold at **every** report. Feasibility concerns lottery marginals. Utilities are expected quasilinear utilities.

For a Borel function `rho:[0,1]->[0,1]`, first take

`r_rho(t,z)=(rho(t),0)`.

Define the pointwise future-capacity envelope

`m(t)=inf {rho(s): t<=s<=1}`.

The actual infimum, including individual exceptional types and the endpoint, is intended. The function `m` is nondecreasing, hence Borel, even if `rho` is not semicontinuous and the infimum is not attained.

**Theorem 1 (complete inner solution).** The unrestricted randomized DSIC/IR residual value is

`V(r_rho)= integral_{1/2}^1 (2t-1)m(t) dt`.

An optimal mechanism at every report is

```
q(t)=0                         if t<=1/2,
q(t)=m(t)                      if t>1/2,
x(t,z)=(q(t),0),
u(t,z)=integral_0^t q(s) ds,
p(t,z)=t q(t)-u(t,z).
```

In particular, no attainment of the future infimum is required for primal attainment here.

*Proof.* DSIC between types with the same `z` implies that `x_1(t,z)` is nondecreasing in `t`. Thus `x_1(t,z)<=rho(s)` for every `s>=t`, and hence `x_1(t,z)<=m(t)` pointwise. The one-dimensional envelope identity on every such line is

`u(t,z)=u(0,z)+integral_0^t x_1(s,z) ds`.

It holds because the utility is convex and Lipschitz and the selected allocation is a subgradient at every point; arbitrary selections at nondifferentiability points do not alter the integral. Since item 2 has zero capacity, DSIC between `(t,z)` and `(t,z')` also gives `u(t,z)=u(t,z')` exactly. Consequently the extra coordinate cannot supply extra screening power. Integration of the envelope gives

`R=integral_0^1 integral_0^1 (2t-1)x_1(t,z) dt dz - integral_0^1 u(0,z) dz`.

IR makes the last term nonpositive. Drop the negative virtual values below `1/2`, and use the pointwise bound `x_1<=m` above `1/2`, to obtain the claimed upper bound. The displayed `q` is nondecreasing, lies below `rho` at every type, and is a subgradient of its displayed integral, including both endpoints and all jumps. Its payment is nonnegative, its utility is nonnegative, and it attains the bound. This proves pointwise DSIC, IR, and capacity, not merely their almost-everywhere versions. QED.

The solution uses the entire future fiber of types. Replacing `m(t)` by the local physical cap `rho(t)` generally violates IC and gives the wrong revenue.

## 2. Transporting virtual mass to capacity bottlenecks

Suppose there is a Borel map `T:(1/2,1)->[0,1]` such that, for almost every `t`,

`T(t)>=t` and `rho(T(t))=m(t)`.

This hypothesis is verified directly in the examples below. It is **not** inferred for an arbitrary Borel capacity with an unattained infimum. Let

`nu=T_#((2t-1) 1_{t>1/2} dt)`

be the pushforward of positive virtual mass. Define finite nonnegative capacity-price measures on the complete two-dimensional type square by

`pi_1=nu(dt) dz`,  `pi_2=z dt dz`.

**Theorem 2 (a support on the full capacity domain).** For every pointwise Borel capacity `r:[0,1]^2->[0,1]^2`, allowing both items and arbitrary dependence on both coordinates,

`V(r)<=V(r_rho)+<pi,r-r_rho>`.

Thus this is a genuine global supergradient of the concave residual value functional at `r_rho`; it is not only a support on the face `r_2=0`.

*Proof and exact gap identity.* For any feasible two-item DSIC/IR mechanism, write its allocation as `x` and utility as `u`. Conditional envelope along the first coordinate gives

`R=integral (2t-1)x_1(t,z) dt dz + integral z x_2(t,z) dt dz - integral u(0,z) dz`.

This formula permits arbitrary cross-coordinate screening and follows directly by integrating `p=t x_1+z x_2-u`. The first allocation is nondecreasing in `t` on every fixed-`z` line. Therefore

```
<pi,r>-R
 = integral u(0,z) dz
 + integral_{t<1/2} (1-2t)x_1(t,z) dt dz
 + integral_{t>1/2} (2t-1)[x_1(T(t),z)-x_1(t,z)] dt dz
 + integral (r_1-x_1) d pi_1
 + integral (r_2-x_2) d pi_2.
```

Every term is nonnegative pointwise or almost everywhere, with the singular capacity integrals retaining their actual pointwise values. This proves `R<=<pi,r>` for the full randomized class. At the mechanism in Theorem 1, `m(T(t))=m(t)` by monotonicity and the minimizing property. All five slack terms vanish. Thus `<pi,r_rho>=V(r_rho)` and taking the supremum proves the stated support. This proof constructs a support where its hypotheses hold; it makes no general dual-attainment assertion. QED.

The measure `pi_1` charges the reports at which capacity constrains later screening choices. It can put positive price on a zero-probability set of reports and on capacity whose effect propagates to a positive-measure set of earlier types. The term `pi_2=z dt dz` is sufficient to make the support global when the second item is restored; no separability assumption is made about competing mechanisms.

## 3. Exact bottleneck example: a lottery and a singular global support

Fix `1/2<b<1` and `0<c<1`. Consider either of the following capacities:

```
plateau:    rho(t)=c for t<=b, and rho(t)=1 for t>b;
single line:rho(b)=c, and rho(t)=1 for every t!=b.
```

Both have the same future envelope: `m(t)=c` for `t<=b`, and `m(t)=1` for `t>b`. Therefore both have exactly the same residual value

`V=1/4-(1-c)(b-1/2)^2`.

The complete menu is

| Allocation of item 1 | Payment |
| --- | --- |
| 0 | 0 |
| c | c/2 |
| 1 | b-c(b-1/2) |

Item 2 is never allocated. Choose the empty row at `t=1/2`; choose the `c` lottery at `t=b`; use the uniquely optimal row away from ties. These rules enforce the single-line capacity at the tie itself. The displayed payments equal the envelope payments.

For `T(t)=b` when `1/2<t<=b`, and `T(t)=t` when `t>b`, set `K=(b-1/2)^2`. The exact global support is

`pi_1=[K delta_b+(2t-1)1_{t>b}dt] dz`,

`pi_2=z dt dz`.

The atom is not an approximation to a density. It is required to retain the pointwise bottleneck.

For the fully rational example `b=3/4`, `c=1/2`, the menu is

`(0,0); (1/2,1/4); (1,5/8)`

and the exact optimal revenue is `7/32`. Here `pi_1=[(1/16)delta_{3/4}+(2t-1)1_{t>3/4}dt]dz`. Removing the bottleneck restores value `1/4`, an increase of `1/32`. This is the incremental information-rent cost relative to capacity `(1,0)`, not the user's total opportunity cost relative to `(1,1)`.

The lottery is essential **for this residual instance**. At an optimum the nonnegative virtual-revenue slack in Theorem 1 must vanish, so the allocation equals `c` almost everywhere on `1/2<t<b`. A deterministic allocation, being zero or one and nondecreasing on every fixed-`z` line, must instead be zero through `b`; its best revenue is `b(1-b)`. The randomized advantage is `c(b-1/2)^2`, equal to `1/32` in the rational example. This does not establish essential randomization for an optimal mechanism in the original two-bidder auction.

## 4. The functional cannot discard exceptional capacities

For the single-line capacity, `r_rho` agrees almost everywhere with `(1,0)`, but their inner values differ by `(1-c)(b-1/2)^2>0`. Thus `V` is not even well-defined on `L^p` equivalence classes of arbitrary pointwise capacities. A measure support absolutely continuous with respect to report-volume measure cannot support `V` at this capacity: increasing only the bottleneck line gives a strict value increase and zero pairing with every such measure.

This is compatible with the original residual formulation. Define bidder 1's mechanism, for every own report `y`, by

`x_{11}(y,t,z)=(1-c)1_{t=b}`, `x_{12}(y,t,z)=1`, `p_1=0`.

Its allocation is independent of its own report; hence it is complete pointwise DSIC and IR. Its residual is exactly the single-line example. Together with the displayed optimal bidder-2 menu it is pointwise feasible, including at `t=b`. The fractional allocations there can be coupled by assigning item 1 to bidder 1 with probability `1-c` and to bidder 2 with probability `c`.

Nevertheless this particular bidder-1 mechanism is not shown optimal against the displayed price measure; no unrestricted auction upper bound follows from the inner support alone. It is an exact diagnostic instance, not a replacement for solving the residual of the V3 candidate.

One can also lower capacity on `[b-epsilon,b]` instead of just `{b}`. The same positive revenue loss persists while the difference from `(1,0)` tends to zero in every finite `L^p` norm. Consequently an `L^p` continuity assumption for this unrestricted pointwise residual functional needs additional justified restrictions. The uniform norm keeps the bottleneck visible.

## 5. What is verified and what remains open

`verifier/screening_verify.py` checks the rational menu's global affine dominance on complete closed type intervals, exact tie choices and pointwise bottleneck feasibility, envelope payments, exact randomized and deterministic revenues, the singular price masses and support equality, and the formal coefficient identity for the general nonnegative gap decomposition. It also rejects optimized Python execution. Its checks are exact rational calculations; the general functional claims rest on the proofs above, not on a grid computation.

## 6. An exact nonlocal directional equation

The single-line example permits a direct calculation of inner re-optimization after a capacity change. Let `h` be a bounded Borel first-item capacity direction such that `rho+epsilon h` stays in `[0,1]` for sufficiently small positive `epsilon`; keep the second cap zero. Assume `2 epsilon ||h||_infinity < 1-c`. The strict gap between the bottleneck and all other capacities then ensures that the future minimum is still attained at `b` for every `t<=b`. For `t>b` the future envelope is `1+epsilon inf_{s>=t} h(s)`. Thus the following equality, not merely an infinitesimal approximation, holds:

```
V(r_rho+epsilon(h,0))-V(r_rho)
 = epsilon [ K h(b)
             + integral_b^1 (2t-1) inf_{s>=t} h(s) dt ].
```

This is the one-sided derivative of the **fully re-optimized** inner problem. It is generally nonlinear in `h`. The difference between the supporting linear price and this exact change is

`epsilon integral_b^1 (2t-1)[h(t)-inf_{s>=t}h(s)]dt >= 0`.

The support is exact in some directions and strictly slack in others. For example, a new decrease at just one later type `d>b` can lower value on the entire interval `(b,d]`, although the original support has no atom at `d`. Failure of this particular support to make every directional value change an equality is expected for a concave nondifferentiable functional, not evidence that its global support inequality fails.

The results supply: an exact multidimensional residual-screening solution with a genuinely type-dependent cap; a full-domain capacity support; a precise information-rent effect from a future bottleneck; an exact forced lottery; and a nonlocal directional equation after complete inner re-optimization. They do not solve the inner screening problem at V3's actual residual, produce a higher two-bidder revenue, or establish the outer bidder's optimality against the same measure.
