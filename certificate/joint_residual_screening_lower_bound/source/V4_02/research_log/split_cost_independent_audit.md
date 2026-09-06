# Independent audit of the split-cost continuation

**Conclusion.** For every \(|\theta|\le1/1000\), the proposed continuation defines a complete pointwise feasible DSIC/IR auction. The concrete trial uses \(\theta=-1/1000\), hence \(s'=142/125\). It changes the jointly selected base allocation, and bidder 2 is fully reoptimized on the fixed closed region \(Q\). The proof below establishes feasibility and the inner certificate; it does not establish the sign of total revenue change or optimality over the original auction class.

## 1. The precise family

Freeze \(a=159/250\), \(b=91/100\), \(s=1137/1000\), and all opponent-dependent increments in the complete V3 menus. Change only the split cost to
\[
s'=s+\theta,\qquad d'=s'-a,\qquad q'=s'-b.
\]
The shared base selects, in its frozen tie order, a maximizer of total reported allocated value minus cost: zero for no sale, \(a\) for a singleton, \(b\) for a same-bidder bundle, and \(s'\) for a split.

For opponent report \(z\), put
\[
H(z)=\max(0,z_1-a,z_2-a,z_1+z_2-b).
\]
The new conditional base prices are
\[
P'_1=H+\min(a,s'-z_2),\quad
P'_2=H+\min(a,s'-z_1),\quad P'_{12}=H+b.
\]
Define the frozen increment vector as the **complete V3 menu minus its original base menu**, at exactly the same opponent report. Add that vector to the new base menu. This includes the V3 joined nonlinear menus, rather than reverting to the older fee-table-only baseline.

For each bidder, choose empty at zero maximal utility. Otherwise retain its new shared base allocation if that maximizes the final menu; if it does not, choose the smallest maximizing subset of that base allocation. Section 2 proves such a subset always exists.

Finally, on
\[
Q=\{w:\max(w_1,w_2)\le2/3,\quad w_1+w_2\le b\},
\]
replace bidder 2 by its new full-inner optimum. If \(t=\max(w)\le d'\), use the full-capacity SJA menu. If \(t>d'\), put \(k=t-q'\) and give its scarce coordinate price \(2/3\), its safe coordinate price \(C(k)-k\), and the bundle price \(C(k)=5/6+3k^2/4\). The tie order is empty, safe singleton, scarce singleton, bundle. Outside \(Q\), keep its new-base-plus-frozen-increment menu.

At \(\theta=0\), these allocation, payment, utility and menu rules recover V3.1. No old file or mechanism definition is changed.

## 2. Why the frozen increments remain admissible

Every frozen V3 increment vector \(\Delta(z)\) has the form
\[
\Delta_\varnothing=0,\quad
\Delta_1=f+\eta\mathbf1_{j=1},\quad
\Delta_2=f+\eta\mathbf1_{j=2},\quad
\Delta_{12}=f+\eta,
\qquad f,\eta\ge0.
\]
Equivalently, \(\Delta_{12}=\max(\Delta_1,\Delta_2)\) and both singleton increments are nonnegative. The baseline table has a nonnegative common fee and possibly one item surcharge. In the joined base branch the increments vanish; in the square-root branch they are a common increase \(C-b\); in the quadratic and affine branches they are the previously certified nonnegative common fee and safe-item-plus-bundle surcharge. The pure-menu evaluator checks this identity exactly at every rational report it evaluates.

Here is the generic argument that makes this structure portable. Let a deterministic two-item base menu satisfy
\[
P_1+P_2-P_{12}>0.
\]
A common nonnegative fee either preserves the same base maximizer or makes empty preferable. Now add a nonnegative surcharge to one singleton and the bundle. If the current base choice is the other singleton, its utility is unchanged and no rival's utility increases. If the base choice is the bundle, any replacement is a subset. If the base choice is the surcharged singleton, the other singleton's pre-fee utility must already be strictly negative: otherwise strict subadditivity makes the bundle strictly better than the selected singleton. That other singleton therefore cannot become the new positive-utility choice. Empty is safe in all cases. Thus a maximizing subset exists, including ties.

For the changed base, the uniform strict subadditivity bound is
\[
P'_1+P'_2-P'_{12}\ge s'-b=q'>0.
\]
To verify it, write \(\min(a,s'-z_j)=a-(z_j-d')_+\). If neither coordinate exceeds \(d'\), use \(H\ge0\) and \(s'\le2a\). If one exceeds \(d'\), use \(H\ge z_j-a\). If both do, use \(H\ge z_1+z_2-b\) and \(s'\ge b\). All these inequalities hold throughout the stated parameter range.

The selected final allocations are therefore subsets of the **new** shared base outcome, so they are jointly feasible before the bidder-2 replacement. These subsets need not lie inside the old shared base outcome at the same original report.

Both conditional menus depend only on opponents' reports. Menu maximization proves full DSIC, and the zero-price null option proves IR. The tie conventions above are part of the mechanism.

## 3. New free fibers, including their boundary

Each new base singleton price is at least \(d'\). In the branch using \(s'-z_j\), use \(H\ge z_j-a\); in the other branch use \(a>d'\). The base bundle price is at least \(b\). Frozen nonnegative increments preserve both bounds.

For \(w\in Q\) with \(t\le d'\), every singleton utility is nonpositive and the bundle utility is also nonpositive. Bidder 1 therefore chooses empty for **every** bidder-2 report, with equality handled by the null-first convention. Hence the residual is exactly full capacity, and the single-bidder SJA menu is feasible and inner optimal there.

The moving boundary \(t=d'\) belongs to these full-capacity fibers. The constrained formula immediately above that boundary need not converge to the same conditional menu; such opponent-report discontinuity is allowed and the boundary has been explicitly assigned.

## 4. Feasibility of every constrained candidate option

For \(w\in Q\) with \(t>d'\), the smaller coordinate \(\rho\) satisfies
\[
\rho\le b-t<b-d'<d',
\]
because \(2d'>b\) throughout the parameter range. Thus bidder 1 can receive only its high-coordinate item or nothing. Its bundle cannot have positive utility because \(w_1+w_2\le b\).

Write bidder 2's value for that scarce item as \(x\), and its value for the safe item as \(y\). Its candidate singleton price for the scarce item is \(A=2/3\), while its bundle price is \(C=C(t-q')\). The relevant new base price for bidder 1 satisfies
\[
\begin{array}{ll}
y\le d':&P'_{\rm scarce}\ge a,\quad P'_{\rm scarce}\ge x,
\quad P'_{\rm scarce}\ge x+y-c,\\
y>d':&P'_{\rm scarce}\ge x+q'.
\end{array}
\]
Frozen increments only raise it.

A candidate scarce-singleton maximizer has \(x\ge A\ge t\), so bidder 1 is empty. A bundle maximizer has \(x\ge t-q'\) and \(x+y\ge C\). For \(y>d'\), the first inequality makes bidder 1's price at least \(t\). For \(y\le d'\) and \(t\le a\), its price is at least \(a\ge t\). The remaining case is \(y\le d'\), \(a\le t\le2/3\), where its price is at least \(C-c\).

The required remaining inequality holds with uniform strict slack:
\[
C(t-q')-c-t\ge\frac{9247}{250000}>0.
\]
The expression decreases with \(t\) on \([a,2/3]\) and decreases with \(\theta\); its minimum occurs at \(t=2/3,\theta=1/1000\). All parameters here are rational, and the displayed bound is exact.

Consequently every candidate maximizing allocation is feasible with bidder 1, including all boundary ties. Outside \(Q\), the earlier shared-base subset argument already supplies feasibility.

## 5. Exact top edge and matching full inner certificate

Every frozen increment vanishes when either opponent coordinate equals one. For the joined menus this is their final base branch when the other coordinate is at most \(c\); otherwise the joined branch is absent. Baseline bundle fees are absent because the sum exceeds one, and the remaining old common/item fees do not apply. The point \((1,0)\) is covered by the same base branch.

Hence on the top safe-value edge \(y=1\), bidder 1's actual scarce-item price is exactly \(d'\) for \(x\le c\), and \(x+q'\) for \(x>c\). For \(t>d'\), the actual residual has threshold
\[
r_{\rm scarce}(x,1)=0\quad(x<k),\qquad
r_{\rm scarce}(x,1)=1\quad(x\ge k),\qquad k=t-q'.
\]
At equality, bidder 1's zero utility makes it choose empty. The safe item has full capacity everywhere on the fiber, and the scarce item has full capacity on \(x>2/3\).

The V3.1 inner certificate applies to every \(k\) here: \(c<k\le2/3-(q-1/1000)<2/3\), within its established range. The feasible candidate has zero utility on its no-sale region and saturates the actual residual on the certificate's interior and singular top-edge supports. The exact gap identity therefore attains equality. Thus each replaced conditional menu is optimal among **all randomized DSIC/IR inner mechanisms at the actual new residual**, not only among three-price menus.

There is no assertion that the retained bidder 2 is inner optimal outside \(Q\), or that this split-cost family contains an optimal original auction.

## 6. A genuine change of the shared allocation

For \(\theta=-1/1000\), take
\[
w=(1/100,3/5),\qquad v=(1,747/2000).
\]
The old V3.1 allocation is \((0,3)\), and the old shared base also allocates \((0,3)\). The continued mechanism allocates \((2,1)\). Thus item 2 is genuinely reallocated to bidder 1, and the new allocation is outside the original shared outcome's containment set.

Bidder 1's new price at the witness is \(1199/2000=.5995\), with strictly positive utility \(1/2000=.0005\). The same calculation holds if its first coordinate is zero, as in the root trial's boundary witness.

There is also a strict positive-volume transfer. Put \(\varepsilon=1/1000\), and parameterize a closed slanted prism by
\[
\rho\in[.005,.015],\quad t\in[.595,.605],\quad
y\in[.99,1],\quad h\in[\varepsilon/4,3\varepsilon/4],
\qquad x=t-q+h.
\]
The actual reports are \(w=(\rho,t)\), \(v=(y,x)\). This affine coordinate substitution has determinant one, and the prism volume is exactly \(1/2{,}000{,}000{,}000\).

Throughout it, \(x>c\), \(x+y>1\), and \(y>a\); all frozen increments in bidder 1's menu vanish. The old item-2 price is \(x+q=t+h>t\); the new one is \(x+q'=t+h-\varepsilon<t\). Its other options have strictly negative utility. The old shared base gives the bundle to bidder 2, and the new shared base splits the two items. In the final bidder-2 menus, the old scarce-item threshold is \(k=t-q\), while the new one is \(k+\varepsilon\). Since \(k<x<k+\varepsilon\) and \(y\) is high, the old bidder 2 strictly chooses the bundle and the new bidder 2 strictly chooses the safe item 1. Thus final masks change from \((0,3)\) to \((2,1)\) on the whole real prism, including its boundaries. Bidder 1's new utility is \(\varepsilon-h\ge\varepsilon/4\).

This direction is opposite to the particular Figure 3 graft's transfer. That is permissible: the figure supplied a diagnostic question, not a constraint on which direction must improve revenue. The total revenue calculation, rather than visual similarity, must decide the useful direction.

`verifier/split_cost_candidate.py` defines the complete rational-report evaluator and pure menu functions for integration or independent checks. `candidate(profile)` selects the concrete split cost \(142/125\); `mechanism(profile, theta)` evaluates the whole admitted family. Its finite checks supplement this all-real proof, including the 16 vertices in the prism's independent coordinates. It deliberately does not assert an aggregate revenue improvement.
