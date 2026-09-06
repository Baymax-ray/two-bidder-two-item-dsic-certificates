# V4.6: a profitable strip outside both Q and E

The V4.5 lottery splice can be extended to a strictly larger, positive-area
opponent region. This is an improvement of complete conditional menus with
the opposite bidder initially fixed, followed by a proof that the two changes
are compatible. The separate `inner_lottery_certificate.md`, combined with
the actual occupied-trace proof in `outer_capacity_junctions.md`, now proves
that these resulting menus solve the full randomized inner problem.

Use the frozen V4.02 constants

\[
a=159/250,\quad b=91/100,\quad c=b-a=137/500,\quad
s=142/125,\quad d=s-a=1/2,\quad q=s-b=113/500.
\]

Write \(A=2/3\), \(T=613/750\), \(U=839/750\). For
\(A<t<T\), use exactly the V4.5 functions

\[
\delta(t)=\frac9{16}(T-t)(U-t),\qquad
\beta(t)=\frac{3t-2}{3t-2+2\delta(t)}.
\]

The enlarged region is

\[
E^+=\{w:A<\max(w)<T,\ \min(w)<c\}.
\]

It strictly contains the old \(E\), whose low-coordinate cap was
\(b-t\). The added region is

\[
E_{\rm add}=\{w:A<t<T,\ b-t<\rho<c\}.
\]

The face \(\rho=c\) explicitly retains the full old rule: the frozen base
can select a bundle on this face at a positive-utility tie. This face is not
silently discarded when proving pointwise feasibility.

## 1. Actual residual geometry on the added strip

Suppose the retained bidder has own report \((t,\rho)\), with \(t>A\)
and \(\rho<c\). Its low singleton is unaffordable because every retained
singleton price is at least \(d>c\). Its bundle is strictly worse than its
high singleton: at an arbitrary other report \((x,y)\), the base price
difference satisfies

\[
P^0_{12}-P^0_1=b-\min(a,s-y)\ge b-a=c>\rho.
\]

The inherited V3 increments preserve this inequality because the bundle
increment is the maximum of the two singleton increments. Thus the retained
bidder can receive only its high item at every opposing report, including
all own-report and other-report ties. In particular, the other item has full
residual capacity. The condition \(t+\rho\le b\) was sufficient but was not
necessary for this conclusion.

Moreover, throughout this strip the pivot is \(t-a\), because
\(\rho<c\), and the other bidder's common-base prices are exactly

\[
P_1=t,\qquad P_2=d,\qquad P_{12}=t+c.
\]

They do not depend on \(\rho\). Its possible high-item occupation hole is
therefore the same V4.5 majorant:

\[
\{y\le d,\ x\le t,\ x+y\le t+c\}
\ \cup\ \{y\ge d,\ x\le t-q\}.
\]

The exact V4.5 menu and hole inequalities apply without alteration. The
five options, in tie priority order, are

| Allocation | Price |
|---|---:|
| \((0,0)\) | \(0\) |
| \((0,1)\) | \(d+\delta\) |
| \((1,0)\) | \(t\) |
| \((1,1)\) | \(t+c+\delta\) |
| \((1,\beta)\) | \(t+\beta c\) |

Align item 1 with the unique larger opponent coordinate, and rotate back
after menu selection. The inequality \(\beta(q+\delta)\le q\) ensures that
the lottery loses to empty or the safe singleton throughout the entire
possible occupation hole. These preceding options settle the equality cases.

## 2. Both bidders may use the extension

Replace each bidder's entire conditional menu on \(E_{\rm add}\), retaining
V4.5 elsewhere. Conditional menu maximization immediately gives pointwise
DSIC and IR for each bidder; there is no interpolation of own-type choices.
The following cases give joint feasibility.

* If the reverse row is a retained subset of the shared base, Section 1 and
  the V4.5 hole proof apply.
* If both reports lie in \(E^+\) with the same high-item orientation, each
  own low coordinate is below \(c\). The lottery is strictly worse than the
  high singleton, and the bundle is strictly worse than that singleton
  because its upgrade price is \(c+\delta>c\). A safe singleton is
  unaffordable. Only the bidder with strictly larger high coordinate can buy
  the common high item; equal high reports select empty at zero utility.
* If both reports lie in \(E^+\) with opposite orientations, each aligned
  scarce coordinate is below \(c<t-q\). The lottery, high singleton, and
  bundle cannot maximize positively. Only the distinct safe singletons can
  be bought. This proves samplewise feasibility of all lotteries as well.
* It remains to check bidder 1's new row against bidder 2's inherited Q
  override. Write bidder 1's Q report as \((x,y)\), aligned with bidder 2's
  report \((t,\rho)\in E^+\). Since \(x\le A<t\) and \(x+y\le b<t+c\),
  bidder 1 cannot choose the high singleton or bundle. A positive lottery
  choice requires \(y>c\) and
  \(x>t-\beta(y-c)\), implying \(x+y>t+c>b\), also impossible. Thus only
  the safe singleton is possible. If chosen, \(y>d+\delta>d\) and
  \(x\le b-y<y\). Bidder 2's Q menu has its high direction along physical
  item 2. Its value \(\rho<c\) is below both the high singleton price and
  the bundle upgrade threshold \(y-q>c+\delta\), so it cannot consume
  physical item 2. At the singleton's entry tie bidder 1 chooses empty.

The parameter functions are rational and Borel on their open region;
finitely many Borel utility comparisons and explicit first-maximizer priority
prove measurability. Prices are nonnegative, and accepted prices do not exceed
reported allocated value. For a chosen lottery the scarce item is allocated
surely and a Bernoulli(\(\beta\)) coin allocates the available safe item.
All exceptional faces use a complete frozen rule.

The exact evaluator is `verifier/outer_lottery_strip.py`. It constructs this
whole auction, not only its changed region. The rational boundary cases
supplement the all-real proof; they do not replace it.

## 3. Exact revenue and strict improvement

Let \(q_o=227/1000\), and put

\[
\delta_o(t)=\tfrac12-c+\tfrac34q_o^2-\tfrac32q_ot,\qquad
t_o=\frac{1/2-c+3q_o^2/4}{3q_o/2}.
\]

On the entire added strip both frozen conditional menus have the same
V4.02 prices as on the original E fibers. Thus V4.5's complete-cell revenue
identity applies, with strictly positive conditional gains

\[
g_1(t)=(\delta-\delta_o)^2+\delta_o(3t-2)^2/8
\quad(A<t\le t_o),\qquad
g_2(t)=\delta^2\quad(t_o\le t<T).
\]

The newly available low-coordinate width is
\(c-(b-t)=t-a>0\). Therefore the exact whole-auction gain is the positive
rational number

\[
\Delta_{\rm strip}
=4\int_A^{t_o}(t-a)g_1(t)\,dt
+4\int_{t_o}^{T}(t-a)g_2(t)\,dt>0.
\]

The factor four accounts for both item orientations and both bidder payment
changes. It does not presume statistical independence between allocations.
The verifier evaluates these polynomial integrals in rational arithmetic and
independently repeats them using dictionary polynomials and the frozen
continuous-cell polygon integrator. The certificate contains the rational
gain, before/after-cutoff components, coefficients, and a revenue enclosure.

A strict witness is \(((.7,.25),(.72,.29))\). The opposing sum is .95, so it
lies outside both Q and the original E. V4.5 sells only the high item to
bidder 2; the extension instead selects the genuine lottery strictly.

## 4. Consequences and limitations

The full randomized Q certificate survives this extension for the same
reason it survived V4.5: the reverse row can change only Q's high item at
opposing scarce-item value \(\rho<c<A\) and other coordinate \(t<T<1\).
Both the high-coordinate volume price and its top-edge price miss this
change. The unchanged Q menu is still feasible and matches its prior support.

The positive conditional gain identifies an actual residual-menu defect on
\(E_{\rm add}\); no change to the opponent's allocation was necessary to
obtain the one-sided gain. A purported capacity support for the old menu on
this region must fail the corresponding full inner optimality test. This
is a constructive certificate rejection, not an inference from a failed
finite basis. The full unrestricted inner certificate was subsequently
obtained in `inner_lottery_certificate.md`: candidate feasibility and the
two exactly occupied traces proved in `outer_capacity_junctions.md` verify
all its hypotheses for both bidders on Eplus. It also survives the later
free and bundle-exchange splices, whose changed report regions miss those
traces and preserve the candidate's pointwise feasibility.

No claim is made here about opponents with \(\rho>c\), where the other item
need not be free, or about \(t\ge T\), or about a matching auction upper
bound. The added strip is selected by a proved residual-capacity identity,
not by extending a lottery into a region with unchecked item availability.
