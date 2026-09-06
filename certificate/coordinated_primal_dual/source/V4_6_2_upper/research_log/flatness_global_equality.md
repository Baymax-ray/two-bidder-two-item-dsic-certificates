# Global equality constraints for the V4.6.2 upper branch

This component derives reusable whole-auction identities and two rigorous
obstructions to equality in particular certificate architectures. It does
not prove that the V4.6 final mechanism is optimal or suboptimal, and does
not report a new numerical auction upper bound. The unchanged V4.6 source
is the complete mechanism in `V4_6/verifier/price_joint_reallocation.py`.

## 1. A conditional support is a global inequality

Write the profile as `(w,v)`, with bidder 1 type w and bidder 2 type v.
Suppose, measurably in w, a finite nonnegative capacity measure pi_w and
constant c_w satisfy

    R_2(M_2 | w) <= c_w + <pi_w, x_2(.,w)>

for every full randomized DSIC/IR conditional mechanism. In particular,
`V_w(r) <= c_w + <pi_w,r>` for every residual r. A support discovered at
one residual does not require that residual to remain in place. For the
V4.6 lottery support, c_w=0 and the exact noncapacity slack is
`T_g + lambda M_a + S_u`.

A support must be supplied on every opponent fiber used by this formula.
On fibers outside a selected supported region, one may use the constant
full-capacity single-buyer bound instead, with pi_w=0. Assume the kernel
and constants are jointly measurable and integrable. Assemble P on the
full profile space, in physical item coordinates, by integrating pi_w
against Lebesgue measure dw, and put C=int c_w dw. Tonelli applies to
capacity and nonnegative slack terms. Then

    R_2 <= C + <P,x_2>,
    OPT <= C + <P,1> + H_1(P),
    H_1(P) = sup_{M_1 full DSIC/IR} {R_1 - <P,x_1>}.

The first bidder in H_1 has only its own marginal box constraint
`0<=x_1j<=1`; joint capacities have already been priced. Supports for the
same fiber may be mixed using fixed nonnegative weights summing to one.
Their constants and measures mix with those weights. Adding several
unweighted full-revenue bounds would double count the revenue.

No assumption that H_1 attains its supremum is needed for weak duality.
No measurable selector of conditional optimizers is presumed: H_1 is
defined on complete jointly measurable mechanisms. A separately proved
pointwise upper for its conditional problems can always be integrated to
upper-bound H_1 without an interchange-of-supremum theorem.

## 2. Exactly four gap categories, without counting IC twice

Let a flow system upper-bound the charged problem. For bidder 1, write

    D_1(t,r;v)=u_1(t,v)-u_1(r,v)-(t-r).x_1(r,v) >= 0.

Let nonnegative incentive flow Lambda and sink nu satisfy
`out(Lambda)-in(Lambda)+nu = Lebesgue(profile)`. Opponent reports do not
change along an edge. Assume all displayed integrals are defined. Set

    C_1 = w Lebesgue + incoming (r-t) Lambda,
    Q_1 = C_1 - P.

These are vector signed measures. Take a finite positive measure eta that
dominates their total variations, and let q_1j=dQ_1j/deta. The unrestricted
allocation support is

    Hbar_1 = int sum_j max(0,q_1j) deta.

The sign convention is the same as the independently replayed phase-2
`analysis/cycles.md`: adding IC and IR slacks to revenue gives the
allocation coefficient C_1. Define U=C+<P,1>+Hbar_1. For any complete
feasible mechanism, exactly

    U-(R_1+R_2) = S_screen + S_capacity + S_virtual + S_weighted_IC,

where

    S_screen = C + <P,x_2> - R_2,
    S_capacity = <P,1-x_1-x_2>,
    S_virtual = int sum_j [max(0,q_1j)-q_1j*x_1j] deta,
    S_weighted_IC = int D_1 dLambda + int u_1 dnu.

All four terms are nonnegative. IR is included in the fourth category as
the IC constraint for a fixed outside option `(allocation,payment)=(0,0)`.
Its sink subterm is still reported explicitly, so a positive-utility type
cannot silently absorb sink flow. The local trace, monotonicity, and IR
terms used to prove S_screen are internal to that category. They must not
be added again to S_weighted_IC, which here belongs only to bidder 1.

If H_1 is evaluated exactly but no flow representation is supplied, the
same exact identity has only three terms: S_screen, S_capacity, and the
charged-screening regret `H_1-(R_1-<P,x_1>)`. Splitting that last term into
virtual and weighted-IC slack requires an actual charged dual; it cannot
be inferred from a numerical optimum.

For a conventional common two-bidder flow system, let eta_j dominate both
allocation coefficients and zero. Its exact gap is instead

    sum_i int D_i dLambda_i + sum_i int u_i dnu_i
    + sum_j int eta_j*(1-x_1j-x_2j)
    + sum_ij int (eta_j-C_ij)*x_ij.

In that architecture there is no separately peeled conditional-screening
term; set that category to zero. Inserting a second copy of a local
certificate slack into this identity would be double counting.

## 3. Opponent-null singular charges cannot be common at equality

**Null-opponent lemma.** Let P be any finite nonnegative capacity measure.
Let N be a Lebesgue-null Borel set of bidder 2 reports. For any complete
bidder-1 mechanism M_1, replace its entire menu by empty when v belongs
to N, retaining its complete menu elsewhere. This remains pointwise DSIC,
IR, and jointly measurable, since opponent reports are fixed along every
bidder-1 deviation. Its expected bidder-1 revenue is unchanged and its
charged cost falls by `<P restricted to v in N, x_1>`. Consequently

    H_1(P) - [R_1(M_1)-<P,x_1>]
      >= <P restricted to v in N, x_1>.

Thus a common measure at equality cannot charge positive incumbent
allocation mass on an opponent-null set for either charged bidder. The
statement concerns the projection of the consumed measure, not whether
P is singular in the four-dimensional profile space. A graph can have
absolutely continuous projections onto both opponent spaces and is not
excluded by this lemma.

Replacing the incumbent by the revenue-equivalent empty-menu patch does
not remove the total gap: where bidder 2 still takes zero, the same mass
moves from charged-screening regret into capacity slack. Exceptional-report
repair therefore cannot be counted as a global certificate improvement.

The lottery support has physical-item-1 prices on `v_2=1` and `v_2=c`.
When it supports bidder 2 and is assembled over w, both are opponent-null
sets for bidder 1. On an untouched lottery fiber `(t,rho)`, define as in
V4.6

    A=2/3, q=113/500, c=137/500, k=t-q,
    alpha=3t-2,
    delta=q+3q^2/4-3qt/2+alpha^2/16,
    B=1/2+delta, L=delta+alpha/2,
    lambda=alpha*(c+L/4).

The incumbent bidder 1 consumes all capacity on the top line for 0<x<k,
and on the corner line for A<x<t. The total singular charge on just
these occupied pieces is

    top: integral_0^k (2-3B)*x dx = (2-3B)*k^2/2,
    corner: integral_A^t 3t*(c+L/4) dx = t*lambda.

Choose the untouched opponent rectangle

    3/4 < t < 4/5,       0 < rho < 1/5,

in one physical orientation. It is inside Eplus and disjoint from the
final corner-release exclusion. Integrating only these pieces gives the
exact charged-screening regret lower bound

    H_1(P)-[R_1-<P,x_1>] >= 455595915031/300000000000000
                              > 0.0015186.

This lower bound applies when the old lottery support is used with unit
weight on this rectangle and other added prices are nonnegative. If its
weight is theta(w), integrate the displayed fiber mass against theta.
It does not bound the regret of every possible alternative support.
It does prove that this particular locally tight measure cannot itself
be a matching common certificate for the incumbent mechanism. The bound
holds even if H_1 is solved exactly and no finite dual basis is imposed.

## 4. A family of equally tight local measures, all with the same obstacle

The corner monotonicity step has genuine freedom. For any fixed
`b in [A,t)`, a nondecreasing function a satisfies

    integral_0^t a(x) dx <= t/(t-b) * integral_b^t a(x) dx.

Replacing the old terminal average `[A,t]` by `[b,t]` therefore gives
another valid support: its corner price is `lambda*t/(t-b)` on (b,t),
zero below b, and lambda on (t,1). The candidate is still locally tight
because its scarce allocation and residual are both zero on (b,t).
Every choice charges the opposing bidder exactly lambda*t on that
occupied segment. Convex mixtures of these supports keep the same mass.

More generally, any probability measure sigma on [0,t] whose tails
satisfy `sigma([s,t]) >= (t-s)/t` dominates the uniform average for all
nondecreasing a. To retain candidate tightness it must also put its
charged mass on the actually occupied portion and handle atoms at ties
correctly. Terminal uniform measures avoid all atomic tie issues.

This supplies alternative supporting measures for one conditional
optimum, and rules out an entire natural redistribution direction as a
way to make the support common. It does not rule out replacing the
corner transport itself by a different all-report IC transport, changing
its affine intercept, or using measures with different opponent
projections. A singular graph with nonnull opponent projections is a
concrete representation left open.

## 5. The actual lottery forces a positive-volume zero virtual plateau

The final V4.6 mechanism is unchanged on the open box

    w_1 in (3/4,19/25),  w_2 in (1/20,1/10),
    v_1 in (17/20,19/20), v_2 in (3/10,7/20).

Its volume is 1/400000. Here bidder 2 receives `(1,beta(w_1))`, bidder 1
is empty, `4/5<beta<19/20`, and `u_2>9/100`. To verify the whole box:
delta decreases, beta increases, and L increases in this t interval;
`c<3/10<7/20<c+L(3/4)` puts every y strictly between the lottery's lower
and upper interfaces; x>t gives strict positive utility. The opposing
report has high coordinate above T, low value below 1/2, and the retained
menu cannot sell either singleton or bundle to w. The box misses F, G,
the fee rectangle S, and the price-cut rectangle W. Finite exact corner
checks in the verifier only supplement these inequalities.

For any matching common flow dual with ordinary density coefficients,
capacity complementary slackness on the safe item gives eta_2=0,
because a fraction 1-beta remains unallocated. Allocation slack then
gives C_22=0, because beta>0. Thus the required plateau is

    C_22(w,v)=eta_2(w,v)=0 almost everywhere on the whole box,
    C_12(w,v)<=0 there.

It is not merely a tie between bidders on a purchase boundary. Sink
complementarity also gives nu_2(box)=0, because u_2>9/100 throughout.
For general measure coefficients these same statements are interpreted
with a common dominating measure and consumed/unallocated measures.

In flow notation, on this box the conditions become

    incoming (r_2-t_2) Lambda_2 = -v_2 Lebesgue,
    out(Lambda_2)-in(Lambda_2) = Lebesgue,

with zero sink. This identifies both the allocation moment and the
mass-balance obligations for a search over long-range flow measures.

## 6. Quantitative failure of constant translated-cell lifts

The phase-2 translation lift with constant edge densities on a finite
uniform type partition gives `C_22=v_2+constant` on every profile cell.
Such a field cannot vanish on an open y interval, regardless of the
accuracy of approximate ties at cell centers. On a y subinterval of
length ell, with beta fixed by w, any additive shift kappa obeys

    integral [max(0,y+kappa)-beta*(y+kappa)] dy
        >= beta*(1-beta)*ell^2/2.

The minimum has the zero at the `(1-beta)` quantile. This lower-bounds the
sum of capacity and virtual-allocation slacks, even if the competing
bidder's score is arbitrary. On the displayed box,
`beta*(1-beta)>=1/25`. A uniform n-cell y partition cuts its y interval
into at most n+1 pieces, and Cauchy gives
`sum ell_i^2 >= (1/20)^2/(n+1)`. Integrating over the other three
coordinates yields

    U_lift - R(V4.6) >= 1/[400000000*(n+1)] > 0

for this constant-density translated-cell architecture, whenever the
remaining flow conditions make it a valid upper. This is an obstruction
to exact equality at every fixed finite partition, not an obstruction
to convergence as n tends to infinity, and not an assertion about richer
within-cell or continuum flows.

Cycle-only updates retain divergence, hence retain the sink measure.
If an inherited sink has density at least a>0 on this box, then weighted
IR slack is at least `9*a/40000000`. No amount of divergence-free cycle
augmentation can remove that floor. A matching search must allow sink
redistribution, including exactly zero sink on positive-utility regions.

## 7. A certified long-range descent interface

Let two congruent own-report rectangles be A+s and B+s, with d=A-B,
and let the same opponent rectangle W index both. Add edge density
`epsilon>=0` to the two truthful-to-report translations

    B+s -> A+s,       A+s -> B+s.

Their divergence is zero. The allocation coefficient shifts by
`+epsilon*d` at A+s and `-epsilon*d` at B+s. If the incumbent upper's
maximizing allocation vectors are constant a_A and a_B on the entire
profile boxes, and all winning comparisons remain valid after the shift,
the exact lifted continuous upper changes by

    epsilon * |A| * |W| * d.(a_A-a_B).

Thus a strictly negative weak-monotonicity expression yields a genuine
upper decrease. The virtual maximizing allocation is allowed to violate
DSIC; that violation is precisely the useful signal. The rectangles must
remain in the domain and have equal shape, and winner margins must be
proved on the whole boxes. Center samples alone do not certify the
formula. These cycles can improve an upper even though a positive sink
elsewhere prevents them from completing a matching certificate.

## 8. What is resolved, and what remains open

The nonoverlapping gap identity separates local screening tightness from
global charged regret. Null-opponent charges identify an exact source of
charged regret that cannot be repaired by solving the charged problem
more accurately. The positive-volume lottery identifies a zero virtual
plateau and zero-sink requirement that a finite constant-density lift
cannot satisfy exactly. These are reusable constraints and diagnostics
for the upper branch, not a classification of all optimal mechanisms.

The exact replay uses only rational arithmetic, independently checks the
singular integral by degree-five quadrature, checks the hinge-shift
integral, and checks the actual frozen mechanism at 24 rational box
corners/intermediate t values. The written measure and convexity
arguments establish the continuum scope; those 24 reports alone do not.
Run `python -B -X utf8 verifier/flatness_constraints.py` from this phase.
