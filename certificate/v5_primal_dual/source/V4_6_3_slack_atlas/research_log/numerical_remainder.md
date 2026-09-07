# Numerical remainder of the frozen upper certificate

For the unchanged amplitude-one stream and the unchanged low-square
support splice, define

\[
E=(B_{20}-B)+(D-\Delta_{1024}).
\]

The exact rational/interval computation proves the outward-rounded bounds

\[
\boxed{0.0001209011046653<E<0.0004139067520082.}
\]

The full rational endpoints are in `certificate/numerical_remainder.json`.
Against the exact frozen upper bound and the preserved V4.6.1.1 lower
revenue enclosure, E is **less than 6.41% of the current gap**. More than
0.0060449820349107 of the gap remains after this entire numerical
remainder is removed. Thus it cannot materially explain most of the
0.0064588887869... gap. No new coefficient, dual architecture, lower
mechanism, subtraction, or active upper bound is introduced here.

| Component | Certified outward-rounded interval |
|---|---:|
| B20 minus the exact stream integral B | [0, 0.0002879952477480] |
| Actual splice saving D minus Delta1024 | [0.0001209011046653, 0.0001259115042602] |
| Opponent-averaging part of the splice loss | [0.0000856859264952, 0.0000906970737044] |
| Own-cell Jensen and omitted-cell part | [0.0000352144305557, 0.0000352151781702] |

The opponent-averaging term persists even if the own-type 1024 partition
is refined indefinitely. It is the loss from averaging a field over the
opponent square before taking a positive part. It is recorded as part of
the numerical remainder of the chosen integral certificate, not as an
incentive or capacity slack of the frozen common price.

## Two-sided Bernstein integration

On a dyadic chart cell, let a and b be lower integer approximations to
the two Bernstein control tensors, with exact coefficients in
[a,a+e_a]/S and [b,b+e_b]/S. Here S=10^12. Positivity and unit sum of
the tensor Bernstein basis imply the pointwise upper polynomial with
controls max(0,a+e_a,b+e_b)/S. Its mean, rounded upward by at most one
integer unit, gives the saved upper majorant.

Independently, Jensen's inequality for the maximum gives

\[
\int_C\max(0,f_1,f_2)\ge |C|\max(0,\overline f_1,\overline f_2).
\]

Each polynomial mean is the arithmetic mean of its exact Bernstein
controls. Lower integer control means, rounded downward, therefore give
a rational lower integral. For a sum of positive parts the same argument
is applied to each field separately. Midpoint de Casteljau subdivision
carries an explicit one-sided error equal to at most the split degree;
all final sums are Python integers and rational numbers. These are
bounds over the full continuous chart cells, not sampled values.

The B calculation traverses precisely the frozen four depth-20 adaptive
trees: it uses the same axis scores, stopping tests and rounding rule.
The sum of its upper integrals is exactly the preserved B20 rational,
231831916327659047/262144000000000000. The lower integral is new audit
information. The independent archive polynomial builder is used for B;
`flow_majorant.py` is not imported.

## Additive regional records for B error

Each chart is partitioned by the first six binary path decisions of its
existing tree; an earlier certified leaf retains its shorter path. The
JSON records 60, 62, 62 and 64 cells respectively, with exact dyadic
coordinates, integer coverage, descendant lower/upper sums and leaf
counts. Their interiors form a disjoint cover. Coordinates are
(s1,t1,s2,t2); chart 0 maps a bidder to (s,s*t), and chart 1 to (s*t,s).

Each record describes item 1 on its indicated physical chart cell C.
Item symmetry sends it to item 2 on the physical cell obtained by swapping
both bidders' item coordinates: chart (c1,c2) becomes (1-c1,1-c2), with
the same radial coordinates. Twice the recorded interval width therefore
bounds this **item-indexed pair**, not both items on C. Its totals are:

| Item-indexed pair | Upper bound on its B error |
|---|---:|
| item 1/chart 00 plus item 2/chart 11 | 0.0000991938292799 |
| item 1/chart 01 plus item 2/chart 10 | 0.0000552744503802 |
| item 1/chart 10 plus item 2/chart 01 | 0.0000552744503803 |
| item 1/chart 11 plus item 2/chart 00 | 0.0000782525177078 |

These are error bounds, not estimates that every chart attains them.
The tiny asymmetry between 01 and 10 comes from integer subdivision
rounding. It does not assert an asymmetric exact stream integral.
For the full physical chart 00 or 11, adding the two appropriate item
widths instead gives an error upper bound 0.0000887231734938; for physical
chart 01 or 10 the bound is 0.0000552744503802. A physical regional atlas
must overlay the prefix partition with its item-swapped mirror, then
with structural regions, low-square boundaries and cycle-source boxes.
Adaptive item-1 partitions are not assumed to be mirror invariant.

The saved upper mean has a pointwise lift: use its coefficientwise
majorant polynomial on each terminal cell and add the nonnegative
constant needed for the final integer ceiling. Subtracting the actual
maximum gives a nonnegative density whose integral is B20-B. Thus
regional attribution of this remainder does not require signed
cancellation.

## Actual splice saving versus the averaged calculation

Write L=[0,43/100]^2 and w=43/100. In the own radial chart
v=(s,s*t), let f_j(s,t,z,r)=s*phi_j(v,w*z,w*r), and let
P_j(s,t)=w^2 integral_[0,1]^2 f_j dz dr. The two f_j are rational
polynomials; the radial singularity has cancelled. Their averaged
coefficients agree exactly with every frozen P_j coefficient in
`conditional_global_splice.json`.

With R0=4/9+2 sqrt(2)/27, the exact identities are

\[
D=4w^2\int_{[0,1]^4}\sum_j(f_j)_+-2w^2R_0,
\]
\[
D_{\rm av}=4\int_{[0,1]^2}\sum_j(P_j)_+-2w^2R_0.
\]

The factors account for the two own-item charts and the two bidder
substitutions. The subtraction is exact by the stream envelope applied
to the full-capacity SJA menu. An integer-square-root interval with 40
decimal digits encloses sqrt(2). The four-dimensional positive-part tree
has maximum depth 20; the averaged two-dimensional tree has depth 26.
Both are two-sided integral calculations and use the original stream.
Convexity gives D>=D_av>=Delta1024. Subtracting the intervals yields
the nonnegative opponent-averaging and own-cell/omission bounds above.

The D tree's prefix records are integrals of the raw positive fields.
They must not be presented as regional D errors after distributing the
constant subtraction arbitrarily. A correct nonnegative regional lift
is available directly from the existing Delta cells, as follows.

For an included own-type cell C, the SJA allocation a_j is constant.
Set sigma_j=1-2a_j, F_j=max(0,sigma_j*f_j), and
J_j=integral_(C times L) sigma_j*f_j. Select the fixed linear branch
L_j=sigma_j*f_j if J_j>0 and L_j=0 otherwise. Then pointwise

\[
F_j-L_j\ge0,\qquad \int L_j=\max(0,J_j).
\]

On every omitted cell use L_j=0 and the actual pointwise SJA allocation
in F_j. Boundaries retain its complete tie rule and are null for the
volume integrals. Summing this lift, with the chart and bidder factors,
gives exactly D-Delta1024. It is nonnegative before any regional
integration, including when the chosen linear branch is negative at a
particular report. On L times L it is zero by the frozen sign theorem
and the no-sale SJA allocation. This supplies the appropriate density
for a common regional overlay.

## Omitted cells versus Jensen loss inside included cells

The separate refinement, sharing the Bernstein primitives, in
`verifier/numerical_remainder_classification.py` reproduces the frozen
1024-by-1024 cell classification exactly. A cell entirely within one SJA
region has gap fields (1-2a_j)P_j. A sign-certified gap field is linear
under its positive part, so every finer included cell has exactly zero
Jensen loss. Only unresolved sign cells need further integration.
Negative fields use the valid control interval [-a-e,-a], preserving
one-sided arithmetic after sign reversal.

For each of the 1,706 omitted cells, further dyadic subdivisions classify
the actual SJA allocation when possible. At an unresolved terminal cell
the lower bound is zero and a Bernstein majorant of sum_j |P_j| gives
the upper bound. Thus the remaining boundary strip is explicitly bounded,
not discarded because the ideal menu boundary has measure zero. Included
cells use the two-sided positive-part integral minus an interval for the
positive part of their exact polynomial mean. The selected SJA regions
and all retained records are checked again by the ledger auditor.

The exact per-cell records are in
`certificate/numerical_remainder_classification.json`. A record's integer
pair must be multiplied by `record_integral_multiplier=4` and divided by
`integral_denominator`; the multiplier is not already in the stored
integers. The resulting global included-cell Jensen loss is

\[
8.1446069765\,10^{-8}<J_{\rm own}<8.1449150678\,10^{-8}.
\]

Its empty/single/bundle contributions are approximately 3.7290e-8,
1.5190e-8 and 2.8967e-8, with exact separate intervals in the JSON.
Subtracting this interval from the separately enclosed
D_av-Delta1024 and intersecting the direct omitted-cell enclosure gives

\[
\boxed{0.0000351329814050<O_{1024}<0.0000351337321004.}
\]

These tightened rational endpoints are in
`certificate/numerical_remainder_audit.json`. More than 99.7% of the
own-cell/omission loss comes from the omitted boundary cells. This is a
regional diagnosis of the frozen calculation; none of it is added to
the active support subtraction.

## Computation and limitations

`verifier/numerical_remainder.py` generated the rough calibration and the
final exact records. The final run took about 276 seconds and reproduced
the frozen depth-20 upper accumulator exactly. Its normal mode is
read-only and checks the saved result; `--write` writes only into this
atlas's certificate directory. The 248 regional records expose coverage
and both integral sums for replay or a second auditor.

The proof of each integral inequality is the explicit Bernstein/Jensen
argument above. The finite tree is an integral partition, not a finite
type or menu restriction. Exact agreement with the old upper integral
does not itself prove the new lower integral; the carried coefficient
intervals and lower-mean argument supply that separate obligation.
The frozen stream-envelope and support-splice theorems remain trusted
mathematical dependencies. No proof-assistant formalization is claimed.

The final ledger auditor independently checks all dyadic box volumes,
pairwise interior disjointness, path coverage, integer sums, frozen
source identities, interval arithmetic, saved tree statistics and every
retained 1024-cell region classification. It also produces both-item
whole-physical-chart bounds using the mirror map, and checks the exact
6.41% comparison. This audit is deliberately distinguished from a second
traversal of every new lower-integral tree; that full replay is the normal
operation of the primary two-sided integrator. Both roles are stated in
the audit certificate.
