# Independent Q compatibility audit for the rebuilt symmetric candidate

Audit target: `parameter_candidate.py`, parameters A=a=2/3, d=1/2,
c=47/150, b=49/50, s=7/6, q=14/75. This note proves Q-Q and Q-base
compatibility directly for the new three-region mechanism. It does not import
feasibility of a predecessor at different constants. E interactions are audited
separately. All tie assertions refer to a choice among complete-menu maximizers.

## Q against the affine base

Fix the Q report w=(t,rho), t>=rho, t<=A and t+rho<=b. In particular
rho<=b/2<d. For opposing report v=(x,y), the base menu faced by w has pivot
H(v)=max(0,x-A,y-A,x+y-b), singleton prices
H+min(A,s-y), H+min(A,s-x), and bundle price H+b.

The base bidder w cannot select its bundle with positive utility because
H+b>=b>=t+rho. Its low singleton price is always at least d:
if x<=d the price is H+A>=A>d; if x>d, H>=x-A gives
H+s-x>=s-A=d. Thus rho<d prevents a positive low singleton. At zero utility
choose empty. The only possible conflicting base allocation is w's high item.

For the free Q branch t<=d, the same lower bound d on each base singleton
makes w empty globally. Every Q allocation is then feasible.

For t>d, the opposing Q menu has scarce singleton price A, safe price
B=C-k, bundle C, with k=t-q and C=max(C0(t),t+rho),
C0(t)=5/6+3(t-q)^2/4. Its singleton/bundle comparisons have these implications:

* If it selects the scarce singleton at positive utility, x>A>=t and
  y<=C-A<d. The strict last inequality follows from b<s and C0(A)<s.
  The base high price is therefore H+A>=A>=t, and w cannot purchase it.
* If it selects the bundle, the bundle-versus-safe comparison gives x>k
  when a tie selects the safe singleton first. If the base high price uses
  its A term, it is at least t. If it uses s-y, then
  H+s-y >= x+y-b+s-y = x+q > t.
  Again w cannot purchase the contested high item.
* If it selects only the safe item, the base bidder's only possible allocation
  is its high item, so the two allocations are disjoint.

Hence there is a pointwise feasible pair of menu maximizers for every Q-base
profile, including the max and sum faces of Q. This argument is unchanged by
rotating physical items. At a bundle/safe equality choose safe; at zero utility
choose empty. A global lexicographic search for a feasible maximizer pair is
therefore well-defined, even if another menu-maximizing pair is incompatible.

## Q against Q

Every scarce singleton utility is nonpositive. Safe singleton prices satisfy
B>=C0(A)-(A-q)>d because the function 5/6+3k^2/4-k decreases on the parameter
interval k in [c,A-q]. Both coordinates of a report in the free branch are
at most d, and every report's low coordinate is below d. Thus a positive
singleton can only be its owner's high item under opposite-high orientations.
Two such singletons are disjoint.

Two positive-utility bundles would require sum(v)>C(w)>=sum(w) and
sum(w)>C(v)>=sum(v), which is impossible. For a bundle/safe conflict with
opposite-high orientations, write v_low for the bundle purchaser's low value
and w_high for the singleton purchaser's high value. Safe-first priority gives
v_low>w_high-q, while singleton purchase requires

w_high>B(v)=C(v)-v_high+q>=v_low+q.

This is a contradiction. If one menu is in the free branch, the potential
opponent singleton is priced at A and cannot give positive utility within Q.
These arguments construct a feasible max pair on every QQ report, with empty
and safe choices resolving equalities.

## Conditional certificates on Q

The abstract V4.6 full randomized Q certificates depend on the scalar hole
parameter k and bundle C, not on the frozen numerical c. They apply here once
these actual supports are checked:

* For constrained Q, at own report (x,1), x<k, the opponent receives its high
  item strictly under the base menu. Its high price is d when x<c and x+q
  when c<x<k. Both are below t. These reports are outside E and Q.
* If the bundle is raised above C0 so C=t+rho<=b, the priced bottom and
  x=1/2 anchors lie in Q_free and have bundle prices strictly below C; the
  other bidder purchases a bundle strictly. All its singleton utilities are
  nonpositive. The inherited diagonal support therefore saturates.
* In Q_free with C=b0, the candidate is the full-capacity SJA optimum and is
  feasible; its upper bound remains valid under any residual below one.
  If C=sum(w)>b0, the same diagonal anchors give the raised symmetric support.

The numerical conditions required by these arguments are exact rational ones:
q>0, b<1, c<A-q<2/3, C0(c)>b0, C0(A)<s, and C0(A)-(A-q)>d.
The b0 comparison is reduced to squaring positive rationals. The standalone
`sym_parameter_q_audit.py` verifies these constants and the affine-gap identities.
This is a full randomized inner certificate on the new Q fibers once the whole
candidate's independent E compatibility proof is combined with the above.
It is not a matching full-auction certificate.
