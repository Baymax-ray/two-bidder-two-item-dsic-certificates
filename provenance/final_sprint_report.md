# Bounded final research sprint and freeze decision

Date: 26 August 2026.

The sprint began from the exact degree-3 depth-22 upper bound

`372431922023109/419430400000000 = 0.887946896608135700225830078125`.

Three independent routes were bounded in advance and then frozen.

## Route A: higher-degree witness plus certificate-aware refinement

The degree-4 rational stream has 32 antisymmetric coefficients. Its sampled
objective was promising, but a uniform finite Bernstein certificate left too
much slack at winner-switching surfaces. The successful change was to optimize
the final partition decision rather than deepen every box blindly.

The verifier builds a hybrid depth-20 tree. For each unresolved base box it
compares the common-depth hold charge with all four one-step axis-split charges
and accepts a split only on a strict certified decrease. Of 277,676 unresolved
base boxes, 233,184 split and 44,492 remain held. The resulting exact bound is

`930318295428931/1048576000000000 = 0.88722066443341350555419921875`.

This improves the starting bound by

`1523019257683/2097152000000000 = 0.000726232174722194671630859375`.

A same-code precision stress replay at scale `10^8` yields
`18606431629403/20971520000000 = 0.8872237982465268...`, still strictly below
the starting bound. A clean-room implementation then independently
reconstructed the basis, chart polynomials, Bernstein arithmetic, base rule,
and adaptive rule. Its sole full run matched the exact accumulator and every
recorded count, with coverage `8388608/8388608`. Its shallow Fraction mode made
3,087,315 exact enclosure checks and 444 charge checks.

This route is the frozen theorem path.

## Route B: certificate-aware witness redesign

A localized degree-3 coefficient redesign produced one complete exact
candidate at parameter `47/50`, but its bound was
`0.8879981743147969...`, worse than the starting certificate. Other Sobol-local
candidates improved shallow discovery objectives and then deteriorated at
deeper exact certification. This route supplied useful negative evidence that
sampled/local gains do not predict certification near switching surfaces; it
did not enter the theorem path.

## Route C: stronger convexity-sensitive dual constraints

The sprint derived two valid extensions of the weak-duality family: a
positive-semidefinite matrix-field correction paired with the Hessian measure
of convex utility, and a symmetric nonlocal monotonicity kernel. Low-degree
smooth bases had no sampled descent direction, although adversarial slice
tests found substantial pairwise/cyclic violations in the allocation selected
by the older pointwise envelope. Localized rational kernels showed only
approximately `2e-7` to `5e-7` sampled improvements, far below existing
Bernstein slack, and were not exactly certified. These structural results are
promising future directions but are not claims of the release theorem.

## Freeze decision

No route produced a stronger rigorously verified endpoint than Route A. The
release therefore freezes

- lower bound: `26232788323031183/30000000000000000`;
- upper bound: `930318295428931/1048576000000000`.

The unrestricted optimum remains open. Floating-point values near `0.88325`,
all sampled kernel improvements, and every optimizer trace are discovery-only.
The trusted proof inputs are the rational candidate manifests, analytic proof,
directed-rounding verifier, independent replay, and exact lower-bound
certificates.
