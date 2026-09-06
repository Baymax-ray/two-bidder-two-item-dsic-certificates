# Exact reverse free-capacity screening

This construction keeps the extended V4.6 bidder-2 mechanism fixed and optimizes bidder 1 completely on a newly identified set of its opponent reports. It is not an alternating-best-response calculation: the whole residual is proved exactly full on each changed fiber, and a universal single-buyer certificate gives the matching optimum there.

Let `a=159/250`, `b=91/100`, `d=1/2`, `c=137/500`, and set

$$b_0=(4-\sqrt2)/3,\qquad F=\{v:\max(v_1,v_2)\le1/2,\quad v_1+v_2\le b_0\}.$$

## 1. Exact zero-allocation type set of bidder 2

Bidder 2 receives nothing at every opponent report if its own report is in F, including the closed boundaries.

Outside Q and the extended lottery strip, its retained deterministic menu has singleton prices at least d and bundle price at least b. On a free Q fiber it faces singleton prices 2/3 and bundle price b0. On a constrained Q fiber both singleton prices exceed d, while the bundle price exceeds b0. These comparisons are uniform over the full opponent square. Zero-utility choices use empty first.

On an extended lottery fiber its singleton prices are t>2/3 and d+delta>d; its bundle price is t+c+delta>b. If a lottery containing the scarce item can beat the high singleton, its safe coordinate y is at least c. Its utility is then at most `x+y-t-c`, which is strictly negative for own reports in F, since b0<b<t+c. Below c it loses to the high singleton, which itself has negative utility. Thus the lottery also cannot be selected. This proves the assertion for every report, with no exceptional-set omission.

The set is maximal for this global zero-allocation property. If one coordinate exceeds d, an opponent report giving value one only to the other item yields a positive-utility d-priced singleton. If both coordinates are at most d but their sum exceeds b0, opponent report (0,0) gives the SJA menu and a positive bundle choice. Hence the exact global zero-allocation set is F.

## 2. Complete new mechanism

First execute the complete extended lottery mechanism `outer_lottery_strip.mechanism`. Retain bidder 2 everywhere. If bidder 2's report is outside F, also retain bidder 1. If it is in F, offer bidder 1

- empty at zero;
- each singleton at 2/3;
- the bundle at b0.

Choose the smallest physical mask among utility maximizers, empty first. These are complete menus on the whole real own-type square. The preceding theorem makes residual capacity exactly (1,1) for every own report on each changed fiber. Thus every realized allocation is feasible, taxation proves pointwise DSIC/IR, the Borel predicates and priorities prove measurability, and payments are bounded.

The exact single-buyer certificate already rederived in V3.1 applies to every randomized DSIC/IR competitor under full capacity. Its revenue is `4/9+2sqrt(2)/27`. Therefore bidder 1 is now fully conditionally optimized on F.

## 3. Exact revenue gain

On every opponent report in F, the old bidder-1 menu is exactly `(0,a,a,b)`: its pivot vanishes, both split-price minima equal a, every common fee starts above the old d=501/1000, bundle fees require sum at least b, and the joined menus start above the same old d. The extended lottery strip is disjoint from F. There are no hidden moving fee regions in this integral.

The region has exact area

$$|F|=\frac14-\frac12(1-b_0)^2=\frac1{12}+\frac{\sqrt2}{9}.$$

The old constant menu revenue is `136719583/250000000`. Consequently the exact gain is

$$
\Delta_F=|F|\left(\frac49+\frac{2\sqrt2}{27}-\frac{136719583}{250000000}\right)
=\frac{1925713777}{243000000000}-\frac{11719583}{2250000000}\sqrt2>0.
$$

This is approximately 0.000558528842850313. No factor two belongs here: only bidder 1 changes, and F already includes both item orientations. The gain adds to the separately proved lottery-strip extension because the old conditional menu on F is unchanged by that extension.

## 4. Preservation of the other screening certificates

Every Q screened menu has zero utility and zero allocation on F. The old Q capacity measure also assigns F zero mass in both coordinates: its volume prices lie above the candidate's no-sale boundaries and its edge part lies at safe value one. Since b0 is below every constrained-Q bundle price and both F coordinates are below its singleton prices, F is contained in those zero regions. Thus arbitrary changes of the other bidder's capacity on F leave the Q pairing unchanged. The old Q menu remains feasible and retains its matching global inner bound.

For an extended lottery opponent type `(t,rho)` with rho<c, the former bidder-1 menu on F assigns its high item whenever t>2/3. The new SJA menu keeps that high item and may add the safe item if rho exceeds b0-2/3. Residual capacity can only decrease there. The current screened lottery menu is empty on F by Section 1. Thus any full-inner upper certificate for the previous residual remains an upper bound for the reduced residual, while the same menu still attains it. This proves preservation of full-inner optimality once the independent E-plus certificate is applied; it does not assume that safe capacity stays globally one after this change.

The reverse statement is also useful: after this change bidder 1 is itself globally empty at every own report in F. Every one of its retained, lottery, and SJA menus has that property. Bidder 2 already uses the SJA menu whenever its opponent belongs to F. Hence both bidders have a full-capacity optimal conditional section on F.

No global auction optimality is asserted. New outer bundle-competition changes may alter the remaining certified regions and require a new support check.
