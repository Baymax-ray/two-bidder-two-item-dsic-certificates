# Independent hostile audit of the V4 residual-screening result

**Outcome:** no substantive mathematical gap found in the stated support,
explicit mechanism, or exceptional-report claims. This is an independent
proof audit and exact arithmetic replay, not formal verification or a proof
of the original auction's optimality.

Audited snapshots:

* `research_log/type_dependent_screening.md`, SHA256
  `1e747dfbf7a1225e1a97ef02957bb18b95c9e1ba4574c23abeade23d69cf43e3`;
* `verifier/screening_verify.py`, SHA256
  `56b8f29ac05a4e6535d2ef18d1414e1bd398e0c7c47311b71d8c97de00b96ce1`;
* `certificate/screening_verified.json`, SHA256
  `8b72fa35c204d4f552f15fae933ca3ac17cbc557e6b40832cc5917d820771ca5`.

The author's files were not modified.

## Attempted failure: the support might apply only on the one-item face

The full-domain claim survives. For an arbitrary two-item competitor, DSIC
on a fixed-`z` line gives both monotonicity of `x_1(t,z)` in `t` and
`u(t,z)=u(0,z)+integral_0^t x_1(s,z)ds`. Consequently

`R=integral(2t-1)x_1 + integral z x_2 - integral u(0,z)`.

This identity does not require the competing utility or menu to be
separable. The transported virtual-mass price bounds the positive first
term by monotonicity, while `pi_2=z dt dz` bounds the second term by capacity.
IR supplies the correct sign of the remaining term. I independently
expanded the five claimed nonnegative slacks; their sum is exactly
`<pi,r>-R`, with no omitted cross-coordinate incentive term.

For arbitrary dependence on the opponent report `y`, apply this calculation
on every own-type slice and integrate. The complete-profile price is
`dy tensor pi_j`. This makes the extension to the original four-dimensional
profile domain explicit; it requires no interchange of a supremum and an
integral or selection of slice optimizers.

## Attempted failure: transport could ignore exceptional reports

The pushforward retains the actual values `r_1(T(t),z)` and
`x_1(T(t),z)`. A transport collapsing a positive-measure interval to `b`
therefore creates an actual atom, rather than using a version of a density
defined only almost everywhere. Borel composition makes these integrals
well-defined. The permitted null exceptional set in the hypotheses on `T`
has zero transported source mass and does not invalidate the nonnegative
integral argument.

The upper bound needs both `T(t)>=t` and the candidate bottleneck attainment
`rho(T(t))=m(t)` for equality. The note states both hypotheses explicitly.
It does not falsely infer a minimizing selector for arbitrary Borel
capacities. Thus the result is compatible with the separate counterexample
in `residual_functional.md` where no countably additive support exists.

## Attempted failure: the claimed optimizer might fail at ties or endpoints

The allocation `q` is monotone at every type and lies below the original
capacity, not merely its almost-everywhere representative. A monotone
function's own value at a jump lies between its one-sided limits and is a
relative subgradient of its integral. At the endpoints the corresponding
one-sided subgradient condition also holds. Hence its displayed payments
implement all reports, including jumps and the endpoint `1` even when the
future infimum is not attained earlier.

In the rational example the empty row at `1/2` and the half-allocation row
at `3/4` are utility maximizers. The latter is essential for pointwise
feasibility of the single-line capacity. The joint diagnostic construction
has first-item marginal allocations `(1-c,c)` at that line and `(0,q(t))`
elsewhere; second-item allocations are `(1,0)`. They admit a feasible
lottery coupling at every report. Bidder 1's free allocation is independent
of its own report, so its pointwise IC claim is correct.

The essential-randomization claim is confined to this residual instance.
The positive-virtual-value slack forces `q=c` almost everywhere on
`(1/2,b)`. A deterministic competitor must be zero through `b`, giving
upper bound `b(1-b)`; posting that reserve with a rejected tie attains it.
This does not establish essential randomization in the original auction.

## Directional calculation and replay

The strict inequality `2 epsilon ||h|| < 1-c` keeps `b` as the future
minimum below `b`. Above `b`, the future minimum is exactly
`1+epsilon inf_{s>=t}h(s)`. Thus the stated one-sided value formula is an
exact re-optimization calculation under its capacity-admissibility
hypothesis. It is not an unrestricted stationarity theorem.

Ran `python -B -X utf8 V4/verifier/screening_verify.py`: **PASS**. Independently
checked the values `7/32`, `3/16`, their difference `1/32`, the atom `1/16`,
and the second-bottleneck value `107/512`. The replay checks exact affine
dominance and coefficient identities. General analytic claims continue to
depend on the written proofs.

After the replay interface was changed to read-only operation by default,
inspected the revised code and repeated the normal replay: **PASS**. It
reconstructs the exact result and compares it with the saved JSON; only
`--write` generates a certificate. The source and certificate hashes above
identify this revised, successfully replayed snapshot. No mathematical
formula or certificate value changed.

**Remaining scope limitation, already stated correctly by the author:**
the inner support is for a diagnostic residual, not V3's residual, and
bidder 1 is not proved optimal against the same price. It supplies no
matching upper bound for the original two-bidder optimum.
