# Exact affine-base revenue as the split cost changes

This calculation concerns the globally feasible affine base with fixed singleton cost `a=159/250`, bundle cost `b=91/100`, and split cost s. It supplies the base term for the root investigator's complete changed mechanism; it does not include the separately retained fee corrections or the reoptimized residual fibers.

Let `s0=1137/1000`, `c=b-a=137/500`, `d=s-a`, `q=s-b`, and `h=1-q`. Throughout `s in [s0-1/1000,s0]`, the relevant strict inequalities are

`0<c<d<a<1`, `q>0`, `h<1`, and `h>b-d>c`.

The base chooses a common maximum over the nine feasible deterministic allocation pairs, with costs 0,a,a,b,a,a,b,s,s. For opponent `(x,y)` its conditional prices are

`A=H+min(a,s-y)`, `B=H+min(a,s-x)`, `C=H+b`,

where `H=max(0,x-a,y-a,x+y-b)` is independent of s. The exact shared-base allocation and tie convention remain the mechanism definition. Revenue calculations below ignore ties only for integration: these finitely many affine equalities have zero four-dimensional measure.

## The derivative includes the high-price menus

For any strictly discounted conditional menu in the present base range, put `k=C-B`. Here `0<k<1`. If `0<B<1`, the item-2 choice cell is the rectangle

`0<=v1<=k`, `B<=v2<=1`.

Increasing B while holding A,C fixed raises payments on that rectangle, moves its entry edge upward, and moves its contact with the bundle leftward. The resulting derivative is

`partial_B R = k(1-B)-Bk+k(1-B)=k(2-3B)`.

This formula also holds when A>=1 and the other singleton has disappeared: neither moving contact depends on the presence of that singleton. It therefore does not silently extend the proper-menu cubic past an invalid A-boundary. If B>1, the item-2 option is unavailable at positive utility and `partial_B R=0`. At B=1 use the appropriate one-sided derivative; the corresponding opponent level has zero area in this calculation.

By item symmetry, the per-bidder derivative is consequently

`D_1(s)=2 integral_(x=d)^1 integral_(y=0)^1 (x-q)(2-3B(x,y;s)) 1_{B<1} dy dx`. (1)

The factor 2 here is item symmetry, not the number of bidders. Differentiating the min functions creates no additional term at x=d because the conditional prices and revenue are continuous there. Both price partial derivatives are locally uniformly bounded; the moving B=1 and A=1 opponent levels are null. Thus differentiation under the opponent integral is justified, including all own allocation-boundary movements.

## Exact reduction to polynomial integrals

For x>d>c, the base pivot simplifies to

`H=max(0,x-a,x+y-b)`.

For d<=x<=a, the zero-pivot interval is `0<=y<=b-x`, with `B=s-x`. Above it, `B=y+q`.

For a<=x<=1, the singleton-pivot interval is `0<=y<=c`, with `B=d`. Above it, again `B=y+q`.

The bundle-pivot term is active exactly for y<h. Its primitive is

`F(y)=(2-3q)y-3y^2/2`.

Combining each lower interval with its adjacent upper interval cancels the linear terms. Formula (1) becomes

`D_1(s)=2 F(h) integral_d^1(x-q) dx`

`        -3 integral_d^a(x-q)(b-x)^2 dx`

`        -3 c^2 integral_a^1(x-q) dx`.                                  (2)

Put `z=a-q`. Since `d-q=c` and `b-q=z+c`, direct evaluation gives

`D_1(s)=(3h^2/2-h)(h^2-c^2)`

`        -(z^4-c^4)/4-c z^3+z c^3-3c^2(h^2-z^2)/2`.                   (3)

All topology inequalities used above hold on the entire requested s interval. No type grid or numerical optimizer is used.

## Exact derivative and revenue-change polynomial

Expanding (3) gives the quartic

`D_1(s)=39760023849/3906250000 -(48411347/1953125)s`

`        +(221343/10000)s^2 -(216/25)s^3 +(5/4)s^4`.

At s=s0,

`D_1(s0)=173733429/4000000000000`.

Writing `theta=s-s0 in [-1/1000,0]`, integration gives

`R_1,base(s)-R_1,base(s0)`

`  =(173733429/4000000000000)theta`

`   -(612392179/2000000000)theta^2`

`   +(314537/400000)theta^3`

`   -(591/800)theta^4 +theta^5/4`.                                     (4)

The total affine-base revenue change is exactly twice (4). The frozen calibration is

`R_base,total(s0)=26232089810531183/30000000000000000`,

read from `V3/certificate/baseline_mechanism.json`, field `expected.base`. This calibration is not used to derive the derivative or change polynomial.

The base term itself decreases when s is decreased anywhere in this interval: every nonzero term in (4) is negative for theta<0. Equivalently,

`173733429/4000000000000 <= D_1(s) <= 514209/781250000`.

This does not determine the sign of the full changed auction's revenue. The fixed-increment corrections and the new residual optima can outweigh the base loss; they are independent terms assigned to the root investigator.

## Replay scope

`verifier/base_split_cost.py` verifies the polynomial identities, exact derivative bounds, and calibration dependency using standard-library rational arithmetic. It also checks the entire parameter interval through endpoint inequalities and a Bernstein coefficient sign certificate. It does not rerun or assert a new full-mechanism revenue claim. The complete changed shared-base and residual mechanism requires the root investigator's separate feasibility and integration proof.
