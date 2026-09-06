# BASE-1: actual strongest archived explicit mechanism

The ticket is resolved. The named archive supplies an actual deterministic auction with exact revenue

`L=83962078694672281756033/96000000000000000000000`.

It is a layered taxation mechanism. It is not just a lower integration estimate and is not restricted to a common convex potential. The V3 reconstruction is self-contained: `certificate/baseline_mechanism.json` contains all 20 common rows, 41 bundle-pivot rows, eight item rows, endpoint conventions, exact component revenues, and SHA-256 bindings to 12 named source files. `verifier/baseline_mechanism.py` evaluates the allocation and payments using only that V3 JSON. No earlier root file or archive file was modified.

## 1. Source identity and retrieval scope

Only the BASE-1 ticket, the archive README, and its named lower-construction/proof/certificate files were read. The principal sources are:

- `research/closed/two-bidder-two-item-dsic-certificates/README.md`;
- `manuscript/manuscript.tex`, sections on the affine base, entry surcharge, and exact revenue;
- `certificate/ama_lower_bound/README.md`, its named manifest and verifier;
- the README and manifest in `piecewise_surcharge_twenty_band_lower_bound`, `piecewise_surcharge_bundle_pivot_lower_bound`, and `refined_item_containment_bundle_pivot_lower_bound`;
- the active named `verify_final_combined.py`.

The current common, bundle, and base manifest hashes were compared against the active predecessor bindings; the base verifier hash also matches its recorded binding. The twelve exact source paths and current hashes are embedded in the V3 JSON. No discovery archive, broad literature audit, upper-proof implementation, or unnamed predecessor was opened. The source's external GemNet figure is not reconstructed here; L is the strongest explicit exact lower mechanism named in this ticket.

## 2. Base mechanism and global normalization

Write the report profile as `(x,y,z,w)`. Let

`a=159/250`, `b=91/100`, `sigma=1137/1000`,

`c=b-a=137/500`, `d=sigma-a=501/1000`, `e=sigma-b=227/1000`.

The nine base outcomes are ordered as follows. A mask is 0 for empty, 1 for item 1, 2 for item 2, and 3 for both items.

| id | bidder masks | score |
|---:|---|---|
| 0 | (0,0) | 0 |
| 1 | (1,0) | x-a |
| 2 | (2,0) | y-a |
| 3 | (3,0) | x+y-b |
| 4 | (0,1) | z-a |
| 5 | (0,2) | w-a |
| 6 | (0,3) | z+w-b |
| 7 | (1,2) | x+w-sigma |
| 8 | (2,1) | y+z-sigma |

Choose the smallest-id score maximizer, and call its two bundles `S_i^0`. For opponent report `q=(q1,q2)`, put

`H(q)=max(0,q1-a,q2-a,q1+q2-b)`.

The base taxation prices for empty, item 1, item 2, and both are

`(0,A0,B0,C0)`,

`A0=H+min(a,sigma-q2)`,

`B0=H+min(a,sigma-q1)`,

`C0=H+b`.

Equivalently, if the chosen base outcome has cost cA, its payments are `p_i^0=H(q)-V_{-i}(A)+cA`. Both descriptions agree on the selected outcome, including ties.

Every nonempty price is at least `sigma-1=137/1000>0`. Thus the zero-type normalization is exact for every opponent report: `u_i(0,q)=p_i(0,q)=0`. At the equal-scale instance these prices are the actual payments; there is no hidden additive utility constant or expected-payment-only normalization.

The base menu is strictly subadditive everywhere, including where its bundle price exceeds one. Let `m1=min(a,sigma-q2)` and `m2=min(a,sigma-q1)`. If both q coordinates are at most d, then `A0+B0-C0>=2a-b=181/500`. If exactly one exceeds d, use `H>=q_high-a` to obtain a lower bound `sigma-b=e`. If both exceed d, use `H>=q1+q2-b` to obtain `2e`. Consequently

`A0+B0-C0>=e=227/1000>0`

on the entire opponent square. Also `A0,B0<C0` because `a<b`.

## 3. Exact opponent-dependent tariffs

Let `t=max(q1,q2)`, `rho=min(q1,q2)`. The complete frozen rational rows are in the V3 JSON; no external table is needed at runtime.

First test the 20 common rows in their listed order. Both ends of every high-coordinate interval are closed. A Z row also requires `0<=rho<=b-t`; an S row requires `0<=rho<=c`. The first matching row supplies f. These supports have t between 53/100 and 71/100.

If none matches, set `u=t+rho` and first test

`b<=u<=1`, `c<=rho<=u-d`.

Only inside this region compute `r=(rho-c)/(u-c-d)`. Its denominator is at least `27/200>0`. Test the 41 positive bundle-pivot rows in listed order, with closed u and r intervals. The first match supplies f; all unlisted cells give f=0. All S/Z rows have priority over bundle rows, including on `rho=c` and `u=b`.

This common fee is added to all three nonempty prices, leaving the empty option at zero.

Finally, only if the first common row was S5.1 or S5.2, test the eight corresponding item rows. Each high-coordinate interval is left-open and right-closed. Add its delta to the singleton corresponding to the opponent's low coordinate and to the bundle; leave the other singleton unchanged. The low coordinate is unique on these rows. At `t=139/200` the predecessor S4.2 row wins and no item surcharge applies; at `t=281/400` the selected item row is I1.4.

In low-coordinate-first orientation, the item row changes

`(A,B,C)=(d+f,t+f,t+c+f)`

to

`(A+delta,B,C+delta)`.

The row tables verify `0<delta<d-c+f`. This is a sufficient deletion margin; it is not the full set of permissible DSIC variations.

The stronger general argument does not require this archived margin. For any subadditive base menu, nonnegative increments `(alpha,beta,gamma)` with `gamma>=max(alpha,beta)` admit a maximizing subset of every originally selected mask. For an old singleton 1, `v2<=C0-A0<=B0`, so singleton 2 remains nonpositive; the bundle's advantage over singleton 1 cannot increase because `gamma>=alpha`. The other singleton is symmetric; old bundles allow all subsets and old empty types can remain empty. The archived changes and the V3 joined changes satisfy this condition for every nonnegative selective surcharge. Thus the archived strict delta bound is optional sufficient evidence, not an additional hypothesis of the general contraction lemma.

## 4. All-report allocation and tie rules

The prices alone are not permission to break bidder ties independently. Both bidders first project their bundles from the same global smallest-id base maximizer.

For the common-fee menu, preserve that base bundle if its new utility is strictly positive. If the maximum utility is zero, choose empty, even where f=0. Raising all nonempty prices by f preserves their ranking, so these rules always choose a menu maximizer.

For the final item menu, choose empty at maximum utility zero. At positive utility, retain the common predecessor bundle whenever it remains maximizing. Otherwise choose the smallest-id maximizing itemwise subset of that predecessor bundle. Within each bidder, the inherited bundle order is empty, item 1, item 2, bundle.

Charge the selected final menu price. This defines allocation and payment at every profile, including all row overlaps, item endpoints, menu indifferences, equal opponent coordinates, and zero-utility cases. The global outcome priority need not preserve bidder or item symmetry at ties; those tie sets have measure zero for revenue integration.

## 5. Full pointwise proof and binding IC structure

For each fixed opponent report, truthful reporting selects a maximizer from one fixed four-option taxation menu. A misreport can select only another available option and cannot produce greater true utility. The empty option proves pointwise IR. This proves full DSIC against all own-type reports; it is not a finite-grid IC check.

Common fees leave a bidder's base bundle unchanged or delete it. For an item row, write `g=A+B-C=d-c+f>0`. If the predecessor chose the changed singleton, its preference over empty gives the corresponding value at least A, and its preference over the bundle bounds the other value by C-A. Its utility lead over the other singleton is at least g. Since `delta<g`, it cannot switch across items. Its ranking against the bundle is unchanged because both prices rise by delta. An unchanged-singleton buyer stays there; a bundle buyer can move only to a subset; an empty buyer cannot enter. The declared tie retention makes each statement pointwise. Hence each final bundle is a subset of its base bundle, and the two final bundles remain disjoint for every profile.

For a fixed final menu `(0,A,B,C)`, the potentially exposed binding IC equalities are

| adjacent options | equality |
|---|---|
| empty / item 1 | x1=A |
| empty / item 2 | x2=B |
| empty / bundle | x1+x2=C |
| item 1 / bundle | x2=C-A |
| item 2 / bundle | x1=C-B |

Each equality is binding only where both options maximize and the facet lies in the type square. Item 1 and item 2 cannot both maximize: at their positive or zero utility tie the bundle gives strictly greater utility because `A+B-C>0`. The common fee increases this discount margin; the item-plus-bundle change preserves it.

There is also a continuum of binding IC constraints inside every demand cell: between any two own reports assigned the same bundle, the price is identical and both directed DSIC inequalities hold with equality. Capacity is binding on each allocated item and slack where the base or deletion stages withhold it. Opponent-row jumps impose no direct cross-opponent DSIC inequality, but simultaneous capacity and the coupled tie rule still matter.

The archived item ceilings `C+delta<=1` bind at the upper endpoints of I1.4, I2.2, and I2.4. All strict deletion margins remain positive, with minimum `2161/10000`. These are different statements: the ceiling is an integration-chamber condition, not a necessary DSIC/IR/capacity inequality. The base mechanism already has C>1 on other opponent regions. Neither these caps nor the archived delta bounds should be imposed on the full V3 admissible-variation class.

## 6. A strict interior obstruction to a common convex potential

Consider the entirely interior profiles

`v=(321/500,1/100,539/1000,1/100)`,

`v'=(643/1000,1/100,541/1000,1/100)`.

At v, bidder 1 faces Z1.1 with fee `233/50000`, receives item 1, and pays `32033/50000`. Bidder 2 receives nothing and pays zero. At v', bidder 1 faces Z1.2 with fee `807/100000`; its item-1 price is `64407/100000`, above its value `643/1000`, and both bidders receive nothing and pay zero.

Thus, for the joint four-coordinate allocation vector X,

`(X(v')-X(v)) dot (v'-v)=-1/1000<0`.

A convex function's subgradients satisfy the opposite weak inequality. Therefore this allocation is not the gradient or subgradient selection of a common convex potential. If the bidder blocks are multiplied by arbitrary positive constants alpha1 and alpha2, the pairing is `-alpha1/1000<0`, so constant positive affine-maximizer weights cannot repair it. This is not a DSIC violation: the comparison changes the opponent report as well as the bidder's own report. DSIC requires own-report incentive comparisons with the opponent fixed.

The same exact witness also works with the two low coordinates set to zero. Both versions are checked by the evaluator, so the obstruction is not a boundary-only artifact.

## 7. Exact revenue replay and independent base calculation

The source decomposes the exact revenue as follows:

| component | exact revenue or increment |
|---|---|
| affine base | 26232089810531183/30000000000000000 |
| Z common rows | 113291698497241117/1000000000000000000000 |
| S common rows | 2400553481931223/31250000000000000000 |
| bundle-pivot rows | 70946101529751/10240000000000000000 |
| item rows | 3963982653557301/800000000000000000000 |

For replacement of the S part, the exact archived amount to subtract is

`G_S+G_I=327090758954983049/4000000000000000000000`.

The JSON exposes this directly as `expected.S_common_plus_item`.

The V3 replay imports no archived implementation. It independently recomputes the affine-base revenue as follows. Set `x=a,t=c,h=d`, `q=x-t`. At h=t, all two-item outcomes have cost x+t; the common score is a four-option menu in the two itemwise maximum values, whose independent marginal CDFs are m squared. Direct integration gives

`H=t(1-x)^2+(1-t)^2(1-x)+q^3/6`,

`I_top=5/3-(x+t)+t^3/3`,

`I4=4t^2(1/3-x/2+x^3/6)+(4/3)(1-t^3)(1-t^2)`

`   -(x+t)(1-t^2)^2+(2/3)t^2q^3+tq^4/3+q^5/30`.

For the continuation from t to h, set `ell=1-eta`, `delta=x-eta`,

`M=ell^2/2+t*ell`, `T=t^2*delta^2/2+t*delta^3/3+delta^4/24`.

The split-event probability is `2(M^2-T)` and its top-face probability is `(ell+t)M`. The revenue derivative is `12(M^2-T)-4(ell+t)M`. Therefore the base revenue is

`4 I_top-6 I4+2 H + integral_t^h [12(M^2-T)-4(ell+t)M] deta`.

This quartic integral is evaluated exactly and matches the archived base fraction. It is a new V3 analytic replay of the base value, separate from the archive's single four-polytope verifier; the archived verifier itself was not executed.

For the added layers, the conditional menu revenue on the checked regime is

`R(A,B,C)=A(1-A)(C-A)+B(1-B)(C-B)`

`         +C[(1-C+B)(1-C+A)-(A+B-C)^2/2]`.

Every row's price inequalities are checked on its closure. Affine endpoint checks cover common/item intervals, and multi-affine corner checks cover bundle rectangles. The common integrands have degree at most four; the item integrands degree at most three; the bundle integrand after multiplying by the Jacobian has degrees at most four in u and three in r. Exact Boole integration therefore computes all row gains without numerical quadrature error. Its rational evaluations are an integration identity for known polynomial degrees, not a type-grid approximation.

The row formulas are integrated with their own polynomial extension to endpoints. The actual first-match tariffs can differ at shared endpoints, which have measure zero. Pointwise behavior is separately handled by the literal evaluator. All 69 individual row values, their sums, the full L, exact cap/deletion margins, normalization cases, overlap rules, and the common-potential obstruction pass the V3 replay.

## 8. Artifacts and limits

- `certificate/baseline_mechanism.json`: complete frozen tables, component values, source identities.
- `certificate/baseline_structure.json`: normalization, binding IC formulas, cap distinctions, and the strict interior obstruction.
- `verifier/baseline_mechanism.py`: exact all-report allocation and payment evaluator.
- `verifier/baseline_replay.py`: independent rational base and full layer revenue replay, with targeted boundary checks.

Run `python -B -X utf8 verifier/baseline_replay.py` from V3. It prints results and writes no files; it rejects `-O`. The mathematical taxation/deletion proof covers all reports; the finite boundary checks only audit the implementation. L remains a feasible primal value, not a global optimality certificate. No claim is made that deletion-only changes, the archived partition, or any finite menu family exhausts admissible V3 mechanisms.
