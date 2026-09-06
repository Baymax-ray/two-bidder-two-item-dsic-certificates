# Independent structural audit of the selected refined mechanism

This note certifies the complete continuous-domain feasibility of
`verifier/refined_candidate.py` and verifies full randomized conditional
optimality on its Q and E fibers. The finite replay in
`verifier/refined_structure_audit.py` independently reconstructs the menus
and checks implementation identities; the all-real arguments below, and
the explicitly identified inherited envelope identities, supply the proof.
Neither the replay nor this note proves global auction optimality or a
common capacity support across both bidders. The revenue evaluation is a
separate obligation and is not audited here.

## 1. Exact parameters and complete menus

Write

\[
 A=2/3,\quad d=1/2,\quad c=157/500,\quad q=d-c=93/500,
\]
\[
 \nu=q^2/2=(1-2c)^2/8,\quad a=A+\nu=1025947/1500000,
\quad b=a+c=1496947/1500000,\quad s=a+d,
\]
\[
 e=4/5,\quad u=3421/10000,\quad
 g(x)=\begin{cases}e(u-x)&c\le x\le u,\\0&\text{otherwise},\end{cases}
 \qquad h(x)=x+q+g(x).
\]

The symbol e here denotes the slope coefficient, not a report or a
lottery probability. In particular g(c)=281/12500 is positive and the
left limit of h at c is d. The h value at c is 6531/12500; h(u)=5281/10000.
The function h is right-continuous and strictly increasing, with slopes
1, 1/5, 1 and one upward jump. Define the generalized inverse by

\[
 k(t)=\begin{cases}
 t-q,&t\le d,\\
 c,&d<t\le h(c),\\
 (t-q-eu)/(1-e),&h(c)<t<h(u),\\
 t-q,&t\ge h(u).
 \end{cases}                                                    \tag{1}
\]

Thus for t>d, x<k(t) implies h(x)<t, while x>=k(t) implies h(x)>=t.
Also k(t)<=t-q and t<=h(k(t)); equality in the latter can fail on the
plateau. These implications, rather than an invalid identity h(k(t))=t
through the jump, are used throughout the proof.

For an opponent report w, write t=max(w), rho=min(w), z=sum(w). Define

\[
 Q=\{t\le A,\ z\le b\},\qquad
 E=\{A<t<T,\ \rho<c\},\quad T=1-2c/3,\quad U=5/3-2c.
\]

The Q region is closed; E has strict inequalities. At a Q_free report
(t<=d), offer empty, item 1, item 2, bundle at prices

\[
 0,A,A,\max(b_0,z),\qquad b_0=(4-\sqrt2)/3.
\]

At a constrained Q report t>d, orient the scarce item along the
opponent's high coordinate. Put

\[
 C_0(k)=5/6+3k^2/4,\qquad
 C=\max\{C_0(k(t)),z,k(t)+h(\rho)\},\qquad B=\min\{A,C-k(t)\}.
                                                               \tag{2}
\]

Offer empty, safe singleton, scarce singleton, bundle at prices 0,B,A,C.
The cap in B is essential to this candidate and its full Q claim.

At an E report, put

\[
 \delta=9(T-t)(U-t)/16,\quad \alpha=3t-2,\quad
 \beta=\alpha/(\alpha+2\delta).
\]

Offer allocation/payment pairs, with the scarce coordinate first,

\[
 (0,0;0),\ (0,1;d+\delta),\ (1,0;t),\
 (1,1;t+c+\delta),\ (1,\beta;t+\beta c).                         \tag{3}
\]

All remaining reports use the base menu. If w=(w1,w2), set

\[
 H=\max(0,w_1-a,w_2-a,w_1+w_2-b),
\]
\[
 P_1=H+\min(a,s-w_2),\quad
 P_2=H+\min(a,s-w_1),\quad P_B=H+b.                              \tag{4}
\]

Add g(rho) to the singleton for the physical low coordinate of w and
to the bundle. This includes the rho=c face. Orientation ties use the
same fixed item priority as the implementation; a positive fee at equal
coordinates cannot occur on a retained base report, since those equal
coordinates would lie in Q_free.

At each profile form the two full menu argmax sets. A bidder with zero
maximum utility uses empty only. For positive utility retain all
maximizers. Select the lexicographically first jointly feasible pair
of those options, in the explicit menu orders above and the base
empty/item1/item2/bundle order. Sections 3--6 prove that this pair always
exists. Thus every real report, threshold face, inverse knot, and tie is
covered by the rule.

## 2. The extra C floor is uniformly redundant

Let

\[
 K=A-q=721/1500,\quad \rho_*=b-A=165649/500000,
 \qquad B_0(k)=C_0(k)-k.
\]

On constrained Q, c<=k<=K<d, and B0 decreases there. The exact inequalities

\[
 d<B_0(K)\le B_0(k)\le B_0(c)<A,\qquad
 B_0(K)-h(\rho_*)=37/5000000>0                                  \tag{5}
\]

hold. If rho lies outside [c,u], then g(rho)=0 and t-k>=q, giving
z>=k+h(rho). For rho in [c,u], Q gives

\[
 k\le\min(K,b-\rho-q).
\]

When rho<=rho*, decreasing B0 and increasing h give
B0(k)-h(rho)>=B0(K)-h(rho*). When rho>=rho*, the lower bound
B0(b-rho-q)-h(rho) has derivative

\[
 e-\tfrac32(b-\rho-q)\ge e-\tfrac32K=79/1000>0.
\]

Its minimum is again at rho*. Consequently (2) simplifies everywhere to
C=max(C0(k),z), with strict uniform slack against the extra floor on the
fee support. There is no unintegrated extra-floor region. If B is capped,
then necessarily C=z and C>b0, because B0(k)<A and C0(c)>b0.

A second inequality used in Q/base compatibility is

\[
 S(k):=C_0(k)-k-d\ge g(k).
                                                               \tag{6}
\]

Outside the support it follows from (5). On [c,u], the difference has
positive derivative 3k/2-1+e and has minimum
S(c)-g(c)=212401/3000000>0. Together with t<=h(k), (6) gives
C0(k)>=t+c, including every plateau type.

## 3. Base/base and the precise surcharge argument

Before the fee, menus (4) are the pivot-normalized menus of the common
nine-outcome affine maximizer: the empty allocation has cost 0, one bidder's
singleton has cost a, one bidder's bundle has cost b, and an allocation
splitting the items across bidders has cost s. Hence there is a common
feasible pair of base menu maximizers at every profile. Removing any
zero-utility allocation preserves a feasible maximizing pair with the
stated empty rule.

Adding a common nonnegative fee to the safe singleton and bundle does
not follow from a generic claim that prices increased. The needed strict
discount condition is

\[
 P_{\rm scarce}+P_{\rm safe}-P_B\ge q>0.                         \tag{7}
\]

This follows from (4). If both coordinates are at most d, the left side
is at least a-c>q. If exactly one is above d, use H>=t-a to obtain q.
If both exceed d, use H>=sum(w)-b to obtain 2q.

For any old safe maximizer at own report (x,y), comparison with the
bundle gives x<=PB-Psafe<Pscarce; its scarce singleton has negative
utility. The common fee leaves the bundle-minus-safe comparison
unchanged, so a new maximizer can be chosen to be the same safe item or
empty. An old scarce or empty maximizer remains a maximizer because
its price is unchanged and the others only increased. An old bundle
contains any possible new allocation. Thus every old maximizer admits
a new maximizing allocation contained in it, including all positive
ties. Applying this fact to a common feasible base pair proves
base/base compatibility after both fees. This is a local argument for
the fee rows, not a claim that the whole refined mechanism is contained
in a predecessor allocation.

## 4. Q against base and Q against Q

Fix a Q report w=(t,rho), aligned along item 1, and let the other report
be v=(x,y). Any base price is at least d per singleton and at least b
for the bundle. Since sum(w)<=b and rho<d when t>d, the base bidder of
type w can only obtain item 1 positively; at t<=d it must be empty.

For y<=d, its item-1 price is H+a plus a nonnegative fee and satisfies
P1>=max(x,x+y-c). An opposing Q scarce singleton with positive utility
requires x>A>=t. An opposing Q bundle, if selected, requires
x+y>=C>=C0(k)>=t+c by IR and (6). Therefore the base high price is at
least t whenever the opposing Q menu consumes item 1. The base bidder
then has maximum utility zero and uses empty. The free-Q case was
already covered by t<=d.

For y>d the base price is at least x+q. If the base bidder had a strictly
positive item-1 purchase, x<t-q<=K<d<y. Thus x is precisely the low
coordinate of the base report: the fee, if active, is applied to this
physical item, giving P1>=h(x). On the Q side, a scarce singleton needs
x>=A>k, and a bundle needs x>=C-B>=k by comparison with safe. Hence
h(x)>=t, contradicting the positive base purchase. This argument covers
the rho=c fee face, all inverse knots, and capped Q bundles.

For Q/Q profiles, each own coordinate is at most A. No scarce singleton
at price A is positive, and no capped safe singleton at A is positive.
Any positive uncapped singleton costs more than d, while a constrained
Q report's low coordinate is below d. Therefore singleton choices can
only be the two distinct own high goods when the reports have opposite
orientations. Two positive bundles are impossible because each bundle
price is at least the opposing report's sum.

It remains to exclude bundle/safe conflict under opposite orientations.
An uncapped safe buyer with high value y and opposing low value rho has

\[
 y>B\ge h(\rho).
\]

A conflicting bundle in the other menu needs rho>=k(y); the cap can
only increase that bundle-upgrade threshold. Equation (1) then gives
h(rho)>=y, a contradiction. The strict inequality comes from the safe
buyer's positive utility, so it persists when the bundle/safe comparison
on the other side is tied. Same orientations have no positive singleton
and hence no remaining conflict. At Q_free types the singleton prices A
also exclude positive singletons; their low maximum precludes positive
safe purchases in the opposite constrained menu. Empty at zero completes
all remaining equality cases.

## 5. E compatibility, including the reserve allowance boundary

For (3), let L=delta+alpha/2, Y=c+L and j=1-t/2. Algebra gives

\[
 \beta L=\alpha/2,\quad t+c+\delta-Y=j,\quad
 c<Y<d<d+\delta<A,\quad d<j<A<t,
\]

with 0<beta<1 and E upgrade threshold t-q>c. These strict inequalities
hold throughout A<t<T and follow from the factored delta.

First pair E against an uncharged base menu. A bidder of own E type
w=(t,rho), rho<c, cannot buy its low base singleton, and its base bundle
is dominated by the high singleton because PB-P1>=c>rho. Only item 1
can conflict. If the other own report is (x,y) with y<=d, the base high
price is at least max(x,x+y-c). An E scarce purchase needs x>=t; a bundle
needs x+y>=t+c+delta; a lottery is dominated by bundle for y>Y and its
IR condition is x+beta(y-c)>=t. In the lottery case y>=c implies
x+y-c>=t, while y<c implies x>=t. In all cases that consume item 1,
the base high price is at least t. If y>d, the base high price is at
least x+q; the E lottery cannot win, and any bundle needs x>=t-q.
Again the base buyer is empty. This proves the clean E/base pair;
Section 3's maximizing-subset lemma then permits the actual base fee
without changing the E allocation.

For E/Q, an own Q report v has coordinates at most A and sum at most
b=a+c, which is now larger than A+c. The old simpler total-value
argument therefore requires replacement. Its E scarce singleton has
negative utility. Its E lottery utility is at most

\[
 A-t+\beta(a-A).
\]

Indeed for the lottery's safe coordinate y>=c this follows by writing
its value as (1-beta)x+beta(x+y-c), and for y<c the scarce singleton
dominates it. Now

\[
 (t-A)/\beta=t-A+2\delta/3
\]

is strictly increasing on (A,T), with derivative at least d+c>0. Its
infimum at A is 2delta(A)/3=q^2/2=nu=a-A. Therefore the lottery has
strictly negative utility throughout the actual open E interval,
including the chosen equality in the reserve allowance. The Q buyer's
E bundle utility is at most a-t-delta. The function t-A+delta is
strictly increasing, and delta(A)=3q^2/4>nu, so this utility is also
negative. Thus only an E safe singleton can be positive.

That safe purchase has coordinate y>d, making y the own Q high
coordinate. The reverse Q menu has scarce-upgrade threshold at least
k(y)>=c, including the generalized-inverse plateau. Its buyer's E low
value rho<c cannot obtain the conflicting good as scarce or bundle.
There is no E/Q conflict. Notice that the weak k(y)>=c is enough;
strict k(y)>c would be false for this h.

Finally, at E/E reports with the same physical orientation, own low
value below c makes the bundle and lottery dominated by the scarce
singleton; only the larger high value can buy it. Equal high values
give zero utility. At opposite orientations, each own scarce coordinate
is below c, below the bundle upgrade t-q, and below the E lottery cell's
smallest scarce coordinate j>d. Only the disjoint own high goods can
be allocated. These cases cover all menu-region pairs.

## 6. Pointwise mechanism properties

The preceding arguments prove a nonempty feasible pair of full menu
maximizers at every profile. The finite rule in Section 1 thus defines
a complete mechanism on [0,1]^4. For a fixed opponent report, every
selected option attains exactly the maximum utility of the same fixed
conditional menu. Every possible misreport selects another option in
that menu and cannot improve the true type's utility. This proves
pointwise DSIC for all true reports, all deviations, and all opponent
reports, independently of the report-dependent joint tie selection.
Empty gives pointwise IR. Borel menu formulas, comparisons and finite
selection prove measurability. Each payment is nonnegative and bounded
by the type's allocated value, at most 2, so revenue is integrable.

Joint feasibility of marginal allocations can be realized as a
samplewise feasible allocation: for each item use disjoint intervals
of lengths x1j and x2j in [0,1] for a uniform random variable, leaving
any remainder unassigned. Expected allocation and payment reproduce
the stated menus. The theorem is truthful in expected utility and
does not claim universal truthfulness of individual random seeds.

## 7. Full randomized conditional certificates on Q

The identities used here are in the frozen predecessor
`V4_6/research_log/inner_diagonal_capacity.md`, including its coupled
singleton/bundle section. These are exact envelope identities for every
complete measurable randomized DSIC/IR competitor, not finite-menu
comparisons. We verify their parameter signs and actual residual
saturation for the refined mechanism.

For a constrained Q opponent w=(t,rho), fix k=k(t). At the actual own
report (x,1) with x<k, the opposing base high price is exactly

\[
 \max(d,x+q)+g(x)=\max(d,h(x))<t.
\]

Its low singleton and bundle cannot yield positive utility for w.
Hence the opponent strictly occupies the scarce good at every such
report, giving the required actual top capacity hole r1(x,1)=0.

For an uncapped row, prices are (A,C-k,C), with c<=k<=K<d,
d<C-k<=A, and C>=C0(k). The value C0(k) can exceed 1 near t=A;
no C<=b or C<1 assertion is used when C=C0(k). The coupled envelope has
top coefficient

\[
 f(x)=\begin{cases}3(C-k)-2,&x<k,\\
                  3C-3x-2,&k<x<A,\\1,&x>A,\end{cases}
 \quad m=\int f=2(C-C_0(k))\ge0.
\]

Thus f<=0 below A and the anchored cumulative price Fm is nonnegative.
The predecessor's displayed upper limit .91 is not a theorem
hypothesis used by the derivation: the operative conditions are the
ordering k<d<A, the sign C-k<=A, and m>=0, all verified here. When
m=0 the occupied top hole and feasibility give equality directly.

When m>0, C=sum(w)>C0(k)>b0. At the actual own reports (x,0), 0<x<d,
and (d,y), 0<y<C-d, the reverse menu is Q_free. Its bundle price is
strictly below C. Since both coordinates of w are at most A, its
singleton utilities are nonpositive, while its bundle utility is
strictly positive. The opponent strictly occupies both goods on the
needed bottom and vertical anchors. This proves all additional actual
capacity saturation requirements of the coupled identity.

For a capped row, Section 2 gives C=sum(w)>b0 and both singletons cost
A. The symmetric diagonal theorem applies with k'=C-A<d and

\[
 m'=1/3-3(4/3-C)^2/2\ge0.
\]

It needs the same bottom and vertical anchors, which were just proved.
It does not need a top hole below k': its top capacity price is zero
there. Above k' the candidate allocates the priced scarce good with
probability one, and feasibility supplies saturation. Thus increasing
the effective upgrade from k to k' creates no missing capacity premise.

For Q_free with C=max(b0,sum(w)), C=b0 has the full-capacity SJA upper
certificate and feasibility. At C>b0 the symmetric diagonal theorem
and the same Q_free anchors apply. Here k'=C-A<d and m'>=0 continue to
hold up to b, so no old .91 parameter limit is inherited without
checking its operative conditions.

The nonnegative volume, top and anchor capacity measures and their
nonnegative utility slack therefore match the candidate throughout Q,
for either bidder's actual residual. This proves full randomized
conditional optimality on every Q fiber. The cap is necessary to this
claim; an uncapped C-k>A row would violate f<=0 and admits the explicit
singleton-price improvement investigated separately in this branch.

## 8. Full randomized conditional certificates on E: an IC trace repair

The general E identity is the frozen
`V4_6/research_log/inner_lottery_certificate.md`, Sections 1--6. With
q=93/500 its geometry is as in Section 5. Its zero-top-mass identity is

\[
 3\{A(t+c+\delta)-Aj+j^2/2-(t-q)^2/2\}-1=0,
 \qquad j=1-t/2.                                                \tag{8}
\]

Our verifier expands (8) as a rational polynomial in t and checks every
coefficient. The remaining algebra uses beta L=alpha/2, c=d-q and the
strict sink lower bound q(1-3q/2)>0. Thus the inherited nonlinear convex
trace and arbitrary-allocation envelope inequalities retain their signs.

Its actual top-hole premise H1 remains valid. At own (x,1), x<t-q,
outside [c,u] the opposing high price max(d,x+q) is less than t. On
[c,u] it is h(x)<=h(u)=5281/10000<A<t. The opposing E type has low
value below c and strictly buys its high good. Thus r1(x,1)=0 on the
entire required top interval.

The old literal junction-hole premise H2 must **not** be asserted:
for a>A, the actual residual at some (x,c), A<x<t, is positive. The
independent verifier retains an exact vacant-face example. The needed
replacement is the following actual-inner implication.

For every own report (x,y) in the open rectangle

\[
 A<x<t,\qquad 0<y<c,
\]

the reverse menu is E. The opposing type w=(t,rho) buys its high singleton
strictly, since t>x and rho<c. Bundle and lottery are dominated by that
singleton; safe utility is negative. Hence the actual residual scarce
capacity is zero throughout this open rectangle.

Let (v,allocation) be any complete DSIC/IR competitor under the actual
residual. The selected scarce allocation is zero there. Applying the
two DSIC inequalities at any two horizontal reports in the rectangle
shows that v(x,y) is constant in x for each fixed y<c. Bounded allocation
in [0,1]^2 makes v coordinatewise 1-Lipschitz. Continuity therefore
extends horizontal constancy to y=c. At an interior x in (A,t), applying
the subgradient inequalities to a point on each side along the constant
trace forces the selected scarce allocation at (x,c) to equal zero.
This conclusion includes exceptional selected subgradients; it is not
just an almost-everywhere derivative claim.

In the inherited E identity, H2 is used only for the nonnegative
singular-line price

\[
 3t(c+L/4)\,dx\,\delta_c(dy)\quad\text{on }A<x<t.
\]

Every actual-residual competitor now has zero allocation on that segment
by the IC argument. Remove that segment from the capacity-price constant
and from its pairing with allocations; both allocation terms are zero.
Retain the original exact identity with its nonnegative convex-trace
slack, corner-monotonicity slack, and IR sink. The remaining volume,
top-line, and upper junction-line prices are saturated by the feasible
candidate. Its trace is constant below c and affine through the lottery
interval, so all original candidate slacks are zero. This gives a tight
upper bound for every complete randomized competitor under the actual
residual and proves full conditional optimality throughout E.

This repair is an actual-residual inner certificate. Removing the line
segment does not establish a supergradient valid for every other Borel
residual: the vanished allocation was inferred using this particular
open rectangle's capacity. A common global capacity-price measure for
the two bidders remains an independent unresolved task.

## 9. Replay and claim boundary

The independent verifier reconstructs all menus without importing the
candidate implementation, checks 47 specifically selected rational
types and every one of their 2,209 pairs, verifies inverse jump/image
knots and actual Q/E trace cases, and then compares all 47 menus and
188 selected profiles with `refined_candidate.py`. It checks the exact
uniform floor slack 37/5000000, the reserve allowance equality, the E
polynomial identity, and the strict sink bound. It distinguishes an
actually vacant E junction face from the occupied open rectangle that
forces its allocation by IC. Its exact JSON records those counts.

These are finite implementation and algebra replays supporting the
written all-real proof. They are neither a type-grid optimization nor a
proof-assistant formalization. The full conditional Q/E conclusions
bound arbitrary randomized mechanisms and do not assume a finite
allocation range. Remaining base fibers, parameter optimality, joint
outer optimality, exact revenue integration and a matching unrestricted
auction upper bound are outside this audit's conclusion. Alternative
structural experiments in this branch are not additive gains to this
selected combined mechanism.
