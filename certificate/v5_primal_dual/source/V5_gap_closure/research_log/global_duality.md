# V5: a global conditional-support substitution with a material certified gain

The frozen mechanism is unchanged. A different global support system gives a
certified common-capacity-envelope decrease

\[
 G\ge G_{\rm cert}=0.0004502783756947465\ldots>0.
\]

The exact rational number is `global_gain_lower` in
`certificate/global_duality.json`. This decrease compares against the inherited
radial-plus-stream field **with its existing low-square conditional splice**.
Disjoint inherited corrections can be retained. Overlapping QQ first-event
corrections must be removed from the subtraction ledger before this gain is
added; giving back the entire inherited first-event lower subtraction is safe.
An overlapping new QQ curl is an alternative, not an additional deduction.
The main report assembles the resulting unrestricted auction upper bound.

This is a universal support substitution, not a deformation of the incumbent,
not a finite type-grid mechanism, and not a claimed solution of the auction.

## 1. Complete conditional revenue identities

Write the own type as \(v=(x,y)\) and the opposing report as \(w\). A complete
randomized pointwise DSIC mechanism has a convex utility \(u(v;w)\), its actual
selected allocation \(a(v;w)\in\partial_vu(v;w)\cap[0,1]^2\), and payment
\(v\cdot a-u\). Ex-post IR gives \(u(0;w)\ge0\). Set
\(\bar u(v;w)=u(v;w)-u(0;w)\); then \(0\le\bar u\le2\).

The inherited radial field plus the frozen zero-trace polynomial stream is

\[
 \phi_j(v;w)=v_j\left({3\over2}-{1\over2\max(v)^2}\right)
                 +\operatorname{CORR}_j(v,w).
\]

Its integrable singularity at the origin is harmless; choose any Borel value
there. For every such conditional mechanism the exact identity is

\[
 R(w)=\int\phi(v;w)\cdot a(v;w)\,dv-u(0;w).                 \tag{1}
\]

The curl contribution is zero by the inherited weak gradient/zero-boundary
stream identity, including nonsmooth convex utilities. No extra boundary flux
or singular measure is introduced in the present construction.

Set
\[
 A={2\over3},\quad B_0={4-\sqrt2\over3},\quad
 k=B_0-A={2-\sqrt2\over3},\quad Z={3\over4},
\]
and define \(\ell(x)=A\) for \(x<k\), \(\ell(x)=B_0-x\) for
\(k<x<A\). Define
\[
\begin{array}{c|ccc}
 &x<k&k<x<A&x>A\\ \hline
 f(x)&0&3(k-x)&1\\
 F(x)&0&\tfrac32(x-k)^2&1-x.
\end{array}
\]
With \(H(y)=4(y-Z)_+\), the inherited full-capacity support is
\[
 \Psi_1=3(x-A)_++4F(x)1_{y>Z},\qquad
 \Psi_2=3(y-\ell(x))_+1_{x<A}+f(x)H(y).                    \tag{2}
\]
Both components are nonnegative. For example, below \(A\) and above \(Z\),
the second component is
\((1-H)3(y-\ell)+H(3y-2)\), a sum of nonnegative terms.
Let \(D_0=\{x\le A,y\le A,x+y\le B_0\}\). The universal identity is
\[
 R(w)=\int\Psi(v)\cdot a(v;w)\,dv-3\int_{D_0}u(v;w)\,dv. \tag{3}
\]
It applies to all randomized pointwise DSIC/IR menus, including infinite
allocation ranges. Its proof is the inherited conditional screening identity,
not an assertion that every pointwise virtual maximizer is implementable.
Moreover
\[
 |D_0|=A^2-\tfrac12(2A-B_0)^2={1\over3},\qquad
 \int(\Psi_1+\Psi_2)=R_0={4\over9}+{2\sqrt2\over27}.       \tag{4}
\]
For the last equality, the SJA menu with prices \((A,A,B_0)\) has zero utility
on \(D_0\), saturates every positive support component, and has revenue
\(R_0\). Thus (3) also reads
\(R=\langle\Psi,a\rangle-3\int_{D_0}\bar u-u(0)\).
Item swapping gives an equally valid support \(\Psi^s\) and the same source.

Consequently any Borel choice \(\theta(w)\in[0,1]\) and Borel orientation
\(o(w)\) gives the complete conditional identity
\[
 R(w)=\int\big[(1-\theta(w))\phi(v;w)+\theta(w)\Psi^{o(w)}(v)\big]
               \cdot a(v;w)\,dv
       -(1-\theta(w))u(0;w)-3\theta(w)\int_{D_0}u(v;w)\,dv. \tag{5}
\]
Equivalently the final two terms are \(-u(0;w)-3\theta\int_{D_0}\bar u\).
The switching variable is the opponent's report: there is no own-type
derivative of \(\theta\), no omitted interface flux, and no free utility source.
The normalized pairings are bounded even for singular opponent measures.
Here all opponent integrations are Lebesgue. If \(\int u(0;w)=\infty\),
expected revenue is \(-\infty\) and the upper bound is immediate; otherwise
all displayed utility/source terms are integrable.

## 2. The enlarged support domain and common price

Retain the inherited square \(W=[0,43/100]^2\). Introduce
\[
 J=(43/100,1/2]\times[0,7/20],\quad J^s=\{(y,x):(x,y)\in J\},
 \qquad D^\sharp=W\cup J\cup J^s.                         \tag{6}
\]
The three pieces have disjoint interiors. Both added rectangles satisfy
\(\max(w)\le1/2\) and \(w_1+w_2\le17/20<B_0\); the latter strict
inequality follows from \((29/20)^2>2\). Also \(2(43/100)<B_0\).
Thus \(D^\sharp\subset D_0\), and **both** support orientations vanish there.

Use \(\theta=1_{D^\sharp}\), inherited orientation on \(W\), physical
orientation (2) on \(J\), and item-swapped orientation on \(J^s\). Denote the
resulting bidder fields by \(A_{ij}\). Define a single nonnegative common
capacity density on the full four-dimensional report cube:
\[
                 \Pi_j=\max(0,A_{1j},A_{2j}).              \tag{7}
\]
Every bidder's complete charged problem satisfies
\(R_i-\langle\Pi,a_i\rangle\le0\); the empty mechanism attains zero, so
\(H_i(\Pi)=0\). Joint pointwise capacity therefore proves
\[
                 \mathrm{OPT}\le\int\sum_j\Pi_j.          \tag{8}
\]
Opposing virtual values are charged in (7), not discarded by an unproved
dominance assertion. The support is Borel, integrable, and valid for all actual
pointwise allocations; measure-zero tie choices never change the primal.

For the frozen V4.6.1.1 mechanism, every opponent in \(D^\sharp\) induces
exactly the SJA menu: its `Q_free` branch has \(\max(w)\le1/2\) and bundle
price \(\max(B_0,w_1+w_2)=B_0\). Thus the new conditional-screening source
remains zero against the incumbent. This fact is useful for the slack ledger
but is not needed for the global validity of (8).

The exact gap decomposition for any feasible mechanism is
\[
\begin{split}
\int\Pi-\sum_iR_i={}&
 \sum_i3\int_{w\in D^\sharp}\int_{D_0}u_i(v;w)\,dv\,dw\\
&+\sum_i\int_{w\notin D^\sharp}u_i(0;w)\,dw\\
&+\sum_j\int\Pi_j(1-a_{1j}-a_{2j})
 +\sum_{i,j}\int(\Pi_j-A_{ij})a_{ij}.                    \tag{9}
\end{split}
\]
These are conditional screening, remaining IR source, capacity, and virtual
allocation slack, all nonnegative. Preserved disjoint IC-flow corrections add
their actual weighted IC slack. There is no requirement of positive sink at
positive-rent types. Numerical enclosure in the bound below is separate from
these mechanism slacks.

## 3. A pointwise overlap-safe decrement inequality

Let \(\Pi^W\) be the old common envelope with only the inherited \(W\) splice.
Fix one oriented added opponent \(w\in J\), and abbreviate per item
\(a=\phi_j(v;w)\), \(b=\phi_j(w;v)\), \(p=\Psi_j(v)\ge0\).
Outside \(W\cup J\cup J^s\), the old envelope is \(\max(0,a,b)\) and
the new envelope is \(\max(p,b)=p+(b-p)_+\). Therefore a valid directed
decrement lower bound is
\[
                      a_+-p-(b-p)_+.                     \tag{10}
\]
The remaining cases are essential:

* If \(v\in W\), both actual old and new common prices are zero. The inherited
  exact sign theorem gives \(a\le0\), while \(p=\Psi(v)=0\) and \(\Psi(w)=0\). Formula (10)
  is \(-b_+\le0\), so remains a conservative lower bound.
* If both reports lie in \(J\cup J^s\), both new supports are zero. The two
  directed lower bounds for that profile are \(a_+-b_+\) and \(b_+-a_+\),
  which sum to zero. The actual old common price is nonnegative. Hence their
  aggregate is safe; no assumption of disjoint bidder substitutions is made.
* If neither report is in an added rectangle, the change and the directed
  lower contributions are both zero.

Summing (10) over both bidders and the two simultaneous item images gives
\[
\int\sum_j(\Pi^W_j-\Pi_j)\ge
4\left[L-|J|R_0-E\right],                                \tag{11}
\]
where
\[
 L=\int_Jdw\int_{[0,1]^2}dv\sum_j(\phi_j(v;w))_+,
 \quad E=\int_Jdw\int_{[0,1]^2}dv\sum_j(\phi_j(w;v)-\Psi_j(v))_+.
\]
Here \(|J|=49/2000\). Item covariance of the archived curl is verified exactly
in the script, and orienting the support with the high opposing item makes
the two item contributions identical. The source and all interactions have
already been charged in (11); no extra unknown low-square correction is needed.

## 4. Continuous lower enclosure for L

Partition \(J\) into 7 by 7 exact rational rectangles. On each opponent box
\(B\), average every polynomial coefficient of the curl exactly. For the two
own-type charts \(v=(s,s\tau)\) and \(v=(s\tau,s)\), the Jacobian is \(s\).
Define \(P_j(s,\tau;w)=s\phi_j(v;w)\); it is a rational polynomial, since
the radial pole cancels. Convexity gives
\[
 \int_B(P_j)_+\,dw\ge|B|\left({1\over|B|}\int_BP_j\,dw\right)_+.
\]
Then partition each \((s,\tau)\) square into 128 by 128 dyadic integration
cells \(C\). On every complete cell,
\(\int_C(\bar P_j)_+\ge(\int_C\bar P_j)_+\).
Rational monomial integrals, enclosed outward as described below, give
\[
 L\ge {119448693432877\over8796093022208000}
       =0.01357974422636255\ldots.                          \tag{12}
\]
Cells crossing virtual-winner or virtual-zero curves are included through
the convex positive-part inequality; no sign interpolation is used.

## 5. Continuous upper enclosure for opposing excess E

Take \(K=195263/10^6>k\), certified by \(0<2-3K\) and
\((2-3K)^2<2\). A rational lower support for item 1 is
\[
 q(x,y)=\begin{cases}
 0,&x<A,y<Z,\ \text{or }x<K,y>Z,\\
 6(x-K)^2,&K<x<A,y>Z,\\
 3x-2,&x>A,y<Z,\\
 2-x,&x>A,y>Z.
 \end{cases}                                             \tag{13}
\]
The middle expression is below \(6(x-k)^2\); the high-band expression equals
\(3x-2+4(1-x)\). Use \(q_2=0\le\Psi_2\). As \(w=(t,r)\in J\) has
\(t>r\), clearing the positive denominator \(2t^2\) gives
\[
\begin{split}
 P_1&=3t^3-t+2t^2\operatorname{CORR}_1(t,r,x,y)-2t^2q(x,y),\\
 P_2&=3t^2r-r+2t^2\operatorname{CORR}_2(t,r,x,y).
\end{split}
\]
The five item-1 support pieces and one item-2 square, for all 49 opponent
boxes, form 294 rational root boxes covering the full integral.
On a box write \(P=\sum_\beta c_\beta B_\beta\) in tensor Bernstein basis.
Because the basis is nonnegative and partitions unity,
\[
 {P_+\over2t^2}\le
 {\sum_\beta(c_\beta)_+ B_\beta\over2t_{\min}^2}.
\]
Every basis element has integral box-volume divided by the number of controls.
The certificate stores a full binary tree of 12,000 midpoint subdivisions,
giving 12,294 terminal boxes. Default replay visits every root and every
recorded split, verifies that no disconnected recorded split is omitted,
and sums all leaf bounds. It certifies
\[
 E\le E_{\rm cert}=0.000011750019243246275\ldots.            \tag{14}
\]
No finite type-grid relaxation is involved. The split choice was numerical
discovery; every accepted whole-cell integral bound is independently replayed.

## 6. Arithmetic and reproducibility boundary

`verifier/global_duality.py` rejects optimized Python. Its exact inputs are
`Fraction` values from the frozen polynomial archive. Each conversion to
binary64 is bracketed by comparison of the exact floating rational with the
input. Each addition, multiplication, subtraction, and division used in an
enclosure is expanded with `nextafter` toward the appropriate infinity.
Basic IEEE-754 binary64 round-to-nearest arithmetic and correct `nextafter`
are explicit trusted numerical assumptions. No BLAS reduction supplies a bound.

The monomial-integral and Bernstein transformations propagate lower/upper
intervals operation by operation. Midpoint de Casteljau uses upper-rounded
convex combinations. Final nonnegative masses are rounded outward to dyadics
and summed in checked integer arithmetic; the denominator and box volumes
are exact rationals. Square root 2 is bracketed with integer square root at
denominator \(10^{50}\). All adaptive heuristics affect efficiency only.
The verifier records inherited stream, polynomial, conditional proof, and
conditional certificate hashes, checks item covariance and \(|D_0|=1/3\), and
recomputes the exact rational certificate on default read-only replay.

Run from the auction directory:

```
python -B -X utf8 V5_gap_closure/verifier/global_duality.py
```

The written revenue identities, the inherited W sign theorem, and the stated
IEEE arithmetic assumptions remain trusted dependencies; this is not a formal
proof-assistant kernel. The partition proves continuous integral bounds, not
optimality over a finite type set.

## 7. Retention ledger and remaining limitation

The old sparse long-range cycle has both profile types outside \(D^\sharp\),
as do the old BB master corridors. Those fields and weighted IC terms can
remain unchanged. The root's new BB translated-IC support is also disjoint:
its opponent maximum is at least .82, and the other type has sum at least .95,
whereas every added-splice type has maximum at most .5 and sum at most .86.
These pointwise disjointness facts permit additive envelope deductions.

The inherited QQ first-event endpoints do intersect the new splice. Their
decrement cannot be retained without joint reevaluation. Giving back the
**entire** inherited first-event lower decrement is a conservative explicit
ledger operation; it is much smaller than (11). The separately discovered
V5 QQ curl also overlaps and is not added here.

This gain escapes the earlier local complementary-stress moment restriction
by replacing complete conditional revenue identities, including their source
terms, on a positive-measure set of opposing reports. It supports broad Q/Q
and mixed profiles simultaneously. It does not provide equality with the
incumbent, establish that its geometry is optimal, or close the remaining gap.
