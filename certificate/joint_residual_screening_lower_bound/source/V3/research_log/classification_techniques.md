# CLASS-1: local classification techniques with explicit exposure conditions

Status: primary-source retrieval and bounded-domain transfer completed; frozen for independent audit. Only the named original characterization was retrieved. No broad survey, finite type grid, or classification theorem for the unrestricted auction is used.

## 1. Source audit and the exact dependency chain

The identity-locked source is Christodoulou–Koutsoupias–Vidali, ESA 2008, arXiv:0807.3427v1. The local PDF and its hash are recorded in `sources/classification_source_card.md`. The technical source has 20 pages; the author record describes the 11-page conference publication. The relevant chain is Theorem 2, Lemma 1, Corollary 1, and Lemmas 3–10 in Section 3.

The theorem's scheduling domain is all real costs, with deterministic assignment of every task. Each bidder's allocation determines the other's by complementation. Decisiveness means the player can force the specified allocation against any fixed opponent report; global occurrence of an allocation is weaker. Three-outcome decisiveness is also stated as an extension. The classification theorem itself assumes no approximation guarantee. Continuity is not a blanket premise: the argument derives threshold regularity before its Pexider step. The separate makespan approximation results do not transfer to expected auction revenue.

The proof's first isolation explicitly uses arbitrarily large reports. Its later inverse/translation arguments use reachable thresholds, nonzero interaction, and decisive two-sided ranges. A compact value cube supplies none of those facts automatically. Sign reversal from costs to values changes minimization to maximization; it does not enlarge the domain or remove withholding. The paper itself cautions against identifying two independently described slice boundaries without a joint argument. We therefore transfer the following local constructions by giving complete proofs in the bounded auction model.

## 2. Local model and exposure assumptions

Types are `x,y in [0,1]^2`. Allocations are joint matrices; DSIC and IR are pointwise. All statements below concern open regions inside this cube. Boundary selections require their own supporting-vector completion.

Consider four particular joint labels indexed by `a in {00,10,01,11}`:

`A^a_1=a`, `A^a_2=(1,1)-a`.

Thus, within this block, both items are allocated and the labels are complementary. Other global labels, including withholding and fixed lotteries, may exist. Whenever a panel below is called **exposed**, it means that the actual joint rule selects exactly the two stated labels on its two open sides, all tested reports stay in the cube, and other labels do not intervene on that panel. A positive utility margin against all other own-menu rows is one convenient certificate of exposure, but exposure itself is the hypothesis.

Let `Y=I_1 x I_2` be a product of nonempty connected open opponent intervals. Assume that for each `y in Y` the four bidder-1 rows are attained at some own reports. Their bidder-1 prices `p_a(y)` are then well-defined: two reports giving the same row must give the same payment, by the two opposite IC inequalities. Prices can be gauged by subtracting `p_00(y)`.

The additional hypotheses used for rigidity are explicit:

1. For every `y in Y`, each of the four one-item comparisons `00/10`, `01/11`, `00/01`, `10/11` has a persistent regular `C^1` exposed joint interface in the own cube. Its own normal block is nonzero.
2. When the resulting interaction constant is nonzero, the appropriate diagonal comparison is also exposed throughout Y: `00/11` for a bundle discount, or `10/01` for a bundle surcharge.
3. No claim is made about a missing panel, an inactive menu comparison, an isolated junction, or a parameter set having no open product neighborhood.

These are local, checkable replacements for global large-report isolation. They are not consequences of finite range, DSIC, or optimality alone.

## 3. Single-item exposed panels separate payment coordinates

For a regular interface between labels K and L, put `d_i=A_i^K-A_i^L`, and orient its normal n into K. Holding the opponent fixed and adding the two IC inequalities gives

`(a_i(v)-a_i(r)) dot(v-r)>=0`.

Testing transverse directions implies `d_i=c_i*n_i`, `c_i>=0`, whenever `n_i!=0`. If the row changes, its normal block is either zero or a nonnegative multiple of the row jump. If the row does not change, that bidder places no restriction on its normal block.

Apply this to an exposed item-1 transfer, for example `00/10`. The joint row jumps are `e1` and `-e1`. Bidder 1's price comparison places its interface on

`x1=p_10(y)-p_00(y)`.

The exposure and regularity assumptions make this threshold a `C^1` function on Y. The opponent block of the interface normal is minus its y-gradient. Bilateral IC forces its second component to vanish. Consequently

`p_10(y)-p_00(y)=f_1(y1)`.

The other three panels similarly yield

`p_11-p_01=g_1(y1)`,

`p_01-p_00=f_2(y2)`,

`p_11-p_10=g_2(y2)`.

Each exposed scalar threshold is nondecreasing in its own opponent coordinate. A zero derivative is allowed; strict positivity requires an additional transverse opponent block. This local proof uses an actual bounded panel instead of an arbitrarily large isolating report.

## 4. The payment rectangle identity makes interaction constant

Pure price telescoping gives

`g_1(y1)-f_1(y1)=g_2(y2)-f_2(y2)` for every `(y1,y2) in Y`.

The left side depends only on y1 and the right side only on y2. Because Y is a product, both are one constant c. Thus the four prices, after subtraction of `p_00`, are

`p_00=0`, `p_10=f_1(y1)`, `p_01=f_2(y2)`,

`p_11=f_1(y1)+f_2(y2)+c`.

If `c=0`, bidder 1's comparison within this block separates item by item. Away from ties, the local rule is task-independent: item j goes to bidder 1 according to the scalar threshold `xj>f_j(yj)`. The threshold may be nonlinear. The presence of other global labels can still stop this block from being active elsewhere.

If `c<0`, the discount produces a potential `00/11` diagonal, with equation

`x1+x2=f_1(y1)+f_2(y2)+c`.

If `c>0`, the surcharge produces a potential `10/01` diagonal, with equation

`x1-x2=f_1(y1)-f_2(y2)`.

These algebraic equations alone do not establish exposure. Clipping, withholding, or other active rows may remove the diagonal from the available own-type square.

## 5. A bounded Pexider lemma and local affine rigidity

**Bounded Pexider lemma.** Let f and g be continuous on nonempty open intervals I and J. Suppose

`f(u)+g(v)=H(u+v)` for every `(u,v) in I x J`.

Then f and g are affine with the same slope, and H is affine on I+J. Continuity can be replaced by monotonicity or local boundedness of a component.

**Proof.** For a sufficiently small increment d and admissible base points,

`f(u+d)-f(u)=g(v+d)-g(v)`.

The common increment depends only on d, since u and v vary independently over open intervals. These increments are locally additive. Continuity, monotonicity, or local boundedness excludes pathological additive solutions, so the increment equals `alpha*d`. Partition any longer interval difference into sufficiently small increments. This gives `f(u)=alpha*u+beta_1`, `g(v)=alpha*v+beta_2`, and then the displayed equation gives H. QED.

**Local four-label rigidity theorem.** Under the panel hypotheses of Section 2, if `c!=0` and its corresponding diagonal is exposed throughout Y, then

`f_j(yj)=alpha*yj+beta_j`, with one `alpha>=0`.

If the opponent normal block of the diagonal is nonzero, `alpha>0`. Within the active block the rule is consequently a weighted affine maximizer with weights `(1,alpha)` and constants

`gamma_a=beta_1*a1+beta_2*a2+c*a1*a2`.

**Proof.** For `c<0`, the diagonal transfers both items, so its joint row jumps are `(1,1)` and `(-1,-1)`. The bilateral normal constraint forces

`f_1'(y1)=f_2'(y2)>=0` throughout Y.

For `c>0`, the jumps are `(1,-1)` and `(-1,1)`, giving the same equality. As y1 and y2 vary independently, both derivatives equal one constant alpha. Equivalently, the diagonal threshold is constant on connected fibers of `y1+y2` (or `y1-y2`), and the bounded Pexider lemma applies. Finally,

`x dot a + alpha*y dot((1,1)-a)-gamma_a`

equals `x dot a-p_a` plus the label-independent term `alpha*(y1+y2)+p_00`. Hence the maximizing labels coincide. QED.

The common ratio is constant on this exposed product block. Agreement between blocks can be propagated only through overlapping exposed open panels: two affine threshold expressions agreeing on an open interval have the same slope and intercept. Agreement merely at one endpoint or one junction does not suffice. The V2 triple-junction lemma gives compatible tangent ratios at a nondegenerate point; the present product-panel argument provides the additional open-set information needed to propagate a ratio.

## 6. What must not be imported

### 6.1 Withholding breaks the one-bit/complement correspondence

Here is an exact deterministic nine-outcome DSIC mechanism on the bounded cube. Put `s=3/4`, `b=1`, `h=1/2`, `e=1/4`, and define

`z(y)=max(0,y1-s,y2-s,y1+y2-b)`,

`u=(y1-h)_+`, `v=(y2-h)_+`,

`F_e=max(e*z,x1-s+e*v,x2-s+e*u,x1+x2-b)`.

Expand this as the maximum over disjoint joint assignments, select a fixed maximizing label, and use normalized utilities `F_e-F_e(0,y)` and `[F_e-F_e(x,0)]/e`. This proves pointwise DSIC/IR and joint feasibility. Direct substitution gives `F_e(0,y)=e*z` and `F_e(x,0)=z(x)`.

Bidder 1's price difference between no item and item 1 is

`P_1=s+e*(z-v)`.

At opponent reports `(3/5,1/5)` and `(3/5,9/20)`, this price is respectively `3/4` and `61/80`, despite the same first coordinate. Both corresponding own rows are attained. This does not contradict the bilateral lemma: when bidder 1's row changes by one bit, the other bidder's row need not change by that same complementary bit. In one region both items were withheld; in another the other bidder loses a bundle. The source's four complementary labels are absent from this argument.

### 6.2 Global occurrence of four outcomes is not decisiveness

Offer bidder 1 the menu `0,3/4,3/4,1`; give every remaining item to bidder 2 for free. This is pointwise DSIC/IR and allocates both items. Every complementary allocation occurs on an open report region. Yet bidder 2 cannot change its allocation at any fixed bidder-1 report. Item 1 is withheld from bidder 1 at `x=(3/5,1/10)` and included in its bundle at `x=(3/5,3/5)`, so the rule is not task-independent.

It is not an affine maximizer with both weights strictly positive: its interior bundle/no-bundle boundary is independent of bidder 2's report, although that bidder's allocation changes. It is an affine mechanism with zero second weight. This is precisely a degeneracy excluded by a positive-weight, decisive classification. Global onto is not a substitute for each required opponent-fiber exposure.

### 6.3 Mandatory allocation still allows nonlinear bundle thresholds without the needed range

Let `S=(x1+x2)/2` and `T=(y1+y2)/2`. Give both items to bidder 1 iff

`S>=T/(2-T)`.

Its winning price is `2*T/(2-T)`; otherwise bidder 2 wins at price `4*S/(1+S)`. The two critical thresholds are increasing inverses. Hence this binary-range mechanism is DSIC/IR, deterministic, and allocates every item. It is neither item-independent nor a fixed weighted affine maximizer with at least one positive bidder weight. Three interior rational boundary points in (S,T) have determinant `-2/105`. The missing singletons prevent decisiveness for three or four allocations. Thus mandatory assignment alone does not restore the theorem.

### 6.4 Fixed translation laws are weaker than Pexider rigidity

For real u let `r=u-floor(u)` and

`f(u)=u+r*(1-r)/4`.

This continuous strictly increasing function satisfies `f(u+1)=f(u)+1`. Its slopes inside integer cells lie between 3/4 and 5/4, but `f(0)=0`, `f(1/2)=9/16`, `f(1)=1`, so it is not affine. A semiperiodic threshold relation alone cannot prove affine structure. On a bounded interval, a required translated argument might additionally leave the domain.

Likewise a Pexider-looking identity restricted to a curve is insufficient: `f(u)=u^2`, `g(v)=v^2`, `H(z)=z^2/2` agree when u=v but are not affine. A product of open intervals, or a separately proved equivalent propagation condition, is essential.

### 6.5 Increasing scalar thresholds cannot be coupled arbitrarily

Consider the deliberately unverified joint rule obtained by offering bidder 1 prices

`p_00=0`, `p_10=y1^2/2`, `p_01=y2`, `p_11=y1^2/2+y2-1/16`,

and assigning the complementary bundle to bidder 2. Bidder 1 is truthful under this menu, and each scalar threshold increases with its corresponding opponent coordinate. Nevertheless the nonzero discount makes this allocation rule incompatible with bidder 2's IC.

Fix `x=(3/32,15/32)`. At `yA=(11/20,37/80)`, bidder 1 uniquely selects both items. At `yB=(9/20,43/80)`, it uniquely selects no item. Thus bidder 2's rows are respectively `(0,0)` and `(1,1)`, and its two-cycle expression is

`(1,1) dot(yB-yA)=-1/40<0`.

No bidder-2 payment can repair this violation without changing the allocation. This is an exact obstruction to arbitrary nonlinear threshold gluing, not a truthful counterexample. It illustrates why the exposed diagonal supplies a substantive compatibility condition beyond separate one-item monotonicity.

## 7. Pointwise and optimality implications

All transfer theorems above identify open regions. The actual finite joint label at each interface, cube face, and exceptional opponent report still has to satisfy both relative supporting-vector conditions. Neither a source's strict region inequalities nor an a.e. picture settles pointwise ties. Source threshold inverses also cannot be silently evaluated outside the locally attained interval.

For an optimality-driven next step, the classification machinery now gives a concrete audit:

- Identify an actually active four-label complementary block and certify bounded exposure of its one-item panels.
- Measure its payment interaction c and test whether its diagonal remains exposed on an opponent rectangle.
- If these hypotheses hold, restrict local variations to common affine slopes and compatible intercepts; if they fail, retain the unforced functional degrees of freedom.
- Distinguish clipping, zero normal blocks, withholding, missing alternatives, and merely pointwise junction contact. Each is a specific obstruction to a rigidity inference, not evidence that a non-affine perturbation is automatically DSIC.

No result here says a revenue optimizer has this block structure, all items are always sold, or fixed lotteries can be removed. Establishing an exposed block or a valid variation from the strongest certified mechanism is a separate task. The source transfer supplies conditional rigidity and explicit failure witnesses, not a classification of the bounded auction.

In particular, a nonlinear branch obtained by deleting options from an affine base is not ruled out just by the base's affine representation. Its actual surviving labels and exposed interfaces must be audited. Withholding alone does not prove that every complementary block is absent, while a plateau permits a zero normal block and does not supply the strict inverse hypotheses. This note makes no feasibility or revenue claim about a separately constructed candidate.

## 8. Exact replay

`certificate/classification_exact_witnesses.json` records the rational witnesses. `verifier/classification_verify.py` checks exact menu outcomes, the withholding price variation, nonlinear-boundary determinant, the constant-interaction identity, the negative bidder-2 two-cycle, and the semiperiodicity and lower-dimensional Pexider obstructions. Its checks are algebraic and on explicitly specified counterexample reports; no sampled grid is treated as an implementation or classification theorem. The replay completed with `CLASSIFICATION_TECHNIQUES_EXACT_PASS`.

The analytic local theorems are proved above. Source retrieval and arithmetic replay do not certify novelty, revenue optimality, or the correctness of every line of the source's global proof.
