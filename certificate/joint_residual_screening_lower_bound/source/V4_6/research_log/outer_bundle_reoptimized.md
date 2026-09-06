# Coupled screening response: the bundle exchange with bidder 2 reoptimized on Q

The preceding `outer_bundle_exchange.md` left the safe singleton price fixed
when it raised bidder 2's bundle price on constrained Q. That response was
feasible but suboptimal. The admissible simultaneous change derived here
strictly improves it and, with the independent anchored capacity theorem,
restores full randomized inner optimality on the entire Q region.

The extra gain over that preceding complete exchange is exactly

\[
\boxed{
-\frac{15039791471060638832530097}{486000000000000000000000000000}
+\frac{742187}{113906250000}\sqrt{23}}
\]

or approximately `0.00000030246527089655005`. The total bundle-exchange gain
over the preceding free-plus-lottery baseline is therefore

\[
\boxed{
-\frac{284123855487033850073}{15750000000000000000000}
+\frac{155394217}{12150000000}\sqrt2
-\frac{12167}{1328906250}\sqrt{23}}
\]

or approximately `0.0000037741126752056845`.

## 1. Optimality identifies the missing safe-price direction

Set `A=2/3`, `d=1/2`, `q=113/500`, `b=91/100`. For a constrained-Q opponent
report w, let

\[
t=\max(w),\quad k=t-q,\quad C_0=5/6+3k^2/4,\quad B_0=C_0-k.
\]

The preceding exchange changed the bundle price to `z=sum(w)` on
`z>C0`, keeping the singleton prices `(A,B0)`. The full-cell revenue
derivative with respect to the safe singleton price B is

\[
\partial_B\mathscr R(A,B,z)=(z-B)(2-3B).
\]

It is strictly positive throughout this region, since `B0<z-k<=b-c=a<A`.
The cap threshold at the top requires `z-B>=k`, so it is natural to follow
this admissible direction up to its binding endpoint, `B=z-k`. This is a
variation of an entire menu, rather than a pointwise virtual-revenue test.

## 2. The complete pointwise mechanism and compatibility proof

Keep bidder 1's entire bundle-exchange mechanism unchanged. Keep bidder 2
unchanged except on

\[
w\in Q,\quad t>d,\quad z=w_1+w_2>C_0(t).
\]

There offer the complete menu with high, low, and bundle prices

\[
(A,z-k,z).
\]

Use the inherited order empty, low singleton, high singleton, bundle, and
rotate by the unique high coordinate. At `z=C0`, keep the preceding rule;
the prices agree there. All other exceptional reports are handled by the
preceding complete mechanism.

For feasibility, compare this final menu directly with the certified
pre-exchange Q menu `(A,B0,C0)`. The low and bundle prices both increase by
the same positive amount `z-C0`; the high price stays fixed. The difference
between bundle and low-singleton utility remains `x-k`. If the old choice
was the low singleton, its own scarce value satisfies `x<=k<A`, so the high
singleton has strictly negative utility. It can therefore only retain the
low singleton or switch to empty. A former bundle can be retained or
contracted to the high singleton or empty. A former high singleton or empty
choice remains unchanged. The unchanged low-before-bundle priority resolves
all equality cases. Thus the final selection is pointwise a subset of the
original Q selection.

Relative to the intermediate bundle-only response, some safe-singleton
buyers can now buy the bundle. This does not undermine the proof: their
scarce item was available in the original certified Q mechanism, and the
only subsequent bidder-1 change is the explicit G bundle exchange.

When the bidder-2 report v is outside G, bidder 1 is unchanged from that
pre-exchange baseline, so subset feasibility applies. When v is in G, both
its coordinates are at most d, and both singleton prices remain strictly
above d. It can only buy a bundle. If bidder 1 takes its new G bundle,
`sum(w)>sum(v)`, while bidder 2's final bundle price is `sum(w)`; hence
bidder 2 is empty. If bidder 1 takes a singleton, the price and value
argument in `outer_bundle_exchange.md` again makes bidder 2 empty. This
proves joint feasibility at every report and tie.

Each fixed-opponent row is a full utility-maximizing menu with empty priced
at zero. Pointwise DSIC, IR, Borel measurability, bounded nonnegative
payments, and the retained lotteries' samplewise feasibility follow. The
implementation is the separate wrapper `verifier/outer_bundle_reoptimized.py`;
the preceding feasible trial and its certificate remain available unchanged.

## 3. Exact opportunity cost and gain

The affected constrained-Q region is exactly

\[
d<t<t_b=q+\sqrt{23}/15,\qquad C_0(t)<z\le b.
\]

For the complete final menu, the polynomial identity

\[
\mathscr R(A,z-k,z)-\mathscr R(A,C_0-k,C_0)=-(z-C_0)^2
\]

holds exactly. Thus the total constrained-Q screening cost, including both
item orientations and every moved own-report cell, is

\[
\begin{aligned}
\Delta^{\rm coupled}_{2,C}
&=-2\int_d^{t_b}\int_{C_0(t)}^b(z-C_0(t))^2\,dz\,dt\\
&=-\frac23\int_d^{t_b}(b-C_0(t))^3\,dt\\
&=\frac{6214545829445349343}{141750000000000000000000}
-\frac{12167}{1328906250}\sqrt{23}.
\end{aligned}
\]

It is approximately `-0.00000006735990074221434`, instead of the preceding
bundle-only response's cost of approximately `-0.000000369825171638740`.
Subtracting the former exact cost yields the positive extra gain displayed
above. The unchanged bidder-1 gain and free-Q cost then give the displayed
total exchange gain.

The primary replay integrates the degree-six rational polynomial exactly
and encloses the square root rationally. Independent continuous polygon
integration checks the whole menu identity. The root's independently
assembled double integral gives exactly the same additional
rational-plus-\(\sqrt{23}\) pair; no primary polynomial was imported by that
calculation.

## 4. The actual occupied traces required by the full inner theorem

For an affected constrained-Q fixed report w, its high value satisfies

\[
1/2<t<t_b<159/250=a,
\]

its low value is also below a, and its total is z>b0. The actual residual
under the completed exchange obeys:

\[
r_1(x,0)=0\quad(0\le x\le1/2),
\]

\[
r_2(1/2,y)=0\quad(0\le y<z-1/2),
\]

\[
r_1(x,1)=0\quad(0\le x<k).
\]

The first follows because the opposing report `(x,0)` lies in the closed
free region F; the bidder-1 SJA menu sells the bundle strictly at own report
w, since its sum z exceeds b0 and both singleton values are below A.

For the second, the opposing report `(1/2,y)` is in F if its sum is at most
b0, or in G if its sum is between b0 and z. In the first case the same SJA
argument applies. In the second, the new bundle price `1/2+y` is strictly
below z, and bidder 1's values are below a, so it buys the bundle. The closed
face `max(v)=1/2` is included in both F and G; it has not been removed to
avoid the singular capacity constraint. The exact sum=b0 face uses F.

For the top trace, neither F nor G applies to the opposing report `(x,1)`.
The retained scarce-item price is d when `x<=c` and `x+q` when `x>c`.
It is strictly below t for `x<k`. The other singleton is unaffordable and
the bundle is not profitable on this top trace, so the opponent takes the
scarce item surely. The new lottery splices do not apply at either coordinate
one, and the Q override does not apply there.

The full-inner anchored theorem uses exactly these traces, candidate
feasibility, and the parameters

\[
A=2/3,\qquad B=z-k,\qquad C=z,\qquad
m=2(z-C_0)\ge0.
\]

The candidate uses the scarce item on the rest of the priced top trace,
and uses the safe item on the priced vertical trace above `y=z-1/2`.
All hypotheses are therefore satisfied. The separate generalized
`inner_diagonal_capacity.md` proof gives a nonnegative global capacity
support for the full randomized DSIC/IR class, not merely this deterministic
family.

The free-Q changed region G uses the same anchored theorem with `(A,A,z)`;
the bottom and vertical occupied-trace proofs are identical, and its top
price below the bundle-upgrade threshold is zero. Unchanged Q fibers retain
their earlier full certificate by residual monotonicity. Consequently the
entire Q region is again solved as a full inner problem for this completed
joint reallocation. This restoration is a new certificate result and must
not be attributed to the preceding bundle-only trial.

The F and enlarged-lottery certificates remain valid as before. None of
these conditional results constitutes a common supporting capacity price
for both bidders over all reports, and the unrestricted auction upper
remains unmatched.
