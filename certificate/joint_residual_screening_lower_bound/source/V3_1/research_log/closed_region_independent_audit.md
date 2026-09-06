# Independent final audit: the closed solved opponent region

**Outcome:** the explicit measure certificate and the closed-region
implementation pass independent proof inspection and read-only replay.
No blocking mathematical gap was found. This note extends the actual
scope checked in `forced_gradient_constraints.md`; its rectangle-majorant
lemma remains restricted to `t<=a`.

Audited `research_log/constrained_screening.md`,
`verifier/constrained_screening_verify.py`, and the root implementation
`verifier/constrained_candidate.py`. These files were not modified.

## 1. The general screening theorem and its endpoints

The measure identity

`<pi,r>-R=<pi,r-a>+3 integral_(D_0)u`

is valid for arbitrary competing randomized DSIC/IR mechanisms. It follows
from exact horizontal and vertical envelope integrations and a separate
top-edge envelope, not a volume-a.e. gradient substitution. The signs,
three equal areas, zero boundary terms for `F`, and all price coefficients
are correct. The proof includes unnormalized IR utilities: the remaining
utility term still has the required nonnegative sign.

For `k_min=(2-sqrt(2))/3 <= k <= A=2/3`, the condition `B<=2/3` makes
`f<=0` through `A`, so its zero total integral implies `F>=0`. At `k_min`,
the price below the excluded top segment vanishes; the certificate also
matches full-capacity SJA. At `k=A`, the bundle discount becomes zero,
`B=1/2`, `C=7/6`, and the exact value is `17/36`. No strict-discount step is
needed in the analytic proof at that endpoint. The stated priority still
chooses no item 1 at `x=k`, even when the residual there is zero.

The positive price supports match the candidate in Theorem 1, so the
certificate proves its full inner optimality, rather than merely a
four-menu upper bound. The accompanying polynomial interpolation is an
algebraic identity check with the stated degree bound, not a finite type
grid argument.

## 2. Direct feasibility through t=2/3

Use the frozen V3 constants `a,b,c,d,q` from the preceding notes. Fix the
orientation `w=(t,rho)` with

`d<t<=A=2/3`, `0<=rho<=b-t`, `k=t-q`,

and bidder 2 report `(x,y)`. Bidder 1 can receive only item 1: its low
singleton is unaffordable, its bundle utility is nonpositive, and V3
rejects zero-utility ties. All final V3 prices are nonnegative increments
of the affine base prices.

The earlier assertion that all capacity holes lie in `x<=k` is **not used**
for `t>a`. Instead inspect every way the new menu can allocate item 1:

* If its item-1 singleton is selected, positive utility implies `x>A`.
  For `y<=d`, the base price satisfies `P1>=x`; for `y>=d`, it satisfies
  `P1>=x+q`. In either case `P1>t`, so bidder 1 is empty.
* If its bundle is selected, positive utility and the safe tie priority
  imply `x>k` and `x+y>C`. For `y>=d`, the base price is at least
  `x+q>t`. For `y<=d`, it is at least `x+y-c>C-c>=t`.

The last inequality is uniform on the entire interval. With
`C(t)=5/6+3(t-q)^2/4`, the function `C(t)-c-t` is decreasing up to `A`
because `3(t-q)/2-1<0`. Its minimum is exactly

`C(A)-c-A=150587/4000000>0`.

Thus the candidate is pointwise feasible through `t=A`, including
`t+rho=b`, all own-report ties, and the transition from `t=a`. This
argument does not identify the complete interior hole and does not need
to: the candidate never attempts an actually occupied item.

## 3. Matching the actual residual to the same global support

The support requires capacity saturation only where its density is
positive. Those conditions hold on the extended range:

* On `x>A`, the price bound just proved makes the actual first-item
  residual one, and the candidate allocates it surely.
* The exact top-edge V3 price remains `d` for `x<=c` and `x+q` for `x>c`.
  Therefore the residual is zero for `x<k` and one for `x>=k`. The
  candidate has the same allocations except possibly at the single safe
  tie, which has zero mass under `F(x)dx`.
* The second-item residual is one everywhere, and the candidate allocates
  it on the positive support of `pi_2`.

Also the candidate utility vanishes on `D_0`. Hence the same identity
proves full randomized inner optimality and a matching global conditional
capacity support at the actual residual for `d<t<=2/3`, `rho<=b-t`.
This extension uses feasibility and support saturation; it does not assert
that the actual residual satisfies the stronger interior-cap hypothesis
of the diagnostic class in Theorem 1.

For `t<=d` with `t+rho<=b`, the actual first bidder is empty on the whole
own-report square, including zero-utility boundaries, and SJA solves the
full-capacity inner problem. Combining both cases and both orientations
gives the closed opponent region

`Q={max(w1,w2)<=2/3, w1+w2<=b}`.

Its exact area is `63871/180000`. The conditional certificates integrate
over this region to bound its contribution. They do not by themselves
certify the inner contribution from opponent reports outside `Q`, nor
the outer bidder's optimality against the same price measure.

## 4. Code correspondence and verification

The root code tests the closed set `Q`, uses full-capacity SJA when
`t<=d`, and the constrained menu otherwise. The constrained high coordinate
is unique because `t>d` and `2d>b`. Its positive tie priority favors the
low-coordinate item before the high-coordinate item or bundle, giving the
safe allocation at `x=k`. The first bidder is unchanged. On the complement
of `Q`, the entire V4 continuation is returned.

Normal read-only executions of both `constrained_screening_verify.py` and
`constrained_candidate.py` passed. The independent exact checks above also
verified `k_max=1319/3000`, the derivative bound `-681/2000<0`, and the
strict price margin `150587/4000000`. These replays accompany the continuum
proofs; their finite report examples do not prove all-report feasibility.

The implementation changes some zero-measure boundary fibers as well as
the positive-volume revenue region `d<t<t1, rho<b-t`. The closed definition
of `Q` and its explicit branch rules govern those reports. A description
of the strict revenue-integration region must not be read as the complete
pointwise modification set.
