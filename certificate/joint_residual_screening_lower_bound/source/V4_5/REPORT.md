# V4.5: lotteries from residual geometry, with revised capacity supports

V4.5 produces a complete pointwise feasible randomized DSIC/IR auction with exact revenue

$$
R_{4.5}=R_{4.02}+\frac{472617707798758460108653}{101062797120000000000000000000},
$$

and an independently checked enclosure

`0.875254527439813321170777 <= R_4.5 <= 0.875254527439813321170782`.

The new result is an actual-residual lottery improvement beyond Q, together with exact changes to the dual support and local exclusion tests. The new five-option menu is not certified as the full inner optimizer. There is no matching unrestricted auction upper bound.

## 1. A residual constraint that requires a different menu direction

Keep the actual V4.02 split cost `s=142/125`, with

$$a=159/250,\quad b=91/100,\quad c=b-a=137/500,\quad d=s-a=1/2,\quad q=s-b=113/500.$$

Fix an opponent report `(t,rho)` with `t>2/3` and `rho<=b-t`, aligning the first item with its high coordinate. The opponent can receive only that item; the second item is free. Its possible first-item occupation is contained in

$$
\{y\le d,\ x\le t,\ x+y\le t+c\}
\ \cup\ \{y\ge d,\ x\le t-q\}.
$$

These are inequalities on the full continuous report square. Frozen menu increments may shrink the hole. At low safe-item values there are actual occupied reports with `2/3<x<t`, so continuing the old Q singleton price `2/3` beyond Q is infeasible. This does not imply the current conditional menu is optimal or that only an outer allocation change can help.

Write its four deterministic prices as `A=t`, `B=d+delta`, `C=t+c+delta`. The deterministic singleton boundary is pinned at `x=t`. The binding corner `(t,c)` nevertheless permits a new allocation

$$L=(1,\beta),\qquad p_L=t+\beta c.$$

Its utility plane passes through that corner. It is feasible whenever

$$0<\beta<1,\qquad \beta(q+\delta)\le q.$$

In the possible occupation hole it loses to empty or the safe singleton. Prioritizing those options at ties proves pointwise feasibility. The lottery allocates the high item surely and the other item with probability beta; its second item is available in every realized outcome.

## 2. The complete revenue variation determines its parameters

The new lottery wins precisely on the interior of

$$c<y<Y=c+\frac{\delta}{1-\beta},\qquad x>t-\beta(y-c).$$

The feasibility condition implies `Y<=B`. Integrating revenue over all affected buyers, including bundle buyers who switch to the lottery, gives

$$
\Delta_L=\frac{\delta^2}{2}\bigl[(3t-2)z-\delta z^2\bigr],\qquad z=\frac{\beta}{1-\beta}.
$$

The derivative at beta zero is positive for every `t>2/3`, `delta>0`. Thus the four-option stationary menu fails unrestricted conditional optimality by an explicit feasible improvement. This conclusion does not rest on a failed dual fit.

Optimizing this variation gives `z=(3t-2)/(2delta)`. Optimizing the bundle parameter jointly, rather than holding its old stationary value fixed, gives

$$
\delta(t)=\frac9{16}(T-t)(U-t),\qquad
T=\frac{613}{750},\quad U=\frac{839}{750},
$$

$$\beta(t)=\frac{3t-2}{3t-2+2\delta(t)}.$$

These formulas are admissible on `2/3<t<T`. Their simplicity uses the actual equality `d=1/2`. The intermediate allocation is fixed within each conditional menu but varies with the opponent report. The full mechanism therefore allows a continuum of lottery probabilities; no finite global allocation-range assumption is made.

Define the opponent region

$$E=\{w:2/3<\max(w)<613/750,\quad w_1+w_2\le91/100\}.$$

It has area `791/15625=0.050624`. For **each bidder**, when its opponent lies in E, replace its complete conditional menu by the following options, in tie priority order:

| Option | Aligned allocation | Payment |
|---|---|---|
| Empty | `(0,0)` | `0` |
| Safe singleton | `(0,1)` | `d+delta(t)` |
| Scarce singleton | `(1,0)` | `t` |
| Bundle | `(1,1)` | `t+c+delta(t)` |
| Lottery | `(1,beta(t))` | `t+beta(t)c` |

Outside E retain that bidder's full V4.02 rule. The faces `t=2/3` and `t=T` retain the old mechanism explicitly. Rotate the menu into physical item coordinates according to the opponent's unique high coordinate.

Complete menu maximization proves pointwise DSIC against every misreport and IR. The rational Borel parameter functions and finite priority prove measurability. Payments are nonnegative and at most reported allocated value. Joint feasibility requires more than two separate best-response arguments: when both reports lie in E, simultaneous lotteries are impossible; equal item orientations allocate only to the strictly larger high report, and opposite orientations allocate distinct items. The reverse splice against bidder 2's inherited Q menu is also checked separately. The full proof and an independent all-real audit cover these cases and all ties.

For example, at reports `(0.7,0.1)` and `(0.72,0.29)`, the old allocation is empty for bidder 1 and item 1 for bidder 2. The new bidder-2 allocation is `(1,3125/4852)` with payment `85053/97040`. This lottery is selected strictly on a positive-volume set.

Let `q_old=227/1000` and

$$\delta_{\rm old}(t)=\max(0,1/2-c+3q_{\rm old}^2/4-3q_{\rm old}t/2).$$

Before its old cutoff, the conditional gain is

$$g_1(t)=(\delta-\delta_{\rm old})^2+\delta_{\rm old}(3t-2)^2/8;$$

afterwards it is `g_2(t)=delta(t)^2`. Integrating `2(b-t)g(t)` over t accounts for both item orientations of one changed bidder. Applying the valid splice to both bidders doubles that gain exactly. Independent halfplane clipping and dictionary-polynomial integration reproduce the displayed rational increment. The exact total revenue is the frozen V4.02 algebraic/logarithmic expression plus this rational number.

## 3. Successful conditional certificates still eliminate directions

The complete bidder-2 inner optimum on

$$Q=\{w:\max(w)\le2/3,\quad w_1+w_2\le91/100\}$$

survives the two-sided change. On these fibers the reverse splice can only release scarce capacity at bidder-2 reports with scarce coordinate below c and safe coordinate between `2/3` and T. The old Q measure gives this released set zero mass. The inherited Q menu remains feasible and still attains its unchanged full randomized upper bound. Thus this is a certificate at the **new actual residual**, not merely the old V4.02 residual.

The new lottery also has a sharper local test. Add a slightly higher second-item probability, with its price adjusted so that it crosses the old lottery at `y0` in `(c,Y)`. The complete first revenue variation is

$$-\frac{\beta}{2}(y_0-c)(Y-y_0)^2<0.$$

This sign is independently derived from utility integration and from payments on all moved cells. The tempting opposite perturbation lowers its price below the supporting corner and violates actual capacity near `(t,c)`. These facts exclude particular nearby trace changes. They do not rule out all further lotteries, lower first-item probabilities, or a complete redesign of the inner menu.

## 4. Common prices: an obstruction, two exact repairs, and a new restriction

A common nonnegative capacity price pi gives the weak upper expression

$$U(\pi)=\langle\pi,1\rangle+\sum_i\sup_{M_i}\{R_i(M_i)-\langle\pi,x_i\rangle\}.$$

A necessary condition for equality is that each bidder's consumed-price measure has an opponent marginal absolutely continuous with respect to the opponent type law. Otherwise it can replace its whole menu by empty on an opponent-null set, preserving revenue and strictly improving its priced objective.

The existing Q top-edge support violates this condition when reused verbatim as a common price. It charges bidder 1 on opponent-null faces with total mass

$$M=\frac{11884909837073}{6075000000000000}>0.$$

Any nonnegative completion retaining that support has Lagrangian slack at least M at the candidate. This is a quantified failure of that architecture. It is not proof that a different common measure does not exist, and the null-face deletion itself has zero revenue gain.

There is an exact repair. In an aligned Q fiber write the existing tail as F, with `F'=-f` and `F(0)=F(1)=0`. The pointwise IC envelopes give

$$\int F(x)a_1(x,1)dx=\int F(x)a_1(x,z)dx+\int\!\int_z^1 f(x)a_2(x,y)dy\,dx.$$

Average over `z in [5/6,1]`. The edge price becomes an interior density `6F(x)` on that band, and item 2 gains the term `6(y-5/6)_+ f(x)`. The combined item-2 density remains nonnegative. The exact identity

$$\langle\pi,r\rangle-R=\langle\pi,r-a\rangle+3\int_{D_0}u$$

is preserved for every randomized DSIC/IR competitor. The actual candidate saturates the new support. This is an exact redistribution, not approximate smoothing.

Alternatively, move only the consumed edge segment `x<k`. Integration by parts forces an additional **junction measure** `F(k)6(y-5/6)_+ delta_{x=k}dy`. It is nonnegative and tight. The harmless remainder of the top-edge measure stays. Both constructions remain matching on Q after the two-sided lottery splice, because the changed allocation lies outside their supports.

Neither repaired support has been proved to support both bidders. In particular, concentrating the repair in a band of width `1/1000` fails a positive-measure conditional menu-deletion test, leaving a proved Lagrangian gap at least `15635863/240000000000`. This excludes that narrow-band architecture and does not exclude the broader support.

For the new genuine lottery region L, any matching nonnegative inner capacity measure must obey

$$\pi_{\rm safe}(L)=0,$$

because safe-item capacity is one while its allocation is strictly between zero and one. This excludes singular charges on L as well as positive densities. Tight incentive transport must therefore account for the lottery region without leaving a positive safe-item capacity coefficient there. A matching system of such transports and junction measures remains to be constructed.

## 5. Functional exchange thresholds were tested as complete mechanisms

Two separate admissible trials use `h(y)=y+q+e(y)` and `h(y)=y+q-e(y)`, with inverse exchange thresholds and a localized piecewise-affine tent e supported on `[.29,.39]`. Its concrete height is `.001`; all slopes have magnitude `.02`.

Both trials are complete pointwise DSIC/IR and feasible mechanisms, and each fully reoptimizes bidder 2 on Q under its changed residual. Their exact revenue-variation formulas integrate over all complete conditional menus that must move together. Floating quadrature suggests losses for both tested continuations, including the cost of their bundle-junction or outside-Q changes. Those signs are discovery evidence, not certified global losses or a theorem against functional thresholds. The trial mechanisms are retained separately and are not combined with the new incumbent without a joint proof.

## 6. Remaining target

The incumbent improves and the full randomized Q certificate survives. Beyond Q, E is now known to admit a lottery improvement, but its full inner optimum remains open. The common-support search has exact rejection tests, repaired regional measures, and new zero-price requirements. It still lacks a common measure and tight incentive-flow system supporting both bidders everywhere.

The inherited unrestricted upper remains `3715139591287203/4194304000000000`, approximately `0.8857583025186546`. It is unchanged and not newly fully recertified here. The new lower does not meet it. The allocation boundaries, rents, and prices have been made more consistent locally; unrestricted optimality and the requested exact optimal mechanism remain unresolved.
