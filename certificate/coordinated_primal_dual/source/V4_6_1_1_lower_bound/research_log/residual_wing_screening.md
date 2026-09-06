# Full randomized screening on a larger base wing

This is a new **zero-gap certificate**, rather than an extra lower-bound
increment. For the frozen V4.6.1.1 mechanism, it proves that each bidder's
existing conditional menu is optimal over the full continuous randomized
DSIC/IR class on a region of opponent area **0.1755468**. The proof does
not require a finite menu for competitors. It identifies where a further
revenue improvement must change the other bidder's allocation.

The applicable mechanism is precisely `verifier/refined_candidate.py`,
with its displayed real-report formulas and joint tie rule. The earlier
`residual_high_screening.md` remains a separate result about the preserved
V4.6.1 mechanism. This note supplies the actual V4.6.1.1 applicability
argument, including its reserve above 2/3 and capped Q price.

## 1. A screening identity that uses actual occupation and incentives

Let 0<p<=1, 1/3<=k<=1, z=k+p>=4/3, and suppose

\[
(3k+1)p\ge k+1.                                      \tag{1}
\]

Consider the feasible complete menu empty, item 2 at p, bundle at z,
with utility

\[
u^*(x,y)=\max(0,y-p,x+y-z).
\]

At p=1 the singleton cannot give positive utility. Write, with the type
square implicit,

\[
D_0=\{y<p,\ x+y<z\},\quad
H=\{x<k,\ y>p\},\quad
G=\{x>k,\ x+y>z\}.
\]

Assume the actual residual capacity r satisfies:

1. Its first marginal is zero on the open vertical strip x<k, and on
   the interior of D0.
2. Its second marginal is zero on the left edge x=0, 0<=y<p.
3. The displayed candidate is pointwise feasible against r.

Relative interiors and their continuity closures are enough for the
first assumption. Neither zero residual in both marginals on D0, nor
zero residual on its entire boundary, is needed.

For any complete measurable randomized DSIC/IR competitor with allocation
alpha<=r, let u be its convex utility and u0=u(0,0)>=0. The left-edge
constraint makes u(0,y)=u0 for y<p. Horizontal incentive compatibility
and the first-marginal constraint then give u=u0 throughout D0. Also,
on x<k at every height, u(x,y)=u(0,y). These conclusions hold without
differentiability: a chosen allocation is a subgradient, its coordinate
is the derivative of the corresponding line restriction almost
everywhere, and all utilities are Lipschitz because allocations lie in
the unit square. In particular, alpha=0 almost everywhere on D0.

The exact revenue identity is

\[
\boxed{\begin{aligned}
R(\alpha)+u_0={}&
\int_G\left[\frac{3x-1}{2}\alpha_1+
                  \frac{3y-1}{2}\alpha_2\right]dxdy\\
&+\int_H\frac{(3k+1)y-(k+1)}{2k}\alpha_2\,dxdy.
\end{aligned}}                                             \tag{2}
\]

All coefficients are nonnegative. On G, x>=k>=1/3 and
y>=z-1>=1/3; on H, (1) gives the nonnegative minimum at y=p.
The candidate uses both marginals surely on G and the second surely
on H. Consequently (2) bounds every competing randomized menu by

\[
\boxed{V(k,p)=pk(1-p)+(k+p)
\left[(1-k)(1-p)+\frac{(1-k)^2}{2}\right].}                 \tag{3}
\]

The candidate attains (3). This is a full conditional screening optimum.
The associated gap is exactly the integral of the displayed nonnegative
densities times the candidate-minus-competitor allocations, plus u0.

### Derivation

Average the horizontal and vertical envelope formulas on the entire
square to obtain the identity valid for every DSIC utility:

\[
R=\int\left[\frac{3x-1}{2}\alpha_1+
             \frac{3y-1}{2}\alpha_2\right]
 -\frac12\int_0^1u(0,y)dy-\frac12\int_0^1u(x,0)dx.
\]

The bottom trace is constant u0. The horizontal strip constraint and
the one-dimensional envelope give

\[
\int_0^1u(0,y)dy
=u_0+\frac1k\int_{x<k}(1-y)\alpha_2(x,y)dxdy.
\]

Substitution and alpha=0 almost everywhere on D0 give (2). Thus the
information rent on the left edge is charged over the entire strip
on which incentive compatibility forces that same utility. This is why
the safe price may be below 2/3 here, unlike the earlier certificate.

The argument uses actual capacity-zero constraints to eliminate rents.
It does **not** assert that the displayed nonnegative density alone is
a supporting measure for arbitrary residual perturbations that free
those constraints. The separate pure-bundle global support in
`residual_high_screening.md` remains applicable on the pure-bundle part.

## 2. Actual applicability to the frozen mechanism

Use the exact frozen constants

\[
A=2/3,\quad c=157/500,\quad q=93/500,\quad
a=1025947/1500000,\quad b=a+c<1,\quad u=3421/10000.
\]

The surcharge is g(r)=(4/5)(u-r) on the closed interval [c,u],
and zero elsewhere. Its maximum is J=281/12500; r+g(r)<=u.
The proof uses the actual menu formulas, including the Q safe-price cap.
Define

\[
\boxed{\mathcal W=
\{\max(w)\ge1-q,\quad w_1+w_2\ge1+u\}.}                  \tag{4}
\]

Align the high item with item 1 and write w=(t,rho), z=t+rho.
Then rho>=u>c, t>=1-q=407/500, and g(rho)=0.
These opponents lie outside Q and E. Since z>b and rho>c,
the base outside-option potential is H=z-b. The actual conditional
prices are

\[
P_{\rm scarce}=
\begin{cases}z-c,&rho\le1/2,\\ t+q,&rho\ge1/2,
\end{cases}
\qquad P_{\rm safe}=rho+q,\qquad C=z.
\]

The scarce price is at least one, and is strictly above one if rho<1/2.
Set p=min(rho+q,1), k=z-p. Therefore the existing conditional utility
is exactly u* above. An unaffordable singleton can be suppressed, or
a price above one replaced by the dummy price one, without changing the
empty-at-zero choice or any positive utility allocation.

We verify the required capacity constraints by studying the *other*
bidder, of own type w, on the menus induced by v=(x,y).
Every occupation claim below holds for every maximizing option in the
specified open region. Thus the global joint tie rule cannot undo it.

### First-marginal occupation on the strip when p<1

Here k=t-q. On an unmodified base menu the first-item singleton price is
at most max(a,x+q). Indeed, if y<=1/2 it equals
max(a,x,y,x+y-c), while if y>1/2 it equals
max(a+1/2-y,x+1/2-y,1/2,x+q).
For x<k this is strictly less than t.

If that singleton receives a surcharge, x is the low report in [c,u].
Its price is then at most max(a+J,u+q), which is strictly below 1-q<=t.
The other orientation leaves its price unchanged. Thus the empty option
cannot win. The bundle's upgrade over the singleton of item 2 is
max(c,x-q), except that it is c+g(x)<=u when x is the surcharged low
report. These thresholds are strictly below t on the strip, so the
item-2-only option cannot win either. Every base maximizer includes
item 1 surely.

On Q the first-item singleton costs at most A<t. The bundle's upgrade
over the second-item singleton is either C-A or
max(C-A,k_v), where k_v<=A-q. The uniform bound

\[
C\le\max\{5/6+3(A-q)^2/4,\ b+J\}<1+u
\]

makes both thresholds smaller than t. This includes the capped Q menu
and the free Q menu. Every maximizing Q option therefore includes item 1.

On E, if item 1 is scarce, its singleton price is t_v<T<1-q<=t,
and the bundle's upgrade over the item-2 singleton is t_v-q<t.
The only remaining options, bundle and lottery, include item 1 surely.
If item 1 is safe, its singleton costs 1/2+delta<A<t;
the opposing orientation's lottery is strictly dominated by the bundle
at safe value t, because their junction Y is below 1/2.
The item-2 singleton is also dominated, since c+delta<1/2<t.
Thus E also occupies item 1 surely throughout the strip.

### First-marginal occupation in the no-sale interior

Take 0<x,y<1 with y<p and x+y<z. On a base menu without a surcharge,
the bundle price max(b,x+c,y+c,x+y) is strictly below z.
For a surcharged base row the price is
max(b,x+y)+g(min(x,y)), and hence at most

\[
\max\{b+J,\ \max(x,y)+u\}<1+u\le z.
\]

This bound also covers the new reserve a>A: it does not assume the
report sum is above b. The bundle is positive. Its upgrade over the
item-2 singleton is max(c,x-q), or c+g(x)<=u in the one changed
orientation. It is strictly below t because x<1 and t>=1-q.
Thus every base maximizer includes item 1.

The Q argument above already makes its first-item singleton positive
and rules out the only option missing item 1. The E argument above is
also independent of the strip. Therefore every maximizer includes
item 1 throughout the no-sale interior, even where item 2 may remain
partly or fully free.

### Both marginals on the left edge

At v=(0,y), y<p, no base surcharge applies. Its bundle price is
max(b,y+c)<z, and the upgrade thresholds are c<t and
max(c,y-q)<rho. Thus the bundle is strict.

For free Q, C=b0=(4-sqrt(2))/3 and C-A<rho, so both upgrades are strict.
For constrained Q on this edge, k_v=inverse(y)<=y-q and
C=C0(k_v)=5/6+3k_v^2/4. The safe cap is inactive: C0(k_v)-k_v<A.
The bundle upgrade in the low-valued physical item is k_v<rho, since
y<p=rho+q. The other upgrade C0(k_v)-A is below t.

For E on this edge, item 1 is safe. Its bundle/lottery junction is
below 1/2<t; the bundle upgrade over the safe singleton is
y-q<rho, and the other upgrade c+delta<t. Its bundle price is
at most T+c=1+c/3<z. The bundle is again strict.

Consequently actual residual r2(0,y)=0 for all y<p. Combined with
first-marginal occupation in D0, this makes every feasible competitor's
utility constant throughout D0. Literal occupation of item 2 everywhere
inside D0 is unnecessary.

### The case p=1 and exceptional reports

If p=1 then rho>=1-q, so both values are at least 407/500.
The preceding base comparisons show strict bundle occupation on the
interior of x+y<z, and Q and E have both bundle upgrade thresholds
below these values. Since x<k=z-1 implies x+y<z for y<1, the same
strip condition holds. At y=1, the upgrade adding item 1 is still
strictly below t when x<k, so any possible singleton/bundle tie keeps
item 1 surely allocated. The left-edge proof is unchanged.

At x=k, y=p, x+y=z, own boundary coordinates, or menu knots, some
normal marginals may remain free or some options may tie. The proof
does not replace the mechanism's tie rule and does not assert a false
closed-region capacity occupation statement. It uses the actual strict
comparisons where required, continuity of every competitor's utility,
and almost-everywhere envelope identities. The finite joint argmax
selection and empty-at-zero convention remain exactly those of the
full mechanism, so exceptional reports remain DSIC, IR and feasible.

## 3. Coefficient signs and area, exactly

For p<1, p>=u+q and k=t-q>=1-2q>1/3. Also z>=1+u>=4/3.
The coefficient margin gamma=(3k+1)p-k-1 increases in k for p>=u+q>1/3.
Using k>=1+u-p gives

\[
\gamma\ge -3p^2+(5+3u)p-2-u.
\]

The right side is increasing for p<=1 because u>=1/3. Its minimum
is thus at p=u+q, and equals

\[
(4-3q)(u+q)-(2-q)=\frac{18601}{5000000}>0.              \tag{5}
\]

For p=1, k=z-1>=u>=1/3 and gamma=2k>0. These prove all sign
hypotheses of the unrestricted screening theorem uniformly on W.

Since u<=2c, ordered opponents satisfy 1-q<=t<=1 and
1+u-t<=rho<=t. Both item orientations give exact area

\[
\boxed{|\mathcal W|=2q(1-q-u)
=\frac{438867}{2500000}=0.1755468.}                     \tag{6}
\]

W is disjoint from Q and E. It can be added to their independently
proved conditional zero-gap regions, with the final Q cap and E
incentive-trace repairs stated in their respective proofs. This note
does not inherit literal E boundary occupation from the old a=A
mechanism: for the new a>A that statement fails, and any full E
certificate needs the separate incentive-trace repair.

## 4. Replay and claim boundary

`verifier/residual_wing_screening.py` independently integrates complete
deterministic and lottery menus over exact polygonal cells. It checks
(2), including competitors with positive origin rent, in 168 cases.
It also checks the frozen mechanism on 12,220 exact profiles across
both bidder labels, both item orientations, the functional jump,
Q/E boundaries, ties, and the wing thresholds. These profile checks
are bounded implementation evidence, not the all-real theorem; Sections
1--3 establish the full continuous statement.

The resulting value (3) is exact for each conditional problem on W.
No auction revenue increment, complete global capacity-price support,
or unrestricted auction optimum is claimed. A profitable deformation
touching these fibers must change actual residual capacity through a
joint reallocation, rather than merely substitute a more elaborate
conditional menu.
