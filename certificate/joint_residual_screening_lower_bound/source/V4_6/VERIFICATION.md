# V4.6 verification record

The combined read-only runner completed with exit code 0 using
`python -B -X utf8 V4_6/verifier/run_all.py`. It reported:

- 11 new mathematical replays passed.
- 14 inherited V4.5/V4.02/V3.1 mathematical replays passed.
- All 945 pre-V4.6 stable identities were preserved, mapping only the saved
  navigation file to its preserved predecessor bytes.

The complete output is in [final_replay.txt](research_log/final_replay.txt).
An initial baseline replay is separately retained in
[baseline_replay.txt](research_log/baseline_replay.txt).
After the combined replay, the lottery-strip scope label was clarified to
point to the separate full-inner theorem; its certificate was regenerated
and its default read-only replay passed again. No mathematical quantity or
formula changed in that clarification.

## What was checked

| Component | Exact replay evidence |
|---|---|
| Eplus extension | 1,372 rational profile/occupied-trace cases; two independent continuous polynomial integrations |
| Reverse free optimization | 156 rational boundary cases; exact quadratic-field area and revenue |
| Full lottery inner theorem | 20 arbitrary-menu polygon/line gap examples; 63 occupied-trace cases |
| Bundle exchange | 167 profile cases; 15 continuous menu-cell integrals |
| Coupled response | 267 profile/trace cases; 8 continuous menu-cell comparisons |
| Generalized diagonal inner theorem | 24 polygon/line gap examples; 45 occupied-trace cases |
| Joint capacity release | 315 named boundary cases; independent positive rational gain bound |
| Exact joint revenue | Polynomial partial-fraction identities and signed rational logarithm tails |
| Independent fee/cut audit | 33 entire fee fibers, 140 source-menu cells, five lottery-cut fibers |
| Independent total revenue | Direct two-variable cell integration, quadratic-field Horner primitives, independent radical/log bounds |

The finite examples test implementation, exact identities, and selected
boundary behavior. The accompanying all-real menu and measure proofs
establish pointwise DSIC/IR, complete feasibility, and unrestricted
conditional claims. Passing examples alone is not a continuum certificate.
The two inner proofs and final scope map were independently reviewed;
[report_audit.md](research_log/report_audit.md) records the corrections.

## Trusted execution boundary

The replayers use Python standard-library rational and integer arithmetic;
optimized `-O` execution is rejected. Default execution does not write
certificates. Explicit `--write` commands created this phase's certificates
before the read-only checks. No floating solver, grid optimizer, numerical
quadrature, or automatic differentiation supplies a theorem here.

The baseline revenue is the frozen V4.5 expression and its exact V4.02
integration dependencies. The new independent replay reconstructs every
V4.6 increment, not the entire historical source package from first
principles. The inherited unrestricted upper certificate was preserved by
identity and cited with its original scope; it was not fully recertified
in this phase. There is no Lean/Isabelle/Coq formalization.

`V4_6/SHA256SUMS` and the outer `SHA256SUMS` cover the stable inventories.
Their read-only verifiers check file identity, safe paths, missing/extra
files, and changes during verification. A manifest is evidence of identity
and coverage, not an additional mathematical proof.

Previous mathematical packages remain unchanged. Their original current
navigation and manifest are saved in `certificate/pre_V4_6_CURRENT_PHASE.md`
and `certificate/pre_V4_6_SHA256SUMS`. Only the outer current-phase pointer
and outer manifest are updated to expose the new phase.
