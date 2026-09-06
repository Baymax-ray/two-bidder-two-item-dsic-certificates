# Independent audit of the V3 joined-threshold mechanism

The audit passes. Independent rational polynomial integration and a bounded binomial series give

`0.874648885321014009995481 <= R <= 0.874648885321014009995482`.

Subtracting the exact archived revenue L gives

`0.000043898918177741703470 <= R-L <= 0.000043898918177741703471`.

These endpoints are rational outward bounds, not floating estimates. They lie inside the candidate's published enclosure. This certifies an improved feasible lower construction; it supplies no unrestricted optimality certificate.

## 1. Independence and execution boundary

The audited definition is `research_log/joined_threshold_candidate.md`, with exact rational-report implementation `verifier/joined_threshold.py`. The separate replay `verifier/joined_independent.py` reconstructs both new integrals using its own sparse rational polynomial arithmetic. It never calls either candidate `calculate()` function. In particular, it does not use the candidate's logarithm series, decimal square-root brackets, interval class, polynomial class, expanded coefficient tables, or reported new-S integral as an input to integration. It compares against the reported new-S value only after computing its own answer.

The retained base and bundle revenues are recomputed by the V3 `baseline_replay.py`, which imports no archived verifier. This is shared V3 baseline evidence, not a second independent execution of the old archive's polytope verifier. The exact mechanism function is invoked only for targeted implementation checks after the revenue calculation is complete.

The replay is print-only by default and compares its result with `certificate/joined_independent.json`. Its explicit `--write` mode creates that one V3 certificate. Assertions are protected by an early rejection of `-O`.

## 2. Menu revenue and the radical identity

Use the candidate constants `a=159/250`, `b=91/100`, `c=137/500`, `d=501/1000`, `q=d-c`, `K=2/3+c^2`. Let `t` and `rho` be the opponent's high and low reports and `k=t-q`.

For singleton prices A,B and bundle price C with `0<A,B<1`, `max(A,B)<C<A+B`, the singleton areas are `(1-A)(C-A)` and `(1-B)(C-B)`. The bundle region is the rectangle above the singleton/bundle thresholds, minus the corner triangle of side `A+B-C`. Its area is

`(1-C+B)(1-C+A)-(A+B-C)^2/2`.

Multiplying by prices yields the candidate's conditional revenue G. These geometric arguments only need the displayed discount inequalities and singleton prices below one; they do not need `C<=1`. Continuous boundary limits apply at degenerate endpoints.

Direct expansion, independently of either candidate polynomial implementation, gives

`G(C-c,C-k,C)=C[1+3(c^2+k^2)/2]-C^3/2-c^2-c^3-k^2-k^3`.

At the common-fee stationary point `C^2=K+k^2`, the bracket multiplying C is `3C^2/2`. Hence

`G=(K+k^2)^(3/2)-c^2-c^3-k^2-k^3`.

For the base menu `(a,b-k,b)=(b-c,b-k,b)`, subtraction cancels the last four terms and gives

`G_new-G_base=(K+k^2)^(3/2)-3b(K+k^2)/2+b^3/2`.

This confirms the radical term and every sign in the candidate's integrand.

Let `h=b-q`. The opponent width in Z is `b-t=h-k`. The factor four counts two bidders and two item orientations. Consequently the radical contribution is the integral of four times the preceding difference times `h-k`.

For the stated primitive

`J(k)=k(2k^2+5K)sqrt(k^2+K)/8 + 3K^2 log(k+sqrt(k^2+K))/8`,

differentiate the first term to obtain `(8k^4+16Kk^2+5K^2)/(8sqrt(k^2+K))`; differentiating the logarithmic term adds `3K^2/(8sqrt(k^2+K))`. Their sum is `(k^2+K)^(3/2)`. Also the integral of `k(k^2+K)^(3/2)` is `(k^2+K)^(5/2)/5`. This proves the candidate's exact radical/logarithmic expression separately from the independent enclosure method below.

## 3. Independent enclosure without logarithms

Set `r0=b^2-K` and `r1=4c/3-2/9`. Each endpoint square root is enclosed by 160 exact dyadic bisections, with its squared inequalities checked. Write

`(K+k^2)^(3/2)=(93/100)^3(1+z)^(3/2)`,

`z=[K+k^2-(93/100)^2]/(93/100)^2`.

The replay verifies `|z|<=1/20` over the whole outer endpoint enclosure. Let `c_n=binomial(3/2,n)`. It integrates the first 25 terms, n=0 through 24, as an exact polynomial in k. For n>=2,

`|c_(n+1)/c_n|=(n-3/2)/(n+1)<1`.

The omitted absolute tail is therefore at most

`(93/100)^3 |c_25| (1/20)^25 /(1-1/20)`.

This bound remains valid for negative z; it does not rely on alternating-series signs. The positive weight `4(h-k)` multiplies the uniform error, integrated over the outer bracket. Interval Horner evaluation of the exact polynomial primitive encloses the endpoint uncertainty. All operations are on rational numbers.

The Z quadratic segment is integrated from `q+sqrt(r1)` to a using its independent exact polynomial primitive and the same dyadic endpoint enclosure. The two S segments, from a to 2/3 and then to `1058587/1362000`, have rational endpoints and are integrated exactly. The resulting new-S gain is

`45691126330408099543/367740000000000000000000`.

The replay's root and quadratic Z contribution enclosures, endpoint brackets, tail bound, and final rational bounds are saved in its JSON certificate.

## 4. Whole-mechanism accounting and the opponent widths

The old nonzero Z rows are contained in `d<=t<=a`, `rho<=b-t`. The old S and selective-item rows are contained in `a<=t<=1`, `rho<=c`. All are inside the replacement chamber, apart from boundary priorities that the new rule explicitly replaces. New Z widths are `b-t`; new S widths are c. The factor four is the same two-bidder, two-orientation factor in both regions.

Every old positive bundle-pivot cell has interior `t+rho>b` and `rho>c`. These interiors are outside the new chamber. For t<=a the new chamber instead satisfies `t+rho<=b`; for t>=a it satisfies `rho<=c`. Thus the bundle-pivot gain is retained, and no positive-volume contribution is omitted or counted twice. Boundary changes have measure zero for integration and are handled pointwise by the explicit menu rule.

The independent total is therefore computed as

`R=base revenue + retained bundle gain + new S gain + new Z gain`.

The first two terms are

`26232089810531183/30000000000000000`

and

`70946101529751/10240000000000000000`.

The replay independently confirms that subtracting all old Z, S, and selective gains from L gives exactly those same two retained terms. The removed sum is

`780257552943947517/4000000000000000000000`.

In particular, the archived S common-plus-item amount is removed once, not merely the S common fees, and the bundle-pivot gain is not removed.

## 5. All-report admissibility and the optional archived guard

The shared affine base has nonempty prices bounded below by `137/1000` and base discount `A0+B0-C0>=227/1000` for every opponent. The base outcome is chosen globally with one declared priority, and both bidders use projections of that same outcome.

For a subadditive base menu, any nonnegative increments `(alpha,beta,gamma)` with `gamma>=max(alpha,beta)` admit a maximizing subset of each originally selected mask. To prove this, suppose the old choice is singleton 1. Its preference over the old bundle gives `v2<=C0-A0<=B0`, so the other singleton cannot become strictly profitable. The bundle's relative utility versus singleton 1 cannot increase because its increment is at least alpha. Hence empty or singleton 1 is a new maximizer. The singleton-2 case is symmetric. For an old empty choice all nonempty utilities only fall; for an old bundle every mask is already a subset. At zero maximum utility choose empty. This argument includes all ties.

All joined increments have the form `(f,f+delta,f+delta)` in the high-item, low-item, bundle orientation. Their f and delta are nonnegative on each prescribed branch. The square-root branch starts at `C=b`; its common fee is `C-b`. At the root/quadratic junction `k^2=r1`, the surcharge `1/6-c+3k^2/4` is zero, and it increases thereafter. The common fee is `2/3-a` before t=a and `2/3-t` after that pivot, reaching zero at 2/3. The last surcharge is linear and falls to zero exactly at the stated cutoff.

No inequality `delta<base discount` is needed in this proof. The archived strict delta guard is an optional sufficient condition that happens to hold for its frozen rows. It is not a condition on the joined construction or the general increment cone. Likewise `C<=1` is not required for DSIC or capacity; the new affine tail has C>1 at some reports. The final discount is the base discount plus f, so it stays positive regardless of delta.

The revenue geometry is valid throughout the replacement. Before the root transition, A=a and B=b-k lie below one and have positive discount a-k. On the root branch A runs from a to 2/3, B decreases and remains positive, and the discount inequality is equivalent to `2ck<2/3`, verified using `k<a-q`. On the quadratic branch A=2/3, B decreases while remaining between zero and 2/3, and the discount is `2/3-k>0`. On the affine and final base branches A=t<=1, B lies between d and its value at t=2/3, and the discount is q. Bundle-minus-singleton differences are positive throughout. The single endpoint A=1 uses the continuous area formula for revenue, without asserting an extension of the same directional derivative beyond that endpoint.

For each bidder the final menu depends only on the opponent's report. Choosing a menu maximizer proves DSIC against every own report; empty proves IR. The positive prices imply exact zero-type normalization. Base-subset containment proves item capacity at every joint profile. Finite formulas with square roots on positive radicands, closed branch tests, and finite priority rules are Borel. Payments are bounded by reported allocated value under IR and so are integrable.

The final choice must be tied to the shared affine base, not necessarily to the archived mechanism's already deleted allocation. Replacing an archived fee can restore an item that the archive had deleted, while still preserving containment in the same feasible base. The inspected implementation uses `base_masks` for precisely this reason.

## 6. Rational tie implementation audit

The exact executable comparison uses one quadratic field per bidder. The sign rule for `r+s sqrt(w)` compares signs first and, when the terms oppose, compares `r^2` with `s^2 w`; no approximate square root enters mechanism decisions. The mathematical mechanism definition covers all real reports. The executable is an exact evaluator of rational reports, not a purported enumeration of all real inputs.

The separate replay checks 20 rational profiles across the base, root, quadratic, affine, and inherited branches. For every checked profile it independently recomputes all four own-option utilities from the returned prices, verifies exact utility maximization and selected-price payments, verifies containment in the common base, and checks disjoint masks and zero-utility opt-out. Specific checks include:

- Opponent `(11/20,1/10)` and own `(3/4,c)`: a strictly positive high-singleton/bundle tie; global base retention selects singleton 1.
- The same opponent and own `(323/1000,3/4)`: a strictly positive low-singleton/bundle tie; global base retention selects the bundle.
- The rational parametrization `C=(3/5+K/(3/5))/2`, `k=(K/(3/5)-3/5)/2`, opponent `(q+k,1/10)`, own `(C-c,c/2)`: an exact root-branch zero-utility tie, resolved to empty.
- Rational junctions t=a, t=2/3, and the exact affine cutoff; zero own types at rho=c; an all-ones joint report.

A separate strictly interior bundle-pivot opponent `(49/80,3/10)` verifies retained first-bidder allocation and payment against the baseline evaluator. Algebraic root junctions are checked by exact gluing identities, rather than by pretending they are rational test inputs.

Run `python -B -X utf8 verifier/joined_independent.py` from V3. The analytic menu and containment proof covers all reports; finite profile checks audit the implementation only. Four-direction stationarity and full unrestricted optimality are separate obligations; neither is inferred from this replay.
