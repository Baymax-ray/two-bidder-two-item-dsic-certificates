# Independent audit of the corner release and lottery payment cut

The substantive joint construction in `price_joint_reallocation.py` and
`price_joint_reallocation.md` passes this independent mathematical audit.
Its gain is an exact strictly positive lower bound, not an evaluation of
the full increment. The separately evaluated rational-plus-log increment
is recorded by `price_joint_revenue.py`. The selected parameter is now
epsilon=9/10000; the audit below covers this larger parameter. It used
the complete menu changes, not only the named rational examples.

## Full conditional gain

Independent integration of the enlarged lottery cell gives

\[
\Delta R_2(t)=\frac{\alpha L}{4}\varepsilon
-\frac{\alpha}{4\beta(1-\beta)}\varepsilon^2
-\frac1{2\beta(1-\beta)^2}\varepsilon^3.
\]

This was derived independently before reviewing the joint-route note and
is replayed as a polynomial identity in `inner_lottery_certificate.py`.
It includes lost payments of high-singleton and bundle buyers switching
to the cheaper lottery. In particular the derivative is alpha L/4, not
the raw corner mass lambda. The latter includes a trace-convexity slack
which changes at first order.

The initial coarse bound in the joint note is also valid: the
enlarged cell has at most 7epsilon more area, its utility change is at
most epsilon, and the exact utility-revenue identity supplies the stated
21epsilon-squared error bound. The original lottery's right-edge trace
changes by epsilon throughout an interval of length L; its top trace is
unchanged because the enlarged upper junction is below 1/2. For the
selected larger epsilon, positivity instead uses the sharper exact
formula above. The uniform bounds beta>=3/5, 1-beta>=1/4 and alpha<=13/100
give a quadratic coefficient at most 13/60 and a cubic coefficient at
most 40/3.

## All-real capacity check

For t in [0.7,0.71] the new lottery's entire winning region satisfies
x>=0.645-4epsilon>1/2. Therefore neither the free-region nor the bundle
exchange bidder-1 splice is present anywhere in that region: those
opponent regions have both coordinates at most 1/2. This is stronger than
checking only the fee rectangle S. A broad assertion that arbitrary
changes confined to opponent maxima at most 2/3 are harmless would not
suffice, because the new cell can contain x between .645 and 2/3.

At these winning reports bidder 1's low own value is at most .2<c. On
retained rows its safe item is unavailable as a positive choice and its
bundle is dominated or nonpositive. On the possible Eplus rows, the own
low value below c excludes its lottery and bundle upgrades. Thus only
the scarce item can conflict. Its conditional price satisfies
P>=max(x,x+y-c).

If the new lottery wins and bidder 1 previously buys that item, comparing
the lottery with empty, the high singleton, and the bundle forces

\[
c-2\varepsilon<y<c+4\varepsilon,\qquad
0.7-4\varepsilon<x<0.71,
\]

and the old bidder-1 utility is strictly less than epsilon. Hence all
possible conflicts fall within the charged closed rectangle S, and the
full entry-fee menu selects empty at every such report. Weak endpoint
inequalities are covered by the specified first-maximizer rules. Outside
these conflicts the bidder-1 change is a contraction. The safe marginal
is free throughout the new lottery region, so every Bernoulli realization
is jointly feasible.

## Full entry-fee cost

For each opponent report in S there are at most four nonempty menu
options, each having at least one unit allocation marginal. The set where
one such option has utility in (0,epsilon] has area at most epsilon by
integrating along that coordinate. The set of dropped buyers therefore
has area at most 4epsilon, even when its boundary intersects several old
menu cells. Their old payments are at most 2 by IR. Every retained buyer
pays epsilon more, so a conditional loss bound of 8epsilon is valid.
This checks the complete entry-fee effect, rather than discarding the
information-rent changes of buyers who keep their original allocations.

This coarse 8epsilon bound remains valid, but is not sufficient to prove
positivity at the selected larger parameter. A stronger complete fee
calculation is therefore necessary.

On an Eplus row a common entry fee e on all nonempty options changes the
no-sale area by Ce+e^2/2 while the high/lottery, lottery/bundle and
bundle/safe boundaries stay fixed. Both top and right traces remain
positive, so the exact conditional revenue change is

\[
\Delta R_{\rm fee}=-\lambda e-\frac32Ce^2-\frac12e^3.
\]

Below y=c all rows in S are Eplus, and monotonicity of lambda and C
gives lambda<1/25 and C<101/100. Above y=c the literal frozen rows are
B13.1, B14.1, and zero tariff. Writing z=y-c and f for the row fee,
their prices are A=x+z+f, B=1/2+z+f, C=x+c+z+f. Their no-sale mass is
lambda=3[AB-(A+B-C)^2/2]-1. Its x derivative is 3B>0; along an upper
cell boundary x=H-c-z the derivative in z is 3(x-q)>0; for the final
constant-x boundary it is 3C>0. The three maximum values are strictly
negative, so lambda<=0 throughout these cells. The same exact fee
identity applies, with C<1.

Integrating those bounds gives the full conditional-menu fee loss bound

\[
(1/100+4e)\{(2/25)e^2+(903/100)e^3+3e^4\}.
\]

Combining this bound with the exact lottery formula at e=9/10000 gives

\[
\Delta R\ge\frac{26902077489}{12500000000000000000}>0.
\]

The full exact increment calculation separately integrates these same
entry-fee identities and the lottery's rational function. The latter
reduces to rational terms plus logarithms by polynomial partial fractions.
The algebraic reconstructions and signed logarithm remainder bounds are
exact. One source-hypothesis correction was requested during audit: the
frozen normalized-rho denominator uses old d=501/1000, not the current
d=1/2. The corrected row-membership bound remains strictly below 1/8;
the tariff cells, fee values and revenue expression do not change.

## Conditional-certificate scope after the joint change

The payment cut intentionally releases the previously binding corner
capacity, so the original full Eplus inner equality is not a certificate
for the changed rows. Moreover the entry fee can release the corner
trace for bidder-2 opponent reports just outside W: if
x in [J0-4epsilon,J1] and 0<t-x<=epsilon, then

\[
J0-4\varepsilon<t\le J1+\varepsilon.
\]

Thus preserving old inner optimality merely on the complement of W
would be too broad. A sufficient preserved Eplus region for bidder 2
excludes this wider high-value band. Bidder 1's conditional menus on S
are also changed and do not retain an equality certificate merely by
being outside W. The global capacity-support inequalities themselves
remain valid at every residual; what may fail is their tightness at
the final mechanism.

The final Q certificate's occupied bottom, vertical and top traces are
disjoint from this corner operation. More specifically, at own w in Q
and opponent v in S, bidder 1 can only buy physical item 2: the other
singleton costs more than 2/3, and the bundle and lottery require total
value greater than x+c>b. A positive item-2 choice implies w2>1/2, so
that item is the scarce item in the Q alignment. Below y=c its price is
at least 1/2 and therefore k=w2-q>c>=y. Above y=c its price is at least
1/2+y-c, again giving k>y. Thus every released capacity lies at aligned
scarce report y<k and safe report x near .7. The scarce volume density
is zero there; the top and bottom lines are absent; and the new safe
vertical line is at scarce report 1/2 rather than y near c. Every Q
support therefore prices the capacity change at zero. Candidate menus
remain feasible and unchanged, so all restored Q supports remain tight.

None of these statements establishes a matching common-price upper bound
for the unrestricted auction.
