# Degree-four two-level nonuniform continuous-stream certificate

This self-contained package certifies the global upper bound

`3715139591287203/4194304000000000 = 0.8857583025186545848846435546875`

for the established continuous stream dual covering all measurable integrable
randomized DSIC ex-post-IR mechanisms in the iid-uniform two-bidder/two-item
problem.  It improves the preceding degree-four nonuniform upper bound
`18588262788621/20971520000000` by the exact positive margin
`2512966436997/4194304000000000`, approximately `0.000599137887238741`.

Against the certified primal lower bound
`26237753173862063/30000000000000000`, the remaining exact global gap is
`10977145706826122741/983040000000000000000`, approximately
`0.011166530056585818`.  The endpoints still do not match, so the unrestricted
optimum remains open.

## Frozen witness and partition

`manifest.json` repeats all 32 rational coefficients of the active
antisymmetric degree-four stream.  The verifier reconstructs the boundary
factor, divergence-free correction, four radial chart pairs, Jacobians, and
the two pointwise competitors from those coefficients.

The fixed-point scale is `10^9`.  The depth-21 prefix is identical to the
active certificate: maximum-variation axes are used above the last four base
levels, and exact one-step fixed-point child-bound lookahead is used in those
last four levels.  At an unresolved depth-21 leaf, its best split is retained
only if it saves at least one integer accumulator unit.  For every unresolved
retained depth-22 child, the best depth-23 split is independently retained only
if it also saves at least one unit.  All contributions are accumulated on the
common depth-23 denominator.

This is a finite directed-rounding certificate.  The two immediate-savings
tests guarantee that the promoted tree cannot worsen the active finite bound;
they are not asserted to define a generally convergent adaptive algorithm.

## Independent verification

From this directory run:

```powershell
python -B -X utf8 verify_stream_dual.py
python -B -X utf8 independent_replay.py
```

Do not run either program with `python -O`: both proof programs deliberately
use Python `assert` statements for internal certificate consistency checks.

`verify_stream_dual.py` is manifest-driven.  `independent_replay.py` imports
neither the verifier nor any experiment module: it separately reconstructs
the sparse polynomial arithmetic, rational Bernstein roots, directed floor
subdivision, propagated error radii, winner tests, iterative tree, and integer
accumulators.

Both implementations reproduce the active depth-22 accumulator
`1858826278862100` as a regression and the promoted depth-23 accumulator
`3715139591287203`.  They visit `3738334` retained-tree nodes, refine `609951`
of `610038` unresolved depth-22 children, observe maximum propagated error
radius `181`, and cover exactly `4 * 2^23 = 33554432` chart-volume units.  The
manifest seals these counts, both selective-level savings, the exact strict
improvement, and the remaining gap.
