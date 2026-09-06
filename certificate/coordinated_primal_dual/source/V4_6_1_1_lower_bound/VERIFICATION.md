# Verification record

The coordinated read-only replay completed with exit code 0 on 2026-09-06:

```text
V4_6_1_1_EXACT_REPLAY_PASS mathematical_replays=14 plus 12 preserved V4.6.1 replays
```

The complete captured output is [final_replay.txt](research_log/final_replay.txt).
The command was `python -B -X utf8 verifier/run_all.py`, with output saved
inside this branch. No optimized Python execution was used.

## Selected mechanism and revenue

| Obligation | Result | Evidence |
|---|---|---|
| Complete real-report definition, DSIC, IR, joint feasibility, measurable tie rule | All-real case proof audited; rational implementation replay passed | [Structural proof](research_log/refined_structure_audit.md), [candidate certificate](certificate/refined_candidate.json) |
| Candidate implementation and reallocation witness | 8,961 exact profiles; 16 witness-box corners plus separate uniform scalar inequalities | [refined_candidate.py](verifier/refined_candidate.py) |
| Independently reconstructed menus and capacity traces | 47 menus, 2,209 profile pairs, 64 positive-tie profiles; source comparisons for 47 menus and 188 profiles passed | [Structural audit certificate](certificate/refined_structure_audit.json) |
| Exact continuum revenue | Three algebraic coefficients agree exactly between independent integrations; 45 direct conditional polygon checks passed | [Root calculation](certificate/refined_revenue.json), [independent calculation](certificate/refined_revenue_audit.json) |
| Strict improvement over preserved V4.6.1 | Exact rational radical enclosures prove gain >17/2000000 | [Final ledger](certificate/branch_summary.json) |
| Full randomized conditional optimality on Q and E | Inherited envelope identities applied with new hypotheses and actual-capacity checks; E junction repaired using pointwise IC | [Structural proof, Sections 7–8](research_log/refined_structure_audit.md) |
| Full randomized conditional optimality on W | New all-real screening identity and occupation proof; 168 exact continuous-menu identities and 12,220 actual candidate profiles passed | [Wing proof](research_log/residual_wing_screening.md), [certificate](certificate/residual_wing_screening.json) |

The independent revenue calculation does not import the root's
`constant_kernel` or use `refined_candidate` as its calculator. It uses
direct conditional-menu integrals and Green boundary integration. The
root calculation uses a different polynomial representation and simplex
moments. The implementations share rational arithmetic and inherited
mathematical definitions; this is independent computational reconstruction,
not two entirely independent foundational formalizations.

A separate [final mathematical cross-audit](research_log/final_cross_audit.md)
rechecked the complete case proof, exceptional reports and actual-residual
screening identities and found no blocking issue. The
[report audit](research_log/report_audit.md) checked the displayed values,
tie rules, areas, references and limits of the claims against the frozen
source and replay evidence.

The structural auditor reconstructs the menus before comparing them with
the source implementation. Its finite checks support a written all-real
argument. They do not prove continuum DSIC by grid sampling. The envelope
proofs explicitly cover arbitrary measurable randomized conditional
competitors; a finite candidate menu is not a finite-menu assumption on
the upper-bounded class.

## Other branch checks

The same replay also passed the exact integrated functional kernel,
7,061-profile affine-jump trial, the restricted analytic functional
optimizer with 927 rational profiles and five algebraic tie cases,
reserve and safe-cap alternatives, split-direction comparisons, the
incentive-derived trace argument, and the preserved-baseline high-region
screening identity (98 continuous-menu identities and 488 profiles).
These alternatives establish their own bounded claims; their revenue
gains are not added to the selected combined mechanism.

The three `*discovery.json` files are floating numerical discovery
records, excluded from proof replay. The selected parameters have been
separately rationalized and verified exactly. Neither their numerical
search nor the restricted analytic optimum proves unrestricted parameter
or auction optimality.

## Preservation and package checks

The final run verified that the saved V4.6.1 manifest is byte-identical
to its current manifest, that all 52 listed files retain their hashes,
and that the predecessor inventory is complete. The replay also passed
the predecessor's checks for 992 older live identities plus one archived
navigation identity, and the 47-file V4.6 manifest.

The current outer navigation and outer manifest differ from that older
archived snapshot; the replay reports this explicitly. They are outside
this branch's managed scope. No claim that they remained unchanged is
made. No predecessor, publication package, or concurrent upper branch
was edited by this branch.

After the report audit, run the separate checks:

```powershell
python -B -X utf8 verifier/artifact_audit.py
python -B -X utf8 verifier/verify_manifest.py
```

The first validates JSON syntax, local Markdown targets and formula
delimiters. The second verifies `SHA256SUMS`, including complete stable-file
coverage and unchanged files during verification. Hashes establish
artifact identity and coverage, not mathematical validity. Mathematical
claims depend on the displayed proofs and exact replays described above.

All outputs for this phase are contained in `V4_6_1_1_lower_bound`.
The complete verification is not a proof-assistant formalization and
does not supply a matching unrestricted auction upper bound. Further
joint allocation improvements remain possible.
