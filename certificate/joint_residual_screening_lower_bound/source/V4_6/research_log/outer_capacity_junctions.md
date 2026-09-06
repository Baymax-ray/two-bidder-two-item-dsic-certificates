# Actual occupied traces for the enlarged lottery region

This note supplies the actual-capacity hypotheses needed to apply the V4.6
inner-lottery certificate on the enlarged region
`Eplus={2/3<t<T, rho<c}`, for either bidder. The notation, complete mechanism,
and all-real feasibility proof are in `outer_lottery_strip.md`.

Fix an opponent report `(t,rho)` in Eplus and align item 1 with its high
coordinate. Write `k=t-q`, `A=2/3`. The actual residual satisfies

\[
r_1(x,1)=0\quad(0\le x<k),\qquad
r_1(x,c)=0\quad(A<x<t).
\]

These are pointwise statements, not almost-everywhere replacements of the
mechanism at the charged lines.

On the top trace the other bidder sees report `(x,1)`. This report is outside
Q, outside Eplus, and outside the additional root free region (whose maximum
is at most `1/2`). Its menu is therefore retained. All frozen increments
vanish on this top trace. Its high-item price is `d` for `x<=c`, and `x+q`
for `x>c`. Both prices are strictly below `t` when `x<k`. The low singleton
is unaffordable and the bundle is strictly dominated by the high singleton
because its upgrade threshold is at least `c>rho`. The opponent thus receives
item 1 surely, including `x=c`; this proves the first residual identity.

On the interior junction trace `(x,c)`, `A<x<t<T`. It is outside Q because
`x>A`, and explicitly outside Eplus because its low coordinate equals `c`.
It is also outside the root free region. The retained shared-base high-item
price is exactly `x`. The inherited joined-threshold rule on this face has
zero high-item increment: only its low and bundle prices change. The fixed
opponent's own high value is `t>x`, while its low value is strictly below
`c`. Thus its high singleton is uniquely preferred and has positive utility.
It receives item 1 surely, proving the second identity.

Keeping the old rule at `rho=c` serves two separate purposes. It avoids
uncontrolled old bundle ties on the boundary of the new primal splice, and
it retains the exactly occupied junction trace charged by the full inner
certificate. The line is not priced by convention after changing its
allocation.

The root free-region splice does not change either occupied trace, since
the opposing reports there have maximum greater than `A` or equal to one.
Other capacity changes introduced by that splice preserve the new lottery
menu's pointwise feasibility. A nonnegative matching inner price can charge
positive residual capacity only where the candidate consumes it fully; the
only candidate-zero charged constraints required by the inner theorem are
the two occupied traces above. Hence these verifications, together with the
complete primal feasibility proof, are the interface for the separate full
randomized screening certificate. No hypothesis of a finite global menu or
finite type grid is involved.

`outer_lottery_strip.py` checks 144 exact rational instances of the occupied
trace identities in both bidder directions, in addition to its primal
boundary cases. The universal assertions rely on the price formulas just
proved, not on those finite checks.
