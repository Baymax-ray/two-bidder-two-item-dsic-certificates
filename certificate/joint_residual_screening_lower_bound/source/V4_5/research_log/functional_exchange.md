# Localized non-affine exchange families: two complete trials

This V4.5 route constructs two complete functional deformations of frozen V4.02. Both retain the full randomized residual-screening certificate on Q at their **actual changed residual**. Numerical integrated first variations are negative in the tested interval, so neither is promoted as a new lower-bound improvement. They identify the cost of two conservative junction continuations; they do not imply that nonlinear exchange thresholds are unprofitable in the unrestricted problem.

## 1. Parameters and the threshold function

Write bidder 1 as w=(r,t), bidder 2 as v=(x,y), with item 2 the exchanged item. Freeze V4.02, including s'=142/125, a=159/250, b=91/100, q'=s'-b=113/500, d'=s'-a=1/2, and Q={max(w)<=2/3, sum(w)<=b}. Let e be any nonnegative continuous piecewise-affine function supported in J=[L,U]=[29/100,39/100], with e<=1/1000 and every slope strictly between -1 and 1. Put

    h_up(y)=y+q'+e(y),       h_down(y)=y+q'-e(y).

Extend e by zero to the real line. Both h functions are strictly increasing piecewise-affine homeomorphisms of R; write g=h^{-1}. Their inverses equal t-q' outside [L+q',U+q']. No own-report transformation is used. The conditional menus keep their original deterministic allocation vectors.

The concrete trial uses the tent with nodes (29/100,0), (17/50,1/1000), (39/100,0). Its slopes are +/-1/50. The evaluator permits heights from 0 through 1/1000. At height zero it recovers the complete frozen candidate.

Write p_i=(0,A_i,B_i,C_i) for each frozen conditional menu, in item 1 / item 2 / bundle order. Prices depend only on the opposing report. Let (m_1,m_2) denote the frozen jointly feasible choice including its original tie rules.

## 2. Upward threshold: a contraction and a full Q response

Bidder 1's new menu is

    (0,A_1,B_1+e(y),C_1+e(y)).

On Q with t>d', bidder 2 receives the menu

    (0,C(k)-k,2/3,C(k)),  k=g_up(t),  C(k)=5/6+3k^2/4.

The safe item is item 1. On other reports bidder 2 retains its frozen menu and selection. In particular the Q fibers whose larger coordinate is item 1 are unchanged: they have t<=b/2<d'.

Bidder 1 chooses empty if maximal utility is zero, retains m_1 if it remains maximizing, and otherwise chooses the smallest maximizing subset of m_1. Such a subset always exists. Every frozen menu has strict subadditivity A_i+B_i-C_i>0: outside Q it follows from the shared-base gap q'>0 and nonnegative increments; on Q it is 2/3-k>0, or its positive SJA counterpart. Raising one singleton and the bundle by the same nonnegative amount admits a maximizing subset of any original maximizing allocation. If the old choice was the surcharged singleton, the other singleton cannot have had nonnegative utility, since strict subadditivity would then make the old bundle strictly better. The other original choices are immediate. Thus bidder 1 only drops items.

Bidder 2 uses tie order empty, safe singleton, scarce singleton, bundle on each changed Q fiber. The argument below proves that **every** candidate maximizer is feasible there, including all ties. Outside Q bidder 2 is unchanged, so bidder 1's contraction already proves joint feasibility.

## 3. Downward threshold: price cut, conservative outside-Q response, full Q response

Bidder 1's new menu is

    (0,A_1,B_1-e(y),C_1).

Choose empty at zero maximal utility; retain m_1 if maximizing; otherwise choose item 2, the only option whose utility has increased. Its item-1 allocation can only decrease.

On Q with t>d', give bidder 2 the same full-screening formula with k=g_down(t). On other Q fibers retain the frozen rule. Outside Q give bidder 2

    (0,A_2,B_2+eta(t),C_2+eta(t)),
    eta(t)=g_down(t)-(t-q') >= 0.

Use empty first, then retain m_2 if maximizing, otherwise the smallest maximizing subset of m_2. The same strict-subadditivity argument proves that this selection exists.

If bidder 1 newly obtains item 2, the opponent's y lies in J and its positive utility implies t>B_1-e(y). For every y in J, the frozen base price obeys

    B_1 >= min(a,y+q') = y+q'.

Indeed, when x>d', use H(x,y)>=x+y-b and the base price H+s'-x; when x<=d', use H+a>=a, and y+q'<=U+q'<a. Frozen increments are nonnegative. Hence a new item-2 acquisition requires t>h_down(y), or y<g_down(t).

Outside Q, the frozen retained menu has

    C_2-A_2 >= max(b-a,t-q').

The difference of its frozen increments is nonnegative. After eta, a bundle maximizer requires y>=C_2-A_2+eta by comparison with item 1. An item-2 singleton maximizer instead has y>=B_2+eta by IR; strict subadditivity gives B_2>C_2-A_2. Thus every bidder-2 maximizer containing item 2 requires y>=C_2-A_2+eta>=g_down(t). This contradicts a new positive-utility acquisition by bidder 1. Old bidder-1 item-2 allocations remain safe because bidder 2 chooses a subset of m_2. Item 1 remains safe because neither bidder can newly acquire item 1. This proves complete outside-Q feasibility, including equality reports.

## 4. Actual residual on Q and its full inner certificate

Only t in [L+q',U+q'] can change the inverse threshold. Such t exceeds d' and is below a-1/1000; for w in Q, r<=b-t<d'. Bidder 1 therefore cannot obtain the safe item. The upward trial only raises the bundle price; the downward trial leaves it unchanged. Both have bundle price at least b, so no bundle can give positive utility on Q. Null-first handles the sum=b boundary.

At the safe-value top edge x=1, the frozen increments vanish and the old item-2 price is y+q' on J. The new price is exactly h(y); the own bundle stays nonpositive on Q. Since h is strictly increasing, the actual scarce residual is zero for y<g(t), one for y>=g(t), on the moved threshold range. At equality bidder 1 has zero utility and chooses empty. Outside the moved range the top threshold remains the frozen one, or the entire fiber remains free.

Feasibility of every new screening maximizer follows directly. Rename bidder 2's scarce coordinate z and safe coordinate z_safe. A scarce-singleton maximizer has z>=2/3; the perturbation is absent there, and the frozen price bound makes bidder 1 empty. A bundle maximizer has z>=k=g(t) and z+z_safe>=C(k). When z_safe>d', the frozen scarce price is at least z+q'; after the perturbation it is at least h(z) in either trial. Thus z>=g(t) gives price>=t. When z_safe<=d', the frozen scarce price is at least a. In the downward trial it remains at least a-1/1000>U+q'+1/1000>=t on every affected fiber. The upward trial only raises that price. The unchanged fibers retain their old proof; if a downward price cut newly changes an unchanged high-item-2 Q fiber, its unchanged k equals g(t), and the same inverse comparison excludes a scarce-item conflict. A low item-2 report on a high-item-1 Q fiber cannot newly acquire item 2 because t<=b/2<d'<h(J).

The scarce residual remains full for z>2/3. The safe residual is identically one. Therefore the V3.1 gap identity applies unchanged at parameter k=g(t): its no-sale utility is zero and its interior and singular top-edge capacity supports are saturated. This proves the replacement is a full randomized inner optimizer at the actual residual, with its matching nonnegative capacity measure. No optimization over a fixed menu is substituted for that certificate.

All menus are Borel, with finite affine or previously certified algebraic pieces. The explicit finite tie rules are Borel. Menu maximization gives pointwise DSIC, the null option gives IR, and bounded prices give integrability. The all-real feasibility arguments above complete the mechanism on the entire report cube.

## 5. Globally linked revenue variations

Let G(A,B,C) be the exact expected payment of the four-option menu on the uniform own-type square, defined by integrating its utility-maximizing polygon cells. Let L_2G denote its directional derivative when B and C are increased equally. This definition remains valid when a singleton price exceeds one; the usual untruncated three-price polynomial must not be used outside its cell assumptions.

For an infinitesimal tent height epsilon, write e(y)=epsilon*phi(y). The changes integrate over complete opponent fibers, not pointwise virtual values. At zero height, put t=y+q' and

    V(k)=59/108+k^2/4-k^3+9k^4/16,
    V'(k)=k/2-3k^2+9k^3/4.

The exact first-variation kernels are

    K_up(y) = integral_0^1 L_2G(p_1(x,y)) dx
              - (b-y-q') V'(y),

    K_down(y) = -integral_0^1 partial_B G(p_1(x,y)) dx
                + (b-y-q') V'(y)
                + integral_(b-y-q')^1 L_2G(p_2(r,y+q')) dr.

Thus R'(0)=integral_J phi(y) K(y) dy. There is no factor two: this family singles out bidder 1 and item 2. The Q width b-t accounts for every first-bidder type whose full inner menu must move together. The outside-Q integral is the cost of the conservative bidder-2 menu continuation in the downward trial. In the downward first integral, on this J the relevant prices satisfy 0<B<1 and 0<C-B<1, so partial_B G=(C-B)(2-3B), even where A>1.

`discovery/functional_kernel_probe.py` and `functional_up_kernel_probe.py` use adaptive one-dimensional quadrature and exact polygon geometry in floating arithmetic; a finite central difference evaluates L_2G. Their numerical results are discovery evidence only. Quadrature error outputs do not certify floating roundoff or finite-difference error. They do not enter the exact verifier.

The tested downward kernels at y=.28,.30,.34,.38,.40 are approximately -.41565,-.43338,-.46790,-.50208,-.51906. The tested upward kernels at those points are approximately -.02126,-.03288,-.06158,-.09695,-.11720. The extra .28 and .40 probes explore neighboring admissible intervals, beyond the concrete tent's [.29,.39] support. No interval-wide sign theorem or strict aggregate loss theorem is claimed from these numerical values.

The positive Q benefit in the upward trial is real: V'(k)<0 on this interval, and its threshold k moves downward. Nevertheless, the globally linked bidder-1 bundle surcharge costs more in the numerical tests. Removing that surcharge would move the bidder-1 singleton/bundle junction and permit new item-1 demand. The V4.02 junction witness already shows that a naked singleton price increase can conflict with bidder 2. That junction must be redesigned, or the complementary residual must be fully optimized, before this route can justify a less conservative functional continuation.

This is neither a stationarity certificate nor a proof against an unrestricted improvement. Successful Q certificates remove inner directions on Q; the failed total variations isolate the unresolved cost of completing the exchange across bundle junctions and outside-Q residuals.

## 6. Exact replay and strict transfers

`verifier/functional_exchange.py` evaluates the complete rational-report mechanisms with exact quadratic-field menu comparisons. It checks 54 exact inverse identities and 1480 named pointwise/boundary cases, including both sides and equality of the moving transfer surface and sum=b. These bounded checks supplement the written all-real proof; they are not a type approximation.

At w=(1/100,1133/2000), v=(1,17/50), the upward tent changes frozen masks (2,1) to (0,3). At w=(1/100,1131/2000), v=(1,17/50), the downward tent changes (0,3) to (2,1). Both have strict comparisons at the transfer decision. These verify literal joint reallocations in both directions without asserting a profitable total revenue change.

