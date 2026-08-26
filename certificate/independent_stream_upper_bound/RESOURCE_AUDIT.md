# Resource and arithmetic audit

- Shallow paired-Fraction audit: one run, about 61.2 seconds wall time.
- Full scale-1e9 independent replay: one run, about 633.2 seconds wall time.
- Python 3.10.16; NumPy 2.0.1.
- Maximum initial absolute control: 1,475,346,733.
- Maximum axis degree: 8; maximum propagated radius through depth 21: 169.
- Conservative maximum stored magnitude: 1,475,346,901.
- Conservative pair-sum bound: 2,950,693,802.
- Conservative single-box common-depth numerator: 3,094,026,706,223,104.
- Signed-int64 limit: 9,223,372,036,854,775,807.

All NumPy additions are therefore strictly inside signed-int64 range.  The
accumulator is a Python integer and is also below that limit.  The proof JSON
transcripts omit runtime so their bytes are deterministic.  Optimized Python
mode is explicitly rejected before any assertion can be skipped.

The earlier scale-1e8 result was a same-code precision stress test of the
discovery/formal adaptive implementation.  It is not an independence check.
The scale-1e9 run recorded here is the new clean-room independent replay.
