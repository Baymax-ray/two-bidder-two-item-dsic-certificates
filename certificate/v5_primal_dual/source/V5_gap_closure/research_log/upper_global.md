# V5 independent global-upper audit and alternative curl trial

The enlarged conditional-support substitution in `global_duality.md` passes
independent source-aware review and a fresh full continuous-cell replay. Its
certified decrease from the inherited radial-plus-stream envelope with the
old low-square splice is

\[
G_{\rm splice}\ge 0.00045027837569474655\ldots>0.
\]

The exact rational value is recorded in
`../certificate/global_duality.json` and independently recomputed in
`../discovery/upper_splice_audit.json`. The decrease is a whole-auction
common-capacity-envelope comparison, not a conditional revenue gain counted
without its opposing cost. It does not close the optimality gap.

This note also records the independent translated-IC algebra audit and an
alternative QQ curl trial. The QQ trial is **not an accepted upper-bound
improvement** and must not be added to the splice decrement.

## 1. Scope and files

The primary splice proof, verifier, and certificate were read without edits:

* `research_log/global_duality.md`;
* `verifier/global_duality.py`;
* `certificate/global_duality.json`.

The independent checker `discovery/upper_splice_audit.py` first executes the
entire primary default replay, then performs additional exact `Fraction`
comparisons independently of the floating interval transformations. It pins
the three primary files and the archived stream manifest by SHA-256.
Its generated result is `GLOBAL_SUPPORT_SPLICE_INDEPENDENT_AUDIT_PASS`.

The primary replay covers all 294 root boxes and 12,294 terminal boxes,
including all 12,000 recorded subdivisions. The supplementary exact checks
cover:

* 1,251 monomial-integral enclosure comparisons;
* 1,182 rational-coefficient bracket comparisons;
* 132 tensor Bernstein controls reconstructed directly from exact rational
  formulas on 12 selected roots;
* the exact factor-four lower-bound formula and all pinned source identities.

The supplementary checks do not claim to reconstruct every Bernstein
control independently. Full coverage comes from the primary replay; the
second implementation checks selected transformation outputs and the
coefficient and integration primitives.

## 2. Why the support substitution is global

For each fixed opposing report \(w\), any pointwise randomized DSIC/IR
mechanism has a convex utility \(u(v;w)\) and its selected allocation
\(a(v;w)\in\partial u(v;w)\cap[0,1]^2\). Let
\(\bar u=u-u(0;w)\), so \(0\le\bar u\le2\).

The inherited radial-plus-zero-trace-stream identity and full-capacity
screening identity are, respectively,

\[
R(w)=\langle\phi(\cdot;w),a(\cdot;w)\rangle-u(0;w),
\qquad
R(w)=\langle\Psi,a(\cdot;w)\rangle-3\int_{D_0}u(v;w)\,dv.
\]

Here
\[
D_0=\{x,y\le2/3,\ x+y\le(4-\sqrt2)/3\},\qquad |D_0|=1/3.
\]
The second identity has its utility source explicitly retained. The
nonnegative support \(\Psi\), or its item swap, vanishes on \(D_0\), and
\[
\int(\Psi_1+\Psi_2)=R_0=4/9+2\sqrt2/27.
\]

The enlarged opponent domain is
\[
W=[0,43/100]^2,\quad
J=(43/100,1/2]\times[0,7/20],\quad
D^\sharp=W\cup J\cup J^s\subset D_0.
\]
The support identity switches according to the *opponent's* report.
Consequently no own-type derivative of the indicator, boundary flux,
or singular source is being suppressed. In normalized form the exact
remaining source is
\[
u(0;w)+3\,1_{D^\sharp}(w)\int_{D_0}\bar u(v;w)\,dv.
\]
It is nonnegative for every complete DSIC/IR mechanism. Measurable selected
subgradients and exceptional reports are allowed; no finite allocation range
or finite type set enters the argument.

If \(A_{ij}\) are the two substituted fields, the common capacity price is
\[
\Pi_j=\max(0,A_{1j},A_{2j}).
\]
Every bidder's unrestricted charged screening problem has value zero:
the retained source and \((\Pi-A_i)\cdot a_i\) are nonnegative, and the empty
mechanism attains zero. Summing and using actual joint pointwise capacity
gives \(\mathrm{OPT}\le\int\sum_j\Pi_j\). In particular, positive opposing
virtual values are charged by the same maximum; they are not discarded.

The exact gap consists of the retained screening/IR sources, priced unused
capacity, virtual-allocation mismatch, and any retained weighted IC terms.
For the frozen V4.6.1.1 mechanism the new source on \(D^\sharp\) is zero
because its conditional menu there is exactly the SJA menu. That last
zero-slack assertion is specific to the frozen incumbent. If the V5 primal
branch changes its menus, its screening source must be recomputed; the
universal upper inequality itself is unaffected.

## 3. Overlap accounting and numerical enclosure

For \(w\in J\), write \(a=\phi_j(v;w)\), \(b=\phi_j(w;v)\),
and \(p=\Psi_j(v)\). The directed decrement
\[
a_+-p-(b-p)_+
\]
is a valid lower estimate when the other report is outside the new domain.
When both reports are in the added rectangles, the two directed estimates
cancel exactly, while the actual old envelope is nonnegative and the new
envelope is zero. When the other report is in \(W\), the inherited
whole-square sign theorem and vanishing support make the directed estimate
nonpositive, so it is again safe. Exact item covariance then gives
\[
G_{\rm splice}\ge4\{L-|J|R_0-E\},
\quad |J|=49/2000,
\]
where
\[
L=\int_J\!\int\sum_j(\phi_j(v;w))_+,\qquad
E=\int_J\!\int\sum_j(\phi_j(w;v)-\Psi_j(v))_+.
\]
This explicitly charges the opposing bidder and the simultaneous switch
on both sides.

The replay certifies
\[
L\ge119448693432877/8796093022208000,\qquad
E\le0.000011750019243246275\ldots.
\]
The first enclosure averages exact opponent-polynomial coefficients, uses
the two radial charts with their Jacobian, and applies convexity of the
positive part on every complete integration cell. It does not infer signs
from samples. The second uses a rational lower support for \(\Psi_1\),
the valid lower support zero for \(\Psi_2\), positive denominator \(2w_1^2\),
and a tensor Bernstein integral upper bound over every root and terminal box.

The interval code brackets exact rational coefficients and expands
arithmetic operations outward with `nextafter`. De Casteljau subdivision
uses upward-rounded convex combinations of upper controls. Exact rational
box volumes and denominator bounds, checked dyadic integer accumulation,
and an integer-square-root bracket for \(\sqrt2\) complete the bound.
Basic IEEE-754 binary64 operations and correct `nextafter` remain explicit
trusted arithmetic assumptions. The written weak identities and inherited
low-square sign theorem also remain theorem dependencies; a successful
replay is not a formal proof-assistant kernel.

The old sparse cycle and BB master corrections are disjoint from the
new support domain and can be retained. The old QQ first-event corrections
overlap. Giving back the **entire inherited first-event subtraction** before
adding the new splice gain is conservative. The new BB translated-IC
support is also disjoint. The separate QQ curl below overlaps and is never
added to this gain.

## 4. Independent translated-IC checks

`discovery/upper_bb_audit.py` and `.json` record
`BB_FULL_ENVELOPE_ALGEBRA_AND_SOURCE_AUDIT_PASS`. The audit independently
reconstructs 1,576 centered polynomial coefficients from the archived source,
checks 2,592 exact scalar first-event max identities, 648 chart point
enclosures, and 225 interval multiplication cases.

For endpoints \(B=A+(3/20,-1/40)\), a nonnegative two-way IC measure of
density \(\lambda\) changes the own virtual field by
\(\lambda(-3/20,1/40)\) at \(A\), and its negative at \(B\). Where the
virtual-own allocation changes from \(00\) at \(A\) to \(01\) at \(B\),
stopping at the first zero or winner tie reduces the envelope by
\(\lambda/40\). Both directions of IC retain their actual nonnegative
weighted slack. Tightness at the incumbent is not assumed.

This algebra/source audit is not a replacement for the root branch's
continuous selected-box certificate. It checks the construction on which
that separate acceptance proof rests, including exact field reconstruction
and the correct first-event formula. The translated boxes and their four
symmetry copies have disjoint interiors; shared null boundaries can be
assigned zero density.

A separate fresh default run of the final exact-Fraction
`verifier/bb_global.py` also passed, rechecking all 64 selected endpoint
box pairs and certifying
\[
G_{\rm BB}=4786305147/17179869184000000.
\]
Its complete finite-measure proof and correlated regional slack identities
were reviewed. With \(g=\lambda/40,h=3\lambda/20\), endpoint A's incumbent
allocation is item 2, while endpoint B has bidder allocations \(a,b\).
The changes
\[
\Delta C=-g(1-a_2-b_2),\quad
\Delta K=h a_1+g(1-a_2),\quad
\Delta V=-g-h a_1-g b_2
\]
sum to \(-g\) exactly. The 27 boxes where a menu interface prevents a
constant endpoint-B choice retain the full allocation ambiguity; they are
not classified as having zero additional IC or capacity slack.

## 5. Alternative QQ compact-curl trial: no accepted gain

The independent discovery route tested the full common-envelope effect of
a compact continuous tent stream, with no requirement of incumbent
complementarity. Its weak curl has zero pairing with every bounded
gradient of a convex utility because the stream vanishes at the own-type
support boundary. Thus there is no missing IC or utility cost. The trial
still accounts for both bidders through the maximum envelope.

The final interval trial uses amplitude \(-1/500\), own tent center
\((13/25,99/400)\), own half-widths \((2/25,31/400)\), and opponent rectangle
\([11/25,33/50]\times[1/100,13/40]\). Its support was trimmed to avoid
the inherited corridor endpoint boxes. It nevertheless overlaps the new
conditional-support splice, so their gains cannot be added without
reevaluating the combined maximum.

The 64,000-leaf continuous interval computation in
`verifier/upper_global.py` / `certificate/upper_global.json` encloses its
envelope decrease by
\[
-5.24801322582032\,10^{-7}
\ \le G_{\rm curl}\le\
5.026045237218986\,10^{-6}.
\]
The certificate status is `ENCLOSURE_NOT_YET_POSITIVE`. It is a rigorous
enclosure with an inconclusive sign, not a certified improving correction.
Float discovery suggested a positive effect; that suggestion has no role
in the accepted upper endpoint. Further subdivision was stopped because
the enlarged support splice had already supplied a much larger certified
global decrease.

This interval uncertainty proves neither that the compact-curl family has
no gain nor that any interface is unrepairable. It provides no evidence
that the incumbent mechanism must change.

## 6. Reproduction

From the auction directory, with assertions enabled:

```text
python -B -X utf8 V5_gap_closure/discovery/upper_splice_audit.py
python -B -X utf8 V5_gap_closure/discovery/upper_bb_audit.py
```

Both default audit entry points compare their read-only recomputations to
stored evidence. The splice entry point also runs the full primary
continuous replay. The much longer QQ enclosure replay is separate and is
not needed to accept either improved upper-bound component.

All predecessors were preserved. These checks support the accepted global
upper improvements within their stated dependencies; they do not identify
an optimal mechanism or establish equality between the lower and upper
bounds.
