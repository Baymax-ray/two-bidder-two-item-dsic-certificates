# Independent analytic audit of the lottery screening certificate

The root audit reconstructed the envelope partition and every sign before using the new inner theorem. This is independent analytic review of the full competitor class; the separate certificate script supplies rational algebra and continuous-polygon regressions. Neither is a proof-assistant formalization.

## 1. Reconstructing the partition

Let `j=C-Y=1-t/2` and `A=2/3`. Above the lottery-to-bundle junction Y, assigning all bundle points with x>A to the horizontal envelope makes the right-edge coefficient zero there. The remaining vertically integrated set has thresholds B for x<k, C-x for k<x<j, and Y for j<x<A. These regions cover the whole positive-utility set, including the intermediate bundle wedge j<x<A below the former vertical boundary; no buyer region is dropped.

The top-edge coefficient has total mass

`3*(A*C-A*j+j*j/2-k*k/2)-1`.

Substitution gives zero exactly at the proposed delta. Since every threshold is at most B<2/3, the coefficient is nonpositive below A and positive above A. Its tail F is therefore nonnegative. The top-line integration uses the actual selected allocation on that line, justified by its own horizontal DSIC envelope.

## 2. The convexity term has the correct sign

On the lottery interval write s=y-c and L=Y-c. Its right-edge coefficient is alpha-3beta*s. It has zero first moment because alpha=2beta*L. For an arbitrary convex right trace, the coefficient of a hinge starting at r is

$$\int_r^L(\alpha-3\beta s)(s-r)ds=-\frac\beta2 r(L-r)^2\le0.$$

The below-c part is bounded using monotonicity of the same trace. This yields exactly the nonnegative slack Tg stated in the theorem. Affinity of a candidate lottery region is an equality condition in this full convexity inequality; it is not imposed on competitors. Changes with first-item allocation below one are therefore covered by the proof rather than just by the tested examples.

## 3. Corner charge and the IR sink

At y=c, monotonicity of the selected first-item allocation gives

`integral_0^t a1 <= t/(t-A)*integral_A^t a1`.

Multiplication by lambda=3(t-A)(c+L/4) produces the stated finite line price. In particular there is no unbounded coefficient as t tends down to A. The sign in the final identity was checked explicitly: the line price equals lambda times the whole horizontal allocation integral plus lambda times the nonnegative monotonicity slack Ma.

The rectangle `[0,k] x [c,B]` is contained in the candidate's no-sale region. For every competitor, coordinate monotonicity makes its utility there at least u(0,c). The uniform margin

`3k(B-c)-lambda >= q(1-3q/2)>0`

therefore validates the remaining IR term. The proof permits unnormalized nonnegative utilities and negative transfers by competitors; it uses no assumption that all competitors have a zero-priced empty option.

Combining these steps reconstructs exactly

`<pi,r>-R = <pi,r-a> + Tg + lambda*Ma + Su`.

All terms are nonnegative. The line and volume measures are finite Borel measures, and every trace is of a complete pointwise DSIC utility. Arbitrary measurable randomized mechanisms are covered.

## 4. Equality and changes to the outer allocation

At the candidate, the right trace is constant below c and affine on (c,Y), the corner allocation vanishes below t, and utility vanishes on D0. These make all non-capacity slacks zero. Candidate feasibility saturates every positive volume price because that coordinate is allocated surely there. The two remaining zero-capacity requirements are precisely H1 and H2. The first concerns the top trace x<k; the second is the whole interval A<x<t on y=c, not only the corner point.

The enlarged strip proof checks both actual traces even when the opponent's total value exceeds b. The rho=c face is deliberately excluded from that enlargement. The free-capacity splice can only reduce residual capacity on its affected set for a fixed strip opponent, while the candidate is empty there. Hence its old upper bound and feasible value remain equal. The bundle trial must preserve H1/H2 and feasibility separately; its changed reports have both coordinates at most 1/2 and cannot meet either priced trace.

A later joint capacity release can violate H2, change positively priced volume capacity, or change the candidate menu itself. The old measure is still a universal support but its former equality conclusion then does not follow. In particular the tiny joint-release trial is not allowed to inherit a blanket claim of conditional optimality on all altered fibers.

The full-inner theorem passes this audit. It is a genuine reduction of the remaining optimization problem. It is not a common two-bidder upper certificate.

## 5. Independent reconstruction of the diagonal-hole anchor

For the four-option menu `(0,A,B,C)` with `A=2/3`, `k=C-B<1/2`,
`B<=A`, and `C>=C0=5/6+3k^2/4`, set the vertical no-sale boundary
`ell(x)=B` below k and `C-x` between k and A. The top coefficient is
`f=3ell-2` below A and one above A. Direct integration, independent of the
certificate implementation, gives

`m=integral(f)=2(C-C0)` and `3 area(D0)=m+1`.

Below A, f is nonpositive. Therefore
`F_m(x)=integral_x^1 f - m 1_{x<1/2}` is nonnegative: below the anchor it
is `-integral_0^x f`; above the anchor the tail is at least the positive
rightmost mass until A, and equals `1-x` beyond A. There is no missing
atomic allocation price at the jump; the anchor utility accounts for it.

Expanding `u(1/2,1)` along the bottom edge followed by the vertical line
at x=1/2 gives nonnegative capacity charges on those two segments.
The exact gap is

`<pi,r>-R=<pi,r-a> + 3 integral_D0 u - m u(0,0)`.

The last expression is at least `u(0,0)>=0` by the exact area identity.
For equality, only the top hole x<k (if B<A), the bottom occupied segment
x<1/2, and the vertical occupied segment y<C-1/2 are needed, besides
candidate feasibility. On the bottom and vertical segments the new F/G bundle exchange
forces bidder 1 to take the relevant items; the top hole is inherited
from the earlier capacity proof. This is an unrestricted
randomized conditional certificate, not a claim that the four-option
menu contains an optimizer for arbitrary residuals.

The root separately integrated the coupled price revenue by first
integrating the direct menu-cell polynomial over C0(t)<z<b and then over
1/2<t<q+sqrt(23)/15. Its exact extra pair agrees with the separate
Taylor-cost calculation; see `certificate/independent_revenue.json`.
