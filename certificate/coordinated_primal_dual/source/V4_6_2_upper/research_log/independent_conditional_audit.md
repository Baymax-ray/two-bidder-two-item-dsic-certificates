# Independent audit of the conditional global splice

The root reconstructed the whole-auction inequality, the opposing charged
screening bound, the two-bidder overlap, and the exact regional subtraction.
All match the corrected certificate.

A blocking error was found in the initial integration-cell classifier:
`sum >= b0 OR low >= k` did not guarantee the SJA bundle wins. In particular
radial cell n=16, i=14, j=3 crosses the low-coordinate upgrade threshold.
The bundle test now requires BOTH minimum sum >= b0 and minimum low >= k.
The entire seven-stage sequence was recomputed; the earlier larger
subtraction was discarded. No issued final bound uses that initial value.

The independent script reconstructs both averaged radial fields using
analytic derivatives and symbolic tensor Boole integration, then compares
all coefficients with the primary monomial integration. It also makes
20,968 exact menu-utility comparisons at included cell corners, using
quadratic-field sign tests, and checks 30 continuous cell integrals by
independent monomial primitives against integer Horner tables. The named
crossing-cell regression is mandatory. Default replay passed.

The proof uses cellwise Jensen LOWER bounds on a nonnegative continuous
virtual-allocation slack. Unclassified boundary cells are omitted, so no
finite allocation grid or finite IC relaxation is being promoted to an
upper certificate. The candidate single-buyer allocation is used only to
identify an exact nonnegative slack; competitors remain unrestricted.

The root also reviewed the alternative lottery-support redistribution:
its exact trace expansion, nonnegative terminal-average terms, and IR
sink bound are valid. Its remaining fixed-face price is still consumed
on an opponent-null set. It is recorded as an alternative valid support
and diagnostic, not used in the numerical incumbent.
