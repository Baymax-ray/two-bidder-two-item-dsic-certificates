# Independent revenue and geometry audit

The primary discovery derives a lottery from the binding residual-capacity corner. This audit reconstructs revenue without importing the candidate evaluator, its polynomial class, its menu-revenue formula, or an optimizer. The separate script is `verifier/independent_lottery.py`.

For a fixed aligned opponent report `(t,rho)`, put `c=137/500`, `q=113/500`, `d=c+q=1/2`. The four deterministic prices are `t`, `d+delta`, `t+c+delta`. The lottery allocates `(1,beta)` for `t+beta*c`. Comparing utilities directly shows that its whole new winning cell is

`c<y<Y=c+delta/(1-beta)`, `x>t-beta*(y-c)`.

The condition `beta*(q+delta)<=q` is exactly `Y<=d+delta`, so the low singleton is nonpositive on this cell. The minimum horizontal threshold is `t-beta*delta/(1-beta)>=t-q>0`. All cell boundaries therefore remain inside the unit square. Ties do not affect the integral; their pointwise handling is a separate obligation satisfied by the empty/low/high/bundle/lottery priority.

Write `z=beta/(1-beta)`. Integrating the lottery revenue over this cell and subtracting the old high-singleton and bundle revenue gives

`Delta_L=delta^2*((3t-2)*z-delta*z^2)/2`.

The integral includes bundle buyers who switch to the lottery. Omitting their payment changes would give the wrong variation. At the optimized `z=(3t-2)/(2delta)`, adding this gain to the four-menu quadratic in `delta` gives

`delta*=(9/16)(613/750-t)(839/750-t)`.

In fact the optimized lottery cell satisfies the stronger condition `Y<d` throughout `2/3<t<613/750`. To see this, put `T=613/750`, `U=839/750`; then

`d-Y=(T-t)*(3/2-(9/16)*(U-t))>0`.

Thus its oblique no-sale boundary lies above the actual residual corner `(t,c)` and below the next horizontal capacity junction. This helps explain what the lottery accomplishes: it rotates a boundary that the deterministic singleton price cannot lower.

The independent code clips the unit square by every utility-comparison halfplane for each of the five options, evaluates each complete polygon area by the shoelace formula, and sums price times area. It checks exact conditional revenues at both sides of the old cutoff and at additional rational parameter values. These are checks of the integrated formulas, not a finite type proof of DSIC or optimality.

A separate dictionary-polynomial implementation integrates the conditional gains over both item orientations, with density factor `2*(b-t)`. It reconstructs the one-sided gain

`472617707798758460108653/202125594240000000000000000000`.

The complete two-sided mechanism changes each bidder's conditional menu on the same opponent region. Linearity of revenue doubles this number once simultaneous feasibility is proved; it does not require the affected sets of joint reports to be disjoint. The resulting gain is

`472617707798758460108653/101062797120000000000000000000`.

The primary and independent computations agree exactly on this rational increment. The total-revenue enclosure adds it to the preserved V4.02 enclosure, whose primary and independent replays were rerun in this trial.

The two-sided feasibility audit must address the inherited bidder-2 override on `Q`, rather than merely invoke symmetry of the base. When the reverse splice meets `Q`, a new high singleton, bundle, or lottery would require an own report outside `Q`; only the low singleton can win. Its price exceeds `d`, and the other bidder's value for that item is below `c`, which is below the required bundle-upgrade threshold. When both reports belong to the new band, their low coordinates are below `c`: equal high-item orientations cannot both win that item, while opposite orientations select distinct items. The primary proof supplies these full real-report arguments, and a separate agent audits them independently.

This certifies an admissible strict revenue improvement. It does not certify optimality of the five-option menu among all conditional randomized menus, nor of the full auction.
