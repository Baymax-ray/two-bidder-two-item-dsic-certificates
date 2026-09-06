# Final cross-audit of the selected all-real mechanism

This audit found no blocking issue in the selected mechanism's complete
pointwise feasibility, DSIC, expected-utility IR, or measurability, or in
the claimed unrestricted randomized conditional optimality on Q, E and W.
It is a mathematical cross-check of the written arguments and actual
implementation, supplemented by the read-only exact replays below. It is
not a formal proof-assistant verification or a common global auction dual.

The inspected current sources are `verifier/refined_candidate.py`,
`research_log/refined_structure_audit.md`,
`research_log/residual_wing_screening.md`, and `REPORT.md`. For the Q and E
identities I also read the preserved V4.6 notes
`inner_diagonal_capacity.md` and `inner_lottery_certificate.md`; their old
parameter and residual hypotheses were checked against the new arguments,
not assumed to survive unchanged. The mechanism and existing artifacts
were not edited.

## 1. The jump, plateau and selection rule

The source uses the fee on the closed interval [c,u], with its positive
right-hand value at c. It implements every branch of the displayed
generalized inverse. For t>d, its exact properties are

\[
x<k(t)\implies h(x)<t,\qquad
x\ge k(t)\implies h(x)\ge t.
\]

On the inverse plateau, k=c and t can be strictly less than h(c). None
of the compatibility arguments audited below needs the false identity
h(k)=t. The jump endpoints, t=d, t=h(c), and t=h(u), are assigned
consistently. At t=d the mechanism uses free Q; at t=h(c) it still uses
the plateau, and at t=h(u) the two inverse formulas coincide.

The source first retains empty alone whenever maximum utility is zero;
otherwise it retains all menu maximizers and selects a jointly feasible
pair. This is compatible with taxation DSIC: with the opponent fixed,
every selected allocation/payment is an option of the same complete menu,
and every truthful selection attains its maximum utility. Dependence of
tie selection on the reported pair does not change that argument.

The common affine base has a jointly feasible maximizing pair. Raising
safe and bundle payments equally admits a maximizing subset of each old
base maximizer: an old safe winner cannot become a positive scarce winner,
because the old strict bundle discount gives
P_bundle-P_safe<P_scarce. An old scarce or empty option stays maximizing;
an old bundle contains every new allocation. Applying this to an old
jointly feasible pair establishes existence for base/base, including ties.
The remaining region comparisons exclude conflicting positive options
directly. Equality at a conflicting ownership threshold leaves the other
bidder at zero utility and invokes the explicit empty rule.

All formulas, comparisons and the finite selection are Borel. The source
contains empty in every menu and has nonnegative prices; a chosen option
therefore has nonnegative expected utility and payment at most 2.
Marginal feasibility can be implemented samplewise for each item using
disjoint intervals under a uniform seed. This does not assert universal
truthfulness, or IR separately for each realized lottery outcome.

## 2. Compatibility with the increased reserve

The uniform slack for the extra Q floor is 37/5000000. On the fee
support the proof controls the maximum adverse value at rho=b-A and
k=A-q; its derivative bound has the correct positive sign. Off that
support, k<=t-q implies k+h(rho)<=t+rho. Thus retaining the additional
floor in the actual menu is harmless even though C0(k) can exceed 1.
The argument does not silently use C<1.

For Q/base with the base buyer's low report coordinate at most d, its
contested singleton price is at least max(x,x+y-c). A positive Q bundle
has x+y>=C0(k)>=t+c. The last inequality follows from

\[
C_0(k)-k-d\ge g(k),\qquad t\le h(k),
\]

and remains valid on the plateau. When the other coordinate exceeds d,
any potentially conflicting contested coordinate is the low coordinate,
so the fee is charged to precisely the needed singleton and its price is
at least h(x). A Q bundle requires x>=C-B>=k, including the capped case.
These inequalities exclude conflict at all reports.

For Q/Q, capped singleton prices A rule out positive singleton utility
for Q types. An uncapped safe winner has value strictly above B and hence
above h(rho); a conflicting bundle requires rho>=k of that value,
contradicting the inverse implication. Two positive bundles contradict
their respective C>=sum(opponent) inequalities. If a menu is free Q,
its Q buyer has no positive singleton option; the opposite low-maximum
buyer cannot buy an uncapped safe singleton above d, so the bundle test
covers this case as well.

For E/Q the old shortcut t+c>b would be false when A<t<a. The new
proof correctly replaces it. Every Q type's E-lottery utility is at most

\[
A-t+\beta(a-A).
\]

The ratio (t-A)/beta=t-A+2 delta(t)/3 is strictly increasing for
A<t<T and has infimum q^2/2=a-A. Therefore the lottery is strictly
excluded even at the selected reserve allowance equality. The analogous
bundle comparison uses delta(A)=3q^2/4>q^2/2. Only the safe item can
remain positive. In the reverse Q menu the scarce-upgrade threshold is
at least c, exceeding the E type's low coordinate. This handles the new
reserve chamber, not just the earlier a=A special case.

The E/base comparisons exclude empty and conflicting singleton choices
by complete-menu dominance. In E/E of opposite orientation, the lottery
purchase region requires scarce value at least j=1-t/2>d>c; it is not
necessary, and would be false, to require that value to exceed A.
Same-orientation E pairs reduce to the single higher high-valued bidder,
with empty at equality. The source's excluded E faces fall into Q or
base and are covered by those comparisons.

## 3. The Q and E conditional certificates

For uncapped Q the inherited top coefficient is nonpositive below A
because B<=A; its anchored cumulative density is nonnegative, and its
mass is 2(C-C0)>=0. The required order is k<d<A, which the new
parameters satisfy. The earlier numerical upper bound C<=91/100 is
not used by these identities or signs.

The actual top trace is strictly occupied below k: against own report
(x,1), the opposite bidder's contested price is max(d,h(x))<t.
When the anchor mass is positive, C is the opponent sum and exceeds b0.
On the bottom and vertical anchor intervals the reverse free-Q menu
sells the opposite bidder a bundle strictly, because its bundle price
is below C and its singleton values are at most A. The capped case
uses the symmetric (A,A,C) certificate; its top density vanishes below
C-A, so a new physical hole below that larger threshold is not required.
Endpoints of the priced intervals have zero line measure; allocations
there are still specified by the complete pointwise mechanism.

For E, the actual face (x,c), A<x<t, can be physically vacant when
a>A. The repair in the structural note is essential and valid. In the
open rectangle A<x<t, 0<y<c, the reverse menu is E and the opposite
bidder strictly buys the contested singleton. Every competing complete
DSIC mechanism under this actual residual consequently has first
allocation zero there. Its two horizontal incentive inequalities force
utility to be constant in x for each y<c. Bounded allocations make
utility coordinatewise Lipschitz, so that constancy extends to y=c.
Subgradient inequalities to points on both sides of an interior x then
force every selected first allocation at (x,c) to equal zero, including
exceptional subgradients.

I checked the inherited lottery certificate's exact identity: the only
use of the missing H2 physical hole is its priced line segment A<x<t,
y=c. On the repaired feasible class, both the candidate and every
competitor allocate zero to that segment by the preceding IC argument.
Deleting it from both pairings preserves the identity and all other
nonnegative slacks. The actual H1 top occupation survives because the
fee support ends below A-q. Candidate saturation holds on the remaining
volume and singular supports. Thus the repaired result is full
randomized conditional optimality for the fixed actual residual.

This deletion does not produce a support valid for arbitrary new
residuals: the proof of the vanished line allocation used the particular
occupied open rectangle. The structural note and REPORT retain this
distinction correctly.

## 4. Strict occupancy and the W screening identity

For W, t>=1-q and z>=1+u imply rho>=u>c. Its menu is an uncharged
base menu; after suppressing an unaffordable scarce option it has safe
price p=min(rho+q,1) and bundle price z=k+p.

I checked occupation using strict dominance rather than a favorable
tie choice. In the strip x<k when p<1, an uncharged base singleton
has price at most max(a,x+q)<t. When it is charged, its price is bounded
by max(a+jump,u+q)<1-q<=t. The bundle upgrade over the other singleton
is max(c,x-q), or c+g(x) in the charged low-coordinate case, and is
strictly below t. Thus neither empty nor an allocation omitting the
contested item can maximize. The same conclusion holds on reverse Q
and E: their first singleton and relevant upgrade thresholds are
strictly below the W high value; a reverse E lottery that omits part
of the contested safe item is strictly dominated because that value
exceeds its lottery/bundle junction Y<d.

On the interior no-sale region y<p, x+y<z, the uncharged base bundle
price max(b,x+c,y+c,x+y) is strictly below z. For a charged base report,
the price is max(b,x+y)+g(min(x,y)), bounded by
max(b+jump,max(x,y)+u)<1+u<=z. Bundle utility is positive and its
upgrade over the other singleton is strictly below t. The reverse Q/E
comparisons above also hold there. Therefore every selected maximizer
contains the contested item; no favorable selection at a tie is needed.

On the left edge x=0,y<p, the opposite bidder strictly prefers its
bundle. In base, the two bundle upgrades are c and max(c,y-q), both
strictly below the respective W values. In constrained Q the low
upgrade is k(y)<=y-q<rho; the other is C0-A<t. In E, the safe value
t>Y rules out the lottery and the low upgrade y-q<rho rules out the
safe-only option. These are strict throughout the required edge.

When p=1, the strip x<k=z-1 lies in the interior no-sale set for y<1.
At y=1, the bundle is still positive and the contested upgrade is
strictly below t. The left-edge proof also survives y<1 because
y-q<1-q<=rho. Thus this limiting chamber is not omitted. Other null
boundaries are handled by utility continuity and the complete tie rule;
the proof does not assume literal occupation at every such boundary.

For an arbitrary competing utility, the stated holes make it constant
on the no-sale region and horizontally constant on x<k. Averaging the
two exact coordinate envelope identities gives

\[
R+u(0,0)=
\int_G\left({3x-1\over2}\alpha_1+{3y-1\over2}\alpha_2\right)
+\int_H{(3k+1)y-k-1\over2k}\alpha_2.
\]

The strip trace substitution is justified by the horizontal constancy;
the no-sale allocation vanishes almost everywhere. The coefficients are
nonnegative because k>=1/3, z>=4/3 and
(3k+1)p-k-1>=0. The actual W parameters satisfy the last condition
with the displayed positive margin 18601/5000000 for p<1, and with
value 2k for p=1. The candidate saturates all positively priced
marginals. This proves the full randomized fixed-residual upper bound,
without requiring both capacities to vanish in the no-sale interior.
The exact W area 438867/2500000 and its disjointness from Q/E check out.

## 5. Read-only replay and scope review

Executed with assertions enabled and bytecode writing disabled:

- `python -B -X utf8 verifier/refined_structure_audit.py`:
  `REFINED_STRUCTURE_FULL_CONTINUUM_AUDIT_PASS`, 2,209 independently
  reconstructed profile pairs and 188 source-profile comparisons.
- `python -B -X utf8 verifier/residual_wing_screening.py`:
  `RESIDUAL_WING_SCREENING_EXACT_PASS`, 168 continuous-menu identity
  checks, 12,220 actual-residual profile checks, exact W area confirmed.

These finite replays support the source/proof cross-check; their counts
are not themselves proofs over the continuum. No new revenue computation
was needed here; the separate independent continuum revenue audit remains
the revenue evidence.

REPORT correctly states a strict lower-bound improvement and an actual
positive-volume ownership change, while leaving global optimality and a
matching unrestricted auction upper bound open. Its 64.1627% coverage is
the opponent area of conditionally solved fibers, not a fraction of the
auction revenue gap closed. Alternative fixed-constant examples are not
added to the final candidate's revenue. No blocking mathematical or scope
issue was found in this final cross-audit.
