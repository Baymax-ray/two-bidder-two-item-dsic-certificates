# Self-contained adaptive exact stream certificate

This is the trusted formal upper-bound package. It contains a frozen rational
degree-4 stream, self-contained exact polynomial and Bernstein arithmetic, a
fail-closed manifest verifier, box/gap decompositions, deterministic
transcripts, and arithmetic metadata. It imports nothing from exploratory
directories.

## Result

At fixed-point scale `1e9`, the exact adaptive upper bound is

```
930318295428931 / 1048576000000000
= 0.88722066443341350555419921875
```

It is strictly below

```
372431922023109 / 419430400000000
= 0.8879468966081357...
```

by the exact margin

```
1523019257683 / 2097152000000000 > 0.
```

A precision-sensitivity replay at scale `1e8` gives

```
18606431629403 / 20971520000000
= 0.8872237982465268...
```

also strictly below the target. The two fixed-point answers differ by only
`3286041219 / 1048576000000000`, about `3.134e-6`.

## Adaptive rule and proof of safety

The base tree uses the frozen hybrid-4 rule to depth 20: largest adjacent
Bernstein-control variation until the final four levels, then the axis with
minimum immediate certified child charge. At every unresolved depth-20 box,
the adaptive step compares:

- holding the box at common depth 21, with charge `2*b`; and
- splitting along each of four axes, with charge equal to the sum of its two
  certified child charges.

A split is accepted only when its charge is strictly smaller than `2*b`.
Otherwise the parent box is retained. This is fail-closed because both choices
are independently valid upper bounds and equality never triggers a split.

For a polynomial with exact Bernstein controls `c`, the stored integer control
is `m=floor(S*c)`, hence `m/S <= c < (m+1)/S`. A degree-`n` floor de Casteljau
split performs `n` floor averages, so adding `n` fixed-point error units encloses
every exact child control. A fixed-winner box uses the Bernstein mean-integral
identity with an upper integer ceiling. An unresolved child uses
`max(0,max(first)+error,max(second)+error)`. Multiplying by the common dyadic
volume, summing four chart pairs, and applying item symmetry factor 2 yields the
reported exact fraction. Concretely, every early fixed box at level `l` is
multiplied by `2^(21-l)`, every retained depth-20 box by `2`, and every split
child at depth 21 by `1`. If the resulting four-chart accumulator is `A`, the
final normalization is exactly `2*A/(S*2^21)`, where the leading `2` is item
symmetry and `S` is the fixed-point scale.

## Arithmetic bounds

- Maximum coordinate degree: `8`.
- Initial error radius: `1` fixed-point unit.
- Maximum radius through common depth 21: `1 + 21*8 = 169` units.
- Maximum initial absolute `int64` control at scale `1e9`: `1,475,346,733`.
- Maximum stored control plus radius: `1,475,346,902`.
- Maximum pair sum or difference: `2,950,693,466`, far below
  `2^63-1 = 9,223,372,036,854,775,807`.
- Control means, shifts, child-charge sums, accumulator, and final fractions use
  Python arbitrary-precision integers or `Fraction`.

## Box and gap decomposition

Of 277,676 unresolved base boxes, 233,184 have a strict one-step improvement;
44,492 are retained. The accepted split axes occur
`[58,611, 58,729, 57,689, 58,155]` times. The exact adaptive improvement is

```
52331847893 / 41943040000000
= 0.0012476884816408158...
```

The chart gain units are `390596434610`, `295250818800`, `295305721446`, and
`327143222469` for charts `00`, `01`, `10`, and `11`. The result JSON includes
the 50 largest-gain dyadic boxes. The largest boxes lie near high radial
coordinates and thin angular intervals, consistent with unresolved
winner-switching surfaces. After refinement, 363,695 child boxes remain
unresolved; this switching geometry is the remaining certificate bottleneck.

## Reproduction and checks

Run the fast frozen-output and arithmetic audit:

```
python -B audit_saved.py
```

Run the complete manifest-driven traversal:

```
python -B verify_manifest.py
```

The recorded scale-`1e9` and scale-`1e8` discovery-to-certificate runs took
690.536 s and 590.983 s respectively; runtimes are segregated in
`runtimes.json` because they are environmental, not proof inputs. Their
deterministic arithmetic records are `proof_transcript_s1000000000.json` and
`proof_transcript_s100000000.json`.

`verify_manifest.py` is the manifest-driven full fail-closed verifier. It checks
the candidate hash, reruns the scale-`1e9` traversal, checks every expected
integer field, recomputes the fraction from the accumulator, checks the strict
target inequality, and checks the saved `1e8` replay. `audit_saved.py` performs
all non-traversal frozen-output and arithmetic checks. No completed result
depends on imports from `output/` or another scratch directory.
