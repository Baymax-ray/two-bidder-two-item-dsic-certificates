# Conditional revenue-gap map

This map distinguishes an exact inner value gap against a fixed actual
residual from a gain requiring a coordinated outer allocation change.
Unresolved cells are not assigned zero. All regions describe the opponent's
continuous report, and the bidder label matters.

## Certified baseline V4.6

Use its original constants `a=159/250`, `c=137/500`, `b=91/100`,
`A=2/3`, `b0=(4-sqrt(2))/3`, and `z=sum(v)`.

| Opponent region / bidder | Actual conditional gap | Evidence and implication |
|---|---|---|
| F: max(v)<=1/2, z<=b0; both | 0 | Full-capacity optimum already attained |
| Q: max(v)<=A, z<=b; bidder 2 | 0 | V4.6 full residual certificate; improvement requires outer change |
| max(v)<=1/2, b0<z<=b; bidder 1 | Gamma(a,z)>0 | Entire menu can be replaced by `(A,A,z)` |
| max(v)<=1/2, b<z<=A+c; both | Gamma(z-c,z)>0 except the upper endpoint | Both whole-menu replacements compose pointwise |
| Certified Eplus fibers outside V4.6 corner exclusions | 0 | Use the exact bidder-dependent exclusions in the predecessor coverage map |
| Remaining Q fibers for bidder 1 | Not identified here as a fixed-residual gap | A complete Q mirror with coordinated tie choices improves total revenue |
| Remaining opponent space, including excluded corner fibers | Unresolved | No zero-gap or optimizer claim |

The exact positive gap function is

\[
\Gamma(P,z)=3(A-P)^2(z-A)+2(A-P)^3.
\]

This is the difference between the unrestricted randomized residual value
and the actual old deterministic menu revenue on the specified low-square
fibers. Candidate feasibility and a full diagonal-hole measure certificate
supply the matching upper bound; it is not just a comparison of two menus.
Integrating the two low-square rows gives the exact total gain

\[
\frac{1291191981929}{3164062500000000}
-\frac{180389}{632812500}\sqrt2
\approx0.00000494589800751369.
\]

See [gap_low_square.md](gap_low_square.md). At a fixed low-square own type,
these replacements leave the opposing realized expected allocation
unchanged, so the stated gap refers to the actual baseline residual.

The upper endpoint `A+c=1411/1500` is a real capacity boundary. The profile
`v=(.49,.49), w=(.68,.28)` has bidder 2 taking a bundle in the baseline;
replacing the opposing singleton by price A would overallocate. Inspecting
only the axis `w2=0` misses this obstruction. Above the certified region,
scalar price reduction is not an admissible extension.

## Independent symmetrization experiment

Mix strongest V4.6 with its bidder-swapped version with equal probability.
Revenue is unchanged and pointwise expected DSIC/IR and feasibility are
preserved. On G={max(v)<=1/2,b0<z<b}, fully re-optimize bidder 1 while
holding this mixture's bidder 2 pointwise fixed. The full optimizer is
`(A,A,z)`, with certified exact gain

\[
\frac{30892611299}{151875000000000}
-\frac{180389}{1265625000}\sqrt2
\approx0.00000184087481579964.
\]

The residual has levels zero, one half, and one on explicitly identified
sets. The matching capacity support avoids its fractional intermediate
region. This proves a strict gain after symmetrization, but does not prove
that essential fractional allocation is required there. The direct
low-square replacement gives a larger gain. See
[sym_rescreen.md](sym_rescreen.md).

## Coordinated Q replacement and outer parameter change

A complete mirror of bidder 2's Q menus to both bidders, starting before
the tiny corner correction and using jointly feasible menu-maximizing ties,
gains about `0.0000252283325640061` over strongest V4.6. Its conditional menu
revenue difference is integrated exactly. Because tie selections may change
on both sides, it is not labeled a fixed-actual-residual gap throughout Q.
See [sym_full_q_mirror.md](sym_full_q_mirror.md).

Re-optimizing the larger symmetric mechanism moves the reserve to A and the
bundle increment to 47/150. This is the selected new candidate, with total
gain greater than .00063. These gains are alternatives, not additive patches
on top of each other.

## Selected V4.6.1 mechanism

Now `a=A=2/3`, `c=47/150`, `b=49/50`, `T=178/225`.
For **both bidders**, the actual residual gap is exactly zero throughout

\[
Q=\{\max(v)\le A,\ \sum v\le b\},\qquad
E=\{A<\max(v)<T,\ \min(v)<c\}.
\]

All old corner exclusions disappear. The low-square extension ends at
`A+c=b`, so it is already part of symmetric Q. The revised inequalities,
occupied traces, zero top mass, and IR sink were independently verified at
the new parameters. These are full randomized conditional certificates,
not finite-menu or finite-grid optima.

The remaining region is unresolved. An improvement there may replace a
whole conditional menu. An improvement affecting Q or E must change the
outer residual or its coupled equality conditions; conditioning alone
cannot beat the existing certificate. This is an exact region map, not a
classification of all globally optimal mechanisms.
