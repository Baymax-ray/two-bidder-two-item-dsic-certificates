# V4.02 — Independent audit of split-cost fee corrections and exact revenue

**The proposed revenue change passes this audit.** An independent rational enclosure calculation confirms a strictly positive gain for \(s_1=142/125=s_0-1/1000\). It uses no import of the primary revenue module and no evaluation of the primary logarithmic antiderivatives. The new mechanism's full feasibility and inner optimality have separate audits; this note verifies the revenue decomposition, surviving fee support, moment integrals, and moving-region subtractions.

The fixed parameters are

\[
a=159/250,\ b=91/100,\ s_0=1137/1000,\
c=b-a=137/500,\ d_0=s_0-a=501/1000,\ q_0=s_0-b=227/1000.
\]

## 1. Surviving fee support and branch stability

The frozen V3 `joined_threshold.menu` overwrites the 20 common Z/S rows and all 8 subsequent item rows: every such row lies inside its joined chamber. Its nonzero increments occur between

\[
t_0=q_0+\sqrt{r_0},\qquad
t_{\mathrm{cut}}=1058587/1362000,
\]

where \(r_0=b^2-K\), \(K=2/3+c^2\). The low-coordinate width is \(b-t\) below \(a\), and \(c\) above \(a\). The other surviving positive-area fee supports are the 41 bundle-fee polygons. The old first-match rule still determines shared boundaries; changing a boundary convention is unnecessary for this integral calculation, because these finitely many boundaries have zero opponent area.

On nonzero joined support, \(t>13/25=.520\) because \((.520-q_0)^2<r_0\), and \(\rho<.390\). On bundle support, writing \(\sigma=t+\rho\) and \(\eta=(\rho-c)/(\sigma-c-d_0)\), the row bounds give

\[
.91\le\sigma\le.98,\quad0\le\eta\le3/4,
\quad t\ge.53475,\quad\rho\le.42775.
\]

Consequently, for every \(|\theta|\le.001\), all nonzero fee support satisfies

\[
\rho<d_0+\theta<t.
\]

The pivot \(H\) is unchanged when only \(s\) varies. The base singleton price matching the opponent's low coordinate is therefore the only moving menu price: \(B\mapsto B+\theta\); \(A,C\) remain fixed. No moving fee-support boundary is omitted: the increments themselves are frozen functions of the opponents' original reports.

Every surviving increment vector in ordered singleton/bundle prices has form

\[
(\Delta A,\Delta B,\Delta C)=(\alpha,\beta,\beta),
\qquad 0\le\alpha\le\beta.
\]

For joined rows this follows directly from the displayed root, quadratic and affine prices; for bundle rows all three increments equal the common fee. Thus both bare and fee-adjusted menus have

\[
C-B=t-q_0.
\]

The proper-menu revenue polynomial used below does **not** require \(C<1\). Its relevant shape conditions are \(0<A,B<1\), \(\max(A,B)<C<A+B\). In the joined tail, \(C\) can exceed one while these conditions continue to hold. On the fee supports, the original discount is at least \(q_0\), the bare low price is at least \(d_0\), and the joined increment is at most its value at \(t=a\), less than \(1/20\). These yield uniform positive shape margins after \(|\theta|\le.001\). For the bundle polygons, the independent verifier checks all the requisite affine inequalities at polygon vertices and both parameter endpoints; convexity covers their interiors.

## 2. Exact cubic identity and its cancellation

For a proper four-option menu,

\[
G(A,B,C)=A(1-A)(C-A)+B(1-B)(C-B)
+C\left[(1-C+B)(1-C+A)-\frac{(A+B-C)^2}{2}\right].
\]

Differentiating in \(B\) gives

\[
G_B=(C-B)(2-3B),\quad
G_{BB}=6B-2-3C,\quad G_{BBB}=6.
\]

Hence the exact finite difference is

\[
G(A,B+\theta,C)-G(A,B,C)
=\theta(C-B)(2-3B)
+\theta^2(3B-1-3C/2)+\theta^3. \tag{1}
\]

Apply (1) to the fee menu \((A+\alpha,B+\beta,C+\beta)\) and subtract (1) for the bare menu. The cubic terms cancel; the first term uses the same \(C-B=t-q_0\). The resulting correction is exactly

\[
\boxed{\beta\left[-3(t-q_0)\theta+\frac32\theta^2\right].} \tag{2}
\]

In particular, changes of the high-singleton increment \(\alpha\) are irrelevant to this finite difference even though \(\alpha\) affects the baseline revenue. This is an algebraic cancellation, not a neglect of high-singleton purchase boundaries.

## 3. Moments and all multiplicative factors

Define, over the entire opponent square and over the fixed solved region \(Q\), respectively,

\[
M_j=\int \beta(t,\rho)(t-q_0)^j\,dw,
\qquad M_{j,Q}=\int_Q\beta(t,\rho)(t-q_0)^j\,dw,
\quad j=0,1.
\]

Each moment already includes both item orientations. There is no bidder factor inside it. For joined support, with \(t_1=q_0+\sqrt{r_1}\), \(r_1=4c/3-2/9\), the increment is

\[
\beta(t)=
\begin{cases}
\sqrt{K+(t-q_0)^2}-b,&t_0<t<t_1,\\
5/6+3(t-q_0)^2/4-b,&t_1<t<a,\\
5/6+3(t-q_0)^2/4-t-c,&a<t<2/3,\\
1/2-c+3q_0^2/4-3q_0t/2,&2/3<t<t_{\mathrm{cut}}.
\end{cases}
\]

The full-square width is \(b-t\) below \(a\) and \(c\) above. The \(Q\) width is \(b-t\) throughout, and its high coordinate stops at \(2/3\). Bundle-fee polygons have \(\sigma>b\) in their interiors, so they make no contribution to \(M_{j,Q}\). This explains every joined/full/Q integration range in the primary script.

For bundle row fee \(f\), the four mapped vertices are obtained from the row's \((\sigma,\eta)\) corners through

\[
\rho=c+\eta(\sigma-c-d_0),\qquad t=\sigma-\rho.
\]

If its polygon area is \(E\) and first \(t\)-moment is \(T_E\), its whole-square contributions are \(2fE\) and \(2f(T_E-q_0E)\). The independent verifier computes these via shoelace/centroid identities, independently of the primary Jacobian formula. Their exact totals are

\[
M_{0,\mathrm{bundle}}=\frac{368347}{3200000000},\qquad
M_{1,\mathrm{bundle}}=\frac{1179812659}{25600000000000}.
\]

Let \(F(s)\) be the one-bidder fee correction to the bare base, and \(F_Q(s)\) its restriction to \(Q\). The complete candidate has total revenue

\[
R(s)=2R_{\mathrm{base},1}(s)+2F(s)
+I_Q(s)-B_Q(s)-F_Q(s).
\]

The last three terms replace only bidder 2's old menu on \(Q\). Thus

\[
\boxed{\Delta R=2\Delta R_{\mathrm{base},1}-\Delta B_Q+\Delta I_Q
-3\theta(2M_1-M_{1,Q})
+\frac32\theta^2(2M_0-M_{0,Q}).} \tag{3}
\]

The factor 2 in the base derivative polynomial's geometric derivation is item symmetry; the additional leading factor 2 in (3) is bidder symmetry. They should not be merged with the orientation factor already in the moments.

## 4. Independent treatment of the radical and the moving Q strips

The primary radical antiderivatives are consistent with

\[
J_0=\tfrac12[k\sqrt{K+k^2}+K\log(k+\sqrt{K+k^2})],\quad
J_1=\tfrac13(K+k^2)^{3/2},
\]
\[
J_2=\tfrac18[k\sqrt{K+k^2}(2k^2+K)-K^2\log(k+\sqrt{K+k^2})].
\]

The independent computation instead writes

\[
\sqrt{K+k^2}=b\sqrt{1+z},\qquad z=(k^2-r_0)/b^2,
\quad0\le z<.07.
\]

On this range, even/odd binomial truncations of orders 26 and 27 bracket the square root. Their weighted polynomial integrals are evaluated exactly between inward dyadic endpoint brackets of precision 180 bits. The omitted endpoint stubs have nonnegative integrands bounded by two, giving an explicit upper error. No logarithm or primary interval routine is used. All eight unrounded independent moment enclosures lie inside the primary stored 30-digit intervals.

For \(\theta=-.001\), put \(d_1=s_1-a<d_0\). The independent calculation of \(\Delta B_Q\) uses the newly constrained strip \(d_1<t<d_0\), formerly a constant \((a,a,b)\) menu. If \(\mathcal D(B,C;\delta)\) denotes the right side of (1), then

\[
\begin{aligned}
\Delta B_Q={}&2\int_{d_1}^{d_0}(b-t)\mathcal D(a,b;d_1-t)\,dt\\
&+2\int_{d_0}^{a}(b-t)\mathcal D(s_0-t,b;\theta)\,dt\\
&+2\int_a^{2/3}(b-t)\mathcal D(d_0,t+c;\theta)\,dt.
\end{aligned}
\]

This agrees exactly with the primary subtraction of its two full-region values:

\[
\Delta B_Q=-\frac{1273728454067}{101250000000000000}.
\]

For \(V(k)=59/108+k^2/4-k^3+9k^4/16\) and \(R_{\rm SJA}=4/9+2\sqrt2/27\), the independent inner change is

\[
\Delta I_Q=2\int_{d_1}^{d_0}(b-t)[V(t-q_0-\theta)-R_{\rm SJA}]\,dt
+2\int_{d_0}^{2/3}(b-t)[V(t-q_0-\theta)-V(t-q_0)]\,dt.
\]

The exact pair is

\[
\Delta I_Q=\frac{479301333586681529}{6480000000000000000000}
-\frac{91}{1500000}\sqrt2,
\]

again agreeing with the primary result. These strip calculations explicitly include the change of the free-capacity region and do not freeze its moving boundary.

## 5. Result and verification boundary

Using the separately derived [base derivative](base_split_cost.md), its total base change is

\[
2\Delta R_{\mathrm{base},1}=-\frac{1401666113}{2000000000000000}.
\]

Combining it with the independently enclosed remaining terms in (3) gives

\[
\frac{1252797645849837077}{200000000000000000000000}
\le\Delta R\le
\frac{3131994114624592693}{500000000000000000000000},
\]

approximately \(0.000006263988229249185\), strictly positive. Adding the frozen V3.1 independently certified revenue interval gives

\[
0.875249850964183643304405
\le R(s_1)\le
0.875249850964183643304407.
\]

The [independent verifier](../verifier/independent_split_revenue.py) generated [its certificate](../certificate/independent_split_revenue.json) with `--write` and passed the read-only replay. It uses only standard-library exact arithmetic. The base derivative's geometric derivation and the prior V3.1 revenue certificate are explicit trusted inputs, rather than falsely claimed new independent derivations in this script. The new mechanism's complete DSIC/IR/capacity and inner certificate have their own [audit](split_cost_independent_audit.md). This calculation certifies the candidate's revenue improvement when combined with those mechanism proofs; it does not establish the optimal split cost, solve the residual problem outside \(Q\), or provide an unrestricted matching upper bound.
