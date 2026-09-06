# Independent degree-4 adaptive audit

This is a clean-room replay of the degree-4 continuous stream-dual certificate.
`independent_audit.py` uses only the rational data in
`candidate_degree4_exact.json`; it imports no formal verifier, adaptive search
code, or project polynomial module.

It reconstructs the 32 antisymmetric total-degree-four monomial pairs, the
tangent-boundary stream, four radial chart polynomials, tensor Bernstein
controls, scale-1e9 floor controls, and dyadic error propagation. The base
partition uses largest control variation until the last four levels, then the
smallest immediate child charge. A depth-20 unresolved box is refined once only
when this strictly lowers its charge.

The bounded audit ran exactly:

```powershell
python -B independent_audit.py shallow
python -B independent_audit.py full
```

The shallow paired-Fraction run passed 3,087,315 enclosure checks and 444 charge
checks with full coverage. The sole full replay reproduced every count and
accumulator `930318295428931`, with coverage `8388608/8388608`. Therefore the
independent bound is `930318295428931/1048576000000000`, or
`0.8872206644334135...`, strictly below
`372431922023109/419430400000000`.

The earlier scale-1e8 result was only a same-code precision stress test. This
scale-1e9 clean-room implementation is the independent replay. Optimized Python
mode is rejected so audit assertions cannot be disabled. Proof transcripts omit
runtime; wall times appear only in `RESOURCE_AUDIT.md`.
