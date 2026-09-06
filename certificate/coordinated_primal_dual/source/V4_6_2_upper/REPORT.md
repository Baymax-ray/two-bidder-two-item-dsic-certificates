# V4.6.2 — a stronger global upper certificate

This branch proves, for the original two-bidder, two-item auction with independent uniform coordinates on \([0,1]\),

\[
\boxed{\mathrm{OPT}\le 0.882923053259.}
\]

The bound covers the unrestricted class of jointly measurable, pointwise DSIC, ex-post IR randomized mechanisms, with pointwise item feasibility. The parallel [V4.6.1 lower branch](../V4_6_1_lower_bound/REPORT.md), which appeared during this run, gives revenue in
\([0.8764556138363258521461526,\,0.8764556138363258521461527]\).
The current combined gap is approximately **0.0064674394223911**. The upper certificate is independent of this lower construction; its frozen ledger also retains the earlier V4.6 comparison. An optimal mechanism and a matching certificate have **not** been obtained.

The new contribution is a common capacity measure that combines reusable conditional-screening inequalities with a continuous incentive-flow certificate. Both unrestricted charged screening values are solved exactly at this measure. A separate sparse long-range flow deformation gives a further strict decrease. The [exact ledger](certificate/upper_ledger.json) contains sixteen strictly decreasing rational upper bounds.

| Certified stage | Upper bound, rounded upward |
|---|---:|
| Inherited global upper | 0.885758302518655 |
| Sharper continuous integration, depth 20 | 0.884368577299725 |
| Add the reusable conditional-support replacement | 0.882923061358717 |
| Add four sparse long-range IC cycles | **0.882923053258717** |

All three operations use the same frozen rational stream coefficients, with amplitude one. Their compatibility is proved, rather than assumed from separate numerical improvements. The improvement over the inherited upper lies in
\([0.0028352492599376156240,\,0.0028352492599376156241]\).

## Exact endpoint

Write \(\Delta_{1024}\) for the exact rational number in the final `delta` entry of [conditional_global_splice.json](certificate/conditional_global_splice.json). Its value is approximately \(0.001445515941007789\). The new certified endpoint is the explicitly specified rational

\[
U_{4.6.2}
=\frac{231831916327659047}{262144000000000000}
-\Delta_{1024}-\frac{81}{10000000000}.
\]

Its full numerator and denominator are in the ledger. Exact directed decimal conversion gives

\[
0.8829230532587169692606
<U_{4.6.2}<
0.8829230532587169692607.
\]

Thus the shorter rational \(882923053259/10^{12}\) is also an unrestricted upper bound. The frozen ledger compares against the original V4.6 revenue and gives gap
\([0.0071031991102945139145,\,0.0071031991102945139146]\).

The stronger parallel lower branch has the exact revenue
\[
R_{4.6.1}=\frac{309078860435260513361}{367416000000000000000}
+\frac{31}{1215}\sqrt2-\frac{170368}{664453125}\sqrt{11}.
\]
The [separate cross-branch arithmetic certificate](certificate/current_bound_comparison.json) uses integer-square-root enclosures to prove
\[
0.0064674394223911171144741
<U_{4.6.2}-R_{4.6.1}<
0.0064674394223911171144742.
\]
This update changes the comparison, not the upper measure or any of its sixteen endpoints.

## Turning a conditional support into a whole-auction inequality

Suppose a measurable conditional capacity-price kernel gives, for every complete conditional mechanism of bidder 2,

\[
R_2\le C+\langle P,a_2\rangle.
\]

It can be used at every residual capacity. Joint feasibility and the definition of the opposing unrestricted charged screening problem imply

\[
\mathrm{OPT}\le C+\langle P,1\rangle+H_1(P),\qquad
H_1(P)=\sup_{M_1\ {\rm DSIC/IR}}(R_1-\langle P,a_1\rangle).
\]

This uses complete jointly measurable mechanisms directly; no interchange of an uncountable supremum and an integral is required. The [conditional-support proof](research_log/conditional_global_splice.md) also gives the version with a signed or singular incentive measure, using a common dominating measure and the actual allocation selections on singular sets.

For the numerical improvement, specialize the existing full-capacity screening certificate to the single-buyer menu with prices

\[
(0,A,A,b_0),\qquad A=2/3,\quad b_0=(4-\sqrt2)/3.
\]

Its utility is \(u^*=\max(0,x-A,y-A,x+y-b_0)\). The menu has fixed empty-first tie priority. A nonnegative bounded capacity density \(\Psi\), specified explicitly in the conditional-support proof, satisfies the universal identity

\[
\langle\Psi,a\rangle-R=3\int_{D_0}u\ge0
\]

for every randomized DSIC/IR conditional mechanism. Here \(D_0\) is this menu's no-sale region. Its total mass is \(R_0=4/9+2\sqrt2/27\), and \(\Psi\) vanishes on \(W=[0,43/100]^2\).

An exact sign certificate proves that both inherited virtual values of a bidder are nonpositive whenever that bidder reports in \(W\), for **every** opposing report. This is what makes the support compatible with the other bidder. The sign statement is a continuous polynomial inequality on two complete radial charts, checked by rational Bernstein subdivision.

Let \(\phi'_i\) be the original stream field after the four cycles described below. Those cycles avoid every profile at which either bidder belongs to \(W\). Define one common capacity price for both bidders:

\[
\Pi'_j(w,v)=
\begin{cases}
0,&w,v\in W,\\
\Psi_j(v),&w\in W,\ v\notin W,\\
\Psi_j(w),&v\in W,\ w\notin W,\\
\max(0,\phi'_{1j},\phi'_{2j}),&w,v\notin W.
\end{cases}
\]

When the opponent belongs to \(W\), use the universal screening identity. Outside that opponent region, use the stream identity, the sign theorem, and the actual added IC inequalities. This proves

\[
R_i-\langle\Pi',a_i\rangle\le0\quad\text{for every }M_i.
\]

The empty mechanism attains zero, so **\(H_1(\Pi')=H_2(\Pi')=0\)** exactly. Consequently \(\mathrm{OPT}\le\int\sum_j\Pi'_j\). Empty leaves priced capacity unused; solving the charged problems at zero does not establish equality for the auction.

The [combined certificate](research_log/combined_certificate.md) specifies the measure and the complete proof. Values on volume-null chart boundaries can be defined measurably; the proof uses convex utilities and their almost-everywhere gradients and retains the actual zero-type IR trace. It places no finite-range assumption on the competing mechanisms.

## What made the bound decrease

The inherited stream gives an exact revenue identity with a single IR source at the zero type. Its curl correction has zero divergence and zero normal boundary flux. There is **no positive interior sink density** that would forbid positive information rents.

First, the [continuous majorant](flow_proof.md) integrates the lifted continuous virtual maximum more tightly. For competitors expressed in the same Bernstein basis,

\[
\max\left(0,\sum_k B_k a_k,\sum_k B_k b_k\right)
\le\sum_k B_k\max(0,a_k,b_k).
\]

Integrating the right side preserves within-cell variation. Directed integer arithmetic accounts for every rounding and subdivision error. Four radial charts and item symmetry cover the full report space. The primary and independent implementations agree through all **1,351,220 tree nodes**, including all five recorded depth bounds and chart coverages.

Second, replace the stream prices by \(\Psi\) on the two opponent-low regions. Their overlap has zero old and new price, so the two improvements add without double subtraction. The reduction equals an integrated nonnegative virtual-allocation slack against the single-buyer menu. Opponent variables are integrated out exactly. On each radial rectangle lying wholly in one menu region, the positive-part inequality

\[
\int_B(f)_+\ge\left(\int_B f\right)_+
\]

gives a rational lower bound on the reduction. Boundary-crossing rectangles are omitted. Refinement yields the seven increasing reductions \(\Delta_{16},\ldots,\Delta_{1024}\). These rectangles partition an **integral certificate**, not a finite type domain or a grid mechanism.

An initial bundle-region classifier was found to be too permissive: exceeding the bundle price in total value is insufficient when the lower coordinate still prefers a singleton. It was corrected to require both minimum total value and minimum lower coordinate to pass their thresholds. The older subtraction was discarded. The saved endpoint uses only the corrected computation. An independent audit reconstructs every coefficient of the averaged fields, checks 20,968 exact menu-corner comparisons, and includes the offending crossing-cell regression.

Third, [two-way long-range IC flows](research_log/sparse_cycle.md) join own-report boxes centered at \((2/5,39/40)\) and \((7/20,23/40)\), for an opposing box centered at \((3/5,1/5)\). Each coordinate halfwidth is \(3/200\), and flow density is \(1/20\). Equal forward and reverse flow preserves mass balance and adds no sink. The virtual correction is opposite on the two boxes. Exact whole-box polynomial bounds prove the old and new winners stay strict, making the change in the continuous maximum exactly computable.

Bidder exchange and simultaneous item exchange give four disjoint images. All eight profile boxes are disjoint from the conditional replacement regions. Their exact combined reduction is \(81/10^{10}\). The small size of this gain does not affect its role: it is a verified continuous long-range IC improvement outside the original smooth stream architecture. A separate implementation checks the whole-box inequalities, symmetry, disjointness, and gain.

## Every gap term is explicit

For \(O_i=\{v_{-i}\in W\}\), write

\[
\begin{aligned}
S_{\rm screen}&=\sum_i3\int_{O_i}\int_{D_0}u_i,\\
S_{\rm capacity}&=\sum_j\int\Pi'_j(1-a_{1j}-a_{2j}),\\
S_{\rm virtual}&=\sum_{i,j}\int_{O_i^c}(\Pi'_j-\phi'_{ij})a_{ij},\\
S_{\rm IC}&=\sum_i\int_{O_i^c}u_i(0;v_{-i})
+\sum_{\rm added\ edges}\int \text{weighted truthful IC residual}.
\end{aligned}
\]

All four are nonnegative, and their sum is exactly \(\int\Pi'-R\). The conditional certificate's internal utility terms are included once in screening slack, rather than counted again as IC slack. The last term includes the origin IR trace explicitly.

The reported rational upper also contains a numerical certification remainder. If \(B\) is the exact original continuous maximum integral and \(D\) the exact conditional replacement reduction, then

\[
E=(B_{20}-B)+(D-\Delta_{1024})\ge0,\qquad
U_{4.6.2}-R=S_{\rm screen}+S_{\rm capacity}+S_{\rm virtual}+S_{\rm IC}+E.
\]

The first remainder is the Bernstein and rounding majorization; the second is omitted boundary-cell slack and the positive-part averaging remainder. These are distinguished from failures of mechanism equality. For a four-category accounting of the reported bound, use \(S_{\rm virtual}^{\rm certified}=S_{\rm virtual}+E\). This supplies an exact decomposition, but the separate integrals of the V4.6 mechanism have not all been numerically evaluated.

## Alternative supports and a diagnosed equality obstruction

The branch also constructs a different universal support for the same conditional lottery optimum. It moves part of a singular line charge into a volume density, preserving a nonnegative global residual-screening inequality and the reference equality conditions. The [redistribution proof](research_log/conditional_lottery_redistribution.md) and [exact replay](certificate/conditional_lottery_redistribution.json) show that a convenient local support need not be unique.

This alternative reduces, but does not remove, its demonstrated opposing-bidder charge on a null set of opponent reports. A complete bidder menu can be replaced on such a null opponent set without revenue loss or loss of its own DSIC/IR. Therefore positive consumed charge there creates charged-screening regret. Patching the other bidder's menu merely moves that loss to unused priced capacity. This obstructs the tested family; it does not exclude all singular common measures. This alternative is diagnostic and contributes no subtraction to the numerical endpoint above.

The V4.6 mechanism has an untouched open region with bidder 1 empty and bidder 2 allocated \((1,\beta)\), where \(4/5<\beta<19/20\) and utility is positive. Equality requires the safe item's common price and the winning virtual value both to vanish there, with zero interior sink. A [separate exact test](certificate/remaining_lottery_slack.json) proves that the final field is bounded away from zero on a rational subbox. Thus this final dual has strictly positive capacity-plus-virtual slack against V4.6.

The updated [V4.6.1 flatness certificate](research_log/current_lower_flatness.md) proves the same failure for the stronger selected lower mechanism. On a nearby rational box centered at `(151/200,3/40,9/10,63/200)`, all functional threshold changes and upper-cycle changes are absent. Bidder 1 uniquely chooses empty, and bidder 2 uniquely chooses `(1,beta)` with `9/10 < beta < 49/50`. The safe virtual field is strictly negative throughout the box. A whole-box exact calculation gives a positive rational capacity-plus-virtual slack. This identifies a specific allocated region whose current incentive field must change before equality is possible; it is not a proof of a globally admissible primal improvement.

There is also a structural reason: on each open radial chart, a finite polynomial curl produces an analytic field whose radial pole cannot vanish identically. Such a field cannot have the required open zero plateau. Constant-density translated-cell flows likewise cannot create the needed plateau inside an untouched cell. Approximate ties on grid boundaries would not meet this condition.

The useful message to the primal branch is therefore precise: either construct a complete admissible reallocation that changes this partial-allocation region, or build a locally different, nonanalytic support/flow system that is exactly flat there. Failure of this certificate is **not** evidence that such a primal improvement exists, and is not a proof that V4.6 is suboptimal.

Two other trials were bounded and rejected. Extending the sign square to side \(1/2\) is false: an exact profile gives a positive virtual value exceeding \(1/40\). A scalar stream amplitude selected by a coarse continuous majorant worsened the finer certified endpoint; it was not substituted into the combined bound. Neither experiment is presented as optimization of the unrestricted dual class.

The current result is a rigorously decreasing sequence of unrestricted upper bounds and an explicit common capacity/incentive system. It provides no proof that this fixed sequence converges to the optimum, no equality mechanism, and no uniqueness or attainment result. [VERIFICATION.md](VERIFICATION.md) records the actual replays, dependencies, and preservation boundary.
