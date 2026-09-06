# A joint exchange jump, an inverse plateau, and the exact revenue functional

The fixed-parameter analytic candidate constructed here has revenue

\[
0.876463378441815267238668800979<R_\star<
0.876463378441815267238668800980.
\]

Its gain over the strongest V4.6.1 construction is approximately
0.000007764605489415093. A simpler affine candidate is preserved with an
exact rational revenue increment and lies less than 0.000000000535 below
this analytic candidate. The calculations identify the optimizer of an
explicit sufficient exchange family. They do not identify the optimal
auction, certify global stationarity, or produce an unrestricted upper
bound.

The new structure is a jump in the exchange threshold and a whole
interval on which its generalized inverse is constant. It replaces an
arbitrarily steep artificial ramp. The closed jump face matters to
pointwise feasibility and is included explicitly below.

## 1. Fixed constants and the starting complete mechanism

Use the V4.6.1 clean three-region mechanism, before its small functional
tent, with

\[
a=A=2/3,\quad c=47/150,\quad b=A+c=49/50,
\quad d=1/2,\quad q=d-c=14/75,\quad s=7/6.
\]

Let Q be the closed opponent region
`max(w)<=A, sum(w)<=b`. Its free part has `t=max(w)<=d` and menu
`(A,A,max(b0,sum(w)))`, where `b0=(4-sqrt2)/3`. On the constrained part,
`d<t<=A`, use scarce value aligned with the opponent's high physical
coordinate and safe value aligned with its low coordinate.

The E lottery strip is `A<t<T, rho<c`, with
`T=178/225`, `U=26/25`, `rho=min(w)`. It retains the five-option menu
from the clean construction: empty, safe at `d+delta`, scarce at `t`,
bundle at `t+c+delta`, and allocation `(1,beta)` at `t+beta*c`, where
`delta=9(T-t)(U-t)/16` and `beta=(3t-2)/(3t-2+2delta)` in aligned
coordinates.

Every remaining opponent report uses the affine-base menu with
`H=max(0,w1-a,w2-a,sum(w)-b)`, singleton prices
`H+min(a,s-w_other)`, and bundle price `H+b`. Its two sides have a common
feasible maximizing allocation over all nine deterministic outcomes.

## 2. A sufficient family permitting threshold jumps

Put `V=69/200=.345`. Consider a nonnegative function g supported on the
closed interval [c,V]. Take g right-continuous, piecewise continuously
differentiable, with finitely many upward jumps in

\[
h(x)=x+q+g(x),
\]

and require h to be strictly increasing between jumps and nondecreasing
on its full domain. At the upper support edge require g to go to zero;
a positive right jump at c is allowed. Impose the explicit capacity
slack restriction

\[
0\le g(x)\le S(x),\qquad
S(x)=\frac{9761}{30000}-\frac{119}{100}x+\frac34x^2.
\]

The exhibited affine and analytic candidates have only the jump at c.
Define the generalized inverse, for t>d, by

\[
k(t)=\min\{x\in[0,1]:h(x)\ge t\}.
\]

Right continuity makes the minimum attained. Monotonicity gives the
pointwise implications

\[
x<k(t)\ \Longrightarrow\ h(x)<t,\qquad
x\ge k(t)\ \Longrightarrow\ h(x)\ge t.                 \tag{1}
\]

These implications, not an unjustified ordinary inverse identity at a
jump, are used in the feasibility proof. In particular k is constant
through an omitted interval in the range of h.

For a constrained-Q opponent w=(t,rho), offer the complete menu

\[
C=\max\{C_0(k),\ t+\rho,\ k+h(\rho)\},\quad
C_0(k)=5/6+3k^2/4,
\]

\[
\text{scarce singleton }A,\quad \text{safe singleton }C-k,
\quad\text{bundle }C,\quad\text{empty }0.                \tag{2}
\]

Keep free Q and every E menu unchanged. At a remaining base opponent
report, add g(rho) to the safe singleton and bundle prices, and leave
the scarce singleton price unchanged. This rule includes the face
`rho=c`, where the new g(c) is strictly positive. At any support
endpoint with g=0 the formula agrees with the base.

For every real report profile take each complete menu's maximizers,
force empty if maximum utility is zero, and choose the first jointly
feasible maximizing pair in the fixed orders. The orders are empty,
safe, scarce, bundle for constrained Q; the inherited physical orders
for free Q and the base; and empty, safe, scarce, bundle, lottery for E.
This finite joint rule handles all positive ties. The proof below shows
that at least one such pair exists at every profile.

## 3. The extra capacity maximum is redundant under S

The larger definition (2) makes compatibility transparent. The S bound
shows it creates no extra revenue region for these candidates.

Since h(x)>=x+q, its generalized inverse obeys k<=t-q, including its
plateau. For rho in [c,V], Q implies t<=b-rho and hence
`k<=b-rho-q`. The function `B0(k)=C0(k)-k` is decreasing on the relevant
range `c<=k<=A-q`. Thus

\[
B_0(k)\ge B_0(b-\rho-q)=\rho+q+S(\rho)\ge h(\rho).
\]

If rho lies outside the support, then h(rho)=rho+q and
`t+rho>=k+h(rho)`. Consequently throughout Q,

\[
C=\max\{C_0(k),t+\rho\}.                              \tag{3}
\]

Also `C0(k)-k>d`, and `C-k<=A`: the C0 branch satisfies this directly,
while the sum branch uses `b-k<=b-c=A`. Every used deterministic menu
has its proper discounted topology. No assertion about a missing
capacity cell is based on sampling.

## 4. Complete pointwise feasibility, including the jump face

The base fee raises the safe and bundle prices together by a
nonnegative amount. A maximizing subset of every old base choice still
exists. This uses the actual strict tariff discount
`Pscarce+Psafe-Pbundle>=q>0`, not a generic increasing-price assertion.
An old safe winner has scarce value `x<=Pbundle-Psafe<Pscarce`, so it
cannot switch to a positive scarce winner; its bundle comparison stays
unchanged. An old scarce or empty winner remains maximizing, and an old
bundle contains any new choice. The tariff inequality follows directly
from the three pivot cases, as in the detailed base argument of
[the refined structural proof](refined_structure_audit.md), Section 3;
the same argument applies here with a=A and c=47/150.
Therefore a base/base pair has a feasible maximizing pair, and
an E/base pair remains feasible by the old E/base argument and
containment.

In Q/Q pairs each positive choice is a bundle or safe singleton: all
own coordinates are at most A, and each safe price is above d. Same
high orientations prevent any positive safe purchase, since both low
values are below d. Opposite high orientations allocate different items
if both choose safe. A bundle/safe conflict is impossible: if one safe
purchase has high value y, then `y>B(w)>=h(rho)`; the conflicting
bundle requires `rho>=k(y)`, which by (1) gives `h(rho)>=y`. Two
positive bundles are excluded by `C>=sum(opponent)`. If a free Q row is
present, its Q buyer cannot buy a positive singleton, and the free
opponent's two values are at most d, so the other buyer cannot create a
positive safe conflict either. Equal-utility zero choices are empty.

For Q against a base row, the Q opponent w has sum at most b, so it
cannot buy a positive base bundle, and its low value is below d, so it
cannot buy the safe item. Only its scarce item can conflict. If the
other report v=(x,y) has y<=d, the base scarce price is at least A>=t.
If y>d and x is outside the support, it is at least x+q=h(x). If x is
inside the support and v is outside Q, x is its unique low coordinate
and y>d. The changed price of the contested item is therefore at least

\[
x+q+g(x)=h(x).
\]

A positive base purchase needs h(x)<t, whereas a Q purchase using that
scarce item needs x>=k(t). Relation (1) rules out the conflict. At x=k
with h(k)=t the opposing base utility is zero; if h(k)>t at a jump, it
is strictly negative. This is why the positive base fee on the exact
face x=c must be included. Omitting that null face would invalidate the
pointwise proof even though the expected-revenue integral would be
unchanged.

In E/Q pairs, the Q report cannot buy an E scarce singleton, bundle, or
lottery positively, since its coordinates are at most A and its sum at
most b<t+c. It can only buy E's safe item, with its high value y>d. The
opposing Q threshold k(y) is at least c, while the E own low value is
strictly below c. Thus the Q row cannot take the conflicting item, even
when k(y)=c on the new plateau. E/E is unchanged. The E face rho=c is
outside E and receives the base safe/bundle fee; its contested scarce
price on the old junction remains untouched.

These cases establish nonempty jointly feasible maximizing sets at all
real profiles and ties. For each fixed opponent, selecting an option
that maximizes one complete own-report menu proves DSIC against every
misreport. Empty gives pointwise IR in expected utility. The inverse of
a right-continuous monotone function, all algebraic or rational menu
functions, and the finite selection are Borel. Prices and allocations
are bounded, so revenue is integrable. The inherited per-item marginal
realization assigns at most one bidder each physical item on every
random draw. Thus allocation feasibility is samplewise, and DSIC is in
expected utility as required.

## 5. Deriving the whole-mechanism opportunity-cost functional

Write

\[
I(x)=59/108+x^2/4-x^3+9x^4/16.
\]

The proper-menu identity is

\[
G(A,C-k,C)=I(k)-[C-C_0(k)]^2.
\]

On the changed support, `C0(k)<b` and `C0(k)>h(k)`. These inequalities
are certified uniformly by `C0(V)<b` and
`C0(c)>V+q+S(c)`. Integrating all low opponent reports rho at fixed t
therefore gives the complete conditional contribution

\[
(b-t)I(k)-\frac13[b-C_0(k)]^3.                            \tag{4}
\]

The factor four later counts both bidders and both physical
orientations. Formula (4) integrates every own-report cell moved by
the incentive-compatible menu change.

For a continuous part of h substitute t=x+q+g(x) and dt=(1+g'(x))dx.
Let

\[
F(x)=(b-x-q)I(x)-[b-C_0(x)]^3/3.
\]

Expansion and integration by parts give

\[
\Delta_Q=4\int\left[-(b-x-q)I'(x)-\frac32x[b-C_0(x)]^2\right]g(x)dx
+2\int I'(x)g(x)^2dx,                                    \tag{5}
\]

provided the inverse plateaus at jumps are included. For example, at
the lower jump G=g(c), the omitted t interval is `(d,d+G]`, with
k=c. Its integral is exactly

\[
G F(c)-G^2 I(c)/2.
\]

This cancels the lower boundary terms `-G F(c)+G^2 I(c)/2` from
integration by parts. The same cancellation applies at an interior
upward jump, using its left and right values. There is no lost atom in
the change of variables.

The remaining base reports with low value x in the support have high
value t in [b-x,1] and prices `(t+x-c,x+q,t+x)`. Raising the safe and
bundle prices together by g(x) changes their complete menu revenue by

\[
\Gamma(t,x)g(x)-g(x)^2,
\]

where the high-singleton-price-one boundary is handled explicitly:

\[
\Gamma(t,x)=
\begin{cases}
1-2c+\frac32(t-q)^2-\frac32(t+x-c)^2,& t\le1+c-x,\\
\frac32-2(t+x)+\frac32(t-q)^2,&t\ge1+c-x.
\end{cases}
\]

Hence

\[
\Delta_B=4\int g(x)\int_{b-x}^1\Gamma(t,x)\,dt\,dx
-4\int(1-b+x)g(x)^2dx.                                  \tag{6}
\]

Combining (5) and (6), after integrating the rational polynomials in t,
gives the exact global identity

\[
\boxed{R(g)-R_{\rm clean}=\int_c^V
[\mathsf A(x)g(x)-\mathsf B(x)g(x)^2]dx.}                 \tag{7}
\]

The two coefficient polynomials are

\[
\begin{aligned}
\mathsf A(x)={}&\frac{315889}{1687500}+\frac{227}{3750}x
+\frac{69}{25}x^2-\frac{791}{50}x^3+9x^4-\frac{27}{8}x^5,\\
\mathsf B(x)={}&\frac{2}{25}+3x+6x^2-\frac92x^3.
\end{aligned}
\]

The linear term already includes the opposing bidder's entire menu
response and its information rents. Thus maximizing (7) is not
pointwise virtual-revenue maximization over report profiles.

## 6. Simple affine jump candidate with rational gain

Take

\[
g_{\rm aff}(x)=\frac34(43/125-x)\quad(c\le x\le43/125),
\]

and zero elsewhere. Its jump at c is exactly 23/1000. The generalized
inverse is c on

\[
1/2<t\le523/1000,
\]

then `4(t-q-129/500)` until `t=43/125+q`, and `t-q` thereafter.
The slope of h to the right of its jump is 1/4. Exact Bernstein
coefficients give

\[
\min_{[c,43/125]}(S-g_{\rm aff})\ge47/15000>0.
\]

Its exact improvement over the clean candidate is

\[
\boxed{\Delta R_{\rm aff}
=\frac{2982529415201233}{369140625000000000000}.}
\]

The clean revenue is the previously proved expression

\[
R_{\rm clean}=\frac{482935538268336599}{574087500000000000}
+\frac{31}{1215}\sqrt2-\frac{170368}{664453125}\sqrt{11}.
\]

Subtracting the old V4.6.1 tent gain
`68161978301/216000000000000000` gives a strict net improvement of about
0.000007764091690845. The exact rational difference is stored in
`functional_kernel.json`.

At `w=(.515,.1)`, `v=(c+.001,1)`, the old V4.6.1 mechanism splits the
items, giving item 1 to bidder 1 and item 2 to bidder 2. This new
mechanism gives the bundle to bidder 2. All inequalities at that profile
are strict except unneeded empty options, so the ownership transfer
persists on a positive-volume neighborhood. The replay also checks the
exact face v1=c, where the closed surcharge is essential.

## 7. The analytically forced optimizer inside this sufficient family

The exact sign certificates on [c,V] include

\[
\begin{aligned}
\mathsf B&\ge367659/250000>0,\\
-\mathsf A'&\ge19245947/10000000>0,\\
2\mathsf B S-\mathsf A&\ge221352943/22500000000>0,\\
2\mathsf B^2+\mathsf A'\mathsf B-\mathsf A\mathsf B'
&\ge63612871521763/56250000000000>0.
\end{aligned}
\]

S itself has positive Bernstein coefficients there. Also A(c)>0 and
A(V)<0. Thus there is a unique algebraic root

\[
\kappa\in(c,V),\qquad \mathsf A(\kappa)=0,
\quad\kappa\approx .3441659285920403.
\]

Pointwise completion of the square in (7) forces

\[
\boxed{g_\star(x)=\frac{\mathsf A(x)}{2\mathsf B(x)}
\text{ on }[c,\kappa],\quad g_\star(x)=0\text{ elsewhere}.}
\]

The positive slack certificate proves gstar<S on its support. The last
polynomial inequality proves

\[
\frac{d}{dx}(x+q+g_\star(x))>0.
\]

So neither monotonicity nor the sufficient capacity restriction cuts
this pointwise maximizer. It is an admissible right-continuous member
of the fully feasible family, with jump

\[
g_\star(c)=1508114993/66178620000.
\]

Its Q threshold is c for
`1/2<t<=34597424993/66178620000`. On its remaining changed interval,
k is the unique root in `(c,t-q)` of

\[
2\mathsf B(k)(k+q-t)+\mathsf A(k)=0.
\]

On the unchanged interval it is t-q. These rules completely specify
all reportwise allocations and payments through (2), including the
algebraic support endpoint, the plateau ends, and the closed jump face.

For every g in the stated sufficient class, (7) and pointwise completion
of the square show `R(g)<=R(gstar)`. This is an exact optimization of a
coordinate family justified by a complete feasibility proof. It does
not upper-bound mechanisms outside that family, and is not used as an
unrestricted auction certificate.

## 8. Exact analytic revenue and independently checkable evaluation

The stronger analytic candidate has the exact characterization

\[
\boxed{R_\star=R_{\rm clean}+
\int_c^\kappa\frac{\mathsf A(x)^2}{4\mathsf B(x)}dx.}
\]

This is an integral of an explicit rational function at a uniquely
specified algebraic endpoint, not a variational supremum or numerical
optimization output. It can equivalently be written using elementary
algebraic/logarithmic primitives. The supplied verifier evaluates this
exact expression with rational polynomial operations and a convergent
geometric series for 1/B. After affine normalization to [0,1], the
series ratio is bounded in absolute value by
`33505531/597930125<.06`; powers through index 28 (29 summands) leave an explicitly bounded integral
remainder smaller than 1e-39. The endpoint is enclosed by 140 exact
bisections of the strictly decreasing polynomial A. No floating
quadrature is used to certify the reported revenue.

`functional_star.py` also evaluates rational report profiles exactly.
For the nonrational inverse price parameter it stores the unique
simple root of the displayed degree-five polynomial. Polynomial gcds
detect equalities, using the uniqueness of that root in its isolating
interval; every nonzero sign is decided by rational interval
refinement. The replay includes rational report profiles whose inverse
is an exact rational root to exercise algebraic tie detection. The
all-real proof above supplies the mechanism's meaning beyond finite
regression reports.

The stronger candidate exceeds the affine candidate by approximately
0.000000000513798570350209. A separate complete-square bound, without
evaluating its rational integral, certifies this difference lies
between 0.00000000047417472577 and 0.00000000053477366276. Thus the
simple affine mechanism captures almost all of this family's gain,
while the exact optimizer identifies the remaining shape analytically.
