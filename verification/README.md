# Publication verification

`reproduce_all.py` is the release orchestrator. It reruns the two exact lower
certificates, the formal adaptive upper certificate, the independent shallow
Fraction audit and full replay, theorem/README consistency checks, a clean
temporary-directory LaTeX build, and the root SHA-256 verification.

`make_hashes.py` creates `../SHA256SUMS`; `verify_hashes.py` requires exact
coverage of every stable file. Generated clean-run transcripts under
`generated/` and temporary LaTeX build products are intentionally excluded
from the root manifest. The release PDF and all frozen certificate transcripts
are included.
