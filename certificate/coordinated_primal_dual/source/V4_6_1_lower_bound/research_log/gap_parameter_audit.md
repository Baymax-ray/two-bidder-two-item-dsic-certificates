# Independent allocation and conditional-support audit of the rebuilt family

This audit concerns the final parameter choice

\[
a=A=2/3,\quad c=47/150,\quad b=49/50=A+c,
\quad d=1/2,\quad s=7/6=A+d,\quad q=14/75=d-c.
\]

It does not reuse the old V3 fees, V4.6 free/bundle patches or final corner
perturbation. The candidate has only shared affine-base menus, symmetric
full Q menus, and symmetric Eplus menus. The main revenue evaluation is
separate from this audit.

The old-baseline branch `gap_low_square.py` remains a separate mechanism.
Its proposed upper low-square extension b<z<=A+c is now empty because
b=A+c. Symmetric Q already incorporates the fully optimized low-square
menus; there is no additional gain to count from that branch here.

## Definitions needed for the audit

For a report v=(x,y), set

\[
H(v)=\max(0,x-A,y-A,x+y-b).
\]

The base prices are

\[
P_1=H+\min(A,s-y),\quad P_2=H+\min(A,s-x),\quad P_B=H+b.
\]

They are the menus of the common nine-outcome affine maximizer. Base-base
profiles use a common maximizing allocation; zero-utility allocations
are discarded. This choice is necessary for the simple boundary arguments
below. Choosing incompatible independent base maximizers is not justified.

Define the closed region

\[
Q=\{\max(w)\le A,\quad w_1+w_2\le b\}.
\]

For opponent w in Q with maximum t<=1/2, the Q menu is
`(A,A,max(b0,sum(w)))`, where b0=(4-sqrt(2))/3. For t>1/2, align the first
item with w's high coordinate, put k=t-q and C0=5/6+3k^2/4, and use
`(A,C-k,C)` with C=max(C0,sum(w)).

Define the open high/strict low strip

\[
E^+=\{A<t<T,\quad\rho<c\},\quad
T=178/225,\quad U=26/25.
\]

It uses the complete empty/safe/scarce/bundle/lottery menu

\[
(0,0;0),\ (0,1;B),\ (1,0;t),\ (1,1;C),\ (1,\beta;t+\beta c),
\]

where delta=9(T-t)(U-t)/16, alpha=3t-2,
beta=alpha/(alpha+2delta), B=1/2+delta, C=t+c+delta,
L=delta+alpha/2, Y=c+L, and j=1-t/2.
For every strict Eplus row,

\[
0<\beta<1,\quad c<Y<1/2,\quad j>1/2,
\quad 1/2<B<A,\quad k=t-q>c.
\]

The T face and rho=c face use base unless Q applies. The A face belongs
to closed Q exactly when its total is at most b; otherwise it is base.

## Q against a retained base row

Let w=(t,rho) be the Q report and v=(x,y) be outside Q and Eplus. Then
H(v)>0. A bidder of own type w facing v cannot buy a base bundle:
its value is at most b, while the bundle price is H+b>b. Every base
singleton price is at least d=1/2. Thus if t<=1/2 it is empty; if t>1/2,
its low value satisfies rho<=b-t<1/2, so it can only buy its high item 1.

If y<=1/2, its high price H+A>A>=t precludes that purchase. If y>1/2,

\[
P_1=H+s-y\ge x+q.
\]

A strictly positive purchase therefore implies x<t-q=k. The other bidder's
Q menu cannot allocate item 1 there: scarce-singleton utility x-A is
negative, and bundle utility is strictly below safe-singleton utility by
x-k. Hence no item conflicts. At x=k, the base bidder's maximum utility
is at most zero and the stated rule selects empty. This argument covers
all ordinary base rows and the retained Eplus boundary faces.

## Eplus against a retained base row

Fix w=(t,rho) in Eplus, with high item 1, and let the other own report be
v=(x,y). A bidder of type w facing any retained base menu can buy only
item 1 or empty: its low singleton costs at least 1/2>rho, and the
bundle-minus-item-1 price is at least c>rho. In particular item 2 is free.

For y<=1/2 its base high price satisfies

\[
P_1=H+A\ge\max(x,x+y-c).
\]

For y>1/2 it satisfies P1>=x+q. Every possible Eplus choice that consumes
item 1 implies P1>=t:

- A scarce singleton needs x>=t.
- A bundle needs x>=k=t-q by comparison with safe, and x+y>=C by IR.
  The first inequality applies when y>1/2; the second gives
  x+y-c>=t+delta when y<=1/2.
- A lottery is dominated by bundle when y>Y, so y<=Y<1/2. Its IR
  condition is x+beta(y-c)>=t. If y>=c, then x+y-c>=t; if y<c, then
  x>=t. Either way P1>=t.

Thus the base bidder is empty whenever an Eplus choice consumes item 1.
Equality again invokes empty at zero utility. No contraction argument or
unexamined containment assumption is used for the lottery.

## Eplus against Q

A Q own report v=(x,y) cannot choose an Eplus bundle or lottery. The bundle
price C exceeds t+c>b, while x+y<=b. The scarce singleton price t exceeds
A, so its utility is negative. For a lottery with y<c it is dominated by
that singleton; for y>=c, positive lottery utility would imply

\[
x+y>t+c+(1-\beta)(y-c)\ge t+c>b.
\]

Therefore only the safe singleton can be allocated, and it requires
`y>B>1/2` (zero-utility ties select empty). Q then forces x<1/2, so y is
the Q high coordinate. The opposing Q menu has scarce upgrade threshold
kQ=y-q>c>rho. Its buyer w therefore cannot obtain the conflicting item 2:
its scarce singleton is unprofitable and its bundle is dominated by the
safe singleton. Equality y=B causes no conflict either.

## Eplus against Eplus

With matching physical orientations, both own low coordinates are below
c. Low singleton and bundle are dominated, and the lottery is dominated
by the scarce singleton. Only the bidder with the larger high value can
buy the common high item. Equal high values give zero utility and empty.

With opposite physical orientations, each own scarce coordinate is below
c<k and below the lottery cell's lower scarce bound j>1/2. Each bidder
therefore buys only its own high item as the other menu's safe singleton.
Those items are distinct. Safe purchases are strictly positive since
own high>A>B.

## What remains for joint menu selection

The preceding arguments handle base/base using the shared maximizer and
every pair involving Eplus or one Q report against a base report.
The independent symmetry route supplies Q/Q compatibility and its explicit
boundary priority. The implementation must select the joint feasible pair
of menu maximizers specified by those proofs. Arbitrary independently
selected maximizers should not be assumed compatible on a tie face.

DSIC remains valid for any specified selected maximizer of each complete
conditional menu: its achieved utility is the menu maximum. The final
finite joint priority is Borel. These are sufficient for the all-real
pointwise mechanism, including exceptional and boundary reports.

## Matching full conditional supports survive the reconstruction

The existing V4.6 full randomized certificates depend on occupied traces
and feasibility, not on the discarded fee representation.

For an Eplus row, the required top trace r1(x,1)=0 for x<k is occupied by
the opposing base bidder. Its high base price is max(1/2,x+q)<t. The
junction trace `(x,c)`, A<x<t, lies outside both Q and Eplus, because the
strict rho<c condition excludes it. Its base high price is exactly x<t.
This proves both hypotheses H1 and H2 for the actual new residual. Hence
the five-option lottery remains a full randomized conditional optimizer
on every Eplus row, with no old corner exclusions.

For a constrained Q row t>1/2, the same top trace is occupied because
max(1/2,x+q)<t whenever x<k. If C=C0, the zero-mass Q certificate applies.
If C=sum(w)>C0, its bottom and vertical anchor traces are occupied by
symmetric low-Q bundle purchases: C>b0 and the reopened t is below A, so
both singleton utilities of w are negative on those menus. At own trace
(1/2,y), y<C-1/2, the opposing bundle price is max(b0,1/2+y)<C.

For a low Q row t<=1/2, the symmetric diagonal-hole certificate applies
with z=max(b0,sum(w)). Its old displayed z<=.91 restriction extends to
z<=b=.98: `k=z-A<=c<1/2` and
`m=1/3-3(4/3-z)^2/2>=0` are the actual sign requirements. Bottom and
vertical occupied traces follow from the same strict bundle purchases.

After complete pointwise feasibility is established, these supports prove
full randomized conditional optimality for **both bidders on Q and Eplus**
for the reconstructed mechanism. They do not establish optimality of its
outer allocation, of the chosen parameters, or of the entire auction.


## Parameter substitution and independent source replay

The Eplus support is not accepted merely by replacing decimal constants
in an old assertion. With the new q=14/75, its geometric inequalities
`0<k<j<A<t`, `c<Y<B<A`, and `0<beta<1` follow from
`T=(2+2q)/3`, `U=(2+6q)/3`, `alpha=3t-2`, and the factored delta.
The uniform sink lower bound remains
`q*(1-3q/2)>0`. The independent replayer checks as an exact polynomial
identity in t that

\[
3\{AC-Aj+j^2/2-k^2/2\}-1=0,
\]

which is precisely the zero total mass of the top-trace coefficient.
The convex-hinge and junction identities use only `beta*L=alpha/2` and
`c=1/2-q`, so they are unchanged. These checks verify the relevant
hypotheses of the inherited unrestricted conditional theorem.

For constrained Q, `k` lies in `[c,A-q]` and `k<1/2`. The unconstrained
safe price `C0-k` stays strictly between 1/2 and A. If the sum floor binds,
`C-k<=b-k<=b-c=A`. Thus the nonpositive top coefficient and nonnegative
anchored capacity measure in the diagonal-hole proof also retain their
signs. No regularization, finite type grid optimum, or existence of a
finite optimal menu is assumed.

`gap_parameter_audit.py` independently reconstructs all three conditional
menu formulas, tests 178 exact rational reports on named boundary,
junction, and lottery-indifference configurations, and checks every one
of their 31,684 report pairs for a feasible maximizer pair. It then compares
all 178 reconstructed menus directly with `parameter_candidate.menu` and
compares 890 final selected profiles against independently computed argmax
sets. The certificate separately records 1,796 positive-argmax tie
profiles and the occupied top/junction trace checks. These are bounded
implementation replays supporting the written all-real proof, not a grid
optimality argument.

The audit caught and corrected a false intermediate claim that a winning
Eplus lottery requires scarce value at least A. The correct lower bound
is j=1-t/2, which is less than A but greater than 1/2 and c. This corrected
bound is sufficient for the Eplus/Eplus argument above. The final candidate
and revenue formulas did not need to change.
