# A genuine bundle exchange, with its full induced screening cost

Starting from V4.6's free-bidder-1 and enlarged-lottery mechanism, the change
below increases total revenue by the exact positive number

\[
\boxed{
\Delta_{\rm exchange}
=-\frac{61265474244901887143940289321}{3402000000000000000000000000000}
+\frac{155394217}{12150000000}\sqrt2
-\frac{12495509}{797343750000}\sqrt{23}}
\]

whose value is approximately `0.000003471647404309135`. The calculation
includes the revenue lost by redesigning bidder 2's entire affected menus.
It is a genuine transfer of already allocated bundles, on a positive-volume
set. It does not fully reoptimize bidder 2 after the change, and is therefore
an admissible primal step rather than an unrestricted optimizer.

## 1. The complete mechanism

Write

\[
a=159/250,\quad b=91/100,\quad d=1/2,\quad q=113/500,
\quad A=2/3,\quad b_0=(4-\sqrt2)/3.
\]

Begin with `free_bidder_one.mechanism`, which includes both enlarged lottery
splices. Denote bidder 1's report by w and bidder 2's by v. Define

\[
G=\{v:\max(v)\le d,\quad b_0<v_1+v_2<b\}.
\]

If v lies in G, replace bidder 1's complete menu by

\[
(0,0;0),\quad(1,0;a),\quad(0,1;a),
\quad(1,1;v_1+v_2).
\]

Use the displayed order at ties. If v is outside G, retain its entire
previous row, including the faces `sum(v)=b0` and `sum(v)=b`. In particular,
the already certified closed free-region menu is unchanged.

Simultaneously, for every bidder-1 report w in the closed region Q, keep
bidder 2's two singleton prices and its existing tie priority, but replace
the bundle price by

\[
C_{\rm new}(w)=\max\{C_Q(w),w_1+w_2\}.
\]

Here the complete inherited Q prices are

\[
(A,A,b_0)\quad\hbox{if }t=\max(w)\le d,
\]

and, in high/low alignment,

\[
(A,C-k,C),\quad C=5/6+3k^2/4,\quad k=t-q
\quad\hbox{if }d<t\le A.
\]

Outside Q bidder 2 keeps its previous complete menu. This defines both
bidders on the entire continuous report space. Every changed row is a
complete utility-maximizing menu, so the mechanism is pointwise DSIC and IR
against all misreports. Its parameters and region tests are Borel, and its
finite first-maximizer rules give measurability. All accepted prices are
nonnegative and bounded by reported value of the allocation. Existing
lotteries retain their implementation.

## 2. Joint feasibility, including all ties

Raising bidder 2's bundle price alone can only retain its previous selected
allocation or replace its bundle by a subset. The unchanged priority makes
this statement pointwise even on ties. Therefore a profile with v outside
G remains feasible immediately, because bidder 1 is unchanged.

Now fix v in G. Bidder 2 can never buy a singleton: in retained rows every
singleton price is at least d, and Q's singleton prices are strictly above
d. Its own two coordinates are at most d, and empty has priority at zero
utility. In the enlarged lottery rows the safe-singleton price is greater
than d. A positive lottery or bundle choice there requires its own value
sum to exceed `t+c>b`, which contradicts `sum(v)<b`. Outside Q and the
lottery rows, the retained bundle price is at least b. Thus bidder 2 can be
nonempty only by buying Q's deterministic bundle.

If bidder 1 buys its new bundle, it has strictly positive utility because
empty comes first. Hence

\[
w_1+w_2>v_1+v_2.
\]

If w lies in Q, bidder 2's new bundle price is at least `sum(w)`, so bidder 2
strictly rejects it. Outside Q it is already empty by the preceding
paragraph. Thus no other item is allocated when bidder 1 takes the bundle.

If bidder 1 buys a new singleton, its corresponding coordinate exceeds a.
When w is outside Q, bidder 2 is empty as above. When w is in Q, its high
coordinate exceeds a and hence d, so bidder 2's bundle price is at least

\[
C(a)=5/6+3(a-q)^2/4>b>v_1+v_2.
\]

It is empty here too. At a singleton entry tie bidder 1 chooses empty.
These cases cover all allocations and ties. The new mechanism is therefore
jointly feasible pointwise, and each retained randomized outcome is feasible
in every realization.

This is not an after-the-fact allocation repair. Both changes are complete
conditional menus; their compatibility follows from the same ordered bundle
comparison that sets their payments.

## 3. A strict ownership transfer

At

\[
w=(.45,.45),\qquad v=(.44,.44),
\]

the preceding mechanism allocates the bundle to bidder 2 at price b0 and
leaves bidder 1 empty. The new mechanism allocates it to bidder 1 at price
`.88`; bidder 2 is empty because its new bundle price is `.90`.

The transfer is strict throughout the open rational box

\[
(.449,.451)^2\times(.439,.441)^2,
\]

whose volume is \(1/62500000000\). Indeed both sums are between b0 and b,
all coordinates are below d, bidder 1's sum is strictly larger than bidder
2's, and both bidders' singleton values are below a or A. This proves an
actual joint reallocation on positive volume, not merely additional use of
previously unallocated capacity or a boundary-only change.

## 4. Revenue: all incentive-compatible menu changes are integrated

For a deterministic menu with singleton prices r,s and bundle price p in
the present chamber, its full continuous-type revenue is

\[
\mathscr R(r,s,p)=r(1-r)(p-r)+s(1-s)(p-s)
+p\left[(1-p+s)(1-p+r)-\tfrac12(r+s-p)^2\right].
\]

All prices used below satisfy the chamber inequalities. This polynomial
integrates the complete winning cells, including buyers who change from a
bundle to a singleton or who stop buying.

On G, bidder 1 previously had the constant menu `(a,a,b)`. The new price is
z=`sum(v)`. The density of z in the square `[0,1/2]^2`, for `z>1/2`, is
`1-z`. Its exact gain is

\[
\Delta_1=\int_{b_0}^{b}(1-z)
[\mathscr R(a,a,z)-\mathscr R(a,a,b)]\,dz
=-\frac{6270448598899}{243000000000000}
+\frac{221749217}{12150000000}\sqrt2.
\]

This is approximately `+0.000006446105519710819`.

Bidder 2's Q menus must be changed on every affected opponent fiber,
including fibers where bidder 1 itself does not have an immediate pointwise
gain. In the free part of Q, the changed region is precisely G up to its
null boundary. Its total revenue change is

\[
\Delta_{2,F}=\int_{b_0}^{b}(1-z)
[\mathscr R(A,A,z)-\mathscr R(A,A,b_0)]\,dz
=\frac{93808494641}{12150000000000}
-\frac{13271}{2430000}\sqrt2.
\]

This is approximately `-0.000002604632943763093`.

For the constrained part of Q, put

\[
C(t)=5/6+3(t-q)^2/4,\quad B(t)=C(t)-(t-q),
\quad t_b=q+\sqrt{23}/15.
\]

The bundle price changes only for `d<t<t_b` and
`C(t)<z=sum(w)<=b`. Both item orientations give

\[
\Delta_{2,C}=2\int_d^{t_b}\int_{C(t)}^b
[\mathscr R(A,B(t),z)-\mathscr R(A,B(t),C(t))]\,dz\,dt.
\]

This is approximately `-0.000000369825171638740`. The exact verifier records
its rational-plus-\(\sqrt{23}\) coefficients separately.

There are no other payment changes. Therefore

\[
\Delta_{\rm exchange}=\Delta_1+\Delta_{2,F}+\Delta_{2,C}.
\]

This is the positive algebraic number displayed at the start. Its sign is
certified by rational square-root enclosures, not by floating quadrature.
The exact verifier also reconstructs the polynomial derivatives and checks
continuous winning-cell polygon integration independently at rational
parameters. Finite polygon checks are algebra audits, not type-grid
approximations to DSIC.

For an independently reproducible one-dimensional polynomial integrand,
write `h=b-C`,

\[
K=1+2A+2B-\tfrac32(A^2+B^2),\quad
\mathscr R_p=K-4C+\tfrac32C^2,\quad
\mathscr R_{pp}=-4+3C.
\]

Then the inner z integral is exactly

\[
\tfrac12\mathscr R_p h^2+\tfrac16\mathscr R_{pp}h^3+\tfrac18h^4.
\]

The verifier stores the coefficients after multiplication by the two
orientations and integrates them from d to \(q+\sqrt{23}/15\).

## 5. Which full inner certificates survive

The bidder-1 free-region certificate survives: bidder 2 with own report in
the closed F region was already empty everywhere, and raising a bundle price
cannot create a positive choice. The bidder-1 F menu is unchanged.

Both enlarged-lottery certificates survive. Their complete menus remain
feasible, and the two exactly occupied traces used by the inner theorem
(`y=1,x<k` and `y=c,A<x<t`) lie outside Q and outside G. Neither new change
alters these traces. The full inner theorem therefore still applies under
the new actual residuals; a globally free second item is not required.

The original Q statement must be narrowed to

\[
Q^- = \{w\in Q:w_1+w_2\le C_Q(w)\}.
\]

On these fibers bidder 2's menu is unchanged. The bidder-1 change lowers
only its bundle price, so its allocation can only increase componentwise
(the sum=b face is explicitly retained). The residual therefore decreases,
and the unchanged Q menu remains feasible by the joint proof. Monotonicity
of the residual value functional gives

\[
R_Q\le\mathcal V(r_{\rm new})\le\mathcal V(r_{\rm old})=R_Q.
\]

Thus the existing full randomized inner bound remains tight on Qminus.
On `sum(w)>C_Q(w)`, the bidder-2 menu was changed and its inner optimum is
again open. The calculated negative screening cost is real; it is paid for
by a larger bidder-1 revenue gain. One must not retain the old full-Q
certificate claim after making this joint reallocation.

The full auction upper bound remains unmatched. This step supplies an
explicit admissible outer move, a complete inner response, and the exact
opportunity cost of that response. It does not assert that this response is
the fully optimized value functional on the changed Q fibers.
