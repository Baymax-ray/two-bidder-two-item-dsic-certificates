# V5 — Final Primal–Dual Gap-Closure Sprint

V5 improves **both global bounds**. A complete reserve transformation raises revenue by more than 0.000048, while a globally accounted conditional-support replacement and a disjoint BB incentive correction lower the upper endpoint by more than 0.00045014117. Together they reduce the previously certified gap by **at least 7.8608%**.

| Quantity | Certified enclosure or upper endpoint |
|---|---:|
| Revenue of the new complete mechanism | [0.876512208776757709245241140006, 0.876512226027595234048128153175] |
| Unrestricted randomized-DSIC upper bound, rounded upward | 0.882351585488796576205586892264 |
| Remaining upper-minus-mechanism gap | [0.005839359461201342157458739089, 0.005839376712038866960345752257] |
| Reduction of the previous certified gap | [7.860837678054709245934428147882%, 7.861109877948168823533398191185%] |

All displayed endpoints are outward rounded. The exact rational upper endpoint, revenue enclosure endpoints, and assembly are in [phase_ledger.json](certificate/phase_ledger.json). These are bounds for the original two-bidder, two-item, independent uniform additive-value problem on the full continuous report space. The gap has decreased; an optimal mechanism and a matching upper certificate have **not** been established.

## 1. A complete mechanism that changes ownership

Let $(x^0,p^0)$ be the complete V4.6.1.1 mechanism, including its full menus and tie completion. Set $\tau=1/100$, $s=99/100$, and apply the coordinate map
\[
T(t)=\max\{(t-\tau)/s,0\}.
\]
At every report profile $v$, define
\[
x_i^\tau(v)=x_i^0(Tv),\qquad
p_i^\tau(v)=s\,p_i^0(Tv)+\tau\sum_jx_{ij}^0(Tv).
\tag{1}
\]
This is an explicit mechanism specification in terms of the preserved exact implementation; [primal_global.py](verifier/primal_global.py) evaluates it using exact report arithmetic.

At transformed reports the source rule selects empty at zero maximal utility, and otherwise the lexicographically first jointly feasible pair of full-menu maximizing rows. This completes clipping thresholds, menu interfaces, endpoints, and ties. Pointwise feasibility is inherited at the transformed profile, and all maps are Borel measurable.

The crucial source property is that a zero-valued item is never allocated, including at ties. Every relevant bundle upgrade has a strictly positive price; the lottery comparisons also force strictly positive values for both coordinates that it allocates. Therefore
\[
u_i^\tau(v_i;v_{-i})=
s\,u_i^0(Tv_i;Tv_{-i})
\]
has the selected allocation in (1) as a subgradient even at clipping knots. Convexity and coordinatewise monotonicity give all-pairs DSIC; source IR gives IR. This proof is for every real report, not a grid check. Expected allocations can be realized item by item as bidder 1, bidder 2, or unsold, with the specified expected payments.

The transformation goes outside contraction of the old allocation at the same reports. On the entire box of radius $1/10000$ about
\[
v_1=(1577/2000,123/200),\qquad v_2=(3/5,4/5),
\]
the old BB allocation is bundle/empty, while the new allocation gives item 1 to bidder 1 and item 2 to bidder 2. Within this box the singleton surcharge changes from $q$ to $sq$, while the bundle price remains the opposing sum. Exact affine inequalities at all 16 vertices prove the ownership switch throughout the positive-volume box.

### Full revenue, including every induced switch

For one uniform coordinate, $T(V)$ has law $\tau\delta_0+s\,\mathrm{Unif}[0,1]$. For each subset $S$ of the four coordinates, let $R_S,N_S$ be source revenue and allocated quantity integrated on the face where precisely those coordinates are fixed at zero. Then the exact revenue characterization is
\[
R_\tau=\sum_{S\subseteq\{1,2,3,4\}}
\tau^{|S|}s^{4-|S|}\bigl(sR_S+\tau N_S\bigr).
\tag{2}
\]
This degree-five identity includes all four-dimensional ownership, sale, lottery, payment, and rent changes. It is not an extrapolation from the local BB witness.

The coefficient integrals reduce to rational polynomial integrals over conditional menu branches, with a separately bounded algebraic price and narrow crossing-strip remainders. All 296 resolved strips and 15 enclosed strips are accounted for. The resulting revenue enclosure has width below $1.726\,10^{-8}$, much smaller than the certified gain. The derivative at the old mechanism is also rigorously positive:
\[
R'_0=N_4+4R_3-5R_4
\in[0.0120503811119742,0.0120521625636254].
\]
This is an admissible global direction that improves the old mechanism. It does not establish optimality of $\tau=.01$, or of this transformation family.

The complete proofs and moment formulas are in [primal_global.md](research_log/primal_global.md); [primal_independent_review.md](research_log/primal_independent_review.md) records the separate exact polynomial and accounting checks.

## 2. An upper improvement after charging the opposing bidder

The main upper improvement enlarges the opponent domain on which a full-capacity screening identity replaces the old radial/stream identity. Put
\[
W=[0,43/100]^2,\quad
J=(43/100,1/2]\times[0,7/20],\quad
D^\sharp=W\cup J\cup J^{\mathrm{swap}}.
\]
This domain is inside the single-bidder no-sale region
\[
D_0=\{x,y\le2/3,\ x+y\le(4-\sqrt2)/3\},\qquad |D_0|=1/3.
\]

For each fixed opposing report, the explicitly constructed nonnegative screening field $\Psi$ satisfies
\[
R_i(w)=\langle\Psi,x_i\rangle-3\int_{D_0}u_i(v;w)\,dv.
\tag{3}
\]
Its full boundary trace is retained: top/right flux matches the revenue identity; bottom/left flux is zero; internal normal traces match. There is no uncharged singular interface contribution. The switch between identities depends only on the opposing report, so it introduces no own-type derivative of the switching indicator.

Writing $\theta(w)=1_{D^\sharp}(w)$ and $\bar u=u-u(0;w)$, the exact normalized utility term after the switch is
\[
u_i(0;w)+3\theta(w)\int_{D_0}\bar u_i(v;w)\,dv\ge0.
\tag{4}
\]
It is explicitly charged in the global identity. The remaining fields and inherited incentive terms are assembled before using the common capacity price
\[
\Pi_j=\max(0,\Phi_{1j},\Phi_{2j}).
\tag{5}
\]
Both opposing virtual values therefore contribute to the same envelope. This gives an unrestricted upper bound; no incumbent complementarity is assumed to justify it.

The certified net splice decrease satisfies
\[
G_{\mathrm{splice}}\ge
4\bigl[L-|J|R_{\mathrm{SJA}}-E\bigr]
\ge0.00045027837569474655.
\tag{6}
\]
Here $L$ integrates the displaced positive virtual field, $|J|R_{\mathrm{SJA}}$ pays for the complete new support, and $E$ bounds all positive opposing-price excess. Simultaneous replacement in both added domains is accounted for pointwise. On intersections with $W$, the inherited sign theorem makes the directed estimate conservative. Thus (6) is a net whole-auction comparison.

The replay encloses every one of 294 roots and 12,294 terminal boxes. Exact coefficient bracketing, outward-rounded tensor Bernstein arithmetic, rational volumes, dyadic accumulation, and an integer-square-root enclosure supply a continuous certificate. [global_duality.md](research_log/global_duality.md) specifies the field, source, trace formulas, overlap proof, and arithmetic assumptions.

### BB incentive transport with explicitly allowed slack

A disjoint addition places equal nonnegative measures on both IC directions between
\[
B=A+(3/20,-1/40).
\]
Utility marginals cancel exactly. Allocation covectors are bounded body densities even though the IC pair measure lives on translated graphs; no boundary flux or singular capacity price is created. The actual weighted IC slack remains in the identity.

Sixty-four whole boxes with exact rational densities stop no later than the first virtual zero or winner tie. Their full common-envelope decrease, including four disjoint symmetry copies, is
\[
G_{\mathrm{BB}}=
\frac{4786305147}{17179869184000000}.
\tag{7}
\]
Some of these boxes meet incumbent menu interfaces and may have positive added IC slack. The correction is accepted because its **total** upper value decreases. The correlated capacity, virtual, and IC changes are recorded in [bb_global.md](research_log/bb_global.md), not silently discarded.

### Conservative overlap accounting

Before subtracting (6), the assembly removes **all** old V4.8A first-event fields and gives back their entire certified deduction. This is more conservative than removing only the overlapping QQ part. It retains the disjoint sparse flows, previous $W$ support, inherited enclosure allowance, and BB master correction. The new BB boxes are also disjoint from the splice and all retained corrections.

Precisely,
\[
U_5=U_{4.8B}+G_{\mathrm{old\ event,lower}}
-G_{\mathrm{splice,lower}}-G_{\mathrm{BB}}.
\tag{8}
\]
The resulting exact decrease is enclosed by
\[
[0.000450141171417495958112646039,\,
 0.000450141171417495958112646040].
\]
The separate QQ compact-curl trial has an inconclusive certified sign and overlaps the splice. Its purported gain is not included.

## 3. The common ledger and what remains open

For the new primal, the origin utility and the source in (4) are zero by a fresh argument: $T(w)\le w$ keeps the relevant conditional menu in its free-SJA branch, and $T(v)\le v$ preserves zero utility on $D_0$. This does not imply the remaining capacity, allocation, or IC terms vanish.

With all retained terms and the explicit enclosure allowance,
\[
U_5-R_\tau=C_5+V_5+K_{\mathrm{retained}}+K_{\mathrm{BB}}+E_5.
\tag{9}
\]
Here $C_5$ is priced unused capacity, $V_5$ is virtual-allocation mismatch, the $K$ terms include actual finite IC and inherited PSD convexity pairings, and $E_5$ is certificate enclosure slack. All are nonnegative. [gap_ledger.md](research_log/gap_ledger.md) defines their pairings and separates old-incumbent diagnostics from new-primal quantities.

The total remaining gap is rigorously enclosed, but it has not been newly integrated into a complete numerical BB/QQ/mixed atlas for the changed primal. Old atlas components are not relabeled as V5 numbers. In particular, the new bound need not support the new mechanism with equality, and no unique equality system has been obtained.

V5 meets two of the requested decisive outcomes: a materially stronger complete mechanism and a materially smaller unrestricted upper bound. It does not close the full problem or rule out broad classes of alternative mechanisms. The direction now justified by evidence is to study the globally improving transformed ownership interfaces together with the enlarged common support; failure of the unused finite libraries provides no additional impossibility claim.

## 4. Verification and preservation

The package includes six accepted proof/assembly replays, independent upper and primal audits, optimized-Python rejection checks, and a preservation check for all 4,278 predecessor files. Default replay is read-only. The final receipt is [replay_receipt.json](certificate/replay_receipt.json); [VERIFICATION.md](VERIFICATION.md) states precisely what it covers.

The inherited V4.6.1.1 mechanism theorem, inherited global upper identities and certified integration remainder, and the low-square sign theorem remain explicit dependencies. They were source-hash checked, not all reproved from scratch in V5. The new arguments cover continuous cells and universal mechanism inequalities; finite implementation samples supplement those proofs. A successful Python replay or manifest check is not a formal proof-assistant verification.
