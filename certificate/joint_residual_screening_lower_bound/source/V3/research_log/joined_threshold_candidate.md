# V3 joined thresholds: an explicit improvement forced by admissible variations

## Result and scope

This construction is deterministic, Borel, pointwise feasible, pointwise DSIC and normalized ex-post IR on the entire original report cube. Its revenue has the exact algebraic/logarithmic expression in Section 6 and the rational enclosure

    874648885321014009/10^18 <= R_V3 <= 874648885321014010/10^18.

It exceeds the strongest inherited feasible revenue L by more than 43898918177741/10^18. This is a new lower construction. No matching upper bound or unrestricted optimality is claimed. The formulas arise from revenue effects of complete, globally admissible changes; nevertheless the resulting stationarity covers only the specified contraction directions and opponent chamber.

## 1. Shared feasible base and inherited mechanism

Use a=159/250, b=91/100, s=1137/1000, c=b-a=137/500, d=s-a=501/1000, q=d-c=227/1000. The affine base selects the first maximum of total reported value minus cost, with ordered pairs of bidder item masks

    (0,0),(1,0),(2,0),(3,0),(0,1),(0,2),(0,3),(1,2),(2,1)

and respective costs 0,a,a,b,a,a,b,s,s. Masks 0,1,2,3 mean empty, item 1, item 2, bundle. These are all nine jointly feasible deterministic outcomes.

For opponent w, let H(w)=max(0,w1-a,w2-a,w1+w2-b). The base conditional prices are

    P1=H+min(a,s-w2), P2=H+min(a,s-w1), P12=H+b, P0=0.

Its selected own mask is the projection of the SAME global maximizer for both bidders. The inherited mechanism, completely reconstructed in certificate/baseline_mechanism.json and verifier/baseline_mechanism.py, adds its 20 common-fee rows, otherwise its 41 bundle-pivot rows, and then its eight selective rows, with explicit first-match boundary priority. Every inherited choice is an itemwise subset of this common base selection. Its exact revenue is

    L=83962078694672281756033/96000000000000000000000.

The base discount is globally strict: P1+P2-P12>=s-b=227/1000. If neither opponent coordinate exceeds d, use H>=0; if exactly one exceeds d, use H>=w_high-a; if both exceed d, use H>=w1+w2-b. These give lower bounds 2a-b, s-b, 2(s-b), respectively. All nonempty base prices are at least s-1=137/1000.

## 2. Complete replacement rule

For each bidder separately, set t=max(w1,w2), rho=min(w1,w2). Replace the inherited menu exactly on the closed chamber

    d <= t <= 1, 0 <= rho <= b-min(t,a).

There is a unique high opponent coordinate because t>=d and rho<=b-d<d. Denote by A the price of the item corresponding to that high coordinate, and by B the other singleton price. Put k=t-q and K=2/3+c^2. Define

    r0=b^2-K,
    r1=4c/3-2/9,
    t0=q+sqrt(r0),
    t1=q+sqrt(r1),
    t2=2/3,
    t3=(1/2-c+3q^2/4)/(3q/2)=1058587/1362000.

The four transitions obey d<t0<t1<a<t2<t3<1. The replacement menu is:

| Opponent high value | A | B | C (bundle) |
|---|---|---|---|
| d<=t<=t0 | a | b-k | b |
| t0<t<=t1 | sqrt(K+k^2)-c | sqrt(K+k^2)-k | sqrt(K+k^2) |
| t1<t<=t2 | 2/3 | 5/6-k+3k^2/4 | 5/6+3k^2/4 |
| t2<t<=t3 | t | 1/2+q+3q^2/4-3qt/2 | 1/2+3q^2/4+(1-3q/2)t |
| t3<t<=1 | t | d | t+c |

The empty option costs zero. All adjacent formulas agree exactly, so assigning endpoints to either adjacent branch gives the same menu. The affine base pivot t=a lies strictly inside one quadratic branch and creates no price kink. C may exceed 1; that is compatible with DSIC, feasibility and the menu-area formula.

Outside the specified chamber, keep the inherited menu. At its boundary use the closed chamber above, even where the old first-match row priority differed. This is an explicit rule on every real report, including algebraic transition reports.

For both bidders compute the SAME base outcome first. At the final menu:

1. If maximal utility is zero, choose empty.
2. If maximal utility is positive and the bidder's projected base mask maximizes, retain it.
3. Otherwise select the smallest mask among maximizing itemwise subsets of that projected base mask.

Charge its final menu price. This gives the full allocation/payment mechanism. The mathematical definition covers all real reports. joined_threshold.py implements exact evaluation for rational reports using quadratic-field arithmetic, rather than claiming a numerical test of every real report.

## 3. Pointwise admissibility proof

For a discounted menu 0,A0,B0,C0 with C0<=A0+B0, any price increments

    alpha>=0, beta>=0, gamma>=max(alpha,beta)

admit a maximizing subset of ANY originally selected mask. Empty stays optimal when it was selected. If singleton 1 was selected, then v2<=C0-A0<=B0; the other singleton cannot have positive utility after the change, and the bundle's utility relative to singleton 1 decreases by gamma-alpha>=0. Thus a new maximizer exists among empty and singleton 1. The other singleton is symmetric. An old bundle contains all four possible new choices. At positive ties select a maximizing subset; at zero choose empty. This proves containment without discarding exceptional reports.

Every replacement above is obtained from the base by a common nonnegative fee f and a nonnegative low-item surcharge delta: increments are (f,f+delta,f+delta) in the aligned A,B,C coordinates.

- Before t0: f=delta=0.
- Square-root branch: f=sqrt(K+k^2)-b, delta=0.
- Quadratic branch with t<=a: f=2/3-a, delta=1/6-c+3k^2/4.
- Quadratic branch with t>=a: f=2/3-t, same delta.
- Affine branch: f=0, delta=1/2-c+3q^2/4-3qt/2.
- After t3: f=delta=0.

Their nonnegativity follows from the transition definitions. Outside the replacement chamber the inherited rule is also a subset of the SAME base. Therefore both bidders' new masks are jointly feasible at every profile. This is why lowering some inherited common fees is safe here: containment is proved afresh relative to a common feasible base.

Each final price menu depends only on the opponent's report, and the selected mask maximizes reported utility. The taxation inequality proves DSIC against every own misreport. Empty gives IR. Strictly positive nonempty prices imply zero allocation and payment at zero own type, hence normalization. Prices and selections are Borel; finite masks with explicit priority supply measurable choices. IR and nonnegative prices bound each charged payment between 0 and 2, giving integrability. No finite-grid or almost-everywhere argument is needed for these facts.

## 4. Revenue equations that generated the branches

For 0<A,B<1 and max(A,B)<C<A+B, conditional revenue is

    G(A,B,C)=A(1-A)(C-A)+B(1-B)(C-B)
             +C[(1-C+B)(1-C+A)-(A+B-C)^2/2].

The selected areas are complete menu cells. The formula remains valid with C>1: the relevant requirements are A,B<1 and the discount inequalities, not C<=1. At t=1 take the continuous limiting formula; this endpoint has zero revenue measure.

Its gradient is

    G_A=(C-A)(2-3A), G_B=(C-B)(2-3B),
    G_C=1-4C+2(A+B)+(3/2)C^2-(3/2)(A^2+B^2).

The globally admissible contraction cone has four extreme directions

    (0,0,1), (1,0,1), (0,1,1), (1,1,1).

At any unrestricted optimum with such a conditional menu, the corresponding four integrated directional revenues must be nonpositive for almost every opponent. This is a necessary condition for the full problem, conditional only on the candidate having this menu topology. It is not pointwise virtual-value maximization.

A common added fee e has exact revenue effect beta*e-3C*e^2/2-e^3/2, where beta=G_A+G_B+G_C. A low-item surcharge z has exact effect Gamma*z-z^2, where Gamma=G_B+G_C. These formulas integrate all reports that the changed menu forces to move together.

In the zero-pivot chamber, C-A=c and C-B=k. With delta inactive, beta=0 gives C=sqrt(K+k^2). It begins at f=0, namely C=b. It reaches A=2/3 exactly at k^2=r1. At that point the low-item direction becomes neutral and then active.

When f and delta allow two-sided variation, beta=Gamma=0 implies G_A=0, hence A=2/3. Solving Gamma=0 gives C=5/6+3k^2/4, B=C-k. The common fee reaches zero at t=2/3. Thereafter A=t is pinned by that active inequality, and Gamma=0 gives the affine branch. The low-item surcharge reaches zero at t=t3, returning to the base.

All four contraction-cone derivatives are nonpositive for d<=t<1, hence almost everywhere in the replacement chamber. At t=1 the polynomial continuation need not equal a right derivative after crossing the A=1 menu topology; only pointwise feasibility and the continuous revenue formula are used there. On the square-root branch beta=0 with G_A,G_B>=0. On the quadratic branch G_A=Gamma=0, G_B>0. On the affine branch G_A<0, Gamma=0, G_B>0. After t3 both G_A<=0 and Gamma<=0. Before t0 beta<=0 with G_A,G_B>=0. These are verified algebraically, not inferred from a floating stationary point. They do not rule out other globally admissible allocation changes or new lotteries.

## 5. Junction and representation implications

The t0 junction is zero common fee; the t1 junction is zero selective surcharge and A=2/3; t2 is zero common fee; t3 is zero selective surcharge. Adjacent prices agree exactly. No new outcome was introduced merely to fit a numerical partition. Each added branch has a named binding inequality or integrated revenue balance.

A nonlinear price here does not imply that both bidders' allocations change across its surface. For example, in the square-root branch there are open one-item entry panels where the other bidder remains empty. Then the bilateral rigidity hypotheses for two nonzero row jumps are absent. By contrast, any panel where both rows change must still satisfy the V2 bilateral normal and junction tests. CLASS-1 supplies only a local conditional affine-rigidity lemma under explicit exposure hypotheses; it is not a classification of this auction.

The replacement has four deterministic allocations per conditional menu and nine possible jointly feasible deterministic outcomes. This finite range is a property of this candidate, not a restriction justified for the unrestricted optimizer. No finite type grid is used.

## 6. Exact revenue characterization

Let G_Z be the sum of the inherited ten Z-row gains and G_SI the inherited ten S-row plus eight selective-row gains. They are explicitly rational in certificate/joined_threshold.json. Let G_newS be the exact rational integral of the S replacement, computed independently of any optimizer:

    G_newS=4c integral_(a,t3) [G(new A(t),new B(t),new C(t))-G(t,d,t+c)] dt.

Set k0=sqrt(r0), k1=sqrt(r1), C0=b, C1=c+2/3, h=b-q, and

    J(k)=k(2k^2+5K)sqrt(k^2+K)/8 + 3K^2 log(k+sqrt(k^2+K))/8.

On the common-fee optimum, direct substitution gives

    G=(K+k^2)^(3/2)-k^2-k^3-c^2-c^3.

Consequently the square-root branch's improvement over its base is

    G_root=4{h[J(k1)-J(k0)]-(C1^5-C0^5)/5
             + integral_(k0,k1) (h-k)[-3b(k^2+K)/2+b^3/2] dk}.

For the quadratic branch within Z, write C(t)=5/6+3(t-q)^2/4 and

    Z(t)=4(b-t)[G(2/3,C(t)-(t-q),C(t))-G(a,b-(t-q),b)].

This is an explicit rational polynomial (its coefficient list is in the certificate). The exact final revenue is

    R_V3=L-G_Z-G_SI+G_newS+G_root+integral_(q+k1,a) Z(t) dt.

All remaining integrals in this display are integrals of explicitly specified rational polynomials at rational or quadratic-algebraic endpoints. This is an exact finite expression in rational numbers, two square roots and one logarithm of an explicit positive algebraic ratio. It is not defined by its decimal enclosure.

The factor 4 counts two bidders and two item orientations. The remaining opponent width is b-t in Z and c in S. All changed boundaries have measure zero for revenue but have complete pointwise selection rules above.

joined_threshold.py proves the enclosure using rational square-root bounds and the atanh series for the logarithm, with an explicit positive remainder bound. stationary_s.py independently records the rational S-only intermediate candidate and its strict exact gain. That intermediate candidate is retained as a checkable milestone, not reported as the best V3 mechanism.

## 7. Remaining obstruction

The inherited unrestricted upper remains 3715139591287203/4194304000000000, leaving a gap between .011109417197640574 and .011109417197640575. A candidate-specific full weak-dual support system is derived separately. No feasible multiplier system matching R_V3 has been produced. Four-ray stationarity in this chamber, a local classification lemma, and the existence of a full weak-dual formula each leave this obligation open. The unchanged opponent regions also have not been proved stationary under all admissible changes. This candidate must not be labeled optimal.

