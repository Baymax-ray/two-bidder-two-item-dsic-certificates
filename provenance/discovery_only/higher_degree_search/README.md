# Higher-degree numerical snapshots

These JSON files preserve useful pre-certificate provenance:

- `qmc_degree*_p*.json`: sampled quasi-Monte Carlo optimizer outputs;
- `candidate_degree*_exact.json`: rational reconstructions proposed for exact
  checking;
- `exact_degree5_hybrid4_d18.json`: an early fixed-point Bernstein bound before
  the successful adaptive terminal refinement; and
- `partition_formal_d14.json`: a diagnostic localization of unresolved
  certificate slack.

The values are historical discovery records. In particular, sampled objectives
near `0.88325` are not rigorous upper bounds, and the early degree-4/5
fixed-point outputs are superseded by the trusted adaptive certificate.

One superseded degree-4 depth-20 snapshot was intentionally omitted from the
publication archive because a cached Boolean comparison field contradicted its
own displayed exact fraction.  The underlying rational witness is preserved
as `candidate_degree4_exact.json`, and the trusted adaptive verifier
reconstructs the release result directly from that witness.
