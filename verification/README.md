# Reproducing the revenue certificate

The final mechanism uses `tau=83/10000` and guarantees more than **99.3384%**
of unrestricted randomized DSIC optimal revenue. The exact expressions and
certified intervals are in the [final manifest](../certificate/reserve_parameter/manifest.json).
The optimal mechanism and a matching upper bound remain open.

From the package root, with Python 3.10 or newer, NumPy and a supported TeX
installation (see [ENVIRONMENT.md](../ENVIRONMENT.md)), run:

```
python -E -s -B -X utf8 verification/reproduce_all.py
```

The default checks the text and compilation first, then runs the mathematical
certificates and verifies the complete file-hash inventory. Use `--checks math`
for the mathematical checks alone, or `--checks release` for text, compilation
and hashes. To save your own log, add
`--transcript verification/generated/reproduction.txt`; this optional directory
is created when needed and excluded from the hash inventory.

## Files

| File | Purpose |
|---|---|
| `reproduce_all.py` | Runs the certificate dependency chain and checks the final numerical claims. |
| `verify_hashes.py` | Checks every supplied stable file against the root `SHA256SUMS`. |
| `joint_explanation_check.py` | Independently checks the rational polygon integrals and fee identities used in the joint mechanism's revenue derivation. |
| `test_portable_runner.py` | Checks the runner's path handling, Python import isolation, rejection of optimized mode and exact zero-value margins. |

The mathematical chain includes the seed certificates, coupled IC and capacity
certificates, face moments, final reserve arithmetic and rational-report boundary
checks. The intermediate upper/face package reports `tau=1/100`; the final
reserve checker supplies the paper's selected `83/10000` mechanism and revenue.
The original research workspace is unnecessary: the wrappers stage the supplied
inputs in temporary directories and verify their identities.

## Scope of verification

Hash agreement establishes file identity. The pointwise DSIC, IR, feasibility
and unrestricted upper-bound arguments are in the manuscript and its analytic
sources. Finite implementation checks do not replace these continuous proofs.

The seed revenue and stream majorant have independent full reconstructions.
The conditional subtraction combines a full accumulation with independent
coefficient and bounded checks. The shared-cell master system has a separate
complete replay. The opposing-excess tree has one full directed-arithmetic
implementation and bounded independent checks. The manuscript specifies these
independence levels and the arithmetic assumptions.

Proof kernels use assertions: do not use `-O`, `-OO` or `PYTHONOPTIMIZE`.
The runner checks the execution environment and emits Python/NumPy versions
and module locations. The installed interpreter and libraries remain trusted.
