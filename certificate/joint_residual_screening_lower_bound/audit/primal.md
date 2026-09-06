# Independent audit of the complete V4.6 primal mechanism

**Verdict: PASS for pointwise feasibility, DSIC, IR, and complete-domain
definition, with the explicitly identified predecessor dependencies below.**
No blocking defect was found in the composition
`outer_lottery_strip -> free_bidder_one -> outer_bundle_exchange ->
outer_bundle_reoptimized -> price_joint_reallocation` at
`epsilon = 9/10000`. This audit does not certify the revenue integral,
conditional optimality measures, or the inherited unrestricted upper bound;
those are separate audit obligations. It does not establish an auction
optimizer or close the remaining gap.

The mathematical conclusion concerns every real report in `[0,1]^4`, not
only rational inputs accepted by the Python evaluator. Allocations are
marginal allocation probabilities; DSIC and pointwise IR use the expected
utility `v dot x - p` in the stated randomized-mechanism model. Each item's
marginals have a feasible joint realization, by assigning at most one
recipient to that item. Universal truthfulness is not asserted.

## Independence and dependencies

I read the actual five V4.6 mechanism wrappers and their written feasibility
arguments, then traced their live predecessor definitions through V4.5
`residual_lottery.py`, V4.02 `split_cost_candidate.py`, V3.1
`constrained_candidate.py`, and V3 `joined_threshold.py` and
`baseline_mechanism.py`. I rederived the inequalities below instead of
treating any stored PASS string as a theorem.

The retained portions depend on the frozen V3 first-match fee table, its
joined-price formulas, and the shared affine-maximizer rule with split cost
`142/125`. The structural justification needed from those definitions is
reconstructed in the next section. I did not separately rederive the old
base revenue or rerun its continuous four-dimensional revenue integration.
The regression shares predecessor `retained_menu` and exact quadratic
scalar arithmetic; its new final-menu assembler does not import the V4.6
menu predicates or menu-construction helpers. This is a distinct composition
check, not a wholly independent implementation of every predecessor.

## 1. The inherited facts actually needed

Write

`a=159/250`, `b=91/100`, `c=b-a=137/500`, `s=142/125`,
`d=s-a=1/2`, `q=s-b=113/500`, and `A=2/3`.

For an opponent report `z`, the shared-base menu is

\[
H=\max(0,z_1-a,z_2-a,z_1+z_2-b),\qquad
P_1=H+\min(a,s-z_2),\quad
P_2=H+\min(a,s-z_1),\quad P_{12}=H+b.
\]

The frozen V3 increment has the form common nonnegative fee `f`, followed
by a nonnegative surcharge `eta` on one singleton and the bundle. Thus
`Delta_12=max(Delta_1,Delta_2)` and both singleton increments are
nonnegative. This is immediate on the literal fee rows. In the joined
square-root branch the increase is common, `C-b>=0`; its quadratic branch
has the common increase plus the safe-item surcharge starting at zero at
the root/quadratic junction. The affine continuation uses its nonnegative
surcharge until its stated zero cutoff. These identities are preserved
when the base split cost changes because the increments are frozen as
opponent functions.

The strict subadditivity inequality is

\[
P_1+P_2-P_{12}\ge s-b=q>0.
\]

It follows by splitting according to whether zero, one, or both opponent
coordinates exceed `d`, and using respectively `H>=0`, `H>=z_j-a`, or
`H>=z_1+z_2-b`. The numerical parameter requirements are `b<s<2a`.
A common fee preserves the selected base allocation or chooses empty. If
a subsequent item-plus-bundle surcharge changes a singleton choice to a
disjoint singleton with nonnegative utility, the original bundle would
have strictly beaten the original singleton by strict subadditivity. This
is impossible. A changed bundle can only become a subset. Therefore the
retained mechanism always has a utility-maximizing subset of the selected
shared affine outcome. The prescribed rule picks such a subset and is
jointly feasible, including shared-allocation ties.

The useful global price bounds are

\[
P_j+\Delta_j\ge d,\qquad P_{12}+\Delta_{12}\ge b,
\qquad (P_{12}+\Delta_{12})-(P_j+\Delta_j)\ge c.
\]

For the first, use `H>=z_other-a` whenever the split term is the minimum;
otherwise the price is at least `a>d`. For the last use
`b-min(a,s-z_other)>=b-a=c` and `Delta_12>=Delta_j`.

The inherited Q replacement is on the closed set
`Q={max(w)<=A, sum(w)<=b}`. For `t=max(w)>d`, the opposing bidder's low
coordinate is at most `b-t<d` and its total is at most `b`; the retained
opponent can only take the high item. In aligned coordinates `(x,y)` its
price is at least `max(a,x,x+y-c)` if `y<=d`, and at least `x+q` if `y>=d`.
The Q menu `(A,C0-k,C0)`, with `k=t-q` and `C0=5/6+3k^2/4`, respects that
hole: a scarce singleton requires `x>=A>=t`; a bundle requires `x>=k`
and `x+y>=C0`; on the remaining low-`y` branch `C0-c>t` for `a<=t<=A`.
The safe-before-bundle tie rule covers `x=k`. For `t<=d` the retained
opponent is empty on the whole Q row, including equality, so the SJA
replacement is feasible. This reconstructs the predecessor property used
by the new splices.

## 2. Enlarged lottery strip: no missing two-sided case

The union of the V4.5 region and the V4.6 added region is exactly

\[
E^+=\{A<t<T,\ 0\le\rho<c\},\qquad
T=613/750,\quad U=839/750,
\]

with `t=max(opponent)` and `rho=min(opponent)`. In particular the old
`sum=b` face is covered by V4.5, while `rho=c`, `t=A`, and `t=T` retain
the predecessor rule. For this open strip

\[
\delta=\frac9{16}(T-t)(U-t)>0,\quad
\alpha=3t-2>0,\quad \beta=\frac{\alpha}{\alpha+2\delta}\in(0,1).
\]

In scarce/safe item order the complete menu is

\[
(0,0;0),\ (0,1;d+\delta),\ (1,0;t),\
(1,1;t+c+\delta),\ (1,\beta;t+\beta c).
\]

The inherited bidder with report `(t,rho)` cannot buy the safe singleton
because `rho<c<d`. It cannot prefer the bundle to the scarce singleton
because the bundle upgrade is at least `c>rho`. Its possible scarce-item
occupation is contained in

\[
\{y\le d,\ x\le t,\ x+y\le t+c\}
\ \cup\ \{y\ge d,\ x\le t-q\}.
\]

On the lower part, the lottery loses to empty when `y>=c` because
`x+beta(y-c)<=x+y-c<=t`, and loses to the scarce singleton when `y<c`.
On the upper part it loses to empty for `y<=d+delta` and to the safe
singleton for `y>=d+delta`. Both statements follow from

\[
\beta(q+\delta)\le q,
\]

which is exactly `delta*(alpha-2q)<=0`; it holds because `t<T`.
Empty, safe singleton and scarce singleton precede the lottery, so equality
does not create an occupation-hole violation. The deterministic bundle
also avoids the hole by its comparisons with empty and the safe singleton.

When both reports lie in Eplus with the same orientation, each low value
is below `c`; only the high singleton can be bought, and only by a bidder
whose high value strictly exceeds the other's. With opposite orientations,
each scarce value is below `c` and only distinct safe singletons can be
bought. This resolves the interaction of the two replacements.

The remaining case is the reverse Q override. If bidder 1's own report
`(x,y)` belongs to Q and its opponent belongs to Eplus, then `x<=A<t` and
`x+y<=b<t+c`. It cannot take the scarce singleton, bundle, or positive
lottery; only the safe singleton is possible. A positive safe choice has
`y>d+delta` and `x<=b-y<y`, so bidder 2's Q scarce direction is physical
item 2. Its own value for that item is `rho<c`, below both its scarce
singleton price and bundle-upgrade threshold `y-q>c+delta`. It cannot
consume the conflicting item. At safe-entry equality bidder 1 is empty.
Thus the Eplus construction is jointly feasible on every real report.

## 3. Closed F splice and G bundle exchange

Let `b0=(4-sqrt(2))/3` and
`F={max(v)<=d, sum(v)<=b0}`. At an own report in F, bidder 2 is empty
against every opponent: retained singleton prices are at least `d` and
bundle prices at least `b`; free-Q prices are `(A,A,b0)`; constrained-Q
singletons exceed `d` and bundles exceed `b0`. In a lottery row, a lottery
that beats its high singleton needs safe value at least `c` and has utility
at most `sum(v)-t-c<0`; below `c` it loses to that singleton. These are
uniform inequalities and include all closed faces by zero-utility empty.

Consequently bidder 1's complete SJA menu `(A,A,b0)` on F has full
residual capacity. There is no assumption that the low item remains free
everywhere on unrelated lottery fibers after this operation; it need not.

On `G={max(v)<=d, b0<sum(v)<b}`, bidder 1's new menu is `(a,a,sum(v))`.
Bidder 2 at a report in G can buy only a Q bundle: other singletons cannot
give positive utility; retained bundles cost at least `b`; a positive
Eplus lottery or bundle needs total value above `t+c>b`.

If bidder 1 buys the new G bundle, `sum(w)>sum(v)` strictly. Bidder 2's
Q bundle price was simultaneously raised to at least `sum(w)`, so it
rejects the bundle. If bidder 1 buys a singleton, its corresponding own
coordinate is strictly above `a`; on Q this forces
`C0(max(w))>=C0(a)>b>sum(v)`, again making bidder 2 empty. Outside Q it
was already empty. For `v` outside G, raising only bidder 2's bundle price
contracts its old allocation, so the unchanged bidder 1 remains compatible.

The irrational face `sum(v)=b0` belongs to F. The upper face `sum(v)=b`
retains the prior bidder-1 rule. These are different complete menus on
different opponent reports, an allowed discontinuity; neither face is
discarded. Positive singleton or bundle purchases in these arguments use
strict inequalities because empty is selected at zero utility.

## 4. Coupled Q response checked against the correct reference

For constrained Q rows with `z=sum(w)>C0(t)`, the final prices are

\[
(A,z-k,z),\qquad k=t-q.
\]

Compare directly with the *pre-exchange* menu `(A,C0-k,C0)`. The safe
singleton and bundle receive the same price increase `z-C0`; the scarce
singleton stays fixed. A previous safe singleton has scarce own value
`x<=k<A`, so it cannot switch to a positive scarce singleton and can only
remain safe or become empty. A previous bundle can only retain or contract
to a subset; a previous scarce singleton or empty is unchanged. The
safe-before-bundle priority handles `x=k`. Thus the result is pointwise
a subset of the original certified Q allocation. It need not be a subset
of the intermediate bundle-only response, and no such false requirement
is used here.

Outside G the original bidder-1 allocation is unchanged. On G both own
coordinates of bidder 2 are at most `d`, while the new Q singleton prices
are strictly larger than `d`. Only its bundle is possible, and the same
strict total-order argument from Section 3 excludes a conflict. At `z=C0`
the prices agree and the previous rule is retained. This covers the entire
coupled response without an unexamined allocation-expansion case.

## 5. Final price cut: independent conflict localization

Use physical orientation `w=(t,rho)` and `v=(x,y)`, with

\[
W=[.7,.71]\times[0,.2],\qquad
S=[.7-4e,.71]\times[c-2e,c+4e],\quad e=9/10000.
\]

The operation cuts only bidder 2's lottery price on W. On bidder 1's
opponent rows in S it adds the same `e` to every nonempty reference option,
keeping empty at zero. This latter menu either retains the old allocation
with payment increased by `e`, or chooses empty when the old maximum
utility is at most `e`. Positive-option ties are retained.

On W, `3/5<beta<3/4`. To check this over the full interval, `delta`
decreases there while `alpha` increases; the endpoint inequalities
`alpha(.7)>3 delta(.7)` and `alpha(.71)<6 delta(.71)` imply both bounds.
Let `Y=c+delta/(1-beta)`. Exact endpoint evaluation also gives
`Y+4e<d`. A newly selected lottery must satisfy

\[
c-e/\beta\le y\le Y+e/(1-\beta),\qquad
x+\beta(y-c)-t+e>0.
\]

These are comparisons with the unchanged scarce singleton, bundle, and
empty. Since `beta*(Y-c)=alpha/2`, they imply

\[
x>1-t/2-e/(1-\beta)>1-t/2-4e>1/2.
\]

Thus the reference F/G splices on bidder 1 are absent in the entire changed
lottery cell. Its low value `rho<=.2<c` precludes safe singleton, bundle
and any opposing Eplus lottery by the upgrade comparisons above. Bidder 1
can only take the scarce singleton. In a retained row with `y<d` its price
is at least `max(a,x,x+y-c)`; in an Eplus row it is exactly `x` with `y<c`.
Hence in all cases

\[
P\ge P_0=\max(x,x+y-c).
\]

If the old bidder-1 choice could conflict, it has `t>P>=P0`. For `y<c`,
comparison of the new lottery with the scarce singleton gives
`c-y<=e/beta<2e`. For `y>=c`, combining `t>x+y-c` with the positive
lottery utility gives `y-c<e/(1-beta)<4e`. Also `x<t<=.71`; the same
inequalities give `x>.7-4e`. Thus **every** conflict is in S. There

\[
t-P\le t-P_0
<x+\beta(y-c)+e-P_0\le e.
\]

The complete entry-fee menu chooses empty. The safe item was already free
at these reports. Unchanged bidder-2 choices retain feasibility because
bidder 1 only contracts. This is a complete all-real proof, including
closed rectangle faces and the retained `y=c` menu. It uses no assumption
that the frozen tariff above `c` is a constant fee: only the verified
nonnegative increments and the lower bound P0 are needed for feasibility.

## 6. DSIC, IR, measurability, and the precise wording correction

For fixed opponent report, every final selected allocation/payment pair
belongs to one fixed complete menu and maximizes truthful utility on that
menu. A misreport can only select another pair from the same menu. Therefore
truth-telling weakly dominates **every** real misreport. This argument is
pointwise, permits lotteries, and does not rely on a finite report grid.
The empty option proves pointwise IR. All accepted payments are bounded
and nonnegative; finite Borel predicates and utility comparisons give a
jointly measurable allocation/payment rule. The finitely many algebraic
and first-match boundary rules explicitly define every exceptional row.

There is one nonblocking overstatement in V4.6 `REPORT.md`: the sentence
"Priority is explicit and independent of the own report" is not literally
true of every inherited retained row. V4.02's retained selection refers to
the shared affine outcome, which depends on both bidders' reports. This is
necessary to coordinate some base ties. It still selects a maximizer of
one fixed opponent-dependent menu, which is sufficient for DSIC.

Recommended archive clarification, without changing the frozen source:

> Every new splice has an explicit fixed tie priority. Retained rows use
> their complete predecessor tie rule, always selecting a maximizer of a
> fixed opponent-dependent menu.

Do not replace the inherited shared-outcome rule by independent
smallest-mask choices: the feasibility proof retains that coordination.

## 7. Fresh exact implementation evidence

Executed on the live source, with assertions enabled and bytecode writes
disabled:

`python -B -X utf8 output/output/two_bidder_two_item_full_dsic_exact_auction/V4_6_archive_audit/primal/check_primal.py`

Result: `INDEPENDENT_PRIMAL_REGRESSION_PASS`.

- 2,939 exact rational profiles, including 421 fee profiles, 620 cut
  profiles, and 251 profiles where both operations apply.
- Exact lottery indifference lines, entry-fee faces, Q transition and
  singleton/bundle ties, global extrema, both item orientations, and
  `+/- 1/10000000` perturbations around selected boundaries.
- 258 opponent reports at literal inherited tariff endpoints, checking
  nonnegative structured increments, singleton and bundle bounds, bundle
  upgrade bounds, and strict shared-base subadditivity.
- Each production allocation/payment is independently checked for membership
  in the directly assembled final menu, maximization, nonnegative utility
  and payment, empty selection at zero utility, and both item capacities.

These bounded checks verify source/formula agreement and attack boundary
handling. They do not replace Sections 1-6 and are not evidence for exact
optimal revenue, attainment, or an unrestricted matching dual.

The V4.6 source and closed archive were not edited by this sub-audit.
Only this audit directory contains its new files.
