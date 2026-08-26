# Exact rational affine-maximizer lower bound

This directory certifies one explicit deterministic DSIC, ex-post-IR, ex-post-feasible
mechanism.  It is **only a primal lower bound** for the continuous two-bidder,
two-item problem.  Nothing here is a global upper bound or a claim of optimality.

## Mechanism

Write the report profile as

\[
(x,y,z,w)=(v_{11},v_{12},v_{21},v_{22}).
\]

Set

\[
a=\frac{159}{250},\qquad b=\frac{91}{100},\qquad
s=\frac{1137}{1000}.
\]

The nine feasible outcomes, in tie-breaking order, are:

| id | allocation | affine score | cost |
|---:|---|---|---:|
| 0 | seller keeps both | \(0\) | \(0\) |
| 1 | item 1 to bidder 1 | \(x-a\) | \(a\) |
| 2 | item 2 to bidder 1 | \(y-a\) | \(a\) |
| 3 | both to bidder 1 | \(x+y-b\) | \(b\) |
| 4 | item 1 to bidder 2 | \(z-a\) | \(a\) |
| 5 | item 2 to bidder 2 | \(w-a\) | \(a\) |
| 6 | both to bidder 2 | \(z+w-b\) | \(b\) |
| 7 | item 1 to bidder 1, item 2 to bidder 2 | \(x+w-s\) | \(s\) |
| 8 | item 2 to bidder 1, item 1 to bidder 2 | \(y+z-s\) | \(s\) |

Choose an outcome of maximum affine score.  On every equality surface choose the
smallest outcome id.  This assigns every report profile, including all boundaries.

Define the exact pivot values

\[
H_1(z,w)=\max\{0,z-a,w-a,z+w-b\},
\]
\[
H_2(x,y)=\max\{0,x-a,y-a,x+y-b\}.
\]

If outcome \(A\) is selected, let \(c_A\) be its cost in the table, and let
\(W_i(A)\) be bidder \(i\)'s reported value for their assigned items.  Charge

\[
p_1=H_1(z,w)-W_2(A)+c_A,
\qquad
p_2=H_2(x,y)-W_1(A)+c_A.
\]

These formulas are a complete evaluable allocation and payment specification.

## Pointwise mechanism proof

Feasibility is immediate because every table row is a feasible allocation.  Fix
bidder 1's true type and bidder 2's report.  Under any report that induces outcome
\(A\), bidder 1's true utility is

\[
v_1\!\cdot x_1(A)+v_2\!\cdot x_2(A)-c_A-H_1(v_2).
\]

The last term is independent of bidder 1's report.  A truthful report selects a
maximizer of the preceding affine score over all nine outcomes, so no misreport can
increase utility.  The same argument applies to bidder 2.  This proves pointwise
DSIC, including ties (the fixed tie rule always selects a maximizer).

The outcomes that allocate nothing to bidder 1 are included in the definition of
\(H_1\).  Hence the selected total affine score is at least \(H_1\), so bidder 1's
truthful utility is nonnegative.  Likewise for bidder 2.  Thus IR is ex post and
pointwise.  The mechanism is deterministic, measurable, bounded, and therefore
integrable.

## Exact revenue certificate

The exact expected revenue is

\[
\boxed{\frac{26\,232\,089\,810\,531\,183}{30\,000\,000\,000\,000\,000}}
=0.874402993684372\ldots.
\]

`verify_ama.py` does not sample and does not invoke an LP, nonlinear optimizer,
floating-point hull package, or third-party dependency.  It reconstructs all
\(9\times4\times4=144\) regions obtained by fixing the winning outcome and the
active affine branch of each pivot value.  On each region the payment sum is affine.
The verifier enumerates all rational vertices from the defining inequalities,
reconstructs the exact face lattice, barycentrically subdivides the convex
four-polytope, and integrates the affine payment over every rational simplex.

Run from this directory with:

```powershell
python verify_ama.py
```

The committed `verification_output.txt` is the captured clean-run transcript.
