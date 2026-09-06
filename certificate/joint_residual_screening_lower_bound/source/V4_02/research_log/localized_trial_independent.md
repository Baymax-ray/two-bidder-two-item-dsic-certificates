# Independent audit: localized common fee with full residual reoptimization

**Result.** The proposed localized construction is globally pointwise feasible and DSIC/IR, and its new bidder-2 menu is a full randomized-inner optimum on the target opponent region. The proof below includes all ties and support boundaries. This note does not determine the sign of the total revenue change.

## 1. Complete definition and admissible constants

Use the frozen V3.1 mechanism. Its bidder 1 is exactly V3. Set
\[
a=159/250,\quad b=91/100,\quad d=501/1000,\quad
c=137/500,\quad q=227/1000,
\]
\[
k_0=17/50,\quad k_1=39/100,\quad 0<\varepsilon\le1/200,
\qquad C(k)=5/6+3k^2/4.
\]
Write bidder 1's report as \(w=(\rho,t)\) and bidder 2's as \(v=(y,x)\). Define the closed sets
\[
W=\{q+k_0\le t\le q+k_1,\ 0\le\rho\le b-t\},
\]
\[
E_\varepsilon=\{k_0-\varepsilon\le x\le k_1,
\quad y\ge C(x-\varepsilon)-x\}\cap[0,1]^2.
\]
For bidder 1, add the same fee \(\varepsilon\mathbf1_{E_\varepsilon}(v)\) to every nonempty option of its old conditional menu. If its old maximal utility is at most that fee, choose empty; otherwise keep its old selected option and charge the extra fee. The null option remains zero.

For bidder 2, keep its complete old conditional menu outside \(W\). On \(W\), replace it by the deterministic menu, in physical-item order,
\[
(p_\varnothing,p_{\{1\}},p_{\{2\}},p_{\{1,2\}})
=(0,C(k)-k,2/3,C(k)),\qquad k=t-q-\varepsilon.
\]
Choose the first utility maximizer in the order empty, item 1, item 2, bundle. In particular, the safe item 1 wins its tie with the bundle.

These are complete rules on the original continuous report domain. The target and support are closed, not defined only almost everywhere.

The numerical range supplies the sufficient inequalities
\[
k_0-2\varepsilon>0,\quad k_0-\varepsilon>c,\quad
C(k_0-\varepsilon)>b,\quad q+k_1<a.
\]
These conditions, rather than the particular decimal endpoints, explain the local validity range.

## 2. DSIC/IR and outside continuation

Each of bidder 1's fees depends only on its opponent report \(v\), so its menu remains self-bid independent. Adding a common fee to all nonempty options preserves their utility ordering. The prescribed choice is therefore a menu maximizer, including the zero-utility boundary. It receives either its old allocation or nothing. This proves bidder 1's full DSIC/IR and allocation containment in its old allocation.

Bidder 2's replacement depends only on \(w\) and uses utility maximization from a menu with a free null option; its full DSIC/IR follows immediately. A jump in its menu as \(w\) crosses \(\partial W\) is permissible because \(w\) is an opponent report for bidder 2. Outside \(W\), its old allocation is feasible with bidder 1's contracted allocation.

This use of a common fee does not confine the **joint** final allocation to the old shared outcome: bidder 2 can acquire an item actually released by bidder 1.

## 3. All-report joint feasibility inside W

The target \(W\) lies in the already certified region \(Q\). Bidder 1's smaller coordinate is less than \(d\), and \(\rho+t\le b\); its old allocation is either empty or item 2. This includes the sum-equals-\(b\) boundary: a zero-utility bundle is rejected. Hence item 1 is always free for bidder 2, before and after the fee.

For a singleton-2 choice by bidder 2, its value \(x\) is at least \(2/3>t\). The old base threshold excludes bidder 1 from item 2, so there is no conflict. Empty and singleton-1 choices are also safe.

It remains to consider a bundle maximizer. Put \(k_{\rm old}=t-q\), \(k=k_{\rm old}-\varepsilon\). Utility maximization gives
\[
x\ge k,\qquad x+y\ge C(k).
\]
For \(y\le d\), the old base price of item 2 for bidder 1 is at least \(a>t\), so it cannot hold item 2. For \(y>d\), the base price is at least \(x+q\); if \(x\ge k_{\rm old}\), this again excludes bidder 1. These exclusion statements also apply to V3 because its allocation is contained in the shared base allocation, with empty selected at zero utility.

Thus any possible conflict is confined to
\[
y>d,\qquad k\le x<k_{\rm old}.
\]
It follows that \(x\in[k_0-\varepsilon,k_1]\). Moreover,
\[
0<x-\varepsilon\le k,
\quad C(x-\varepsilon)\le C(k),
\quad y\ge C(k)-x\ge C(x-\varepsilon)-x.
\]
The relevant report lies in \(E_\varepsilon\), including the equality cases.

We must also bound the old **final** payment, not merely a base payment. On this possible-conflict set, \(x>c\), \(y>d\), and
\[
x+y\ge C(k)>b.
\]
Consequently the joined V3 menu branch is absent. If \(y\le a\), its branch would require \(x+y\le b\); if \(y>a\), it would require \(x\le c\). Both fail. The base pivot is \(x+y-b\), and its item-2 price is exactly \(x+q\). The remaining baseline menu modifications here are a nonnegative common bundle-region fee; they can only raise that price.

Therefore bidder 1's old utility, if it receives item 2, is at most
\[
t-(x+q)\le\varepsilon.
\]
The added fee makes the prescribed bidder-1 choice empty. This proves capacity at every report in \(W\). In particular, the support inequality and the empty-at-fee-equality convention cover all new bundle ties. No sampled or almost-everywhere repair is used.

## 4. Exact residual on the top edge

At \(y=1\), the frozen bidder-1 threshold is \(d\) for \(x\le c\), and \(x+q\) for \(x>c\); there are no bundle-region surcharges because the opponent sum exceeds one. Since \(t\ge q+k_0>d\), the low-\(x\) part is occupied by bidder 1.

For \(x<k\), any added fee is at most \(\varepsilon\), and \(x+q+\varepsilon<t\). Bidder 1 therefore still receives item 2. For \(k\le x<k_{\rm old}\), the support covers \((1,x)\) and the added fee gives a price at least \(t\); bidder 1 chooses empty, including at equality. For \(x\ge k_{\rm old}\), the original allocation was already empty and the fee cannot create an allocation.

Thus the actual new residual satisfies exactly
\[
r_2^{\rm scarce}(x,1)=\begin{cases}0,&x<k,\\1,&x\ge k.\end{cases}
\]
Also, the scarce item has full residual capacity whenever \(x>2/3\), and the safe item has full residual capacity everywhere on the target fibers.

## 5. Full inner certificate transfers to the actual new residual

The V3.1 gap identity is valid for every randomized DSIC/IR competitor and every residual capacity; its parameters here are \(A=2/3\) and \(k=t-q-\varepsilon\). This lies within its admitted parameter range. The new deterministic menu is feasible by Section 3.

Its utility vanishes on the certificate's no-sale region. On the support of the certificate's scarce-item interior density, \(x>A\), actual residual is one and the menu uses it. On the certificate's singular top-edge support, the actual residual is the exact threshold just established, matching the menu almost everywhere in the one-dimensional trace measure. On the safe-item interior density, residual is one and the menu allocates that item. Therefore all terms in the global gap identity vanish.

Hence the new menu attains the supremum over the **full randomized DSIC/IR inner class** for each \(w\in W\), at the actual modified bidder-1 allocation. This is stronger than stationarity in a three-price family. It supplies no inner-optimality assertion for the altered residual outside \(W\), where bidder 2 has deliberately been left unchanged.

## 6. Strict genuine transfer and its revenue scope

For any admitted \(\varepsilon>0\), a strict witness is
\[
w=(1/100,q+73/200),\qquad v=(1,73/200-\varepsilon/2).
\]
The old bidder 1 receives item 2 with utility \(\varepsilon/2\), while old bidder 2 receives item 1. The fee makes bidder 1 empty, and the new inner menu makes bidder 2 strictly prefer the bundle. Thus the ownership changes from \((2,1)\) to \((0,3)\).

For a positive-volume version, use
\[
\rho\in[.005,.015],\quad k_{\rm old}\in[.36,.37],\quad
y\in[.995,1],\quad
x\in[k_{\rm old}-3\varepsilon/4,k_{\rm old}-\varepsilon/4].
\]
All old/new choices above are strict throughout this correlated closed region. Its four-dimensional volume is \(\varepsilon/4{,}000{,}000>0\). The two \(x\)-bounds move with \(t=q+k_{\rm old}\); this is a polytope, not an independent-coordinate box.

The global fee also changes bidder 1's revenue and participation at reports outside \(W\). An inner gain on \(W\) alone cannot establish an auction gain. The net revenue must include the full fee-support contribution and the replacement contribution, with their overlap counted correctly. Nothing in this audit assigns a positive sign to that total.

`verifier/localized_trial_independent.py` is an independent exact evaluator for bounded top-edge, tie, witness and outside-continuation checks. Its finite checks supplement the all-real menu and certificate proofs above; they do not replace them.
