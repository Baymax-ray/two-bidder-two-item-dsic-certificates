# Inherited upper and face-moment component


**This component reports an intermediate lower mechanism at `tau=1/100`.**
Its `0.8765122087...` lower enclosure and `99.3382%` guarantee are valid
component results. The final paper uses `tau=83/10000`, revenue beginning
`0.876514341027...` and a guarantee above `99.3384%`; see
[the final reserve package](../reserve_parameter/README.md) and
[its manifest](../reserve_parameter/manifest.json). The unrestricted upper
computed here is still the final paper's upper.

Run `python -E -s -B -X utf8 verify_v5.py` from this directory after placement under
the archive's `certificate/` directory. Python 3.10 or later and NumPy are
required. The staged audit copy can be tested with `--archive-root PATH`.
`--temp-root PATH` selects an existing short temporary parent when Windows
path-length limits require it.

The wrapper checks every bundled source and named archive dependency, copies
the bound source inventory into a disposable original-layout
tree, performs thirteen mathematical replays plus independent exact assembly, and
checks all copied and original identities again. It does not read the original
AI4MATH research workspace. The original source files are preserved byte for byte. `source_bindings.json`
labels every file by `role` and `status`, including accounting-only inputs,
nonexecuted provenance and unused candidates. File binding does not imply
that a candidate contributes to the final bound.

The thirteen replays cover V5 global support, BB, face moments, complete primal,
independent primal, both upper audits, the inherited V4.8A primary and
independent master, and the V4.6.3 numerical remainder at explicit depths
20/20/26, plus this audit's fresh independent face cubature, primal structure,
and upper checks. The remainder is a full recomputation, not a hash-only allowance.
It can take several minutes. The selected lower mechanism and V4.6.2 upper
remain explicit dependencies of the archive's `coordinated_primal_dual`
package; that package's `verify_coordinated.py` replays their older chain.

`portable_assembly.py` independently checks the exact reduced upper formula
`U_V462 - E_lower - G_master - G_splice - G_BB`, all numeric fields of the
unchanged V5 phase ledger, the independent primal endpoints, and a conservative
99.3382% of OPT guarantee. It also verifies algebraic cancellation of the old
first-event deduction. The canceled first-event theorem and V4.8B support
proposal are not required to establish this reduced upper endpoint.

The original `phase_ledger.py` and `run_all.py` are retained as provenance but
are not this package's entrypoints: they demand the original 4,278-file
workspace preservation inventory. That historical preservation result is
separate from portable mathematical assembly. This package does not fake,
monkeypatch, or claim to rerun that inventory.

`provenance_adapter.py` handles a limited portability issue. Both V5 upper
audit outputs record one absolute external stream-manifest path; some source
outputs also record platform-specific path separators. The adapter preserves
all source hashes and compares all arithmetic results, counts and nonpath
fields exactly. Only those provenance keys are canonicalized. The two audit
functions run unchanged in write mode inside the disposable tree so their
full result can be compared; their temporary JSON outputs are then restored
byte for byte. The numerical remainder's unchanged `calculate` function runs
with explicit `depth_b=20, depth_d=20, depth_avg=26`; only its two relative
dependency-key separators are normalized. No arithmetic or proof condition
is removed or weakened.

The fresh independent audit files retain their original parent-directory
structure in the temporary tree. Their complete computed receipts are checked
against the preserved receipts. The fresh face program always writes its
receipt; the adapter restores it, normalizes only its absolute upper-source
provenance path, and excludes its measured `elapsed_seconds` from equality.
That elapsed value must still be finite and nonnegative. All exact values,
enclosures, predicate counts and source hashes remain equality-checked.

The manifest binds package files and the archive dependency list. A successful
replay certifies these finite computations and their dependency identities;
the documented continuum arguments and inherited mechanism/duality theorems
remain mathematical dependencies. Expected-utility DSIC and pointwise IR on
`[0,1]^4` retain the archive's convention of averaging over internal lotteries.
The mechanism and upper certificate do not match; unrestricted OPT remains
open. Predecessor Q/E/W conditional-optimality coverage is not transferred to
the transformed mechanism.

The runner validates resolved paths strictly inside their declared roots,
including rejection of Windows drive-relative and root-relative names.
Direct Python children use `-E -s`, a cleared ambient `PYTHON*` environment,
and an explicit no-user-site setting for legacy descendants. A runtime probe
prints the Python executable/version, NumPy version, import flags and resolved
paths of NumPy and core arithmetic modules. The same command policy is used
for the replays. This records the interpreter and installed-library trust
boundary; it is not a hermetic build or proof that vendor site initialization
is harmless. `verification/test_portable_runner.py` exercises the path and
import-environment policy from the package root.
