# V5 common global and regional ledger

This ledger uses the complete V5 fields and measures. It preserves the V4.8B directed IC convention, completed boundary identities, and flux budget. New cancellations are justified by either exact source-sink balance or explicit weak boundary traces; a junction crossing is not treated as a free gain.

## 1. Exact universal identity

After all body corrections have been summed, let $\Phi_i$ be bidder $i$'s allocation covector density. Let $K_{\mathrm{retained}}(u,x)$ collect the retained finite directed-IC and PSD convexity pairings, and $K_{\mathrm{BB}}(u,x)$ the new translated two-way IC pairing. They are nonnegative for every pointwise DSIC mechanism. The inherited stress terms use their previously completed trace formulas and legitimate measure pairings.

For normalized own utilities $\bar u_i=u_i-u_i(0;w)$, define
\[
S_5(u)=\sum_i\int\left[
u_i(0;w)+3\,1_{D^\sharp}(w)\int_{D_0}\bar u_i(v;w)\,dv
\right]dw.
\]
For every complete DSIC/IR mechanism, the globally accounted identity is
\[
R=\sum_i\langle\Phi_i,x_i\rangle-S_5-K_{\mathrm{retained}}-K_{\mathrm{BB}}.
\tag{1}
\]
All old first-event fields and their associated terms are removed together. No endpoint correction is retained without its generating measure.

The new screening field has the explicit body source $3\,1_{D_0}u$, top/right trace matching the revenue boundary, and zero bottom/left flux. Its internal traces match. The opponent-domain switch does not create an own-type distributional derivative. The new BB pair measure has equal source and sink marginals, hence zero utility source; its allocation covectors are absolutely continuous, with zero boundary flux. Existing singular or PSD pairings stay inside the retained term with their archived formulas. There is no new unrecorded singular-capacity component.

Let $\Pi_j=\max(0,\Phi_{1j},\Phi_{2j})$ and $U_{\mathrm{env}}=\int\sum_j\Pi_j$. Then
\[
C_5(x)=\int\sum_j\Pi_j(1-x_{1j}-x_{2j}),\qquad
V_5(x)=\int\sum_{i,j}(\Pi_j-\Phi_{ij})x_{ij}.
\]
All pairings exist: allocations are bounded Borel functions, normalized utilities are convex Lipschitz functions, body covectors are integrable, and inherited singular terms retain their legitimate traces. Boundary and tie profiles of measure zero remain specified by the complete primal; their zero Lebesgue mass is not used to suppress any singular pairing.

The exact rational reported upper endpoint satisfies $U_5\ge U_{\mathrm{env}}$. Set $E_5=U_5-U_{\mathrm{env}}\ge0$, including the inherited enclosure remainder and conservatism of the splice comparison. The full gap is
\[
U_5-R=C_5+V_5+S_5+K_{\mathrm{retained}}+K_{\mathrm{BB}}+E_5.
\tag{2}
\]
This is also the unrestricted charged-screening inequality for each bidder under the same $\Pi$. Each charged value is at most zero and is attained by the globally empty mechanism. It is not an assertion that the proposed auction separately attains those charged optima.

For the new reserve-transformed mechanism, $S_5=0$. Indeed its normalized origin utility is zero. If $w\in D^\sharp$, then $T(w)\le w$ keeps the source conditional menu in the free-SJA branch. For $v\in D_0$, $T(v)\le v$ is still in $D_0$, so its transformed source utility vanishes. Equation (2) therefore reduces to the identity reported in the phase ledger.

## 2. Regional changes that are actually certified

| Region or term | Accepted effect | Accounting status |
|---|---|---|
| Added conditional slices $J$ and item swap, including QQ/mixed intersections | Global net splice decrease at least 0.00045027837569474655 | Complete common envelope, positive opposing excess, simultaneous switch, and source retained |
| Old first-event supports | Entire previous deduction given back | Removed as complete fields and terms, preventing overlap double counting |
| Disjoint BB translated boxes | Exact decrease $4786305147/17179869184000000$ | Actual IC slack is allowed; exact first-event and whole-box proof |
| Reserve-transformed primal | Revenue gain strictly greater than 0.000048 | Full four-coordinate pushforward, all face moments and rents included |
| New primal conditional source and origin | Exactly zero | Reproved under the transformation |
| New primal remaining $C,V,K$ | Nonnegative; total with $E$ enclosed by the remaining-gap interval | Not separately reintegrated into a new numerical regional atlas |
| QQ compact curl | No accepted decrease | Certified enclosure straddles zero; overlap prevents addition |

The splice bound pays $|J|R_{\mathrm{SJA}}$ for the new support and an additional opposing-price excess $E$. Its decomposition is an upper-value comparison, not a claim that each signed regional summand improves independently.

## 3. Correlated BB slack, at the old incumbent only

Per translated pair let $g=\lambda/40$, $h=3\lambda/20$, and let actual allocations at endpoint B be $a=(a_1,a_2)$ to the moved bidder and $b=(b_1,b_2)$ to the opponent. Endpoint A selects item 2 throughout the certified cells. The exact changes are
\[
\Delta C=-g(1-a_2-b_2),\quad
\Delta K=h a_1+g(1-a_2),\quad
\Delta V=-g-h a_1-g b_2.
\]
Consequently
\[
\Delta C+\Delta K+\Delta V=-g.
\]
The joint identity is decisive: positive IC slack is permitted and is already paid by the decrease in other terms. Thirty-seven cells retain item 2 at both endpoints; twenty-seven meet option interfaces. Their correlated interval bounds and exact integral are in certificate/bb_global.json.

These incumbent-specific component bounds are not transferred unchanged to the new primal. For V5, use the actual allocations in the universal definitions (1)--(2). No fresh whole-profile numerical claim is made about where all remaining IC or capacity slack lies.

## 4. Exact endpoint assembly and residual uncertainty

The exact assembly is
\[
U_5=U_{4.8B}+G_{\mathrm{event,lower}}
-G_{\mathrm{splice,lower}}-G_{\mathrm{BB}}.
\]
The revenue is exactly the degree-five face-moment expression in the primal proof. Algebraic price and unresolved-strip allowances enclose its coefficients. The phase ledger propagates every endpoint with rational arithmetic; all printed decimals are outward rounded.

Thus the remaining global gap is rigorously positive and enclosed, while its detailed allocation among the new $C,V,K,E$ terms is open. No finite-family failure, enclosure ceiling, or opposing-menu crossing is used as an impossibility theorem. Neither the new primal nor the new support is claimed globally optimal.
