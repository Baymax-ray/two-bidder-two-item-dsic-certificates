# Independent continuous-cell audit of the selected corner deformation

This audit uses the actual complete baseline
`outer_bundle_reoptimized.mechanism` and the selected rational entry fee
and lottery payment cut

\[
e=9/10000.
\]

It independently verifies the fee and payment-cut revenue identities by
rational halfplane clipping of entire continuous winning cells and shoelace
areas. It imports no polynomial coefficient or primitive from the primary
`price_joint_revenue.py` calculation. This is a bounded exact algebra audit,
not a finite type grid or a claim of optimality on sampled reports.

## Actual menu identities and all tariff chambers

The audit considers 33 complete fee fibers in

\[
S=[.7-4e,.71]\times[c-2e,c+4e],\qquad c=.274.
\]

They include:

* The below-c Eplus region with its genuine five-option lottery menu.
* The exact y=c face, where the actual rule explicitly retains the earlier
  four-option menu. It is not replaced by a limiting lottery menu.
* Literal B13.1 and B14.1 tariff interiors and their exact first-match sum
  boundaries, and the adjoining zero-fee chamber above c.
* Both endpoints of the selected x range and the upper and lower y faces.

For each fiber, every positive-area winning cell is computed explicitly.
The audit then evaluates the actual complete baseline at an exact interior
point of that cell and checks both its allocation and payment against the
independently reconstructed menu. All 140 such cell/source checks passed.

Above c, writing z=y-c and the inherited fee as f, the actual deterministic
prices are confirmed to be

\[
A=x+z+f,\quad B=1/2+z+f,\quad C=x+c+z+f.
\]

The literal fees are `7/2000` in B13.1 and `7/10000` in B14.1. The first
matching row is used on their shared boundaries. Their no-sale cell has
exact area

\[
D_0=AB-\tfrac12(A+B-C)^2.
\]

The y=c face generally has a different inherited menu. Its separate audit
is relevant to pointwise mechanism identity, although that face has zero
two-dimensional mass in the fee-revenue integral.

## Full entry-fee revenue effect

Add e to every nonempty option of the entire actual menu, leaving empty at
zero. The old and new full winning-cell integrals agree exactly with

\[
\Delta R_{\mathrm{fee}}
=e(1-3D_0)-\tfrac32Ce^2-\tfrac12e^3,
\]

where C is that fiber's actual bundle price and D0 its independently
computed old no-sale area. The separate no-sale-area check is

\[
D_0(e)=D_0+Ce+e^2/2.
\]

Both identities passed on every one of the 33 audited fibers, including the
genuine lottery cells. They account for all retained buyers' extra payments,
all dropped buyers, and every switch at a moved no-sale boundary. No
information-rent effect is omitted by counting only the newly released
scarce-item cell.

The all-real chamber and feasibility arguments remain those in
`price_joint_reallocation.md` and its independent inner audit. These exact
cell checks supply an independent replay of the revenue identity, not a
replacement for those universal arguments.

## Full lottery payment-cut effect

At five independent rational high reports spanning `[.7,.71]`, the old and
new five-option menus are each integrated over the full own-report square.
Writing `alpha=3t-2` and `L=delta+alpha/2`, the resulting difference agrees
exactly with

\[
\Delta R_{\mathrm{cut}}
=e\frac{\alpha L}{4}
-e^2\frac{\alpha}{4\beta(1-\beta)}
-e^3\frac{1}{2\beta(1-\beta)^2}.
\]

The check includes the payment losses of old high-singleton and bundle
buyers who now select the cheaper lottery, as well as the additional buyers.
All five exact continuous-cell checks passed.

The complete read-only replay is
`verifier/outer_fee_polygon_audit.py`; detailed rational values are stored in
`certificate/outer_fee_polygon_audit.json`. The result is
`OUTER_FEE_POLYGON_AUDIT_EXACT_PASS`.
