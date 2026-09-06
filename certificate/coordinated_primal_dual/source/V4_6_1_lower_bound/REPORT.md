# V4.6.1 lower-bound branch

This branch gives a complete feasible mechanism with exact revenue

\[
\boxed{
R_{4.6.1}=
\frac{309078860435260513361}{367416000000000000000}
+\frac{31}{1215}\sqrt2
-\frac{170368}{664453125}\sqrt{11}.
}
\]

In particular,

\[
0.8764556138363258521461526
<R_{4.6.1}<
0.8764556138363258521461527.
\]

The increase over the strongest certified V4.6 mechanism lies strictly between
`0.0006357596879033968000721` and `0.0006357596879033968000762`.
Thus **OPT is at least this new exact revenue**. This branch does not give
a matching global upper bound or determine the unrestricted optimum.

The main gain comes from replacing the inherited asymmetric construction
with a rebuilt symmetric system of conditional menus, while changing its
global reserve and bundle increment. The mechanism definition drops the
old fee tables, joined square-root menus, F/G wrappers, and corner patches.
A separate monotone exchange deformation then gives a smaller strict gain.
Both constructions are preserved and evaluated independently.

The auction model is the original one: two additive bidders, two items,
four independent uniform coordinates on [0,1], pointwise DSIC and IR in
expected utility, and pointwise joint capacity. Finite menus below specify
particular admissible mechanisms; no finite-menu restriction is imposed
on OPT or on the conditional screening upper certificates.

## 1. What the conditional-gap search found

The [conditional revenue-gap map](research_log/conditional_gap_map.md)
distinguishes exact unrestricted inner gaps, coordinated outer changes,
and unresolved regions. Four experiments have different scopes:

| Construction | Certified gain over its stated starting mechanism | Meaning |
|---|---:|---|
| Whole low-square menu replacements in V4.6 | approximately 0.0000049458980 | Exact inner gap against the actual fixed residual on specified fibers |
| Symmetrize V4.6, then re-screen one bidder | approximately 0.0000018408748 | Strict gain with the mixture's other allocation held pointwise fixed |
| Mirror the full Q menus to both bidders | approximately 0.0000252283326 over strongest V4.6 | Coordinated complete menu replacement with compatible joint ties |
| Rebuild Q, E, and the global base constants | approximately 0.0006354441232 over V4.6 | The main new mechanism; ownership changes globally |

These are alternative mechanisms, **not additive increments** to stack.
The functional refinement in Section 4 is an increment to the last row.

On the positive low-square fibers, the exact conditional gap is

\[
\Gamma(P,z)=3(A-P)^2(z-A)+2(A-P)^3,
\]

where A=2/3, z is the opponent's sum, and P is the old singleton price.
A feasible replacement `(A,A,z)` and a matching capacity-support certificate
establish the unrestricted randomized screening value there. This is more
than a comparison with another deterministic menu. A concrete capacity
obstruction prevents extending that scalar price change beyond its proved
region; it is recorded in the gap map.

The symmetrization experiment produced residual capacities zero, one half,
and one. Complete one-bidder re-screening gives a strict gain. The optimal
replacement on those fibers avoids the fractional intermediate set, so
this experiment does not establish a need for essential randomization.
Its exact formulas and fixed-residual proof are in
[sym_rescreen.md](research_log/sym_rescreen.md).

## 2. The rebuilt mechanism, before the functional refinement

Use exact constants

\[
A=a=\frac23,\quad c=\frac{47}{150},\quad
b=A+c=\frac{49}{50},\quad s=\frac76,\quad
d=\frac12,\quad q=s-b=\frac{14}{75},
\]

\[
b_0=\frac{4-\sqrt2}{3},\qquad
T=\frac{178}{225},\qquad U=\frac{26}{25}.
\]

Both bidders use the same following map from the opponent report w to a
complete menu. Put t=max(w), rho=min(w), and z=w1+w2. Where the high
coordinate is unique, call its physical item **scarce** and the other
physical item **safe**. These names specify orientation only.

**Closed region Q: t<=A and z<=b.** If t<=d, offer both singletons at A
and the bundle at C=max(b0,z). If t>d, set

\[
k=t-q,\qquad C_0(k)=\frac56+\frac34k^2,
\qquad C=\max\{C_0(k),z\},\qquad B=C-k.
\]

Offer safe at B, scarce at A, and the bundle at C. The high coordinate is
unique in this branch since z<=b<1 and t>1/2.

**Open region E: A<t<T and rho<c.** Put

\[
\delta=\frac9{16}(T-t)(U-t),\qquad
\alpha=3t-2,\qquad \beta=\frac{\alpha}{\alpha+2\delta}.
\]

Offer safe at d+delta, scarce at t, bundle at t+c+delta, and a lottery
allocating scarce with probability one and safe with probability beta,
at expected payment t+beta*c. Here 0<beta<1.

**Every remaining report: base menu.** Set

\[
H(w)=\max\{0,w_1-a,w_2-a,w_1+w_2-b\}.
\]

The physical singleton prices and bundle price are

\[
P_1=H+\min(a,s-w_2),\qquad
P_2=H+\min(a,s-w_1),\qquad C=H+b.
\]

Every menu also contains empty allocation at zero payment. All E faces
excluded by its strict inequalities use Q or the remaining base rule.
All maxima include equality. No reports are left undefined.

The complete joint selection rule, also used after refinement, is in
Section 3. The rational-report evaluator is
[parameter_candidate.py](verifier/parameter_candidate.py). The displayed
formulas define the same mechanism on every real report.

## 3. Pointwise implementation and proof

For each bidder, form its full finite set of utility-maximizing menu
options. If its maximum utility is zero, retain empty alone. Choose the
lexicographically first **jointly feasible pair** in these two sets.
Order the bidders 1 then 2. In a free Q or base menu, order options empty,
physical item 1, physical item 2, bundle; in constrained Q use empty, safe,
scarce, bundle; in E use empty, safe, scarce, bundle, lottery. Charge each
selected option's price.

The existence of such a pair at every real profile is proved by six
region-pair arguments in
[parameter_rebuilt_family.md](research_log/parameter_rebuilt_family.md).
The central inequalities are:

- In Q/base, a positive base purchase of the contested item requires
  x<k, while the opposing Q allocation of that item requires x>=k.
- In Q/Q, prices at least the opponent's sum exclude two positive bundle
  purchases. Oppositely oriented safe/bundle conflicts would require
  both y>rho+q and rho>=y-q. Free Q cases and same orientations are
  covered separately.
- In E/base, any E option allocating the contested item forces the
  opposing base price to be at least its value t. For the lottery this
  follows on the entire winning interval c<=y<=Y<=1/2, not only on an
  axis or a sampled boundary.
- In E/Q, a positive E safe purchase requires y>1/2, while the E low
  value is below c<y-q, excluding the conflicting Q upgrade.
- In E/E, opposite orientations cannot buy conflicting lotteries or
  bundles. A winning lottery needs scarce value at least 1-t/2>1/2>c.
- Base/base menus admit a common maximizing feasible allocation among
  all nine deterministic outcomes, with costs 0,a,a,b,a,a,b,s,s.

At contested equalities the opposing utility is at most zero, and the
empty-at-zero rule applies. The proofs also handle positive-utility
indifference sets. This all-real argument supplies feasibility; the
finite profile replays are additional implementation checks.

For fixed opponent report, every selected outcome maximizes the bidder's
utility over the same complete menu. Every misreport selects some option
in that menu. This proves DSIC for **every** true type, misreport, and
opponent report, even when the joint tie selection changes. Empty proves
pointwise IR. The formulas and finite first-feasible selection are Borel.
Payments are nonnegative and, at truthful reports, at most two per bidder,
so revenue is integrable.

To realize the marginals, draw a fresh uniform number for each item,
assign bidder 1 an interval of length x1j and bidder 2 the following
interval of length x2j, and leave the remainder unassigned. The proved
inequality x1j+x2j<=1 gives samplewise allocation feasibility. The formal
truthfulness and IR statements concern expected utility, as in the task;
universal truthfulness is not asserted.

## 4. A profitable functional exchange

Let L=8/25, M=33/100, and N=17/50. Define the continuous tent

\[
\phi(x)=
\begin{cases}
100(x-L),&L\le x\le M,\\
100(N-x),&M\le x\le N,\\
0,&\text{otherwise}.
\end{cases}
\]

Set epsilon=1/1000 and h(x)=x+q+epsilon*phi(x). The slopes are 1 outside
the support and 11/10, 9/10 inside. Its inverse is explicit:

\[
h^{-1}(t)=
\begin{cases}
t-q,&t\notin(L+q,N+q),\\
(t-q+100\varepsilon L)/(1+100\varepsilon),
 &L+q<t\le M+q+\varepsilon,\\
(t-q-100\varepsilon N)/(1-100\varepsilon),
 &M+q+\varepsilon<t<N+q.
\end{cases}
\]

In constrained Q replace k by h^{-1}(t) and use

\[
C=\max\{C_0(k),z,k+h(\rho)\},\qquad B=C-k.
\]

In every base row with rho in the tent support, add epsilon*phi(rho) to
the safe singleton and bundle prices together. Free Q and E stay as
defined above. Use precisely the joint selection rule in Section 3.
This is the final selected mechanism, implemented in
[functional_exchange.py](verifier/functional_exchange.py).

These changes coordinate both bidders' menus. The Q/base conflict becomes
x>=h^{-1}(t) versus h(x)<t. The Q/Q conflict becomes y>h(rho) versus
rho>=h^{-1}(y). The E/Q argument uses h(c)=1/2. For changed base/base
and E/base pairs, compatible maximizing subsets exist: the old discounted
bundle inequality prevents an old safe winner from switching to a
positive scarce singleton after the common surcharge. Thus that subset
argument is valid for these menus, without asserting it for arbitrary
price changes. The full proof is in
[functional_exchange.md](research_log/functional_exchange.md), with a
separate [pointwise and residual audit](research_log/functional_gap_audit.md).

The extra capacity condition creates no hidden revenue region here. For
rho in [L,N],

\[
C_0(k)-k-\rho-q
\ge C_0(b-N-q)-(b-N-q)-N-q
=\frac{14}{1875}>\varepsilon.
\]

For rho outside the support, z>=k+h(rho). Consequently C=max(C0(k),z)
everywhere, and the Q menus change only for t in [L+q,N+q]. This slack
inequality and all inverse-knot conventions hold on the full continuum.

For every 0<=epsilon<=1/1000 the **whole-mechanism** revenue change is

\[
\Delta R(\varepsilon)
=\frac{70410824789}{216000000000000}\varepsilon
-\frac{31233979}{3000000000}\varepsilon^2.
\]

It is increasing on this proved interval. At the selected endpoint,

\[
\Delta R=\frac{68161978301}{216000000000000000}>0.
\]

For comparison, the neighboring positive tent on [.34,.36,.38] has
right-derivative upper bound -1392246823/1687500000000<0. That rejects
this one direction, not the functional search. The positive lower tent
also proves the simpler three-region candidate is strictly suboptimal.
Neither calculation asserts stationarity over all h.

## 5. Exact revenue verification

The simpler rebuilt mechanism has exact revenue

\[
R_{\rm clean}=
\frac{482935538268336599}{574087500000000000}
+\frac{31}{1215}\sqrt2
-\frac{170368}{664453125}\sqrt{11}.
\]

Its base contribution is 330901662677/379687500000. The exact calculation
partitions the ordered opponent triangle into nine positive-area rational
polygons, integrating the appropriate menu revenue polynomial on each.
It treats singleton prices above one separately. Full-Q replacements
then give polynomial integrals with rational or quadratic endpoints; E
contributes the exact integrated menu gain delta(t)^2.

Two implementations agree on every final radical coefficient:
[parameter_revenue.py](verifier/parameter_revenue.py) uses Green boundary
integrals; [independent_family_revenue.py](verifier/independent_family_revenue.py)
reconstructs menu polynomials and uses triangle simplex moments without
importing any other project calculator.

The functional increment integrates both bidders' forced changes. In Q,
the full conditional integral is

\[
(b-t)I(k)-\frac13[b-C_0(k)]^3,\qquad
I(k)=\frac{59}{108}+\frac{k^2}{4}-k^3+\frac{9k^4}{16}.
\]

Substitution t=h(k), including its Jacobian, gives the quadratic change.
The base increment is integrated over rho in [L,N], t in [b-rho,1],
splitting at t=1+c-rho where one singleton becomes unaffordable.
[independent_functional.py](verifier/independent_functional.py) reconstructs
the base price-shift polynomial and directly expands the Q Jacobian.
All four linear/quadratic component coefficients match the primary
calculation exactly. Adding the rational increment to R_clean gives the
boxed final expression. No numerical quadrature enters either certificate.

## 6. What remains open

For both bidders, the rebuilt and final functional mechanisms attain the
**unrestricted randomized conditional screening optimum against their
own actual residual capacities** throughout Q and E. The union has exact
opponent-report area

\[
|Q\cup E|=\frac{62101}{135000}\approx0.4600074074.
\]

This is an area of two-dimensional opponent reports, not a proportion
of the four-dimensional allocation space or an estimate of the global
optimality gap. The inherited continuum screening certificates have
their new scalar hypotheses and occupied capacity traces checked in
the independent audits. There are no inherited corner exclusions in
these new regions. On the functional Q traces the relevant price is
h(x); the E support traces remain occupied.

The remaining base region is unresolved. It may permit whole-menu
replacement. Improvements involving already certified Q or E fibers
must change the residual allocation or its coupled equality conditions.
The profitable h deformation is an explicit example of such a coordinated
change. No optimality of c, of the lottery parameters, of a finite menu
class, or of the unrestricted mechanism has been established.

All artifacts, including alternative experiments, exact certificates,
independent audits, and the branch-only manifest, are contained in this
directory. See [VERIFICATION.md](VERIFICATION.md) for replay commands,
results, and the distinction between all-real proofs and bounded checks.
