# Independent continuous revenue audit of the refined capped mechanism

The full continuous calculation agrees exactly with the refined
candidate's reported revenue:

\[
0.876464164471798049944906113027<R<
0.876464164471798049944906113028.
\]

The exact gain over the corresponding clean capped mechanism is

\[
\frac{12679344561540434503009375151}
{1575000000000000000000000000000000}.
\]

This audit does not import or call `constant_kernel` or
`refined_candidate` as a revenue calculator. It reconstructs the full
base integral with Green boundary integration and integrates the final
conditional menus directly, including their plateau and cap cells. The
root investigator uses a different polynomial representation and simplex
moments. This is an independent revenue calculation; the separate
pointwise mechanism proof is still required for the auction lower-bound
claim.

## 1. Constants and relevant endpoints

\[
A=2/3,\quad c=157/500,\quad d=1/2,\quad q=93/500,
\]

\[
a=1025947/1500000=A+(1-2c)^2/8,
\quad b=1496947/1500000=a+c,\quad s=a+d.
\]

Write

\[
m=b-A=165649/500000,\quad u=3421/10000,
\quad \lambda=4/5,\quad G=\lambda(u-c)=281/12500.
\]

The fee is `g(x)=lambda(u-x)` on the closed interval [c,u], zero
elsewhere. Its threshold has a right jump G at c. The generalized
inverse is c for `d<t<=d+G`, then the inverse of
`h(k)=(1-lambda)k+q+lambda*u`, and becomes t-q after t=u+q.
The safe price in the constrained Q menu is capped at A:

\[
C=\max(C_0(k),t+\rho,k+h(\rho)),\quad
B=\min(A,C-k),\quad C_0(k)=5/6+3k^2/4.
\]

The endpoint for an active bundle-competition cost is

\[
\xi=\sqrt{4(b-5/6)/3}
=\sqrt{246947/1125000},\qquad c<m<u<\xi<A-q.
\]

## 2. Removing no region by assumption: the extra C bound

Let `B0(k)=C0(k)-k`, and put `ka=A-q`. Monotonicity gives
`k<=min(ka,b-rho-q)`. The B0 function is decreasing there.
For rho in [c,m], therefore,

\[
B_0(k)-h(\rho)\ge B_0(k_a)-h(m).
\]

For rho in [m,u], use `k<=b-rho-q`. The derivative of the sufficient
slack is

\[
\frac{d}{d\rho}[B_0(b-\rho-q)-h(\rho)]
=\lambda-\frac32(b-\rho-q)>0.
\]

Both sides consequently have their minimum at rho=m, and exact
arithmetic gives

\[
B_0(k_a)-h(m)=37/5000000>0.
\]

Outside the support, `t+rho>=k+h(rho)`. Thus
`C=max(C0(k),t+rho)` everywhere in Q for these exact parameters. The
safe-price cap does not change this C calculation. This check is
particularly relevant because the slack is small; its positivity is
proved exactly rather than inferred from floating samples.

## 3. Base revenue over every opponent report

On the ordered opponent triangle `0<=rho<=t<=1`, partition according to

\[
H=\max(0,t-a,t+\rho-b),
\]

then the two min boundaries `t=d`, `rho=d`, and both singleton-price-one
boundaries. On each affine cell use the actual three prices

\[
P_a=H+\min(a,s-\rho),\quad P_b=H+\min(a,s-t),
\quad P_c=H+b.
\]

When both singletons are affordable, integrate the proper-menu cubic

\[
\mathscr R(A,B,C)=A(1-A)(C-A)+B(1-B)(C-B)
+C[(1-C+B)(1-C+A)-(A+B-C)^2/2].
\]

When the high singleton exceeds one, put k=C-B and use

\[
B k(1-B)+C[(1-k)(1-B)+(1-k)^2/2].
\]

When both exceed one, only the bundle sells and its revenue is
`C(2-C)^2/2`. No polynomial is continued through an invalid
singleton topology. The nine positive-area rational polygon cells sum
exactly to ordered area 1/2. Green integration gives

\[
R_{\rm base}=\frac{33016262254015350834722212412993}
{37968750000000000000000000000000}.
\]

The factor four counts the two bidders and the two item orientations.

## 4. Exact Q cap formula from complete own-report cells

Put

\[
I(k)=59/108+k^2/4-k^3+9k^4/16.
\]

Before capping B at A, the complete menu revenue is
`I(k)-(C-C0(k))^2`. The cap is active only when
`H=C-k-A>0`, and only on the sum branch C=z. Direct integration of
the singleton-price derivative, or direct polygon areas, gives

\[
\mathscr R(A,A,z)-\mathscr R(A,z-k,z)
=\frac32 k H^2+\frac12 H^3.
\]

Integrating z from A+k to b yields exactly

\[
J(k)=\frac{k(m-k)^3}{2}+\frac{(m-k)^4}{8}
\quad(c\le k\le m),
\]

and zero when k>=m. This accounts for the whole cap region and every
own-type cell affected by the safe-price change.

For a fixed t, integrate the menu over all opponent low reports
`0<=rho<=b-t`. Since z=t+rho, the resulting conditional contribution
is

\[
(b-t)I(k)-\frac13[b-C_0(k)]_+^3+J(k)\mathbf1_{k<m}.
\]

The lower entry thresholds are positive throughout the relevant domain,
so no missing rho truncation is hidden in this formula.

## 5. Direct integration through the inverse plateau

The final constrained-Q integral, for one bidder in one ordered
orientation, is the sum of three explicitly integrated pieces.

On `d<t<=d+G`, k=c. Its contribution is

\[
P=I(c)[(b-d)G-G^2/2]-G[b-C_0(c)]^3/3+GJ(c).
\]

On the sloped inverse branch, substitute
`t=h(k)=(1-lambda)k+q+lambda*u`, with constant Jacobian
`1-lambda`. Its contribution is

\[
S=(1-\lambda)\int_c^u
[(b-h(k))I(k)-[b-C_0(k)]^3/3]dk
+(1-\lambda)\int_c^mJ(k)dk.
\]

On the unchanged part it is

\[
W=\int_u^{A-q}(b-k-q)I(k)dk
-\frac13\int_u^\xi[b-C_0(k)]^3dk.
\]

Consequently the full constrained-Q correction to the base is

\[
4\left[P+S+W-
\int_d^A(b-t)\mathscr R(a,s-t,b)dt\right].
\]

This calculation includes the whole t-interval mapped to the single
point k=c. It does not discard the plateau as a measure-zero set in k.
In particular its total cap contribution is

\[
4\left[GJ(c)+(1-\lambda)\int_c^mJ(k)dk\right].
\]

The corresponding clean capped mechanism has contribution
`4 integral_c^m J(k)dk`; the exact difference is stored separately.

The free Q contribution remains

\[
2L[R_F-\mathscr R(a,a,b)]
+2\int_{b_0}^b(1-z)[\mathscr R(A,A,z)-R_F]dz,
\]

where `L=1/4-(1-b)^2/2`, `b0=(4-sqrt2)/3`, and
`RF=4/9+2sqrt2/27`. The density at a fixed low-square sum z is 1-z.

## 6. The E correction needed when a>A

The final E menu has own-report revenue

\[
\mathscr R(t,d,t+c)+\delta(t)^2,
\quad\delta(t)=9(T-t)(U-t)/16,
\]

where `T=1-2c/3` and `U=5/3-2c`. However for
`A<t<a`, `rho<c`, the base menu is `(a,s-t,b)`, not
`(t,d,t+c)`. Therefore the complete E correction is

\[
4c\int_A^T\delta(t)^2dt
+4c\int_A^a[\mathscr R(t,d,t+c)-\mathscr R(a,s-t,b)]dt.
\]

The second term is negative for the frozen parameters. Omitting it
would overstate the revenue.

## 7. The additional base strip when a>A

For low reports r in [c,u], the ordinary bundle-pivot base domain has
`t from b-r to 1`. With safe and bundle fee g(r), its exact integrated
revenue change is

\[
4\int_c^u\left[g(r)\int_{b-r}^1\Gamma(t,r)dt
-g(r)^2(1-b+r)\right]dr,
\]

using the two correct singleton topologies for Gamma:

\[
\Gamma(t,r)=
\begin{cases}
1-2c+3(t-q)^2/2-3(t+r-c)^2/2,& t\le1+c-r,\\
3/2-2(t+r)+3(t-q)^2/2,& t\ge1+c-r.
\end{cases}
\]

There is also an outside-Q zero-pivot strip

\[
c\le r\le m,\qquad A<t<b-r.
\]

Its base prices are `(a,s-t,b)`, so the same safe-plus-bundle fee has
derivative

\[
\Gamma_Z(t)=1-2c+3(t-q)^2/2-3a^2/2.
\]

Its entire additional gain is

\[
4\int_c^m\left[g(r)\int_A^{b-r}\Gamma_Z(t)dt
-g(r)^2(m-r)\right]dr.
\]

This strip is absent when a=A. It has been integrated separately rather
than folded into a formula derived under a=A.

## 8. Final exact identity and audit scope

All terms above are rational polynomial integrals, except the free
endpoint b0 and the endpoint xi. Exact quadratic-field primitives give

\[
\begin{aligned}
R={}&\frac{35791404252341621852527735747861637}
{42525000000000000000000000000000000}
+\frac{31}{1215}\sqrt2\\
&-\frac{15059524650320123}{5537109375000000000}
\sqrt{\frac{246947}{1125000}}.
\end{aligned}
\]

The clean capped mechanism has exactly the same two radical coefficients.
Their difference is the rational gain displayed at the beginning, which
agrees with the root investigator's independently assembled formula.

In addition to the all-real integration, the replay clips complete
own-report menu cells directly at 45 rational parameter choices:
constrained-Q cap/no-cap cases, both E base regimes, and the base
singleton-price-one boundary. Every polygon revenue agrees exactly with
the corresponding formula. These bounded checks supplement the
continuous derivation; they do not replace it. The audit asserts revenue
of the explicitly given menus, not unrestricted optimality or a new
common upper certificate.
