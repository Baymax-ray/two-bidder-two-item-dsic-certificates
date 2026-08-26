# Final targeted literature and novelty audit

Audit date: 26 August 2026. Scope: the exact two-bidder, two-item additive
auction with four independent `U[0,1]` coordinates, pointwise DSIC, ex-post IR,
ex-post item feasibility, and arbitrary internal randomization.

This was a bounded, claim-driven audit performed after the mathematical
candidate was complete. It asked whether the release may accurately claim an
improved rigorous upper bound and how the signed stream witness should be
related to existing continuous flow, transport, and Beckmann formulations. It
was not an attempt to survey all of mechanism design.

## Primary-source findings

1. [Jiang, Parkes, and Wang, arXiv:2606.10112v1](https://arxiv.org/abs/2606.10112)
   develops continuous weak duality for DSIC multi-item, multi-bidder auctions
   through nonnegative flow-conserving deviation kernels and gives a lifting
   construction from uniform grids. Its two-bidder, two-item uniform table
   reports a `50 x 50` continuous certificate of `0.8919` (also rounded to
   approximately `0.892` in the discussion). This is the closest directly
   comparable prior upper bound located. The paper is a 2026 preprint. Its
   released source did not expose an exact target dual array that could be
   replayed here.
2. [Kolesnikov, Sandomirskiy, Tsyvinski, and Zimin,
   arXiv:2203.06837v2](https://arxiv.org/abs/2203.06837) proves a continuous
   Beckmann optimal-transport formulation and strong duality for multi-item,
   multi-bidder Bayesian auctions. The operative constraints are BIC and
   interim IR; this does not certify the pointwise DSIC/ex-post-IR target.
3. [Daskalakis, Deckelbaum, and Tzamos,
   arXiv:1409.4150v3](https://arxiv.org/abs/1409.4150) and
   [Giannakopoulos and Koutsoupias,
   arXiv:1404.2329v4](https://arxiv.org/abs/1404.2329) provide continuous
   transport/measure and partial-derivative duality for the multi-good
   monopolist. Those are one-bidder formulations and do not directly enforce
   cross-bidder ex-post supply.
4. [Rochet (1987)](https://doi.org/10.1016/0304-4068(87)90007-3) supplies the
   cyclic-monotonicity and convex-potential foundation for multidimensional
   DSIC. [Cai, Devanur, and Weinberg,
   arXiv:1812.01577](https://arxiv.org/abs/1812.01577) supplies finite-type
   flow-induced virtual-value duality for Bayesian mechanism design, and
   [Zuo, arXiv:1711.10922](https://arxiv.org/abs/1711.10922) explicitly treats
   both Bayesian and dominant-strategy formulations. None gives the present
   target-specific rational continuous certificate.
5. [Wang, Jiang, and Parkes,
   arXiv:2406.07428v3](https://arxiv.org/abs/2406.07428) constructs exactly
   strategy-proof menu mechanisms after a compatibility transformation, but
   its reported target revenues are computational experiments rather than an
   exact globally optimal mechanism. [Sandholm and Likhodedov
   (2015)](https://doi.org/10.1287/opre.2015.1398) studies automated design in
   restricted families such as affine maximizers; such a restriction is not
   known to be without loss for the present problem.

No later or stronger directly comparable continuous DSIC certificate for this
canonical instance was located in the bounded audit. That is evidence for the
positioning below, not a universal priority theorem over unpublished or
unindexed work.

## Approved novelty boundary

The release may claim:

- an explicit 32-parameter rational, instance-specific signed stream witness;
- a direct weak-duality proof against Lipschitz convex truthful utilities;
- an exact directed-rounding tensor-Bernstein certificate with
  certificate-aware refinement near winner-switching boxes;
- an independent clean-room arithmetic replay; and
- the rigorous bound
  `930318295428931/1048576000000000`, which is strictly below the previously
  printed `0.8919` benchmark by the exact difference
  `4906638971069/1048576000000000`.

The release must not claim:

- invention of continuous mechanism-design duality, flow duality, continuous
  DSIC certificates, or Beckmann-style auction duality;
- that every signed stream field is equivalent to a nonnegative Jiang-style
  deviation kernel, or conversely;
- that the exact difference from the printed decimal reconstructs Jiang et
  al.'s unreleased underlying certificate;
- global optimality of the deterministic lower-bound mechanism; or
- solution of the unrestricted optimum, because the exact lower and upper
  endpoints remain unequal.

## Relationship of formulations

The present proof has the same high-level weak-duality architecture as the
Jiang--Parkes--Wang DSIC framework: conservation removes payments, a dual
object induces virtual coefficients, and ex-post feasibility bounds virtual
surplus item by item. The representation is specialized. A radial field gives
the revenue source identity, and an opponent-dependent curl is divergence-free
with zero normal trace. The paper proves this signed field's validity directly
and does not place it inside the nonnegative deviation-kernel cone.

The Beckmann formulation is closer in continuous variational language but
lives in interim BIC space and proves a different strong-duality statement.
The one-bidder transport papers supply important integration-by-parts
precedents without resolving multi-bidder ex-post supply. The conservative
publication claim is therefore the explicit rational witness, exact
Bernstein/adaptive certification machinery, and improved target-specific
upper bound—not a new general duality theory.
