# Author check: the selected joint deformation and its entry fee

This is a bounded author-revision calculation, not an additional referee
report. It concerns the one selected mechanism with
\(e=9/10000\), \(c=137/500\), \(q=113/500\),
\(W=[7/10,71/100]\times[0,1/5]\), and
\(S=[1741/2500,71/100]\times[c-2e,c+4e]\).
Write \(J_2\) for the complete bidder-2 revenue change and \(J_1\)
for the complete bidder-1 entry-fee change, each integrated over all
affected own reports and opponent reports. Then \(J=J_2+J_1>0\).

## 1. Why the corner mass is not the lottery-price derivative

For a fixed opponent high report \(t\), put

\[
\alpha=3t-2,\quad
\delta=q+3q^2/4-3qt/2+\alpha^2/16,\quad
\ell=\delta+\alpha/2,\quad
\beta=\frac{\alpha}{\alpha+2\delta},\quad Y=c+\ell.
\]

Thus \(\beta\ell=\alpha/2\). The inner capacity certificate has corner
mass \(\lambda=\alpha(c+\ell/4)\). Its exact convex-trace slack is

\[
T_g=\lambda g(c)-\int\sigma_g g
=\alpha\int_0^c[g(c)-g(y)]\,dy
+\frac\beta2\int_0^\ell s(\ell-s)^2\,d\nu(c+s).
\]

Let \(g_h(y)=u_h(1,y)\) be the right trace when only the lottery price
is decreased by \(h\), for \(0\le h\le e\). This is a calculation for
one complete conditional menu; it does not claim that an arbitrary joint
mechanism indexed by \(h\) is feasible. The verified selected-parameter
geometry gives \(h/\beta<c\). On \([0,c]\), the old trace is constant,
and its increment is zero below \(c-h/\beta\) and
\(h-\beta(c-y)\) above that point. On the whole frozen interval
\((c,Y)\), both traces are affine and their difference is \(h\).
Consequently the hinge-measure term remains zero, and

\[
T_{g_h}-T_{g_0}=\alpha\left(ch-\frac{h^2}{2\beta}\right),
\qquad
\left.\frac{dT_{g_h}}{dh}\right|_{0+}=\alpha c.
\]

The raw term \(\lambda g_h(c)\) increases at rate \(\lambda\), while
the trace slack removes exactly \(\alpha c\) at first order. This
explains the difference \(\lambda-\alpha c=\alpha\ell/4\).
The complete revenue derivative can also be obtained without using the
certificate: the old lottery cell has area
\(A_L=(1-t)\ell+\beta\ell^2/2\), its right-edge trace has length
\(\ell\), and the top trace is unchanged. Therefore the uniform revenue
identity gives

\[
\left.\frac{d\Delta R_2(t;h)}{dh}\right|_{0+}
=\ell-3A_L=\frac{\alpha\ell}{4}.
\]

Integrating the entire new lottery cell and the displaced singleton and
bundle purchases gives the finite, exact change

\[
\Delta R_2(t;e)=
\frac{\alpha\ell e}{4}
-\frac{\alpha e^2}{4\beta(1-\beta)}
-\frac{e^3}{2\beta(1-\beta)^2}.
\tag{1}
\]

Equation (1), not the positive derivative alone, is used at the selected
\(e\). The old inner-optimality theorem is consistent with this gain:
the lottery cut needs capacity that the old residual did not supply,
and the other bidder's complete fee menu releases that capacity.

## 2. Entry-fee identity and the actual geometric hypotheses

For a reference conditional utility \(u\), adding \(h\) to every
nonempty option and preserving the free empty option gives
\(u_h=(u-h)_+\). Let \(D(h)=|\{u\le h\}|\). Suppose, on the actual
range \(0\le h\le e\), that

1. the no-sale polygon keeps its stated topology inside the unit square,
   so \(D(h)=D+Ch+h^2/2\);
2. the right and top traces stay positive everywhere.

Here \(C\) is the reference bundle price. From
\(R=\int u(1,y)dy+\int u(x,1)dx-3\int u\), the boundary derivative
is \(-2\) and the interior derivative is \(3[1-D(h)]\). Integrating
\(R'(h)=1-3D(h)\) proves

\[
\boxed{\Delta R_{\rm fee}
=(1-3D)e-\frac32Ce^2-\frac12e^3.}
\tag{2}
\]

There is no hypothesis \(C<1\). The following polygons explain why (2)
applies to both actual row types in \(S\).

**E-plus rows below \(y=c\).** Set \(t=x\),
\(B=1/2+\delta\), \(C=t+c+\delta\), \(j=1-t/2\),
and \(k=t-q\). The no-sale polygon after the common fee has vertices

\[
(0,0),\ (t+h,0),\ (t+h,c),\ (j+h,Y),\ (k,B+h),\ (0,B+h).
\]

Its area is

\[
D(h)=c(t+h)
+\int_c^Y[t+\beta(c-y)+h]dy
+\int_Y^{B+h}(C+h-y)dy.
\]

Differentiation gives \(D'(h)=B+k+h=C+h\), hence the required area
expansion. Sufficient hypotheses are
\(0<k<j<t\), \(0<c<Y<B\), \(t+e<1\), and \(B+e<1\).
They hold throughout \(t\in[1741/2500,71/100]\): in particular
\(2/3<t<613/750\), \(\delta>0\), and \(\delta\) decreases there;
the endpoint inequalities give the last two bounds. The scarce and safe
singletons respectively give the uniform trace lower bounds
\(1-t-h>0\) and \(1-B-h>0\). Direct area evaluation gives
\(D=(1+\lambda)/3\).

**Frozen deterministic rows above \(y=c\).** With \(z=y-c\), their
prices are \(A=x+z+f\), \(B=1/2+z+f\), and
\(C=x+c+z+f\), for the literal fees
\(f=7/2000,7/10000,0\) on the three recorded cells. Here
\(\max(A,B)<C<A+B\) and \(A+e,B+e<1\). The no-sale polygon is a
rectangle with a triangular corner removed, so

\[
D(h)=(A+h)(B+h)-\frac12(A+B-C+h)^2
=D+Ch+\frac12h^2.
\]

The singleton options again keep both traces positive. This triangle
formula describes these deterministic rows; it must not be substituted
for the E-plus polygon that also contains the lottery boundary.

**Actual row with \(C>1\).** At \(t=7/10\), the exact values are

\[
\delta=\frac{1727}{62500},\quad
C=\frac{31301}{31250}>1,\quad
B=\frac{32977}{62500},\quad
\lambda=\frac{9169}{312500},\quad
D=\frac{107223}{312500}.
\]

For the selected \(e\), equation (2) gives the exact conditional change

\[
\boxed{\Delta R_{\rm fee}(7/10)
=-\frac{1381203369}{50000000000000}
=-0.00002762406738.}
\]

Thus this row explicitly rules out the explanation that all relevant
bundle prices must be below one. It does not invalidate the fee formula.

## 3. The exact signed decomposition at the selected parameter

Integrating (2) over the lower strip gives

\[
J_{1,-}=-\frac{92624010033429}{125000000000000000000000}.
\]

The three upper-strip cells give, respectively,

\[
\frac{3161434941}{25000000000000000000},\qquad
\frac{15610239}{62500000000000000},\qquad
\frac{838578339}{5000000000000000000}.
\]

They are positive; a common fee need not reduce conditional revenue on
every charged row. Their sum and the lower-strip term give the actual
net compensation cost

\[
\boxed{J_1=-\frac{24631898853429}{125000000000000000000000}<0.}
\tag{3}
\]

Since the opponent low-report interval has length \(1/5\), equation
(1) yields

\[
\begin{aligned}
J_2&=\frac15\int_{7/10}^{71/100}
\left[\frac{e\alpha\ell}{4}
-\frac{e^2\ell^2}{2\delta}
-\frac{e^3\ell^3}{\alpha\delta^2}\right]dt\\
&=\frac{1110803432734877157}{1363542488000000000000000000}
+\frac{6248637}{282500000000000}\log\frac{161}{176}
-\frac{61575471}{282500000000000}\log\frac{613}{628}
-\frac{9308601}{5000000000000000000}\log\frac{13}{10}.
\end{aligned}
\tag{4}
\]

An outward rational logarithm enclosure gives

\[
4.113183132969685666897026142330621130\times10^{-9}
\le J_2\le
4.113183132969685666897026142330621131\times10^{-9}.
\]

Adding (3) and (4) proves

\[
\boxed{
3.916127942142253666897026142330621130\times10^{-9}
\le J\le
3.916127942142253666897026142330621131\times10^{-9}.}
\]

In particular \(J>26902077489/12500000000000000000>0\), the
separate conservative lower bound. This is a fixed-parameter complete
revenue comparison. It is not an optimization over \(e\), an unrestricted
auction optimum, or a claim that the old conditional certificate still
attains equality after the residual changes.

## 4. Suggested concise manuscript wording

> Fix \(e=9/10000\). Lowering the lottery payment on the specified
> bidder-2 menus has exact full-menu revenue gain (1). Although the old
> inner certificate has corner mass \(\lambda=\alpha(c+\ell/4)\), its
> convex-trace slack increases at first-order rate \(\alpha c\), so the
> actual conditional revenue derivative is \(\alpha\ell/4\). On each
> compensating bidder-1 menu, the common entry fee satisfies (2), because
> its no-sale area is \(D+Ch+h^2/2\) and both outer traces stay positive
> for \(0\le h\le e\); these facts remain valid on the E-plus rows
> with \(C>1\). Exact integration gives \(J_1<0\), \(J_2>0\), and
> \(J_1+J_2>0\) as displayed above. Pointwise joint feasibility is
> supplied by the separate complete-menu construction at this fixed
> parameter.

Avoid presenting the order comparison alone as the proof, omitting
displaced purchases or dropped buyers, calling every fee contribution a
loss, identifying \(\lambda\) with the actual payment-cut derivative,
or inferring a feasible generic \(e\)-family from the selected example.

## 5. Sources and verification boundary

The source base is
`research/closed/two-bidder-two-item-dsic-certificates/certificate/joint_residual_screening_lower_bound/source/V4_6/`.
Read: `research_log/price_joint_reallocation.md`,
`research_log/price_joint_exact_revenue.md`,
`research_log/inner_lottery_certificate.md`, and their named verifiers.
The trace identity is the inner note's Section 4; the full lottery change
is its equation (9), checked by `payment_cut_identity`. The selected
mechanism note's equations (5)--(7) specify the conditional changes and
strict bound. The exact-revenue verifier's `fee_revenue` and `calculate`
functions supply the source integrals compared here.

Both existing verifiers were replayed with `python -B -X utf8`, without
`--write` or `-O`, and passed:

- `price_joint_revenue.py`: `PRICE_JOINT_REVENUE_EXACT_PASS`.
- `inner_lottery_certificate.py`:
  `INNER_LOTTERY_FULL_RANDOMIZED_CERTIFICATE_PASS` (20 exact polygon
  examples and 63 actual residual boundary checks).

The companion `joint_explanation_check.py` imports no source verifier.
It independently computes full-menu revenues and no-sale areas by rational
polygon clipping, integrates the fee cells through exact triangle monomial
moments, and integrates the lottery rational function by local simple and
double-pole residues. The reconstructed numerator identity is checked
exactly, and logarithms receive rational series remainder bounds. It passed
with `JOINT_EXPLANATION_INDEPENDENT_EXACT_PASS` and reproduced (3), (4),
and the outward intervals. Its finite menu examples check the formulas;
the continuum geometric derivations above and the source's separate
pointwise construction are the stated proof dependencies. No optimizer,
literature search, source edit, or reviewer-report edit was performed.

After this independent calculation, I also read the newly added paragraphs
in `research/closed/two-bidder-two-item-dsic-certificates/manuscript/joint_residual_screening.tex`,
from the discussion of the coefficient lambda to the fixed-choice claim
boundary. The trace slack, fee geometry, actual C-greater-than-one row,
signed revenue decomposition, and conservative positive bound agree with
this check. I found no overstatement of the capacity-pairing derivative
or of an admissible epsilon family. I recommended the notational refinement
of writing the conditional payment-cut derivative at `0+`, to specify the
nonnegative cut direction. I did not edit that manuscript.
