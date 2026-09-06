# Exact constrained screening at actual V3 residuals

This route reaches a full randomized inner optimum and a matching global capacity support. The proof does not assume a finite menu, deterministic allocations, or a finite type grid for its competitors. The three-option nonempty menu emerges as an optimizer certified against the full class.

## 1. The solved residual class and complete optimizer

Let the screened bidder's type be `(x,y)`, uniform on the unit square. Set

`k_min=(2-sqrt(2))/3`, `k_min<=k<=2/3`,

`A=2/3`, `C=5/6+3k^2/4`, `B=C-k`.

Consider any pointwise Borel residual with second-item capacity identically one, first-item capacity one for `x>k`, and first-item capacity zero on the top edge `y=1, x<k`. Interior first-item capacity for `x<k` can be completely arbitrary. At `x=k`, it also can be arbitrary.

**Theorem 1.** Every such residual has the same unrestricted randomized DSIC/IR value

`V_k=59/108+k^2/4-k^3+9k^4/16`.                 (1)

A complete optimal mechanism offers the menu

| Allocation | Payment |
| --- | --- |
| `(0,0)` | `0` |
| `(1,0)` | `A` |
| `(0,1)` | `B` |
| `(1,1)` | `C` |

Choose empty whenever maximal utility is zero; at positive ties prioritize item 2, then item 1, then the bundle. Its utility is

`u*(x,y)=max(0,x-A,y-B,x+y-C)`.

An option containing item 1 cannot be selected when `x<k`: the item-1 singleton has nonpositive utility because `k<=A`, and the bundle loses strictly to item 2. At `x=k` the stated priority still selects no item 1. Thus the mechanism is feasible for every residual in the theorem, at every report. Taxation gives complete DSIC and IR. The proof of unrestricted optimality follows from the measure certificate below.

The theorem says that once the top-edge constraint is imposed, all remaining interior capacity details on the left strip cease to affect optimal revenue. It does not assert that those details cease to affect the feasible mechanism set.

## 2. A global price measure and an exact nonnegative gap

Define

```
ell(x)=B                  for 0<=x<=k,
ell(x)=C-x                for k<x<=A.
```

Partition the square, assigning boundaries arbitrarily for volume integration, into

```
D_R = {x>A},
D_T = {x<=A, y>ell(x)},
D_0 = {x<=A, y<=ell(x)}.
```

Each region has area exactly `1/3`. This follows from `A=2/3` and

`area(D_0)=A*C-A^2/2-k^2/2=1/3`.

Put

```
f(x)=3B-2                 for 0<=x<=k,
f(x)=3C-3x-2              for k<x<=A,
f(x)=1                    for A<x<=1,
F(x)=integral_x^1 f(s)ds.
```

The price measures on the **complete report square**, retaining the top edge, are

```
pi_1 = 3(x-A)_+ dx dy + F(x) dx delta_{y=1},
pi_2 = 3(y-ell(x))_+ 1_{x<=A} dx dy.
```

These are finite nonnegative countably additive Borel measures. To check positivity, `B<=2/3` is equivalent in the stated parameter interval to `k>=k_min`. Thus `f<=0` on `[0,A]`, while `f=1` above `A`. Also `integral_0^1 f=0`, by the equal-area identity. Consequently `F(0)=F(1)=0`, `F>=0`, and `F(A)=1-A`. More explicitly,

```
F(x)=(2-3B)x                                      for x<=k,
F(x)=1-A+(3C-2)(A-x)-3(A^2-x^2)/2                  for k<=x<=A,
F(x)=1-x                                          for x>=A.
```

**Theorem 2 (full capacity support).** For every arbitrary pointwise Borel residual `r` and every complete randomized DSIC/IR mechanism `(a,p)` with `a<=r`, utility `u=x a_1+y a_2-p`, and integrable payments,

`<pi,r>-R = <pi,r-a> + 3 integral_{D_0}u >=0`.       (2)

The equality is exact; no stationarity, asymptotic expansion, or fixed menu is involved. For a residual in Theorem 1, the displayed candidate makes both nonnegative terms vanish. Hence

`V(r)<=V(r*)+<pi,r-r*>`

for every residual `r`, with equality at the solved residual `r*`.

*Proof.* Let `g(x)=u(x,1)` and `h(y)=u(1,y)`. Pointwise IC gives convex Lipschitz own-type utilities and the coordinate envelope identities on every horizontal and vertical line, including the boundary lines. Thus

`R=integral g + integral h - 3 integral u`.

On `D_R`, use the exact envelope `u(x,y)=h(y)-integral_x^1 a_1(s,y)ds`. On `D_T`, use `u(x,y)=g(x)-integral_y^1 a_2(x,s)ds`. Keep the integral of `u` on `D_0` unchanged. Fubini gives

```
R = integral f(x)g(x)dx
    + 3 integral (x-A)_+ a_1(x,y)dxdy
    + 3 integral_{x<=A}(y-ell(x))_+ a_2(x,y)dxdy
    - 3 integral_{D_0}u.
```

The `h` coefficient vanishes because `1-3(1-A)=0`. Since `F'=-f` and `F(0)=F(1)=0`, integration by parts on the top edge gives

`integral f g = integral F g' = integral F(x)a_1(x,1)dx`.

The last equality uses the **top-edge** IC envelope; replacing it by an almost-everywhere-in-volume gradient statement would be invalid. This proves (2). IR and pointwise capacity prove nonnegativity. All measures and functions are Borel and bounded where integrated, so no measurable selection or dual-attainment theorem is used. The proof even permits unnormalized IR utilities; normalization is available for the optimizer. QED.

At the candidate, `u*=0` on `D_0`. The volume part of `pi_1` lies in `x>A`, where the candidate always allocates item 1. The top-edge part sees allocation zero below `k` and one above `k`. The density of `pi_2` lies precisely where the candidate allocates item 2. These observations prove equality with the residual capacities of Theorem 1, including arbitrary interior holes below `k`. The edge's junction point `x=k` has zero measure, while the complete tie rule makes its allocation pointwise feasible anyway.

## 3. Exact value, free boundary, and interpretation

Let `G(A,B,C)` be the revenue of the stated discounted four-option menu:

```
G=A(1-A)(C-A)+B(1-B)(C-B)
  +C[(1-C+B)(1-C+A)-(A+B-C)^2/2].
```

Direct substitution yields (1). An independent pairing calculation gives the same value:

```
<pi,r*>
 = 3(1-A)^2/2
   + integral_k^1 F(x)dx
   + (3/2)k(1-B)^2
   + [(1-C+A)^3-(1-B)^3]/2.
```

The first two geometric equations, `area(D_R)=area(D_0)=1/3`, force `A=2/3` and `C=5/6+3k^2/4`. These are the equations needed for cancellation in a certificate valid for every DSIC utility. They are stronger evidence than stationarity in a convenient price family.

The value's derivative has the exact capacity interpretation

`V_k' = -k(2-3B) = -F(k)`.

Moving the top-edge exclusion boundary prices its information-rent effect at the singular capacity density. The remaining capacity freed strictly inside the left strip has zero price in this supporting measure. That does not mean no feasible mechanism uses it; it means it cannot improve the fully optimized inner revenue under the retained top constraint.

At `k=k_min`, the prices reduce to `A=B=2/3`, `C=(4-sqrt(2))/3`. The edge price below `k` is then zero, and the same proof certifies the familiar unrestricted one-buyer two-item menu. This observation is derived here from the displayed identities; no external classification theorem is invoked.

## 4. Verification at actual frozen V3 residuals

Use V3's exact constants

`a=159/250`, `b=91/100`, `sigma=1137/1000`,

`c=b-a=137/500`, `d=sigma-a=501/1000`, `q=sigma-b=227/1000`.

Fix bidder 1's report `w=(t,rho)` with

`d<t<=a`, `0<=rho<=b-t`, and set `k=t-q`.

The low coordinate satisfies `rho<d`. Bidder 1's item-2 singleton and its bundle have nonpositive utility at every opponent report, by the base price floors and the nonnegative V3 increments. Zero-utility rejection removes their ties. Bidder 1 can therefore receive only item 1, so the residual second-item capacity is one everywhere.

For `t<a`, its base item-1 allocation can only arise through the split outcome. Comparing the nine shared-base scores gives the exact strict winning rectangle

`x<k`, `y>sigma-t`.

At `t=a`, the extra singleton tie still has zero utility and is rejected; the conclusion that the final first-item hole lies in `x<k` remains valid. At `x=k` the opponent's bundle has earlier base priority than the split, so bidder 1 does not take the item. All V3 final allocations are subsets of the shared base. Thus the actual residual equals one whenever `x>k`.

The actual interior hole is generally smaller than the base rectangle; joined surcharges and finite bundle-pivot rows clip it. The proof does not replace that actual hole by an assumed rectangle. Instead it checks the needed top trace directly. At opponent `(x,1)`, bidder 1's final item-1 price is

```
d             if x<=c,
x+q           if x>c.
```

For `x<=c` the joined menu has returned to its base branch at opponent high type one. For `x>c`, the joined chamber is absent and all inherited bundle-pivot fees vanish because `x+1>1`; the base formula gives `x+q`. Hence bidder 1 takes item 1 exactly when `x<k`: its utility is strictly positive there, and at `x=k` zero-utility rejection chooses empty. The second item remains unavailable to bidder 1. This verifies the top-edge hypothesis on every report, not by extrapolating from interior samples.

Consequently Theorems 1 and 2 solve the full inner problem at these **actual, nonfree V3 residuals**. At `t=51/100`, `rho=1/100`, one has `k=283/1000`, and

`V_k=236416913460803/432000000000000`.

The optimal menu and its global supporting measure are explicitly given above. The old V3 menu before its first square-root transition is suboptimal for this fixed first bidder. This is a complete re-optimization of the second bidder, not an alternating response or an allocation-contraction calculation.

The strict condition `t>d` is necessary for this top-hole argument: at `t=d`, the relevant top utility ties at zero, and rejection removes part of the bottleneck. No inner-optimality claim at that endpoint is inferred by continuity.

For `t1=q+sqrt(4c/3-2/9)<=t<=a`, the frozen V3 menu already equals the certified menu. Thus those existing conditional fibers are now globally certified, while the earlier ones admit the strict replacement. A separate geometry audit handles the further extension through `t=2/3`; the certificate itself requires only candidate feasibility and saturation on its stated price supports.

## 5. Exact replay and discovery record

`verifier/constrained_screening_verify.py` checks the equal-area equations, price conditions on a containing rational parameter interval, nonnegative-tail formula, exact menu revenue and independent measure pairing, and the identity `V_k'=-F(k)`. The measure-pairing identity is checked as a degree-at-most-six polynomial identity using seven exact rational interpolation nodes; this is an algebraic identity check, not a finite-type approximation. It also checks complete menu dominance on its defining affine cells and exact top-edge V3 price comparisons at the rational example. Default replay compares the saved certificate without writing; `--write` generates it.

An earlier optional one-lottery probe in `verifier/constrained_lottery_probe.py` integrated entire continuous polygon cells and found no positive gain in its explored parameters. That nonfinding is not used in the proof. The exact gap identity now rules out every randomized improvement at the solved residual, including any number or continuum of lotteries.

This solves the inner problem on the stated positive-measure set of actual outer reports. It does not certify the first bidder's global optimality against the same prices, or identify the unrestricted optimal two-bidder mechanism.
