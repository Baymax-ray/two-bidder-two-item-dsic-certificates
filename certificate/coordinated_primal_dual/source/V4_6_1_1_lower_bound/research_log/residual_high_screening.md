# A new full conditional certificate on high base fibers

This route finds a substantial **zero-gap region**, not an additional
revenue increment. It eliminates high base fibers from inner-menu search
while keeping outer reallocations available. The conditional upper bound
covers every measurable randomized pointwise DSIC/IR mechanism, including
arbitrary menus and lotteries.

## 1. A screening theorem forced by the no-sale region

Fix parameters

\[
2/3\le p\le1,\quad 1/3\le k\le1,\quad z=k+p\ge4/3.
\]

Consider the complete menu empty, safe item 2 at p, bundle at z. At p=1
the singleton is never chosen with positive utility and this is pure
bundling. Empty is preferred when maximum utility is zero. Its utility is

\[
u^*(x,y)=\max\{0,y-p,x+y-z\}.
\]

Let

\[
D_0=\{y<p,\ x+y<z\},\quad
H=\{x<k,\ y>p\},\quad
G=\{x>k,\ x+y>z\},
\]

with the square `[0,1]^2` implicit. G and H partition the positive-utility
set up to their shared zero-volume boundary. Suppose an actual residual r
is zero in both marginals throughout the **interior** of D0 and that the
candidate menu is pointwise feasible against r. No restrictions on r
elsewhere are required.

For any competing complete pointwise DSIC/IR utility u and selected
allocation a<=r, incentive compatibility makes u constant on the interior
of D0. The constant is u0=u(0,0)>=0. The bounded allocation range implies
Lipschitz continuity, so u=u0 on its closure as well. This handles normal
allocation choices on exceptional boundary reports without discarding them
from the mechanism definition.

The following identity holds exactly:

\[
\boxed{\begin{aligned}
R(a)+u_0={}&
\int_G\left[\frac{3x-1}{2}a_1(x,y)
             +\frac{3y-1}{2}a_2(x,y)\right]dxdy\\
&+\int_H(3y-2)a_2(x,y)\,dxdy\\
&+\frac{3k-1}{2}\int_p^1(1-y)a_2(k,y)\,dy.
\end{aligned}}                                                   \tag{1}
\]

Every coefficient is nonnegative: on G, x>k>=1/3 and y>z-x>=z-1>=1/3;
on H, y>p>=2/3; the line coefficient is nonnegative because k>=1/3.
The candidate allocates item 1 and item 2 surely on G, and item 2 surely
on H and on the priced line x=k,y>p. Its possible safe/bundle ties on that
line always give item 2 surely. Candidate feasibility forces the residual
to equal one on every priced marginal support. Hence (1) gives the exact
global conditional gap

\[
\langle\pi,r\rangle-R(a)=\langle\pi,r-a\rangle+u_0\ge0,
\]

where pi consists of the displayed nonnegative volume densities and one
vertical line measure. Equality holds at the candidate. The exact full
conditional value is

\[
\boxed{
V(k,p)=p k(1-p)+(k+p)
\left[(1-k)(1-p)+\frac{(1-k)^2}{2}\right].}
                                                               \tag{2}
\]

This is a matching upper bound over the full randomized class, not
stationarity of its two offered nonempty options. The proof uses the
actual capacity hole to establish u=u0 on D0. Consequently this version
of the displayed capacity measure is a support **conditional on that
hole hypothesis**; a supporting inequality for arbitrary residual
perturbations that fill D0 is not asserted automatically.

### Derivation of the identity

Write v=u-u0 and e(x)=p for x<k, e(x)=z-x for x>k. Applying the vertical
envelope on all G union H gives top coefficient 3e(x)-2 and right
coefficient one. Alternatively use the horizontal envelope on G and the
vertical envelope on H. Its right coefficient is 3 max(k,z-y)-2; its top
coefficient is 3p-2 below k and one above k. Average these two exact
identities.

The resulting top coefficient is 3p-2 below k and
`[3(z-x)-1]/2` above k. The right coefficient is
`[3 max(k,z-y)-1]/2`. Expand the top trace vertically from the point
(x,e(x)), where v=0. Expand the right trace horizontally from the
zero-utility diagonal when y<=p. When y>p, first expand vertically from
(k,p) to (k,y), then horizontally to (1,y). Fubini combines the resulting
terms into (1). The extra vertical path produces precisely the line
coefficient `(3k-1)(1-y)/2`. All expansions use actual selected
allocations on their report lines; they are valid for convex Lipschitz
DSIC utilities, without differentiability or a finite-menu hypothesis.

### Stronger corollary on the pure-bundle subregion

For p=1 the actual positive region is the diagonal triangle x+y>z.
There is also a global supporting capacity measure that remains valid
when this no-sale hole changes. For every complete DSIC/IR utility,
integration by parts on the entire square gives

\[
R=\int\sum_{j=1}^2\frac{3v_j-1}{2}a_j(v)\,dv
 -\frac12\int_0^1u(0,y)\,dy-\frac12\int_0^1u(x,0)\,dx.
\]

Consequently the nonnegative volume measure
`pi_j(v)=max((3*v_j-1)/2,0)` gives `V(r)<=<pi,r>` for **every** residual
r. At the actual pure-bundle residual in this theorem, equality holds:
the residual vanishes almost everywhere below x+y=z, the candidate uses
both marginals surely above it, both coordinates there exceed 1/3, and
its left/bottom utility traces vanish. Normal marginal freedoms on
exceptional report edges have zero volume price. Thus

\[
V(r)\le V(r^*)+\langle\pi,r-r^*\rangle
\]

is a genuine global capacity support on this pure-bundle subregion.
It is still a conditional support; no common two-bidder certificate at
the complete auction's revenue follows automatically.

## 2. The actual high-base region

The argument applies to the rebuilt family and its coordinated exchange
surcharges under the following transparent parameter conditions:

\[
1/6<c<1/3,\quad q=1/2-c,\quad a\le A=2/3,
\quad b=a+c<1,\quad 1/3\le u<1/2.
\]

Base surcharges g are nonnegative, supported at low reports r in [c,u],
and satisfy `r+g(r)<=u`. They raise only the safe singleton and bundle
prices by g(r). Jumps at c are allowed. The Q menus retain their complete
screening form with k<=t-q, bundle at least the opponent sum, and safe
price above 1/2; the Eplus menus have the displayed unchanged five-option
form. If additional menu regions are introduced, their interaction must
be checked separately rather than inferred from this statement.

Define

\[
\boxed{\mathcal H(c,u)=
\{\max(w)\ge1-q,\quad \min(w)\ge1/2,
                 \quad w_1+w_2\ge1+u\}.}                       \tag{3}
\]

These are base opponents. Align their high item with item 1 and write
w=(t,rho), z=t+rho. Their actual conditional base prices are

\[
t+q,\quad\rho+q,\quad z.
\]

The scarce singleton costs at least one and can be removed without
changing any selected positive utility or allocation. Put

\[
p=\min(\rho+q,1),\qquad k=z-p.
\]

Replacing any unaffordable safe price by the dummy price one also leaves
the implemented utility and the empty-at-zero choice unchanged. Thus the
existing row is exactly the screening candidate above. Its hypotheses
hold: p>=1-c>2/3; if p<1, k=t-q>=2c>1/3; if p=1,
k=z-1>=u>=1/3; and z>=1+u>=4/3.

### Why the no-sale interior has zero actual residual

At an own report v=(x,y) inside D0, y<p<=rho+q and x+y<z. We show that
the opposing bidder of own type w strictly purchases the bundle.

On a retained base row, the bundle price is
`max(b,x+c,y+c,x+y)`. The first three terms are below z, since z>=1+u
and u>=c, while the last is below z by D0. Its bundle-minus-singleton
thresholds are `max(c,y-q)` and `max(c,x-q)`. The low value rho beats the
first threshold because y<rho+q; the high value t>=1-q beats the second
strictly when x<1. Thus the bundle strictly dominates every other option
at interior reports.

On a changed base row with low r in [c,u], the bundle price is at most
`max(v)+r+g(r)<=max(v)+u<1+u<=z`. The changed upgrade threshold on the
unraised scarce singleton is `c+g(r)<=u<1/2<=rho`; the upgrade threshold
on the jointly raised safe singleton is unchanged. The previous strict
comparison still holds. This proof is valid for a discontinuous g and
at every one of its support knots.

On Q, the bundle price is below 7/6<1+u. Both upgrade thresholds are
strictly below 1/2: k<=A-q<1/2, and C-A<1/2. The candidate's own values
are at least 1/2, so it purchases the bundle strictly. These inequalities
also cover the free-Q menus. They should be verified for the final Q
maximum floors; the known sum and k+h(rho) floors satisfy them because
rho<1/2 and h(rho)<=rho+q+g(rho)<1/2+q.

On Eplus the bundle price is at most `T+c=1+c/3<1+u`, and its lottery is
dominated by the bundle at safe own values at least 1/2, since its
bundle/lottery junction satisfies Y<1/2. If its scarce item is the high
item of w, the high value t>=1-q exceeds every scarce upgrade threshold.
If it is the low item of w, the D0 inequality y<rho+q gives exactly
rho>y-q, again forcing the bundle. The remaining singleton comparison
uses c+delta<1/2. Thus its bundle is strict as well.

This proves zero residual on the interior of D0. Candidate feasibility is
inherited from the complete mechanism's independently checked global
construction. The theorem therefore gives a full randomized conditional
upper matching the existing row for either bidder throughout (3).

At t=1-q and an own coordinate equal to one, bundle/singleton ties can
leave a normal boundary marginal available. The proof deliberately does
not claim literal zero residual on that boundary. Continuity fixes the
competitor's utility there, and every positive price support is a
candidate-saturated marginal. Equal total reports and menu ties retain
the original finite joint selection; no mechanism change is performed.

## 3. Size and implication of the new map entry

When u<=2c, the exact opponent area is

\[
|\mathcal H(c,u)|=\frac14-c^2-(u-c)^2.                         \tag{4}
\]

For the preserved V4.6.1 constants c=47/150 and tent endpoint u=17/50,
this is 34/225, about 15.11 percent of the opponent square. It is disjoint
from Q and Eplus. Combined with their existing certificates, it raises
the fully classified conditional region for each bidder to
`82501/135000`, about 61.11 percent.

For a broader endpoint u=43/125=.344 at the same c, the parametric result
gives area `84871/562500`, about 15.09 percent. This is an applicability
calculation, not a claim that an unspecified new candidate was verified.
The final branch must separately confirm that its actual menus satisfy
the stated surcharge and Q hypotheses.

There is no revenue increment in this route: the existing mechanism is
already a full conditional optimum on these fibers. A profitable change
would have to alter their residual capacity through a coordinated outer
reallocation, or work on a different unresolved base region. The result
therefore redirects search rather than declaring these reports irrelevant
to global auction optimality.
