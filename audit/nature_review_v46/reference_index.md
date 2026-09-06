# Active-reference specification: author integration note

Deliverable: `reference_specification.tex`, one subsection with label `sec:active-reference-specification`, no new theorem environments. Insert immediately before the existing Complete joint reallocations subsection. It uses only the packages already loaded by `manuscript/manuscript.tex`.

Purpose: define the V4.5 reference and final active mechanism through complete ordered menu rules, exact source entrypoints and a four-dimensional payment integral. The text does not require consulting historical research logs, introduce an optimality claim, or replace the frozen review reports.

## Fixed conventions

| Term | Definition |
|---|---|
| Profile | `omega=(w1,w2,v1,v2)`, bidder 1's two physical-item values followed by bidder 2's |
| Original split cost | `s0=1137/1000`; original `d0=501/1000`, `q0=227/1000` |
| Active split cost | `s=142/125`; active `d=1/2`, `q=113/500` |
| Retained price increments | Frozen V3 full menu minus the original shared-base menu; add these increments to the new shared-base prices |
| M4.5 | Complete V4.02 candidate followed by both original lottery splices |
| M6 | M4.5 followed by strip, reverse-free, and coupled bundle modifications |
| MJ | M6 followed by the final one-orientation lottery price cut and opposing entry fee |

The active shared outcome order is literally `(0,0),(1,0),(2,0),(3,0),(0,1),(0,2),(0,3),(1,2),(2,1)`. `split_cost_candidate.mechanism` uses that sequence from `base.OUTCOMES`, with costs `0,a,a,b,a,a,b,s,s`, and chooses the first score maximizer. This intentionally preserves the active source tie order, which differs from the earlier deterministic table in the main paper.

In constrained Q rows the high-item predicate is `opponent[0] > opponent[1]`, otherwise item 2. The lottery rotation predicate is `opponent[0] < opponent[1]`, otherwise item 1 stays first. No constrained Q row can have equal coordinates: `t>1/2` and `sum<=91/100`. No lottery row can have equal coordinates either. The text retains the separate source conventions.

## Verified source anchors

All paths below are relative to `research/closed/two-bidder-two-item-dsic-certificates/certificate/joint_residual_screening_lower_bound/source/`.

| Definition | Source entrypoints and current lines |
|---|---|
| Frozen tariffs and original selection | `V3/verifier/baseline_mechanism.py`: `fee_rows` 43, `menu` 64, `mechanism` 91 |
| Joined prices and affine continuation | `V3/verifier/joined_threshold.py:menu` 55; `V3/verifier/stationary_s.py:prices_for_t` 105 |
| New split cost with frozen increments | `V4_02/verifier/split_cost_candidate.py`: `increments` 45, `retained_menu` 58, `screening_menu` 62, `candidate` 131 |
| V4.5 lottery and priority | `V4_5/verifier/residual_lottery.py`: `in_region` 29, `menu` 44, `mechanism` 85 |
| Added lottery strip | `V4_6/verifier/outer_lottery_strip.py`: `in_added_region` 28, `mechanism` 33 |
| Reverse free menu | `V4_6/verifier/free_bidder_one.py`: `in_free` 17, `mechanism` 20 |
| Bundle exchange and coupled response | `V4_6/verifier/outer_bundle_exchange.py:mechanism` 33; `outer_bundle_reoptimized.py:changed_menu` 22 and `mechanism` 43 |
| Final active rule | `V4_6/verifier/price_joint_reallocation.py`: `bidder_two_cut` 25, `bidder_one_fee` 30, `mechanism` 35 |
| Historical reduced integral | `V4_02/verifier/split_cost_revenue.py`: `base_Q` 33, `inner_Q` 44, `moments` 55, `calculate` 99 |
| V4.5 increment integral | `V4_5/verifier/independent_lottery.py:reconstruct` 90 |
| New reduced additions | `V4_6/verifier/independent_revenue.py:calculate` 108; `price_joint_revenue.py:calculate` 192 |
| Fresh additions and final enclosure | `V4_6_archive_audit/revenue/fresh_exact_gap.py`: `algebraic_increment` 129, `joint_increment` 212; `V4_6/verifier/consolidated_bounds.py:verify` 38 |

Finite table identity: `V3/certificate/baseline_mechanism.json` has 20 common rows, 41 bundle rows, and 8 item rows. The 41-row description refers specifically to the bundle table.

## Checks performed

- Parsed the cited Python modules with `ast` and confirmed every named function exists.
- Read the complete defining source chain, including V3.1 and V4 free-capacity predecessors; confirmed the constants and profile slicing against the active evaluator.
- Ran read-only, exact rational checks of both excluded lottery t endpoints, the included original lottery sum face, excluded added-strip rho=c face, an interior added-strip report, and both endpoints of each final closed rectangle.
- Evaluated the final price-release witness and the bundle-transfer witness. Allocations matched the stated physical-item order; the latter charges bidder 1 exactly 22/25.
- Result: `REFERENCE_ENTRYPOINT_AND_NAMED_BOUNDARY_CHECKS_PASS`. These checks verify the transcription and selected boundaries; they are not a new all-real feasibility proof or historical revenue reconstruction.
- Standalone LaTeX compilation was attempted in a temporary directory but TinyTeX returned an environment-level failure before producing a PDF. The parent task is handling the full manuscript build and visual QA; page count is not yet verified here.

No unresolved mechanism-definition ambiguity remains from these checks. The revenue dependency limitation is explicit: the independently reconstructed V4.6 additions share the historical V4.5 base enclosure, whose chain includes the earlier affine-polytope revenue calculation.
