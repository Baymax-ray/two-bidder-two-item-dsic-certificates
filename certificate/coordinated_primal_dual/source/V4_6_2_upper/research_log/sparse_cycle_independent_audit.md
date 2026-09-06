# Independent audit of the sparse continuous cycle

**PASS.** The selected two-way incentive flow reduces the actual continuous
virtual envelope by exactly `81/40000000000`. Its four disjoint symmetry
images reduce that envelope by `81/10000000000`. This audit verifies the
local field reconstruction, whole-box comparisons, IC signs, and
composition geometry. It does not independently repeat the predecessor's
3.7-million-node integration certificate.

## Source and exact field reconstruction

The reviewed primary files are `verifier/sparse_cycle.py` and
`certificate/sparse_cycle.json`. The field is reconstructed from the 32
rational coefficients in the archived
`continuous_stream_degree4_two_level_nonuniform_upper_bound/manifest.json`.
The underlying radial identity and field convention were checked against
the archive's `manuscript/manuscript.tex`, analytic weak-duality section,
and the archive's polynomial reconstruction.

For profile `(x,y,z,w)` on these boxes, `y>x` and `z>w`. The radial fields
are therefore

    F^0_1j = (3y^2-1)*(x,y)_j/(2y^2),
    F^0_2j = (3z^2-1)*(z,w)_j/(2z^2).

With `D=2y^2z^2>0`, the primary numerators are exactly

    D F_1j = (3y^2-1)*(x,y)_j*z^2 + D G_1j,
    D F_2j = (3z^2-1)*(z,w)_j*y^2 + D G_2j.

The independent replay expands the boundary factor
`xy-x^2y-xy^2+x^2y^2` directly against each signed manifest monomial,
differentiates its terms, and assembles those four numerator dictionaries.
All four agree exactly with the primary reconstruction. Rational manifest
coefficients are parsed as fractions, never through floating conversion.
The stream boundary factor gives zero normal components and the mixed
partials give zero own-type divergence. Bidder 2 uses the same correction
with the two bidder coordinate pairs exchanged.

## Whole boxes, including the new comparisons

The centers are

    A=(2/5,39/40), B=(7/20,23/40), W=(3/5,1/5),

with halfwidth `h=3/200` in all four coordinates, and flow density
`epsilon=1/20`. Every closed box lies inside the type domain and strictly
inside the asserted radial charts. On the A box the winners of items
1 and 2 are bidders 2 and 1; on the B box bidder 1 wins both.

For each item, each box, and both original and modified fields, the
verifier bounds the selected numerator and its difference from the rival
numerator. If a centered polynomial is

    P(center+s)=a_0 + sum_{e!=0} a_e s^e,

then throughout the entire closed box

    P >= a_0 - sum_{e!=0} |a_e| h^|e|.

This finite identity is an absolute polynomial bound, not a truncated
Taylor approximation. There is no omitted remainder. Positivity of D
preserves signs when returning to the rational fields.

The independent replay translates one coordinate at a time, separately
from the primary simultaneous multinomial expansion. It checks every
coefficient, and all 16 certificate bounds, exactly. All lower bounds
are strictly positive; the smallest numerator lower bound is approximately
0.001913084435623365. An additional 256 exact endpoint evaluations fall
inside their certified ranges. Those endpoint tests supplement the
polynomial whole-box argument and are not its basis.

## Incentive signs and the exact integrated decrease

Let `d=A-B=(1/20,2/5)`. Add density epsilon to both directed edges

    B+s -> A+s,      A+s -> B+s

for the common two-dimensional offset s and opponent reports in W's box.
An edge points from truth to report. Its incoming coefficient at A is
`A-B=d`; the reverse incoming coefficient at B is `B-A=-d`.
The sum of the two DSIC slacks is exactly

    d . [x_1(A+s,W+r)-x_1(B+s,W+r)] >= 0.

The flow is nonnegative, finite, and has equal incoming and outgoing
marginals. Thus it adds a nonnegative IC term to the stream's exact
revenue identity. The modified field need not itself belong to the smooth
divergence-free stream family: validity follows by adding this explicit
IC inequality to the previously proved stream identity.

The original and modified winners are unchanged on both whole boxes.
Their bidder-1 allocation vectors are `a_A=(0,1)` and `a_B=(1,1)`, so

    d.(a_A-a_B)=-1/20.

One full profile box has volume `(3/100)^4=81/100000000`. The exact
change in the continuous envelope is therefore

    epsilon*(3/100)^4*(-1/20) = -81/40000000000.

Consequently subtracting that rational amount from the predecessor's
certified upper bound is valid even though the predecessor upper was an
outward enclosure of its envelope rather than its exact integral.
No discrete objective or quadrature estimate enters this subtraction.

## Four symmetry images and conditional-splice compatibility

Bidder exchange and simultaneous item exchange generate four images of
the selected flow. The archive uses the same correction for each bidder.
Its stream is antisymmetric under simultaneous item exchange; direct
coefficient comparison independently verifies

    G_11(y,x,w,z) = G_12(x,y,z,w).

The radial field has the same item equivariance. Thus each transformed
flow has the same strict comparisons, box volume, incentive dot product,
and exact decrease.

The replay forms all eight full-profile rectangles (A and B for each
of the four images). All 28 pairs are strictly separated in at least
one profile coordinate. This matters: without disjointness, independent
single-cycle winner comparisons would not certify their sum. Here no
profile receives two corrections, so the four reductions add exactly.
The aggregate decrease is `81/10000000000`.

Every rectangle also has each bidder's maximum own coordinate strictly
greater than 43/100, even after subtracting the halfwidth. Hence every
cycle support is disjoint from a conditional splice indexed by an own
report in `[0,43/100]^2`, regardless of which bidder labels that index.
This establishes geometric composition with that splice. Validity and
size of the separate splice improvement are outside this audit.

## Replay boundary

The read-only independent command is

    python -B -X utf8 verifier/flatness_sparse_cycle_audit.py

It returned `SPARSE_CYCLE_INDEPENDENT_AUDIT_PASS`, with four exact
numerator reconstructions, 16 strict whole-box comparisons, 256 endpoint
checks, and 28 disjoint rectangle pairs. Both one-cycle and four-image
reductions were checked as fractions. The verifier refuses optimized
Python. No predecessor file was modified and no full inherited upper
integration is claimed by this component.
