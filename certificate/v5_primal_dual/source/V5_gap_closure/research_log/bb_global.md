# A complete globally profitable BB incentive flow

The accepted correction has exact net upper decrease
\[
G_{\rm BB}=\frac{4786305147}{17179869184000000}
=0.0000002785996270249598\ldots.
\]
It is a small additional component of the materially larger V5 support replacement. No finer search of this family is needed for the V5 claim. The much larger floating first-event estimate is not counted.

## Complete finite measure and revenue identity

For a report pair \(A=(x,y)\), \(B=A+(3/20,-1/40)\), with the same opponent report \(w\), give both directed IC edges equal density \(\lambda(A,w)\ge0\). Their utility marginals cancel exactly. If \(d=A-B=(-3/20,1/40)\), their allocation correction is \(+\lambda d\) at A and \(-\lambda d\) at B. For every complete DSIC mechanism,
\[
K_\lambda=\int\lambda d\cdot(x_i(A,w)-x_i(B,w))\ge0.
\]
Consequently
\[
R=\langle\Phi_{\rm new},x\rangle-K_{\rm old}-K_\lambda
-\text{all inherited utility and screening terms}.
\]
No integration by parts is invoked. The pair measure is supported on translated report graphs, but its allocation covectors have bounded body densities; it creates no singular capacity price, boundary flux or uncanceled utility source. All pairings are finite for normalized conditional potentials. The original origin utilities are retained.

The root source domain is
\[
x\in[.5,.65],\quad y\in[.45,.75],\quad
w_1\in[.82,1],\quad w_2\in[0,.65].
\]
Sixty-four disjoint subboxes and rational densities are specified in
certificate/bb_global_input.json. The density is zero outside their interiors and on their boundaries. The translated endpoint boxes are disjoint from the source boxes except on null faces. Item exchange and bidder exchange give four disjoint copies: the smaller-report maximum is at most .8 and the larger-report maximum is at least .82. These maxima and minimum-coordinate bounds also exclude every inherited sparse, first-event and master endpoint support. Both reports are outside the conditional low-square splice. The selected cells are all BB, as certified by their whole-box branch inequalities.

## Net envelope effect, including intermediate slack

Write \(\phi_{ij}\) for the inherited body fields on these supports. Initially bidder i is not a virtual winner of either item at A; at B it is the virtual winner of item 2 and not of item 1. The exact interval checks impose
\[
\begin{aligned}
\phi_{i1}(A)&\le\max(0,\phi_{-i,1}(A)),\\
\lambda/40&\le\max(0,\phi_{-i,2}(A))-\phi_{i2}(A),\\
3\lambda/20&\le\max(0,\phi_{-i,1}(B))-\phi_{i1}(B),\\
\lambda/40&\le\phi_{i2}(B)-\max(0,\phi_{-i,2}(B)).
\end{aligned}
\]
Thus the common envelope is unchanged at A and on B's first item, and falls by exactly \(\lambda/40\) on B's second item. Winner ties at the first event preserve this equality. Integrating all four copies gives the displayed exact gain. Nonzero incumbent IC slack is allowed and retained.

For the old incumbent, A selects item 2 on every certified box; B's possible rows are empty, item 2 and bundle. Write \(g=\lambda/40,h=3\lambda/20\), the actual allocations at B as \(a=(a_1,a_2)\) and \(b=(b_1,b_2)\). The exact changes, per pair parameter, are
\[
\Delta C=-g(1-a_2-b_2),\qquad
\Delta K=h a_1+g(1-a_2),\qquad
\Delta V=-g-h a_1-g b_2.
\]
Their sum is \(-g\). These are correlated identities, not independently optimized regional estimates. The certificate bounds the remaining allocation ambiguity explicitly. Thirty-seven pairs have item 2 selected at both endpoints; the other twenty-seven meet incumbent menu interfaces. The total gain is valid on all of them. Conditional screening, origin, source and boundary changes are zero.

## Independent exact replay

The discovery integrator used outward integer Taylor bounds and retained only positive cells. The final verifier reconstructs the original rational stream coefficients through the independently implemented V4.6.3 source, expands them about the two endpoint roots using the binomial theorem, and evaluates polynomial values and gradients using exact Fraction monomials. Global absolute coefficient sums bound polynomial Hessians; elementary rational bounds cover the radial Hessian. Where a box crosses an own-maximum diagonal, both smooth radial extensions are enclosed and their union is used.

The chosen densities are rounded down to multiples of \(2^{-20}\). Every retained box is rechecked with exact rational arithmetic, independent of the discovery interval engine. All source boxes are pairwise disjoint, and all inherited-support exclusions are replayed. The independent review additionally checks source reconstruction, interval primitives and the first-event envelope identities. See verifier/bb_global.py, certificate/bb_global.json and the upper-branch independent review.

The 12,000-cell discovery enclosure ceiling is not a mathematical limit on this family's attainable gain. It is not used to diagnose primal optimality or suboptimality.
