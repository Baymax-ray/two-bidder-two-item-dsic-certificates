# The final common dual also has strict slack against the new selected lower mechanism

**PASS, with a strictly positive rational gap.** This note concerns the
selected `V4_6_1_lower_bound/verifier/functional_exchange.py` mechanism.
It proves that the final V4.6.2 common capacity/incentive system cannot
match that mechanism. It does not prove that the new lower mechanism is
suboptimal, nor does it alter either lower-bound package.

The old V4.6 witness with safe coordinate 13/40 lies inside the new
functional tent. Instead use the nearby closed box centered at

    (w1,w2,v1,v2) = (151/200,3/40,9/10,63/200),

with halfwidth 1/10000 in every coordinate. Its interior has positive
volume `1/625000000000000`. This box is strictly disjoint from the new
functional tent, the upper branch's conditional-support square, and all
eight sparse-cycle rectangles. The old field's nonzero-value proof is
reconstructed on this different box; the old JSON is not reused as if
its old center covered the new center.

## Complete selections on the whole real box

Write `t=w1`, `rho=w2`, `x=v1`, and `y=v2`. The new lower parameters are

    A=2/3, c=47/150, b=49/50, s=7/6, q=14/75,
    T=178/225, U=26/25.

Throughout the closed box,

    A<t<T, rho<c, t>rho,

so bidder 2 faces the E lottery menu, with physical item 1 scarce. Put

    delta(t)=9(T-t)(U-t)/16,
    alpha(t)=3t-2,
    beta(t)=alpha/(alpha+2delta),
    L(t)=delta+alpha/2.

Delta decreases, beta increases, and L increases throughout the t
interval: the exact derivative signs are checked at the appropriate
endpoints. Exact endpoint comparisons imply

    9/10 < beta(t) < 49/50,
    c < y < c+L(t),      x>t.

The lottery utility is `x-t+beta(y-c)>0`. Its advantage over the scarce
singleton is `beta(y-c)>0`. Its advantage over the bundle is
`(1-beta)(c+L-y)>0`, using `delta=(1-beta)L`. Against the safe singleton,
its advantage is greater than `x-t+1/2-y>0`. Thus it is the unique
utility maximizer on the entire box, with allocation `(1,beta)`.

The opponent v indexing bidder 1's menu has x>T, so this is a base menu.
Also y>c and x>A, hence

    H(v)=x+y-b.

The inequalities `s-y>A` and `s-x<A` hold throughout the box. Thus the
base prices simplify exactly to

    P1=x+y-c,       P2=y+q,       C=x+y.

Using lower endpoints for prices and upper endpoints for bidder 1's
values gives strict inequalities

    P1>t,       P2>rho,       C>t+rho.

Every nonempty option therefore gives negative utility. Bidder 1 uniquely
chooses empty.

These all-real inequalities establish the complete selected pair
`((0,0),(1,beta(t)))` with no tie exception inside or on the closed box.
The exact evaluator is additionally checked at all 16 corners and the
center; these 17 reports supplement, rather than replace, the continuum
selection proof.

## Why both functional modifications are absent

The tent support is `(8/25,17/50)`. Both opponent minima are strictly
below its lower endpoint: rho is near .075 and y is near .315<.32.
Consequently no base functional surcharge is active. Both opponent
maxima exceed `17/50+q`, and their menu branches are respectively base
and E, so neither is a constrained-Q inverse-threshold modification.
The E branch is unchanged by the functional construction in any case.
This explicitly checks the selected functional mechanism, not only its
simpler parameter predecessor.

## The upper field is unchanged and nonzero

Both bidders' own maxima exceed 43/100 throughout the box, so the common
capacity price is in its stream branch. Exact coordinate separation
from each of the eight cycle rectangles shows that no added flow changes
the field on this box.

Both radial maxima here are the physical item-1 coordinates w1 and v1.
The bidder-2 safe field can therefore be written

    phi_22 = N(w1,w2,v1,v2) / (2*w1^2*v1^2),

where N is reconstructed exactly from the archived 32 rational stream
coefficients. The separate verifier expands N at this new box center and
bounds every nonconstant monomial by its absolute coefficient times the
corresponding halfwidth powers. Its upper numerator bound is strictly
negative on the whole closed box. Dividing its absolute value by the
positive denominator's upper bound gives an exact rational number
`m>0` with `|phi_22|>=m` everywhere on the box.

Let Pi'_safe be the final common safe-item density. The local sum of
capacity and virtual-allocation slack is exactly

    Pi'_safe - beta*phi_22.

Since `Pi'_safe>=max(0,phi_22)` and
`min(beta,1-beta)>1/50`, this is at least `|phi_22|/50`.
Integration gives the exact positive lower bound

    S_capacity + S_virtual >= m/(50*625000000000000) > 0.

Its full rational numerator and denominator are in
`certificate/current_lower_flatness.json`; its numerical display is
approximately `3.7862102141371773e-19`. The small magnitude is immaterial
to the logical conclusion: this particular common dual has strictly
positive slack against the selected new lower mechanism. It remains an
unrestricted valid upper certificate, while the matching-certificate
problem remains open.

## Replay and source boundary

Run the read-only verifier

    python -B -X utf8 verifier/current_lower_flatness.py

The generation and subsequent normal replay both returned
`CURRENT_V4_6_1_LOWER_STRICT_DUAL_GAP_PASS`. The two external lower source
files are read-only dependencies, identified by SHA-256 in the new JSON.
No old lower artifact, `remaining_lottery_slack.py`, or old flatness JSON
was changed. The written mechanism proof plus exact polynomial bound
supply the continuum result; this is not a finite-grid optimality test.
