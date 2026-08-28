# Stronger exact piecewise-surcharge lower mechanism

This formal certificate package certifies a deterministic, ex-post-feasible,
DSIC, ex-post-IR mechanism with exact expected revenue

\[
\boxed{\frac{26237753173862063}{30000000000000000}}
=0.8745917724620687\ldots.
\]

It strictly improves the active predecessor
`26232788323031183/30000000000000000` by

\[
\frac{10343439231}{62500000000000}=0.000165495027696.
\]

This is a primal lower bound only.  It is not a global optimality claim.

## Mechanism

Start from the exact affine-maximizer mechanism with

\[
a=159/250,\qquad b=91/100,\qquad s=1137/1000.
\]

For an opponent report `q`, retain its four-option taxation menu and add the
same nonnegative fee to all three nonempty prices.  Write
`t=max(q1,q2)` and `rho=min(q1,q2)`.  The fee is the first matching row below;
if no row matches, it is zero.  Closed-row endpoint overlaps use table order.

| id | conditions | fee |
|---|---|---:|
| Z1 | `53/100 <= t <= 11/20`, `0 <= rho <= b-t` | `3/500` |
| Z2 | `11/20 <= t <= 57/100`, `0 <= rho <= b-t` | `13/1000` |
| Z3 | `57/100 <= t <= 59/100`, `0 <= rho <= b-t` | `21/1000` |
| Z4 | `59/100 <= t <= 61/100`, `0 <= rho <= b-t` | `29/1000` |
| Z5 | `61/100 <= t <= 159/250`, `0 <= rho <= b-t` | `19/500` |
| S1 | `159/250 <= t <= 13/20`, `0 <= rho <= b-a` | `39/1000` |
| S2 | `13/20 <= t <= 133/200`, `0 <= rho <= b-a` | `31/1000` |
| S3 | `133/200 <= t <= 17/25`, `0 <= rho <= b-a` | `23/1000` |
| S4 | `17/25 <= t <= 139/200`, `0 <= rho <= b-a` | `3/200` |
| S5 | `139/200 <= t <= 71/100`, `0 <= rho <= b-a` | `7/1000` |

The Z rows occupy the zero-pivot one-high triangular chamber.  In one
orientation their base prices are

\[
(A,B,C)=(s-t,a,b),\qquad 0\le\rho\le b-t.
\]

The S rows are a genuinely additional affine chamber, where a singleton of
the opponent sets the pivot.  In one orientation their base prices are

\[
(A,B,C)=(t,s-a,t+b-a),\qquad 0\le\rho\le b-a.
\]

The table is symmetric under swapping the two item coordinates and is used by
both bidders.

## Pointwise incentive and feasibility proof

For every fixed opponent report, the displayed rule adds one common amount to
all nonempty options of the bidder's taxation menu.  It therefore preserves
the ranking of all nonempty bundles.  Relative to the feasible base
affine-maximizer allocation, each bidder either keeps exactly their base
bundle or selects the zero-price opt-out.  The final allocation is consequently
an itemwise subset of the base allocation at every report profile.

Thus the rule is pointwise ex-post feasible.  It is DSIC because each bidder
chooses a utility-maximizing bundle from a menu depending only on the opponent,
and it is ex-post IR because opt-out is always available.  The stated first-row
boundary rule makes the surcharge Borel and single-valued everywhere; all
integration-boundary choices have measure zero.

## Exact revenue

For an active subadditive menu, the exact conditional revenue is

\[
r(A,B,C)=A(1-A)(C-A)+B(1-B)(C-B)
+C\left[(1-C+B)(1-C+A)-\frac{(A+B-C)^2}{2}\right].
\]

The symbolic verifier reconstructs this polynomial, checks the entire price
regime, and integrates each rational band.  Including two item orientations
and two bidders, the exact gains are

\[
G_Z=\frac{14055427773}{125000000000000},\qquad
G_S=\frac{9541919439}{125000000000000},
\]

so

\[
G_Z+G_S=\frac{5899336803}{31250000000000}.
\]

Adding the hash-bound affine base revenue gives the boxed result above.

## Independent replay and discovery boundary

Run from this directory:

```powershell
python verify_piecewise_surcharge.py
python independent_replay.py
Get-FileHash -Algorithm SHA256 manifest.json,README.md,verify_piecewise_surcharge.py,verification_output.txt,independent_replay.py,independent_replay_output.txt
```

The second script imports no code from the first.  It evaluates the scalar menu
formula using `Fraction`, checks the fifth forward difference is zero on every
band, and applies exact five-point Boole quadrature.  The committed transcripts
and `SHA256SUMS.txt` bind both paths.

Numerical chamber probes were used only to choose rational bands.  They suggest
that the remaining bundle-pivot one-high chamber may add roughly another
`7e-6` in revenue, but that two-dimensional candidate has not been converted to
an exact certificate and is not included in this bound.  Simple one-fee
triangular extensions reached only about `0.8745022`; the exact improvement here
comes from five fees in that chamber plus five fees in the new singleton-pivot
chamber.

Against the active exact global upper bound

\[
\frac{18588262788621}{20971520000000},
\]

the remaining exact gap is

\[
\frac{1445765276937161827}{122880000000000000000}
=0.011765667943824559\ldots.
\]
