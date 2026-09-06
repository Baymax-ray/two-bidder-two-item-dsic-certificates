# Rebuilding the parameter family: a symmetric three-region mechanism

This is a complete new lower-bound mechanism, not a wrapper that preserves
V4.6 ownership and adds another local correction. Its only menu regions are
a symmetric screening region Q, a symmetric lottery strip E, and the
remaining affine-base region. Old fee tables, square-root joined menus,
F/G wrappers, and corner corrections are absent from its definition.

The exact revenue satisfies

\[
0.8764552982716114956646711668<R<
0.8764552982716114956646711669.
\]

The fully evaluated exact expression is

\[
\boxed{R=\frac{482935538268336599}{574087500000000000}
+\frac{31}{1215}\sqrt2-\frac{170368}{664453125}\sqrt{11}.}
\]

The root's independent simplex-moment computation and this branch's
Green-boundary integration yield exactly the same three coefficients.

In particular it exceeds the certified V4.6 upper endpoint for that
construction by more than 63/100000. This does not establish optimality of
the new constants, this family, or the unrestricted auction problem.

## 1. Constants and complete menus

Write

\[
A=a=2/3,\quad c=47/150,\quad b=A+c=49/50,
\quad s=7/6,\quad d=s-a=1/2,\quad q=s-b=14/75.
\]

Also put

\[
b_0=(4-\sqrt2)/3,\qquad T=1-2c/3=178/225,
\qquad U=5/3-2c=26/25.
\]

All values are exact. For an opponent report w, let t=max(w), rho=min(w),
z=sum(w). If there is a unique high coordinate, call the corresponding
physical item scarce and the other item safe. This naming just fixes the
coordinate orientation in the formulas.

**Q: t<=A and z<=b.** When t<=d, offer empty, both physical singletons at
price A, and the bundle at C=max(b0,z). When d<t<=A, put

\[
k=t-q,\quad C_0=5/6+3k^2/4,\quad C=\max(C_0,z).
\]

Offer empty, safe at C-k, scarce at A, and the bundle at C. The high
coordinate is unique because z<=b<1 and t>d.

**E: A<t<T and rho<c.** Put

\[
\delta=9(T-t)(U-t)/16,\quad \alpha=3t-2,
\quad \beta=\frac{\alpha}{\alpha+2\delta}.
\]

Offer, in order, empty at 0, safe at d+delta, scarce at t, bundle at
t+c+delta, and the lottery assigning the scarce item surely and the safe
item with probability beta at payment t+beta*c. Thus 0<beta<1.

**Everywhere else: affine-base menu.** Let

\[
H(w)=\max(0,w_1-a,w_2-a,w_1+w_2-b).
\]

The two singleton prices are

\[
P_1=H+\min(a,s-w_2),\quad P_2=H+\min(a,s-w_1),
\]

and the bundle costs H+b. These are the menus of the common maximizer over
all nine feasible deterministic allocations, with costs
`0,a,a,b,a,a,b,s,s` in the order
`(0,0),(1,0),(2,0),(3,0),(0,1),(0,2),(0,3),(1,2),(2,1)`.

Empty at price zero is included in every row. Q is closed; E excludes its
rho=c, t=A, and t=T faces. All unlisted faces use the explicit remaining
base rule. In particular the algebraic sum=b0 face is included in Q and
uses the identical maximum price formula.

At a report profile, form each bidder's full set of menu maximizers. If
its maximum utility is zero, replace its maximizer set by empty alone.
Among all pairs in the two resulting finite sets whose item marginals
sum to at most one, choose the lexicographically first pair in the menu
orders above; base menu order is empty, item 1, item 2, bundle. Charge the
selected option's price. The proof below establishes that this set is
nonempty at every real profile, so this is a definition without an
unresolved selection condition.

## 2. All-real pointwise feasibility

The proofs use only inequalities in the reports. The rational replay is
additional implementation evidence and is not a finite-grid proof.

The retained base has a common feasible maximizing allocation at every
profile. Zero-utility bidders can be changed to empty without affecting
the other's allocation, so a feasible pair of retained base maximizers
always exists. Every base singleton price is at least d=1/2; its bundle
price is at least b and at least the opponent's sum. In the aligned
coordinates, its bundle-minus-scarce price is at least c.

### Q against the retained base

Fix w=(t,rho) in Q and let v=(x,y) be the other bidder's own report, with
x on w's high physical coordinate. If t<=d, neither singleton can give w
positive utility under the retained base; its sum is at most b, so it
cannot buy the base bundle either. The other bidder's whole Q menu is
then feasible.

If t>d, rho<=b-t<d excludes w's safe singleton, and z<=b excludes its
bundle. It can only take the scarce item. When y<=d, its scarce price is
H(v)+A>=A>=t. When y>d, that price is at least x+q. Therefore a positive
retained-base scarce purchase requires x<k=t-q. The Q menu allocates its
scarce item only if x>=k: a scarce singleton needs x>=A>k, and comparing
the bundle to the safe singleton gives x>=k. At x=k, the opposing base
utility is at most zero, so the empty-at-zero rule resolves equality.
No other item conflict is possible.

### Q against Q

A bidder whose own report is in Q cannot have a positive scarce-singleton
utility, because every own coordinate is at most A. A safe singleton in
a constrained Q menu has price C-k>d. To verify the latter uniformly,
k lies in [c,A-q], and C0-k is decreasing there; its endpoint value is
strictly greater than d. In a free Q row all singleton prices are A.
Thus positive choices in a Q/Q pair are only bundles or safe singletons.

If either menu is free, its Q buyer has no positive singleton utility;
that buyer can only take a bundle or empty. A free opponent report has
both values at most d and therefore cannot buy the other constrained
menu's safe singleton either. Thus only bundle/bundle needs checking
in that case. Two positive bundles are impossible, since each bundle price is at least
the opponent's sum. With the same high physical coordinate, each bidder's
own safe value is its low coordinate, below d; neither buys a safe
singleton. With opposite high coordinates, two safe choices allocate
different physical items. A bundle/safe conflict also cannot occur:
write w=(t,r), v=(x,y) with highs t and y. If v buys its safe item,
then y>C(w)-k(w)>=r+q. If w buys a bundle against v, its scarce upgrade
requires r>=y-q. These inequalities contradict each other. The safe
purchase is strict because its utility is positive. Zero utility chooses
empty, including all equal-sum bundle ties.

### E against the retained base

Fix w=(t,rho) in E. At every opponent report v=(x,y), the retained base
cannot allocate w its low item or bundle: rho<c<d, all singleton prices
are at least d, and the bundle-minus-high price is at least c. It can
only allocate w its scarce item. For y<=d its scarce price P obeys

\[
P\ge\max(x,x+y-c),
\]

and for y>d it obeys P>=x+q.

Every E option that gives the other bidder the scarce item makes P>=t.
For its scarce singleton x>=t suffices. For its bundle, comparing to the
safe option gives x>=t-q; when y>d use P>=x+q, and when y<=d its
nonnegative utility gives x+y>=t+c+delta and hence P>=x+y-c>=t.
For its lottery, comparison to scarce and bundle confines y to
[c,Y], where

\[
Y=c+\frac{\delta}{1-\beta}\le d.
\]

Indeed `d-Y=(T-t)[3/2-9(U-t)/16]>0` throughout E.
The lottery utility inequality gives x+beta(y-c)>=t. Since
x+y-c>=x+beta(y-c) for y>=c, again P>=t. Consequently the opposing
retained-base row is empty at a conflicting equality and no positive
conflict occurs. The safe item is always available.

### E against Q

The report v that triggers Q has both coordinates at most A and sum at
most b. It cannot buy an E scarce singleton at price t>A. A positive E
bundle or lottery purchase would imply x+y>t+c>b, also impossible.
Therefore it can only buy E's safe item, with y>d+delta>d. Its own Q
high coordinate is then y. The opposite bidder w has low value rho<c,
below the Q scarce-upgrade threshold y-q>c, so its Q choice cannot use
the conflicting physical item. Equality at zero chooses empty.

### E against E

Both own low values are below c. With matching high orientations, the
lottery and bundle are dominated by the scarce singleton. With opposite
orientations, an E bundle needs scarce value at least k=t-q>c, and a
winning E lottery needs scarce value at least j=1-t/2>1/2>c; hence
neither can win. The lottery/safe and lottery/empty inequalities give
this minimum at y=Y.
Only the singleton corresponding to each bidder's own high coordinate
can then have positive utility. With the same orientation
only a bidder with a strictly larger high value can buy the common
scarce item; equal highs choose empty. With opposite orientations any
positive singleton choices use different physical items.

These cases exhaust Q, E, and the base for both bidders. In a base/base
pair one uses its shared maximizer; in every other pair the strict
arguments above supply compatible positive maximizers, and zero choices
are empty. The finite joint selection in Section 1 is therefore always
well defined.

## 3. DSIC, IR, measurability, and realization

For every fixed opponent report, the selected option maximizes the
bidder's value minus its price in a complete menu that depends only on
that opponent. Changing ties among equal utility maximizers does not
alter this taxation argument. Every own misreport selects an option
already in the same menu, so truth telling weakly maximizes expected
utility against every report, not just almost every report. Empty gives
pointwise IR in expected utility and normalized zero-type utility/payment.

All parameter functions, region predicates, maxima, and finite candidate
pairs are Borel. The first feasible maximizing pair is a finite Borel
selection. Prices are nonnegative and the selected payments are bounded
by realized reported value in expectation, at most 2 per bidder. The
mechanism and its revenue are measurable and integrable. For each
physical item independently, assign bidder 1 on an interval of length
x1, bidder 2 on the following interval of length x2, and nobody on the
remainder of a fresh uniform random variable. The proved marginal
inequality x1+x2<=1 makes this a samplewise feasible implementation.
Truthfulness is in expected utility; universal truthfulness is not used.

## 4. Exact continuous revenue

For a proper discounted deterministic menu define

\[
G(A,B,C)=A(1-A)(C-A)+B(1-B)(C-B)
+C\{(1-C+B)(1-C+A)-(A+B-C)^2/2\}.
\]

Put k=t-q and

\[
I(t)=59/108+k^2/4-k^3+9k^4/16,
\quad C_0(t)=5/6+3k^2/4,
\]

\[
B_Z(t)=G(a,s-t,b),\quad
R_F=4/9+2\sqrt2/27,\quad L=1/4-(1-b)^2/2,
\quad t_b=q+\sqrt{4(b-5/6)/3}.
\]

All the following integrals have explicit polynomial integrands and
rational or quadratic endpoints:

\[
\begin{aligned}
R={}&R_{\rm base}
+4\int_{d}^{A}(b-t)[I(t)-B_Z(t)]\,dt
+4c\int_A^T\delta(t)^2\,dt\\
&+2L[R_F-G(a,a,b)]
+2\int_{b_0}^{b}(1-z)[G(A,A,z)-R_F]\,dz\\
&-\frac43\int_d^{t_b}[b-C_0(t)]^3\,dt.
\end{aligned}
\]

The factors count both bidders and both physical orientations where
appropriate. The low-square density at fixed sum z is 1-z, not twice
that quantity. The constrained-Q opportunity cost is exactly
`G(A,z-k,z)-G(A,C0-k,C0)=-(z-C0)^2`; integration over both bidders and
orientations gives the last term. The E lottery's complete menu revenue
is `G(t,d,t+c)+delta(t)^2`, including every moved own-report cell. Its
polygon-area identity is replayed directly with exact fractions.

The affine base is integrated without extending G past an unaffordable
singleton. On the ordered opponent triangle 0<=rho<=t<=1, split by the
three affine pieces of H, the two min-function boundaries t=d and
rho=d, and the singleton-price-one boundaries. When both singleton
prices are at most one use G. When the high singleton price exceeds one,
write k=C-B and use

\[
B k(1-B)+C[(1-k)(1-B)+(1-k)^2/2].
\]

When both singleton prices exceed one, only the bundle can sell and its
revenue is C(2-C)^2/2. These cases apply on their clipped affine cells.
Exact Green integration of each rational polynomial over its rational
polygon gives

\[
R_{\rm base}=\frac{330901662677}{379687500000}.
\]

There are nine positive-area clipped cells. The cells have total ordered area exactly 1/2.
The code multiplies the resulting one-bidder ordered integral by four.

`parameter_revenue.py` performs those exact polynomial operations and
uses rational square-root brackets for b0 and tb. The final expression
belongs to the biquadratic field Q(sqrt(2),sqrt(11)); it contains
no logarithms, variational supremum, numerical quadrature, or unspecified
root. The stored rational enclosure follows from the exact expression,
not from the floating discovery run. A separate root-agent calculation
reconstructs the coefficients independently.

## 5. Discovery boundary

Continuous conditional-menu integration first found a large improvement
when c increased from .274 to roughly .312, while d stayed exactly 1/2.
The symmetric Q replacement then eliminated the need for the asymmetric
F/G construction. Re-optimizing the enlarged family moved a to A, which
eliminated every remaining joined threshold. The frozen rational choice
c=47/150 was selected for a simple exact description; no claim is made
that it maximizes even this family. Unconstrained numerical exploration
outside a<=A was not accepted as a feasible candidate. The search
coordinates therefore generated and simplified a mechanism, rather than
being promoted to a classification of all optimal mechanisms.
