# A conditional gap map on the entire low-coordinate square

This is an exact branch above the final V4.6 mechanism. It is a complete
whole-menu replacement, with a matching upper bound over every randomized
conditional DSIC/IR mechanism. Its gain is modest; it is useful because it
removes a positive-measure residual region from further inner search. It is
not presented as the main new lower-bound family or as an auction optimum.

Put

\[
A=2/3,\quad a=159/250,\quad b=91/100,\quad c=137/500,
\quad b_0=(4-\sqrt2)/3,\quad z_*=A+c=1411/1500.
\]

The exact reference here is `V4_6/verifier/price_joint_reallocation.py`.
For opponent report v, let z=v1+v2 and consider

\[
L=\{\max(v)\le1/2,\quad b_0<z\le z_*\}.
\]

## Complete mechanism and pointwise feasibility

For **each** bidder whose opponent belongs to L, replace the complete menu
by empty, item 1, item 2, bundle at prices `(0,A,A,z)`. Resolve ties in that
fixed order. Retain V4.6 everywhere else, including the lower face z=b0.
Thus the closed free-region menu already handles that lower face. The upper
face z=z* is included. Equal coordinate and equal utility reports use the
same explicit rule; no exceptional report is omitted.

The relevant structural fact is stronger than a free-capacity observation:
**whenever a bidder's own two coordinates are at most 1/2, its V4.6
allocation is either empty or the complete bundle, at every opponent.**
Every deterministic singleton price is at least 1/2, with empty preferred
at zero utility. In every original Eplus lottery cell the scarce coordinate
exceeds `j=1-t/2>1/2`: this follows from the lottery/bundle/safe-singleton
comparisons in the complete five-option menu. In the final price-cut rows,
the enlarged cell has scarce coordinate at least
`1-.71/2-4*(9/10000)>.5`. Hence no lottery is chosen by a low-square own
type. Raising prices by the final entry fee preserves this fact.

For opponent in L, the actual baseline menus are:

| Range | Bidder 1 singleton prices | Bidder 2 singleton prices | Both bundle prices |
|---|---:|---:|---:|
| b0<z<=b | a,a | A,A | z |
| b<z<=z* | z-c,z-c | z-c,z-c | z |

The final corner rectangles and lottery strips are disjoint from L.
Frozen V3 surcharges vanish when both opponent coordinates are at most
1/2. The table follows directly from the retained pivot tariff and the
V4.6 bundle exchange; at z=b, bidder 2 is still in the closed Q region.

Each actual modification weakly raises singleton prices and leaves the
bundle and empty prices fixed. Therefore the new nonempty choice set is
contained in the old nonempty choice set. If a changed choice adds an item
by moving from a singleton to a bundle, the opponent could not previously
have held a singleton: its own report is in the low square. It also could
not have held the bundle because the first bidder had a positive allocation.
Thus the opponent was empty. Moreover an old empty choice remains empty
under every simultaneous modification. This proves joint feasibility of
the two simultaneous replacements at every report and tie.

Each conditional mechanism is an entire posted lottery menu, so DSIC and
IR follow on the full own-report square. All predicates and prices are
Borel; the finite fixed priority yields joint measurability. Expected
allocations are deterministic in the changed regions and satisfy both
item capacities pointwise. Unchanged V4.6 random allocations keep their
original feasible itemwise implementation.

For a fixed low-square own type, the opposing replacement actually leaves
its allocation and payment unchanged: it cannot choose a singleton before
or after, and the bundle price and empty-first convention are fixed.
Consequently the residual capacity on the L fibers is unchanged. The gap
map below is therefore an exact map for the **actual V4.6 residual**, not
only a comparison with a changed residual.

## Full randomized conditional optimum and gap

The V4.6 diagonal-hole support theorem applies to `(A,A,z)` provided the
candidate is feasible and the opposing bidder occupies the following own
report traces:

\[
r_1(x,0)=0\ (0<x<1/2),\qquad
r_2(1/2,y)=0\ (0<y<z-1/2).
\]

They hold for either bidder. On the bottom trace, the opposing conditional
menu is the full-capacity SJA menu, which sells the bundle strictly because
z>b0 and both coordinates are at most 1/2. On the vertical trace, write
sigma=1/2+y<z. If sigma<=b0 the same argument applies. If b0<sigma<=b, the
opposing bundle price is sigma (for either bidder), and its singleton
prices exceed the fixed low-square coordinates. If sigma>b, the retained
pivot tariff has bundle price sigma and singleton prices sigma-c>=a>.5.
Thus it also sells the bundle strictly. The new replacement keeps those
bundle choices. The corner release is disjoint from these report lines.

Although the original theorem was stated only up to z=b, its displayed
proof extends without modification to z=z*. Indeed `k=z-A<1/2<A`,

\[
m(z)=\frac13-\frac32(4/3-z)^2\ge0,
\]

and `z*<4/3`. Those are exactly the sign and anchor requirements. The
measure, identity, nonnegative IR slack and saturation proof in
`V4_6/research_log/inner_diagonal_capacity.md` remain valid. They allow
arbitrary measurable randomized allocations and arbitrary complete
pointwise DSIC/IR utilities; no finite-menu hypothesis is imposed.
The full conditional value is

\[
V(z)=\frac12z^3-2z^2+\frac73z-\frac8{27}.
\]

For a baseline symmetric singleton price P and bundle price z, the exact
conditional revenue gap is

\[
\boxed{\Gamma(P,z)=3(A-P)^2(z-A)+2(A-P)^3.}
\]

This follows by integrating both price derivatives
`partial R/partial P_i=(z-P_i)(2-3P_i)` from P to A. It is strictly positive
where P<A. The exact baseline residual map is therefore:

| Opponent region | Bidder 1 conditional gap | Bidder 2 conditional gap |
|---|---|---|
| F: max<=.5, z<=b0 | 0 | 0 |
| max<=.5, b0<z<=b | Gamma(a,z) | 0 |
| max<=.5, b<z<z* | Gamma(z-c,z) | Gamma(z-c,z) |
| max<=.5, z=z* | 0 | 0 |
| max<=.5, z>z* | unresolved | unresolved |

After the simultaneous replacement both bidders have zero full
conditional residual gap throughout `max<=.5, z<=z*`.
The other inherited V4.6 map entries remain evidence about their stated
reference: bidder 2 is certified on Q, and both labels on Eplus outside
the explicit final corner exclusions. No zero-gap claim is inferred for
other report fibers merely because their current tariff is stationary.

## Exact total revenue increase

The density of z in the upper part of `[0,1/2]^2` is `1-z`. Hence

\[
\Delta=\int_{b_0}^{b}(1-z)\Gamma(a,z)\,dz
      +2\int_b^{z_*}(1-z)\Gamma(z-c,z)\,dz.
\]

The lower integral is

\[
\frac{30892611299}{75937500000000}
 -\frac{180389}{632812500}\sqrt2,
\]

and each upper integral is

\[
\frac{2999883353}{4746093750000000}.
\]

Their sum is strictly positive and approximately
`0.00000494589800751369`. The new complete mechanism has exact revenue
`R_V4.6 + Delta`, with R_V4.6 retained as its full algebraic/logarithmic
expression. Every own report affected by the complete menus is integrated;
this is not a pointwise virtual-value comparison.

The replayer computes all coefficients with rational arithmetic, checks
an independent polygon revenue formula, brackets sqrt(2) using integer
square roots, and checks named ties, occupied traces and profile cases.
The all-real proof above is the continuum argument; finite regressions do
not substitute for it.

## Why the remaining upper low-square portion is different

Simply continuing to lower singleton prices beyond z* is not justified by
looking only at opponents with one zero coordinate. At
`v=(.49,.49), w=(.68,.28)` the actual V4.6 bidder 2 buys the bundle at .972.
A menu `(A,A,.98)` for bidder 1 would allocate item 1 to w, violating capacity.
This exact profile is a counterexample to that scalar continuation, not a
proof that the existing menu is optimal. The residual contains a binding
junction near low coordinate c together with the Eplus nonlinear boundary.
Lottery screening or a compensating change to the outer allocation is
needed to explore past this obstacle. Such a structure is not imposed here.
