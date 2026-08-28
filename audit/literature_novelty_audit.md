# Final targeted literature and novelty audit

Audit date: 27 August 2026. Scope: the exact two-bidder, two-item additive
auction with four independent `U[0,1]` coordinates, pointwise DSIC, ex-post IR,
ex-post item feasibility, and arbitrary internal randomization.

This was a bounded, claim-driven audit performed after the mathematical
candidate was complete. It asked whether the release may accurately claim an
improved rigorous upper bound, how to report the best directly comparable
primal benchmark, and how the signed stream witness should be related to
existing continuous flow, transport, and Beckmann formulations. It was not an
attempt to survey all of mechanism design.

## Primary-source findings

1. [Jiang, Parkes, and Wang, arXiv:2606.10112v1](https://arxiv.org/abs/2606.10112)
   develops continuous weak duality for DSIC multi-item, multi-bidder auctions
   through nonnegative flow-conserving deviation kernels and gives a lifting
   construction from uniform grids. Its two-bidder, two-item uniform results
   report a strict `50 x 50` continuous certificate of `0.8919`, rounded to
   `0.892` in the comparison table. The same table reports GemNet revenue
   approximately `0.876` and describes GemNet as DSIC/fully strategyproof.
   These are the two external benchmarks used in this archive. The paper's
   released source did not expose an exact target dual array or the GemNet
   mechanism data needed for an independent exact replay here.
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
   strategyproof menu mechanisms after a compatibility transformation.
   Revenue is evaluated computationally rather than as an exact symbolic
   integral. Accordingly, the `0.876` figure in this release is attributed
   specifically to Jiang--Parkes--Wang's 2026 comparison and is not treated as
   a locally certified rational endpoint.
6. [Sandholm and Likhodedov
   (2015)](https://doi.org/10.1287/opre.2015.1398) studies automated design in
   restricted families such as affine maximizers; such a restriction is not
   known to be without loss for the present problem.

No later or stronger directly comparable strict continuous DSIC certificate
for this canonical instance was located in the bounded audit. That is evidence
for the positioning below, not a universal priority theorem over unpublished
or unindexed work.

## Approved novelty boundary

The release may claim:

- an explicit 32-parameter rational, instance-specific signed stream witness;
- a direct weak-duality proof against Lipschitz convex truthful utilities;
- an exact directed-rounding tensor-Bernstein certificate with nonuniform
  certificate-aware refinement near winner-switching boxes;
- an independent non-importing arithmetic replay;
- the rigorous upper bound `18588262788621/20971520000000`, which is strictly
  below the external printed `0.8919` benchmark by
  `116235899379/20971520000000`;
- the explicit ten-band deterministic mechanism with exact revenue
  `26237753173862063/30000000000000000`, improving this archive's predecessor
  by `10343439231/62500000000000`; and
- the remaining exact gap
  `1445765276937161827/122880000000000000000`.

The release must not claim:

- invention of continuous mechanism-design duality, flow duality, continuous
  DSIC certificates, or Beckmann-style auction duality;
- that every signed stream field is equivalent to a nonnegative Jiang-style
  deviation kernel, or conversely;
- that the exact difference from the printed decimal reconstructs Jiang et
  al.'s unreleased underlying certificate;
- that the `0.876` GemNet figure was independently replayed or is our exact
  lower endpoint;
- that our exact lower mechanism improves GemNet's reported revenue;
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
publication claim is therefore the explicit rational witness, the stronger
exact local-certification geometry, the explicit exact lower mechanism, and
the tightened target-specific bracket—not a new general duality theory.
