# A localized trace kink that cannot improve the new lottery menu

This is a targeted analytic test of one remaining direction, not a
lottery classification or an unrestricted optimality proof. It uses the
actual V4.02 residual on the region E specified in
`residual_lottery_extension.md`; the same argument applies after the
two-sided splice because the relevant other row is unchanged at the
capacity-hole witness.

Write the selected menu parameters as `t,c,delta,beta`, and put

`p=t+beta*c`, `B=d+delta`,
`Y=c+delta/(1-beta)`.

The candidate's lottery `(1,beta)` wins between y=c and y=Y. The exact
stationarity relation already derived from complete menu revenue is

`2*beta*(Y-c)=3t-2`.                                      (1)

## 1. A second, higher-slope lottery

Choose any interior anchor `c<y0<Y`. Keep every existing option, and add

`allocation (1,beta+epsilon)`, `payment p+epsilon*y0`,

for epsilon positive and sufficiently small. Its utility exceeds the old
lottery's utility exactly above y0. This is a complete, pointwise
admissible conditional perturbation whenever

`epsilon < min(1-beta, [q-beta*(q+delta)]/(B-y0))`.           (2)

The margin in the numerator is strictly positive in the open band E.
At the cap corner `(t,c)` its price exceeds the supporting-corner price
by `epsilon*(y0-c)>0`. At the other binding cap point `(k,B)`, the
margin is `q-beta*(q+delta)-epsilon*(B-y0)>0`. The affine cap-hole edges
are then controlled by their endpoints; empty and low-singleton priority
handle ties as in the original proof. Inequality (2) also ensures the
new bundle/lottery junction stays below B.

The first variation must include the buyers moved at the new purchase
boundary and at the bundle boundary. Put `h=Y-y0` and
`W=1-p+beta*Y`, the sales width at the old upper junction. The three exact
first-order payment contributions are:

- `y0*(W*h-beta*h^2/2)`: higher payments from old lottery buyers;
- `p*h^2/2`: newly served buyers along the purchase boundary;
- `-Y*W*h`: the payment loss when bundle buyers switch to the new lottery.

Their sum is

`D = h^2/2 * [3p-2-beta*y0-2beta*Y]`
`  = h^2/2 * [3t-2-beta*(y0-c)-2beta*(Y-c)]`
`  = -beta*(y0-c)*(Y-y0)^2/2 < 0`,                         (3)

where the last equality uses (1). This independent payment calculation
agrees with a boundary-trace revenue-envelope calculation. Thus this
particular localized higher-slope trace kink is strictly unprofitable
to first order at every interior anchor. At y0=c the derivative is zero
because the perturbation becomes the already optimized uniform beta
direction; at y0=Y its affected interval has zero length.

## 2. The reverse kink violates actual capacity

The superficially opposite perturbation has allocation `(1,beta-epsilon)`
and payment `p-epsilon*y0`. At `(t,c)` its utility is
`epsilon*(y0-c)>0`, whereas the existing menu's maximal utility is zero.
It is necessary to check the **actual** residual here, rather than rely
on a conservative majorant of its hole.

Take the actual report `(x,y)=(t-eta,c)` with

`0<eta<min(t-2/3, epsilon*(y0-c))`.

Because x>2/3 and the second coordinate equals c, the frozen V3 joined
high-singleton price is exactly x and its high-item increment is zero.
The new split-cost base price is also x: its pivot is `x-a` and
`min(a,s-c)=a`. Bidder 1, with report `(t,rho)` in E, buys that item
with strict utility eta and cannot buy the low item or the bundle.
This remains true after the two-sided splice: the opponent sum
`x+c>b` means its row is not replaced there.

At this actual occupied-capacity report the added reverse lottery has
utility `-eta+epsilon*(y0-c)>0`. Every existing bidder-2 option has
nonpositive utility. The reverse lottery therefore uniquely wins and
allocates item 1 with probability one while bidder 1 already owns it.
This is a strict actual-capacity violation, not a tie problem. The
attached verifier checks explicit rational instances, including one
stored witness; the argument covers every real parameter satisfying the
displayed strict inequalities.

## 3. Consequence and scope

The higher-slope anchored direction is feasible but locally loses
revenue; its lower-slope counterpart is infeasible in the actual
residual. These facts remove a concrete family of possible extra
lottery regions and prevent unnecessary subdivision of the new menu.
They do not exclude changes with first-item probability below one,
multiple moving anchors, nonlocal changes, simultaneous changes of the
outer allocation, or a different full conditional mechanism. No full
inner capacity-price measure follows from these two tests alone.
