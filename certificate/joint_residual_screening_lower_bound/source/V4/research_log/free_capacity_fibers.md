# An exactly optimized residual-capacity region that escapes V3 containment

## Result

Fix bidder 1's entire V3 mechanism, including its payments, exceptional reports, and tie convention. On a positive-area set of bidder 1 reports, its allocation is zero for **every** bidder 2 report. The residual inner problem on each of these fibers is therefore the unrestricted, randomized, two-item uniform single-buyer problem. Solving those fibers completely gives the explicit asymmetric mechanism below and increases total revenue by

\[
\Delta=-\frac{56874392995943}{2250000000000000}
       +\frac{246769}{13500000}\sqrt2
       =0.0005731635998213549702032536877\ldots>0.
\]

This mechanism allocates a bundle on an open set of profiles where the shared affine base underlying V3 allocates nothing. Hence it strictly escapes that base's allocation-containment structure. The modification changes bidder 2's complete screening problem on selected opponent fibers, rather than optimizing a pointwise allocation rule. It does **not** solve the inner problem on the remaining opponent fibers, nor does it prove unrestricted auction optimality.

## 1. The free-capacity fibers

Use the frozen V3 constants

\[
a=159/250,\quad b=91/100,\quad s=1137/1000,\quad d=s-a=501/1000.
\]

Write bidder 1's report as \(w\) and bidder 2's as \(z\). Define the Borel set

\[
E=\{w\in[0,1]^2:w_1<d,\ w_2<d,\ w_1+w_2<b\}.
\]

**Lemma 1.** For every \(w\in E\) and every \(z\in[0,1]^2\), bidder 1 receives nothing and pays zero under V3.

**Proof.** The common affine base has conditional singleton prices

\[
P_1(z)=H(z)+\min(a,s-z_2),\quad
P_2(z)=H(z)+\min(a,s-z_1),
\]

where \(H(z)=\max(0,z_1-a,z_2-a,z_1+z_2-b)\), and bundle price \(P_{12}=H+b\). For a coordinate \(t\le d\), \(\min(a,s-t)=a>d\). For \(t>d\), use \(H\ge t-a\) to obtain \(H+s-t\ge s-a=d\). Thus both singleton prices are at least \(d\), globally, and the bundle price is at least \(b\). At \(w\in E\), every nonempty base option has strictly negative utility. The base selects empty uniquely. The established pointwise V3 containment property then forces bidder 1 to remain empty, with zero payment. This argument includes every opponent report and does not discard null sets. ∎

Consequently the residual capacity \(1-x_1^{V3}(w,z)\) equals \((1,1)\) for every \(z\) when \(w\in E\). This is a statement about the complete two-dimensional screening domain of bidder 2, not capacity at a single profile.

**Lemma 2.** On every fiber \(w\in E\), bidder 2's V3 menu is exactly

\[
\{(0,0),(\{1\},a),(\{2\},a),(\{1,2\},b)\}.
\]

**Proof.** Since each \(w_j<d<a\) and \(w_1+w_2<b\), the affine pivot \(H(w)\) is zero and both singleton minima equal \(a\). Every inherited common-fee row begins at opponent high coordinate strictly greater than \(d\), as checked directly from the frozen table. Every inherited bundle-pivot row requires opponent sum at least \(b\). The V3 replacement chamber begins at high coordinate at least \(d\). Hence no surcharge or joined-threshold replacement applies. ∎

The weak closure of \(E\) also forces zero bidder 1 allocation under the V3 zero-utility tie rule. The construction deliberately uses the strict inequalities above and leaves the complementary boundary unchanged, so no extension of a row-table argument is needed there.

In fact, this closed region is maximal among completely free residual fibers. If \(w_1>d\), choose opponent report \(z=(0,1)\): the final V3 menu prices item 1 at \(d\), giving positive utility. If \(w_2>d\), use \(z=(1,0)\). If both coordinates are at most \(d\) but their sum exceeds \(b\), use \(z=(0,0)\), whose bundle price is \(b\). Thus

\[
\{w:x_1^{V3}(w,z)=0\text{ for all }z\}
=\{w:w_1\le d,\ w_2\le d,\ w_1+w_2\le b\}.
\]

A larger exact inner solution with bidder 1 fixed must therefore handle genuinely type-dependent residual constraints rather than simply enlarging the free region.

## 2. Solve these inner problems and specify the complete mechanism

The known single-buyer optimum has singleton prices

\[
a_*=2/3,\qquad b_*=(4-\sqrt2)/3
\]

and revenue \(R_*=(12+2\sqrt2)/27\). Its optimality covers the unrestricted randomized class; the precise external dependency is audited in [the INNER-1 source card](../sources/inner_source_card.md). No uniqueness claim is used.

Define \(M^{\mathrm{free}}\) on the complete report cube:

1. Compute the V3 outcome with its existing all-report tie convention.
2. Leave bidder 1's allocation and payment exactly as computed.
3. If bidder 1's report lies outside \(E\), retain bidder 2's V3 allocation and payment.
4. If bidder 1's report lies in \(E\), offer bidder 2 the empty option at zero, each singleton at \(a_*\), and the bundle at \(b_*\). Select the smallest item mask among utility maximizers, with masks \(0,1,2,3\) denoting empty, item 1, item 2, and the bundle. Charge that option's price.

This defines all algebraic price ties, axes, vertices, and boundaries of \(E\). In particular, zero maximal utility selects empty.

**Pointwise DSIC and IR.** Bidder 1's own allocation/payment functions are unchanged, so all its original incentive and participation inequalities remain true. Bidder 2 faces a fixed menu for each fixed opponent report, over its **entire** own report square. Its selected option maximizes reported utility; the taxation inequality therefore proves DSIC against every misreport. The zero option gives IR.

**Pointwise feasibility.** On \(E\), Lemma 1 leaves both items available at every bidder 2 report. Outside \(E\), both allocations equal V3's. Thus item capacity is satisfied everywhere. No inference from almost-everywhere gradient constraints or numerical sampling enters this proof.

**Measurability and integrability.** The switching set is Borel, the new finite menu is constant, and the minimum-mask rule selects among finitely many continuous utility expressions. Together with V3's Borel implementation, this gives a Borel complete mechanism. All payments are nonnegative and no greater than the selected reported value, hence bounded by two.

**Scope of the exact inner solution.** Within the class that fixes bidder 1 to V3 and fixes bidder 2 to V3 outside \(E\), this splice is globally revenue optimal even allowing arbitrary randomized DSIC/IR mechanisms on \(E\). For each fixed \(w\in E\), any competing bidder 2 section is an unrestricted single-buyer mechanism and has conditional revenue at most \(R_*\). Integrating this bound over \(E\) proves the claim. There is no incentive constraint connecting bidder 2's menus across different opponent reports. Explicitly choosing the same optimal menu on every such fiber avoids any measurable-selection assumption. No corresponding claim is made for the unrestricted inner problem outside \(E\).

## 3. Exact revenue gain

For a symmetric discounted deterministic menu with singleton price \(a\) and bundle price \(b\), in the regime \(0<b-a<a<1\), each singleton cell has area \((1-a)(b-a)\). The bundle cell is the square \([b-a,1]^2\) with its lower-left triangle of leg \(2a-b\) removed. Its revenue is therefore

\[
G(a,a,b)=2a(1-a)(b-a)
+b\bigl[(1-b+a)^2-(2a-b)^2/2\bigr].
\]

Both the old and SJA prices satisfy this regime. Exact substitution gives

\[
G(159/250,159/250,91/100)=136719583/250000000,
\]

\[
G(2/3,2/3,(4-\sqrt2)/3)=(12+2\sqrt2)/27.
\]

The set \(E\) is a square of side \(d\) with a corner triangle of leg \(2d-b\) removed, so

\[
|E|=d^2-(2d-b)^2/2=246769/1000000.
\]

Bidder 1's revenue does not change, and bidder 2's conditional improvement is constant on \(E\). Independence and the unit density yield

\[
R(M^{\mathrm{free}})=R_{V3}+|E|\left[\frac{12+2\sqrt2}{27}-\frac{136719583}{250000000}\right]
=R_{V3}+\Delta.
\]

This is an exact characterization using V3's already specified algebraic/logarithmic revenue expression plus one explicit quadratic-algebraic constant. Exact rational arithmetic and a certified square-root enclosure prove the strict sign of \(\Delta\).

## 4. A strict escape from the shared base

At the rational profile

\[
w=(1/10,1/10),\qquad z=(9/20,9/20),
\]

the shared affine base uniquely selects \((\varnothing,\varnothing)\): singleton values are below \(a\), each bundle value is below \(b\), and split values are below \(s\). V3 also selects \((\varnothing,\varnothing)\). In the new mechanism, bidder 2 instead buys the bundle, because

\[
(4-\sqrt2)/3<9/10<91/100,
\]

while both singleton utilities are negative. This bundle is not an itemwise subset of bidder 2's empty base allocation.

The conclusion holds on the positive-volume box

\[
w\in[9/100,11/100]^2,\qquad z\in[11/25,9/20]^2.
\]

Throughout this box the original shared base is strictly empty, \(w\in E\), and bidder 2's new bundle utility is strictly positive. The structural escape is therefore not a tie or null-set artifact.

This one-sided construction should not be symmetrized by simultaneously applying the same rule to both bidders: there are profiles in \(E\times E\) where both reports value the SJA bundle above its price. Independent simultaneous replacement could allocate both items twice. The present definition keeps bidder 1 fixed, as required by the residual-capacity formulation.

## 5. Replay and limitations

[free_capacity_fibers.py](../verifier/free_capacity_fibers.py) independently calculates the old and new conditional revenues in \(\mathbb Q(\sqrt2)\), the exact area, the integrated gain, a strict rational enclosure, the witness, and the positive-volume box inequalities. It also evaluates selected rational exceptional reports with V3's exact algebraic comparison engine. The universal pointwise proof is the analytic argument above; those evaluations are smoke checks, not a finite-grid surrogate.

The result supplies a verified strict joint-mechanism improvement outside the old containment cone. It provides no supporting price measure for the full residual-capacity functional, and no matching unrestricted upper bound. Optimizing only these complete free fibers is a genuine inner-screening solution on a specified positive-area region, not a claim that all remaining inner fibers are solved.
