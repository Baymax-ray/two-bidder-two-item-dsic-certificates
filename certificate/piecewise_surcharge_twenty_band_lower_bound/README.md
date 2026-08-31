# Exact twenty-band piecewise-surcharge lower mechanism

This sealed package certifies a deterministic, pointwise ex-post-feasible,
DSIC, ex-post-IR mechanism with exact expected revenue

\[
\boxed{\frac{2623779309282875420759}{3000000000000000000000}}
=0.874593103094291806919666\ldots .
\]

It strictly improves the preserved ten-band predecessor
`../piecewise_surcharge_lower_bound/` by

\[
\frac{1330632223040253}{1000000000000000000000}
=0.000001330632223040253>0.
\]

This is a primal lower bound only, not a global-optimality claim.

## Complete mechanism

Start from the hash-bound affine-maximizer mechanism with

\[
a=159/250,\qquad b=91/100,\qquad s=1137/1000.
\]

For an opponent report $q=(q_1,q_2)$, retain the four-option base taxation
menu and add one common nonnegative fee to all three nonempty prices.  Write
$t=\max(q_1,q_2)$ and $\rho=\min(q_1,q_2)$.  Test the following closed rows
in listed order; the first match supplies the fee, and otherwise the fee is
zero.  For every Z row require $0\le\rho\le b-t$; for every S row require
$0\le\rho\le b-a$.

| id | interval for $t$ | fee | id | interval for $t$ | fee |
|---|---|---:|---|---|---:|
| Z1.1 | `[53/100,27/50]` | `233/50000` | Z1.2 | `[27/50,11/20]` | `807/100000` |
| Z2.1 | `[11/20,14/25]` | `1159/100000` | Z2.2 | `[14/25,57/100]` | `1519/100000` |
| Z3.1 | `[57/100,29/50]` | `1889/100000` | Z3.2 | `[29/50,59/100]` | `567/25000` |
| Z4.1 | `[59/100,3/5]` | `2657/100000` | Z4.2 | `[3/5,61/100]` | `1527/50000` |
| Z5.1 | `[61/100,623/1000]` | `3521/100000` | Z5.2 | `[623/1000,159/250]` | `127/3125` |
| S1.1 | `[159/250,643/1000]` | `4143/100000` | S1.2 | `[643/1000,13/20]` | `937/25000` |
| S2.1 | `[13/20,263/400]` | `3343/100000` | S2.2 | `[263/400,133/200]` | `183/6250` |
| S3.1 | `[133/200,269/400]` | `1259/50000` | S3.2 | `[269/400,17/25]` | `66/3125` |
| S4.1 | `[17/25,11/16]` | `107/6250` | S4.2 | `[11/16,139/200]` | `263/20000` |
| S5.1 | `[139/200,281/400]` | `923/100000` | S5.2 | `[281/400,71/100]` | `67/12500` |

The Z rows lie in the zero-pivot one-high chamber.  In one item orientation
their base prices and cross-section length are

\[
(A,B,C)=(s-t,a,b),\qquad b-t.
\]

The S rows lie in the singleton-pivot chamber.  Their corresponding data are

\[
(A,B,C)=(t,s-a,t+b-a),\qquad b-a.
\]

Both chambers are copied under item transposition and used for both bidders.
All endpoint overlaps have measure zero, while the listed first-row rule makes
the mechanism single-valued everywhere.

## Pointwise DSIC, IR, and feasibility

At every fixed opponent report, a common fee preserves the ranking of all
nonempty bundles.  Relative to the feasible affine-maximizer allocation, each
bidder therefore either keeps exactly the base bundle or chooses the
zero-price opt-out.  The resulting allocation is an itemwise subset of the
base allocation at every report profile.  Feasibility follows by deletion;
taxation gives DSIC; and the available opt-out gives ex-post IR.  The rule is
Borel because it has finitely many rational semialgebraic rows.

## Exact revenue calculation

For an active subadditive menu, the conditional revenue polynomial is

\[
r(A,B,C)=A(1-A)(C-A)+B(1-B)(C-B)
+C\left[(1-C+B)(1-C+A)-\frac{(A+B-C)^2}{2}\right].
\]

The primary verifier reconstructs this polynomial and integrates every row in
exact rational arithmetic.  Including both item orientations and both
bidders, the chamber gains are

\[
G_Z=\frac{113291698497241117}{1000000000000000000000},\qquad
G_S=\frac{2400553481931223}{31250000000000000000},
\]

and hence

\[
G_Z+G_S=
\frac{190109409919040253}{1000000000000000000000}.
\]

Adding the exact affine-base revenue yields the boxed lower bound.  The
manifest binds the affine base, the ten-band predecessor, and the current
upper certificate by SHA-256 before doing any arithmetic.

## Independent replay

Run from this directory, without Python optimization:

```powershell
python -B -X utf8 verify_twenty_band_surcharge.py
python -B -X utf8 independent_replay.py
```

Do not use `python -O`: both implementations deliberately use `assert` as a
proof-obligation check.  The replay imports neither the primary verifier nor
any research/discovery module.  It independently evaluates the scalar menu
formula with `Fraction`, checks exact fifth differences, and applies exact
five-point Boole quadrature.  The committed transcripts and `SHA256SUMS.txt`
bind both executions.

Numerical optimization was used only to discover the rational fees.  No
numerical candidate file is a verifier input.

Against the independently certified current upper bound

\[
\frac{3715139591287203}{4194304000000000},
\]

the remaining exact gap is

\[
\frac{34299492631642453908409}{3072000000000000000000000}
=0.01116519942436277796497688802\ldots .
\]
