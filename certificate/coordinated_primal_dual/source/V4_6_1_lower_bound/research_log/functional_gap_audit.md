# Independent audit of the functional exchange and its conditional gaps

**Verdict:** the displayed tent mechanism is pointwise feasible and DSIC/IR
on the full continuous domain, with the specified maximizing-pair tie rule.
The complete randomized conditional optimality certificates extend to
**both bidders throughout Q and Eplus** for its actual residual. This does
not certify the outer allocation, the chosen tent, or global optimality.

The audit fixes the constants of `parameter_candidate.py`, tent knots
`L=.32`, `M=.33`, `U=.34`, and `0<=epsilon<=.001`. No assertion below is
made for an arbitrary monotone h outside these hypotheses. The separate
root calculation audits the exact revenue variation.

## 1. Global feasibility, including ties

The function h(x)=x+q+epsilon*phi(x) is continuous and strictly increasing;
its two changed slopes are in [1,1.1] and [.9,1]. Its inverse agrees at
both outer image knots and the middle image knot. In particular,
`h(c)=.5`, `h(x)>=x+q`, and `h^{-1}(t)<=t-q`. The changed Q safe price
is strictly above .5. Zero-utility bidders always choose empty.

The Q/Q proof uses the full floor `C>=k+h(rho)`: a positive safe choice
has high value y>B>=h(rho), while the conflicting opposing bundle would
need rho>=h^{-1}(y). Those inequalities contradict strict monotonicity.
Two positive bundles are excluded by C>=sum(opponent); same high
orientations and free-Q branches are handled by the .5 singleton bound.
These arguments remain valid when a bundle/safe comparison is tied,
because the positive safe utility itself supplies the strict inequality.

For Q/base, let w=(t,rho) in Q and let v=(x,y) be the opposing base report,
aligned with w's high physical item. The w bidder cannot obtain a base
bundle or low singleton. If y<=.5 its high price is at least A>=t. If
y>.5 and x is in the tent support, x<.5<y, so the surcharge is applied to
exactly that physical item's base price. Its price is at least h(x).
Outside the support the same inequality holds with h(x)=x+q. A positive
base purchase therefore requires h(x)<t, while the opposing Q menu can
consume the item only for x>=h^{-1}(t). Equality forces empty on the base
side. All support and image-knot faces obey the same non-strict identities.

Eplus/Q remains valid because a Q own report still cannot buy the Eplus
bundle, lottery, or scarce singleton. A positive Eplus safe purchase has
coordinate y>.5. The opposing Q scarce threshold h^{-1}(y) is larger
than c because h(c)=.5, while its buyer's low value is below c. Eplus/Eplus
is unchanged from the independently audited clean mechanism.

For base/base and Eplus/base, a common safe/bundle surcharge requires a
specific contraction lemma; nonnegative prices alone do not prove it.
On the changed base region, the exact aligned prices are

\[
P=t+r-c,\qquad B=r+q,\qquad C=t+r,
\quad C-B=t-q<P.
\]

An old safe maximizer at own report (x,y) must have x<=C-B<P, by comparison
with the bundle. Thus its scarce singleton has negative utility, and
cannot become a new positive choice after the common surcharge. The old
safe can remain or give way to empty; the bundle-minus-safe comparison is
unchanged. An old scarce or empty maximizer stays a maximizer. A previous
bundle contains any new allocation. Therefore every original maximizer
admits a new maximizing subset, including positive ties. Applying this to
a shared feasible base pair, or to the clean Eplus/base feasible pair,
proves nonempty jointly feasible argmax sets. Section 2 of the primary
proof was clarified to include this discounted-tariff argument.

Selecting the first feasible pair of complete menu maximizers is a finite
Borel operation. Each bidder's attained utility is exactly its conditional
menu maximum regardless of that joint tie selection, so every own
misreport remains weakly worse. Empty gives IR in expected utility at
every profile. The same marginal construction yields samplewise feasible
item assignments. No unassigned boundary or tie remains.

## 2. The specific maximum floor is slack

For rho outside the support, t-k>=q gives t+rho>=k+h(rho). For rho inside
[L,U], Q implies k<=b-rho-q. The decreasing function
`B0(k)=5/6+3k^2/4-k` then satisfies

\[
B_0(k)-\rho-q\ge B_0(b-U-q)-U-q=14/1875>1/1000.
\]

The last expression follows by differentiating the intermediate bound:
its derivative in rho is `-3(b-rho-q)/2<0`. Hence B0(k)>h(rho), uniformly
for every allowed epsilon. The actual candidate consequently has
`C=max(C0(k),sum(opponent))`. In particular, no omitted extra-floor cell
is needed in the full conditional certificate or revenue integral.

## 3. Full conditional certificates: the transformed Q top trace

Fix a constrained Q opponent w=(t,rho), set k=h^{-1}(t), and let the
candidate prices be `(A,C-k,C)` with C=max(C0(k),sum(w)). The general
V4.6 screening certificate uses this k in its **menu and occupied top
trace**, rather than requiring k=t-q as a structural assumption.

At the actual own-report trace v=(x,1), with x<k, the opposing bidder's
base high price is exactly

\[
P_1(v)=\max\{1/2,h(x)\}<t.
\]

The modified safe/bundle surcharge produces precisely the h(x) term.
The opposing bidder of own type w therefore strictly occupies item 1.
It cannot buy another item because its low coordinate is below .5 and
its total is at most b. This proves the transformed top capacity hole
`r1(x,1)=0` for every x<k, including all tent knots.

If C=C0(k), the zero-total-mass certificate applies. If C=sum(w)>C0(k),
the bottom and vertical anchors remain occupied. The opposing menus
indexed by `(x,0)`, x<.5, and `(1/2,y)`, y<C-.5, are Q_free menus, which
the functional change leaves exactly unchanged. They sell the bundle to
w strictly: C>b0, its high coordinate is below A in every reopened row,
and their bundle price is below C. Thus the anchor conditions hold for
the actual new residual.

The parameter signs are also preserved. Since h(c)=.5 and h is increasing,
`c<k<=A-q<.5`. Also `C0(k)-k` remains strictly between .5 and A. If the
sum floor binds, `C-k<=b-k<A`. The top coefficient has the required sign,
and `m=2(C-C0(k))>=0`. Therefore the nonnegative capacity measure and the
exact global slack identity from the diagonal-hole proof extend.
They bound every measurable randomized pointwise DSIC/IR competitor,
including arbitrary lotteries and utilities not represented by finite menus.

On Q_free rows, the existing symmetric diagonal-hole certificate still
applies. Its priced bottom/vertical anchors are Q_free rows and unchanged;
all fees and altered constrained Q menus retain singleton prices above
.5, so low-square own types can still choose only empty or bundle.
Consequently both bidders remain fully conditionally optimal throughout Q.

## 4. Eplus top and junction traces remain occupied

The Eplus menu is unchanged, with its own old parameter kE=t-q. Its
junction trace `(x,c)`, A<x<t, is outside Q and Eplus and outside the tent
support because c<L. It has exactly the old base high price x<t.

At its top trace `(x,1)`, x<kE, a changed price can occur only for x in
[L,U]. There it satisfies

\[
h(x)\le h(U)=U+q<A<t.
\]

Outside [L,U] the old price `max(.5,x+q)<t` remains. Thus the top trace is
occupied throughout x<kE and the old H1/H2 hypotheses still hold pointwise.
The candidate is feasible by Section 1, so every volume and line capacity
saturation used in the Eplus upper certificate persists. Both bidders
therefore remain full randomized conditional optimizers on all Eplus.

## 5. Scope and interpretation

The conditional gap map after this functional change has value zero for
both bidders on Q and Eplus, with their complete actual residual capacity.
The profitable functional change is nevertheless possible because the
residual itself changes coherently across the two bidders. Conditional
optimality does not imply outer optimality. Base fibers outside those
regions remain unclassified by this audit; neither a fixed finite menu
nor this one-dimensional tent family is asserted to contain the final
auction optimizer.

The exact replay reconstructs h by affine knot interpolation, reconstructs
all changed menus independently, checks boundary profiles and actual
occupied traces, and compares the resulting choices with the published
candidate evaluator. It is additional implementation evidence. The
all-real inequalities and inherited global conditional slack identities
above are the proof, rather than finite report tests.
