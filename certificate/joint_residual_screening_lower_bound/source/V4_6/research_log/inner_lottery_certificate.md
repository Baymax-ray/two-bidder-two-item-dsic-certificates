# A full randomized inner certificate for the residual lottery

The five-option V4.5 menu solves its complete randomized inner problem on
the region E. This proof does not assume a finite allocation range for a
competitor. More generally, the same certificate applies to any actual
residual satisfying the two occupied-set conditions below, provided the
displayed candidate is feasible. This separates a remaining outer
allocation problem from directions already excluded by full inner
optimality.

## 1. Candidate and the precise residual hypotheses

Set

\[
A=2/3,\quad q=113/500,\quad c=137/500=1/2-q,
\quad T=(2+2q)/3,\quad A<t<T,
\]
\[
\alpha=3t-2,\quad
\delta=q+3q^2/4-3qt/2+\alpha^2/16,
\quad \beta={\alpha\over\alpha+2\delta},
\]
\[
B=1/2+\delta,\quad C=t+c+\delta,\quad k=t-q,
\quad L=\delta+\alpha/2,\quad Y=c+L,\quad j=1-t/2.
\]

The relations \(\beta L=\alpha/2\), \(C-Y=j\), and
\(B=C-k\) hold exactly. In the open interval,

\[
0<k<j<A<t<1,\qquad c<Y<B<2/3,\qquad 0<\beta<1.
\]

For completeness, delta factors as \(9(T-t)(U-t)/16\), where
\(U=(2+6q)/3>T\). It decreases from \(3q^2/4\) at A to zero
at T, so \(B\le1/2+3q^2/4<2/3\). Also
\(B-Y=q-\alpha/2>0\), \(j-k=1+q-3t/2>0\), and
\(L'=9t/8+3/4-3q/2>0\), with \(L(T)=q\).

Offer empty, safe singleton, scarce singleton, bundle, and lottery in
that priority order, with allocation/payment pairs

\[
(0,0;0),\quad(0,1;B),\quad(1,0;t),\quad
(1,1;C),\quad(1,\beta;t+\beta c).
\]

Choose the first utility maximizer at every report. The utility is

\[
u^*(x,y)=\max\{0,y-B,x-t,x+y-C,x+\beta(y-c)-t\}.
\]

This is a complete pointwise DSIC/IR Borel menu with bounded payments.
Its allocation is feasible against a specified residual \(r^*\) whenever
that is separately proved for every report and tie. The inner theorem
requires only that feasibility and

\[
r^*_1(x,1)=0\quad(0\le x<k),                 \tag{H1}
\]
\[
r^*_1(x,c)=0\quad(A<x<t).                    \tag{H2}
\]

No other description of the capacity hole is required. In particular,
the second-item residual need not be one everywhere: feasibility of the
candidate suffices wherever the certificate charges that item.

## 2. Partition determined by the actual lottery geometry

Let

\[
z(y)=\begin{cases}
t,&0\le y<c,\\
t-\beta(y-c),&c\le y<Y,\\
A,&Y\le y\le1,
\end{cases}
\qquad G=\{x>z(y)\}.
\]

Define

\[
e(x)=\begin{cases}
B,&0\le x<k,\\
C-x,&k\le x<j,\\
Y,&j\le x\le A,
\end{cases}
\qquad H=\{x<A,\ y>e(x)\}.
\]

Up to sets of volume zero, G and H are disjoint and their union is the
candidate's positive-utility set. Put \(D_0=[0,1]^2\setminus(G\cup H)\).
Thus \(u^*=0\) on \(D_0\). On G the candidate's scarce allocation is
one; on H its safe allocation is one. The genuine lottery cell is
entirely in G and disjoint from H. The change of integration boundary
from j to A above Y is an assignment of the bundle region to incentive
envelopes; it does not modify the primal allocation.

## 3. Exact envelope identity for arbitrary randomized competitors

Let u be any complete DSIC/IR utility with selected allocation a in
\([0,1]^2\), without any finite-menu assumption. Its coordinate traces
\(g(y)=u(1,y)\), \(h(x)=u(x,1)\) are convex, nondecreasing and
1-Lipschitz. Uniform revenue satisfies

\[
R=\int_0^1g(y)dy+\int_0^1h(x)dx-3\int_{[0,1]^2}u.
\]

Apply the exact horizontal envelope on G and the exact vertical envelope
on H. This gives

\[
R=\langle\pi^{\rm vol},a\rangle+
\int\sigma_g g+\int f h-3\int_{D_0}u,            \tag{1}
\]

where the nonnegative volume densities are

\[
\pi^{\rm vol}_1=3(x-z(y))_+,\qquad
\pi^{\rm vol}_2=3(y-e(x))_+1_{x<A},
\]

and

\[
\sigma_g(y)=\begin{cases}
\alpha,&y<c,\\
\alpha-3\beta(y-c),&c<y<Y,\\
0,&y>Y,
\end{cases}
\]
\[
f(x)=\begin{cases}
3B-2,&x<k,\\
3C-3x-2,&k<x<j,\\
3Y-2,&j<x<A,\\
1,&x>A.
\end{cases}
\]

The stationarity formula for delta is now used as a polynomial identity:
\(\int_0^1f=0\). Also \(f\le0\) below A. Therefore

\[
F(x)=-\int_0^x f(s)ds=\int_x^1 f(s)ds\ge0,
\qquad \int f h=\int F(x)a_1(x,1)dx.             \tag{2}
\]

This is an identity for the competitor's actual top-report allocation;
the top boundary has not been discarded as a null event.

## 4. A convexity transport across the entire lottery interval

Put \(\lambda=\alpha(c+L/4)=\int\sigma_g\). Let nu be the
nonnegative second-derivative measure of the convex trace g on (c,Y).
The zero-moment identity

\[
\int_0^L z(\alpha-3\beta z)dz=0
\]

and integration of the convex hinge representation give the exact slack

\[
\begin{aligned}
T_g&=\lambda g(c)-\int\sigma_g g\\
&=\alpha\int_0^c[g(c)-g(y)]dy
 +{\beta\over2}\int_0^L s(L-s)^2\,d\nu(c+s)\ge0. \tag{3}
\end{aligned}
\]

Indeed the hinge coefficient is
\(\int_s^L(\alpha-3\beta z)(z-s)dz=-\beta s(L-s)^2/2\).
This excludes arbitrary nonlinear convex trace changes and additional
lotteries, including allocations whose scarce probability is below one.
It does not require the candidate's menu to contain an optimizer in
advance. The candidate attains equality: its trace is constant below c
and affine throughout (c,Y).

## 5. A singular capacity price at the binding corner

The horizontal envelope at y=c gives

\[
g(c)=u(0,c)+\int_0^1a_1(x,c)dx.
\]

Pointwise DSIC makes \(a_1(x,c)\) nondecreasing in x, including its
selected values at exceptional reports. Consequently

\[
M_a={t\over t-A}\int_A^t a_1(x,c)dx-
       \int_0^t a_1(x,c)dx\ge0.                         \tag{4}
\]

The proof is the elementary fact that the average of a nondecreasing
function on its terminal interval is at least its average on the whole
interval. All integrals here are one-dimensional integrals of actual
allocations on the singular report line.

Define the nonnegative line density

\[
w(x)=\begin{cases}
0,&x<A,\\
3t(c+L/4),&A<x<t,\\
\lambda,&t<x<1.
\end{cases}
\]

The apparent factor \(1/(t-A)\) in (4) disappears from the price,
because \(\lambda=3(t-A)(c+L/4)\). Thus the measure stays bounded
uniformly as t tends to A.

The no-sale region contains \(K=[0,k]\times[c,B]\). Coordinate
monotonicity and IR give

\[
S_u=3\int_{D_0}u-\lambda u(0,c)\ge0.             \tag{5}
\]

For a uniform strict bound, \(L\le q\), \(k\ge A-q\), and
\(B-c\ge q\), so

\[
3|K|-\lambda\ge
3(A-q)q-2q(c+q/4)=q(1-3q/2)>0.
\]

The sink is supported only through this nonnegative expression on the
no-sale region. There is no requirement of positive sink flow at every
type.

## 6. The global capacity support and exact gap

The complete finite nonnegative Borel capacity-price measure is

\[
\boxed{\begin{aligned}
\pi_1&=3(x-z(y))_+\,dxdy+F(x)\,dx\delta_1(dy)
                         +w(x)\,dx\delta_c(dy),\\
\pi_2&=3(y-e(x))_+1_{x<A}\,dxdy.
\end{aligned}}                                                   \tag{6}
\]

Combining (1)--(5) gives, for every arbitrary Borel residual r and every
complete randomized DSIC/IR mechanism a bounded by r,

\[
\boxed{\langle\pi,r\rangle-R
=\langle\pi,r-a\rangle+T_g+\lambda M_a+S_u\ge0.}  \tag{7}
\]

This is an exact identity with individually nonnegative slacks, followed
by a global inequality. The report-line components retain exceptional
reports. The safe-item measure is identically zero on the genuine lottery
cell, as capacity complementary slackness requires.

At the displayed candidate, \(T_g=M_a=S_u=0\). On volume supports
it uses the priced marginal with probability one. On the top line its
scarce allocation is zero below k and one above k; (H1) and feasibility
give saturation. On the line y=c it is zero below t and one above t;
(H2) and feasibility give saturation. Individual endpoints of these
one-dimensional integrals have zero measure; the stated tie rules still
define a pointwise feasible mechanism there.

Therefore, whenever the candidate is feasible and (H1)--(H2) hold,

\[
\mathcal V(r^*)=R(u^*)=\langle\pi,r^*\rangle,
\qquad
\mathcal V(r)\le\mathcal V(r^*)+\langle\pi,r-r^*\rangle
\]

for every Borel residual r. This is full randomized conditional
optimality, not stationarity in the five-option family.

Its exact conditional value has a particularly short expression:

\[
\boxed{V^*(t)=
ct(1-t)+{t-q\over4}
+(t+c)\{(3/2-c-t)(1-c)-q^2/2\}+\delta(t)^2.}       \tag{8}
\]

The first three terms are the base four-option revenue at prices
\((t,1/2,t+c)\); the optimized bundle adjustment and lottery together
add exactly delta squared. This is a rational polynomial in t and does
not depend on the opponent's lower value once the theorem's residual
hypotheses hold.

## 7. Actual residuals and changes elsewhere

For the V4.5 region \(E=\{A<t<T,t+\rho\le91/100\}\), candidate
feasibility was proved in the frozen `V4_5/research_log/residual_lottery_extension.md`.
At own reports (x,1), the other bidder's scarce singleton price is 1/2
for x<=c and x+q for x>c. It cannot buy its low item or a bundle, and
zero-utility rejection gives (H1).

At own reports (x,c) with A<x<t, the inherited scarce-item surcharge is
zero and the other bidder's scarce-item price is exactly x. It buys
with strict utility t-x. The sum x+c exceeds 91/100, so the reverse E
splice does not alter that row. This proves (H2) on the whole interval,
not just at a rational witness.

The same theorem applies to enlarged opponent regions or to subsequent
joint reallocations once their complete feasibility and the two occupied
sets are verified. A residual decrease on a set where every candidate
allocation is zero automatically preserves tightness: feasibility gives
\(R(u^*)\le\mathcal V(r_{new})\), and monotonicity plus the old bound
gives the reverse inequality. More generally, the measure proof needs
only saturation on (6), not preservation of unpriced capacity.

These singular local prices need not support the other bidder's full
conditional optimization. In particular the line y=c is an
opponent-null set for the other bidder when the local measures are
assembled. Common-support compatibility is a separate obligation; (7)
does not claim an unrestricted upper certificate for the original auction.

## 8. Replay boundary

`verifier/inner_lottery_certificate.py` checks the polynomial equal-area
identity, ordering and uniform positivity identities, independently
integrates finite-menu examples by exact rational polygon clipping, and
checks the exact gap decomposition including the singular lines. Examples
include first-item probabilities below one and both-interior lotteries.
It also checks actual residual values at named boundary cases. These are
replay checks supporting the written continuum proof, not a type-grid
approximation or a formal proof-assistant kernel. The default replay is
read-only; `--write` regenerates only its V4.6 certificate.

## 9. An exact joint-deformation signal

The certificate does not forbid releasing the priced capacity. Keep
t, delta and beta fixed, and lower only the lottery's payment by epsilon.
Its entire new purchase interval is

\[
y_- =c-\epsilon/\beta,
\qquad y_+=Y+\epsilon/(1-\beta),
\qquad x>t+\beta c-\epsilon-\beta y.
\]

Assume \(0<y_-<c<Y<y_+<B\) and that the purchase boundary
stays in the type square. Write \(p'=t+\beta c-\epsilon\) and
\(H=c+\delta\). Relative to the underlying four deterministic
options, exact lottery revenue less displaced revenue is

\[
p'\{(1-p')(y_+-y_-)+\tfrac\beta2(y_+^2-y_-^2)\}
-t(1-t)(H-y_-)
-C\{(1-C)(y_+-H)+\tfrac12(y_+^2-H^2)\}.
\]

Subtract its value at epsilon zero. Using \(\beta L=\alpha/2\)
gives the complete conditional gain

\[
\boxed{\Delta R(\epsilon)=
{\alpha L\over4}\epsilon
-{\alpha\over4\beta(1-\beta)}\epsilon^2
-{1\over2\beta(1-\beta)^2}\epsilon^3.}             \tag{9}
\]

The positive first derivative is \(\alpha L/4\), not lambda.
The missing \(\alpha c\) is exactly a first-order trace-convexity
slack: the value g(c) rises while most of the trace below c does not.
This change violates the original residual at the binding corner; it
is **not** by itself an admissible inner improvement. A complete joint
mechanism must release the conflicting capacity via the other bidder's
entire conditional menu, then account for that bidder's full revenue
change. If such a joint release is accepted, (7) remains a global upper
support but its old equality claim need not remain true on the altered
fibers. The separate joint-deformation construction must establish its
own pointwise feasibility and its own claim boundary.

