# Independent audit of the complete V5 primal transformation

**PASS for the stated global mechanism and revenue enclosure.** The root agent independently checked the convex-potential construction, moment geometry, source-face multiplicities, algebraic branch coverage and strict joint ownership witness. The independent polynomial verifier uses only Python's standard library and does not import the discovery integrator.

## Pointwise transport and ties

Let \(s=99/100,\tau=1/100\) and \(T(v)_j=(v_j-\tau)_+/s\). Every source item with zero own value is unallocated at all source reports, including ties. For the four-row menus this follows from positive singleton prices and strictly positive bundle upgrade thresholds. For E, the safe lottery coordinate must beat the scarce option, so its value is at least c. Combining its comparisons with empty and safe yields a positive lower bound \(t-\beta(q+\delta)\) on its scarce value. Thus neither zero-valued coordinate can be allocated.

For each fixed opponent, \(u_\tau(v;w)=s u_0(Tv;Tw)\) is convex: the source utility is convex and coordinatewise nondecreasing, and T is convex and coordinatewise nondecreasing. Its selected subgradient equals the source allocation evaluated at the transformed joint profile. Below a clipping knot the source allocation in that coordinate is zero; at the knot it is still zero, so there is no missing chain-rule choice. Source pointwise feasibility and its explicit feasible maximizing-pair tie rule transfer to every report profile.

The payment identity is exact at clipping knots as well as in the interior:
\[
p_{\tau,i}=s p_{0,i}(Tv,Tw)+\tau\sum_jx_{0,ij}(Tv,Tw).
\]
The utility is nonnegative, the map and inherited selection are Borel, and bounded source allocations/payments make the transformed payments integrable. No almost-everywhere feasibility argument is being substituted for the pointwise construction.

## Deterministic and E moment geometry

For clipped singleton prices P,B and bundle price C satisfying
\(0\le P,B\le1\), \(\max(P,B)\le C\le P+B\), the singleton areas are
\((1-P)(C-P)\) and \((1-B)(C-B)\). The bundle area is
\[
(1-C+B)(1-C+P)-(P+B-C)^2/2.
\]
The removed triangle fits inside the rectangle because P and B are at most one. Clipping an unavailable singleton price to one changes only null own-type boundaries. Expanding these areas independently gives the source quantity formula
\(2-2C+C^2+(P+B)(1-C)\).

For the E lottery put \(\alpha=3t-2\), \(L=\delta+\alpha/2\),
\(\beta=\alpha/(2L)\), and \(h=y-c\). The added lottery region is
\(0\le h\le L,\ x\ge t-\beta h\). The safe option is inactive there because
\(L\le q+\delta\). Before the change, the strip \(h\le\delta\) sells the scarce singleton for \(x\ge t\); the remaining strip sells the bundle for \(x\ge t-h+\delta\). Direct integration of these regions gives exactly
\[
\Delta N=\alpha\delta/4,\qquad \Delta R=\alpha^2\delta/8.
\]
The independent verifier expands the cleared polynomial identities rather than copying the integrator's menu formula.

## Source faces and the full four-dimensional objective

A transformed uniform coordinate has law
\(\tau\delta_0+s\,{\rm Uniform}[0,1]\). Independence yields sixteen source faces with multiplicities \(1,4,6,4,1\). Three-active-coordinate revenue is the full conditional screening integral against opponent \((t,0)\), plus the ordered-opponent integral of
\(P(1-P)+B(1-B)\). Its quantity counterpart uses \(2-P-B\).

The six two-active-coordinate faces consist of two single-buyer SJA faces, two same-item two-bidder faces, and two opposite-item faces. The same-item mechanism is second price with reserve \(2/3\), giving revenue \(31/81\) and quantity \(5/9\). Each one-active-coordinate face gives \(2/9\) and \(1/3\). The independent assembly using these multiplicities reproduces
\[
R_\tau\in[0.8765122087767577,\ 0.8765122260275953]
\]
to the displayed precision; the exact rational endpoints are in certificate/primal_independent.json. Its certified improvement exceeds \(48/10^6\). This evaluates all induced switches and information rents through a complete distributional change of variables, not selected favorable profiles.

## Branch coverage and algebraic enclosure

The t breakpoints include the Q inverse plateau and linear branches, the Q/E/base changes, the base H change, and singleton clipping at \(t=1-q\). Within a t strip the listed rho cuts include 0,t,c,u,d,1-q, \(b-t\), \(1+c-t\), and the Q sum/floor and cap lines. These exhaust the comparisons used by the menu formulas:

- The base H maximum switches at \(t=a,\rho=c,\rho=b-t\).
- The base singleton minima switch at \(t=d,\rho=d\); clipping at one uses \(t=1-q,\rho=1-q,\rho=1+c-t\).
- Q sum and cap choices use \(\rho=K(k)-t\) and \(\rho=A+k-t\).
- Q free reserve uses \(\rho=B_0-t\); the fee uses \(\rho=c,u\).

Whole-interval ordering bounds make the midpoint branch choice valid throughout every resolved band. The independent replay verifies that all resolved and unresolved t intervals partition [0,1] and that the recorded lost ordered area is exact. On the fifteen unresolved algebraic crossing strips, the global bounds \(N\le2\), \(P(1-P)+B(1-B)\le1/2\), and \(2-P-B\le2\) are valid.

Replacing \(B_0\) by its rational lower enclosure changes only the Q free bundle price, by less than \(10^{-15}\). The fixed-singleton SJA revenue derivative has absolute coefficient sum \(47/6<10\); the quantity derivative has sum \(16/3<8\). The full N4 formula has two bidders but the affected opponent region has area at most 1/4 for each. These bounds justify the recorded \(10^{-12}\) face enclosure allowance. The source R4 is imported from the exact unchanged lower certificate.

## Global ownership witness and new source slack

The source reports
\(v=(1577/2000,123/200)\), \(w=(3/5,4/5)\)
give old bundle/empty and new item-1/item-2 allocation. On the complete box of radius \(1/10000\), both high-sum branches remain active and the old and new strict comparison margins remain positive. This verifies a positive-volume joint reallocation. Its individual revenue effect is not substituted for the full face-moment calculation.

For opponents in the enlarged upper support W or either added rectangle J, \(Tw\le w\) remains in the free-SJA opponent branch with sum below \(B_0\). For every old SJA no-sale type \(v\in D_0\), \(Tv\le v\) implies \(u_{\rm SJA}(Tv)=0\). Hence the new conditional source term \(3\int_{D_0}u_\tau\) is still exactly zero, as is origin IR slack. This conclusion is freshly proved for V5; numerical capacity, virtual and inherited IC slack for the old incumbent are not carried over unchanged.

This audit establishes a stronger complete mechanism and a certified revenue interval. It does not establish exact unrestricted optimality, optimize all reserve transformations, or make the new mechanism complementary to the new upper certificate.
