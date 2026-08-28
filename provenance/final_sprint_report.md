# Bounded continuation sprint and freeze decision

Date: 27 August 2026.

The continuation began from the preceding closed-release endpoints

- lower bound: `26232788323031183/30000000000000000`;
- upper bound: `930318295428931/1048576000000000`.

Three bounded routes were pursued and then frozen.

## Route A: stronger exact nonuniform upper certificate

This route did not change the 32 rational degree-four stream coefficients in
the preceding release. The improvement is therefore not another numerical
optimizer draw. It changes the exact certification geometry: the base tree is
deepened from 20 to 21, exact child-bound lookahead is retained in the final
four base levels, and each unresolved depth-21 leaf is refined once along the
best exact axis only if that split saves at least one integer accumulator unit.

The formal verifier reports 404,804 fixed-winner-or-zero boxes, 462,796
unresolved depth-21 leaves, 391,618 refined leaves, 71,178 retained leaves,
1,735,196 visited boxes, accumulator `1858826278862100`, and complete coverage
`16777216/16777216`. The resulting exact global upper bound is

`18588262788621/20971520000000 = 0.8863574404058933258056640625`.

It improves the preceding active exact upper bound by

`905155997881/1048576000000000 = 0.0008632240275201797...`,

and improves the external strict `0.8919` benchmark reported by Jiang, Parkes,
and Wang by

`116235899379/20971520000000 = 0.005542559594106674...`.

A non-importing iterative replay independently reconstructs the polynomial,
Bernstein, traversal, refinement, and coverage arithmetic and matches every
reported count and the exact accumulator.

## Route B: stronger exact lower mechanism

This route keeps the same exactly verified affine-maximizer base but changes
the surcharge construction structurally. The preceding mechanism used one fee
on two symmetric rectangles. The active mechanism uses ten rational bands:
five zero-pivot triangular bands and five additional singleton-pivot
rectangular bands, always adding a common fee to all nonempty menu entries.

The common-fee deletion argument preserves pointwise DSIC, ex-post IR, and
ex-post feasibility. Exact symbolic integration gives gains

`G_Z=14055427773/125000000000000` and
`G_S=9541919439/125000000000000`,

hence the active exact lower endpoint

`26237753173862063/30000000000000000
=0.8745917724620687...`.

This improves the preceding exact lower by

`10343439231/62500000000000 = 0.000165495027696`.

A second verifier imports no symbolic-verifier code and independently checks
the polynomial degree and exact integral using scalar rational arithmetic and
Boole quadrature. Numerical chamber probes were discovery evidence only.

## Route C: certificate replay, hashes, and claim boundary

The upper and lower active packages each contain a primary verifier, a
non-importing replay, captured outputs, and a local SHA-256 manifest. The root
orchestrator binds the active manifest fractions to the manuscript and README,
rebuilds the paper, and checks complete root-hash coverage.

Jiang--Parkes--Wang's strict continuous upper bound `0.8919` and their reported
fully strategyproof GemNet revenue approximately `0.876` are external
benchmarks. The former is improved by our new exact upper certificate. The
latter is not improved by our exact lower endpoint; our lower contribution is
instead its explicit rational mechanism and exact reproducibility. Neither
external artifact is part of the local proof path.

## Freeze decision

The release freezes

- lower bound: `26237753173862063/30000000000000000`;
- upper bound: `18588262788621/20971520000000`;
- remaining exact gap:
  `1445765276937161827/122880000000000000000
  =0.011765667943824559...`.

The unrestricted optimum remains open. Floating-point candidates, optimizer
traces, and unconverted chamber probes are discovery-only. The trusted proof
inputs are the rational manifests, analytic arguments, directed-rounding
verifier, independent replays, and complete SHA-256 bindings.
