# Exact sign of origin compression at V3.1

This bounded calculation resolves the derivative of one complete feasible family. It does not establish the best parameter in that family or optimality of V3.1.

Let M be the frozen V3.1 mechanism, with bidder-1 type w and bidder-2 type v. For 0<lambda<=1, evaluate M at `(lambda w,v)`, retain its allocation, charge bidder 1 its old payment divided by lambda, and retain bidder 2's old payment. Convex utilities under the linear type change prove pointwise DSIC; evaluation of a complete old joint allocation proves pointwise capacity. Normalized IR is preserved. Every report and tie uses the old complete rule.

Write R_1,R_2 for the two old expected payments and S_i for the sum of the two payment integrals on the top faces of the w square, integrated over all v. Change of variables gives

`R_1(lambda)=lambda^(-3) integral_[0,lambda]^2 integral p_1(w,v) dv dw`,

`R_2(lambda)=lambda^(-2) integral_[0,lambda]^2 integral p_2(w,v) dv dw`.

Consequently the left derivative at one is

`D=S_1+S_2-3R_1-2R_2`.

The menu payments have the required inner traces almost everywhere on the top faces. For bidder 1 this follows by approaching a fixed finite menu along an own-coordinate line; the possibly ambiguous zero-utility edge prices occur on null opponent price levels. For bidder 2, both V3.1 and V4 replacements are absent on a neighborhood of max(w)=1, and the remaining base menu prices vary continuously. The actual boundary tie convention therefore gives the same integrated traces. Singular isolated ties are not being used as substitutes for these traces.

Bidder 1 remains exactly V3, so `R_1=R_V3/2`. All V3.1 improvement belongs to bidder 2, so `R_2=R_V3.1-R_V3/2`. Thus

`D=S_1+S_2-R_V3/2-2R_V3.1`.

## Exact bidder-2 top-face integral

Use constants

`a=159/250`, `b=91/100`, `c=137/500`, `d=501/1000`, `q=227/1000`, `h=1-q`.

For opponent w=(1,r), all replacements are absent and the conditional bidder-2 menu is the affine base. The item aligned with the coordinate 1 is never bought with strictly positive utility as a singleton. Define

`Q(B)=B(1-B)+h q(1-B)+(B+h)q^2/2`.

For 0<=r<=c the conditional revenue is Q(d). For c<=r<=h it is Q(r+q). For h<=r<=1 only the bundle can be sold, with revenue `(1+r)(1-r)^2/2`. To see the middle formula, the low singleton occupies area `h(1-B)`; the bundle occupies area `q(1-B)+q^2/2` and costs B+h. At B=1 the formula joins the bundle-only expression continuously.

Item symmetry gives

`S_2=2[c Q(d)+integral_c^h Q(r+q) dr+integral_h^1 (1+r)(1-r)^2/2 dr]`

`   =5509643569103/12000000000000`.

## Exact base contribution to S_1

For any relevant menu with `0<C-A<1` and `0<C-B<1`, the payment on the own edge (1,r), integrated over r, is

* `C-(C-A)^2` if A<1;
* `C(2-C)` if A>=1 and C<=2;
* zero if A>=1 and C>=2.

The second branch is essential on rich-opponent regions. At A=1 the empty-at-zero rule selects the latter branch; this price level has zero opponent area in the menus integrated here. It is incorrect to use the first formula over the entire opponent square.

For the affine base put `g(y)=max(c,y-q)` and

`C(x,y)=max(b,x+c,y+c,x+y)`.

The base singleton prices are `A=C-g(y)`, `B=C-g(x)`. Before correcting for A>=1, item symmetry gives `2 E[C]-2 E[g^2]`. Exact elementary integrals are

`E[C]=b+c(1-a)^2+(1-c)^2(1-a)+(2a-b)^3/6`,

`E[g^2]=c^2 d+(h^3-c^3)/3`.

For the first identity, the single-buyer utility H=C-b has two singleton rectangles and a bundle rectangle minus a lower-left triangle. Their integrals are respectively `c(1-a)^2`, `(1-c)^2(1-a)`, and the correction `(2a-b)^3/6`.

The region A>=1 is, up to null boundaries,

`c<=y<=d, 1+c-y<=x<=1`, together with `d<=y<=1, h<=x<=1`.

There C=x+y. The correction from the first edge formula to the second is `C-C^2+g(y)^2`. Put `F(z)=z^2/2-z^3/3+c^2 z`. The two correction integrals are

`J_1=integral_c^d [F(1+y)-F(1+c)] dy`,

`J_2=[-(1-h^3)/3+(1-h^2)/2+q^3](1-d)-q(1+q)(1-d^2)/2`.

Therefore

`S_1,base=2(E[C]-E[g^2]+J_1+J_2)`

`        =3453946410567/2000000000000`.

## A rigorous lower bound for the actual V3 S_1

For a proper menu, the sum of its two own-edge payment integrals is

`E(A,B,C)=2C-(C-A)^2-(C-B)^2`.

A common added fee f changes E by exactly 2f. A common fee f followed by a low-item surcharge delta, with base C-A=c, changes E by

`2f+2(1-c)delta-delta^2`.

This is nonnegative for the joined Z and S branches: f,delta>=0 and delta<1-c. The unchanged inherited bundle-pivot cells also contribute nonnegative edge gains. They have nonnegative fees and their singleton prices are at most `a+1-b+max_fee=7643/10000<1`; their fee changes therefore really have edge gain 2f. All old common Z/S and selective S rows are replaced on their full positive-measure supports; row-boundary priorities do not change these integrals.

It follows that discarding the entire nonnegative Z and bundle-pivot contributions gives a valid lower bound. The remaining S contribution is rational. Put

`t_*=1058587/1362000`.

On a<=t<=2/3, use `f=2/3-t`, `delta=1/6-c+3(t-q)^2/4`. On 2/3<=t<=t_*, use `f=0`, `delta=1/2-c+3q^2/4-3qt/2`. Both are zero after t_*. The factor 2 below is the two opponent item orientations; E already includes both own top edges:

`G_S,edge=2c integral_a^t_* [2f+2(1-c)delta-delta^2] dt`

`        =2064375095897180100457/735480000000000000000000`.

Hence

`S_1 >=1272218628117805760100457/735480000000000000000000`

`    >1.7297800458446263`.

No quadrature or type-grid inference enters this lower bound. It intentionally avoids integrating the radical Z branch because its sign is enough for the present question.

## Certified derivative sign and its limit

Using the frozen upper enclosures

`R_V3 <=874648885321014010/10^18`,

`R_V3.1 <=875243586975954394119021/10^24`,

gives the exact rational bound

`D >=10162433525363281121773373/9193500000000000000000000000`

`  >1/1000>0`.

Thus decreasing lambda below one decreases revenue for all sufficiently small positive compression. This rejects the near-identity origin-compression direction. It does not prove a loss for every lambda<1, rule out another anchor or nonlinear reparameterization, or establish any optimality of V3.1.

`verifier/compression_boundary_sign.py` independently recomputes the rational integrals and verifies the certificate using only the standard library. It reads the preserved V3 and V3.1 revenue enclosures as explicit dependencies and hashes those input certificates. It does not rerun their logarithmic revenue computations or treat sampled reports as proof.
