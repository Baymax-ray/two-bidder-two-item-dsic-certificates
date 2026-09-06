# Degree-four nonuniform continuous-stream upper-bound certificate

This package certifies the global upper bound

`18588262788621/20971520000000 = 0.8863574404058933258056640625`

for the established continuous stream dual covering all measurable integrable
randomized DSIC ex-post-IR mechanisms in the iid-uniform two-bidder/two-item
problem.  It uses the same frozen degree-four rational witness as the archive's
preceding active certificate but a stronger exact nonuniform partition.  It
improves that preceding bound
`930318295428931/1048576000000000` by
`905155997881/1048576000000000`, and it improves the independently replayed
degree-three depth-23 bound `93021212643519/104857600000000` by the exact
positive margin `39949350207/52428800000000`.

The certified primal lower bound is
`26237753173862063/30000000000000000`; hence the remaining exact global gap is
`1445765276937161827/122880000000000000000`, approximately
`0.011765667943824559`.  The upper and lower bounds do not match, so the
unrestricted optimum remains open.

## Witness and partition

`manifest.json` freezes all 32 rational coefficients of the antisymmetric
degree-four stream.  The boundary factor `x(1-x)y(1-y)` gives the same exact
divergence-free curl and tangent-boundary construction as the preceding formal
stream certificates.  Numerical QMC provenance is not a verifier input.

The exact fixed-point scale is `10^9`.  The tree uses the maximum-variation
axis above the final four levels of a depth-21 base partition and exact
one-step child-bound lookahead in those final four levels.  Each unresolved
depth-21 leaf is refined once along the best exact child-bound axis iff that
split saves at least one integer accumulator unit.  Thus 391,618 leaves reach
depth 22 and 71,178 remain at depth 21.

## Verification

Run from this directory:

```powershell
python -B -X utf8 verify_stream_dual.py
python -B -X utf8 independent_replay.py
```

The first verifier is manifest-driven and read-only.  The second imports no
certificate or experiment code: it independently reconstructs the polynomial,
radial charts, Bernstein controls, winner tests, adaptive tree, and exact
integer accumulator using an iterative traversal.  Both reproduced accumulator
`1858826278862100`, all box counts, `16777216/16777216` coverage units, maximum
observed error 165, the strict comparison margin, and the remaining exact gap.

The sealed runs used Python 3.10.16 and NumPy 2.0.1.  Under concurrent proof
workloads, the read-only verifier ran for about 27 minutes (process start
11:50:17 ET), and the independent replay for about 26 minutes (process start
11:55:08 ET; both completed by 12:21:09 ET on 2026-08-27).

`verification_output.txt` and `independent_replay_output.txt` record the exact
results.  `SHA256SUMS.txt` seals every package file except itself.
