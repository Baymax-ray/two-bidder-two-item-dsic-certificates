# Forced gradients and an exact reduction for the actual V3 residual

This is an independent derivation for the remaining-problem trial. V3 and
V4 are read-only dependencies. The argument below closes a specified family
of **full randomized inner problems**. It does not close the outer problem
or identify the original auction optimum.

## 1. The actual residual, including the top line

Use the frozen V3 constants

`a=159/250`, `b=91/100`, `s=1137/1000`,
`c=b-a=137/500`, `d=s-a=501/1000`, `q=s-b=227/1000`.

Fix bidder 1's own report `w=(t,rho)` with

`d<t<=a`, `0<=rho<=b-t`, and put `k=t-q`.

Let bidder 2's own report be `(x,y)`. All V3 singleton prices are at least
`d` and all bundle prices at least `b`. Since `rho<=b-d<d` and
`t+rho<=b`, bidder 1 never selects item 2 or the bundle with positive
utility. V3 rejects zero-utility ties. Thus its allocation is either empty
or item 1, and bidder 2's second-item residual is identically one.

V3 is an itemwise subset of its common affine base. If that base gives
bidder 1 item 1 here, it must use the split outcome `(1,2)`: bidder 1's
standalone singleton and bundle scores are nonpositive. Comparing the split
score `t+y-s` with bidder 2's bundle score `x+y-b` and with zero gives

`x<=t-q=k`, `y>=s-t=b-k=:B0`.

Consequently the actual first-item capacity hole lies inside the rectangle
`{x<=k,y>=B0}`. This is a rigorous majorant of the hole, not an assertion
that the V3 fee regions leave the entire rectangle unavailable.

The actual top line is simpler and exact. Against `(x,1)`, the V3 price for
bidder 1's item 1 is

`d` for `0<=x<=c`, and `x+q` for `c<x<=1`.

The first formula is the closed V3 chamber's last branch. Above `c`, the
opponent sum exceeds one, so no inherited bundle-fee cell applies; the
ordinary bundle pivot gives the second formula. Since `t>d`, bidder 1
therefore takes item 1 exactly for `x<k`. At `x=k` its utility is zero and
it chooses empty. Hence the actual residual satisfies

`r_1(x,1)=0` for `x<k`, and `r_1(x,1)=1` for `x>=k`.       (1.1)

These statements are independent of `rho` throughout the displayed outer
region. They include the endpoint `t=a` and the boundary `t+rho=b` because
the frozen mechanism explicitly rejects zero-utility allocations.

## 2. Forced utility trace and the SJA obstruction

More generally, coordinatewise monotonicity forces the line ceiling
`a_j(v)<=inf_{z in [v_j,1]} r_j(v_-j,z)` for every report. The infimum is
pointwise, including exceptional reports. This is an equivalent family of
constraints because it bounds every feasible monotone allocation and is
itself no larger than the original cap. For arbitrary jointly Borel caps,
joint Borel measurability of the projected infimum is not presumed; the
statement here is a pointwise constraint, not an unproved substitution into
the Borel-functional domain.

For any fully DSIC/IR bidder-2 mechanism under the actual residual,
`a_1(x,1)=0` for every `x<k`. The one-dimensional envelope along the top
line implies

`u(x,1)=u(0,1)` for every `0<=x<=k`.                         (2.1)

Continuity supplies the endpoint `k`; no capacity constraint there is
silently strengthened. There need not be a corresponding dimensional
collapse throughout the square: substitutes can sell item 1 at lower
second-item reports and switch to item 2 higher up. The valid conclusion
is the exact flat top trace, not a claim that `a_1=0` throughout `x<k`.

The unconstrained SJA menu has bundle-upgrade threshold
`(2-sqrt(2))/3`, which is strictly less than `c<=k`. At top reports with
that threshold `<x<k`, it strictly wants the bundle and violates (1.1).
Thus applying full-capacity SJA to these actual fibers is not feasible.

## 3. Exact reduction to two one-dimensional boundary traces

Relax the actual residual to just the top-line constraint (1.1), retaining
the usual allocation bounds everywhere. Write

`g(y)=u(1,y)`, `h(x)=u(x,1)`.

Every feasible potential has nonnegative convex nondecreasing 1-Lipschitz
traces, `g(1)=h(1)`, `g(0),h(0)<=1`, and `h` is flat on `[0,k]`. Coordinate
Lipschitz bounds give the pointwise lower bound

`u(x,y)>=u_min(x,y):=max(0,x-1+g(y),y-1+h(x))`.           (3.1)

Conversely, any pair of traces with the stated properties yields a complete
feasible normalized potential by (3.1). The maximum is convex. Its top and
right traces are exactly `h` and `g`, because 1-Lipschitz continuity gives
`g(y)>=g(1)-(1-y)` and the analogous inequality for `h`. Normalization
follows from `g(0),h(0)<=1`.

At an active right-trace branch choose a subgradient `(1,g'(y))`; at an
active top-trace branch choose `(h'(x),1)`, using bounded one-dimensional
subgradient selections at jumps and endpoints. Choose zero when the zero
branch maximizes. At the constrained top line choose the top-trace branch
with first coordinate zero (or zero itself). It is available there: for
`x<k`, the other branch is strictly smaller than `h(0)` whenever that value
is positive. At `x=k`, choose the left subgradient zero. These rules are
Borel and satisfy all selected-subgradient inequalities at every report.
Payments are `x*a_1+y*a_2-u_min`.

For fixed traces the uniform revenue functional is

`R=integral g+integral h-3 integral u`.

Replacing `u` by `u_min` therefore weakly raises revenue. The relaxed full
inner problem reduces **exactly** to

`sup_(g,h) [ integral g+integral h
            -3 integral max(0,x-1+g(y),y-1+h(x)) ]`.      (3.2)

This is a concave functional on a convex class of trace pairs. It is not a
finite-menu or finite-grid reduction. A nonempty selected allocation may
be taken to have at least one marginal equal to one; both-marginals-interior
lotteries are unnecessary for this relaxed problem. Fractional allocations
of the other item, and nonlinear traces, remain allowed at this stage.

## 4. Global optimality in the relaxation

Set

`A=2/3`, `C=5/6+3k^2/4`, `B=C-k`, `H=C-A`.

Throughout the actual parameter range `c<k<=a-q`, one has
`0<H<k<A<1` and `0<B<2/3`. The proposed potential is

`u*(x,y)=max(0,x-A,y-B,x+y-C)`,

with traces `g*(y)=1-A+(y-H)_+` and
`h*(x)=1-B+(x-k)_+`. It is feasible against the actual residual: it gives
item 1 only for `x>k` (choose item 2 or empty at the tie `x=k`), while every
actual capacity hole has `x<=k`. Item 2 is always available.

Here is a direct certificate from the trace reduction, independently of
the screening agent's measure formula. On the strip `x>=A`, use the lower
branch `x-1+g(y)` from (3.1). On the remaining region

`D_T={x<=A, y>ell(x)}`, where `ell(x)=1-h*(x)`,

use the lower branch `y-1+h(x)`. On the complement use zero. These lower
branches equal `u*` at the candidate. The coefficient of `g` cancels because
`1-3(1-A)=0`. The remaining trace coefficient is

`sigma(x)=3B-2` for `x<k`,
`sigma(x)=3(H-x)` for `k<x<A`,
`sigma(x)=1` for `x>A`.

The choice of `C` gives `integral_0^1 sigma=0`. Its cumulative integral
`S(x)=integral_0^x sigma` is nonpositive: sigma is nonpositive through `A`,
then equals one and rises to total zero. Every competing `h` is flat through
`k` and has slope at most one above it. Thus for `delta h=h-h*`,
`delta h'=0` below `k` and `delta h'<=0` above it. Integration by parts gives

`integral sigma*delta h = -integral S*delta h' <=0`.

Together with the pointwise lower branches this proves `R(u)<=R(u*)` for
the full randomized top-line relaxation. Since `u*` is feasible against the
actual residual, it also solves the **actual** inner problem exactly.

In particular, this closes the inner fibers for `d<t<=a`,
`rho<=b-t`. Before the V3 transition `t1`, the new menu differs from V3;
from `t1` through `a`, the V3 menu already equals this certified inner
optimum. This is an inner statement with bidder 1 fixed, not outer
stationarity or original-auction optimality.

## 5. Independent audit of the explicit supporting measure

The screening route strengthens the preceding upper bound to a support
over **all** Borel capacities. Its formula is independently derivable from
the exact coordinate envelope identities. Put

`F(x)=integral_x^1 sigma(s) ds=-S(x)>=0`.

The proposed finite nonnegative measures are

`pi_1 = 3(x-A)_+ dx dy + F(x) dx delta_1(dy)`,
`pi_2 = 3(y-ell(x))_+ 1_{x<=A} dx dy`.

For every normalized fully DSIC/IR competing potential, integrate the
horizontal envelope on `x>A` and the vertical envelope on `D_T`. The
remaining set is

`D_0={x<=A,y<=ell(x)}`.

The horizontal trace cancels, and integration by parts along the top line
converts the remaining `integral sigma h` into
`integral F(x) a_1(x,1)dx`. The exact identity is

`<pi,a>-R = 3 integral_(D_0) u >=0`.                      (5.1)

No separability or finite-menu assumption is used for the competitor.
Singular top-line allocations retain their actual pointwise values.
Consequently `V(r)<=<pi,r>` for every residual capacity.

At the actual V3 residual, capacity is saturated on all positively priced
supports: item 1 is available and the candidate uses it on `x>A`; on the
top line its actual cap and the candidate are both zero below `k` and one
above `k`; item 2 is available and used throughout `D_T`. The single tie
`x=k` has zero mass for `F(x)dx` and is implemented feasibly. Also `u*=0`
on `D_0`. Thus

`R(u*)=<pi,r_actual>=V(r_actual)`

and `V(r)<=V(r_actual)+<pi,r-r_actual>` globally. This confirms both the
actual inner optimum and a matching capacity support at these fibers.
The mechanism construction still requires the explicit tie rule stated
above; the measure calculation alone would not specify those reports.

## 6. Admissible lottery probes beyond the current allocation strip

The structural proof does not assume lotteries away. For comparison, take
the safe rectangle majorant `x<=k,y>=B0`, with `B0=b-k`. An added lottery
`(alpha,beta)` at price `p` cannot win inside that rectangle if

`p>=alpha*k+beta*B-(1-beta)*(B0-B)_+`,

and ties there retain the old non-item-1 row. This follows by maximizing
`alpha*k+beta*y-max(0,y-B)` over `B0<=y<=1`. Such options can allow item 1
below `x=k` at lower second-item reports; therefore the trace constraint
does not itself impose global strip containment.

A useful exact check is a lottery `(1,beta,p)` inserted between the item-1
and bundle options. Suppose its two crossings lie at `H-l` and `H+r`, with
`l,r>0`, `H-l>=0`, `H+r<=B`. Then `beta=r/(l+r)` and direct integration of
the complete affected menu regions gives

`Delta R=l*r*(3A/2-1)-l*r^2/2`.

At `A=2/3` this is strictly negative. In particular, lotteries approaching
the item-1 option can have zero first variation but negative second-order
effect. This probe is consistent with the global certificate, and was not
used as a substitute for it.

## Scope

The subsequent independent audit `closed_region_independent_audit.md`
extends actual inner optimality through `t=2/3` and to the full closed
opponent region `Q`. It uses direct price bounds and support saturation;
the rectangle-majorant argument in Section 1 here remains local to `t<=a`.

The independent screening certificate, the trace proof, and the actual
V3-capacity geometry agree. The root construction must still splice the
certified inner menus into a complete auction, account for its exact
revenue, and preserve all existing outputs. Even after that splice, other
opponent regions and optimality of bidder 1 against a common price remain
separate unresolved obligations.
