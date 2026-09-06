# Reserve and split constants are not structural equalities

This independent route studies the reserve a on both sides of A=2/3 and
separates a base split increment d from the conditional screening reserve 1/2.
Only the explicitly implemented reserve candidate is accepted as a new lower
bound here. Rejected split experiments are recorded as bounded routes, not
as a theorem forcing d=1/2 in the unrestricted optimizer.

## 1. A sufficient joint family with a different reserve

First fix d=1/2, q=d-c, b=a+c, s=a+d, A=2/3 and require

1/2<a, 0<c<1/3, a+c<1,
nu=max(a-A,0) <= (1-2c)^2/8.

Keep Q={max(w)<=A,sum(w)<=b}. Write t=max(w), rho=min(w).
Free Q (t<=d) offers singleton A,A and bundle max(b0,sum(w)), with
b0=(4-sqrt(2))/3. Constrained Q offers scarce A, safe C-k, bundle C,
where k=t-q and C=max(5/6+3k^2/4,sum(w)). Empty is free.

E={A<t<T,rho<c}, T=1-2c/3, U=5/3-2c, keeps the familiar five options:
safe d+delta, scarce t, bundle t+c+delta, lottery (1,beta) at t+beta*c,
where delta=9(T-t)(U-t)/16, alpha=3t-2, beta=alpha/(alpha+2delta).
The lottery's first physical coordinate denotes scarce, as usual.
All remaining reports use the common affine base with pivot
H=max(0,w1-a,w2-a,sum(w)-b), singleton prices
H+min(a,s-w2), H+min(a,s-w1), and bundle H+b.

Every menu contains empty at zero. Zero utility selects empty. Otherwise
choose the lexicographically first jointly feasible pair of menu maximizers,
using empty/safe/scarce/bundle in constrained Q, empty/item1/item2/bundle
in free Q and base, and empty/safe/scarce/bundle/lottery in E. The following
proof establishes existence of this pair on every real profile.

## 2. Q versus base, including a below A

Fix the Q report w=(t,rho), aligned with its high item. Since b<1,
rho<=b/2<d. A base menu cannot sell a bundle positively to w: its price
is at least b>=sum(w). Its low singleton price is at least d, so that
option cannot be positive either. The only possible opposing base
allocation is w's high item.

Let the other own report be v=(x,y). When y<=d the base high price is
P=H+a>=max(x,x+y-c). A positive Q scarce singleton has x>A>=t and is
therefore incompatible with a positive purchase by w. A Q bundle has
x+y>=C>=C0(k), and

C0(k)-t-c = [C0(k)-k]-d >0,

because the safe screening price exceeds 1/2. Thus P>=t in this case too.
This argument uses neither a=A nor a>=A. It replaces the insufficient
argument P>=A when a<A.

When y>d, the base high price is H+s-y>=x+q. A Q bundle requires
x>=k=t-q, and a positive Q scarce singleton requires x>A>k. Hence the
opposing utility is at most zero whenever that physical item is consumed.
At contested equality the base bidder selects empty. The free-Q case has
t<=d, and both base singleton prices are at least d, so the opposing base
bidder is globally empty. This proves Q/base compatibility.

## 3. Q/Q and the role of the sum floor

Every scarce singleton utility at a Q own type is nonpositive. Every
constrained safe price exceeds 1/2, and own low values are below 1/2.
Consequently a positive singleton can only be an own high item under
opposite high orientations; two such singletons are disjoint.
Two positive bundles would require sum(v)>sum(w) and sum(w)>sum(v),
because C>=sum(opponent). In an opposite-orientation bundle/safe conflict,
safe purchase gives y>B>=rho+q, while the other bundle needs
rho>=y-q. These inequalities contradict each other. Free-Q singleton
prices A exclude the exceptional free/constrained case. Empty handles
zero utility; the displayed weak bundle inequality already covers ties.

## 4. E/Q: an explicit allowance above A

For a Q own report v, the E scarce singleton has strictly negative utility.
Using max(v)<=A and sum(v)<=b=a+c, the E lottery utility is at most

A-t+beta(a-A).

Set f(t)=(t-A)/beta=t-A+2delta(t)/3. Its derivative is at least 1/2+c>0,
so its infimum on E is

f(A)=2delta(A)/3=(1-2c)^2/8.

Thus the stated nu bound excludes every positive E lottery at a Q type.
Similarly, t-A+delta(t) is increasing with derivative at least 1/4+3c/2>0,
and delta(A)=3(1-2c)^2/16 exceeds the allowance. The E bundle is therefore
strictly unprofitable at Q types. Only the E safe singleton can be positive,
and that requires a coordinate y>d. The opposing Q scarce threshold is
y-q>c, while the E own low value is below c. Hence no conflicting Q upgrade
is possible. When a<=A, the lottery/bundle exclusion is strictly easier.

## 5. E/base, E/E and base/base

An E type w=(t,rho) with rho<c cannot choose the base bundle in preference
to its high singleton, since their price difference is at least c. Its
low singleton price is at least d>rho. Only the high singleton can matter.

For opposing report v=(x,y), if y<=d its base high price is at least
max(x,x+y-c). An E scarce singleton needs x>=t; an E bundle needs
x+y>=t+c+delta; and an E lottery has c<=y<=Y<=d and
x+beta(y-c)>=t, implying x+y-c>=t. Thus no contested positive base
purchase is possible. If y>d, the base high price is at least x+q. An E
bundle needs x>=t-q, a scarce singleton has x>=t, and an E lottery cannot
win at y>d. Again the base utility is at most zero at contested equality.
These arguments are independent of a=A.

For same high orientations in E/E, a buyer's own safe value is below c,
so bundle and lottery are dominated by its scarce singleton. Only one
strict high-singleton purchase is possible. For opposite orientations,
the own scarce value is below c; E bundle and lottery winning regions
require scarce value above 1/2>c. Only the two disjoint safe singletons
can be bought. Empty handles equality. Base/base feasibility follows from
a common maximizing allocation among the nine feasible deterministic outcomes
with costs 0,a,a,b,a,a,b,s,s.

These six pair arguments prove a feasible maximizer pair exists everywhere.
Every selected option is a conditional menu maximizer, so DSIC holds for every
true report, deviation and opponent. Empty gives IR. The formulas and finite
first-feasible choice are Borel; selected payments are nonnegative and at most
two by IR. Per-item disjoint marginal intervals realize pointwise feasible
allocations. No report, algebraic face, or tie is omitted.

## 6. A complete accepted reserve candidate

Take c=47/150 and

a=A+(1-2c)^2/8=3848/5625,

with all other quantities as above. This is implemented in
`structural_reserve_candidate.py`; the full real formula is Sections 1--5.
Its exact revenue lies strictly between

0.876456168324744236873688693189 and
0.876456168324744236873688693190.

It exceeds the strongest V4.6.1 baseline by approximately 0.0000005544884184.
This is a modest independent alternative, not an increment to stack with
other a,c,h trials. It demonstrates that the equality a=A need not be imposed
by pointwise feasibility. It does not establish a valuable asymptotic rate or
the optimizer's reserve.

The exact revenue certificate supplies three rational coefficients in the
basis (1,sqrt(2),sqrt(D)), D=4(b-5/6)/3. They are computed by rational
polynomial antiderivatives and exact quadratic endpoint evaluation. An
independent decomposition subtracting base menus over Q and the short E
strip A<t<a gives a matching rational enclosure. All conditional menu cells
are integrated over the full continuous domain, including bundle competition;
finite rational cases are supplementary implementation checks.

For clarity the direct decomposition is:

R = R_base,outside(Q,E)
  +2*area(Q_free)*R_SJA
  +2*integral_(b0)^b (1-z)[R(A,A,z)-R_SJA] dz
  +4*integral_d^A (b-t)I(t-q) dt
  -(4/3)*integral_d^(q+sqrt(D)) [b-C0(t-q)]^3 dt
  +4c*integral_A^T [R(t,1/2,t+c)+delta(t)^2] dt.

All polynomial limits other than b0 and q+sqrt(D) are rational. The outside
base contribution is evaluated on explicit rational polygon intersections;
it includes menus having singleton prices above one. Equality surfaces have
zero conditional area, so their complete pointwise tie implementation does
not alter these continuous integrals.

The old full E certificate must NOT be inherited for a>A: its junction trace
(x,c), A<x<t<a, now charges a rather than x and need not be occupied. Raised Q
safe prices can also exceed A. This candidate is certified feasible with exact
revenue, not conditionally optimal throughout Q/E.

## 7. Compatibility with a general right-continuous exchange

The reserve proof extends to a nonnegative g and h(x)=x+q+g(x), provided h is
strictly increasing between its permitted upward jumps, right-continuous,
h(c-)=d, and g is zero below c. Define k(t)=inf{x:h(x)>=t}; a jump at c may
create the plateau k(t)=c. Use

C=max(C0(k),sum(w),k+h(rho))

in constrained Q, and add g(low opponent value) to the safe singleton and
bundle on every base row. Keep E as above. A sufficient additional condition is

g(x)<=S(x):=C0(x)-x-d

on inverse values used by Q, with g(c) interpreted at the upper side of the
initial jump. On a plateau it implies C0(k)>=t+c; elsewhere this follows from
t=h(k). Thus the y<=d Q/base argument in Section 2 survives even for a<A.
When y>d, a positive competing base purchase requires x<t-q<=A-q<d<y.
Its surcharge is therefore applied to exactly the physical item in conflict,
and its price is at least h(x). If x>=k(t), right-continuity gives h(x)>=t.
The Q/Q conflict is y>h(rho) versus rho>=k(y), impossible by monotonicity.
The E/Q argument uses k(y)>=c for y>d and otherwise is unchanged.

A safe/bundle surcharge is a contraction of these discounted base tariffs.
Indeed their singleton prices P,B and bundle C satisfy P+B-C>=q>0. An old
safe maximizer has own scarce value x<=C-B<P, so the scarce singleton cannot
become a new positive choice after the common surcharge. Old scarce and empty
choices remain possible, and any new bundle choice is a subset of an old bundle.
Thus compatible maximizing subsets of old feasible base/base and E/base pairs
exist, including ties. This completes the sufficient-family feasibility proof.

These are **feasibility conditions**, not a full conditional certificate for
arbitrary h. In particular, a newly binding k+h(rho) floor or B>A can invalidate
the old diagonal support. If a<=A and the extra floor is redundant, B<=A on
sum-floor rows; this is one reason lowering a may preserve the simple full-inner
proof more easily than raising it. E's top support also requires a separate
bound ensuring changed h(x)<t on its priced interval. No such condition is
silently assumed from nonnegative g.

## 8. Two rejected split paths

Increasing the physical base split increment above d=1/2, while retaining
all Q/E menus, is pointwise feasible: contested active base prices only
increase, and base/base remains a common feasible allocation problem. Its
exact outside-region revenue change at d=5001/10000 is

-1337292791172831271/243000000000000000000000 <0.

A coordinated decrease is also admissible when b<=2d<=1. Use the free-Q
cutoff d, constrained threshold k=t-(d-c), and replace E's internal constant
by cE=1/2-(d-c)>=c, retaining its low-opponent strip rho<c and using
TE=1-2cE/3. The Q low coordinate is at most b/2<=d, so the conflict proof
still applies; E/Q exclusion is easier because cE>=c. The base/E comparisons
have additional nonnegative slack cE-c. Complete menu maximization gives the
same pointwise implementation, but full conditional optimality is not asserted.
The exact continuous integral in `structural_lower_split.py` gives
R=0.87645277076961753939... at d=.4999 and
R=0.87614302248883926131... at d=.49, both below the clean d=.5 construction.
The free square's sum density is 2d-z here, not 1-z.

These adverse comparisons reject only these specified complete paths.
They do not prove stationarity with respect to all split changes, rule out
simultaneous a,c,h changes, or establish that d=1/2 is necessary for revenue
optimality. In particular, a decrease below b/2 introduces Q reports whose
low coordinate exceeds d and needs a new two-item residual analysis.


## 9. Capping the constrained safe singleton restores its missing optimum

A further complete variant replaces a Q safe price B=C-k>A by A, leaving
scarce price A and bundle price C fixed. Use the same menu-maximizing joint
tie definition. The implementation is `structural_reserve_candidate.capped_mechanism`.
This is a separate increment to the specific uncapped reserve alternative;
it is not stacked onto another a,c,h candidate without re-integration.

The bundle-minus-safe scarce upgrade increases from k to C-A>=k. Hence Q/base
and E/Q contested-item restrictions become stronger. On QQ profiles a capped
safe singleton cannot have positive utility because all own coordinates are
at most A. A capped bundle against an uncapped safe still satisfies the old
bundle threshold rho>=k(y), contradicting the strict safe purchase y>h(rho).
Two positive bundles remain impossible because C>=opponent sum. All equalities
are covered by empty-at-zero and the feasible maximizing-pair rule. Thus the
cap is pointwise feasible and DSIC/IR on the full continuous domain.

For eta=B-A>0, the exact conditional revenue gain follows from
partial_B R(A,B,C)=(2-3B)(C-B):

R(A,A,C)-R(A,B,C) = (3/2)k*eta^2+(1/2)*eta^3 >0.

The formula integrates the entire conditional menu change, including its
single/bundle switching region. It is not a pointwise allocation comparison.

If a capped row has C=sum(w)>b0, the symmetric diagonal-hole certificate applies.
The priced bottom trace (x,0), x<1/2, and vertical trace (1/2,y), y<C-1/2, index
unchanged free-Q menus whose bundle price is strictly below C. The opposing own
Q report w has singleton utilities at most zero and buys that bundle strictly.
Candidate feasibility therefore supplies a matching bound over the full
randomized conditional class. This restores the actual full inner certificate
on these cap rows. If an extra h floor instead caused C>sum(w), this anchor
argument would require a new proof and is not asserted here.

For the explicit identity-h reserve candidate above, every cap row has C=sum(w):
C0(c+nu)<A+c verifies it uniformly. The exact region is

1/2<t<1/2+nu, A-q<rho<b-t,

in either physical orientation, for either bidder. Here eta=rho-(A-q).
Integrating all four label/orientation copies gives the exact further gain

Delta_cap = integral_(1/2)^(1/2+nu)
 [2(t-q)(1/2+nu-t)^3+(1/2)(1/2+nu-t)^4] dt
 = c*nu^4/2+nu^5/5 >0.

Its exact radical revenue and enclosure are in `structural_reserve_cap.json`.
The cap alone does not repair the separate literal a>A E-junction obstruction
in Section 6. Section 10 supplies the additional incentive-derived trace
argument and establishes full E conditional optimality for this reserve
alternative.


## 10. Incentives recover the missing E junction trace

The literal-capacity warning for a>A in Section 6 admits a stronger resolution.
Fix an actual E opponent w=(t,rho), A<t<T, rho<c. At **every** other report
(x,y) with A<x<t and 0<y<c, the opposing bidder w receives its high item
strictly from the E menu indexed by (x,y): its high singleton utility is t-x>0,
while its low value rho<c makes both the bundle and lottery inferior to that
high singleton and the safe singleton unprofitable. Therefore the residual
scarce capacity is zero on the entire open rectangle

(A,t) x (0,c).

Let (u,z) be any complete randomized DSIC/IR competitor under this actual
residual. For fixed y in (0,c), all selected horizontal allocations satisfy
z1(x,y)=0 on (A,t). Applying the two DSIC inequalities between any two such
reports proves u(x,y) is constant in x on that interval. Allocations in [0,1]^2
imply the coordinatewise one-Lipschitz bounds directly from DSIC. Taking y up
to c therefore proves u(x,c) is constant in x on (A,t). A selected subgradient
at an interior point (x,c), tested in both horizontal directions, must satisfy

z1(x,c)=0 for every A<x<t.

This conclusion uses the full pointwise DSIC constraints and continuity,
not an almost-everywhere extension of a sampled allocation. It holds even
when the actual residual capacity on the literal face y=c is one.

In the full E identity of `V4_6/research_log/inner_lottery_certificate.md`,
the old H2 hypothesis is used only to control the nonnegative weighted
allocation integral on (A,t) x {c}. Its weight is 3t(c+L/4). The just-proved
allocation trace is zero for every feasible competitor and for the candidate.
Hence this integral vanishes and is omitted from the upper constant. The
remaining volume/top/upper-line capacity terms, the convex right-trace slack,
the corner monotonicity slack, and the nonnegative IR sink are unchanged.
Candidate feasibility and the actual top hole give equality at the E menu.
This proves its **full randomized conditional optimality** for the reserve
candidate despite the vacant junction face. Individual interval endpoints
have zero line mass, while the mechanism still specifies their allocations.

For identity h, the actual top price at (x,1) is max(1/2,x+q)<t for x<t-q,
so the remaining H1 condition holds. With a changed h, an additional proof
that max(1/2,h(x))<t on the priced top interval is needed; for example a
monotone support ending at u<=A-q with h(u)<=A suffices. No generic h is
certified by the rectangle argument alone.

Thus the **capped identity-h reserve candidate** has full conditional
certificates for both bidders on Q and E. The uncapped candidate retains
its known profitable safe-price gap on some Q fibers. Section 6's warning
remains correct about directly transplanting a literal-capacity H2 bound,
but the stronger incentive-derived trace supplies its missing ingredient.
The E certificate produced this way is an upper bound for the actual inner
problem. It is not automatically a global supporting capacity-price measure
for arbitrary residual perturbations: the zero-line implication depends on
the open rectangle's actual zero capacities.
