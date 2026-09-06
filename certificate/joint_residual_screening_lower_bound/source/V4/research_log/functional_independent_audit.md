# Independent audit of the V4 residual functional

Audited `research_log/residual_functional.md` and read `verifier/functional_verify.py`. This was an independent mathematical review. The author's files were not modified. After the author changed normal replay to read-only comparison, independently ran it with `python -B -X utf8`: PASS. The saved certificate's SHA256 was unchanged before and after replay. Certificate generation now requires explicit `--write`. No mathematical blocker was found in the stated functional results.

## Exact elimination: valid without a selection theorem

The definition of `V(r)` takes a supremum over complete **jointly Borel** mechanisms on the entire opponent/own report space. Its feasible set is nonempty because the zero mechanism belongs to it. Its normalized revenues lie in `[0,2]`. Hence, for any fixed complete `M1` and positive `epsilon`, the definition of supremum supplies one complete Borel `M2` within `epsilon` of the inner value. This is one global choice, not a choice of an optimizer for every opponent slice. Pairing it with `M1` preserves each bidder's separate IC and IR inequalities and gives pointwise capacity feasibility. Taking the two suprema proves the displayed elimination identity.

Normalization also has the claimed scope. Nonnegative allocation and IC imply `u(t,v)>=u(t,0)`, so subtracting `u(t,0)` preserves IR as well as IC. The resulting payment is Borel and lies between zero and `v.a`. For an originally integrable mechanism, the normalization shift is integrable: `u(t,0)<=u(t,v)` and the original utility is integrable because valuations/allocations are bounded and payments are integrable. Thus this normalization does not silently change the admissible optimum.

## Positive homogeneity: the two-way argument is sound

For `alpha>0`, mapping `(a,p)` to `(alpha a,alpha p)` preserves every IC/IR inequality and `u(t,0)=0`; mapping back by `1/alpha` proves the reverse value inequality. Both directions stay admissible whenever the specified capacities `r` and `alpha r` lie in the unit box. In particular, scaling back a mechanism bounded by `alpha r` yields an allocation bounded by `r<=1`.

For `alpha>1` this argument is about scaling marginal allocation vectors and reconstructing a lottery with those marginals, not multiplying the probabilities of a fixed probability distribution by `alpha`. Because the inner bidder has two additive items and each scaled marginal is at most one, such a lottery always exists. This is an explanatory clarification, not an extra hypothesis.

The derived concavity, superadditivity on `r+s<=1`, and convexity of opportunity cost follow. The warning against inferring `<pi,r*>=V(r*)` for every affine support at a boundary point is correct: upward scaling can be unavailable, and the zero-slope support at full capacity is a counterexample.

## Failure of countably additive supports: verified

The capacity with `rho*(z_n)=1/(n+2)` at `z_n=1-1/(n+2)` and `rho*=1/2` elsewhere is Borel, strictly positive at every point, and has zero future envelope for every `z<1`. Formula (5.1) therefore gives value zero. The value at the endpoint does not affect revenue, and its exceptional allocation can be chosen pointwise feasibly.

If a finite signed countably additive measure supports globally at this capacity, testing `rho*+(1/2)1_A` for every Borel set forces positivity of that measure: the perturbed value is nonnegative, and the support bound is `(1/2)pi(A)`. Testing capacity zero then forces `integral rho* dpi<=0`. Positivity forces this integral to vanish. The countable cover by `{rho*>=1/k}` now implies the measure is zero, contradicting positive value at full capacity.

The full two-item embedding is valid as stated. Varying only item 1 makes the second price component disappear from all these tests; arbitrary Borel profile subsets can be used in the positivity argument. The construction also is a realizable residual of the displayed bidder-1 mechanism because that allocation is independent of bidder 1's own report. The conclusion is precisely nonexistence of a **finite countably additive** supporting Borel measure at this example. It makes no claim about existence of finitely additive supports or about regular residual candidates such as V3.

## Additional checks and scope

The selected-subgradient formulation retains the necessary exceptional-report constraints. If joint Borel measurability of the utility is desired explicitly in that formulation, it follows from the stated Borel selection and normalization using

`u(t,v)=integral_0^1 v.a(t,s v) ds`.

The bounded selected subgradients justify this one-dimensional envelope identity even on boundary rays. The top-face integration-by-parts objective and the singular support at the missing top report are also valid. In the latter argument `u(v)>=u(top)` follows from IC against the zero allocation at the top, while coordinate monotonicity gives the reverse inequality.

The final certificate theorem correctly requires both the full residual support and global outer priced optimality. Its alternative `W_1(pi)+W_2(pi)+<pi,1>` bound retains the intercept and capacity complementary slackness. No stationarity-to-optimality inference or unproved dual attainment appears.

The arithmetic verifier clearly limits itself to rational identities and a finite tail sample. The continuum future-envelope argument, the infinite-tail obstruction, and the functional certificate theorem remain written analytic proofs. This audit does not certify the unrestricted optimal auction or supply a support at the actual V3 residual.

## Audited source snapshot

SHA256 values independently read after the final read-only replay change:

```
3892ef36d2f3c9f3329f0459d0aaf3181ac81675cd080bd7e018db64ecbc7692  research_log/residual_functional.md
db06e4237d321cea359087200c1a21d6c4fb8592678326bd97ca41066e2fefdb  verifier/functional_verify.py
c0e497ab1aedf5ae274400f294cea6a53904a096c0b7c27fbe8bc752b94aa3e1  certificate/functional_replay.json
```
