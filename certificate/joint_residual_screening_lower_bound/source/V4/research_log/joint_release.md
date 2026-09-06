# V4 joint item release with a complete bidder-2 redesign on newly free fibers

This is a second explicit V4 mechanism, distinct from the zero-release mechanism in `free_capacity_fibers.md`. It transfers an item between bidders on a positive-volume set and has a rigorous revenue guarantee strictly above V3. It is not asserted to beat the stronger exact zero-release revenue, and it does not solve the inner problem on the remaining constrained fibers.

## Complete definition

Write each profile as `(w,z)`, bidder 1 first. Use the complete frozen V3 mechanism, including all its exact branch and tie rules, and let `(x_i,p_i,u_i)` be its truthful rows. Set

$$
\epsilon=1/100000,\quad d=501/1000,\quad b=91/100,
\qquad E_\epsilon=\{w\in[0,1]^2:w_1,w_2<d+\epsilon,\ w_1+w_2<b+\epsilon\}.
$$

For bidder 1 set `(x_1^epsilon,p_1^epsilon)=(x_1,p_1+epsilon)` if `u_1>epsilon`; set both to zero if `u_1<=epsilon`. This implements `u_1^epsilon=max(0,u_1-epsilon)`. At the equality report choose empty. Positive ties use the original V3 selection among the equally best nonempty options.

For bidder 2, if `w in E_epsilon`, offer the four options

$$
(\varnothing,0),\quad(\{1\},2/3),\quad(\{2\},2/3),
\quad(\{1,2\},(4-\sqrt2)/3).
$$

Choose the smallest item mask in `0,1,2,3` among utility maximizers. Otherwise retain its entire V3 row and payment. In particular, every boundary report outside the **strict** `E_epsilon` uses this continuation. The definition is Borel on the entire closed four-dimensional report cube and specifies all ties and exceptional reports.

## Pointwise proof

A selected original subgradient remains a subgradient of `(u_1-epsilon)_+` wherever `u_1>epsilon`. At `u_1<=epsilon`, the zero vector is a subgradient because the new utility is globally nonnegative and is zero at that report. Thus bidder 1's rule is DSIC/IR against every misreport. Equivalently, add a fee `epsilon` to every nonempty conditional menu option and allow zero-price rejection.

Every V3 singleton price is at least `d`, and every bundle price is at least `b`. These floors hold on all opponent reports, by the affine-base price formula and nonnegative V3 increments. Therefore all nonempty original utilities of bidder 1 are below `epsilon` for every fixed `w in E_epsilon`, uniformly over **all** bidder 2 reports. Bidder 1 is empty on those complete fibers, so bidder 2 has unrestricted full capacity there. Its replacement is the full randomized-class single-buyer optimum, by the precisely scoped theorem in `sources/inner_source_card.md`.

Outside `E_epsilon`, bidder 1 only deletes its old allocation and bidder 2 keeps its V3 allocation. Inside it, bidder 1 is empty and bidder 2's single-buyer menu uses available items. Capacity is therefore pointwise feasible everywhere. Bidder 2's menu depends only on the opponent's report, so its complete own-report optimization proves DSIC/IR. There is no incentive constraint linking different opponent reports. In particular, the jump at the boundary of `E_epsilon` is allowed and creates no missing own-report inequality.

This argument uses V3 containment only to inherit its original validity. The new joint outcome is not required to be a subset of its base outcome.

## Global revenue effect

For any normalized DSIC section with convex utility `u` and allocations in the unit square, its revenue under uniform own types is

$$
R(u)=\int_0^1u(1,t)dt+\int_0^1u(t,1)dt-3\int_{[0,1]^2}u.
$$

Utilities are Lipschitz; payments equal `v.grad u-u` almost everywhere, and the identity follows by integration by parts. Put `h=min(u,epsilon)`. Then

$$
R((u-\epsilon)_+)-R(u)
=-\int h(1,t)dt-\int h(t,1)dt+3\int h\ge-2\epsilon.
$$

The bound holds for every opponent report and integrates to the same bound on bidder 1's total revenue loss. This is a globally admissible change, not a pointwise virtual-value comparison or an assumed stationary deformation.

Let `E=E_0`, interpreted with the same strict inequalities. Bidder 2's increase on `E` is the exact

$$
\Delta=-\frac{56874392995943}{2250000000000000}
+\frac{246769}{13500000}\sqrt2
>0.0005731635998213549702.
$$

On `E_epsilon` outside `E`, its increase is nonnegative: every old V3 conditional mechanism is a valid single-buyer mechanism under full capacity, and the replacement achieves the unrestricted single-buyer optimum. Hence

$$
R_{\rm release}\ge R_{V3}+\Delta-2\epsilon
>R_{V3}+0.0005531635998213549702.
$$

The certified lower guarantee lies between `0.875202048920835364965684` and `0.875202048920835364965686`. The guarantee is bounded to that interval; the actual release revenue is **not** asserted to lie in that interval. An exact evaluation or sharper ranking against the zero-release splice is not provided.

## A genuine positive-volume transfer

At the interior rational profile

$$
w=(100201/200000,1/100),\qquad z=(1/4,99/100),
$$

V3 allocates item 1 to bidder 1 and item 2 to bidder 2. The respective payments are `501/1000` and `127199/200000`; utilities are `1/200000` and `70801/200000`. Bidder 1's utility is below `epsilon`, so its item is released. Its report lies in `E_epsilon`, and bidder 2 strictly prefers the SJA bundle. The new outcome is `(empty,bundle)`. Item 1 changes owners.

The exact replay also certifies the same strict transfer on the entire box

$$
\begin{aligned}
w_1&\in[d+\epsilon/3,d+2\epsilon/3],&w_2&\in[9/1000,11/1000],\\
z_1&\in[249/1000,251/1000],&z_2&\in[989/1000,991/1000].
\end{aligned}
$$

On this box both old V3 sections are on base branches. Bidder 1 uniquely wants item 1 with utility in `[epsilon/3,2epsilon/3]`; bidder 2 uniquely wants item 2 before redesign and the bundle afterwards. All box widths are strictly positive, so this is a positive-volume escape from joint containment, not an exceptional-report trick. The single rational witness and box inequalities are checked by `verifier/release_joint.py`; the universal feasibility and incentive claims rest on the preceding analytic proof.

## Exact inner scope

Bidder 2 is fully reoptimized on **every** free fiber created by the stated region `E_epsilon`; its menu is globally valid on the whole continuous own-type square. This is not alternating best response. Nevertheless the continuation outside `E_epsilon` is merely feasible, and the value of `V(1-x_1^epsilon)` over all constrained fibers remains uncomputed. Its true value is at least the explicit continuation's revenue. The construction establishes a joint reallocation and a strict lower guarantee; it does not turn a partial inner solve into the full eliminated optimizer.
