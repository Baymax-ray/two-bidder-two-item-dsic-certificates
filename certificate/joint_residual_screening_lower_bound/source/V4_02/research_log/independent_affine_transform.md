# V4.02: a globally admissible report transform and a genuine threshold transfer

**Outcome.** Scalar compression of bidder 1, with inverse payment scaling, is an exact globally feasible DSIC/IR transformation. For the frozen V3.1 mechanism it extends to a clipped translation, giving a complete joint auction that actually moves the diagnostic threshold from .373 to .320 and transfers item 2 on the earlier positive-volume box. The transformed bidder 2 remains a full randomized-inner optimum wherever the transformed opponent report lies in the certified region. This note does **not** prove a net revenue improvement.

## 1. Compression: independent proof

Let the original complete mechanism be \(M=(a_1,p_1,a_2,p_2)\). For \(0<\lambda\le1\), evaluate it at \((\lambda w,v)\); keep both allocations, charge bidder 1 \(p_1(\lambda w,v)/\lambda\), and charge bidder 2 \(p_2(\lambda w,v)\).

At fixed opponent \(v\), bidder 1's utility is
\[
U^\lambda_1(w,v)=U_1(\lambda w,v)/\lambda.
\]
Its allocation is a subgradient of this convex utility. Equivalently, scale every original conditional menu price by \(1/\lambda\); maximizing at \(w\) is the same as maximizing the old menu at \(\lambda w\). This proves all-report DSIC and IR, including ties, without differentiability assumptions. Bidder 2 faces the old self-bid-independent menu indexed by \(\lambda w\), hence remains DSIC/IR. Both allocations come from the same original joint profile, proving pointwise capacity.

The residual capacity faced by bidder 2 is exactly the original residual at \(\lambda w\). Therefore its inherited menu is a full randomized-inner optimum wherever \(\lambda w\in Q\), where
\[
Q=\{z\in[0,1]^2:\max(z_1,z_2)\le2/3,\ z_1+z_2\le91/100\}.
\]
No assertion of full inner optimality follows at other reports. Restricting bidder 1's effective reports to a smaller square does not weaken bidder 2's allowed deviation space: its own report \(v\) still ranges over the entire unit square.

If \(P(z)=\int p_1(z,v)\,dv\) and \(S(z)=\int p_2(z,v)\,dv\), the exact revenue identity is
\[
R(\lambda)=\lambda^{-3}\int_{[0,\lambda]^2}P(z)\,dz
+\lambda^{-2}\int_{[0,\lambda]^2}S(z)\,dz.
\]
This is an exact change of variables, not a finite-grid revenue formula. Piecewise mechanisms may require one-sided derivatives at parameter transitions; stationarity of this family does not prove unrestricted optimality.

## 2. A general clipped-translation extension

For a general monotone convex bidder utility with menu \((a_k,p_k)\), define \(f_j(w)=(w_j-\delta_j)_+\). One safe construction expands each old menu option into all subsets \(S\) of coordinates, assigning \(a_{k,S}\) and charging
\[
p_k+\sum_{j\in S}\delta_j a_{kj}.
\]
This fixed menu implements utility \(U(f(w))\). Select an old maximizing option at \(f(w)\), retaining only coordinates with \(w_j>\delta_j\), and drop coordinates at equality. Bidder 2 uses the old menu at \(f(w)\). The new bidder 1 allocation is a subset of the old allocation at that same transformed joint profile, so capacity holds. This is a complete construction for arbitrary nonnegative allocation menus; it does not infer DSIC merely from a report-dependent allocation repair.

For this general construction, bidder 2's residual can be larger than its old residual. Therefore its old conditional optimality does not automatically transfer. The next section proves why equality does hold for the particular frozen candidate.

## 3. Zero-coordinate allocations vanish for bidder 1 in V3.1

The frozen shared base allocation never gives an item with zero reported value to bidder 1. Removing such an item while keeping other allocated items fixed strictly decreases the base outcome cost:

- a lone singleton costs \(a>0\), versus zero for no sale;
- a same-bidder bundle costs \(b\), versus \(a\) after deletion, and \(b-a>0\);
- a split costs \(s\), versus \(a\) after deletion, and \(s-a>0\).

Thus every base maximizer excludes that zero-valued item; this is strict and does not depend on tie conventions. The V3 allocation is a subset of the shared base allocation. V3.1 leaves bidder 1 unchanged. Hence
\[
z_j=0\quad\Longrightarrow\quad a_{1j}(z,v)=0
\]
for every report \(v\), including exceptional reports.

Consequently, in the translated construction no positive allocation is actually discarded. Both bidders receive exactly the original allocations at \((f(w),v)\). Bidder 2's residual is identical to the old residual, so full inner optimality holds whenever \(f(w)\in Q\), including clipped coordinate faces.

For this particular candidate the expanded subset menu is unnecessary. Simply translate each bidder 1 price to \(p_k+\delta\cdot a_k\). Its old selected option at \(f(w)\) has zero allocation on every clipped coordinate and achieves utility \(U(f(w))\). Every other option's utility at \(w-\delta\) is no greater than its utility at \(f(w)\), so it cannot beat the selected option. This also supplies an explicit finite conditional-menu representation whenever the original menu is finite.

## 4. Combined two-parameter family

For scalar \(\lambda\in(0,1]\), \(\delta\ge0\), set
\[
f(w)=((\lambda w_1-\delta)_+,(\lambda w_2-\delta)_+).
\]
For frozen V3.1, keep both allocations from \(M(f(w),v)\), and use
\[
\widehat p_1(w,v)=\frac{p_1(f(w),v)+\delta(a_{11}+a_{12})(f(w),v)}\lambda,
\qquad
\widehat p_2(w,v)=p_2(f(w),v).
\]
The proof above applies after a common utility scaling by \(1/\lambda\). This complete auction is pointwise feasible and DSIC/IR on the full original report domain. It preserves the original joint tie selection at the transformed profile. Its global feasibility does not rely on the old shared allocation at the *untransformed* profile.

On the high-\(v_1\) face in the existing constrained chamber, the old boundary \(t=y+q\), \(q=227/1000\), becomes
\[
\lambda t-\delta=y+q,
\quad\text{or}\quad
y=\lambda t-\delta-q.
\]
This is an admissible movement of the joint threshold. It necessarily changes menus and revenues at other reports as prescribed by the full transformation; its benefits cannot be priced only at the local diagnostic slice.

## 5. Explicit realization of .373 to .320

Choose \(\lambda=1\), \(\delta=53/1000\). At
\[
w=(0,3/5),\qquad v=(1,7/20),
\]
the transformed opponent report is \(f(w)=(0,547/1000)\). Its inner threshold is
\[
k=547/1000-227/1000=8/25=.320.
\]
The full transformed mechanism gives bidder 1 nothing and bidder 2 the bundle, priced at
\[
C=5/6+3(8/25)^2/4=3413/3750.
\]
The current V3.1 mechanism instead gives item 2 to bidder 1 and item 1 to bidder 2. The new auction therefore realizes a genuine change of owner. It is not the arbitrary rounded Figure 3 menu graft from V4.01.

The same strict transfer holds throughout the earlier closed box
\[
w_1\in[.005,.015],\quad w_2\in[.595,.605],\quad
v_1\in[.99,1],\quad v_2\in[.34,.36].
\]
Write \(t=w_2,x=v_1,y=v_2\). The old bidder 1 price of item 2 is \(y+q\), and it uniquely purchases that item; the prior audit supplies the full branch proof. After transformation, \(f_1=0\) and \(f_2=t-.053\in[.542,.552]\), below the lowest relevant price \(.34+.227=.567\). Bidder 1 therefore selects empty.

Meanwhile \(f(w)\in Q\), and bidder 2's new certified menu has threshold \(k=t-.28\in[.315,.325]\). Its bundle beats singleton 1 by at least \(.34-.325=.015\), beats singleton 2 because \(x>C-2/3\), and has positive utility because \(x+y>C\). These inequalities are strict on the whole closed box; its volume remains \(1/50000000\).

This supplies a fully feasible DSIC extension of the desired local reallocation, but **not evidence that it increases total revenue**. It makes substantive changes beyond this box, and at the displayed profile it sacrifices bidder 1's former payment. Its total integrated revenue must decide whether this direction is useful.

## 6. Exact revenue bookkeeping for translation

For \(\lambda=1\), scalar \(\delta\in[0,1]\), and a uniform report coordinate \(w_j\), the transformed coordinate has measure
\[
\nu_\delta=\mathbf1_{(0,1-\delta]}(z)\,dz+\delta\,\delta_0.
\]
The two coordinates are independent. If \(A(z)=\int(a_{11}+a_{12})(z,v)\,dv\), then
\[
R_\delta=\int\bigl(P(z)+S(z)+\delta A(z)\bigr)
\,d\nu_\delta(z_1)d\nu_\delta(z_2).
\]
The zero-face and origin atom contributions cannot be dropped. Inner optimality remains pointwise on these atom fibers when they map into \(Q\); their positive transformed probability is another reason the earlier exceptional-report proofs matter.

`verifier/independent_affine_transform.py` supplies bounded exact arithmetic checks of the transform, the witness, clipping equalities, and 16 box corners. The global DSIC and capacity arguments are the menu proof above, not finite sampling. No new global revenue bound is asserted here.
