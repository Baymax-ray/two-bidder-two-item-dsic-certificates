# Continuous stream bound and a sharper certified integration rule

This branch preserves the inherited rational degree-four stream witness and first improves the integration of its **continuous** dual objective. It does not solve a type-grid auction and then label that grid value an upper bound. The saved witness comes from `research/closed/two-bidder-two-item-dsic-certificates/certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound/manifest.json`; its polynomial builder and directed de Casteljau subdivision are imported read-only. The three dependency hashes are included in each new certificate. The former audit-packet copies were byte-compared against these canonical closed dependencies and all three identities passed. Those imports are trusted code dependencies; they are not an independent reconstruction.

## Whole-auction inequality

Fix an opponent report and write the bidder's report in the two radial charts `(s,st)` and `(st,s)`, `0<s<1`, `0<t<1`. A complete DSIC mechanism has a convex, coordinatewise nondecreasing, 2-Lipschitz utility `u`, with its allocation equal to its gradient almost everywhere. One-dimensional integration of `u(s theta)=u(0)+int_0^s theta.a(r theta) dr` gives

`R_i = integral phi_i.a_i - integral u_i(0,v_-i) dv_-i`,

where the radial virtual value is `phi_i^0=(3s^2-1)theta/(2s)`. A stream correction is the curl of `psi=x(1-x)y(1-y)P(x,y,v_-i)`. It has zero divergence and tangent boundary flux, so its integral against the weak gradient of every such `u` is zero. Thus `phi_i=phi_i^0+curl(psi_i)` obeys the same identity. In particular, the only IR sink in this construction is at the zero type; **there is no positive interior sink density**.

Set `pi_j=max(0,phi_1j,phi_2j)`. Feasibility gives the unrestricted randomized-DSIC bound

`R_1+R_2 <= B(phi) := integral sum_j max(0,phi_1j,phi_2j)`.

The complete exact gap identity is

`B(phi)-R = integral sum_j pi_j(1-a_1j-a_2j)`

`          + integral sum_i,j (pi_j-phi_ij)a_ij`

`          + sum_i integral u_i(0,v_-i) dv_-i`.

These are capacity slack, virtual-allocation slack, and IR slack. This curl architecture uses DSIC's exact envelope and mixed-derivative identities; it does not introduce additional nonnegative weighted IC flows, so its weighted IC slack is identically zero. This is a limitation of the architecture rather than a claim that all incentive inequalities are tight.

## Coefficientwise Bernstein convex majorant

After multiplication by the radial Jacobian, both item-1 virtual competitors are polynomials on each of four unit-cube charts. Elevate them to a common tensor Bernstein degree: `p=sum_k B_k a_k`, `q=sum_k B_k b_k`. Positivity and partition of unity give the pointwise inequality

`max(0,p,q) <= sum_k B_k max(0,a_k,b_k)`.

The integral of each tensor basis function is exactly `1/N`, with `N` the number of controls. Therefore

`integral max(0,p,q) <= (1/N) sum_k max(0,a_k,b_k)`.

The old unresolved-cell rule used `max(0,max_k a_k,max_k b_k)`, losing variation even where it does not change the winner. The new mean-of-coordinatewise-max rule is always at least as tight for identical exact controls. It captures that variation while remaining an upper bound on the full continuum.

For fixed-point scale `S=10^12`, initial controls are floored and each exact coefficient lies in `[a,a+1]`. A degree-d midpoint subdivision floors its d averaging stages; inductively a lower-control error interval `[0,e]` becomes `[0,e+d]`. Each cell is bounded by the integer ceiling of the mean of `max(0,a+e_a,b+e_b)`. All array sums are checked to stay within signed int64; final accumulators and dyadic coverage use Python arbitrary-precision integers. Exact winner tests permit early stopping. Summing with each leaf's dyadic volume and multiplying by item symmetry gives each certified rational upper bound. The run explicitly verifies all four charts' full coverage at every recorded depth.

The saved sequence at depths 12,14,16,18,20 is strictly decreasing. More generally `min(previous certified bound,new certified bound)` is always an independently valid monotone incumbent sequence; no empirical decrease is used as a proof step.

## Actual witness optimization

`flow_scalar_search.py` numerically minimizes the **fixed-partition continuous Bernstein-majorant functional** along an amplitude of the rational stream. Every control is affine in that amplitude, so the objective is convex piecewise affine. The discovery code collects all active pairwise line intersections and solves the one-dimensional convex minimization. It is explicitly numerical discovery; its reported objective is not a certified endpoint. The initial depth-12 selected amplitude `860972/862497` was rationalized and separately passed through `flow_majorant.py`, which rederived its complete continuous upper bounds using directed exact arithmetic. Its depth-20 bound `463664341531926533/524288000000000000` is worse than the amplitude-one anchor, so this trial was rejected. A finer depth-18 follow-up majorant search selected `940619/936604`; this last follow-up remains numerical discovery only and was stopped when the enlarged conditional-support splice proved more structurally promising. Only the exact rational outputs can enter an incumbent sequence. This is a deliberately small direction search, not a claim that the stream class has been optimized.

## Why this analytic stream family cannot match the lottery candidate

Consider any open region on which the candidate gives one bidder `(1,beta)` with `0<beta<1`, gives the opposing bidder no items, and leaves `1-beta` of the safe item unallocated. Such regions occur in V4.6's certified five-option conditional lottery construction. Equality in the two nonnegative allocation slacks above forces `pi_safe=phi_winner,safe=0` throughout that region (almost everywhere suffices).

For every polynomial stream in this architecture, `phi_winner,safe` is real analytic on each connected open radial chart. Vanishing on an open subset forces it to vanish on the whole chart. But its radial base has the term `-theta_safe/(2s)` as `s` tends to zero, while the polynomial curl is bounded; it cannot vanish identically. Thus **no finite polynomial stream, of any degree, can exactly certify this candidate while that positive-measure partial-allocation region remains**. This is an exact structural obstruction, not the failure of a finite fit or approximate grid ties. It does not rule out nonanalytic piecewise incentive flows or a different candidate that reallocates all the safe-item capacity.

## Exact sign certificate enabling a different global support

`flow_sign.py` proves both inherited bidder-1 virtual components are nonpositive whenever its own report lies in `[0,2/5]^2`, uniformly over the other bidder's entire report square. Since `curl_1` is divisible by own coordinate `w_1`, the sign is that of

`Q=3s^2-1+2s^2 curl_1/w_1`.

This is a polynomial after the chart substitution `s=(2/5)z`. Exact Bernstein upper controls certify `Q<0` on both own charts (three cells in the first chart, one in the second); simultaneous item symmetry gives the other component. Zero coordinate faces have virtual value zero by the explicit factor. This sign theorem allows a full-capacity conditional support for bidder 2 to be spliced into that opponent-report square without a positive charged-allocation term for bidder 1. The same proof was expanded to `h=43/100`: `flow_sign_43_certificate.json` uses eight cells on the first chart and one on the second, with maximum depth six. Every normalized numerator upper is at most `-9023081075/10^12` in chart 0 and `-70018012548/10^12` in chart 1. The conditional-support branch supplies the distinct global support and its certified regional saving; this file does not assume that the splice is valid merely from a local complementary certificate.

The attempted extension to `h=1/2` is false, not merely uncertified. `flow_half_counterexample.py/json` evaluates the inherited bidder-1 item-1 virtual value exactly at own report `(1/2,1/2)` and opponent report `(1,1/2)` and proves it is greater than `1/40`. Its exact rational numerator and denominator are recorded. Continuity supplies a relative neighborhood of positive values, so simply extending the zero-charge splice to the larger square would invalidate the argument.
