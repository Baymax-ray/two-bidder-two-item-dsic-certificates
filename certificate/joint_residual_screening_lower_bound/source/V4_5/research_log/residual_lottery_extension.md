# Actual-residual lottery improvement outside Q

First this route keeps bidder 1 **exactly V4.02** and changes bidder 2 on
complete opponent fibers. A second, separately proved compatible splice
applies the same menu to bidder 1 and doubles the gain. All previous
packages are read-only dependencies. The new mechanism has a strictly
larger exact revenue; full conditional optimality is not proved for the
new five-option menu.

## 1. The actual capacity restriction

Write

`a=159/250`, `b=91/100`, `s=142/125`, `c=b-a=137/500`,
`d=s-a=1/2`, `q=s-b=113/500`.

Fix bidder 1's report `(t,rho)`, aligned so that its first coordinate is
the larger, and suppose

`2/3 <= t <= T=613/750`, `0 <= rho <= b-t`.

Bidder 1 can receive only item 1: every retained singleton price is at
least `d`, every bundle price at least `b`, `rho<d`, and `t+rho<=b`.
Zero-utility ties are rejected. Thus item 2's residual capacity is one at
**every** bidder-2 report. No assertion about sum-above-b fibers is needed.

The shared split-cost base has bidder-2 conditional prices

`high=t`, `low=d`, `bundle=t+c`.

Since bidder 1 is a subset of that common base allocation, a conservative
description of reports where it can occupy item 1 is

`x <= t`, `x+y <= t+c` if `y<=d`, and `x<=k=t-q` if `y>=d`.

This follows directly by comparing the shared-base bidder-2 options: if
the base gives bidder 1 item 1, bidder 2's base choice is empty or item 2.
The inequalities are deliberately weak and include all ties. The actual
capacity hole may be smaller because bidder 1's increments can discard
allocation. It is never larger. The proof below verifies every new
positive-probability allocation against this majorant of the actual hole.

## 2. Why the four-option stationary menu is insufficient

Consider any feasible four-option menu on these fibers with prices

`A=t`, `B=d+delta`, `C=t+c+delta`, `delta>0`.

Introduce the additional fixed lottery

`L=(1,beta)`, `p_L=t+beta*c`, with `0<beta<1`.

The first item is allocated surely; the second is allocated with
probability beta. Retain the four original options. This is admissible if

`beta*(q+delta) <= q`.                                      (2.1)

Indeed, in the cap hole with `y<=c` its utility is at most zero. For
`c<=y<=d`, using `x+y<=t+c`, its utility is at most
`-(1-beta)*(y-c)<=0`. For `y>=d`, use `x<=k`. Below `B` its utility is
at most `-q+beta*(B-c)<=0`. Above `B` its utility minus the low-singleton
utility is at most `-q+beta*(B-c)<=0`. Therefore it cannot be chosen in
the hole if empty and the low singleton precede it at ties. This verifies
feasibility even at a singular cap boundary, without relying on an
almost-everywhere derivative.

Let `H=C-t=c+delta`, `Y=c+delta/(1-beta)`. Condition (2.1) says exactly
`Y<=B` and places the lottery cell wholly above the cap hole. The lottery
changes choices only on

`c<y<Y`, `x>t-beta*(y-c)`.

Below `H` it replaces high-singleton sales and gains new buyers. Between
`H` and `Y` it also replaces bundle sales. Integrating **all** these cells,
including the payment losses of the latter buyers, gives the exact gain

`Delta_L = delta^2/2 * [(3t-2)z-delta*z^2]`,
`z=beta/(1-beta)`.                                         (2.2)

In particular, its derivative at beta zero is
`delta^2*(3t/2-1)>0` whenever `t>2/3`. This is a strict admissible
conditional improvement under the actual residual. It invalidates full
inner optimality of that four-option stationary menu. No conclusion is
drawn merely from failure of a chosen dual basis.

The maximizing admissible value in this one-lottery family is

`beta=(3t-2)/(3t-2+2delta)`,
`Delta_L=delta*(3t-2)^2/8`,                                 (2.3)

provided `(3t-2)/2<=q`. These equations are derived from the complete
revenue variation, not pointwise virtual surplus.

## 3. Jointly optimize the bundle and lottery parameters

For fixed `t` and `k=t-q`, the four-option revenue is a concave quadratic
in delta, with stationary value

`delta0=1/2-c+3q^2/4-3qt/2`.

Adding (2.3) makes its maximizing value

`delta*=delta0+(3t-2)^2/16`
`       = (9/16)(T-t)(U-t)`,
`T=(2+2q)/3=613/750`, `U=(2+6q)/3=839/750`.                 (3.1)

The exact factorization uses the actual V4.02 equality `d=c+q=1/2`.
Hence delta is positive throughout `2/3<=t<T` and zero at T. The
admissibility condition in (2.3) holds throughout this interval.

On the closed band set delta by (3.1) and beta by (2.3). At `t=2/3`,
beta is zero and the lottery duplicates the high singleton. At `t=T`,
delta is zero and beta is one, so it duplicates the bundle. There is no
undefined endpoint or limiting-only mechanism.

The V4.02 retained delta on the open band is

`delta_old(t)=max(0,1/2-c+3q_old^2/4-3q_old*t/2)`,
`q_old=227/1000`.

For `t>=2/3`, `delta0-delta_old_raw`
`=(q_old-q)*(3t/2-3(q_old+q)/4)>0`. Before the old cutoff this proves
`delta*>=delta_old`; afterwards the old delta is zero. Thus first raising
both B and C from the V4.02 retained menu to the four-option menu of
Section 3 preserves a maximizing subset of every original chosen mask.
In this step empty and high singleton do not change; the low singleton
can only be discarded, and a bundle can only be retained or contracted.
Feasibility also follows directly from the base cap inequalities.
The subsequent lottery addition is justified separately by Section 2.

## 4. Complete pointwise mechanism

Compute the complete V4.02 mechanism first and keep bidder 1 unchanged.
Outside the opponent region

`E={w: 2/3<max(w)<T, w1+w2<=b}`,

keep bidder 2 unchanged. On E align the first item with the unique high
coordinate of w and offer these five options in this priority order:

1. Empty, allocation `(0,0)`, payment zero.
2. Low singleton, allocation `(0,1)`, payment `B=d+delta*`.
3. High singleton, allocation `(1,0)`, payment `t`.
4. Bundle, allocation `(1,1)`, payment `C=t+c+delta*`.
5. Lottery, allocation `(1,beta)`, payment `t+beta*c`.

Choose the first maximum of reported expected utility. The ordering
implements the hole proof at every tie. The four deterministic options
also cannot be positive maximizers in that hole except the low singleton:
the high singleton has utility at most zero, and for `y<=d` the bundle
has utility at most `-delta*`; for `y>=d` the bundle-minus-low difference
is `x-k<=0`. Low-singleton priority resolves the equality.

Every fixed-opponent section is a complete menu over all own reports, so
the taxation inequality proves randomized DSIC and IR against every
misreport. Finite options and rational Borel price functions prove joint
measurability. Payments lie between zero and reported allocated value,
hence are bounded. An implementation can toss one Bernoulli(beta) coin
for the low item when the lottery is selected: bidder 1 never receives
that item on E, so each realized allocation is feasible. Exceptional
opponent reports, all own-report ties, and both item orientations are
explicitly included.

At t=2/3 and t=T the implementation keeps the entire old row and its
tie choices. The displayed formulas also have defined endpoint values:
at 2/3 the four-option menu agrees with the existing Q menu and the
lottery duplicates the high singleton; at T it duplicates the base
bundle. No limiting convention is needed for any report.

## 5. Exact whole-auction gain

Let `t_old=(1/2-c+3q_old^2/4)/(3q_old/2)`. It lies strictly between
`2/3` and T. Define

`g1(t)=(delta*(t)-delta_old_raw(t))^2`
`      +delta_old_raw(t)*(3t-2)^2/8`,
`g2(t)=delta*(t)^2`.

The exact gain of this **one-sided** splice over V4.02 is the rational number

`2 integral_(2/3)^(t_old) (b-t) g1(t) dt`
`+2 integral_(t_old)^T (b-t) g2(t) dt`.                    (5.1)

The factor two is the two item orientations for the one changed bidder.
The other bidder's revenue is unchanged. Formula (5.1) counts the full
own-type square on each changed opponent fiber. There is no omitted
transition-region correction: all polynomial formulas coincide at
the old cutoff. The verifier publishes the numerator and denominator,
the coefficients of both integrands, and representative exact boundary
and lottery witnesses. This is an exact lower-bound increment, not a
decimal optimization result.

## 6. The same conditional change can be made to both bidders

Also replace bidder 1's row when bidder 2's report lies in E, using the
same rotated menu and priority. The earlier one-sided proof applies
unchanged when bidder 1's report is outside Q and outside E: bidder 2 is
then the retained subset of the common base. Two additional situations
must be checked rather than assumed.

**Both reports in E.** Each report sums to at most b, whereas the other
bidder's bundle price exceeds `t+c>b`, so neither buys a bundle. If the
high coordinates coincide, each aligned low coordinate is at most
`b-2/3<c`; hence neither lottery nor low singleton can be chosen. Only
the bidder with strictly larger high coordinate buys the high singleton;
equal high coordinates give zero utility and both choose empty. If high
coordinates differ, the aligned high-item value is below `b-2/3`, while
any lottery buyer has that value at least `k=t-q>2/3-q`. Hence lotteries
and high singletons are impossible and both may buy only their distinct
low-of-opponent singleton items. These statements include every tie.

**Bidder 1's report in Q, bidder 2's in E.** Write bidder 2's report as
`(t,rho)` and bidder 1's as `(x,y)` in that alignment. The new high
singleton is impossible because `x<=2/3<t`. Its bundle is impossible
because `x+y<=b<t+c`. A chosen lottery would require `y>=c` and
`x>=t-beta*(y-c)`, implying `x+y>=t+c>b`, also impossible. Thus bidder 1
can only take the low singleton. If it does, `y>=B=d+delta>d`, and
`x<=b-y<y`, so the high coordinate for bidder 2's inherited Q menu is
the physical y item. Its own value for that item is `rho<=b-t<c`.
This is below its singleton price `2/3` and below its bundle upgrade
threshold `y-q>=c+delta`. Hence bidder 2 cannot consume the item sold to
bidder 1. At the low-singleton entry tie the new bidder 1 chooses empty.

The complementary case is the one-sided proof already established.
Thus both row replacements are jointly feasible at every profile. They
remain complete own-report menus, so DSIC/IR and measurability follow
as before. The exact total revenue gain is **twice** (5.1), because
expectation is additive and on E both original rows have the same
retained four-option menus. No independence of the two allocation changes
is needed for this revenue identity.

`asymmetric_mechanism` retains the one-sided candidate as a separately
reviewable representative; `mechanism` applies both changes. The full
auction still inherits the original bidder-asymmetric Q rule and must
not be called globally bidder-symmetric.

## 7. What this says about the residual problem and dual search

The existing Q certificate still excludes any improvement with bidder 1
fixed to V4.02 on Q. It also survives the reverse splice in Section 6:
at own w in Q, both the old and new bidder-1 rows against an opponent in
E can take only the low-of-opponent singleton. Any change therefore
concerns w's high item y, with y>d; bidder 2's value for that item is
`rho<=b-t<c<2/3`, and its other value is `t<T<1`. The inherited Q price
for the scarce high item is supported on `x>2/3` in volume and on the
top edge of the other coordinate. Both supports miss the capacity
change, and the other item's capacity is unchanged. Therefore
`<pi_Q,r_new-r_old>=0`. The unchanged Q menu remains feasible by Section
6 and has the same revenue, so the same full randomized inner support
is still tight at the new actual residual on Q.

In contrast, the adjacent t>2/3, sum<=b region admits a
strict inner improvement even after the four-option bundle parameter is
reoptimized. The new lottery uses a binding corner of the actual
residual-capacity geometry, `(t,c)`, and its payment is the support of
that corner in allocation direction `(1,beta)`.

The first high-item cap constraint at low y really does prevent lowering
the deterministic singleton price below t. It does **not** prevent
replacing a portion of the high-singleton region by the displayed
lottery. Thus treating this singleton-price constraint as a sufficient
conditional certificate would incorrectly classify an improvable fiber
as requiring an outer allocation change.

Any proposed common capacity measure supporting the original four-menu
candidate on a positive-measure portion of this region contradicts the
strict feasible gain (2.2). A revised support must accommodate the
lottery, including its unsaturated second marginal, its binding cap
corner, and the new bundle/lottery boundary. Stationarity in the explicit
five-option family is not a proof that this revised candidate solves the
full randomized inner problem. No such full support is claimed here.
