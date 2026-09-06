# Full conditional certificates and their surviving scope

The following claims concern the actual residual of the specified complete
mechanism. They quantify over every measurable randomized pointwise DSIC/IR
conditional competitor, not over the displayed menu family. They do not
assert a common two-bidder certificate.

Write `A=2/3`, `b=91/100`, `c=137/500`, `q=113/500`,
`T=613/750`, `b0=(4-sqrt(2))/3`, and

- `F={max(w)<=1/2, sum(w)<=b0}` (closed).
- `Q={max(w)<=A, sum(w)<=b}` (closed).
- `Eplus={A<max(w)<T, min(w)<c}`; the min=c face is retained.

## Reference before the final corner release

For `outer_bundle_reoptimized.mechanism`:

| Opponent region | Bidder | Full inner optimizer | Support |
|---|---:|---|---|
| F | Both | Single-buyer menu `(A,A,b0)` at full capacity | Inherited SJA theorem, actual global no-sale proof |
| Q | 2 | Retained Q menu unless total exceeds its bundle price; then bundle becomes total, with coupled safe price in constrained rows | Inherited Q support plus new diagonal anchor theorem |
| Eplus | Both | Five-option menu in the lottery certificate | New volume, top-edge, and y=c junction measure |

The F/G bundle transfer changes the residual, so the old Q proof cannot be
reused verbatim on the reopened part. The new anchor measure is essential.
For a reopened constrained row with `t=max(w)>1/2`, `z=sum(w)`,
`k=t-q`, and `C0=5/6+3k^2/4`, the complete optimal response is
`(A,z-k,z)` when z>C0. Its matching coefficient is `m=2(z-C0)`.
For max(w)<=1/2, the response is `(A,A,max(b0,z))`.

## Final corner-release mechanism

The final mechanism uses `epsilon=9/10000`,
`J=[7/10,71/100]`, `W=J x [0,1/5]`, and
`S=[7/10-4epsilon,71/100] x [c-2epsilon,c+4epsilon]`
in the fixed physical orientation of its proof.

The full F and Q certificates survive. The final trial deliberately
releases part of an Eplus junction and changes some Eplus menus, so Eplus
needs the following exclusions:

- For bidder 1, retain the Eplus inner claim only outside the changed
  opponent rectangle S. Neither coordinate of a report in W equals c or
  one. Thus neither item orientation of its priced top and y=c own-report
  traces meets W.
- For bidder 2, a sufficient conservative exclusion is every Eplus opponent
  whose high coordinate lies in
  `[7/10-4epsilon,71/100+epsilon]`. This covers the whole possible release
  of the y=c occupied trace, including opponents outside W. The reverse
  physical orientation could be kept more sharply, but is not needed here.

No full conditional-optimality claim is made on excluded fibers. A
universal support inequality remains valid there, but the old equality
conditions no longer follow.

## Why Q survives the joint release

At an own bidder-1 report w in Q and opponent v=(x,y) in S, the reference
bidder 1 cannot buy physical item 1: its singleton price exceeds A. A
bundle costs more than b. Below c an Eplus lottery is either dominated by
the high singleton or has utility at most `sum(w)-x-c<0`. Thus only
physical item 2 can be released by the entry fee.

If y<c, its safe singleton price is at least 1/2; a positive purchase
implies w2>1/2, hence `k=w2-q>c>y`. If y>=c, its retained safe price is at
least `1/2+y-c`, so again positive purchase implies k>y. Equality at zero
utility selects empty. Consequently every release is at an aligned
scarce own coordinate y<k, with the safe coordinate x strictly between
zero and one. The scarce volume density is zero there; the priced top
and bottom edges are absent. The anchor's vertical line prices the other
item, so it is unaffected. The final bidder-2 lottery-price change has
opponent in W, disjoint from Q. All Q candidate choices and priced
capacity saturations therefore persist.

This argument was checked independently by the inner-certificate route.
The report-region map is a structural reduction, not a classification of
all globally optimal auctions.
