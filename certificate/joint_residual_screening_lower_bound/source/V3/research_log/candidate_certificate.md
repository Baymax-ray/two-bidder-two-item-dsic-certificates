# V3 candidate-specific certificate interface

## 1. What has and has not been constructed

The joined-threshold candidate has an exact *local* polar certificate for all four price-contraction directions on its modified opponent chamber. It also determines the support of every possible matching all-deviation weak certificate. These are different objects. The local polar has not been lifted to a feasible global multiplier system, and no matching unrestricted upper bound has been obtained.

The full weak-duality identity below is retrieved and rederived from the named DUAL-1 source, output/canonical_auction_full_dsic_primal_dual_20260830/full_polar_derivation.md, Sections 5-6. It is written here without bidder symmetry. This avoids making symmetry or minimum-norm selection part of the certificate problem. It applies to arbitrary randomized rows.

## 2. Full weak upper identity, with signs and measures explicit

Let Z=T1 x T2, T=[0,1]^2, m=Lebesgue probability measure on Z. For each i, let D_i contain triples (v_i,r_i,w) with w the opponent report. Take a finite nonnegative Borel/Radon measure lambda_i on D_i. Let alpha_i and beta_i be its true-profile and report-profile marginals, both placed in the original bidder order on Z. Define signed allocation-moment measures

    integral phi(z) dM_ij(z)
      = integral phi(report-profile(r_i,w))*(v_ij-r_ij) d lambda_i.

Let mu_j be a finite nonnegative measure on Z for item j, and let theta_i be a finite signed measure on the opponent square. Let iota_i(w) be the profile with own report zero. Require the following signed measures to be nonnegative:

    sigma_i = m-alpha_i+beta_i-(iota_i)_#theta_i >= 0,
    tau_ij = M_ij+mu_j-v_ij*m >= 0.

Then U=sum_j mu_j(Z) is an upper bound for every normalized pointwise DSIC, IR, jointly feasible Borel randomized mechanism. For a candidate with utility u_i and row x_i, define its IC slack

    g_i(v_i,r_i,w)=u_i(v_i,w)-u_i(r_i,w)-(v_i-r_i).x_i(r_i,w).

Direct expansion gives the exact gap identity

    U-Rev = sum_i integral g_i d lambda_i
            +sum_j integral (1-x_1j-x_2j) d mu_j
            +sum_i integral u_i d sigma_i
            +sum_ij integral x_ij d tau_ij.

The normalization terms vanish because u_i(0,w)=0. Each remaining term is nonnegative. Bounded normalized utilities, allocations and payments make all finite-measure pairings well-defined, including singular multipliers on exceptional reports. An unnormalized admissible mechanism can first have its nonnegative type-zero subsidy removed, weakly increasing its revenue, so the upper bound extends to unnormalized Borel mechanisms. The completed-Lebesgue class uses the preserved repair dependency stated below.

This is a sufficient weak certificate. No countable-additive dual attainment or strong-duality theorem is assumed. A matching measure system, if exhibited, would solve the upper obligation regardless of those open functional-analytic questions. A failed finite basis search would not show such a system cannot exist.

## 3. Binding IC graph of this actual candidate

Fix an opponent w and write the candidate's four lines as ell_S(v)=v.S-P_S(w), S in {0,1,2,12}. Define the *closed active cell*

    A_S(w)={v : ell_S(v)=max_Q ell_Q(v)},

and the *selected-report cell*

    E_S(w)={r : the complete joint tie algorithm actually selects S for i}.

These must be distinguished. On a boundary more than one option can be active, but only one is selected. For a report r in E_S,

    g_i(v,r,w)=u_i(v,w)-ell_S(v).

Hence the complete tight-IC set is exactly the union of A_S(w) x E_S(w), with w unchanged. This formula remains valid on all exceptional reports and lower-dimensional ties. It excludes arbitrary long deviations whose reported option is not active at the true type, but includes all long deviations within one active menu cell. A nearest-neighbor flow ansatz is not justified.

In a proper discounted menu (prices denoted A,B,C in fixed item coordinates), the closed cells are

    A_0={v1<=A, v2<=B, v1+v2<=C},
    A_1={v1>=A, v2<=C-A},
    A_2={v2>=B, v1<=C-B},
    A_12={v1>=C-B, v2>=C-A, v1+v2>=C},

intersected with the own square. The five positive-length contact panels are:

- 0/1: v1=A, 0<=v2<=C-A;
- 0/2: v2=B, 0<=v1<=C-B;
- 0/12: v1+v2=C, C-B<=v1<=A;
- 1/12: v2=C-A, A<=v1<=1;
- 2/12: v1=C-B, B<=v2<=1.

The junctions are (A,C-A), where 0,1,12 meet, and (C-B,B), where 0,2,12 meet. There is no exposed positive-utility 1/2 interface under strict discount. Thus independent shifts of the five panels are not admissible menu perturbations: their intercepts must arise from the same three prices. In particular A+(C-A)-C=0 and B+(C-B)-C=0 are the two elementary price-cycle identities. The universal utility-fee change moves all three entry panels together; a low-item surcharge moves the linked bundle and low-item contacts together.

At any exact matching certificate, lambda_i must give full measure to the tight set above; sigma_i must give full measure to u_i=0; mu_j must give full measure to profiles where that item is fully allocated; tau_ij must give full measure to x_ij=0. These are zero-set conditions in the actual Borel representative, not assertions about topological support in an a.e. equivalence class. Every candidate report and tie convention is relevant when multipliers are singular.

The candidate is deterministic, so at an item-winning profile the winner's corrected allocation measure must agree with mu_j in the complementary-slackness sense, while at an unallocated item mu_j vanishes. A future fractional row would instead force simultaneous equality of the reduced allocation costs for every positive marginal. No such fractional region has been inferred merely from averaging symmetric solutions.

## 4. Exact local polar attached to the joined branches

These derivative statements apply for d<=t<1. At t=1 only the mechanism and continuous revenue formula are asserted; no derivative across the A=1 topology is inferred.

Let g_A=G_A, g_B=G_B, g_C=G_C, beta=g_A+g_B+g_C and Gamma=g_B+g_C, where G is the *integrated conditional menu revenue*, not pointwise virtual revenue. Let (alpha,beta_p,gamma) be an admissible price increment, with alpha,beta_p>=0 and gamma>=max(alpha,beta_p). To avoid symbol ambiguity, beta_p denotes the second price increment; beta above is the common-fee derivative.

The directional revenue is g_A*alpha+g_B*beta_p+g_C*gamma. The branch equations give exact nonpositive decompositions:

- Before the square-root branch, g_A,g_B>=0 and beta<=0:
  beta*gamma - g_A*(gamma-alpha) - g_B*(gamma-beta_p).
- On the square-root branch, beta=0 and g_A,g_B>=0:
  -g_A*(gamma-alpha) - g_B*(gamma-beta_p).
- On the quadratic plateau, g_A=0, Gamma=0, g_B>0:
  -g_B*(gamma-beta_p).
- On the affine branch, g_A<=0, Gamma=0, g_B>0:
  g_A*alpha - g_B*(gamma-beta_p).
- After the affine branch, g_A<=0, Gamma<=0, g_B>0:
  g_A*alpha + Gamma*gamma - g_B*(gamma-beta_p).

These are explicit polar decompositions of the four-ray contraction cone. The vanishing factors identify the available first-order freedom and the active containment inequalities. They show why merely introducing more subbands in this chamber cannot reveal an improving infinitesimal contraction once these equations are imposed.

They are NOT a full revenue certificate. The coefficients g_A,g_B are already integrated over own-type cells and are not item-scarcity prices at individual report profiles. To lift them one must construct actual nonnegative deviation and capacity measures satisfying Section 2 on the entire cube and the support conditions in Section 3. There is no justification for assigning these coefficients pointwise to mu or for omitting opponent regions outside the replacement chamber. Binding constraints determine the candidate certificate interface, but they do not solve its global compatibility automatically.

## 5. The next falsifiable obligations

1. An admissible deformation that leaves the four-ray contraction cone, with complete joint capacity and IC, can refute candidate optimality if its integrated revenue gain is positive. The current cone equalities do not constrain it.
2. A proposed multiplier lift must satisfy signed-measure balance against arbitrary Borel sets, including boundary strata, and the zero-set complementarity conditions above. An exact violation refutes that lift, not the candidate itself.
3. A complete feasible lift with U=R_V3 would certify the unrestricted optimum. None is currently available.

The inherited upper bound remains valid; no global certificate has been discarded because it failed to be expressible in a preferred polynomial or common-potential representation.

### Measurability scope correction

The singular-measure gap identity in Section 2 directly pairs Borel representatives only. Normalization by itself does not justify pairing an arbitrary completed-Lebesgue representative against singular measures. To extend the resulting scalar upper bound to the larger completed-Lebesgue admissible class, use the preserved phase-I attainment/repair theorem, LaTeX/main.tex, Theorem 1 and the section labeled `completed`: the two classes have the same supremum and there is an attaining Borel representative. That earlier proof, rechecked at its named completed-input step in V3, is a dependency of the class extension; it is not a new V3 theorem. Without that dependency this note's sufficient certificate should be stated for the Borel class only.

