# Discovery-only provenance

Nothing below this directory is a proof artifact. Floating-point objectives,
sampled envelopes, optimizer diagnostics, and incompletely certified candidates
must not be cited as theorem values. The trusted path is confined to
`../../certificate/` and the analytic manuscript.

`higher_degree_search/` retains compact immutable JSON snapshots from the
degree-3, degree-4, and degree-5 witness search and early fixed-point partition
experiments. The historical search scripts were intentionally omitted because
they depended on exploratory workspace paths and are unnecessary for replaying
the release theorem. The exact degree-4 candidate that entered the theorem is
defined independently in the trusted upper-bound manifest.

The principal discovery lesson was that objective quality and certificate
quality separated near winner-switching surfaces. A one-step, strictly
improving adaptive partition of the unresolved depth-20 boxes bridged enough of
that gap to produce the release bound. See `../final_sprint_report.md` for the
bounded route comparison and freeze decision.
