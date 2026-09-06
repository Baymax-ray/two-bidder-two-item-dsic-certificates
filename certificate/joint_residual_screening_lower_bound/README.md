# Joint residual-screening lower certificate

This portable package certifies a complete randomized pointwise DSIC,
ex-post IR and jointly feasible mechanism with exact revenue in
[0.8758198541484224553460, 0.8758198541484224553461]. Combined with the
unchanged global upper 3715139591287203/4194304000000000, the gap is
strictly below 1/100. The mechanism earns at least 98.8779% of unrestricted
optimal revenue. It is not proved globally optimal.

The theoretical additions are full randomized conditional capacity supports
for a diagonal hole and a lottery junction, plus complete joint reallocations
suggested by their binding constraints. Competitors need not have finite
menus. The final F/Q and restricted Eplus coverage is stated in the paper and
source/V4_6/research_log/conditional_coverage.md.

Run from this directory or any working directory:

```powershell
python -B -X utf8 verify_joint_residual.py
```

The supported entry point verifies all source identities, runs 29 declared
mathematical entry points in separate processes, adds four fresh independent
audit checks, and verifies the exact rational strict-gap and revenue-ratio
inequalities. No original workspace paths or numerical solver are needed.
Default execution is read-only. Do not use optimized Python.

`source/` is a selected proof dependency snapshot preserving the original
relative version layout. It includes the mathematical runtime closure and
proof notes, not every historical research/discovery file. Old full-archive
preservation runners are intentionally not advertised or included. The
supported entry points are enumerated in entrypoints.json and the root
runner; arbitrary historical commands in copied notes may require their
original research archive. Two small dormant JSON dependencies are included
as a conservative static supplement to the traced closure.

`source_bindings.json` pins every exported source file. The original V4.6
manifest is provenance, not a manifest of this selected export. Independent
proof and arithmetic audits are in audit/. Read ERRATA.md with the verbatim
historical notes. Those two wording clarifications are adopted in the paper.

The exact expression is in manifest.json and the paper. New increments are
reconstructed using rational polynomials, radicals and logarithms. The
historical V4.5 exact integral and enclosure are an explicit dependency;
this is not a new from-scratch integration of every historical base layer.
The global upper certificate remains in its separate sibling package.
