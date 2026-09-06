# A positive functional exchange, and a rejected neighboring direction

The clean three-region mechanism in `parameter_rebuilt_family.md` remains
the main structural construction. This separate mechanism shows that its
exchange boundary still has profitable functional freedom. It changes
both bidders' full menus coherently, rather than holding one residual
allocation fixed and changing a pointwise threshold.

With the constants from that construction, define the tent phi supported
on

\[
L=8/25=.32,\quad M=33/100=.33,\quad U=17/50=.34,
\]

with height one at M and affine slopes on [L,M] and [M,U]. For
0<=epsilon<=1/1000 set

\[
h(x)=x+q+\epsilon\phi(x).
\]

This continuous function is strictly increasing, with slopes 1 outside
the support, 1+100epsilon on the rising side, and 1-100epsilon on the
falling side. Its inverse is explicit on those three affine pieces.
The endpoints of its changed image are L+q and U+q, independently of
epsilon. The final candidate uses epsilon=1/1000.

## 1. Complete coordinated menu definition

On Q with t>1/2 replace the old k=t-q by k=h^{-1}(t) and use

\[
C=\max\{5/6+3k^2/4,\;t+\rho,\;k+h(\rho)\},
\quad B=C-k,
\]

with scarce singleton A, safe singleton B, and bundle C. Empty is free.
On the Q free branch t<=1/2 keep the clean candidate's menu exactly.
Keep every E lottery exactly.

At every remaining base report whose low coordinate rho lies in the
support, add epsilon*phi(rho) to the safe singleton and bundle prices,
leaving the scarce singleton unchanged. All other base menus are
unchanged. Here safe is the physical item aligned with the opponent's
low coordinate; on this support the high coordinate is unique.

At all real profiles, use the same complete maximizing-pair rule as the
clean construction: zero utility selects empty; otherwise choose the
first jointly feasible maximizing pair in the fixed menu orders. Closed
support endpoints have phi=0, and the two tent pieces agree at M. The
inverse pieces agree at their knots. Thus no report or tie is omitted.
The exact rational evaluator is `functional_exchange.mechanism`.

## 2. Pointwise feasibility of the sufficient h family

The base changes increase the safe and bundle prices by the same
nonnegative amount. Their contraction property uses the actual discounted
base tariff. For a changed base opponent `(t,r)` with `L<r<U`, its aligned
prices are `P=t+r-c`, `B=r+q`, and `C=t+r`. They satisfy
`C-B=t-q<P`, since `P-(C-B)=r+q-c>0`. If an original safe singleton
maximizes utility at own report `(x,y)`, comparison with the bundle gives
`x<=C-B<P`; therefore the scarce singleton has strictly negative utility.
The common surcharge leaves the bundle-minus-safe threshold unchanged,
so the safe singleton can remain a maximizer or be replaced by empty.
An original scarce maximizer remains a maximizer because its price does
not change while both competing nonempty prices rise. An original empty
maximizer stays empty, and an original bundle contains every new outcome.
Thus every original base maximizer admits a new maximizing allocation
that is a subset of it, including ties. Selecting these subsets of a
shared feasible base pair proves base/base feasibility. Selecting a subset
of the clean compatible base choice also preserves every E/base pair.
This argument is specific to the verified discounted tariff; a generic
safe/bundle surcharge would not justify contraction without it.

In a Q/Q pair every positive choice is a safe singleton or bundle, as
before: k<=t-q, and `5/6+3k^2/4-k` is decreasing in the relevant k range,
so the safe price remains strictly above 1/2. The C>=sum(opponent)
condition rules out two positive bundles. With opposite orientations,
a safe purchase by one bidder requires its high value y>B(w)>=h(rho).
A conflicting bundle by the other requires rho>=h^{-1}(y), or
h(rho)>=y. Strict monotonicity gives a contradiction. Same orientations
and the free-Q cases are handled exactly as in the clean construction.

For Q against a changed base row, the Q opponent w=(t,rho) cannot receive
a positive base bundle or safe singleton, because its sum is at most b
and rho<1/2. Consider only its scarce item. If the other report is
v=(x,y) with y<=1/2, its base price is at least A>=t. If y>1/2 and
x is outside the tent, its price is at least x+q=h(x). If x is inside
the tent, v outside Q must have y>x and y>1/2; the price of that physical
item is exactly the safe price to which the surcharge is applied.
It is therefore at least x+q+epsilon*phi(x)=h(x). A positive base
purchase requires h(x)<t, whereas a Q bundle or scarce singleton needs
x>=k=h^{-1}(t). The conflict is impossible, and equality leaves the
opposing utility at zero.

For E/Q, the clean argument still excludes an E bundle, lottery, or
scarce singleton bought at a Q own report. A positive E safe purchase
has value y>1/2. The opposing Q scarce threshold is now h^{-1}(y)>c,
since h(c)=c+q=1/2 and h is increasing. The E own low value is below c,
so it cannot acquire that scarce item. E/E is unchanged. These cases
prove nonempty feasible maximizing sets for every real profile.

Menu maximization, empty, and finite Borel selection give pointwise DSIC
and IR in expected utility. All prices remain bounded and nonnegative.
The per-item marginal realization from the clean construction gives
samplewise allocation feasibility. No type grid or numerical regularity
assumption enters these arguments.

## 3. The extra maximum is provably slack for this low tent

The definition includes the constraint C>=k+h(rho), which is useful for
the global proof. For this particular support it does not create an
additional revenue cell.

If rho is outside [L,U], then h(rho)=rho+q and t-k>=q, so
`t+rho>=k+h(rho)`. If rho is inside [L,U], Q implies t<=b-rho and
k<=t-q<=b-rho-q. Let B0(k)=5/6+3k^2/4-k. This function is decreasing
on the entire relevant interval. Furthermore

\[
\frac{d}{d\rho}\{B_0(b-\rho-q)-\rho-q\}
=-\frac32(b-\rho-q)<0.
\]

Hence uniformly over the full affected Q set,

\[
B_0(k)-\rho-q\ge B_0(b-U-q)-U-q=14/1875>1/1000.
\]

Thus B0(k)>h(rho), even at the largest allowed epsilon, and

\[
C=\max\{C_0(k),t+\rho\},\qquad C_0(k)=5/6+3k^2/4.
\]

This is an all-real inequality, not a numerical search for a missing
binding cell. Consequently the Q menu changes only for
`t in [L+q,U+q]`.

## 4. Exact whole-mechanism revenue variation

Let

\[
I(k)=59/108+k^2/4-k^3+9k^4/16,
\qquad C_0(k)=5/6+3k^2/4.
\]

For every affected k, C0(k)<b and C0(k)>h(k). Integrating the entire
conditional menu revenue over rho gives

\[
(b-t)I(k)-\frac13[b-C_0(k)]^3.
\]

Substitute t=h(k), dt=(1+epsilon*phi'(k))dk separately on the two tent
pieces. Exact expansion and integration by parts, with phi zero at the
support endpoints, yield

\[
\Delta_Q(\epsilon)=\epsilon D_Q+
2\epsilon^2\int_L^U\phi(k)^2 I'(k)\,dk,
\]

\[
D_Q=4\int_L^U\phi(k)
\left[-(b-k-q)I'(k)-\frac32k[b-C_0(k)]^2\right]dk.
\]

The factors include both bidders and both orientations. These terms
integrate all own reports whose incentive-compatible choices move
together; they do not maximize virtual revenue independently at profiles.

For a remaining base opponent with low report r in [L,U], the high
report ranges from b-r to 1. Its original aligned prices are

\[
(A_1,B_1,C_1)=(t+r-c,r+q,t+r).
\]

Raising B1 and C1 together by epsilon*phi(r) has exact revenue effect
`epsilon*phi(r)*Gamma(t,r)-epsilon^2*phi(r)^2`, including the high-price
menu region. The derivative is

\[
\Gamma(t,r)=
\begin{cases}
1-2c+\frac32(t-q)^2-\frac32(t+r-c)^2,&t\le1+c-r,\\
\frac32-2(t+r)+\frac32(t-q)^2,&t\ge1+c-r.
\end{cases}
\]

Thus

\[
\Delta_B(\epsilon)=\epsilon D_B-
4\epsilon^2\int_L^U\phi(r)^2(1-b+r)\,dr,
\quad D_B=4\int_L^U\phi(r)\int_{b-r}^1\Gamma(t,r)\,dt\,dr.
\]

All these integrands are rational polynomials on explicitly affine
cells. Combining the two complete-bidder changes gives exactly

\[
\boxed{\Delta R(\epsilon)=
\frac{70410824789}{216000000000000}\epsilon
-\frac{31233979}{3000000000}\epsilon^2.}
\]

This quadratic is strictly increasing on the entire proved interval
[0,1/1000], so the frozen choice is its right endpoint. It gives

\[
\boxed{\Delta R=\frac{68161978301}{216000000000000000}>0.}
\]

The increment is about 0.0000003155647143564815. The final exact revenue
is the clean construction's radical expression plus this rational
increment. This is a secondary functional improvement; almost all of
the phase's gain comes from the preceding global restructuring.

## 5. Certificate failure rejects a different tent, not all functions

The first tested tent used [.34,.36,.38]. Its extra maximum cannot be
ignored globally, but every additional first-order cost from that
maximum is nonpositive. The same polynomial Q expression therefore
provides an upper bound on its right derivative. Exact arithmetic gives

\[
D_Q\le\frac{218153451}{62500000000},\quad
D_B=-\frac{728239}{168750000},
\]

\[
D_Q+D_B\le-\frac{1392246823}{1687500000000}<0.
\]

That positive tent is locally unprofitable. It is not evidence that
all monotone h deformations are unprofitable: the adjacent lower tent
above gives a complete strict improvement. Floating continuous probes
were used only to locate these directions; the accepted increment and
this rejected-direction bound are exact rational calculations.

Neither the positive finite quadratic nor this one negative directional
bound proves stationarity over all h, much less unrestricted optimality.
