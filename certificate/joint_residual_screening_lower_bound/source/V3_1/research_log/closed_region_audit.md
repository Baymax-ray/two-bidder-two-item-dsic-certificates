# Independent audit of the closed solved opponent region

This audit extends the actual-residual compatibility proof through \(t=2/3\), includes all exceptional opponent boundaries, and independently verifies the revenue accounting. The full randomized screening gap is proved separately in [constrained_screening.md](constrained_screening.md); the present note checks its application to the complete, frozen V3 first-bidder mechanism.

## 1. The closed region and its free part

Let \(A=2/3\) and

\[
Q=\{w\in[0,1]^2:\max(w_1,w_2)\le A,\ w_1+w_2\le b\}.
\]

Retain bidder 1's complete V3 allocation and payment. On the closed subset

\[
D=\{w:\max(w_1,w_2)\le d,\ w_1+w_2\le b\},
\]

every V3 nonempty option has utility at most zero for bidder 1, because singleton prices are at least \(d\) and bundle prices at least \(b\). Its zero-utility tie rule selects empty at every opponent report. Hence the residual is identically full on these entire fibers, including \(\max w=d\) and \(w_1+w_2=b\). Offering bidder 2 the SJA menu solves every one of them.

For \(w\in Q\setminus D\), choose the coordinate orientation \(w=(t,\rho)\) with \(t>\rho\). This orientation is unique: \(t>d\) and \(\rho\le b-t<b-d<d\). Put

\[
k=t-q,\qquad C=5/6+3k^2/4,\qquad B=C-k.
\]

Offer bidder 2 singleton prices \(A,B\), with the high-own-value coordinate of bidder 1 assigned price \(A\), and bundle price \(C\). The empty option is free. The complete tie order is empty, low-coordinate singleton, high-coordinate singleton, bundle. The following argument actually proves that every maximizing option is compatible with bidder 1's row, so the specified tie priority is safe.

## 2. Pointwise compatibility on all of \(Q\)

The low own value \(\rho\) is strictly less than every V3 singleton price. Bidder 1's bundle value is at most \(b\), and every bundle price is at least \(b\). The bundle may tie at zero when \(t+\rho=b\), but V3 rejects zero maximal utility. Thus bidder 1 receives either item 1 or empty at every report \((x,y)\); it can never consume item 2. If its item 1 price is at least \(t\), it also selects empty.

Write its base item 1 price as

\[
P_1^0(x,y)=H(x,y)+\min(a,s-y),\qquad
H=\max(0,x-a,y-a,x+y-b).
\]

For \(y\le d\), \(P_1^0=a+H\), so

\[
P_1^0\ge a,\quad P_1^0\ge x,\quad P_1^0\ge x+y-c.
\]

For \(y>d\), \(P_1^0=s-y+H\ge x+q\). Every final V3 price is at least this base price.

If bidder 2's high-coordinate singleton maximizes, then \(x\ge A\ge t\). The preceding price bounds imply \(P_1^0\ge t\) for either range of \(y\). Bidder 1 therefore does not consume that item, including singleton-entry ties.

If bidder 2's bundle maximizes, its comparisons with the low singleton and empty require \(x\ge k\) and \(x+y\ge C\). For \(y>d\), \(P_1^0\ge x+q\ge t\). For \(y\le d\) and \(t\le a\), \(P_1^0\ge a\ge t\). Finally, for \(y\le d\) and \(a\le t\le A\),

\[
P_1^0\ge x+y-c\ge C-c\ge t.
\]

The last inequality follows exactly because \(C(t)-t-c\) decreases on \([a,A]\), and

\[
C(A)-A-c=150587/4000000>0.
\]

Thus every candidate bundle maximizer is also feasible, including every boundary and tie. Low-singleton and empty selections are automatically feasible because bidder 1 never consumes the low item. This proves the complete pointwise joint allocation claim; an almost-everywhere argument is unnecessary.

For each fixed opponent report the bidder 2 rule maximizes a fixed menu, giving DSIC and IR. Bidder 1's own allocation and payment remain V3, so its original pointwise incentive and participation inequalities remain true. On the complement of \(Q\), retaining the entire V4 free-fiber mechanism provides the complete feasible continuation. All predicates are closed or open polynomial inequalities, all menus are Borel, and the finite tie rules are explicit. Payments are nonnegative and bounded by the selected reported value.

The containing-rectangle assertion from the initial geometry note should **not** be extended past \(t=a\): for \(t>a\), bidder 1 may receive its item even at low opponent \(y\). The direct price bounds above establish compatibility without that false extension.

## 3. Saturation of the full randomized capacity certificate

For every \(d<t\le A\), \(0\le\rho\le b-t\), the exact top-edge occupation remains

\[
x_1^{V3}(x,1)=\mathbf1\{x<k\}.
\]

For \(x\le c\), the final price is \(d<t\). For \(x>c\), the opponent sum exceeds one, so inherited bundle fees are absent and the price is \(x+q\). At \(x=k\), zero-utility rejection selects empty. This remains true on \(t+\rho=b\), since bidder 1's bundle utility can only be nonpositive. The residual low-item capacity is one everywhere. Also, for \(x>A\), the direct bounds above give residual high-item capacity one for every \(y\).

The screening certificate uses

\[
\pi_1=3(x-A)_+\,dx\,dy+F(x)\,dx\,\delta_{y=1},\qquad
\pi_2=3(y-\ell(x))_+\mathbf1_{x\le A}\,dx\,dy,
\]

where \(\ell(x)=B\) for \(x\le k\), \(\ell(x)=C-x\) for \(k<x\le A\), and the nonnegative \(F\) is specified in the screening proof. Its exact gap against every randomized DSIC/IR competitor is

\[
\langle\pi,r\rangle-R
=\langle\pi,r-a\rangle+3\int_{D_0}u.
\]

The candidate has zero utility on \(D_0=\{x\le A,y\le\ell(x)\}\). It allocates the high item throughout \(x>A\), where the actual residual is one; it allocates the low item throughout \(x\le A,y>\ell(x)\), where the residual is always one. On the top edge its high-item allocation is zero below \(k\) and one above \(k\), matching the actual residual. The single point \(x=k\) has zero measure for \(F(x)\,dx\), while the preceding pointwise proof separately handles its tie. Both terms in the exact gap therefore vanish.

This applies the arbitrary-residual gap theorem directly. For \(t>a\), it does not invoke the narrower residual-class theorem requiring full interior capacity for every \(x>k\). That stronger hypothesis can fail, but it is unnecessary: pointwise candidate feasibility and saturation on the stated price supports suffice.

It follows that the entire closed \(Q\) has an explicitly attained, fully randomized inner optimum. This statement optimizes bidder 2 with bidder 1 fixed; it is not a global certificate for the outer bidder problem.

## 4. Exact revenue accounting, independently reconstructed

On \(t_1\le t\le A\), the candidate prices agree exactly with V3's quadratic joined branch. At \(t=t_1\), equality follows from

\[
K+r_1=(c+A)^2,\qquad 5/6+3r_1/4=c+A.
\]

Thus the positive-measure revenue changes relative to V4 occur only for \(d<t<t_1\), \(0\le\rho<b-t\), in both item orientations. Additional closed-boundary menus and tie changes have zero expected-revenue measure. The old V3 menu equals the base menu until \(t_0\), then its square-root branch until \(t_1\). Consequently the exact gain is

\[
2\int_d^{t_1}(b-t)\bigl[G(A,C(t)-k,C(t))-G(a,b-k,b)\bigr]dt
-\frac12G_{\mathrm{root}}^{V3}.
\]

The factor two is for the two item orientations of the **one** changed bidder. The preserved V3 square-root gain counted both bidders and both orientations, giving the factor one half in its subtraction. No retained tariff gain or already installed V4 free-fiber gain is removed a second time.

The independent replay rebuilds the integrand with dictionary-based rational polynomial operations and integrates at dyadic brackets of the algebraic endpoint. It obtains the old square-root contribution from V3's independent binomial expansion and rigorous remainder, without calling the new primary revenue routine or its logarithm enclosure. It independently reconstructs the V4 baseline from V3's independent total and the exact free-fiber gain. The resulting enclosure is

\[
\frac{875243586975954394119020}{10^{24}}
\le R_{V3.1}\le
\frac{875243586975954394119021}{10^{24}}.
\]

The region's exact area is verified in two ways:

\[
|Q|=A^2-(2A-b)^2/2
=|D|+2\int_d^A(b-t)dt
=63871/180000.
\]

The candidate's conditional constrained revenue is

\[
V_k=59/108+k^2/4-k^3+9k^4/16.
\]

Integrating its full inner value over the complete solved region, including SJA on \(D\), gives exactly

\[
R_2(Q)=
\frac{3270005919999123155413}{19440000000000000000000}
+\frac{246769}{13500000}\sqrt2.
\]

This is a regional inner value, not the auction's total revenue. The rational and radical coefficients were reconstructed independently and agree with the primary certificate.

## 5. Implementation audit and replay

The updated `constrained_candidate.py` was read in full. It checks membership in closed \(Q\), uses SJA for \(t\le d\), uses the certified menu for \(d<t\le A\), and retains the V4 continuation outside \(Q\). Bidder 1's row and payment are copied unchanged. Every price decision and maximizing comparison is exact for rational input reports.

`closed_region_audit.py` independently checks the algebraic compatibility margin and performs 462 targeted rational boundary replays in both orientations. These cover \(\max w=d\), \(w_1+w_2=b\), \(t=A\), singleton entry, bundle entry, the binding top-edge tie, and nearby occupied points. Three further profiles check exact outside continuation. The all-report proof is Sections 1–3; the finite replay checks that the implementation matches those named boundary cases.

`independent_revenue.py` independently replays the polynomial/binomial accounting, total revenue, closed-region area, and exact regional inner value. It explicitly suppresses `--write` while invoking the frozen V3 replay, so generating its new certificate cannot modify prior versions.

All these replays passed. The remaining unsolved problem is the full residual optimization outside \(Q\), followed by a compatible certificate for bidder 1's unrestricted outer optimization. No implication from conditional optimality to the unrestricted two-bidder optimum is made.
