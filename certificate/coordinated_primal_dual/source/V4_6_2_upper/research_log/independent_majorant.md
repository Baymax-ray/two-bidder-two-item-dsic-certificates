# Independent full replay of the continuous Bernstein majorant

**Full replay PASS.** All 1,351,220 nodes were independently reconstructed
in 210.8 seconds, and every requested comparison matched.

This component reconstructs the complete four-chart majorant certificate
through depth 20 independently of `flow_majorant.py` and the archive's
`verify_stream_dual.py`. Its implementation is
`verifier/independent_majorant.py`; its full-run record is
`certificate/independent_majorant.json`.

## Implementation independence and dependencies

Only the canonical archive `independent_replay.py` is imported. It supplies
its separate sparse-polynomial arithmetic, the chart competitors, manifest
parsing, and integer midpoint de Casteljau subdivision. This component does
not import the primary branch integrator, its Bernstein converter, its
classification function, its tree traversal, or the archive primary
verifier. The two archive dependency hashes and the compared primary JSON
hash are included in the independent record.

The root coefficients use a different conversion algorithm. Place the
sparse power coefficients in a tensor whose degree in each coordinate is
the maximum degree of either competitor. On one coordinate at a time,
apply the exact identity

    x^k = sum_{i=k}^d [binom(i,k)/binom(d,k)] B_i^d(x).

Successive rational one-dimensional transforms give the common-degree
tensor controls. This differs from the primary implementation's direct
sum over every monomial at each tensor index. Initial controls are floored
at scale `10^12`, and every individual floor inequality is checked with
`Fraction` arithmetic.

## One-sided rounding and overflow checks

If a stored coefficient is a and the exact scaled coefficient lies in
`[a,a+e]`, midpoint averaging followed by integer flooring preserves a
lower approximation. After d de Casteljau stages, error at most `e+d`
is sufficient. The independent archive routine carries out these floors
and checks that each signed integer addition is safe. The new tree
propagates the two competitors' errors separately.

Before differences, error additions, or coefficient sums, the replay
checks signed-int64 limits. Each majorant control is nonnegative; bounding
its largest value times the tensor size bounds its whole array sum.
Final dyadic accumulators and coverage counts use Python integers and
have no fixed-width overflow.

## The continuous majorant and stopping tests

For common-degree controls a_k and b_k, positivity and partition of unity
of the tensor Bernstein basis imply

    max(0,p(x),q(x)) <= sum_k B_k(x) max(0,a_k,b_k).

Every basis function integrates to the reciprocal of the tensor size.
The replay therefore integrates the coefficientwise maximum of zero and
the two **upper** control arrays, then rounds its average upward. This
bounds the continuous maximum over a cell; no type-grid primal problem
or center evaluation is used.

The first competitor is certified to win when its lower controls are
nonnegative and its lower-minus-opponent-lower controls dominate the
opponent's error. The second test is symmetric. Both competitors have
nonpositive upper controls when the unsold option wins. These are exact
whole-cell conditions. A certified winner can stop at an earlier level
and contributes its valid bound to every deeper requested depth, scaled
by that cell's dyadic volume.

On every unresolved cell, the split axis is the first coordinate attaining
the largest absolute adjacent-control difference across the two arrays.
The new traversal implements that choice and its own iterative stack. It
records bounds simultaneously at depths 12, 14, 16, 18, and 20. Coverage
at depth d must equal `4*2^d`, accounting for all four unit-cube radial
chart pairs. Multiplication by two supplies the second item using the
proved simultaneous-item symmetry of the stream.

## Required comparison and claim boundary

The full run checks each saved integer accumulator, each coverage count,
each rational upper bound, the total visited-node count, the fixed and
unresolved-leaf counts, and the maximum propagated error against the
latest `flow_majorant_certificate.json`. It also checks that this primary
JSON did not change during the independent computation.

The independent record is generated only after all comparisons pass.
Normal invocation performs the same entire replay and compares that
record without writing files:

    python -B -X utf8 verifier/independent_majorant.py

The `--write` option creates only the independent record after successful
comparison. Optimized Python is rejected. Both the complete continuum
weak-duality proof and the directed coefficient majorant are necessary:
matching integer accumulators alone would not establish an auction bound.
This component replays the new full majorant integration; it does not
rerun the archive's different depth-23 integration algorithm.


## Actual full-run results

| Depth | Exact accumulator | Coverage | Certified upper |
|---|---:|---:|---|
| 12 | 1813563158120057 | 16384 | 1813563158120057/2048000000000000 |
| 14 | 7248706577293113 | 65536 | 7248706577293113/8192000000000000 |
| 16 | 28985686275235047 | 262144 | 28985686275235047/32768000000000000 |
| 18 | 115924891811347673 | 1048576 | 115924891811347673/131072000000000000 |
| 20 | 463663832655318094 | 4194304 | 231831916327659047/262144000000000000 |

The complete statistics are 1,351,220 visited nodes, 200,355 certified
fixed nodes, 475,257 unresolved terminal leaves, and maximum propagated
error 157. All four charts were exhausted. The five rational upper bounds
are strictly decreasing, verified by exact subtraction.

The optimized-Python refusal was also executed and passed: the program
raised `Run without -O.` before any certificate traversal.
