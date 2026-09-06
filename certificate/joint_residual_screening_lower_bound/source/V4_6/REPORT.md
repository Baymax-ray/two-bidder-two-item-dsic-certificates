# V4.6: exact joint improvements and full conditional certificates

**V4.6 improves the lower bound and proves new unrestricted conditional
screening theorems. It does not close the auction gap.** The strongest mechanism constructed in V4.6 is
complete, pointwise feasible, randomized DSIC/IR and has revenue

\[
\boxed{0.8758198541484224553460
       <R_{4.6}<0.8758198541484224553461.}
\]

This is an exact rational enclosure of an explicitly specified expression,
not a floating optimizer output. The improvement over V4.5 lies in

\[
[0.0005653267086091341752,\ 0.0005653267086091341753].
\]

The inherited unrestricted upper remains

\[
U=\frac{3715139591287203}{4194304000000000}
 =0.8857583025186545848846435546875.
\]

Thus the remaining upper-minus-construction gap is between
`0.0099384483702321295385` and `0.0099384483702321295386`.
There is no matching common certificate, optimal mechanism, or new
attainment/nonattainment result. The upper certificate is a preserved
predecessor result; its full proof was not re-executed this phase.

## Exact mechanism and revenue

The final mechanism is the composition implemented by
[`price_joint_reallocation.mechanism(profile)`](verifier/price_joint_reallocation.py).
Its dependency chain retains each intermediate mechanism separately:

| Step | Change | Exact positive revenue increment, approximately |
|---|---|---:|
| Eplus | Extend both lottery splices to the actual low-coordinate strip | 0.00000301983695567258 |
| F | Optimize bidder 1 at opponents where bidder 2 is globally empty | 0.0005585288428503137 |
| Bundle exchange | Transfer bundle ownership and change bidder 2's entire affected menus | 0.00000347164740430913 |
| Coupled response | Adjust the safe singleton with the bundle price | 0.000000302465270896550 |
| Corner release | Release capacity by complete entry-fee menus and lower the opposing lottery price | 0.00000000391612794214225 |

The rows are additive increments in the displayed order; the last two
are not counted a second time in the aggregate expression below.
All components use the same two-bidder iid-uniform formal model.

Let \(R_{4.5}\) denote the exact V4.5 expression: the
[V4.02 exact continuous integral](../V4_02/certificate/split_cost_revenue.json)
plus
\(472617707798758460108653/101062797120000000000000000000\).
The inherited expression and enclosure are replayed through the V4.5
verifiers; no decimal is substituted for that exact baseline.
Then the exact V4.6 revenue is

\[
R_{4.6}=R_{4.5}+a_0+a_2\sqrt2+a_{23}\sqrt{23}+J,
\]

where

\[
\begin{aligned}
a_0&=-\frac{1609541379668231661249547038251}
                {159173905464000000000000000000000},\\
a_2&=\frac{57567793}{7593750000},\qquad
 a_{23}=-\frac{12167}{1328906250},
\end{aligned}
\]

and the fully evaluated joint increment is

\[
\begin{aligned}
J={}&\frac{6578986777818169914603}
           {10652675687500000000000000000000}\\
&+\frac{6248637}{282500000000000}\log\frac{161}{176}
 -\frac{61575471}{282500000000000}\log\frac{613}{628}\\
&-\frac{9308601}{5000000000000000000}\log\frac{13}{10}.
\end{aligned}
\]

The logarithms are natural. Independent rational series bounds give

\[
0.00000000391612794214225366689702614
<J<0.00000000391612794214225366689702615.
\]

A separate, more conservative proof gives
\(J\ge26902077489/12500000000000000000>0\).
The exact expression and all enclosures are stored in
[consolidated_bounds.json](certificate/consolidated_bounds.json).

The Python mechanism functions evaluate rational profiles exactly; the
accompanying formulas define the mechanism on every real report in the
continuous square, including algebraic boundaries. Every changed
conditional mechanism maximizes a complete menu containing empty at
zero price. Priority is explicit and independent of the own report.
Closed faces and retained exceptional rows are specified in the linked
proofs. In particular Eplus excludes its low-coordinate `c` face, F is
closed, the bundle-exchange region excludes its upper sum face, and the
final corner rectangles are closed. The entry fee chooses empty at zero
utility. These are all-real proofs of DSIC/IR and feasibility; the rational
regressions are additional implementation checks.

Expected allocation feasibility is pointwise. It can be implemented by
choosing for each physical item at most one recipient with the stated
marginal probabilities. Payments are bounded and menus are Borel, giving
integrability and joint measurability. DSIC is in expected utility, as in
the requested randomized class; universal truthfulness is not asserted.

## What forced the new primal changes

Use \(a=159/250\), \(b=91/100\), \(c=137/500\),
\(q=113/500\), \(A=2/3\), and \(b_0=(4-\sqrt2)/3\).

The first discovery is the closed global no-sale region

\[
F=\{\max(v)\le1/2,\ v_1+v_2\le b_0\}.
\]

Bidder 2 is empty at its own reports in F for every opponent report.
Consequently bidder 1 has full residual capacity whenever its opponent
lies in F. Its old constant menu `(a,a,b)` is inferior to the certified
single-buyer menu `(A,A,b0)`. Replacing the whole menu gains exactly

\[
\frac{1925713777}{243000000000}
-\frac{11719583}{2250000000}\sqrt2.
\]

This is a one-bidder splice, not twice that number. The proof checks the
other bidder's entire report square, including all earlier lottery rows.
See [free_bidder_one.md](research_log/free_bidder_one.md).

Immediately above F, define
\(G=\{\max(v)\le1/2,\ b_0<v_1+v_2<b\}\).
When bidder 2 reports v in G, bidder 1's bundle price becomes `sum(v)`.
On the affected Q menus, bidder 2's bundle price must become at least
`sum(w)`, where w is bidder 1's report. This causes genuine ownership
transfers: at `w=(.45,.45), v=(.44,.44)`, the old bundle recipient is
bidder 2 and the new recipient is bidder 1, paying `.88`. The proof also
exhibits a positive-volume box of strict transfers.

Changing only the opposing bundle price does not solve the induced inner
problem. In a constrained Q row, write
\(t=\max(w)>1/2\), \(z=\sum w\), \(k=t-q\), and
\(C_0=5/6+3k^2/4\). When z exceeds C0, the safe singleton also admits a profitable adjustment:

\[
(A,B,C)=(A,z-k,z).
\]

The bundle-minus-safe upgrade threshold remains k, so the induced
allocation changes are compatible with actual capacity. The revenue cost
relative to the old optimal conditional menu is exactly
\(-(z-C_0)^2\), after integrating all affected own reports. The full
randomized certificate below proves this is the complete conditional
optimum for that new residual. This is stronger than stationarity of a
chosen price family. See
[outer_bundle_reoptimized.md](research_log/outer_bundle_reoptimized.md).

## Full randomized conditional certificates

The lottery strip expands from the old triangular restriction to

\[
E^+=\{A<t<T,\ \rho<c\},\quad
 t=\max(w),\ \rho=\min(w),\ T=613/750.
\]

The retained bundle and singleton inequalities establish actual joint
feasibility even when `t+rho>b`. For the reference before the final corner release, a new theorem proves
the five-option lottery menu solves the entire randomized inner problem
on this strip for its actual residual. It does not assume that competitors have finite
menus or fixed lotteries.

The proof partitions the positive-utility set into horizontal and
vertical envelope regions. Convexity of the right trace supplies a
nonnegative hinge integral; monotonicity on the binding `y=c` line supplies
a junction inequality; IR controls the no-sale region. The resulting
finite Borel capacity measure contains volume and line components and
satisfies the exact identity

\[
\langle\pi,r\rangle-R
=\langle\pi,r-x\rangle+T_g+\lambda M_x+S_u\ge0.
\]

Each slack vanishes at the reference candidate. Arbitrary lotteries,
nonzero IR utilities, and negative payments by competitors are included.
The hypotheses and exact measures are in
[inner_lottery_certificate.md](research_log/inner_lottery_certificate.md),
with an [independent analytic audit](research_log/independent_inner_audit.md).

The bundle exchange creates a different residual hole. Its response has
a matching certificate obtained by anchoring the top utility trace at
`x=1/2`, then expanding along an occupied bottom segment and vertical
segment. For `B=C-k<=A`, `C0=5/6+3k^2/4`, and `C>=C0`, its mass is

\[
m=2(C-C_0)\ge0,\qquad 3|D_0|=m+1.
\]

The exact global gap for every randomized conditional competitor is

\[
\langle\pi,r\rangle-R
=\langle\pi,r-x\rangle+3\int_{D_0}u-mu(0,0)\ge0.
\]

The actual F/G bundle purchases supply the needed bottom and vertical
constraints; inherited top capacity supplies the remaining saturation. This restores bidder 2's full conditional
optimality throughout Q after the coupled response. See
[inner_diagonal_capacity.md](research_log/inner_diagonal_capacity.md).

Each matching measure also gives a global supporting inequality for its
conditional residual value functional:

\[
\mathcal V(r)\le\mathcal V(r^*)+
                  \langle\pi,r-r^*\rangle.
\]

These are finite measures, including singular supports. The construction
does not force a positive sink at every type. They are **conditional**
supports and need not support the opposing bidder's optimization.

## How the dual conditions produced another joint deformation

The lottery certificate assigns a singular charge to a consumed junction.
This identifies a capacity direction that the old containment construction
cannot use. Set `epsilon=9/10000`, `J=[.7,.71]`, and use one physical
orientation:

\[
W=J\times[0,1/5],\qquad
S=[.7-4\varepsilon,.71]\times[c-2\varepsilon,c+4\varepsilon].
\]

For bidder-2 menus indexed by w in W, lower only the lottery payment by
epsilon. For bidder-1 menus indexed by v in S, charge an entry fee epsilon
on every nonempty menu option. The first is a full menu change; the second
can retain the old allocation or select empty.

The lottery's comparisons with empty, singleton and bundle force every
possible capacity conflict into S. At those profiles bidder 1's old
utility is less than epsilon, so the fee releases the item. Its safe item
is also free throughout the enlarged lottery cell. This proves feasibility
for every report, not merely the integrated allocation.

All buyers forced to move are included in the revenue calculation. For a
lottery row, the complete price-cut effect is

\[
\Delta R_2=\frac{\alpha L}{4}\varepsilon
 -\frac{\alpha}{4\beta(1-\beta)}\varepsilon^2
 -\frac{1}{2\beta(1-\beta)^2}\varepsilon^3.
\]

For a complete entry-fee row with no-sale area D0 and bundle price C,

\[
\Delta R_1=(1-3D_0)\varepsilon
             -\frac32C\varepsilon^2-\frac12\varepsilon^3.
\]

Integrating the actual frozen tariff chambers and rational lottery
parameters gives J above. Independent polygon integration checks both
identities, including the retained `y=c` face and tariff boundaries.
See [joint proof](research_log/price_joint_reallocation.md),
[exact integration](research_log/price_joint_exact_revenue.md), and
[independent audit](research_log/outer_fee_polygon_audit.md).

The pre-release reference is therefore strictly suboptimal even though
its displayed inner problems were solved. No claim of suboptimality or
optimality of the final improved mechanism follows automatically.
The final operation preserves full F and Q certificates but deliberately
breaks some Eplus equality conditions. The precise surviving regions are
listed in [conditional_coverage.md](research_log/conditional_coverage.md).

## Verification and remaining proof obligations

Primary and independent calculations agree on every new exact increment.
The independent revenue replay integrates allocation-cell polynomials over
continuous curved regions using quadratic-field arithmetic. Partial
fractions are checked as polynomial identities and logarithms have signed
rational remainder bounds. Finite rational profile tests check source
implementation and ties; they do not prove continuum optimality.

The package includes the full pointwise arguments, exact JSON certificates,
read-only replayers, predecessor identity preservation, and complete stable
file manifests. [VERIFICATION.md](VERIFICATION.md) records the actual run.
No grid solver, numerical first-order condition, or minimum-norm selection
is used as a theorem.

To close the original problem, the still-unknown outer allocation must
admit a capacity measure and incentive system supporting both bidders
simultaneously, with all equality conditions met. The new conditional
certificates and the explicit joint direction constrain that task, but
do not solve it. The exact lower mechanism is complete; the unrestricted
upper proof at its value remains open.
