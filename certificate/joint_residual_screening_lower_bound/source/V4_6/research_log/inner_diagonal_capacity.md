# Full randomized screening with a binding diagonal capacity hole

The bundle-exchange step changes bidder 2's menu on part of Q and therefore
invalidates the old full-Q equality claim. This note recertifies the entire
changed part having opponent maximum at most 1/2. It does not assume a
finite menu for competitors. The coupled-response section at the end then
recertifies the remaining changed Q fibers whose maximum exceeds 1/2.

Let \(A=2/3\), \(b_0=(4-\sqrt2)/3\), and
\(b_0\le z\le91/100\). The candidate offers empty, item 1, item 2,
bundle at prices \(0,A,A,z\), with the inherited empty-first priority.
Its utility is \(u^*=\max(0,x-A,y-A,x+y-z)\). Put \(k=z-A\).

The theorem below needs candidate feasibility and only these occupied
traces of the actual residual:

\[
r_1(x,0)=0\quad(0<x<1/2),\qquad
r_2(1/2,y)=0\quad(0<y<z-1/2).                    \tag{1}
\]

No capacity assumptions elsewhere are needed. For the actual bundle
exchange, these traces are occupied because bidder 1 purchases a bundle
at all such profiles. Full feasibility on all other profiles was proved
in `outer_bundle_exchange.md`.

Define

\[
\ell(x)=\begin{cases}A&x<k,\\z-x&k<x<A,\end{cases}
\quad D_0=\{x<A,\ y<\ell(x)\},
\]
\[
f(x)=\begin{cases}0&x<k,\\-3(x-k)&k<x<A,\\1&x>A.\end{cases}
\]

Its total mass is

\[
m=\int_0^1 f(x)dx
=\frac13-\frac32(4/3-z)^2
=4z-\frac73-\frac32z^2\ge0.                       \tag{2}
\]

The first equality makes the sign exact: at z=b0 the squared factor is
2/9, and it decreases for z between b0 and 91/100. Also \(k<1/2<A\).

Anchor the top trace at x=1/2. The nonnegative density

\[
F_m(x)=\int_x^1f(s)ds-m1_{x<1/2}
=\begin{cases}
0,&x<k,\\
\tfrac32(x-k)^2,&k<x<1/2,\\
m+\tfrac32(x-k)^2,&1/2<x<A,\\
1-x,&x>A
\end{cases}                                                   \tag{3}
\]

has a jump of m at x=1/2. This is a bounded density on the top edge, not
an omitted atom. Integration by parts for an arbitrary complete DSIC/IR
utility u gives

\[
\int f(x)u(x,1)dx
=m u(1/2,1)+\int F_m(x)a_1(x,1)dx.                \tag{4}
\]

Horizontal envelopes on x>A and vertical envelopes on
\(x<A,y>\ell(x)\) yield the same exact revenue identity as the Q
argument, but the top coefficient now has positive mass m. Expand its
anchor along two actual report lines:

\[
u(1/2,1)=u(0,0)+\int_0^{1/2}a_1(x,0)dx
                         +\int_0^1a_2(1/2,y)dy.             \tag{5}
\]

Thus a global nonnegative capacity-price measure is

\[
\boxed{\begin{aligned}
\pi_1={}&3(x-A)_+\,dxdy+F_m(x)\,dx\delta_1(dy)
                 +m1_{0<x<1/2}\,dx\delta_0(dy),\\
\pi_2={}&3(y-\ell(x))_+1_{x<A}\,dxdy
                 +m\delta_{1/2}(dx)\,dy.
\end{aligned}}                                                \tag{6}
\]

For every randomized complete DSIC/IR mechanism a and every Borel
residual r with a<=r, all pointwise selected subgradients included,

\[
\boxed{\langle\pi,r\rangle-R
=\langle\pi,r-a\rangle+3\int_{D_0}u-mu(0,0)\ge0.} \tag{7}
\]

Indeed \(3|D_0|=m+1\), and monotonicity and IR imply
\(u\ge u(0,0)\ge0\) everywhere. The last slack is therefore at
least u(0,0). No positive sink at every type is required.

At the candidate, u(0,0)=0 and u vanishes on D0. All positive volume
prices charge a marginal allocated with probability one. The top-edge
price vanishes for x<k, and above k the candidate takes item 1 with
probability one. On the bottom edge it allocates nothing, and (1) gives
zero residual for the priced item. On x=1/2 its second marginal is zero
below z-1/2 and one above, so (1) and candidate feasibility again give
saturation. Individual line endpoints have zero price mass; their
allocation is still defined by the complete tie rule.

Consequently the candidate solves the **full randomized inner problem**,
and (6) is a global supporting measure for the residual value functional.
Its exact conditional value is

\[
\boxed{V(z)=\frac12z^3-2z^2+\frac73z-\frac8{27}.}   \tag{8}
\]

This is the complete deterministic menu-cell integral at (A,A,z), now
matched by a bound over every randomized competitor.

## Actual occupied boundaries after both joint reallocations

Fix bidder 1's report w with maximum at most 1/2 and
\(b_0<z=w_1+w_2\le91/100\). At bidder 2's report (x,0),
0<=x<=1/2, the opponent report belongs to the closed free set F. Bidder
1's SJA menu sells its bundle to w strictly, since z>b0 and both
singletons have negative utility. Hence the first condition in (1) holds.

At bidder 2's report (1/2,y), y<z-1/2, its sum is less than z. If that
sum is at most b0, the closed free-region menu sells bidder 1 a bundle at
b0. Otherwise it lies in the bundle-exchange region G and sells bidder 1
a bundle at price 1/2+y<z. This proves the second condition in (1),
including the intermediate boundary y=b0-1/2 because F is closed.

The corner-release perturbation changes bidder 1's menus only when its
opponent's high coordinate is near .7, so neither of these occupied traces
is altered. Its bidder-2 lottery change also has opponent high coordinate
near .7 and is absent on the present w region. The complete candidate is
unchanged and feasible. Therefore this full inner certificate survives
the final joint price deformation.

At z=b0, m=0 and the theorem reduces to the already verified full-capacity
SJA support, so the free-region boundary is covered as well. The endpoint
z=91/100 is also included: the proof uses opponent sums strictly below z
on the occupied vertical interval and retains the stated old rule at its
endpoint. This restores the full inner claim on the entire max<=1/2
part of Q. The coupled-response section below supplies the further screening
needed on the changed max>1/2 portion.

The measure is a conditional support. Its singular charges need not
support the other bidder, so this is not a matching unrestricted auction
upper bound.

## Coupled singleton and bundle response on the constrained part of Q

The same method also closes the reopened constrained fibers, provided the
safe singleton price is reoptimized along with the bundle price. Fix
\(t>1/2\), \(k=t-q\), \(C_0=5/6+3k^2/4\), and
\(C=C_0+\eta\le91/100\), where eta>=0. Set

\[
A=2/3,\qquad B=C-k.
\]

Keep the scarce singleton at A and raise both original safe and bundle
prices by eta. This is a complete pointwise contraction of the original
Q menu. The coupled-response feasibility proof additionally verifies the
new bidder-1 bundle exchange at every report and tie.

In these parameters the preceding proof changes only to

\[
\ell(x)=B\ (x<k),\quad \ell(x)=C-x\ (k<x<A),
\]
\[
f(x)=3B-2\ (x<k),\quad f(x)=3C-3x-2\ (k<x<A),
\quad f(x)=1\ (x>A),
\]
\[
m=\int f=2(C-C_0)=2\eta\ge0,
\qquad F_m(x)=\int_x^1f(s)ds-m1_{x<1/2}.
\]

Here \(k<1/2\) and \(B<2/3\), so f<=0 below A. For x<1/2,
\(F_m=-\int_0^x f\ge0\); for 1/2<x<A it equals that same
nonnegative quantity plus m; above A it equals 1-x. Equations (4)--(7)
hold without any further change, including the identity
\(3|D_0|=m+1\). The capacity measure is therefore a full randomized
global support.

There is one additional saturation obligation compared with the symmetric
case: F_m is now positive below k. The inherited actual top capacity is
zero there, because at own report (x,1) the other bidder purchases its
scarce item exactly for x<k. The bundle-exchange and corner-release
modifications do not change those top rows.

The newly occupied bottom and vertical lines also hold. Reopening is
possible only for

\[
1/2<t<q+\sqrt{23}/15<a=159/250.
\]

Both coordinates of the other bidder are therefore below a (its low
coordinate is C-t<1/2). At report (x,0), x<=1/2, its free-region SJA menu
sells a bundle since its total C exceeds C0>b0. At report (1/2,y) with
y<C-1/2, either the free SJA bundle price is b0<C or the new G bundle
price is 1/2+y<C. No singleton beats that bundle: both own coordinates
are below a and below A. This proves exactly the same two occupied
traces (1), with z replaced by C. Above the vertical threshold the
candidate takes the bundle, since 1/2>k. Candidate feasibility supplies
the remaining saturation.

Thus the coupled response \((A,C-k,C)\) solves each full randomized
inner problem on the reopened constrained Q region. Combined with the
symmetric case above and the retained Qminus theorem, it restores the
full Q conditional-optimality statement after the bundle exchange and
the coupled response. The final corner release is disjoint from the
priced bottom, vertical, and top traces for these Q reports; its own
changed bidder-2 menus have opponent maximum near .7, outside Q. The
restored Q statement survives that deformation.

The exact conditional revenue is the full polynomial
\(\mathscr R(2/3,C-k,C)\), with \(\mathscr R\) defined in the bundle
exchange note. The exact replayer checks its agreement with independent
rational polygon integration and the gap identity. These tests do not
replace the all-real proof above.

