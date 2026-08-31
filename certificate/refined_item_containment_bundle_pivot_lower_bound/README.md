# Bundle-pivot plus refined item-containment lower certificate

This sealed package certifies a deterministic, pointwise ex-post-feasible,
DSIC, ex-post-IR mechanism with exact expected revenue

\[
\boxed{\frac{83962078694672281756033}{96000000000000000000000}}
=0.8746049864028362682920104166\ldots .
\]

It starts from the hash-bound sealed bundle-pivot predecessor and adds the
eight exact non-common item-containment cells in `manifest.json`.  Their exact
gain is

\[
\frac{3963982653557301}{800000000000000000000}
=0.00000495497831694662625>0.
\]

This is a primal lower bound only, not a global-optimality claim.  Numerical
grid searches selected the rational cells and surcharges, but neither verifier
uses numerical evidence.

## Pointwise mechanism

Let

\[
t=\max(q_1,q_2),\qquad \rho=\min(q_1,q_2),\qquad
c=137/500,\qquad d=501/1000.
\]

First evaluate the sealed predecessor's ordered rule.  Its twenty-band common
fee rows are tested before its bundle-pivot rows.  If the first matching row is
`S5.1` or `S5.2`, test the item rows in listed order, where every interval is
open on the left and closed on the right.  On the unique matching item row,
add its `delta` to the price of the singleton corresponding to the opponent's
`rho` coordinate and to the grand bundle.  Leave the other singleton price
unchanged.  At `t=139/200` no item surcharge is applied.  Outside these eight
cells the predecessor menu is unchanged.

The predecessor assigns the shared boundary `rho=c` to its twenty-band S row,
so the item rule applies there when its `t` interval matches.  A bundle-pivot
row is reached only after all S rows fail and therefore has positive-measure
interior `rho>c`.  Thus the two extensions have disjoint interiors and a
complete pointwise first-match rule.

Tie-breaking is deterministic.  If maximum utility is zero, select the empty
outcome.  At positive maximum utility, retain the predecessor-selected outcome
when it remains maximizing; otherwise select the maximizing itemwise subset
with smallest outcome id under the predecessor's fixed outcome order.

## Deletion-containment lemma

Fix an opponent report in an item cell.  After its common fee `f`, write the
predecessor menu prices as

\[
(A,B,C)=(d+f,t+f,t+c+f).
\]

The item rule changes them to `(A+delta,B,C+delta)`.  Every row verifies the
full price regime and

\[
0<\delta<A+B-C=d-c+f.
\]

Let `h=A+B-C`.  If the predecessor chose the changed singleton, preference
over the empty outcome gives its value at least `A`, while preference over the
bundle bounds the other item value by `C-A`.  Its utility lead over the
unchanged singleton is therefore at least `h`; after the surcharge the lead is
at least `h-delta>0`.  Its ranking against the bundle is unchanged because
both prices rise by the same amount.  Hence it can only remain that singleton
or delete it and opt out; it cannot switch across items.

If the predecessor chose the unchanged singleton, its utility is unchanged
while the two changed options lose `delta`, so deterministic retention keeps
that singleton.  A predecessor bundle buyer may move only to one of its
subsets, and an opt-out cannot enter because no nonempty price falls.  The new
outcome is therefore an itemwise subset of the predecessor outcome for every
bidder and every report profile.

The predecessor is pointwise feasible, so simultaneous itemwise deletion
preserves feasibility.  Each fixed opponent report defines a taxation menu
whose rule selects a utility maximizer; this proves DSIC.  The zero-price empty
option and the zero-utility rule prove ex-post IR.

## Exact revenue and replay

For a menu `(0,A,B,C)` let `R(A,B,C)` be its exact expected payment from an
independent uniform bidder.  On an item row the exact incremental revenue is

\[
4c\int_{t_0}^{t_1}
\bigl[R(A+\delta,B,C+\delta)-R(A,B,C)\bigr],dt.
\]

The factor four is two ordered-coordinate orientations times two symmetric
bidders; `c` is the exact length of the `rho` interval.  The primary verifier
uses a closed symbolic polynomial for `R`.  The non-importing replay instead
constructs every demand region by exact rational polygon clipping, verifies
the integrand degree by forward differences, and integrates it by exact Boole
quadrature.  It imports no code from the primary verifier.

Run from this directory:

```powershell
python -B -X utf8 -I verify_final_combined.py
python -B -X utf8 -I independent_replay.py
```

The eight deltas were discovered on a rational `1/100000` grid.  They are not
all at the `C+delta<=1` cap; both verifiers check every row's slack and price
regime exactly.  The remaining exact gap to the current hash-bound upper is

\[
\frac{34262987107793868572569}{3072000000000000000000000}
=0.0111533161158183165926331380\ldots .
\]
