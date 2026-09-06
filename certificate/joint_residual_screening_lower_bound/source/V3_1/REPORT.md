# V3.1: exact screening on a nonfree part of the actual residual

## Result

This trial closes a substantive portion of the remaining inner problem. With bidder 1 fixed to its complete V3 mechanism, bidder 2 is now optimized over the **full randomized pointwise DSIC/IR class** at every opponent report in the closed polygon

$$
Q=\{w\in[0,1]^2:\max(w_1,w_2)\le2/3,\quad w_1+w_2\le91/100\}.
$$

Its area is `63871/180000`, approximately **35.4839%** of the opponent-report square. This includes genuinely constrained fibers where bidder 1 sometimes receives an item; the result does not replace their residual by full capacity.

The improved complete auction has exact revenue

$$
R_{3.1}=R_{\mathrm{free},V4}+\Delta_{3.1},
$$

with a finite algebraic/logarithmic expression specified below and the independently certified enclosure

`0.875243586975954394119020 <= R_3.1 <= 0.875243586975954394119021`.

The strict improvement over the strongest exactly evaluated V4 mechanism exceeds `0.00002153805511902915`.

The decisive new result is the **matching unrestricted inner certificate**, not the size of this gain. It proves that arbitrary lotteries and arbitrary interior-capacity exploitation cannot improve the certified fibers. It does not establish outer bidder optimality or solve the inner problem on the complement of `Q`.

## 1. Actual capacity geometry and the complete mechanism

Use the frozen V3 constants

$$
a=159/250,\quad b=91/100,\quad s=1137/1000,\quad
c=b-a=137/500,\quad d=s-a=501/1000,\quad q=s-b=227/1000.
$$

Let `t=max(w1,w2)` and `rho=min(w1,w2)`. When `w in Q` and `t>d`, the high coordinate is unique: `rho<=b-t<d`. Align bidder 2's type `(x,y)` so that `x` is its value for bidder 1's high-coordinate item. Put `k=t-q`.

Every V3 singleton price is at least `d`, and every bundle price is at least `b`. Bidder 1 therefore never gets its low-coordinate item or the bundle on these fibers, including the boundary `t+rho=b`: zero-utility ties are rejected. It can receive only the high-coordinate item. Its actual residual satisfies

$$
r_1(x,1)=0\ \text{for }x<k,\qquad
r_1(x,1)=1\ \text{for }x\ge k,\qquad r_2(x,y)=1.
$$

This top-edge statement is exact, not an inference from volume samples. At opponent report `(x,1)`, bidder 1's final high-item price is `d` for `x<=c`, and `x+q` above `c`. Its own utility is strictly positive exactly for `x<k`. Interior tariffs can clip the cap hole, but cannot remove this binding top edge.

Define the full new auction as follows.

1. Compute the complete frozen V3 rows and retain bidder 1's allocation and payment everywhere.
2. Outside `Q`, keep bidder 2's complete V4 free-splice row. Since V4's changed free region lies inside `Q`, this continuation also equals V3 there.
3. On `Q` with `t<=d`, offer bidder 2 singleton prices `2/3` and bundle price `(4-sqrt(2))/3`. Choose the smallest mask among maximizers, empty first. These are wholly free fibers, including their closed boundaries.
4. On `Q` with `t>d`, offer prices

$$
A=2/3,\qquad C=5/6+3k^2/4,\qquad B=C-k,
$$

for the high-coordinate item, low-coordinate item, and bundle, respectively. The empty option costs zero. At a tie choose empty first, then the low-coordinate item, then the high-coordinate item, then the bundle. Charge the selected menu price.

These rules specify every real report, including axes, `t=d`, `t=2/3`, `t+rho=b`, algebraic price transitions, and all own-report ties. The switch at `t=d` is deliberate: the top capacity hole disappears there because bidder 1 rejects zero-utility allocation. No continuity assumption is made across that opponent report.

Every bidder-2 section is a complete menu on the whole continuous own-type square, so taxation proves DSIC/IR against every misreport. Bidder 1's row is unchanged. On the free region capacity is immediate. On the nonfree region every maximizing item-1 singleton has `x>=A>=t`; the base price bounds then make bidder 1 empty. A maximizing bundle has `x>=k` and `x+y>=C`. If `y>d`, its base price is at least `x+q>=t`. If `y<=d` and `t<=a`, it is at least `a>=t`. If `y<=d` and `t>=a`, it is at least `x+y-c>=C-c>=t`. The last inequality holds throughout `[a,2/3]`. Nonnegative V3 increments and zero-utility rejection retain these conclusions at ties. Thus item 1 is available whenever the new menu takes it; item 2 is always free.

Borel region predicates and finite maximizing selections give measurability. Payments are between zero and the reported allocated value, hence bounded by two. The joint mechanism is pointwise feasible and fully DSIC/IR.

## 2. The global inner certificate

For the aligned inner problem set

$$
\ell(x)=\begin{cases}B,&0\le x\le k,\\C-x,&k<x\le A,\end{cases}
$$

and partition the square into

$$
D_R=\{x>A\},\qquad
D_T=\{x\le A,\ y>\ell(x)\},\qquad
D_0=\{x\le A,\ y\le\ell(x)\}.
$$

Each has area `1/3`. These cancellation equations force `A=2/3` and `C=5/6+3k^2/4`.

Define

$$
f(x)=\begin{cases}
3B-2,&x\le k,\\
3C-3x-2,&k<x\le A,\\
1,&x>A,
\end{cases}
\qquad F(x)=\int_x^1f(s)ds.
$$

For `(2-sqrt(2))/3 <= k <= 2/3`, one has `F>=0` and `F(0)=F(1)=0`. The finite nonnegative capacity-price measures are

$$
\pi_1=3(x-A)_+\,dx\,dy+F(x)\,dx\,\delta_1(dy),
$$

$$
\pi_2=3(y-\ell(x))_+\mathbf1_{x\le A}\,dx\,dy.
$$

For **every** complete randomized DSIC/IR inner mechanism with utility `u`, allocation `a`, revenue `R`, and pointwise bound `a<=r`, the exact identity is

$$
\boxed{\ \langle\pi,r\rangle-R
=\langle\pi,r-a\rangle+3\int_{D_0}u\ \ge0.\ }
$$

To derive it, write uniform revenue as the two upper-edge utility integrals minus three times the interior utility integral. Integrate the horizontal envelope on `D_R` and the vertical envelope on `D_T`. The right-edge trace cancels. The remaining top-edge coefficient is `f`; integrating by parts gives the singular allocation term with weight `F`. IR supplies the only discarded utility term, on `D0`. This uses the incentive envelope **on the top edge itself**, not a volume-a.e. derivative substituted at exceptional reports.

At the new menu, utility vanishes on `D0`, and all positively priced available capacities are saturated. The item-1 volume price lies at `x>A`, the top-edge price sees exactly the actual zero/one cap separated by `k`, and item 2 is used on `DT`. Therefore

$$
V(r^*)=R_k=\langle\pi,r^*\rangle,
\qquad V(r)\le V(r^*)+\langle\pi,r-r^*\rangle
$$

for arbitrary competing Borel residuals, where `r*` is the actual V3 residual at this fixed opponent report. The price need not reproduce the detailed interior cap hole to prove equality.

The exact value is

$$
\boxed{R_k=\frac{59}{108}+\frac{k^2}{4}-k^3+\frac{9k^4}{16}.}
$$

Its information-rent derivative is `R_k'=-F(k)=-k(2-3B)`. Moving the binding top-edge exclusion boundary has exactly this opportunity cost. Freed capacity strictly inside the left strip has zero price and cannot improve the optimized revenue while that edge restriction remains.

At the free endpoint `k=(2-sqrt(2))/3`, the same identity certifies `A=B=2/3`, `C=(4-sqrt(2))/3`; the top-edge price below `k` is zero. Thus the certificate also handles the full-capacity portion of `Q`. It does not import a finite-menu classification or assume that a finite menu contains an optimizer.

## 3. Exact elimination on the closed region

The parameter and coordinate rotation are Borel in `w`. Integrating the preceding measures over `Q` yields a finite nonnegative measure `Pi_Q` on the full report space, retaining its own-report top edges. Define `V_Q(r)` as the supremum of bidder 2's revenue restricted to opponent reports in `Q`, over globally Borel complete inner mechanisms. Then

$$
V_Q(r)\le V_Q(r^*)+\langle\Pi_Q,r-r^*\rangle
$$

holds globally, and the explicit new mechanism attains equality at `r*=1-x1_V3`.

No unproved interchange of a pointwise supremum and integral is used: every fiber upper bound integrates, and the displayed jointly Borel mechanism attains it. The exact integrated value is

$$
\boxed{V_Q(r^*)=
\frac{3270005919999123155413}{19440000000000000000000}
+\frac{246769}{13500000}\sqrt2.}
$$

By gluing complete mechanisms across the opponent sets `Q` and its complement, the full inner value decomposes exactly as

$$
V(r^*)=V_Q(r^*)+V_{Q^c}(r^*).
$$

The first term is now solved. The second remains open. This regional support must not be described as a matching support for the entire four-dimensional residual objective.

## 4. Exact auction revenue and strict improvement

Only the region `d<t<t1`, `rho<b-t`, contributes a positive-measure change relative to V4; the root-to-quadratic junction is

$$
t_1=q+\sqrt{4c/3-2/9}.
$$

On later nonfree fibers through `t=2/3`, V3 already has the certified optimal menu. Closed-region boundary menus and positive ties are explicitly completed by the new rule; their revenue contribution is zero under the continuous prior.

For a fixed `k`, write `G(A,B,C)` for the exact four-option revenue formula in the screening proof. If `(A0,C0-k,C0)` is the preceding V3 menu, put `delta=2/3-A0` and `C*=5/6+3k^2/4`. Direct integration of `G_A=(C-A)(2-3A)` and optimization in `C` gives

$$
G(2/3,C^*-k,C^*)-G(A_0,C_0-k,C_0)
=(C_0-C^*)^2+\frac32(C_0-2/3)\delta^2+\delta^3.
$$

Every term is nonnegative on the replaced interval, and the sum is strictly positive before `t1`. This is an exact conditional comparison of complete menus; the full certificate, separately, excludes all other randomized screens.

Let `G_root_V3` denote V3's exact square-root-branch gain, including both bidders and both orientations. Set `k=t-q`, `C(t)=5/6+3k^2/4`. The new exact gain is

$$
\Delta_{3.1}=2\int_d^{t_1}(b-t)
\left[G(2/3,C(t)-k,C(t))-G(a,b-k,b)\right]dt
-\frac12G_{\mathrm{root},V3}.
$$

The factor two is the two item orientations for the one changed bidder. The integrand is an explicit rational polynomial of degree five; its coefficients are in `certificate/constrained_candidate.json`. The remaining root term is the preserved finite algebraic/logarithmic V3 expression. This specifies an exact number, not a decimal optimum or a numerical integration.

An independent computation uses dictionary polynomials, dyadic radical bounds and the inherited binomial remainder, without the primary logarithm evaluator. It verifies the new gain, its factor `1/2`, the old V4 endpoint, and the integrated `V_Q` expression. The primary and independent enclosures agree.

A strict escape from the old shared-base outcome occurs at `w=(.51,.01)`, bidder 2 report `(.30,.60)`: the base and V4 allocate nothing, while the new mechanism sells bidder 2 the bundle. These are nonfree opponent fibers: at reports just below `(k,1)`, bidder 1 still gets item 1. Capacity is built into the full replacement menu, rather than repaired after this allocation change.

## 5. Verification and remaining problem

The exact replays verify the actual cap geometry, dual polynomial identities and positivity, menu/measure revenue equality, the complete candidate, and an independent integrated revenue enclosure. The general measure and convex-analysis statements have separate analytic proofs and independent audits. An optional floating single-lottery polygon probe is retained as discovery history; its zero reported gain is not used as evidence of optimality and it is excluded from the exact replay runner.

The inherited unrestricted upper remains

`3715139591287203/4194304000000000`.

It is not matched by this mechanism. Two separate obligations remain: solve bidder 2 on `Q^c` for the relevant outer allocation, and prove bidder 1 globally optimal against the same full supporting prices. The exact inner result on `Q`, including its boundary conventions and arbitrary-lottery upper proof, is the completed V3.1 advance.
