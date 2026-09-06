# Exact common-entry-surcharge lower bound

This directory verifies the exact revenue improvement obtained by adding a
common nonnegative surcharge to all nonempty options of the certified base
affine-maximizer menu on two small opponent-type rectangles.

It is only a primal lower bound. It contains no global upper certificate and
makes no optimality claim.

## Exact perturbation

Use the base parameters

\[
a=\frac{159}{250},\qquad
b=\frac{91}{100},\qquad
s=\frac{1137}{1000}.
\]

When the opponent report lies in

\[
\left([0,\tfrac3{10}]\times[\tfrac{23}{40},\tfrac35]\right)
\cup
\left([\tfrac{23}{40},\tfrac35]\times[0,\tfrac3{10}]\right),
\]

add \(1/40\) to the price of every nonempty bundle. Elsewhere, retain the
base menu.

A common surcharge preserves every ranking among nonempty bundles. Each
bidder therefore either keeps their base bundle or switches to opt-out. This
proves ex-post feasibility by deletion from the base allocation. Because each
bidder chooses a utility-maximizing option from a menu depending only on the
opponent, the mechanism remains pointwise DSIC and ex-post IR.

## Exact arithmetic checked

On one rectangle, after writing the varying high opponent coordinate as
\(t\), the conditional revenue change is

\[
\Delta(t)=
-\frac{2167}{10^6}
-\frac{681}{40000}t
+\frac{3}{80}t^2.
\]

The verifier reads all rational parameters and claimed obligations from
manifest.json, reconstructs this polynomial from the exact four-option
menu-revenue formula, checks the applicable price regime over the complete
closed rectangle, and verifies

\[
\int_{23/40}^{3/5}\Delta(t)\,dt
=\frac{6209}{320000000}.
\]

After both transposed rectangles and both bidders, the gain is

\[
\frac{18627}{800000000}.
\]

Adding the hash-bound base certificate gives

\[
\boxed{
\frac{26232788323031183}{30000000000000000}
}.
\]

Run:

    python verify_surcharge.py

The verifier uses only the Python standard library and Fraction arithmetic.
