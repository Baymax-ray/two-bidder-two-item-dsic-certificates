# V4.6.1.1 lower-bound branch

The new complete mechanism has exact revenue

\[
R=0.876464164471798049944906113027\ldots,
\]

strictly exceeding V4.6.1 by more than **0.0000085**. The result is a
continuum lower bound, with a pointwise DSIC/IR/feasibility proof and two
independent exact revenue calculations. Unrestricted auction optimality
remains open.

- [Report and complete mechanism](REPORT.md)
- [Exact result ledger](certificate/branch_summary.json)
- [All-real structural proof](research_log/refined_structure_audit.md)
- [Independent revenue derivation](research_log/refined_revenue_audit.md)
- [Conditional revenue-gap map](research_log/conditional_gap_map.md)
- [Verification scope and replay](VERIFICATION.md)

From this directory, run the read-only checks with:

```powershell
python -B -X utf8 verifier/run_all.py
python -B -X utf8 verifier/verify_manifest.py
```

Use Python without `-O`. The current branch's verifier entry points use
the standard library. They import preserved exact-arithmetic helpers from
earlier auction versions; keep the surrounding version directories in
place. Discovery JSON files record floating searches and are not proof
certificates. The replay excludes discovery and does not rewrite results.

The selected mechanism is `verifier/refined_candidate.py`. Other candidate
files in this branch are comparison experiments; their gains must not be
added to the selected revenue. This branch preserves the 52-file V4.6.1
package and manages only its own output directory and manifest.
