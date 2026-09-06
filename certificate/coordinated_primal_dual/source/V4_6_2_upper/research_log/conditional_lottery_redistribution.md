# Alternative supports for the same full randomized lottery optimum

The V4.6 lottery support places a large price on the fixed report line
y=c. Most of that line price can be removed without changing the
conditional optimum or the universal inequality. The residual line
coefficient is exactly the first-order lottery price-cut coefficient,
which sharpens the diagnostic linking this local certificate to joint
reallocation. This support is not used in the new numerical upper bound.

Use the V4.6 notation A=2/3, q=113/500, c=137/500, A<t<T,
alpha=3t-2, delta, beta, L, Y, k, and the functions z(y), e(x), F(x),
f(x) and no-sale region D0 from `V4_6/research_log/inner_lottery_certificate.md`.
Put

\[
m=\alpha L/4,\qquad \lambda=\alpha c+m.
\]

For an arbitrary complete DSIC/IR utility u, set g(y)=u(1,y). The old
trace slack can be written without discarding its below-c monotonicity:

\[
\int\sigma_g g=\alpha\int_0^c g(y)dy+m g(c)-K_g,
\quad
K_g=\frac\beta2\int_0^L s(L-s)^2\,dg''(c+s)\ge0.                 \tag{1}
\]

This follows directly from the old exact hinge identity; it is not an
approximation to g. For every y<=c define the weighted IC slack

\[
M_y=\frac{t}{t-A}\int_A^t a_1(x,y)dx-\int_0^t a_1(x,y)dx\ge0.
\]

The inequality is the terminal-average inequality for the nondecreasing
selected own-coordinate allocation. Horizontal envelopes at each actual
report y give

\[
g(y)=u(0,y)+\int_0^1a_1(x,y)dx.
\]

The new support, before the optional top-edge transfer, is

\[
\begin{aligned}
\widetilde\pi_1={}&3(x-z(y))_+\,dxdy+F(x)dx\delta_1(dy)\\
&+\{3t1_{A<x<t}+\alpha1_{t<x<1}\}1_{0<y<c}\,dxdy\\
&+\{3tL/4\,1_{A<x<t}+m1_{t<x<1}\}\,dx\delta_c(dy),\\
\widetilde\pi_2={}&3(y-e(x))_+1_{x<A}\,dxdy.
\end{aligned}                                                    \tag{2}
\]

All terms are finite nonnegative Borel measures. The previous corner
price lambda has become a volume price of total anchor weight alpha*c
plus a smaller corner weight m. Every randomized competitor bounded by
an arbitrary Borel residual r satisfies the exact gap

\[
\begin{aligned}
\langle\widetilde\pi,r\rangle-R
={}&\langle\widetilde\pi,r-a\rangle+K_g
 +\alpha\int_0^c M_y dy+mM_c+S_u,\\
S_u={}&3\int_{D_0}u-\alpha\int_0^c u(0,y)dy-mu(0,c)\ge0.        \tag{3}
\end{aligned}
\]

For the last sign, D0 contains [0,k]x[0,B]. Coordinate monotonicity gives

\[
S_u\ge(3k-\alpha)\int_0^c u(0,y)dy
       +[3k(B-c)-m]u(0,c).
\]

Here 3k-alpha=2-3q>0. On the full parameter interval, k>=A-q,
B-c>=q, alpha<=2q, and L<=q, so

\[
3k(B-c)-m\ge q(2-7q/2)>0.
\]

Thus (3) is a universal capacity support covering the unrestricted
randomized conditional problem. It requires no positive sink at types
where the candidate has positive information rent.

At the displayed lottery menu, K_g=0, all M_y=0, and S_u=0. Therefore
(2) is tight whenever its priced capacity is saturated. Relative to the
old residual assumptions, its new requirement is occupation of the scarce
item throughout A<x<t, 0<y<c. On the reference V4.6 Eplus fibers this
holds: at such opposing reports the reverse Eplus menu offers the high
singleton at x; a bidder of high value t>x and low value rho<c strictly
prefers it to the lottery, bundle, or safe singleton. All price ties are
handled by the complete inherited priority rule. After the final corner
release this equality statement must be restricted to fibers whose
priced occupation remains, exactly as in the V4.6 coverage note.

The top-edge term can independently be moved to a volume band. For
Z>=5/6 and H(y)=(y-Z)_+/(1-Z), replace it by F(x)/(1-Z) on y>Z and
add f(x)H(y) to the second-item volume density. The exact horizontal and
vertical envelope identity proves equality of charges for every DSIC
allocation. For x<A and y>Z the combined safe density is
(1-H)3(y-e(x))+H(3y-2)>=0; for x>A it is H. This is a genuine alternative
measure, not smoothing error. It preserves candidate tightness whenever
the actual high-band allocation remains the inherited threshold x<k.

## A remaining common-price obstruction is smaller and explicit

On an unaltered Eplus fiber, the other bidder consumes the new corner
price on A<x<t, y=c. Its consumed mass is m*t, whereas the old line gave
lambda*t. For both physical item orientations, low opponent coordinate
rho in [0,c), and t in the stable interval [3/4,4/5], integrate these
masses with factor 2c. This t interval is disjoint from the final V4.6
corner-release band. The exact replay computes

\[
M_{\rm old}=2c\int_{3/4}^{4/5}\lambda(t)t\,dt,
\qquad M_{\rm new}=2c\int_{3/4}^{4/5}m(t)t\,dt,
\quad 0<M_{\rm new}<M_{\rm old}.                               \tag{4}
\]

The globally empty conditional menu on the opposing bidder's null report
faces removes this consumed price without changing expected revenue.
Therefore a common price containing (2) on those fibers, with only added
nonnegative measures, cannot support that bidder's current menu: its
charged-objective regret is at least M_new. This rejects that particular
positive completion architecture. It is not nonexistence of a common
support, and it is not a newly feasible revenue improvement.

The remaining coefficient m=alpha*L/4 coincides with the linear revenue
gain from lowering the lottery payment in the V4.6 exact calculation.
The part alpha*c removed into volume was trace-monotonicity slack rather
than that admissible outer-deformation signal. This identifies which
part of the original singular certificate still needs a joint incentive
transport or a change in the candidate. No uniqueness or necessity over
all possible supporting measures is asserted.

`verifier/conditional_lottery_redistribution.py` checks the polynomial
identities and explicit strict rational margins in (1)--(4). The continuum
convexity and envelope arguments above establish the theorem; this small
arithmetic replay is not a type-grid proof.
