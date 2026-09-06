# Conditional revenue-gap map for the frozen V4.6.1.1 mechanism

For **each bidder**, the actual conditional revenue gap is exactly zero
on a disjoint union covering

\[
\boxed{\frac{2887322279191}{4500000000000}
=0.641627173153555\ldots}
\]

of the opponent-report square. The remaining area is unresolved, not a
certified positive gap. These conditional statements do not prove global
auction optimality: changing the opponent's allocation can change the
residual capacities, menus and information rents simultaneously.

All entries refer to the actual selected mechanism in
[`refined_candidate.py`](../verifier/refined_candidate.py), including
its reserve increase, exchange jump, inverse plateau, capped Q menu,
E lottery, closed fee support and complete joint tie rule. No region is
being assigned the residual capacity of a convenient predecessor.

## 1. What the gap means

Fix bidder i and opponent report w. Write v for bidder i's own type,
and let

\[
r_i(v;w)=1-x_{-i}(w,v)
\]

be the actual residual from the complete frozen mechanism. If its
conditional expected payment is R_i(w), define

\[
\Delta_i(w)=\sup_{\substack{M\ \text{complete, measurable, DSIC/IR}\\
                           x_M(v)\le r_i(v;w)\ \forall v}}
               R(M)-R_i(w).
\]

The supremum permits arbitrary randomized allocations and arbitrary
menus over the entire continuous type square. The candidate itself is
feasible, so Delta_i(w)>=0. A zero entry means a matching unrestricted
conditional upper bound has been proved, not that a search failed to
find a better menu. An unresolved entry has neither a zero certificate
nor a certified strictly positive gap.

## 2. Exact region map

Use t=max(w), rho=min(w), z=sum(w), and

\[
A=2/3,\quad c=157/500,\quad q=93/500,\quad
a=1025947/1500000,\quad b=1496947/1500000,
\]
\[
T=1-2c/3=593/750,\qquad u=3421/10000.
\]

| Opponent region | Exact area | Both bidders' actual conditional gap | Proof and implication |
|---|---:|---|---|
| Q: t<=A and z<=b | 1746937679191/4500000000000 | Zero | Full diagonal/coupled screening certificates, including the safe-price cap; further gains require a residual change |
| E: A<t<T and rho<c | 4867/62500 | Zero | Full randomized lottery certificate with the actual IC-derived junction trace; further gains require a residual change |
| W: t>=1-q and z>=1+u | 438867/2500000 | Zero | New strip-and-left-trace screening identity for the actual high base wing; further gains require a residual change |
| Complement of Q union E union W | 1612677720809/4500000000000 | Unresolved | Base fibers where whole-menu replacement and coordinated outer reallocation both remain discovery routes |

The regions are disjoint: Q has t<=A, E has A<t<T, and W has
t>=1-q>T. The closed boundaries defining Q and W are included in their
certificates; E is open as displayed. Reports on other exceptional
faces retain the complete mechanism's specified rule even when the map
does not classify their conditional optimum.

The areas follow directly from planar geometry:

\[
|Q|=A^2-\frac{(2A-b)^2}{2},\qquad
|E|=2c(T-A),\qquad |W|=2q(1-q-u).
\]

Thus Q, E and W occupy approximately 38.8208373154%, 7.7872%, and
17.55468%, respectively. Their total is **64.1627173154%**; the
unresolved complement is **35.8372826846%**. These are opponent-space
areas for each bidder, not four-dimensional auction probabilities or
shares of revenue.

For finer Q accounting, its free part t<=1/2 has area

\[
\frac14-\frac{(1-b)^2}{2}
=\frac{1124990679191}{4500000000000}.
\]

The constrained/capped remainder has area 621947/4500000.
The small triangle with t<=1/2 but z>b is outside Q and is not
silently included in the free-Q certificate.

## 3. Exact conditional values

The following values are both the candidate revenue and the full
randomized residual-screening optimum on their stated regions.

### Q

For a proper deterministic menu with singleton prices P,B and bundle
price C, define

\[
\begin{aligned}
\mathscr R(P,B,C)={}&P(1-P)(C-P)+B(1-B)(C-B)\\
&+C\left[(1-C+B)(1-C+P)
                  -\frac{(P+B-C)^2}{2}\right].
\end{aligned}                                                \tag{1}
\]

This integrates the entire type square, not a pointwise virtual-value
comparison. On all Q rows its geometric hypotheses hold:
0<=P,B<=1 and max(P,B)<=C<=P+B.

On Q_free, put b0=(4-sqrt(2))/3 and C=max(b0,z). The conditional value
is R_i(w)=mathscr R(A,A,C).

On the rest of Q let k=h^{-1}(t), using the actual generalized inverse
with k=c on 1/2<t<=h(c). The structural proof establishes that the
additional floor k+h(rho) is redundant. Thus

\[
C=\max\{5/6+3k^2/4,z\},\qquad B=\min\{A,C-k\},\qquad
R_i(w)=\mathscr R(A,B,C).                                    \tag{2}
\]

The full randomized upper bounds, their actual top and anchor capacity
conditions, and the cap case are proved in
[`refined_structure_audit.md`](refined_structure_audit.md), Section 7.
They apply even where C0(k)>1; a nonexistent C<1 premise is not used.

### E

Put U=5/3-2c and

\[
\delta=9(T-t)(U-t)/16,\quad\alpha=3t-2,\quad
\beta=\frac{\alpha}{\alpha+2\delta},
\]
\[
B=1/2+\delta,\quad C=t+c+\delta,\quad k=t-q,
\quad L=\delta+\alpha/2,\quad Y=c+L.
\]

The scarce-singleton, safe-singleton, lottery and bundle cell areas are,
respectively,

\[
c(1-t),\qquad k(1-B),\qquad
\ell=L(1-t)+\frac{\beta L^2}{2},
\]
\[
m=(B-Y)(1-C)+\frac{B^2-Y^2}{2}+(1-B)(1-k).
\]

Therefore the exact full conditional value, independent of rho<c, is

\[
\boxed{R_i(w)=tc(1-t)+Bk(1-B)+(t+\beta c)\ell+Cm.}            \tag{3}
\]

The full randomized proof is Section 8 of the same structural audit.
Its exceptional-report issue matters: with a>A the old claim that the
opponent literally occupies the entire junction segment is false.
Instead actual occupation on an adjacent open rectangle forces every
DSIC competitor's utility to be constant along the junction trace.
The two horizontal incentive inequalities then force its relevant
selected allocation to zero on that trace. This is a valid actual
residual certificate; it is not an arbitrary-residual supergradient
obtained by discarding a line-price term without its IC argument.

### W

Align the high opponent item with item 1 and put

\[
p=\min(rho+q,1),\quad k=z-p.
\]

The only positively useful options are the safe item at p and the
bundle at z. The exact full conditional value is

\[
\boxed{R_i(w)=pk(1-p)+(k+p)
\left[(1-k)(1-p)+\frac{(1-k)^2}{2}\right].}                  \tag{4}
\]

The proof in [`residual_wing_screening.md`](residual_wing_screening.md)
uses actual first-item occupation plus the left-edge incentive trace.
It allows p below 2/3. Its nonnegative price-density margin is uniformly
at least 18601/5000000. At p=1, (4) is z(2-z)^2/2, and the separate
pure-bundle support also allows arbitrary residual perturbations within
that conditional problem.

## 4. Which positive gaps were repaired, and what the jump establishes

The safe-price cap has an explicit whole-menu revenue reason. In the
uncapped intermediate construction, whenever C=z and
H=z-k-A>0, the safe singleton price z-k is above A. Replacing it by A
changes the full conditional menu revenue by

\[
\mathscr R(A,A,z)-\mathscr R(A,z-k,z)
=\frac32kH^2+\frac12H^3>0.                                \tag{5}
\]

The cap is installed in the frozen candidate and proved compatible
across both bidders' full menus. The final capped row has zero
unrestricted conditional gap, rather than being left at a stationary
point of the uncapped formula. The same cap changes the top-envelope
sign that would prevent the uncapped Q certificate from applying.
The exact integrated cap accounting is in
[`refined_revenue_audit.md`](refined_revenue_audit.md), Section 4.

The exchange jump is a different kind of improvement. It changes base
prices and the other side's entire Q screening response together.
For 1/2<t<=h(c), a positive-measure interval of opponents now has
k(t)=c; the complete screened menus and information rents move with
that plateau. The old Q menus were already optimal for their *old*
residual capacities, so the jump must not be presented as evidence of
a missed fixed-residual gap there.

The frozen candidate has an explicit strict reallocation witness:

\[
(v_1,v_2)=((103/200,1/10),(63/200,99/100)).
\]

The predecessor splits the items; the refined mechanism gives the
bundle to bidder 2 and nothing to bidder 1. The verified strict
inequalities persist throughout a positive-volume box around that
profile. This is a genuine joint residual change. Its revenue gain is
established by integrating the affected complete menus, including the
inverse plateau and cap cells, rather than assigning independent
pointwise virtual revenues to the moved profiles. See the selected
candidate and the independent refined revenue audit. Earlier affine
or analytic trial gains are not additive to the frozen combined result.

## 5. Preserved baseline result and search implications

[`residual_high_screening.md`](residual_high_screening.md) proves a
different, preserved-baseline result: at the V4.6.1 constants
c=47/150 and tent endpoint u=17/50, a high region also requiring
min(w)>=1/2 has zero conditional gap and area 34/225. Its verifier
loads the predecessor's `functional_exchange.py` explicitly. It is
neither the source of the current W area nor an additional region to
add to this map. The new W proof independently checks the final reserve
a>A, revised c, jump and capped Q interactions.

On Q, E and W, successful full conditional certificates eliminate all
fixed-residual menu improvements, including arbitrary lotteries and
infinite allocation ranges. Joint changes remain possible there. On
the complement, the continuous residual-screening problem remains
unresolved: whole conditional menu replacements may help, or the
residual may already be optimal and require an outer reallocation.
No sign or size of its remaining gap is inferred from a failed
certificate basis, a finite report grid, or numerical non-improvement.

The area formulas were evaluated in exact rational arithmetic. In
addition to the cited proof replays, formulas (1)--(3) were checked
against direct exact polygon integration of 24 constrained/capped Q
and E menus in an additional audit outside the bundled replay. That
count is not part of run_all or its recorded certificate counts.
The map is an inner-problem classification for the actual mechanism;
it does not close the auction's unrestricted upper-bound gap.
