# Portable replay correction

The initial isolated run passed every mathematical entrypoint but failed the
final staged-byte check because the fresh support audit rewrote its JSON with
absolute temporary paths. The new audit helper now defaults to comparing a
saved record and uses normalized repository-relative source names; only an
explicit --write regenerates it. Every mathematical JSON field and every
source hash value was unchanged by this correction. All 46 entrypoints were
then rerun in a fresh isolated mirror and final byte checks passed.

This change affects the new audit helper only. The original V4.6.1.1 and
V4.6.2 source branches and inherited mathematical inputs were not changed.
The first reviewer packet predates this correction and remains frozen; the
post-review ledger records the corrected release evidence separately.
