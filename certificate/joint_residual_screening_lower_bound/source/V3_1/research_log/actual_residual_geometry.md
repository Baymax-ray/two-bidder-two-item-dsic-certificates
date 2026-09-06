# The actual nonfree residual under a fixed V3 bidder

The V3 allocation leaves a genuinely type-dependent residual for bidder 2. This note identifies that residual exactly on a useful opponent chamber, then derives restrictions that apply to arbitrary randomized screening mechanisms. It does not infer an inner optimum from a deterministic menu calculation.

Subsequent resolution: [constrained_screening.md](constrained_screening.md) supplies a full randomized gap certificate, and [closed_region_audit.md](closed_region_audit.md) verifies its application to every fiber of the closed region \(Q\). The geometrically admissible lottery freedom identified below does not improve the certified inner optimum. The remaining unknown is outside that region and in the outer bidder optimization.

Use the frozen V3 constants

\[
a=159/250,\quad b=91/100,\quad s=1137/1000,\quad
c=b-a=137/500,\quad d=s-a=501/1000,\quad q=d-c=227/1000.
\]

Let \(t_0=q+\sqrt{r_0}\), \(r_0=b^2-(2/3+c^2)\), and let \(t_1=q+\sqrt{4c/3-2/9}\). Numerically, \(t_0\approx0.52086618\), \(t_1\approx0.60530029\); these decimals are explanatory only.

Fix bidder 1 report \(w=(t,\rho)\), and write bidder 2's full own report as \(z=(x,y)\). Initially assume

\[
d<t<t_0,\qquad 0\le\rho<b-t.
\]

Set \(B_0=s-t\) and \(k=b-B_0=t-q\). The opposite item orientation is obtained by interchanging coordinates.

## 1. Only one of bidder 1's items can be present

Every V3 singleton price is at least \(d\), and every bundle price is at least \(b\), uniformly over the opponent report. Since \(\rho<b-t\le b-d<d\) and \(t+\rho<b\), bidder 1 cannot receive item 2 or the bundle at any \(z\). Every such utility is strictly negative. Its allocation is therefore either empty or item 1, determined solely by whether the final conditional item 1 price is below \(t\).

Consequently the residual for bidder 2 has the form

\[
r_2(x,y)=1,\qquad r_1(x,y)=\mathbf1\{(x,y)\notin H_t\}.
\]

It is independent of \(\rho\) throughout the specified interval. At an exact equality between item 1 price and \(t\), bidder 1's maximal utility is zero and the V3 tie rule selects empty, so the point belongs to the available residual.

## 2. The containing rectangle and the exact top-edge cap

The shared affine base's conditional item 1 price is

\[
P_1^0(x,y)=\max(0,x-a,y-a,x+y-b)+\min(a,s-y).
\]

Because \(t<a\), it is below \(t\) if and only if

\[
x<k,\qquad y>B_0.
\]

Indeed, \(y\le d\) implies \(P_1^0\ge a>t\). For \(y>d\), writing the four pivot inequalities as \(H(x,y)<y-B_0\) gives \(y>B_0\), \(x<k\), and two redundant inequalities. Redundancy follows from \(B_0<a\) and \(k<B_0\). Thus the base occupation set is exactly a rectangle. V3 prices are nonnegative increments of this base, giving

\[
H_t\subset\{x<k,\ y>B_0\}.
\]

More significantly, the actual V3 top-edge occupation is exactly

\[
H_t\cap\{y=1\}=\{(x,1):0\le x<k\}.
\]

For \(x\le c\), the terminal joined branch at opponent high value one prices bidder 1's item 1 at \(d<t\). For \(c<x<k\), the opponent sum exceeds one, so every inherited bundle-pivot fee is absent; the final price is \(x+q<t\). For \(x\ge k\), the base does not allocate item 1, so neither can V3. At \(x=k\) the item is available by the zero-utility tie rule.

The entire argument in this section, including \(\rho\)-independence, remains valid on the larger range \(d<t<t_1\), \(0\le\rho<b-t\). In particular, no inherited fee depends on the fixed \(\rho\) when computing bidder 1's conditional menu: that menu depends on \((x,y)\), while the low own value \(\rho\) only rules out the other own options.

## 3. Exact interior occupation on the initial chamber

Define

\[
h(t)=\frac{1/2+q+3q^2/4-t}{3q/2}.
\]

For \(d<t<t_0\), the actual occupation set is the following disjoint union:

\[
H_t^{\mathrm{joined}}=\{0\le x\le c,\ y>h(t)\},
\]

\[
H_t^{\mathrm{tariff}}=
\{c<x<k,\ x+y>b,\ f_B(x,y)<k-x\}.
\]

Here \(f_B\) is the inherited bundle common fee selected with its **original first-match rule**, and zero if no bundle row matches. This is an exact all-report formula, including row endpoints. The executable predicate is `actual_hole` in the associated verifier.

To prove the first formula, restrict to the containing rectangle. Its high coordinate satisfies \(y>B_0>t_1\). When \(x\le c\), the entire rectangle portion is in V3's joined chamber. The low-item quadratic price before \(y=2/3\) is

\[
Q(y)=5/6-(y-q)+3(y-q)^2/4.
\]

It decreases to \(Q(2/3)=1/2+3q^2/4>t_0\), so it cannot allocate item 1 here. The next branch prices that item at \(1/2+q+3q^2/4-3qy/2\); its crossing with \(t\) is exactly \(h(t)\). This height lies strictly between \(2/3\) and V3's final transition. The terminal branch prices the item at \(d<t\). These facts prove the first formula with the strict crossing inequality.

For \(x>c\), a point in the base rectangle with \(x+y\le b\) lies in the joined chamber below \(y=a\), where the same quadratic lower bound rules out occupation. If \(x+y>b\), the point is outside the joined chamber. Its base item 1 price is \(x+q\); common Z/S rows are absent, and only the inherited bundle fee can apply. The resulting strict condition is \(x+q+f_B<t\), as stated. No selective singleton surcharge applies on this piece.

The normalized bundle-row coordinate is \((x-c)/(x+y-c-d)\). Each original row is therefore bounded by affine inequalities after clearing its positive denominator. The actual cap hole is a finite collection of polygonal pieces and an affine-threshold strip, with exact inherited boundary priority. It is substantially smaller than the containing rectangle.

## 4. Exact support of the actual hole for prospective lotteries

On the positive-width interval

\[
127/250\le t\le51/100,
\]

all relevant normalized bundle coordinates are below \(1/8\). Rows B1.1 through B11.1 have fees at least \(91/10000\), exceeding \(k-c=t-d\), and consequently contain no occupation. The remaining lower corners of the closure of the tariff hole are

\[
\begin{aligned}
P_{12}(t)&=(k-63/10000,\ 193/200-k+63/10000),\\
P_{13}(t)&=(k-7/2000,\ 97/100-k+7/2000),\\
P_{14}(t)&=(k-7/10000,\ 39/40-k+7/10000),\\
P_{15}(t)&=(k,\ 49/50-k).
\end{aligned}
\]

The first three come from B12.1, B13.1, and B14.1. Above total value \(49/50\), every bundle fee is absent. Original first-match ties can exclude a displayed corner from the occupation set itself; each is nevertheless a limit of occupied points, which is the appropriate object for a supremum. The corner \((c,h(t))\) of the joined strip is dominated by \(P_{12}\): the latter has strictly larger first coordinate and strictly smaller second coordinate throughout the interval.

For every lottery vector \((\alpha,\beta)\in[0,1]^2\), one therefore has the exact support identity

\[
\sup_{(x,y)\in H_t}\{\alpha x-(1-\beta)y\}
=\max_{j\in\{12,13,14,15\}}
\{\alpha P_{j,x}-(1-\beta)P_{j,y}\}.
\]

Within each tariff cell the linear expression is maximized at the largest permissible \(x\) and the smallest permissible total \(x+y\), because \(\alpha+1-\beta\ge0\). This proves the identity on the whole cap hole, not only at sampled points.

At \(t=51/100\), these corners are exactly

\[
(2767/10000,6883/10000),\quad(559/2000,1381/2000),\quad
(2823/10000,6927/10000),\quad(283/1000,697/1000).
\]

Suppose an already feasible bidder 2 menu retains the item 2 option at price \(B\). An added lottery \((\alpha,\beta,p)\) is certainly safe against the actual cap hole if

\[
p\ge B+\max_j\{\alpha P_{j,x}-(1-\beta)P_{j,y}\},
\]

and ties give priority to the existing feasible options. On each occupied point this inequality makes the new lottery no better than the available item 2 option. Outside the hole, both item marginals are free. The condition permits lotteries that the larger base rectangle would disallow. It certifies capacity and complete-menu DSIC; it does not by itself establish a positive revenue effect.

## 5. IC propagation from the cap to every offered lottery

Let \(u\) be the normalized truthful utility of **any** bidder 2 mechanism satisfying the actual residual, with arbitrary randomized allocations. On the top edge \(0\le x<k\), allocation of item 1 is zero pointwise. Applying the two DSIC inequalities between \((x,1)\) and \((x',1)\) shows

\[
u(x,1)=u(x',1)=K.
\]

Bounded allocations make \(u\) Lipschitz, so continuity extends this equality to \(x=k\). If the mechanism offers allocation \((\alpha,\beta)\) at payment \(p\) at **any** report, its incentive inequality against every top-edge type implies

\[
\alpha x+\beta-p\le K\quad(0\le x<k),
\qquad\text{hence}\qquad p\ge k\alpha+\beta-K.
\]

This restriction applies to an arbitrary allocation range and is forced by the coupled incentive inequalities along the occupied top edge. It does not presuppose a finite menu.

If a candidate retains item 2 at price \(B\) and top utility \(K=1-B\), the bundle restriction becomes \(C\ge B+k\). More generally a lottery with \(\beta=1\) cannot beat that item 2 option below \(x=k\). Allocation of item 1 below \(k\), when admissible, therefore needs another component or a change of the existing utility/payment structure. On the initial chamber the joined strip supplies the stronger local identity \(u(x,y)=g(y)\) for \(0\le x\le c\), \(y\ge h(t)\), by the same DSIC and continuity argument.

The unrestricted full-capacity SJA fails this residual. At \(t=51/100\), \(\rho=1/100\), \(z=(1/4,99/100)\), bidder 1 receives item 1, while SJA would strictly allocate the bundle to bidder 2. This is an occupied interior profile, not merely a top-edge or tie obstruction.

## 6. A revenue test that rejects unproductive option additions

For any normalized utility with allocations in the unit square,

\[
R(u)=\int_0^1u(1,y)\,dy+\int_0^1u(x,1)\,dx-3\int_{[0,1]^2}u.
\]

Adding a menu option replaces \(u\) by a pointwise larger convex function. If it leaves both upper-edge utility traces unchanged, its exact revenue effect is

\[
R(u_{\mathrm{new}})-R(u)=-3\int(u_{\mathrm{new}}-u)\le0,
\]

strictly negative when utility increases on a positive-area set. Thus a lottery that is feasible only because it remains dominated on both upper edges cannot improve revenue merely by being appended to the menu. A profitable change must affect at least one upper trace or alter other offers as well. This test does not exclude simultaneous menu redesign or lotteries with new exposed upper-edge regions.

## Verification and remaining scope

The exact verifier checks the branch-separation inequalities, tariff entries and priorities, four support corners and their validity on a positive-width opponent interval, plus selected rational threshold and table-boundary reports at several \(\rho\) values. It replays the actual frozen V3 mechanism. These calculations accompany the analytic all-report arguments; they are not a discretized inner optimization.

The geometric findings identify genuine feasible freedom and exact IC restrictions. They alone do not prove that a four-option screen is optimal; that conclusion now follows from the separate full randomized certificate linked above. The support formula in this note is for the **actual cap hole as a geometric set**; it must not be confused with the supporting capacity-price measure subsequently obtained for the residual revenue functional.
