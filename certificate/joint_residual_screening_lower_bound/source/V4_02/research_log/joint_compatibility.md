# V4.02 — Joint winner geometry, inverse transfer thresholds, and junction propagation

This note derives local compatibility conditions and a complete affine transformation interface. It does not optimize the full auction, equate the V4.01 diagnostic with GemNet, or presume that a fixed finite menu contains an optimizer. Sources inspected are the frozen V3/V4/V3.1 implementations and V4.01's structural and independent-slice notes; no new literature was used.

## 1. The active chamber and the exact inverse relation

Write bidder 1's report as \(w=(r,t)\), bidder 2's as \(v=(x,y)\). Consider an open chamber where the only relevant choices of bidder 1 are empty and item 2, while those of bidder 2 are item 1 and the bundle. Require the other menu options to be strictly worse throughout the chamber, rather than suppressing them without justification.

Let the first menu's item-2 price be \(P(x,y)\), its empty price zero, and let the second menu's item-1 and bundle prices be \(A(r,t),C(r,t)\). Put

\[
D(r,t)=C(r,t)-A(r,t).
\]

Away from ties, the two item-2 decisions are

\[
x_{12}=1\{t>P(x,y)\},\qquad
x_{22}=1\{y>D(r,t)\}. \tag{1}
\]

These directions are forced by their allocation differences: bidder 1's comparison has normal \(e_2\) in \(w\), and bidder 2's comparison has normal \(e_2\) in \(v\). Their prices can still depend nonlinearly on the opponents' report.

Suppose the joint mechanism uses all of item 2 on both sides of the switching surface, so the indicators in (1) sum to one. Assume \(P,D\) are continuous and \(D(r,t)\) lies in the interior of the active \(y\) interval. For \(y<D(r,t)\), saturation requires \(t\ge P(x,y)\). For \(y>D(r,t)\), feasibility requires \(t\le P(x,y)\). Taking limits from both sides proves

\[
\boxed{P(x,D(r,t))=t.} \tag{2}
\]

This identity must hold for every \(r,x\) in the active chamber. If these functions are continuously differentiable there, differentiation gives

\[
P_x(x,D)=0,\qquad P_y(x,D)D_r(r,t)=0,
\qquad P_y(x,D)D_t(r,t)=1. \tag{3}
\]

If the orientation is increasing, the derivatives in the last product are positive. Thus on the swept open band,

\[
P(x,y)=h(y),\qquad D(r,t)=h^{-1}(t),\qquad
D_r=0,\quad P_x=0. \tag{4}
\]

The inverse structure is rigid under the stated activity and saturation assumptions; the increasing function \(h\) is not forced to be affine. The conclusion is local: when another option becomes competitive, when item 2 is intentionally unassigned on a strip, or when the relevant boundary exits the chamber, equations (2)–(4) need not continue unchanged.

Without saturation, suppose \(P(x,\cdot)\) is strictly increasing. Feasibility requires, on the active ranges,

\[
D(r,t)\ge\sup_{x\text{ active}}P(x,\cdot)^{-1}(t). \tag{5}
\]

Equality with every inverse is then unnecessary. A four-option menu can accommodate \(x\)-dependent capacity thresholds by choosing the conservative supremum, but this can leave capacity unassigned for other \(x\). Full reallocation without such slack is more restrictive.

For a smooth perturbation \(h_s\), differentiation of \(h_s(D_s(t))=t\) yields

\[
\partial_sD_s(t)=-\frac{\partial_sh_s(D_s(t))}{h_s'(D_s(t))}. \tag{6}
\]

At the current line \(h_0(y)=y+q\), \(q=227/1000\), the first variation is \(\delta D(t)=-\delta h(t-q)\). It is a globally coupled menu change within the active chamber, not independent pointwise reassignment.

## 2. The .320/.373 diagnostic and the freedom it actually identifies

For the V4.01 diagnostic at \(w=(0,.6)\), the frozen first menu has \(P(x,y)=y+.227\) in the relevant high-\(x\) chamber. Its saturated second-bidder transfer threshold is \(D(.6)=.373\). The figure-derived surrogate has threshold .320. It remains only a surrogate of rounded labels, not the identified GemNet network.

An exact binding transfer curve implementing the latter threshold must satisfy

\[
h(.320)=.600,
\]

where the current price at .320 is .547. Thus the needed price displacement at that point is .053. The displacement must propagate through an entire opposing menu: at fixed \((x,y)\), all types \((r,t)\) face the same changed price. It cannot be restricted to the single type \((0,.6)\) by changing that menu price alone.

Equation (4) also locates a reason additional regions could become useful. If full capacity use demands a transfer threshold that genuinely depends on bidder 2's \(x\), direct competition between its deterministic item-1 and bundle options cannot realize it: their allocation difference is exactly \((0,1)\). A new active allocation pair, a new intervening region, or deliberate slack is then necessary. A fixed lottery pair can tilt the comparison only if its allocation difference has nonzero first coordinate. This is a conditional structural necessity, not evidence that the optimal auction needs a lottery.

## 3. A singleton price shift also moves bundle junctions

For a complete first-bidder deterministic menu with prices \((0,P_1,P_2,P_{12})\), the item-2/bundle indifference threshold is

\[
r=P_{12}-P_2. \tag{7}
\]

Thus increasing \(P_2\) by \(\delta>0\) while holding the other prices fixed moves this threshold down by \(\delta\). It can induce bidder 1 to acquire item 1 through the bundle, even though the motivation was to release item 2 elsewhere. To keep this second threshold unchanged one must also change \(P_{12}\) by \(\delta\); then other bundle comparisons change. That propagation is imposed by the single shared menu, not by a choice of optimization method.

There is an exact frozen-code witness. Set

\[
w=(3/4,7/10),\qquad v=(1,7/20).
\]

The current complete V3.1 mechanism chooses masks \((2,1)\). Its menus, in mask order \((0,1,2,3)\), are

\[
p_1=(0,1.076,.577,1.350),\qquad
p_2=(0,.977,.927,1.450).
\]

Bidder 1's item-2 utility is .123 and bundle utility .100. Increasing only its item-2 price by .053 gives utility .070 for item 2, so its unique optimum becomes the bundle. Bidder 2 still uniquely chooses item 1, with utility .023. The modified menus conflict on item 1. The moving threshold in (7) is .773 to .720, and \(r=.750\) lies strictly between them.

This refutes this particular incomplete price graft. It does not refute a simultaneous redesign of both menus, a coordinated change of several prices, or a complete mechanism whose transfer curve happens to contain a shifted affine segment.

## 4. A complete affine report transformation provides an admissible family

Let \(M\) be any complete DSIC/IR mechanism on the original cube, including a specified feasible tie convention. Fix \(\lambda>0\) and \(a\in\mathbb R^2\) with

\[
0\le a_j,\qquad a_j+\lambda\le1\quad(j=1,2).
\]

Evaluate \(M\) at \((\lambda w+a,v)\), preserve both allocations, and set

\[
p'_1(w,v)=\frac{p_1(\lambda w+a,v)-a\cdot x_1(\lambda w+a,v)}{\lambda},
\qquad p'_2(w,v)=p_2(\lambda w+a,v). \tag{8}
\]

For bidder 1, truthful utility becomes \(u_1(\lambda w+a,v)/\lambda\), and the same identity translates each deviation into a baseline deviation to \(\lambda\hat w+a\). Baseline DSIC therefore proves transformed DSIC; baseline IR proves transformed IR. Bidder 2 faces exactly its baseline menu at the fixed opposing report \(\lambda w+a\), so its DSIC and IR also follow. Capacity holds at every profile because the two selected allocations are those of a single baseline profile. Inherited tie selections handle exceptional reports. Payments may become negative, which is allowed by the project's full DSIC/IR class; all payments remain integrable when the baseline ones are integrable over the transformed report distribution (bounded menu payments suffice here).

For finite menus with constant allocation vectors the first bidder's transformed menu is explicitly

\[
(a_1^k(v),[p_1^k(v)-a\cdot a_1^k(v)]/\lambda).
\]

In the active chamber of Section 1, this gives

\[
P'(y)=\frac{y+q-a_2}{\lambda},\qquad
D'(t)=\lambda t+a_2-q. \tag{9}
\]

Thus affine translation permits another intercept while respecting the domain restriction \(a_2\ge0\); positive \(a_2\) partly offsets the earlier transfer induced by compression. Scalar compression is \(a=0\). At \(\lambda=547/600\), \(D'(.6)=.320\) exactly. At \(w=(0,.6),v=(1,.35)\), the transformed V3.1 source report is \(((0,.547),(1,.35))\), whose allocation is \((0,3)\), with second payment \(3413/3750\). The untransformed allocation is \((2,1)\). This proves literal joint reallocation through a complete mechanism, but does not prove its expected revenue improves; root's separate revenue analysis is required.

The integrability qualification in (8) is material for an arbitrary merely Lebesgue-integrable baseline: restriction to a lower-dimensional image could be problematic, but here \(\lambda>0\) maps to a positive-volume rectangle and a change of variables preserves integrability. Allocations here are bounded by one. Consequently original integrability suffices for this nonsingular affine map under the uniform input distribution.

There is also an exact inner-optimality inheritance. For \(T(w)=\lambda w+a\), the residual of the new first bidder is exactly the frozen residual at \(T(w)\), as a function of bidder 2's entire report. Whenever \(T(w)\in Q\), the transformed second bidder is therefore the unrestricted randomized inner optimizer already certified by V3.1, with its same row-specific support measure. The known inner-optimal region becomes \(T^{-1}(Q)\). In particular, for \(a=0\) and \(0<\lambda\le b/2=91/200\), the transformed whole square lies in \(Q\), since \(\max T(w)\le91/200<2/3\) and \(\sum T(w)\le b\). These strongly compressed candidates actually suppress bidder 1 completely: their source reports lie in the free-capacity part of \(Q\), since \(91/200<d=501/1000\). They recover the single-bidder endpoint, rather than a new nontrivial full-inner solution. For larger compression scales the complementary inner rows remain unresolved wherever the source report lies outside \(Q\).

## 5. Why a nonlinear own-report warp is not a free global extension

The nonlinear inverse curve in (4) is permitted locally. Applying an arbitrary nonlinear transformation to a complete two-item mechanism while keeping its allocation vectors unchanged is more demanding.

For a differentiable own-report map \(T\), a baseline affine indifference surface with allocation difference \(d\) pulls back to a surface with normal \(DT(w)^Td\). To implement the same two constant allocations with a self-bid-independent price difference, its active boundary must still be a hyperplane normal to \(d\). Hence a necessary local condition is

\[
DT(w)^Td\ \text{is parallel to }d \tag{10}
\]

at that active boundary. This does not assume all allocation pairs are active everywhere.

If sufficiently rich translated boundary families with directions \(e_1,e_2,e_1+e_2\) sweep the same open rectangle, the first two conditions make \(DT\) diagonal there, and the third equates its diagonal entries. On a connected open rectangle, this forces \(T(w)=\lambda w+a\) with constant \(\lambda\). For a coordinatewise map the elementary version is that every active boundary \(T_1(r)+T_2(t)=c\) between empty and bundle must have slope minus one, requiring \(T'_1(r)=T'_2(t)\). An open family covering a rectangle forces both derivatives to be the same constant.

Where only one allocation direction varies, this argument does not force affine behavior. Nonlinear thresholds can therefore live in such regions, but their interfaces with mixed-allocation regions need an explicit continuation satisfying the relevant price comparisons. No global nonlinear impossibility theorem follows from this conditional observation.

## 6. Exact certificate infrastructure: feasible joint maximizers

For fixed rational allocation vectors (deterministic masks included), define at every report the sets \(W_i\) of all utility-maximizing menu indices. A complete finite-menu mechanism exists with those menus exactly when, at every report, there is some pair \((k,l)\in W_1\times W_2\) with

\[
a_1^k+a_2^l\le(1,1). \tag{11}
\]

Choose the first such pair in a fixed lexicographic order. This is a pointwise feasible tie convention; each truthful bidder still receives a maximizing option in its own unchanged menu. Even if joint tie selection depends on both reports, any deviation only obtains another option in the same bidder's fixed menu, proving DSIC. Finite Borel menus and finite comparisons give a Borel mechanism.

Requiring *every* pair in \(W_1\times W_2\) to be feasible is sufficient but unnecessarily strong. For instance, at a saturated transfer tie both bidders may have an option containing item 2, while a jointly feasible maximum pair still exists. The certificate must either prove existence and specify the selection, or justify the stronger all-pairs test without discarding valid candidates.

If opponent-dependent prices are affine on a report cell and allocation vectors are fixed rational constants, every own-menu comparison is affine in the full report vector. One can check coverage by the cells for the finitely many feasible joint pairs, including lower-dimensional faces. In the deterministic two-item case there are nine feasible outcome pairs out of the sixteen mask pairs. Failure of an incompatible pair alone is not the criterion at ties; failure is absence of any feasible maximizing pair. Nonlinear polynomial price pieces instead give semialgebraic comparisons, requiring appropriate exact sign/coverage methods; a grid is not a substitute. Opponent-dependent allocation vectors introduce additional products and are outside this affine-polyhedral special case.

The small [joint geometry verifier](../verifier/joint_geometry_verify.py) checks the exact junction witness and affine-transform reallocation numerically only in rational arithmetic. The all-real inverse relation, transformation DSIC proof, and finite-menu selection theorem are the written arguments above. None is an unrestricted revenue-optimality certificate.
