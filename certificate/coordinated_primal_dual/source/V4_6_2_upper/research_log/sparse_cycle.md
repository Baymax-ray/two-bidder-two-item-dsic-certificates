# Exact descent by a sparse long-range incentive cycle

This changes the continuous dual witness, not merely its numerical
integration. Start from the frozen rational degree-four stream and its
virtual fields phi_ij. Their exact revenue identity, valid for every
complete pointwise randomized DSIC/IR mechanism, is

    R1+R2 = integral sum(phi_ij*x_ij) - sum_i integral u_i(0;opponent).

The radial origin term is nonnegative. The polynomial curl has zero own
boundary flux and zero divergence, so contributes an exact zero to this
identity. This statement does not require a positive sink at every type.

Let h=3/200, epsilon=1/20 and define open equal-shaped own-report rectangles
with centers A=(2/5,39/40) and B=(7/20,23/40), both halfwidth h in each
coordinate. Let W have center (3/5,1/5) and the same halfwidth. The own
translation is d=A-B=(1/20,2/5).

For every offset s in (-h,h)^2 and opponent w in W, add a directed incentive
edge B+s -> A+s with density epsilon and the reverse edge with the same
density. These are nonnegative finite flows. Opponent reports are fixed
along each edge; translation preserves Lebesgue volume. Source and target
mass cancel exactly, so the added flow has zero divergence and changes no
sink. It contributes the nonnegative weighted IC term

    epsilon integral_{s,w} d . [x1(A+s,w)-x1(B+s,w)].

Indeed this integrand is the sum of the two truthful-report IC inequalities.
The resulting virtual correction is +epsilon*d on A x W and -epsilon*d on
B x W. Outside those two boxes it is zero. All box boundaries can be assigned
zero added density; this is a Borel measure convention, not a relaxation of
the mechanism's pointwise constraints.

The exact whole-box polynomial checks prove the maximizing bidder identities
for the old and corrected fields are:

| Own box | Item 1 winner | Item 2 winner | Bidder 1 allocation |
|---|---|---|---|
| A | bidder 2 | bidder 1 | (0,1) |
| B | bidder 1 | bidder 1 | (1,1) |

All comparisons are strict against both the other bidder and unsold. Both
own boxes have their second coordinate maximal and W has its first
coordinate maximal. Multiplying the virtual values by the positive
D=2*v12^2*v21^2 gives rational polynomials. The verifier reconstructs these
from all 32 frozen coefficients. It translates each comparison to the box
center, bounds the absolute sum of its nonconstant Taylor monomials, and
checks a strictly positive remaining constant. No sampling or floating
polynomial evaluation supplies these inequalities.

Thus the continuous virtual-allocation envelope changes exactly by

    epsilon * (2h)^4 * d . [(0,1)-(1,1)]
      = -81/40000000000.

This also proves the old virtual maximizer violates a specific weighted IC
constraint. The virtual maximizing allocation is a relaxation variable;
it was never asserted to be a truthful mechanism.

Apply bidder exchange and simultaneous item exchange. Symmetry of the
frozen field preserves the same integral decrease in all four images.
The eight full-profile rectangles are pairwise disjoint; the verifier
checks all 28 pairs with exact separating-coordinate inequalities.
Therefore all four cycles can be added simultaneously, giving

    exact strict reduction = 81/10000000000.

Every report in these supports has both bidders' maxima strictly greater
than 43/100. The cycles are therefore disjoint from both sides of the
conditional-support splice on [0,43/100]^2. The reductions add exactly
when both start from the same frozen stream field.

Original and final winner inequalities are strict and linear in the added
density. Consequently every density from zero to epsilon is certified.
The three densities 1/80, 1/40, 1/20 give a strictly decreasing sequence of
valid upper bounds, with reductions one quarter, one half, and all of the
stated four-orbit amount. They can be added to each certified integration
bound for the same stream and to the disjoint conditional splice.

Discovery also tried wider boxes and a larger density. Their elementary
Taylor lower bounds failed, so those choices were discarded. Such a failed
sufficient inequality is not evidence that those boxes or mechanisms are
infeasible. Only the selected rational boxes and density are certified.
The contribution is structurally useful despite its small size: sparse
long-range incentive flow has produced an exact descent outside the pure
polynomial-curl search family.
