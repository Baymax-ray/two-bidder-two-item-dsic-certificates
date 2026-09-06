# V4.6.1 — lower-bound branch

The selected mechanism has exact revenue

`309078860435260513361/367416000000000000000 + (31/1215)*sqrt(2) - (170368/664453125)*sqrt(11)`

or approximately **0.8764556138363259**, improving V4.6 by approximately
**0.0006357596879034**. The main construction rebuilds three menu regions
and global constants; a coordinated monotone exchange gives a further
exact gain. Both complete mechanisms are preserved.

- [REPORT.md](REPORT.md): result, complete menu specification, and scope.
- [Conditional gap map](research_log/conditional_gap_map.md): exact screening gaps, symmetrization, and unresolved regions.
- [Full mechanism proof](research_log/parameter_rebuilt_family.md).
- [Functional refinement proof](research_log/functional_exchange.md).
- [Selected candidate evaluator](verifier/functional_exchange.py).
- [Verification record](VERIFICATION.md).

From the auction package directory:

```powershell
python -B -X utf8 V4_6_1_lower_bound/verifier/run_all.py
python -B -X utf8 V4_6_1_lower_bound/verifier/verify_manifest.py
```

Default replays are read-only. Floating discovery is separate from exact
certification and is not run by the verifier. Predecessor file identities
are checked separately. This branch does not manage the concurrently
updated outer navigation or manifest; it has its own manifest.
No unrestricted or family optimality is claimed.
