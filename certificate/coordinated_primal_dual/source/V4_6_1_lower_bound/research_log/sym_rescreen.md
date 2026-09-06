# Bidder symmetrization followed by full screening on G

This experiment starts from the **strongest complete V4.6 mechanism**, including
its exact corner release, not from a grid or a deterministic approximation.
It produces a strict feasible gain and solves every changed conditional problem
over all randomized DSIC/IR competitors. Its gain is small and is dominated by
the corresponding direct asymmetric replacement; it is independent structural
evidence, not the branch's strongest lower bound.

Write M for `V4_6/verifier/price_joint_reallocation.mechanism`, and M^swap for
its bidder-label swap. Define S=(M+M^swap)/2 by a report-independent fair coin.
Expected allocations, payments and truthful utilities are arithmetic means.
Thus S is jointly measurable, pointwise feasible, DSIC and IR on every real
report; inherited exceptional choices are retained in each coin outcome.

Put A=2/3, a=159/250, b=91/100, q=113/500, and
b0=(4-sqrt(2))/3. Let

G={w: max(w)<=1/2, b0<w1+w2<b}.

For opponents w in G, replace **only bidder 1's entire conditional menu** by
empty, item 1, item 2, bundle at prices (0,A,A,z), z=w1+w2, in that priority.
Retain bidder 2 exactly as in S, including every exceptional report and tie.
Outside G retain S. This is the complete mechanism implemented in
`sym_rescreen.py`; the inequalities defining G include its max=1/2 face and
exclude both sum faces.

## Exact three-level residual geometry

Fix w in G and write z=sum(w). For an arbitrary report v of the other bidder,
define

L_z={v: max(v)<=1/2, sum(v)<z},

K_z={v in Q: C(v)<z},
Q={max(v)<=A, sum(v)<=b}, and

C(v)=max(b0,sum(v)) when max(v)<=1/2;
C(v)=max(5/6+3(max(v)-q)^2/4,sum(v)) otherwise.

In the original V4.6 mechanism, a bidder in position 1 with own report w
receives both items precisely on L_z and nothing elsewhere. A bidder in
position 2 with own report w receives both items precisely on K_z and nothing
elsewhere. To see this, all its singleton prices are at least 1/2; zero utility
selects empty. The retained outside-Q bundle prices are at least b>z. In Eplus,
the lottery cannot win for a report with both coordinates at most 1/2 and sum
less than b. The final corner-cut lottery also cannot win there: its scarce
coordinate threshold exceeds 1/2. The entry fee cannot create an allocation.
Inside Q the full coupled bundle prices are exactly C(v). The F and G bidder-1
splices give exactly the first set L_z. Equality C(v)=z or sum(v)=z gives empty.

Consequently L_z is a subset of K_z and bidder 1's symmetrized residual is

r(v)=(0,0) on L_z;
r(v)=(1/2,1/2) on K_z minus L_z;
r(v)=(1,1) elsewhere.

This is a genuinely fractional residual pattern. It is not inferred from
averaging a numerical optimum. If v is in K_z with max(v)>1/2, then

max(v)<q+sqrt(23)/15<a<A,

because C(v)<z<b. Also sum(v)<z throughout K_z. The replacement (A,A,z)
therefore allocates nothing anywhere in K_z, including the boundary where
it meets L_z. Its nonzero allocations occur only where both residual
capacities are one. This proves pointwise joint feasibility globally.

Each replacement is a complete finite menu with a fixed own-report-independent
priority. Selecting its utility maximizer gives DSIC/IR for bidder 1 for every
fixed opponent. Bidder 2 is unchanged, so retains DSIC/IR. All report regions,
prices, allocations and choices are Borel. Per-item random realization of the
joint feasible marginals gives an actual allocation with no double assignment.

## Full randomized conditional optimum

The V4.6 diagonal-capacity theorem applies with bundle parameter z. Its two
required zero-capacity traces are

r1(x,0)=0 for 0<x<1/2;
r2(1/2,y)=0 for 0<y<z-1/2.

Both lie in L_z, hence have zero residual here. Candidate feasibility was
proved above. Equations (6)--(7) of
`V4_6/research_log/inner_diagonal_capacity.md` therefore supply a nonnegative
capacity-price measure bounding every randomized, complete DSIC/IR competitor,
with equality at the replacement. In particular, no fixed finite menu is
assumed for competitors. The exact value is

V(z)=z^3/2-2z^2+7z/3-8/27.

This certifies the **full inner optimum on every G fiber of this symmetrized
residual**. It does not certify the unchanged fibers or the auction optimum.

## Exact revenue and comparison

Let R(p,p,z) be the ordinary continuous four-option menu revenue. For w in G,
the original position-1 and position-2 conditional menus have prices
(a,a,z) and (A,A,z), respectively. Thus S earns their mean conditionally.
With h=A-a=23/750, exact polynomial expansion gives

R(A,A,z)-R(a,a,z)=h^2(3z-2+2h)>0.

The total gain is exactly

Delta_sym = (1/2) integral_(b0)^b (1-z)h^2(3z-2+2h) dz
 = 30892611299/151875000000000 - (180389/1265625000)sqrt(2)
 = 0.0000018408748157996436... >0.

The cross-section 1-z is the exact length in the square [0,1/2]^2; no grid,
quadrature, or samples enter this integral. Since S has exactly R_V4.6 revenue,
the experiment has exact revenue R_V4.6+Delta_sym. The standalone verifier
uses rational polynomial antiderivatives and an integer-square-root enclosure.

For example, at own report (13/20,1/10) and opponent (11/25,11/25),
S assigns bidder 1 half of item 1. The new conditional optimum chooses empty.
Revenue improvement comes from the complete menu response across all reports,
not a pointwise virtual-revenue maximization at this witness.

A direct position-1 replacement against the original M is also feasible on G,
because it vanishes on K_z, and gains twice Delta_sym. The successful symmetrized
experiment therefore does **not** prove that fractional residuals yield a family
unavailable to direct asymmetric correction. It confirms strict conditional
suboptimality of the symmetrized selection and exactly identifies its optimal
replacement on these fibers. Further fractional-residual discoveries remain open.
