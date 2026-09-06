# Independent audit: release a bidder 1 item and re-solve the resulting free fibers

This audit checks the proposed release construction analytically and replays its exact rational transfer witness. It does not implement the root agent's mechanism or duplicate its certificate. No new external source was retrieved; the single-buyer upper bound has the already audited INNER-1 scope.

## Audited construction

Let \(M^{V3}\) be the complete V3 mechanism and let \(u_1\) denote its normalized truthful bidder 1 utility. Fix

\[
\varepsilon=1/100000,\qquad
E_\varepsilon=\{w\in[0,1]^2:w_1<d+\varepsilon,\ w_2<d+\varepsilon,
\ w_1+w_2<b+\varepsilon\},
\]

where \(d=501/1000\), \(b=91/100\). For bidder 1 replace the utility by

\[
u_1^\varepsilon=(u_1-\varepsilon)_+.
\]

The pointwise implementation retains the V3 allocation and adds \(\varepsilon\) to its payment when \(u_1>\varepsilon\); at \(u_1\le\varepsilon\) it allocates nothing and charges zero. Bidder 2 receives the SJA menu on \(E_\varepsilon\), and its complete V3 allocation/payment section outside \(E_\varepsilon\).

The SJA menu has singleton price \(2/3\) and bundle price \((4-\sqrt2)/3\), with a specified maximizing tie rule. All switching predicates use the exact inequalities above.

## 1. Pointwise incentive and feasibility checks

For each fixed opponent report, \(u_1\) is a continuous convex function on the closed square. The function \(\max(0,u_1-\varepsilon)\) is convex. Where \(u_1>\varepsilon\), the selected original allocation is a subgradient of this function, including any original positive-utility tie. Where \(u_1\le\varepsilon\), the zero vector is a subgradient of the truncated function: the function is nonnegative everywhere and equals zero at the current type. Thus the allocation/payment rule realizes this utility pointwise and is DSIC/IR against every report. At \(u_1=\varepsilon\), the empty selection is valid without an almost-everywhere qualification.

Equivalently, add a common fee \(\varepsilon\) to every nonempty V3 option. Rankings among nonempty options remain unchanged; select the old option only when its new utility is positive, and otherwise select empty. This description is valid because V3 includes the empty option at zero and uses its normalized menu implementation.

Every nonempty V3 singleton price is at least \(d\), and every bundle price is at least \(b\). Indeed, the global affine-base lower bounds are proved in the free-fiber note, and each V3 price is a nonnegative increment of its base price. Consequently, for every fixed \(w\in E_\varepsilon\) and every bidder 2 report, each nonempty V3 utility for bidder 1 is strictly less than \(\varepsilon\). Therefore \(u_1(w,z)<\varepsilon\), and bidder 1 is identically empty over that entire bidder 2 section.

On \(E_\varepsilon\), bidder 2 faces its full unrestricted square with both items available at every own report. The SJA replacement is feasible and DSIC/IR on the complete section. Outside \(E_\varepsilon\), bidder 2 remains V3, while bidder 1 either retains its original row or deletes it. Capacity therefore remains feasible there as well. The boundary of \(E_\varepsilon\) belongs to the outside branch and inherits this argument.

Bidder 1's incentives do not involve bidder 2's payment or allocation; altering the latter after the truncation does not change the established bidder 1 inequalities. For bidder 2, changing its menu as a function of the opponent report introduces no cross-opponent incentive condition. These two facts justify the joint splice. All predicates and finite-option selections are Borel. Every payment is nonnegative and bounded by the selected reported value, hence by two.

## 2. Uniform revenue-loss bound for the release

For any normalized DSIC section with allocation in \([0,1]^2\), its convex utility \(u\) is Lipschitz on the square, with the continuous boundary traces used below. Payment equals \(v\cdot\nabla u-u\) almost everywhere, irrespective of the pointwise allocation chosen on ties. Integration by parts gives

\[
R(u)=\int_0^1u(1,t)\,dt+\int_0^1u(t,1)\,dt
-3\int_{[0,1]^2}u(v)\,dv.
\]

The lower and left faces vanish from the boundary term because their corresponding coordinate is zero. No assumption that utility vanishes on those entire faces is needed.

Set \(h(v)=\min(u(v),\varepsilon)\). Since \(u^\varepsilon-u=-h\),

\[
R(u^\varepsilon)-R(u)
=-\int_0^1h(1,t)\,dt-\int_0^1h(t,1)\,dt
+3\int_{[0,1]^2}h(v)\,dv
\ge-2\varepsilon.
\]

This bound holds on every opponent section. Integrating over the opponent's unit square therefore yields

\[
R_1(M_1^\varepsilon)-R_1(M_1^{V3})\ge-2\varepsilon.
\]

The argument uses almost-everywhere gradients only to compute expected revenue. It does not weaken the preceding pointwise mechanism proof.

## 3. Bidder 2 gain and resulting strict lower guarantee

For every fixed opponent report, the original V3 bidder 2 section is itself a feasible DSIC/IR single-buyer mechanism under full capacity. Hence its conditional revenue is at most the SJA optimum \(R_*=(12+2\sqrt2)/27\), including when the competing section is randomized. Applying the SJA replacement on \(E_\varepsilon\) therefore never decreases conditional bidder 2 revenue there.

On the old region \(E\subset E_\varepsilon\), the V3 menu is exactly \((a,a,b)\), so this gain integrates to the previously verified

\[
\Delta=-\frac{56874392995943}{2250000000000000}
+\frac{246769}{13500000}\sqrt2.
\]

The remaining annulus \(E_\varepsilon\setminus E\) contributes a nonnegative gain. Thus

\[
R(M^\varepsilon)-R_{V3}\ge\Delta-2\varepsilon
>0.0005531635998213549702>0.
\]

This is a certified lower guarantee, not an exact evaluation of the release candidate's revenue. In particular, it does **not** establish that this candidate beats the zero-release free-fiber splice, whose improvement is exactly \(\Delta\). The latter remains a stronger numerical lower guarantee unless the release candidate is integrated more sharply. The release candidate additionally certifies a genuine transfer of an item from bidder 1 to bidder 2.

Only the fully free inner sections on \(E_\varepsilon\) are optimized here. Bidder 2's V3 continuation outside that region is admissible; it is not claimed to maximize the complete residual inner problem.

## 4. Exact genuine transfer witness

The rational profile is

\[
w=(100201/200000,1/100)=(d+\varepsilon/2,1/100),
\quad z=(1/4,99/100).
\]

An independent exact replay of the frozen V3 evaluator gives

| Quantity | Bidder 1 | Bidder 2 |
|---|---:|---:|
| V3 selected mask | 1 | 2 |
| V3 payment | \(501/1000\) | \(127199/200000\) |
| V3 utility | \(1/200000\) | \(70801/200000\) |

The corresponding conditional menus are

\[
(0,501/1000,99/100,158/125)
\]

for bidder 1, and

\[
(0,159/250,127199/200000,91/100)
\]

for bidder 2. These outputs use exact rational and quadratic comparisons, not floating tolerances.

Bidder 1's old utility is \(\varepsilon/2\), so the truncation deletes its item 1. The report \(w\) lies strictly in \(E_\varepsilon\), making bidder 2's menu SJA. Bidder 2's bundle utility is

\[
31/25-(4-\sqrt2)/3=\sqrt2/3-7/75>0,
\]

which strictly exceeds its item 2 utility \(99/100-2/3=97/300\); equivalently \(\sqrt2>5/4\). Its item 1 utility is negative. Thus bidder 2 uniquely selects the bundle and the final masks are \((0,3)\).

The change \((1,2)\to(0,3)\) transfers item 1 from its old winner to the other bidder. It is stronger than filling unallocated inventory. All selection and switching inequalities at the witness are strict, and the V3 formulas are continuous on the corresponding branches, so the same transfer holds on a nonempty open neighborhood. The witness is not a tie or null-set modification.

## Audit verdict

The feasibility, DSIC/IR, universal \(-2\varepsilon\) loss bound, SJA conditional improvement, and genuine-transfer witness are correct under the frozen V3 definitions. The construction certifies a strict improvement over V3 and a positive-measure escape from the old joint containment. No exact ranking against the zero-release splice, complete residual-inner optimum, or unrestricted upper certificate follows from these arguments.

## 5. Independent audit of the implemented release and certificate

The subsequently supplied `verifier/release_joint.py` and `certificate/release_joint.json` were read in full and independently replayed. The checked SHA-256 identities are:

- `release_joint.py`: `f45051baa2a57d3f5a5e655be45108ca09f7c11523fa82a03cf059bea8763349`.
- `release_joint.json`: `88ce213e3671d52064079358da25e223d7ad2d323c068a317f109fbcbe1c78a3`.

The implementation matches the proof: it raises every nonempty bidder 1 menu price by the same exact rational fee; retains the old allocation precisely when old utility is strictly greater than that fee; and assigns empty, zero payment, and zero utility at or below the fee. The bidder 2 SJA replacement occurs precisely on the strict set \(E_\varepsilon\). Outside it, bidder 2's allocation, payment, menu, and utility remain V3. The SJA minimum-mask tie rule selects empty at a zero-utility tie. No floating comparison participates in these decisions.

The certificate's positive-volume box is

\[
\begin{aligned}
w_1&\in[d+\varepsilon/3,d+2\varepsilon/3],&
w_2&\in[9/1000,11/1000],\\
z_1&\in[249/1000,251/1000],&
z_2&\in[989/1000,991/1000].
\end{aligned}
\]

Every point lies inside the appropriate V3 base branches. The menus throughout this box simplify exactly to \((0,d,z_2,z_2+c)\) for bidder 1 and \((0,a,s-w_1,b)\) for bidder 2. Thus bidder 1 uniquely receives item 1 with utility between \(\varepsilon/3\) and \(2\varepsilon/3\), which is deleted by the release. Bidder 2 uniquely receives item 2 before the change: \(z_2>s-w_1\), \(z_1<a\), and \(z_1<w_1-(d-c)\) make that option positive and strictly better than the bundle. Afterward, \(z_1>b_*-a_*\) and \(z_2>a_*\) make the SJA bundle uniquely optimal. These inequalities have uniform strict margins over the full box. Its exact four-dimensional volume is \(1/37500000000000>0\).

Independent execution returned:

```text
PASS release_joint: positive-volume item transfer, strict revenue guarantee, exact ties
PASS independent box-corner replay: 16 exact rational profiles; old/new masks (1,2)->(0,3)
```

The additional 16-corner replay is a smoke check; the preceding affine branch formulas and uniform inequalities prove the claim on the entire box. The implemented exact equality witness also checks \(u_1=\varepsilon\) on the excluded boundary \(w_1=d+\varepsilon\), obtaining masks \((0,2)\): bidder 1 selects empty and bidder 2 retains V3.

The certificate labels its revenue number as a guaranteed lower gain, not an exact revenue evaluation. Both the code and certificate restrict the exact inner-solve claim to \(E_\varepsilon\), and explicitly decline an outside-fiber inner optimum, superiority to the zero-release splice, or unrestricted auction optimality. No code defect or unsupported full-inner claim was found in the audited version.
