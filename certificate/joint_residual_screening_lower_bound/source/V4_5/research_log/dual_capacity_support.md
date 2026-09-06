# V4.5: a common-support obstruction and an exact repair

The successful Q screening certificate cannot be reused verbatim as part of a matching common capacity price. Its singular edge component charges bidder 1 on a set of bidder 1's opponent reports of probability zero. Emptying that bidder's entire menu on those reports leaves revenue unchanged but strictly lowers its priced allocation cost. The resulting separable dual gap is at least

\[
M=\frac{11884909837073}{6075000000000000}
  =0.001956363759188971\ldots.
\]

This is a proved obstruction to this particular support and every extension obtained by adding nonnegative prices. It is not a failure to fit coefficients, and it is not nonexistence of a common certificate. There is an exact constructive repair: transfer the problematic edge price into a positive-volume band, or transfer only its consumed part and retain an explicit moving junction measure. Both repaired measures remain tight global supports for the complete randomized inner problem on Q at the actual V4.02 residual.

The repaired support has not been shown to support bidder 1. A second exact rejection test shows why merely replacing a singular measure by an arbitrarily thin band does not solve that remaining problem.

## 1. A necessary marginal condition on every common price

Write a bidder's full DSIC/IR mechanism as \(M_i=(a_i,p_i)\), and let \(\pi=(\pi_1,\pi_2)\) be finite nonnegative Borel capacity measures on the complete four-dimensional report space. Individual allocations remain bounded between zero and one in the separated problems. Define

\[
L_i(M_i;\pi)=R_i(M_i)-\sum_j\int a_{ij}\,d\pi_j,
\qquad
U(\pi)=\sum_j\pi_j(T)+\sum_i\sup_{M_i}L_i(M_i;\pi).
\]

This is a valid weak upper bound for the unrestricted randomized joint auction: for every feasible joint mechanism, the difference between U and its revenue is the sum of nonnegative conditional-optimization regrets and the nonnegative priced capacity slack.

For each i define a finite measure on the opponent report square,

\[
\mu_i(E)=\sum_j\int 1_{\{v_{-i}\in E\}}a_{ij}(v)\,d\pi_j(v).
\]

**Necessary condition.** If \(M_i\) maximizes \(L_i\), then \(\mu_i\) is absolutely continuous with respect to the opponent's type law.

Indeed, if E is an opponent-null Borel set, replace the entire conditional menu of bidder i by the zero allocation and zero payment whenever its opponent belongs to E. This is a complete pointwise DSIC/IR, Borel mechanism: each fixed-opponent menu is either the old complete menu or the single empty option. It remains jointly feasible when the other bidder is retained. Its expected revenue equals the old revenue because E is opponent-null. Its Lagrangian value increases by exactly \(\mu_i(E)\). Therefore optimality requires \(\mu_i(E)=0\).

The condition concerns the opponent marginal of the **consumed** price. It does not require the full capacity price to be absolutely continuous in four dimensions. A singular price on a moving joint boundary, or a price on an own-report boundary consumed only by that same bidder, can satisfy this necessary condition.

## 2. The exact obstruction at V4.02

Here and below

\[
a=159/250,\quad b=91/100,\quad s=142/125,\quad
c=b-a=137/500,\quad d=s-a=1/2,\quad q=s-b=113/500,
\quad A=2/3.
\]

On the nonfree part of Q, align bidder 1's report as \(w=(t,\rho)\), with \(d<t\le A\) and \(0\le\rho\le b-t\). The scarce item is the first coordinate and bidder 2's report is \((x,y)\). Set

\[
k=t-q,\qquad C=5/6+3k^2/4,\qquad B=C-k.
\]

The old Q support contains \(F_k(x)\,dx\,\delta_{y=1}\) as the price of item 1, where for \(x<k\)

\[
F_k(x)=(2-3B)x
       =(-1/2+3k-9k^2/4)x>0.
\]

At all these reports the actual V4.02 first bidder takes item 1 exactly when \(x<k\). Its top-edge price is d for \(x\le c\), and \(x+q\) for \(x>c\). At \(x=k\), zero-utility rejection selects empty; that single x has zero edge measure. The safe coordinate remains unavailable to bidder 1. Both orientations of the opponent's high coordinate contribute.

Consequently the consumed price over the two opponent-null faces has exact mass

\[
\begin{aligned}
M
&=2\int_d^A(b-t)\int_0^{t-q}F_{t-q}(x)\,dx\,dt\\
&=\int_c^{A-q}(b-q-k)k^2(-1/2+3k-9k^2/4)\,dk\\
&=11884909837073/6075000000000000.
\end{aligned}
\]

For a small explicit witness, take \(t\in[11/20,14/25]\), \(\rho\in[0,1/10]\), \(x\in[1/10,1/5]\), and \(y=1\), with the scarce orientation fixed. Its consumed price is

\[
730317/200000000000>0.
\]

If a proposed common \(\pi\) contains this Q price and adds any other nonnegative measure, emptying bidder 1 on the union of the two opponent faces improves \(L_1\) by at least M. Hence

\[
U(\pi)-R_{4.02}\ge M.
\]

This operation has zero auction revenue gain. Nor does relaxing only this null face necessarily improve bidder 2's inner value: its pointwise IC constraints and the actual adjacent interior capacity holes remain. The operation is a separator of a proposed dual architecture, not a claimed profitable primal deformation.

## 3. Transfer the edge price without changing the screening identity

Recall the exact local identity from V3.1. For every complete randomized DSIC/IR bidder-2 mechanism with utility u and allocation a,

\[
R=\langle\pi^{\rm edge},a\rangle-3\int_{D_0}u,
\]

where

\[
\ell(x)=\begin{cases}B&x\le k,\\C-x&k<x\le A,\end{cases}
\quad
f(x)=\begin{cases}3\ell(x)-2&x\le A,\\1&x>A,\end{cases}
\quad F(x)=\int_x^1f(s)\,ds.
\]

The edge price has densities

\[
\pi^{\rm edge}_1=3(x-A)_+\,dx\,dy+F(x)\,dx\,\delta_1(dy),
\qquad
\pi^{\rm edge}_2=3(y-\ell(x))_+1_{x\le A}\,dx\,dy.
\]

The no-sale integration region is \(D_0=\{x\le A,y\le\ell(x)\}\). The equal-area relation is \(A C-A^2/2-k^2/2=1/3\), which gives \(F(0)=F(1)=0\). We have \(F\ge0\), \(f\le0\) below A, and \(\ell\le A\) on the parameter interval in use.

For any fixed \(z\in[A,1]\), integration by parts in x and the exact vertical IC envelope give

\[
\int_0^1 F(x)a_1(x,1)\,dx
=\int_0^1 F(x)a_1(x,z)\,dx
 +\int_0^1\int_z^1 f(x)a_2(x,y)\,dy\,dx. \tag{1}
\]

This equality does not use the candidate's finite menu. Horizontal IC envelopes hold separately at y=1 and y=z. The vertical envelopes then express \(u(x,1)-u(x,z)\). Thus exceptional top reports are retained throughout the argument.

Choose \(Z=5/6\), and average (1) over z uniformly on \([Z,1]\). Put

\[
H(y)=6(y-5/6)_+.
\]

The resulting **fully absolutely continuous** support has densities

\[
\boxed{
\begin{aligned}
\pi^{\rm band}_1(x,y)&=3(x-A)_++6F(x)1_{y\ge5/6},\\
\pi^{\rm band}_2(x,y)&=3(y-\ell(x))_+1_{x\le A}+f(x)H(y).
\end{aligned}}
\tag{2}
\]

For \(x\le A,y\ge Z\), its second density is

\[
(1-H(y))3(y-\ell(x))+H(y)(3y-2)\ge0.
\]

Below Z it equals the old nonnegative density. For \(x>A\), the added second density is H and is nonnegative. Thus (2) is a finite nonnegative Borel measure. Most importantly,

\[
\boxed{\langle\pi^{\rm band},r\rangle-R
=\langle\pi^{\rm band},r-a\rangle+3\int_{D_0}u\ge0}
\tag{3}
\]

for every arbitrary pointwise residual r and every complete DSIC/IR mechanism bounded by r. This is exactly the old gap identity, with a different measure. It is not a smoothing approximation.

## 4. Saturation at the actual residual, including the band edges

All frozen V3 increments vanish whenever bidder 2's safe-coordinate report satisfies \(y\ge5/6\). If \(x\le c\), the joined menu has returned to its base branch: its exact cutoff is

\[
1058587/1362000<5/6.
\]

If \(x>c\), the joined/common rows are absent, and bundle-fee rows are absent since \(x+y>c+5/6>1\). Therefore the complete retained V4.02 menu is its changed base menu throughout this band.

There the first bidder's scarce-item price is d for \(x\le c\) and \(x+q\) for \(x>c\). Its safe-item and bundle options cannot win for the stated w. Consequently its scarce allocation is exactly \(1_{x<k}\) throughout the whole band. This is a full continuum statement, not an extrapolation from sampled top reports.

The screened bidder's candidate \(u^*=\max(0,x-A,y-B,x+y-C)\) takes item 1 throughout \(x>A\), takes it on the band exactly when \(x>k\), and takes item 2 wherever the added positive second density is supported. At \(x=k\), the explicit priority chooses the safe singleton; that is pointwise feasible. The candidate also vanishes on \(D_0\). It therefore makes both terms on the right of (3) zero at the actual residual.

This proves a matching global inner support on each nonfree fiber in Q. The free-fiber SJA support can be retained: bidder 1 consumes no capacity there, so it has none of the problematic consumed-face charge. Integrating the local supports over Q gives a regional capacity support; the complementary region's inner problem is not thereby certified.

The band starts at 5/6 rather than the earlier exploratory value 4/5 so it lies above the new lottery-splice opponent region examined elsewhere in V4.5. For any later jointly feasible splice retaining Q's screened menu and the first bidder's band allocation, the same equality and saturation proof apply. No agreement outside the price supports is required.

## 5. A targeted repair with a moving junction measure

It is unnecessary to move edge price that bidder 1 does not consume. Restrict the transfer to \(0\le x<k\). Integration by parts now has a nonzero endpoint:

\[
\begin{aligned}
\int_0^kF(x)[a_1(x,1)-a_1(x,z)]\,dx
&=\int_0^k\int_z^1f(x)a_2(x,y)\,dy\,dx\\
&\quad+F(k)\int_z^1a_2(k,y)\,dy.
\end{aligned} \tag{4}
\]

After averaging z, an alternative exact support is

\[
\begin{aligned}
\pi^{\rm junction}_1
&=3(x-A)_+\,dx\,dy
 +6F(x)1_{x<k,y\ge Z}\,dx\,dy
 +F(x)1_{x\ge k}\,dx\,\delta_1(dy),\\
\pi^{\rm junction}_2
&=\{3(y-\ell(x))_+1_{x\le A}+f(x)H(y)1_{x<k}\}\,dx\,dy\\
&\quad+F(k)H(y)\,\delta_k(dx)\,dy.
\end{aligned} \tag{5}
\]

All terms are nonnegative after the same density combination as above. The candidate allocates the safe item with probability one on the added moving line \(x=k\), and the actual residual there is one. The retained top price is carried by the screened bidder, not bidder 1. Thus the gap identity, actual tightness, and the consumed-marginal test all hold.

The junction measure is forced by the endpoint term in (4). Omitting it breaks the identity. This is an explicit reason for retaining nonsmooth measures and tight incentive transport in the search: a smooth finite basis would conceal a natural exact redistribution route.

## 6. A broad band is still only an inner support

For \(Z\ge5/6\), replacing the band width by \(\epsilon=1-Z\) preserves the exact identity and inner tightness. But an excessively narrow band fails bidder 1's optimization even though it is absolutely continuous.

Take \(\epsilon=1/1000\), and an opponent report \((x,y)\) with \(1/5\le x\le1/4<c\), \(1-\epsilon\le y\le1\). Bidder 1's charge from the Q support is

\[
\frac{x}{\epsilon}\,J,\qquad
J=\int_d^A(b-t)(-1/2+3(t-q)-9(t-q)^2/4)\,dt
 =39635863/2700000000.
\]

This is at least \(200J>2\). IR and allocations bounded by one give bidder 1's conditional expected payment at most 2. Replace its complete menu by empty on this positive-measure opponent rectangle. The resulting mechanism remains complete DSIC/IR and jointly feasible. Its revenue can decrease, but its Lagrangian value strictly increases. The consumed charge removed is \(J\cdot9/800\); the revenue lost is at most \(1/10000\). Therefore every nonnegative completion of this thin-band support has gap at least

\[
\frac{15635863}{240000000000}>0.
\]

The test rejects an overly concentrated band support, not the broad \([5/6,1]\) support. No optimality of the broad support for bidder 1 is claimed. It must still be completed and tested against both full conditional objectives.

## 7. Constraints imposed by the new genuine lottery cell

Suppose the new residual-screening candidate elsewhere in V4.5 has utility

\[
u=\max\{0,x-t,y-B,x+y-C,x+\beta y-t-\beta c\},
\qquad0<\beta<1,
\]

and a genuine lottery cell L on which allocation is \((1,\beta)\) while residual capacity of item 2 is one. Any matching nonnegative local capacity measure must satisfy

\[
\boxed{\pi_2(L)=0.}
\]

Indeed, capacity complementary slackness gives \(\int_L(1-\beta)\,d\pi_2=0\). This statement excludes singular charges on L as well as positive densities. If beta depends on the opponent, apply it fiberwise; positivity of \(1-\beta\) still forces zero measure on the genuine cell.

The lottery cell is affine in the bidder's own utility. Tight IC flows may connect types whose relevant supporting affine option is the same. A prospective certificate must use that freedom to cancel the safe-item coefficient while retaining the scarce-item shadow cost and matching junction terms. A coordinate-envelope architecture that leaves positive safe-item capacity price inside L cannot match this candidate.

No complete oblique-flow certificate for the new lottery region has been proved in this note. Its zero-price condition is a compulsory restriction guiding that search, not evidence that the candidate is suboptimal.

## 8. Independent audit of the reverse lottery splice

The final evaluator `verifier/residual_lottery.py` also changes bidder 1 on opponent reports in
\(E=\{2/3<t<T,\ t+\rho\le b\}\), where \(T=(2+2q)/3=613/750<5/6\).
This does not break the three matching Q certificates above.

Fix bidder 1's report w in Q and bidder 2's report v in E. For bidder 1's new menu, the high singleton requires an own coordinate at least \(t>2/3\), which is impossible in Q. The bundle costs at least \(t+c>b\), exceeding w's total value. A positive lottery option can beat the high singleton only when the safe own coordinate exceeds c; its positive-utility region then also requires total value greater than \(t+c>b\). Thus only empty and the safe singleton can be selected at w.

The new safe-singleton threshold is \(d+\delta(t)\); the old threshold is \(d+\max(\delta_{\rm old}(t),0)\). The former is larger throughout E. Before the old cutoff, the difference is an increasing quadratic whose value at \(t=2/3\) is exactly \(2641/4000000>0\); after that cutoff, the claim follows from \(\delta(t)>0\). Consequently the reverse splice only releases this item on Q; it never consumes new Q capacity.

At any released report, w's safe coordinate exceeds d and therefore is its unique high coordinate. In the Q-screening alignment, the released item is the scarce item, its screened-bidder report is \(\rho<c\), and its other screened-bidder report is \(t\in(2/3,T)\). The original scarce volume density vanishes because \(\rho<A\); its edge component is absent because \(t<1\). The broad-band component is absent because \(t<T<5/6\). The targeted junction also cannot meet this region because its scarce coordinate is \(k=w_{\rm high}-q\ge c>\rho\).

Thus every capacity change has zero scarce price under the edge, broad-band, and targeted-junction measures. Bidder 2's Q menu is unchanged and remains jointly feasible. The exact gaps retain zero slack, proving that all three regional inner supports remain matching after the reverse splice. This is a support-preservation statement, not optimality of either new E menu in the unrestricted inner class.

An independent boundary/volume derivation also agrees with the residual agent's exclusion of the more-generous-lottery kink variation: with \(\alpha=3t-2\), \(L=Y-c\), and premium junction \(0<a<L\), its full revenue derivative is \(-\alpha a(L-a)^2/(4L)<0\). That separate result is recorded and replayed with the lottery artifacts; it is not used as a substitute for the missing full inner certificate.

## 9. Replay scope

Run `python -B -X utf8 V4_5/verifier/dual_support_verify.py` from the auction package directory. The saved certificate is `certificate/dual_support.json`; `--write` is required to regenerate it.

The replay independently checks the singular mass by two polynomial antiderivatives, the rational witness charge, the thin-band gap, the actual tariff cutoff and complete band residual at named rational boundary cases, the equal-area and junction identities, and density nonnegativity formulas. The all-real measure and DSIC claims are established in the written envelope proof; the rational cases are regression checks, not a finite-type-grid proof or a formal proof-assistant kernel.

No new universal numerical auction upper bound is claimed. The achieved dual progress is an explicit obstruction, a quantified architecture gap, two exact inner-support redistributions, and complementary-slackness restrictions that a common support must satisfy.
