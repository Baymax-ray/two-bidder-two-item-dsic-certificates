# V4: eliminating one bidder with pointwise residual capacities

This note gives self-contained proofs. No outside-source retrieval was used.
The results concern the unrestricted randomized, pointwise DSIC/IR class. They
do not establish that the V3 candidate, or any new candidate, is optimal.

## 1. The exact functional and the elimination identity

Let `T=[0,1]^2`, let `t` denote bidder 1's report and `v` bidder 2's report,
and use product Lebesgue probability measure `F=dt dv`. A residual capacity is
a Borel function `r:T x T -> [0,1]^2`, with its values retained at **every**
report. Let `K(r)` be the set of jointly Borel pairs `(a,p)` such that

* `0 <= a(t,v) <= r(t,v)` coordinatewise, at every `(t,v)`;
* `v.a(t,v)-p(t,v) >= v.a(t,w)-p(t,w)` for all `t,v,w`;
* truthful utility is nonnegative at every report.

We may impose `u(t,0)=0`, where `u(t,v)=v.a(t,v)-p(t,v)`. Indeed, subtracting
the original nonnegative `u(t,0)` from every utility in its own-type slice
preserves DSIC/IR and increases every payment by that amount. After this
normalization, the two IC inequalities involving type zero imply
`0 <= p(t,v) <= v.a(t,v) <= 2`. Thus normalized revenue is bounded and
integrable; there is no payment-integrability issue in the following suprema.

Define

`V(r) = sup_{(a,p) in K(r), normalized} integral p dF`.

This is a **global Borel-mechanism** supremum, rather than an unproved
interchange of a supremum and an integral over opponent reports. Although
the constraints separate by `t`, replacing this definition by an integral
of slice-wise suprema requires a measurable selection argument. All explicit
constructions below supply the joint Borel mechanism directly.

For any complete normalized DSIC/IR mechanism `M1`, its residual
`1-x1` is Borel. Every jointly feasible mechanism has
`R2 <= V(1-x1)`. Conversely, for any `M1` and any positive `epsilon`, choose
an inner mechanism within `epsilon` of `V(1-x1)`. Combining these two complete
mechanisms preserves each bidder's IC and IR inequalities and satisfies
capacity pointwise. Taking suprema proves exactly

`OPT = sup_M1 [ R1(M1) + V(1-x1) ]`.

No inner optimizer, differentiability, finite range, grid, or common
potential is assumed. The identity includes all exceptional reports and
ties through the definition of `K(r)`.

## 2. Concavity, homogeneity, and opportunity cost

For `0<=theta<=1`, mixing the **complete** mechanisms `(a,p)` and `(b,q)`
gives `(theta a+(1-theta)b, theta p+(1-theta)q)`. IC, IR and normalization
are linear, and its capacity is at most `theta r+(1-theta)s`. Approximate
maximizers therefore give

`V(theta r+(1-theta)s) >= theta V(r)+(1-theta)V(s)`.

Moreover, `V` is monotone and `V(0)=0`. Scaling every allocation, utility and
payment by `alpha>0`, and scaling back, proves

`V(alpha r)=alpha V(r)` whenever both `r` and `alpha r` take values in `[0,1]^2`.

Consequently, `V(r+s)>=V(r)+V(s)` whenever `r+s<=1`. This superadditivity is
not an assertion that independently chosen mechanisms can violate capacity:
the sum of their allocation rows is itself a valid randomized allocation
for the inner bidder because its coordinates are bounded by `r+s<=1`.

The opportunity cost

`C(x)=V(1)-V(1-x)`

is convex, monotone, and satisfies `C(0)=0`, `C(1)=V(1)` and
`C(alpha 1)=alpha V(1)`. In general it is not homogeneous in arbitrary
directions. Superadditivity also gives `C(x)>=V(x)`: the revenue that capacity
can earn alone can understate the revenue lost when removing it from a
larger screening problem. Section 5 gives a strict example on a one-item
face of the capacity domain.

These are functional statements on pointwise Borel capacities. They do not
mean that `V` is defined on equivalence classes modulo sets of measure zero.

## 3. The inner screening problem as a selected-subgradient problem

Pointwise DSIC is equivalent to the following potential formulation. For
each `t`, `u(t,.)` is convex and continuous on `T`, `u(t,0)=0`, and there is
a jointly Borel selection `a(t,v)` satisfying

`a(t,v) in partial_T u(t,v) intersect [0,r(t,v)]`

at **every** report. Here the relative subdifferential consists of all `g`
such that `u(t,w)>=u(t,v)+g.(w-v)` for every `w in T`. Payments are then
`p=v.a-u`. The nonnegative selected subgradients make utility coordinatewise
nondecreasing, so normalization implies IR. Bounded selected subgradients
give `|u(t,v)-u(t,w)| <= |v-w|_1`.

At almost every own type, `a=gradient_v u`, but imposing
`0<=gradient u<=r` only almost everywhere is insufficient. The selected
subgradient constraint at nondifferentiable and boundary reports is part of
the problem, and cannot be repaired independently of `r`.

For normalized feasible potentials, integration by parts gives the exact
uniform-distribution objective

`R2 = integral_t [ integral_0^1 u(t,1,y)dy + integral_0^1 u(t,x,1)dx
                 - 3 integral_T u(t,v)dv ] dt`.

Indeed, `p=v.gradient u-u` almost everywhere, and each coordinate integration
contributes one top-face integral minus the volume integral of `u`. Convex
Lipschitz utilities are absolutely continuous on coordinate lines, which
justifies the identity. This puts the multidimensional free-boundary problem
in explicit form, but it does not remove the selected-subgradient constraint
at exceptional reports or supply a solution for general `r`.

For an explicitly constructed two-sided admissible path `(u_h,a_h)` with
`u_h=u+h phi+o(h)`, where the remainder is `o(h)` in `L^1(dt dy)` on each
top face and in `L^1(dt dv)` in the volume, the first variation of revenue is
the same boundary-minus-volume functional applied to `phi`. This is a
conditional derivative formula, not permission
to choose `phi` freely: convexity and every residual subgradient constraint
must hold for the full path.

## 4. A null set can destroy all inner revenue

Let `top=(1,1)` and set `r^0(t,v)=1` except that `r^0(t,top)=0` for every `t`.
At the top report a feasible allocation is zero. IC using that report yields
`u(t,v)>=u(t,top)` for every `v`; monotonicity gives the reverse inequality.
Hence normalized utility is identically zero. Allocations can still be
nonzero on some boundary reports, but are zero almost everywhere in the own
type square, and revenue is zero. Thus

`V(r^0)=0`, whereas `V(1)>=1/2`

(sell each item separately at price `1/2`). These two capacities agree
Lebesgue-almost everywhere. This obstruction applies to all `L^p` spaces
formed by identifying almost-everywhere equal functions, including essential
`L^infinity`.

The residual is attainable from a complete bidder-1 mechanism: give bidder 1
both items for free exactly when bidder 2 reports `top`, and nothing
otherwise. Its allocation is independent of its own report, so it is DSIC
and IR. Thus this issue cannot be dismissed as an infeasible choice of the
outer variable.

There is nevertheless an explicit **singular** global support here. For
each own-type slice, the objective in Section 3 and monotonicity give

`R_slice <= 2 u(t,top) <= 2 [a_1(t,top)+a_2(t,top)]`.

The last inequality is IC of type zero against the top report. Define the
finite Borel measures

`pi_j = 2 dt tensor delta_top`, for `j=1,2`.

Then `V(r)<=<pi,r>` for every Borel residual. Since `<pi,r^0>=V(r^0)=0`,
this is a global supporting inequality at `r^0`. No price absolutely
continuous with respect to `F` can support there: testing full capacity
would incorrectly give `V(1)<=0`.

## 5. An exactly solved nonlocal screening model

Restrict to capacities `r(v)=(rho(v_1),0)`, independent of the opponent and
the second own coordinate, with Borel `0<=rho<=1`. Because allocation of item
2 is zero, DSIC makes utility independent of `v_2`. This is the ordinary
one-dimensional screening problem, embedded in the original report space.

Define the future bottleneck envelope

`m(z)=inf_{s in [z,1]} rho(s)`.

It is nondecreasing and hence Borel, even when the infimum is not attained.
Every feasible monotone allocation `a` satisfies `a(z)<=m(z)`. The complete
optimal allocation is

`a*(z)=0` for `z<=1/2`, and `a*(z)=m(z)` for `z>1/2`,

with `u*(z)=integral_0^z a*(s)ds` and `p*(z)=z a*(z)-u*(z)`. This monotone
allocation is a selected subgradient of its integral at every type,
including jumps. The stated tie choice is feasible and DSIC. The exact value
is

`V_1(rho)=integral_(1/2)^1 (2z-1) m(z) dz`.                 (5.1)

The upper bound follows from `a<=m` on the positive-virtual-value region
and from the nonpositive virtual value below `1/2`. The displayed mechanism
attains it. This solves the full inner problem on this face, rather than a
finite grid or a selected menu family.

If a measurable map `s(z)>=z` attains `rho*(s(z))=m*(z)` on `z>1/2`, define

`pi(A)=integral_(1/2)^1 (2z-1) 1_{s(z) in A} dz`.

For every competing capacity `rho`, its bottleneck envelope is at most
`rho(s(z))`, so (5.1) gives

`V_1(rho)<=integral rho dpi`, with equality at `rho*`.

This is a constructive global supporting price: virtual revenue from all
types constrained by the same future report is pushed onto that report.

### An atom prices an information-rent restriction

Take `c=3/4` and `rho^c=1` except `rho^c(c)=0`. Then `m=0` on `[0,c]` and
`m=1` on `(c,1]`. The full optimal mechanism posts price `c`, with the tie at
`c` rejected, and earns `c(1-c)=3/16`. Full capacity earns `1/4`, so removing
capacity at one zero-probability report costs exactly `1/16` in revenue.

A matching global price on the one-item capacity face is

`pi = (1/16) delta_(3/4) + (2z-1) 1_{z>3/4} dz`.

Its atom collects `integral_(1/2)^(3/4) (2z-1)dz=1/16`; its continuous part
has mass `3/16`. The atom is forced by monotonicity propagating the capacity
hole to an interval of lower reports. It is not the expected quantity of
physically unavailable allocation at that report.

For strict superadditivity, take `rho_A=1_[0,c]`, `rho_B=1_(c,1]`.
Then `V_1(rho_A)=0`, `V_1(rho_B)=3/16`, but
`V_1(rho_A+rho_B)=1/4`. Relative to the full one-item capacity, removing
`rho_A` costs `1/16`, although it earns zero by itself.

### Countably additive supporting prices need not exist

Let `z_n=1-1/(n+2)`, `n>=1`, and let

`rho*(z_n)=1/(n+2)`, and `rho*(z)=1/2` otherwise.

This Borel capacity is strictly positive at every type and at most `1/2`.
Nevertheless, `m*(z)=0` for every `z<1`, since each future tail contains
capacities tending to zero. Thus `V_1(rho*)=0`.

Suppose a finite countably additive signed Borel measure `pi` supported the
value globally at `rho*`. For any Borel `A`, the capacity
`rho*+(1/2)1_A` is feasible, and nonnegative revenue and the support inequality
give `pi(A)>=0`. Thus the measure is positive. Testing capacity zero gives
`integral rho* dpi <=0`. Since `rho*>0` everywhere, countable additivity
implies `pi=0`: the sets `{rho*>=1/k}` cover the entire interval. Testing
full capacity would then give `1/4<=0`, a contradiction.

The same counterexample embeds in the full two-item residual problem by
using `r*=(rho*(v_1),0)`. The item-1 component of any supporting measure would
be positive and vanish; varying only item 1 gives the contradiction. It is
also the residual of a complete bidder-1 mechanism allocating
`(1-rho*(v_1),1)` to bidder 1 for free, independently of its own report.

This is an obstruction to **existence of countably additive supports for
arbitrary Borel capacities**, not an obstruction for regular candidates.
Using the supremum norm on bounded Borel functions preserves point values,
but its full continuous dual includes finitely additive charges. Invoking a
separation theorem in that space does not automatically produce a finite
countably additive Borel price measure. Neither that separation issue nor
the pathological example decides whether a useful price exists at V3 or at
a better regular allocation.

## 6. What a matching price would prove

Let `pi=(pi_1,pi_2)` be finite nonnegative Borel measures on the complete
profile space, and pair them with the actual pointwise allocation functions.
Suppose a complete candidate `(M1*,M2*)` has residual `r*=1-x1*`, and proves

1. `R2*=V(r*)`;
2. `V(r)<=V(r*)+<pi,r-r*>` for every Borel residual in `[0,1]^2`;
3. `R1(M1)-<pi,x1> <= R1*-<pi,x1*>` for **every** complete bidder-1
   DSIC/IR mechanism.

For any competing `M1`, these inequalities imply

`R1(M1)+V(1-x1) <= R1*+V(r*) = R1*+R2*`.

The elimination identity then certifies unrestricted optimality. No
symmetry or common-potential representation is involved. A global support
alone does not prove condition 3, and a local directional derivative does
not prove either global inequality.

Equivalently, the same `pi` is a subgradient of the nonlinear opportunity
cost at `x1*`: `C(x)>=C(x1*)+<pi,x-x1*>` for every capacity allocation `x`.
The outer screening problem is then bounded using this global lower bound
on its information-rent opportunity cost.

An often more directly checkable sufficient version uses

`W_i(pi)=sup_Mi [R_i(M_i)-<pi,x_i>]`.

Positivity of `pi` gives `V(r)<=W_2(pi)+<pi,r>`, and for every joint mechanism

`R1+R2 <= W_1(pi)+W_2(pi)+<pi,1>`.

This upper bound matches a candidate if each candidate bidder attains its
own `W_i(pi)` and `<pi,1-x1*-x2*>=0`. These are global priced screening
problems, with pointwise IC still intact; candidate binding IC and capacity
constraints can guide their certificates. In particular, this statement
does not turn singular prices into ordinary pointwise virtual prices.

Finally, homogeneity on the capacity box alone does **not** justify the
Euler identity `<pi,r*>=V(r*)` for every affine support. At a boundary of the
box, upward scaling may be unavailable: at full capacity, for example,
the zero price with intercept `V(1)` is a valid support. The priced-screening
version above keeps its intercept and complementary-slackness requirements
explicit and avoids that error.

## 7. Scope of the replay

`verifier/functional_verify.py` checks the rational integrals and polynomial
identities behind the solved one-item examples and the supporting atom. It
also checks explicit finite tail inequalities used in the nonattainment
example. The continuum arguments, the infinite-tail proof, and the functional
certificate theorem are the written proofs above; the replay is not a
formal verification of those analytic statements and does not certify an
optimal two-bidder mechanism.
