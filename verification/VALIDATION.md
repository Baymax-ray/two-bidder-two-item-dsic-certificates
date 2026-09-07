# Verification of the current reader package

The final mathematical record is `certificate/reserve_parameter/manifest.json`:
`tau=83/10000`, revenue in `[0.876514341027067549900397423113,
0.876514355424052828335888359874]`, unrestricted upper below
`0.882351585488796576205586892264`, gap below `0.005837245` and a guarantee
strictly above 99.3384%. The exact revenue is an integral, not a decimal endpoint.

## Actual execution scope

A disposable copy containing the reader and proof materials, with no root
`audit/` or `provenance/` tree and no inherited generated outputs, completed the
default `python -E -s -B -X utf8 verification/reproduce_all.py` run with exit 0
and `PUBLICATION_REPRODUCTION_PASS`. The unedited status transcript is
[reproduction_all.txt](reproduction_all.txt). It includes the complete
mathematical dependency chain: the base certificates, conditional-screening
checks, the coordinated component's 46 entries and both full upper traversals,
the portable component's thirteen mathematical replays and exact assembly,
and the final reserve arithmetic and implementation checks.

All 462 proof-input and Python files in that replay are byte-identical to the
retained package. After that copy was staged, three total-revenue symbols in
the appendix were clarified and their display was reflowed. The final 23-page
PDF was rebuilt and rendered separately; the actual final directory also
completed the release-only check with exit 0 and `RELEASE_CONSISTENCY_PASS`, recorded in [reproduction_release.txt](reproduction_release.txt).
After recording that result, only verification receipts were updated; the
root manifest was regenerated and all 491 stable files were rechecked.
The final source/PDF identities and execution statuses are recorded in
[final_validation.json](final_validation.json), [pdf_build.json](pdf_build.json)
and [pdf_render.json](pdf_render.json).

## Corrections and retained evidence

The reproduction guide and intermediate component now distinguish its
`tau=1/100` lower bound from the final selected mechanism. Conditional revenue,
fiber screening values, total revenue, orientations and exceptional endpoint
values are explicit. Conditional identities for the general jointly measurable
class are stated on almost every opponent fiber; the integrated inequality
covers the full stated mechanism class.

Windows drive-relative, root-relative and escaping paths are rejected. Child
Python processes ignore ambient Python import overrides and user-site imports.
The runtime record identifies the interpreter, NumPy and actual module paths.
All five regression tests passed again in the final directory, including fake
import-path injection and optimized-mode rejection; see
[runtime_guard_checks.json](runtime_guard_checks.json).

All 351 bound source files retain their pre-edit bytes. The seven changed
certificate files contain wrapper fixes, scope/role metadata and the required
manifest rebinding; every other field in the final reserve record is unchanged.
Source roles distinguish required inputs, independent checks, provenance and
unused candidates. No bound source file was removed. The obsolete internal
copies removed from the publication package comprised 272 old audit files,
10 discovery/provenance files and 117 generated authoring files. Still-useful
mathematical checks, current receipts and build/render helpers are retained
under `verification/`. No new research-history archive was created.

## What this validation does not establish

Replaying supplied code is distinct from an independent implementation and
from proving every analytic statement afresh. The opposing-excess integration
still has one full directed-arithmetic tree and bounded independent checks,
not two independent complete trees. Its documented IEEE binary64 and outward
rounding assumptions remain part of the trust boundary. Finite report tests
do not replace the manuscript's all-report DSIC, IR and capacity proofs.

The unrestricted optimum and a matching optimal mechanism remain unidentified.
This revision does not claim a new revenue improvement or a closed gap. No
remote commit, push or publication was performed.
