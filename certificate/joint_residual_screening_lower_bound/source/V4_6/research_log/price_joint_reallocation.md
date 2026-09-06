# A capacity-price obstruction produces a profitable joint reallocation

This route does produce a complete profitable primal change. It lowers a
lottery payment on a positive-area collection of bidder-2 menus, and pays
for the resulting capacity release by an entry fee on a thin collection
of bidder-1 menus. The first change has a positive first-order revenue
effect. The compensating change has only a second-order revenue cost.
At the explicit rational parameter below, the complete auction improves
the reference mechanism by at least

\[
\boxed{\kappa=\frac{26902077489}{12500000000000000000}
             =0.00000000215216619912>0.}
\]

The displayed number is a rigorous lower bound on the increment, not its
exact value. The full pointwise mechanism is specified here; its exact
rational-plus-logarithm increment is evaluated in
`price_joint_exact_revenue.md` and replayed by `price_joint_revenue.py`.
The small conservative magnitude is not the main
structural conclusion: even after its full conditional lottery problems
are solved, the reference mechanism admits a strictly profitable joint
change. Its conditional certificates cannot be assembled into a matching
common support without an additional primal change.

## 1. Reference mechanism and exact deformation

Start from the V4.6 reference `outer_bundle_reoptimized.mechanism`, which
applies the E-plus lottery extension, the reverse free-capacity splice,
and the G bundle exchange with its bidder-2 Q compensation. The last
exchange changes bidder 1 only at opponent maxima at most 1/2 and changes
bidder 2 only at opponent maxima at most 2/3. It therefore leaves both
changed menu collections below unchanged. Write

\[
c=137/500,\quad q=113/500,\quad
J=[7/10,71/100],\quad \varepsilon=9/10000.
\]

Use one fixed physical item orientation; no unproved symmetrization is
made. Bidder 1 reports \(w=(t,\rho)\), bidder 2 reports \(v=(x,y)\).
Let

\[
W=J\times[0,1/5],\qquad
S_\varepsilon=[7/10-4\varepsilon,71/100]
 \times[c-2\varepsilon,c+4\varepsilon].
\]

Every displayed rectangle is closed. Outside the stated menu collections
retain the reference mechanism and its complete tie rules.

* For bidder 2, when its opponent w is in W, retain the five lottery-menu
  options in the order empty, safe singleton, scarce singleton, bundle,
  lottery. Reduce only the lottery payment by epsilon, from
  \(t+\beta(t)c\) to \(t+\beta(t)c-\varepsilon\). Choose the first utility
  maximizer.
* For bidder 1, when its opponent v is in S, add epsilon to every nonempty
  option of its entire reference menu. The empty option keeps price zero.
  Choose empty whenever its reference maximum utility is at most epsilon;
  otherwise retain its reference allocation and add epsilon to its payment.
  Retained positive ties use the reference priority.

The second instruction is exactly a complete entry-fee menu, not a
report-dependent alteration of a selected allocation. The whole menu has
been shifted before maximizing. It always retains the old allocation or
chooses empty.

The rational lottery parameters are those in the inner-certificate note:

\[
\alpha=3t-2,\quad
\delta=q+3q^2/4-3qt/2+\alpha^2/16,\quad
\beta=\frac{\alpha}{\alpha+2\delta},\quad
L=\delta+\alpha/2,\quad Y=c+L.
\]

Throughout J, exact endpoint and derivative inequalities give

\[
\frac35<\beta<\frac34,\quad
L\ge\frac{1213}{15625},\quad
\frac{\alpha L}{4}\ge\frac{1213}{625000},\quad
Y+4\varepsilon<1/2<B=1/2+\delta.
\tag{1}
\]

Both rules remain complete DSIC/IR menus on the continuous own-report
square, including all exceptional reports. Prices are nonnegative.
Rational Borel parameters and finite priorities prove measurability.

## 2. Complete joint-feasibility proof

It suffices to examine a newly selected bidder-2 lottery; other bidder-2
allocations are unchanged, while bidder 1 only contracts. A selected new
lottery satisfies

\[
c-\varepsilon/\beta\le y\le Y+\varepsilon/(1-\beta),\qquad
x+\beta(y-c)-t+\varepsilon>0.
\tag{2}
\]

The first inequalities follow by comparison with the unchanged scarce
singleton and bundle; the strict last inequality follows from empty-first
priority. Moreover its x coordinate is at least
\(1-t/2-4\varepsilon\ge.645-4\varepsilon>1/2\).
Thus this change never meets the reverse free-capacity splice.

For w in W, the reference bidder 1 can take only its scarce singleton at
the reports (2). Its safe singleton costs at least 1/2, above rho. Its
bundle costs at least b=91/100, at least t+rho, and zero utility is rejected.
On an E-plus row a chosen lottery would require rho at least c; W has
rho at most 1/5<c. On retained rows these facts follow from the frozen
base prices and nonnegative increments. The reference G and F changes
to bidder 1 have opponent maximum at most 1/2 and are absent throughout
the entire changed lottery cell.

Whenever that scarce singleton is taken, its price satisfies

\[
P\ge P_0(x,y):=\max\{x,x+y-c\}.
\tag{3}
\]

For retained rows with y<1/2, the base singleton price is
\(\max(a,x,x+y-c)\); increments are nonnegative. On an E-plus row
y<c it is exactly x, again satisfying (3).

Suppose there could have been a capacity conflict before the entry fee.
Then t>P>=P0. Combine this with (2). Below c it forces
\(c-y<\varepsilon/\beta<2\varepsilon\). Above c it forces
\(y-c<\varepsilon/(1-\beta)<4\varepsilon\). Also x<t<=71/100,
and (2) gives x>7/10-4epsilon. Thus every possible conflict lies inside
the explicitly charged rectangle S, including its bounding faces.

On S the old bidder-1 utility for its only possibly winning option obeys

\[
t-P\le t-P_0
 <x+\beta(y-c)+\varepsilon-P_0\le\varepsilon.
\]

The entry-fee rule therefore chooses empty. This proves scarce capacity
feasibility pointwise. The safe item is free whenever the newly selected
lottery could cause a change, by the preceding low-value exclusions.
When the lottery is selected, toss its Bernoulli(beta) coin for the safe
item; every realized allocation is feasible. Equalities are resolved by
the explicit empty-first rules, so no almost-everywhere repair is used.

For a strict owner-transfer witness, take

\[
w=(7/10,1/10),\qquad v=(7/10-\varepsilon/2,c).
\]

The reference allocation is \(((1,0),(0,0))\). The new allocation is
\(((0,0),(1,3125/4852))\). All relevant choices are strict. The gain and
the transfer therefore persist on neighborhoods; this is not a null-report
operation.

## 3. The full lottery revenue effect

For a fixed w in W, the original lottery cell is

\[
c<y<Y,\qquad x>t-\beta(y-c),
\]

with area \(A_L=(1-t)L+\beta L^2/2\). On this cell the changed utility
increases by exactly epsilon. Its right-edge trace increases by epsilon
on an interval of length L. The enlarged lottery cell differs from the
old cell by area at most 7epsilon: lower and upper y expansions contribute
at most 2epsilon and 4epsilon, and the shifted x boundary contributes at
most epsilon. The utility increment is everywhere between zero and epsilon.

The exact uniform revenue identity
\(R=\int u(1,y)dy+\int u(x,1)dx-3\int u\) therefore yields

\[
\Delta R_2(w)\ge\varepsilon[L-3A_L]-21\varepsilon^2
 =\varepsilon\frac{\alpha L}{4}-21\varepsilon^2.
\tag{4}
\]

No affected buyer is omitted: the volume term includes displaced high
singleton and bundle purchasers as well as new lottery customers.
Independently integrating those cells gives the sharper exact formula

\[
\Delta R_2(w)=\varepsilon\frac{\alpha L}{4}
 -\frac{\varepsilon^2\alpha}{4\beta(1-\beta)}
 -\frac{\varepsilon^3}{2\beta(1-\beta)^2}.
\tag{5}
\]

Formula (5) was independently derived by the inner-certificate route and
provides an exact one-variable integral for the bidder-2 increment. Using
alpha at most 13/100 and the beta bounds in (1), it implies the stronger
uniform lower bound used at the selected epsilon:

\[
\Delta R_2(w)\ge\frac{1213}{625000}\varepsilon
 -\frac{13}{60}\varepsilon^2-\frac{40}{3}\varepsilon^3.\tag{5a}
\]

The first derivative is alpha L/4;
it is **not** lambda=alpha(c+L/4). The extra alpha*c term in the raw corner
price is canceled by the changed convex-trace slack.

## 4. Paying for the release costs only second order

Write lambda=3|D0|-1 for the reference no-sale area. For every row occurring
in S, a common entry fee h leaves the internal positive-option boundaries
unchanged and expands the no-sale area by Ch+h^2/2, where C is that row's
bundle price. Both right and top traces stay strictly positive for
0<=h<=epsilon. Integrating the revenue identity therefore gives the exact
conditional entry-fee change

\[
\Delta R_{\rm fee}=-\lambda\varepsilon
 -\frac32C\varepsilon^2-\frac12\varepsilon^3.\tag{6}
\]

For y<c the reference row is E-plus. Its lambda is
alpha(c+L/4), bounded above by 1/25 on the whole x interval, and C<101/100.
For y>c put z=y-c. The frozen tariff has prices

\[
A=x+z+f,\quad B=1/2+z+f,\quad C=x+c+z+f,
\]

where the literal first-match table gives f=7/2000 below sum 39/40
(row B13.1), f=7/10000 between sums 39/40 and 49/50 (B14.1), and f=0 above
49/50. The complete strip has sum above 97/100, and normalized coordinate
z/(x+z-501/1000)<1/8, using the frozen table's original split constant,
so no other row is used. Here
lambda=3[AB-(A+B-C)^2/2]-1. It increases in x and along each moving upper
boundary x=H-z. Its three maxima, at z=4epsilon, are respectively

\[
-1949513/200000000,\quad-2078141/200000000,\quad-3023/3125000.
\]

They are negative; also C<1. Integrating the conservative consequences of
(6) over the lower and upper strip widths 2epsilon and 4epsilon gives

\[
\Delta R_1\ge-(1/100+4\varepsilon)
 \left[\frac2{25}\varepsilon^2+
       \frac{903}{100}\varepsilon^3+3\varepsilon^4\right].\tag{7}
\]

Expectation adds (5a) and (7), although the allocation changes interact at
the same profiles. Since |W|=1/500,

\[
\begin{aligned}
\Delta R\ge&\frac1{500}
 \left(\frac{1213}{625000}\varepsilon-
       \frac{13}{60}\varepsilon^2-\frac{40}{3}\varepsilon^3\right)\\
&-(1/100+4\varepsilon)
 \left[\frac2{25}\varepsilon^2+
       \frac{903}{100}\varepsilon^3+3\varepsilon^4\right]\\
=&26902077489/12500000000000000000>0.
\end{aligned}
\]

An exact characterization of the actual increment is obtained by replacing
(4) with (5), integrating it over W, and adding
\[
\int_{v\in S}\left[
\varepsilon\Pr_w(u_1(w;v)>\varepsilon)
-\mathbb E_w[p_1(w;v)1_{0<u_1(w;v)\le\varepsilon}]
\right]dv.
\]
Every integrand is specified by the finite reference menus and fixed tie
rules. The companion exact-revenue note evaluates this integral as a
rational number plus three rational multiples of logarithms, independently
of the conservative strict bound above.

The initial discovery used epsilon=10^-6 with the coarser cell bound (4)
and the estimate 8epsilon for conditional entry-fee losses. That earlier
trial had guaranteed gain 209963/62500000000000000. It is not the selected
parameter. Exact integration justified increasing epsilon to 9/10000;
no optimality within the whole epsilon family is claimed.

## 5. What the common-price failure taught the primal search

The E inner certificate prices an own-report line y=c, consumed by the
other bidder on a positive interval of x. Reusing that consumed singular
line as a common capacity price fails the opponent-null menu-deletion
condition. The successful response here changes both menus. It spends
only O(epsilon^2) revenue on the thin family of conditional menus that
must release the conflicting capacity, while obtaining O(epsilon)
revenue from the complete lottery menus. The construction identifies the
missing outer allocation direction rather than attempting another smooth
fit around the same candidate.

The fixed-reference inner certificate on W does not survive this change:
the compensation deliberately releases part of its formerly binding
line y=c. The unchanged five-option menu was fully inner-optimal against
the old residual; the lower payment uses the new residual. There is no
conflict between that theorem and the strict joint gain. No matching
common certificate or unrestricted auction optimum is claimed here.

Run `python -B -X utf8 V4_6/verifier/price_joint_reallocation.py` from the
auction output directory. The saved certificate records the exact gain
bound and 315 named rational boundary checks. The continuum proofs above,
not the regression points, establish complete DSIC/IR and feasibility.
