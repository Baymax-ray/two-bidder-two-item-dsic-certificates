# A reusable conditional support gives a strictly better global upper bound

The conditional support is useful away from the capacity at which it was
discovered. This note converts that fact into a common capacity measure
whose charged screening problems are solved over the full randomized DSIC
class. It proves, independently of the new flow-integration improvement,

\[
\boxed{\mathrm{OPT}\le 884312786578/10^{12}=0.884312786578.}
\]

The exact unrounded value and a decreasing sequence of seven certified
bounds are in `certificate/conditional_global_splice.json`. This is an
upper bound for the original continuous problem, not optimality of a
finite type grid. No lower-bound mechanism is changed by this branch.

## 1. A general whole-auction use of an inner support

Let \(\kappa_w\) be a measurable kernel of finite nonnegative capacity
measures such that every complete randomized DSIC/IR conditional mechanism
of bidder 2 satisfies

\[
R_2(w)\le c(w)+\langle\kappa_w,a_2(\cdot,w)\rangle.
\]

There is no requirement that the actual residual equal the residual used
to discover this inequality. Integrating the kernel gives \(\kappa\) and
\(C=\int c\). For every jointly feasible mechanism,

\[
R_1+R_2\le C+\langle\kappa,1\rangle+H_1(\kappa),
\qquad H_1(\kappa)=\sup_{M_1\ \mathrm{DSIC/IR}}
 [R_1-\langle\kappa,a_1\rangle].                 \tag{1}
\]

This follows by substitution and capacity; there is no interchange of an
uncountable supremum and an integral. If a charged-screening upper
certificate supplies

\[
R_1\le\langle\phi_1,a_1\rangle-I_1,
\qquad I_1\ge0,
\]

then, for a common dominating finite measure, Jordan positive parts give

\[
H_1(\kappa)\le\langle(\phi_1-\kappa)_+,1\rangle. \tag{2}
\]

The resulting gap consists exactly of the conditional-screening slack,
priced capacity slack, virtual-allocation slack in (2), and the weighted
IC/IR slack \(I_1\). The allocation relaxation in (2) is used only for an
upper bound; no assertion that its pointwise maximizer is implementable is
needed. Signed or singular field versions use Radon--Nikodym derivatives
with respect to a common dominating measure. All allocations on singular
report sets remain the actual pointwise selections.

## 2. The full-capacity conditional support used here

Set

\[
A=2/3,\quad b_0=(4-\sqrt2)/3,\quad k=b_0-A,
\quad Z=3/4.
\]

The full-capacity single-buyer menu is empty, singleton 1, singleton 2,
bundle at prices \(0,A,A,b_0\), with empty-first fixed tie priority.
Its complete utility is

\[
u^*(x,y)=\max(0,x-A,y-A,x+y-b_0),
\qquad R_0=4/9+2\sqrt2/27.
\]

Define \(\ell(x)=A\) below k and \(\ell(x)=b_0-x\) on
\((k,A)\), and set \(D_0=\{x<A,y<\ell(x)\}\). Also put

\[
f(x)=\begin{cases}3\ell(x)-2,&x<A,\\1,&x>A,\end{cases}
\quad F(x)=\int_x^1 f(s)ds,\quad
H(y)=4(y-3/4)_+.
\]

The following bounded nonnegative densities are the existing exact band
transfer of the full-capacity SJA support:

\[
\begin{aligned}
\Psi_1(x,y)&=3(x-A)_++4F(x)1_{y>Z},\\
\Psi_2(x,y)&=3(y-\ell(x))_+1_{x<A}+f(x)H(y).
\end{aligned}                                                   \tag{3}
\]

For x>A the first term in \(\Psi_2\) is interpreted as zero. Values on
integration boundaries may be chosen Borel arbitrarily; the primal menu
retains its explicit pointwise ties.

The old exact envelope and edge-transfer proof gives, for **every**
complete randomized DSIC/IR utility u and selected allocation a,

\[
\langle\Psi,a\rangle-R=3\int_{D_0}u\ge0.        \tag{4}
\]

In particular (3) is a universal residual support, not a support limited
to full capacity. The old derivation is in
`V4_5/research_log/dual_capacity_support.md`, with the full-capacity
specialization in the V4.6 diagonal certificate at m=0. The transfer to
Z=3/4 remains exact: above Z, \(y\ge A\), so the second density is the
nonnegative combination
\((1-H)3(y-\ell)+H(3y-2)\) below A; above A it is H.
The candidate saturates all positive prices and vanishes on D0. Thus
\(\int(\Psi_1+\Psi_2)=R_0\).

## 3. Exact sign region for the opposing charged screening problem

Write \(v_1=w\), \(v_2=v\), and

\[
W=[0,h]^2,\qquad h=43/100.
\]

The inherited stream field of bidder i is \(\phi_i\), with the exact
32 rational coefficients frozen in the old two-level nonuniform archive.
For each fixed opponent, its revenue envelope is

\[
R_i=\int\phi_i\cdot a_i-u_i(0).                 \tag{5}
\]

For clarity, the radial base is
\(\phi^{\rm base}_j(v)=v_j(3/2-1/(2\max(v)^2))\).
The added field is the curl of a polynomial stream vanishing on the four
edges. Radial integration gives the zero-type utility term in (5); the
curl contributes zero after integration against the gradient of a convex
utility. The value at v=0 is immaterial to the volume integral. The
singularity is integrable, and (5) applies to the bounded selected
subgradients of arbitrary convex DSIC utility, including nonlinear
utilities and infinitely many allocation values.

The separate exact replay `flow_sign.py --cap 43/100 --output flow_sign_43_certificate.json` and
`flow_sign_43_certificate.json` certify

\[
\phi_{ij}(v_i,v_{-i})\le0
\quad\text{whenever }v_i\in W,\quad j=1,2,       \tag{6}
\]

for every opposing report. The proof multiplies out the positive radial
denominator and proves the two chart polynomials negative by exact
Bernstein subdivision; item symmetry supplies the other item.

The support (3) is identically zero on its own-report square W. Indeed
h<A and h<Z; also \(b_0>2h=43/50\), so for x<=h the safe threshold is
\(\ell(x)\ge b_0-h>h\). This proves that the two regional replacements
below have zero interaction on \(W\times W\).

## 4. An explicit common price with both unrestricted H problems solved

Let \(\Lambda_j=\max(0,\phi_{1j},\phi_{2j})\). Define the following
absolutely continuous common capacity price on the full report space:

\[
\Pi_j(w,v)=
\begin{cases}
0,&w\in W,\ v\in W,\\
\Psi_j(v),&w\in W,\ v\notin W,\\
\Psi_j(w),&v\in W,\ w\notin W,\\
\Lambda_j(w,v),&w\notin W,\ v\notin W.
\end{cases}                                                     \tag{7}
\]

This measure uses the fixed physical orientation in (3) for both bidders.
It need not be item symmetric pointwise. Its integrated value and the
subtractions used below are item symmetric because W and the old field
are symmetric.

When bidder i's opponent is in W, inequality (4) bounds its full
conditional revenue by its \(\Pi\)-charge. When its opponent is not in
W, (5), (6), and (7) give the same result. In the latter case a bidder
whose own report is in W has nonpositive virtual value, while the price
is nonnegative. Consequently

\[
R_i(M_i)-\langle\Pi,a_i\rangle\le0
\quad\text{for every unrestricted }M_i.
\]

The globally empty mechanism attains zero. Therefore the charged
screening problems are solved exactly:

\[
\boxed{H_1(\Pi)=H_2(\Pi)=0},\qquad
\boxed{\mathrm{OPT}\le\int\sum_j\Pi_j}.        \tag{8}
\]

This is a genuine common-capacity global certificate. It does not match
the revenue of the V4.6 mechanism, and its equality conditions do not
claim to identify the optimal auction.

## 5. Four nonnegative components of the remaining gap

For any complete feasible auction, let \(O_i\) mean that bidder i's
opponent belongs to W. The exact gap for the actual measure (7) is

\[
\begin{aligned}
\int\Pi-R_1-R_2
={}&\underbrace{\sum_i3\int_{O_i}\int_{D_0}u_i}_{\text{conditional screening}}\\
&+\underbrace{\sum_j\int\Pi_j(1-a_{1j}-a_{2j})}_{\text{capacity}}\\
&+\underbrace{\sum_{i,j}\int_{O_i^c}(\Pi_j-\phi_{ij})a_{ij}}
 _{\text{virtual allocation}}\\
&+\underbrace{\sum_i\int_{O_i^c}u_i(0,v_{-i})}
 _{\text{weighted IC/IR source slack}}.           \tag{9}
\end{aligned}
\]

Every summand is nonnegative. This construction uses exact IC envelope
identities; its weights on strict, separated-report IC inequalities are
zero. The last line is specifically the positive IR slack at the zero
type, not a claim that every type has a positive sink. A sparse
long-range IC-flow extension contributes its actual weighted IC residuals
to that line. There is no pointwise sink on the positive-rent region.

The conservative decimal bounds also contain the old certified
integration remainder and the unused part of the nonnegative virtual
slack in the next section. These are numerical majorization slack, not
incentive or capacity slack of (7).

## 6. Exact subtraction from an already certified integral upper bound

Let \(I=\int\sum_j\Lambda_j\) be the old continuous stream objective,
and let U be any certified upper bound for I using precisely the same
stream coefficients. By (6), on \(w\in W\), \(\Lambda_j=(\phi_{2j})_+\).
For every w, equation (5) evaluated at the SJA menu gives
\(\int\phi_2\cdot a^*=R_0\). Hence

\[
I-\int\Pi
=2\int_{w\in W}\int_v
 \sum_j\{(\phi_{2j}(v,w))_+-a_j^*(v)\phi_{2j}(v,w)\}.             \tag{10}
\]

The factor two is for bidder exchange. On the overlap both the old
objective and both new supports are zero, so nothing is subtracted twice.
The integrand in braces is nonnegative even before averaging over w.

For exact lower bounds on (10), integrate the polynomial dependence on
w over W first. Use one own-type radial chart \(v=(s,s\tau)\), whose
Jacobian is s; the other chart has exactly equal integrated slack.
Let \(P_j(s,\tau)=\int_W s\phi_{2j}(s,s\tau,w)dw\). Both P_j are
rational polynomials: the radial pole cancels against the Jacobian.

On any rational rectangle B wholly within one SJA allocation region,
let \(a^*(B)\in\{(0,0),(1,0),(1,1)\}\) be the chart allocation and
\(J_j(B)=\int_B P_j\). Then

\[
\int_{W\times B}s\sum_j[(\phi_{2j})_+-a_j^*\phi_{2j}]
\ge\sum_j[\max(0,J_j(B))-a_j^*(B)J_j(B)].         \tag{11}
\]

A rectangle is certified as no sale only if its maximum s is at most A
and its maximum sum is at most a lower bound on b0. It is a high-singleton
rectangle only if its minimum s is at least A and its maximum low value
is at most a lower bound on k. It is a bundle rectangle only if **both**
its minimum sum is at least an upper bound on b0 **and** its minimum low
value is at least an upper bound on k. A high type with a low coordinate
below k can prefer the singleton even when its sum exceeds b0. Rectangles
crossing that low-coordinate threshold are omitted. The independent
corner-menu checks include this explicit regression.

All terms on the right are nonnegative rational numbers. Dyadic
subdivision increases their sum by convexity of the positive part.
Previously included cells stay included; newly certified cells only add
nonnegative terms. Cells crossing a menu boundary are omitted, with
\(\sqrt2\) enclosed by integer square-root arithmetic, not rounded to a
floating allocation boundary.

The replay uses n=16,32,64,128,256,512,1024. Its `delta` includes both
item charts and both bidder substitutions. At n=1024,

\[
\Delta_{1024}=0.0014455159410078\ldots,
\qquad \int\Pi\le I-\Delta_{1024}\le U-\Delta_{1024}.             \tag{12}
\]

Combining with the frozen
\(U=3715139591287203/4194304000000000\) proves the opening rational
bound. A better certified integral bound for this same amplitude-one
stream can be used in (12) without modifying this proof. Improvements
from flow changes supported off both low-report squares can also be
combined after their disjointness is verified.

## 7. Replay and claim boundary

Run `python -B -X utf8 verifier/conditional_global_splice.py` from this
phase directory. It is read-only by default. `--write` regenerates only
its named certificate. The replay constructs the stream directly from
the archived rational coefficients, integrates the opponent coordinates
exactly, and independently checks that integration by direct polynomial
differentiation plus tensor Boole quadrature at three rational own-type
points. Boole is exact here because each opponent-coordinate degree is
at most four. Polynomial primitive differentiation and all cellwise
inequalities are exact integer/rational checks.

The finite partition belongs to the **integral certificate**, not to the
auction's type or allocation domain. Every revenue inequality in this
note applies to arbitrary complete randomized DSIC/IR mechanisms. The
written envelope proof and the separate sign theorem remain mathematical
trusted dependencies; these scripts are not a proof-assistant kernel.
The stronger global upper bound still does not close the gap.
