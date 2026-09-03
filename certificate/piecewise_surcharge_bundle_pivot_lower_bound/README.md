# Combined twenty-band and bundle-pivot surcharge lower certificate

This sealed package certifies a deterministic, pointwise ex-post-feasible,
DSIC, ex-post-IR mechanism with exact expected revenue

\[
\boxed{\frac{83961603016753854879913}{96000000000000000000000}}
=0.8746000314245193216657604166\ldots .
\]

It strictly improves the independently sealed twenty-band predecessor
`../piecewise_surcharge_twenty_band_lower_bound/` by

\[
\frac{70946101529751}{10240000000000000000}
=0.00000692833022751474609375>0.
\]

This is a primal lower bound only, not a global-optimality claim.

## Combined mechanism

Start from the exact affine-maximizer mechanism with

\[
a=159/250,\qquad b=91/100,\qquad s=1137/1000.
\]

For each opponent report, first test the twenty closed Z/S rows specified in
the hash-bound predecessor manifest.  If none matches, test the bundle-pivot
rows below.  The first matching row adds its common nonnegative fee to all
three nonempty prices of the base taxation menu; otherwise the fee is zero.
The zero-price opt-out is unchanged.

For the extension, order the opponent coordinates as

\[
t=\max(q_1,q_2),\qquad \rho=\min(q_1,q_2),\qquad u=t+\rho.
\]

Set

\[
c=b-a=137/500,\quad d=s-a=501/1000,\quad
e=s-b=227/1000,\quad k=c+d=31/40.
\]

The bundle-pivot chamber is

\[
91/100\le u\le1,\qquad c\le\rho\le u-d.
\]

Its normalized coordinate is

\[
r=\frac{\rho-c}{u-k}\in[0,1].
\]

Band $i$ is
$u\in[91/100+(i-1)/200,\,91/100+i/200]$, and strip $j$ is
$r\in[(j-1)/8,j/8]$.  The following vectors list the fees for strips
$j=1,\ldots,8$; zero entries mean no extension fee.  Bands 15--18 are all
zero and are omitted.

| band | $u$-interval | strip-fee vector $j=1,\ldots,8$ |
|---:|---:|---|
| B1 | `[91/100,183/200]` | `383/10000, 39/1250, 243/10000, 177/10000, 113/10000, 13/2500, 0, 0` |
| B2 | `[183/200,23/25]` | `353/10000, 139/5000, 103/5000, 137/10000, 71/10000, 1/1250, 0, 0` |
| B3 | `[23/25,37/40]` | `323/10000, 49/2000, 17/1000, 49/5000, 29/10000, 0, 0, 0` |
| B4 | `[37/40,93/100]` | `147/5000, 53/2500, 67/5000, 59/10000, 0, 0, 0, 0` |
| B5 | `[93/100,187/200]` | `33/1250, 179/10000, 49/5000, 1/500, 0, 0, 0, 0` |
| B6 | `[187/200,47/50]` | `47/2000, 147/10000, 31/5000, 0, 0, 0, 0, 0` |
| B7 | `[47/50,189/200]` | `103/5000, 57/5000, 13/5000, 0, 0, 0, 0, 0` |
| B8 | `[189/200,19/20]` | `177/10000, 41/5000, 0, 0, 0, 0, 0, 0` |
| B9 | `[19/20,191/200]` | `37/2500, 49/10000, 0, 0, 0, 0, 0, 0` |
| B10 | `[191/200,24/25]` | `3/250, 17/10000, 0, 0, 0, 0, 0, 0` |
| B11 | `[24/25,193/200]` | `91/10000, 0, 0, 0, 0, 0, 0, 0` |
| B12 | `[193/200,97/100]` | `63/10000, 0, 0, 0, 0, 0, 0, 0` |
| B13 | `[97/100,39/40]` | `7/2000, 0, 0, 0, 0, 0, 0, 0` |
| B14 | `[39/40,49/50]` | `7/10000, 0, 0, 0, 0, 0, 0, 0` |

All listed positive-fee cells are closed and are tested in manifest order;
every unlisted grid cell has the default zero fee.  Endpoint overlaps have
measure zero.  On the only boundaries shared with predecessor support, the
predecessor-first rule is the literal pointwise rule.

## Bundle-pivot chamber and separation proof

In this chamber the affine pivot is $H=u-b$.  Indeed, $u\ge b$,
$\rho\ge b-a=c$, and $t\ge d>c$, so $u-b$ dominates the other three
pivot candidates.  The price minima also have fixed branches, giving

\[
(A,B,C)=(u-c,\rho+e,u).
\]

At every cell vertex the verifier reconstructs these prices from the original
max/min menu and checks, both before and after adding the fee,

\[
0\le B\le A\le C\le1,\qquad C\le A+B.
\]

After substituting $\rho=c+r(u-k)$, each checked price-regime inequality is
multi-affine in $(u,r)$.  Its extrema on a rectangular grid cell occur at the
four corners, so the vertex checks cover the entire cell.

The extension has no positive-measure overlap with the twenty-band component.
Every zero-pivot Z row satisfies
$\rho\le b-t$, equivalently $u\le b$, whereas every bundle-cell interior
has $u>b$.  Every singleton-pivot S row satisfies $\rho\le b-a=c$, whereas
every bundle-cell interior has $\rho>c$.  Thus intersections occur only on
$u=b$ or $\rho=c$, and the declared predecessor-first order resolves them.

## Pointwise DSIC, IR, and feasibility

For each fixed opponent report, the rule adds one common fee to every nonempty
menu option.  It preserves all rankings among nonempty bundles.  Relative to
the feasible affine-maximizer allocation, a bidder therefore either keeps the
base bundle or opts out.  The final allocation is an itemwise subset of the
base allocation at every report profile.  Feasibility follows by deletion;
taxation gives DSIC; and the available opt-out gives ex-post IR.  The finite
rational semialgebraic rule is Borel measurable.

## Exact integration and independent replay

For ordered opponent coordinates, the change

\[
(u,r)\longmapsto
(t,\rho)=\bigl(u-c-r(u-k),\ c+r(u-k)\bigr)
\]

has absolute Jacobian $u-k$.  A factor two accounts for the two item
orientations, and a second factor two accounts for the two symmetric bidders.
The primary verifier reconstructs the conditional revenue polynomial and
integrates it directly in $(u,\rho)$.  It obtains the exact extension gain

\[
G_B=\frac{70946101529751}{10240000000000000000}.
\]

The independent replay imports neither the primary verifier nor any discovery
code.  It uses the scalar menu formula in $(u,r)$; the displayed polynomial
composition has degree at most four in $u$ and three in $r$ on the verified
price region. Exact forward differences serve only as consistency checks;
the analytic composition supplies the degree bounds needed for tensor exact
Boole quadrature. Both implementations
reproduce every one of the 41 positive-cell gains and their sum.

Run from this directory:

```powershell
python -B -X utf8 verify_combined_surcharge.py
python -B -X utf8 independent_replay.py
```

Do not use `python -O`: both implementations use `assert` as a proof-obligation
check.  The manifest binds the affine base, the twenty-band predecessor, and
the current upper certificate by SHA-256.  The committed transcripts and
`SHA256SUMS.txt` bind both local implementations.  Numerical searches selected
the rational cells and fees, but no research or numerical file is a verifier
input.

Against the current exact global upper bound

\[
\frac{3715139591287203}{4194304000000000},
\]

the remaining exact gap is

\[
\frac{34278208801183528608409}{3072000000000000000000000}
=0.01115827109413526321888313802\ldots .
\]
