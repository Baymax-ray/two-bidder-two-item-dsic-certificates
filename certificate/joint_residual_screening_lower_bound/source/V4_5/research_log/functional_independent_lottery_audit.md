# Independent audit: simultaneous actual-residual lottery splice

This audit reads `residual_lottery_extension.md` as a complete mechanism specification, rather than inferring feasibility from its floating discovery or from a conditional revenue formula. It independently checks the binding inequalities, both simultaneous-splice cases, and preservation of the old Q support. The analytic proof is sufficient for pointwise feasibility of the stated randomized auction. It does not establish full inner optimality of the new five-option menus or a global revenue upper bound.

## 1. Conditional residual and lottery feasibility

For an opposing type (t,rho) in E, rho<=b-t<b-2/3<c<d, and total value<=b. Hence the opposing retained bidder can only take the high-coordinate item. The common-base conditional prices are exactly (t,d,t+c), so the possible hole for that high item is contained in

    {y<=d, x<=t, x+y<=t+c} union {y>=d, x<=t-q}.

The low item is free at every report. All these inequalities may be taken weakly, as required for an upper description of the pointwise hole.

With delta>0, B=d+delta, and L=(1,beta) priced at t+beta*c, the hole calculations are correct. For y<=c, u_L<=0 from x<=t. For c<=y<=d, u_L<=-(1-beta)(y-c)<=0 from x+y<=t+c. For d<=y<=B, u_L<=-q+beta(B-c)<=0. For y>=B, u_L-u_low<=-q+beta(B-c)<=0. The requirement beta(q+delta)<=q supplies the final sign because B-c=q+delta. Empty and low-singleton priority prevent lottery selection at every equality. The same priorities make all retained deterministic choices safe in the hole.

The chosen parameters satisfy the requirement exactly:

    beta/(1-beta)=(3t-2)/(2delta),
    beta(q+delta)<=q iff (3t-2)/2<=q iff t<=T.

On the open E band, delta=(9/16)(T-t)(U-t)>0 and 0<beta<1. Endpoint rows retain the complete old mechanism. There is therefore no undefined formula in the implemented auction and no limiting-only treatment of exceptional reports.

The new four-option price increment delta is at least the frozen V4.02 increment. Raising low-singleton and bundle prices by their common nonnegative difference admits a maximizing subset of the prior choice, by strict subadditivity. The subsequent lottery is checked separately against the actual hole. This separation is valid: one cannot infer lottery feasibility merely from a deterministic contraction lemma.

## 2. Both opposing reports in E

Bundle prices exceed b while each own report sums to at most b. If the high coordinates coincide, both own low values are below c. The lottery is then dominated by the high singleton, and a low-singleton purchase is impossible because its price exceeds d. Only the bidder with strictly larger high report can buy the common high item. Equal high reports yield zero utility, so empty-first excludes a conflict.

If high coordinates differ, each aligned high-item value is below c. A lottery maximizer must have that coordinate at least k=t-q. To check this global threshold, for y<=B compare the lottery with empty; for y>=B compare it with the low singleton. Both comparisons yield

    x >= t-beta(B-c) >= t-q=k.

But k>2/3-q>c. Thus neither lottery nor high singleton can be selected. Each bidder may buy only its own distinct high-valued item, called the low-of-opponent singleton in the rotated menu. This proves feasibility at all reports in the simultaneous E-by-E region, including all menu ties.

## 3. Reverse splice against the inherited Q exception

The asymmetric Q exception belongs to bidder 2 and cannot be ignored when also changing bidder 1. Let bidder 1's report lie in Q and bidder 2's report lie in E. Align the latter as (t,rho), the former as (x,y). The new bidder-1 high singleton is impossible because x<=2/3<t. Its bundle is impossible because x+y<=b<t+c. A lottery maximizer must have y>=c and x>=t-beta(y-c), giving

    x+y >= t+c+(1-beta)(y-c) >= t+c > b,

also impossible. Thus bidder 1 can select only empty or the low singleton.

A positive low-singleton purchase implies y>B=d+delta>d and x<=b-y<y. Bidder 2's Q menu therefore treats physical item y as scarce. Its own value rho satisfies rho<=b-t<c, while the scarce-singleton price is 2/3 and the bundle-upgrade threshold is y-q>=c+delta>c. It cannot consume that same item. At y=B the new bidder 1 chooses empty. This confirms the claimed reverse splice against the full inherited Q menu, including singular reports.

Outside Q and E, the unchanged bidder-2 row is a retained subset of the same shared base, so the one-sided hole proof applies with bidder names exchanged. The remaining orientation is exactly the original one-sided proof. These cases exhaust the report cube.

## 4. The Q capacity certificate survives the simultaneous splice

A further useful consequence is that the old Q support still matches the actual residual after both changes; it need not be described merely as a certificate for an obsolete fixed bidder 1.

On a fixed bidder-1 report w in Q, the reverse splice can change bidder 1 only when the opposing report v lies in E. In that case the preceding proof shows both the old and new bidder-1 menus allow only the low-of-v singleton or empty. Its price increases from d+delta_old to d+delta*, so the bidder-1 allocation only contracts. If the fixed w is a free Q fiber, no contraction occurs because max(w)<=d and both prices are at least d with null-first ties.

On a constrained Q fiber, any changed physical item is the scarce coordinate of w: its value exceeds d. In coordinates (z,z_safe) aligned with w, the released capacity lies in

    z<=b-t<c,  2/3<t=z_safe<T<1.

The V3.1/V4.02 matching Q measure on the scarce capacity has an interior density supported only on z>2/3 and a singular component supported on z_safe=1. Both give zero mass to the displayed released set. The safe capacity is unchanged, since bidder 1 never receives the safe item on a Q fiber. Consequently

    <pi_Q, r_new-r_old> = 0.

The inherited bidder-2 Q menu remains feasible. Its old exact support therefore gives, for every arbitrary randomized DSIC/IR inner competitor under the new residual,

    R <= <pi_Q,r_new> = <pi_Q,r_old> = R_Q_old.

The inherited menu attains equality. This verifies full inner optimality on Q for the simultaneous candidate as well. It is a regional conclusion and supplies no support on E or its complement.

## 5. Revenue identity and remaining scope

The lottery's active region is c<y<Y=c+delta/(1-beta), x>t-beta(y-c). Admissibility gives Y<=B; the candidate parameters also keep the lower x threshold strictly positive. Therefore no square-edge clipping is omitted in the stated cell integration. The resulting gain

    delta^2/2 * [(3t-2)z-delta*z^2],  z=beta/(1-beta),

and the optimized gain delta(3t-2)^2/8 have the stated parameter scope. The four-option delta objective has quadratic coefficient -1, so adding the optimized lottery term shifts the maximizer from delta0 to delta*=delta0+(3t-2)^2/16. Relative to the old delta it yields exactly

    (delta*-delta_old)^2 + delta_old(3t-2)^2/8,

or delta*^2 where the old delta is zero. This independently checks the integrands in the exact one-sided revenue calculation. The simultaneous gain doubles because each bidder's revenue is the integral of its own complete conditional menu and both old E rows are the same retained four-option row. This identity does not assume independent allocation changes.

The implementation's finite menu maximization proves DSIC and IR, Borel parameter functions and explicit priorities prove measurability, and the lottery uses only an item whose opposing allocation is zero. Independent Bernoulli realization is therefore pointwise feasible in the applicable lottery regions; in E-by-E the proof excludes simultaneous lottery choices. The new five-option family may still be conditionally improvable. Neither its parameter stationarity nor this independent feasibility audit is an unrestricted optimality certificate.
