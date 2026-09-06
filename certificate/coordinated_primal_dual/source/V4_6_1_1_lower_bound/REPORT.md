# V4.6.1.1: a larger exchange deformation with reserve and menu changes

The selected mechanism increases the certified lower bound to

\[
\boxed{
R=\frac{35791404252341621852527735747861637}
{42525000000000000000000000000000000}
+\frac{31}{1215}\sqrt2
-\frac{15059524650320123}{8305664062500000000000}\sqrt{493894}.
}
\tag{1}
\]

Exact rational enclosures give

\[
0.876464164471798049944906113027<R<
0.876464164471798049944906113028
\]

and, relative to the preserved V4.6.1 mechanism,

\[
0.000008550635472197798753464735<\Delta R<
0.000008550635472197798753464736.
\tag{2}
\]

Thus \(\mathrm{OPT}\ge R\), with strict gain greater than
\(17/2000000\). This is a modest numerical improvement, accompanied by
a new allocation pattern and broader exact conditional screening
certificates. It does not close the unrestricted auction gap. No global
matching capacity-price or incentive-flow certificate is claimed.

The formal model remains two additive bidders and two items with four
independent uniform coordinates on [0,1]. DSIC, IR and capacity
feasibility hold for every report, with expected utility over internal
randomness. No restriction on the optimizer's menus or allocation range
is inferred from this particular construction.

## 1. What changed and why

The former small exchange perturbation is replaced by a monotone threshold
with an upward jump. Its generalized inverse consequently has a plateau:
an interval of opponent high reports now induces the same scarce-item
upgrade threshold. This changes entire conditional menus on a region of
positive measure. The base reserve a and discount c are re-optimized jointly with this
threshold; d remains 1/2. A previously uncapped safe singleton price is
capped at 2/3.

The jump has an exact integrated revenue effect. In the fixed-constant
discovery family, the total change takes the form

\[
\int_c^V [\mathsf A(x)g(x)-\mathsf B(x)g(x)^2]\,dx.
\tag{3}
\]

Both bidders' full conditional revenue changes are included before this
one-dimensional kernel is formed. In particular, the inverse plateau
contributes positive measure in the original opponent coordinate. It
cannot be discarded because it is a single point in inverse coordinates.
The polynomial derivation and its restricted analytic maximizer are in
[the functional-exchange note](research_log/functional_jump.md).

The safe-price cap is forced by a profitable complete-menu variation
where the uncapped price exceeds A=2/3. For scarce price A and bundle
price C, the proper-menu revenue obeys

\[
\partial_B\mathscr R(A,B,C)=(2-3B)(C-B).
\]

If the uncapped safe price is C-k=A+\eta>A, replacing it by A gains

\[
\frac32k\eta^2+\frac12\eta^3>0.
\tag{4}
\]

This calculation integrates all own reports that change menu choice.
The joint feasibility proof below verifies that the cap can be made
throughout its conditional region. It also repairs a sign obstruction in
the full conditional screening certificate.

The reserve can rise above A while preserving E/Q compatibility. With
the E menu retained, a sufficient exact allowance is
\(a-A\le q^2/2\). The selected candidate uses equality. This is a proved
compatibility allowance, not a theorem that the unrestricted optimizer
must satisfy or bind this inequality.

## 2. Complete pointwise definition

Set

\[
A=\frac23,\quad d=\frac12,\quad c=\frac{157}{500},\quad
q=d-c=\frac{93}{500},\quad \nu=\frac{q^2}{2},
\]
\[
a=A+\nu=\frac{1025947}{1500000},\quad
b=a+c=\frac{1496947}{1500000},\quad
s=a+d=\frac{1775947}{1500000},
\]
\[
\lambda=\frac45,\quad u=\frac{3421}{10000},\quad
b_0=\frac{4-\sqrt2}{3},\quad T=1-\frac{2c}{3},\quad U=\frac53-2c.
\]

The endpoint u here is a parameter, not the bidder utility. Define

\[
g(x)=\begin{cases}\lambda(u-x),&c\le x\le u,\\0,&\text{otherwise},\end{cases}
\qquad h(x)=x+q+g(x).
\tag{5}
\]

The interval is **closed at c**: \(g(c)=281/12500\).
The right-continuous increasing threshold h has slopes 1, 1/5 and 1,
and an upward jump at c. Its generalized inverse for the needed reports is

\[
k(t)=\begin{cases}
t-q,&t\le d,\\
c,&d<t\le d+281/12500,\\
(t-q-\lambda u)/(1-\lambda),&d+281/12500<t<u+q,\\
t-q,&t\ge u+q.
\end{cases}
\tag{6}
\]

Both bidders receive the following menu as a function of the opponent's
report \(w\). Write \(t=\max(w),\rho=\min(w),z=w_1+w_2\).
In an oriented menu, the **scarce** item is the opponent's high-valued
physical item; the **safe** item is the other one. If an orientation tie
is needed, item 2 is designated high. Such a tie never carries a positive
base fee and never occurs in constrained Q or E.

**Closed Q region:** \(t\le A,z\le b\).
If \(t\le d\), offer empty at zero, each singleton at A, and the bundle
at \(\max(b_0,z)\). If \(t>d\), put

\[
C_0(k)=\frac56+\frac34k^2,\qquad
C=\max\{C_0(k(t)),z,k(t)+h(\rho)\},\qquad
B=\min\{A,C-k(t)\}.
\tag{7}
\]

Offer empty at zero, safe at B, scarce at A, and bundle at C.

**Open E region:** \(A<t<T,\rho<c\).
Set

\[
\delta=\frac9{16}(T-t)(U-t),\quad \alpha=3t-2,\quad
\beta=\frac{\alpha}{\alpha+2\delta}.
\]

Offer empty; safe at \(d+\delta\); scarce at t; bundle at
\(t+c+\delta\); and a lottery giving scarce surely and safe with
probability \(\beta\), at payment \(t+\beta c\).

**Every other opponent report:** let

\[
H=\max(0,w_1-a,w_2-a,z-b),\quad
P_j=H+\min(a,s-w_{3-j}),\quad P_B=H+b.
\tag{8}
\]

Offer empty, both singletons and bundle at these prices, adding
\(g(\rho)\) to the safe singleton and bundle. On retained base rows,
the face \(\rho=c\) uses the positive fee in (5); all boundaries
excluded from E are covered by Q or this base rule.

**Joint selection and ties:** form each full menu's utility-maximizing
options at the reported type. At zero maximum utility retain empty only.
At positive maximum utility retain every maximizer. Select the first
jointly feasible pair in lexicographic order, bidder 1 then bidder 2.
The menu orders are empty/item1/item2/bundle for free Q and base;
empty/safe/scarce/bundle for constrained Q; and
empty/safe/scarce/bundle/lottery for E. A jointly feasible maximizing pair
always exists, as proved in the next section. This rule applies on every
face and tie, not just almost everywhere.

These formulas specify the mechanism for all real reports. The exact
rational-report implementation, with algebraic comparison for b0, is
[refined_candidate.py](verifier/refined_candidate.py).

## 3. Feasibility, incentives and a new ownership pattern

The [complete structural proof](research_log/refined_structure_audit.md)
covers base/base, Q/base, Q/Q, E/base, E/Q and E/E pairs. Three checks
matter particularly for the changed parameters.

First, throughout Q the extra bound \(k+h(\rho)\) in (7) is redundant.
On the fee support the least sufficient slack is exactly

\[
[C_0(A-q)-(A-q)]-h(b-A)=\frac{37}{5000000}>0.
\tag{9}
\]

Outside that support, z supplies the bound. Thus the actual C is
\(\max(C_0(k),z)\) everywhere. The proof does not assume C<1:
C0(k) can exceed 1 near t=A. The inverse implications used at the jump
are \(x<k(t)\Rightarrow h(x)<t\) and
\(x\ge k(t)\Rightarrow h(x)\ge t\), rather than the false plateau
identity \(h(k(t))=t\).

Second, the base fee admits a maximizing subset of each old base
maximizer because the original tariffs satisfy the strict discount
\(P_{\rm scarce}+P_{\rm safe}-P_B\ge q>0\). This rules out a switch
from an old safe winner to a positive scarce winner. This argument is
used only for base compatibility; the complete new mechanism is not
contained in the predecessor allocation.

Third, for E/Q compatibility, a Q type's E-lottery utility is at most
\(A-t+\beta(a-A)\). The ratio

\[
\frac{t-A}{\beta}=t-A+\frac{2\delta(t)}3
\]

is strictly increasing on the open E interval with infimum \(q^2/2\).
The selected allowance therefore gives strict exclusion even at
\(a-A=q^2/2\). The remaining bundle and singleton comparisons, including
the capped Q upgrade, are proved in the structural note.

Every selected option maximizes the same fixed menu when the opponent's
report is fixed. Any deviation selects another menu option, proving full
pointwise DSIC. Empty proves IR. Borel formulas and finite selection
prove measurability. Nonnegative IR payments are at most 2, so they are
integrable. For each item, disjoint intervals of lengths \(x_{1j},x_{2j}\)
under a uniform random seed implement a samplewise feasible allocation.
Truthfulness is in expected utility, as in the formal model; universal
truthfulness of individual seeds is not asserted.

There is a strict ownership change at

\[
(v_1,v_2)=((103/200,1/10),(63/200,99/100)).
\]

V4.6.1 splits the goods: bidder 1 gets item 1 and bidder 2 gets item 2.
The new mechanism gives bidder 1 nothing and bidder 2 the bundle.
The same change holds throughout the four-dimensional open box of
radius 1/100000 around this profile. The scalar checks in the verifier
keep the first high report strictly inside the inverse plateau, the
second low report above c and below the old fee support, and give
\(h_{\rm old}(x)<t<h_{\rm new}(x)\) throughout the box. All relevant
positive menu-choice comparisons stay strict. The 16 corner checks
supplement these uniform inequalities; corners alone are not a
continuum proof. This is a positive-volume joint reallocation.

## 4. Exact revenue, independently recomputed

[The independent derivation](research_log/refined_revenue_audit.md)
integrates every conditional menu over the continuous own-type square
and then the entire opponent square. It accounts for nine base polygons,
free Q, all three inverse branches of constrained Q, capped Q prices,
the E lottery, and both base-fee strips. Boundary ties have zero measure
in each nondegenerate conditional menu and do not change these integrals.
The pointwise selection proof still covers them.

Two terms absent when a=A must be included: the negative correction
between the old base menu and the E menu for A<t<a; and the base-fee
strip \(c\le\rho\le b-A,\ A<t<b-\rho\). Omitting the first would
overstate revenue. Both calculations include both terms.

The root calculation uses rational polynomial dictionaries and simplex
moments; the independent calculation uses a separate direct Q decomposition
and Green boundary integrals for base polygons. Their three algebraic
coefficients agree exactly after
\(\sqrt{246947/1125000}=\sqrt{493894}/1500\).
Forty-five additional exact conditional-menu polygon integrations agree
with the relevant formulas. The finite checks supplement the all-real
integration, which yields (1).

For orientation, the same new constants with the identity exchange and
the Q cap have revenue
\(0.876456114094298659192840710249\ldots\).
The final functional change adds exactly

\[
\frac{12679344561540434503009375151}
{1575000000000000000000000000000000}.
\]

This is already included in (1). The earlier fixed-constant analytic
family, reserve-only examples and cap experiments are alternatives,
not additional revenue increments. Floating parameter searches are
discovery records, not proofs of parameter optimality.

## 5. Conditional gaps and what remains

The [conditional revenue-gap map](research_log/conditional_gap_map.md)
now certifies full randomized conditional optimality, for either bidder
under the actual opposite allocation, on three disjoint opponent regions:

| Region | Opponent reports | Exact area |
|---|---|---:|
| Q | max(w)<=A, sum(w)<=b | 1746937679191/4500000000000 |
| E | A<max(w)<T, min(w)<c | 4867/62500 |
| W | max(w)>=1-q, sum(w)>=1+u | 438867/2500000 |

Their union has area
\(2887322279191/4500000000000\), approximately **64.1627%** of the
opponent-report square. This is not the fraction of the auction's
global revenue gap closed. It is a map of conditional subproblems for
which replacing one bidder's menu alone cannot improve revenue.

The Q certificate uses the capped singleton price and the verified
actual top and anchor capacity constraints. The E certificate requires
an incentive argument at its junction: literal residual scarcity on the
face (x,c) can fail when a>A, but the zero-capacity open rectangle
below it forces a competitor's utility to be horizontally constant.
Continuity and both horizontal deviations force the selected scarce
marginal to vanish on the needed face. The inherited line-flow term
therefore vanishes by DSIC, not by a false physical-capacity assertion.

The [new W certificate](research_log/residual_wing_screening.md) uses
the same principle over a larger region. With
\(p=\min(\rho+q,1), k=z-p\), the conditional menu reduces to safe at p
and bundle at z. Scarce-item occupation in a strip and the no-sale
interior, together with safe-item occupation on a left-edge trace,
force all competitors' utility to be constant in the no-sale region.
An exact nonnegative revenue identity then bounds the full randomized
screening class and is attained by the candidate. Its uniform sign
margin is \(18601/5000000>0\).

These identities do not require a finite menu for competitors. They
are certificates at the candidate's actual residual capacity; they do
not by themselves support arbitrary residual-capacity perturbations.
In particular, they do not furnish a common global auction dual.

The remaining opponent area
\(1612677720809/4500000000000\), about 35.84%, is unresolved. It is
not certified to have a positive conditional gap. The useful next
targets are complete-menu screening there and joint reallocations
that change the currently binding residual constraints on Q, E or W.
The present branch establishes a larger feasible lower bound and
eliminates several unprofitable frozen-residual directions; unrestricted
optimality and a matching upper bound remain open.

## 6. Reproducibility and scope

See [VERIFICATION.md](VERIFICATION.md) for actual replay results,
independence boundaries and preserved-file checks. The final exact
ledger is [branch_summary.json](certificate/branch_summary.json).
All new outputs are confined to this version directory. The predecessor
V4.6.1 package is preserved; outer navigation, the outer manifest and
concurrent branches are outside this branch's managed scope.
