# Independent audit of the V4 mathematical report

**Outcome:** no blocking mathematical error found in the synthesis. This is
a proof-and-transcription audit; it does not certify the unresolved original
optimum or replace the report's stated analytic dependencies.

Audited `LaTeX/main.tex`, SHA256
`8300db3f13adc5ad78f93bf80c135128c775d8d458b4cb9124dc17b6568faf1c`.
Compared the appendix with preserved `V3/certificate/joined_threshold.json`,
SHA256 `188deeda1fd5d7e7cb01ef6353fe1b5a2758907543564aa7a47990a76badbbcd`.
The report source was not modified.

## Scope and normalization

The normalization argument is correct: the zero-type utility is an
opponent-only nonnegative offset, and subtracting it preserves all IC
inequalities and IR while increasing revenue. IC against type zero and IR
then give `0<=p<=v.x<=2`. The preserved phase-1 theorem expressly equates
the Borel and completed-Lebesgue scalar suprema. The report correctly uses
that scalar result and expressly refuses to assume that a Borel repair
preserves an arbitrary prescribed residual capacity.

The elimination identity uses one complete global Borel inner mechanism
within epsilon of the supremum, not an unjustified selection of optimizers
on separate opponent slices. The convex-potential formulation retains
selected relative subgradients at every report. Its integration-by-parts
objective does not replace those pointwise constraints by a.e. constraints.

## Equality, lower guarantee, and diagnostic certificate

The free-fiber construction is reported with an exact revenue equality and
an exact algebraic increment. The release construction is consistently
reported with only a lower guarantee. The latter bound follows from the
two top-face integrals of `min(u,epsilon)` and has the correct `-2 epsilon`
sign and coefficient. The report does not claim that release beats the
free-fiber mechanism or that either construction solves the remaining
constrained inner fibers.

The strict free regions, inherited continuation on their boundaries,
zero-utility rejection, and `u=epsilon` release tie agree with the audited
definitions. Changing bidder 2's menu by opponent report does not create an
unaddressed own-report IC inequality. The claimed positive-volume transfer
and free-fiber statements are consistent with their exact certificates and
the separate release implementation audit.

The diagnostic support genuinely bounds arbitrary two-item competing
mechanisms: the conditional first-coordinate envelope leaves the term
`z*x_2`, bounded by `pi_2=z dt dz`. Its transported first-item measure retains
actual exceptional reports. The report explicitly states that this support
belongs to the diagnostic residual, not either improved auction candidate,
and that the outer priced optimum is unproved.

The lottery necessity claim is limited to the diagnostic residual. The
nonexistence example concerns blanket countably additive support existence
for arbitrary Borel capacities. Neither is extrapolated to the optimum of
the original auction. The separate opportunity-cost discussion retains the
affine intercept, avoiding an unjustified Euler identity at a boundary of
the capacity box.

## Exact appendix and numerical statements

An independent in-memory `Fraction` check compared all 18 rational constants
and polynomial coefficient entries in the appendix with the inherited
certificate and its explicit baseline constant. It also checked

* `k0^2+K=b^2` and `k1^2+K=(c+2/3)^2`;
* that the displayed `P(k)` is exactly
  `(h-k)*[-3b(k^2+K)/2+b^3/2]` with `h=b-q`;
* the copied `J`, both integration endpoints, the factor four, and the
  signs of the three inherited/substituted gain terms;
* the displayed strict increment bounds against the exact free-fiber and
  release certificate intervals;
* the displayed new-revenue and remaining-upper-gap intervals against
  `certificate/combined_revenue.json`.

The exact check returned
`REPORT_APPENDIX_CONSTANTS_AND_DISPLAYED_BOUNDS_PASS`. No coefficient, sign,
endpoint, or equality-versus-bound transcription error was found.

The remaining unrestricted upper is correctly identified as inherited.
There is no claim of a new matching upper certificate, global inner
optimality at the actual candidate residual, or completed original optimum.
