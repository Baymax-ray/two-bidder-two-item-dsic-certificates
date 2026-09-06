# Exact revenue of the selected joint corner trial

For the complete mechanism in `price_joint_reallocation.md`, with the
selected epsilon=9/10000, the exact increment over
`outer_bundle_reoptimized.mechanism` is

\[
\begin{aligned}
\Delta={}&\frac{6578986777818169914603}
 {10652675687500000000000000000000}\\
&+\frac{6248637}{282500000000000}\log\frac{161}{176}
 -\frac{61575471}{282500000000000}\log\frac{613}{628}
 -\frac{9308601}{5000000000000000000}\log\frac{13}{10}.
\end{aligned}
\]

The exact rational logarithm enclosure gives

`0.000000003916127942142253666897026142330621130`

`<= Delta <=`

`0.000000003916127942142253666897026142330621131`.

The independent conservative bound in the mechanism proof is
26902077489/12500000000000000000, which is smaller and strictly positive.
The entire reference auction's exact revenue plus this Delta is therefore
an exact characterization of the selected trial's revenue. Neither a
rounded decimal nor a restricted-family stationarity claim is substituted
for the exact expression.

## 1. Entire conditional lottery menus

Let alpha=3t-2, delta=(9/16)(T-t)(U-t), L=delta+alpha/2,
T=613/750, U=839/750, and t range from 7/10 to 71/100. The complete own-type
integration of the changed lottery and displaced deterministic purchases is

\[
\Delta_2=\frac15\int_{7/10}^{71/100}
\left[\frac{\varepsilon\alpha L}{4}
-\frac{\varepsilon^2L^2}{2\delta}
-\frac{\varepsilon^3L^3}{\alpha\delta^2}\right]dt.
\]

The first term is polynomial. The other two are rational functions with
only rational poles at A=2/3, T and U. The replay divides out polynomial
parts, solves the exact partial-fraction coefficient systems over the
rationals, and multiplies the resulting decomposition by its denominator
to verify the full polynomial identity. The three endpoint ratios are
(71/100-A)/(7/10-A)=13/10, (T-71/100)/(T-7/10)=161/176 and
(U-71/100)/(U-7/10)=613/628. No fitting at type-grid nodes is used.

## 2. Entire compensating entry-fee menus

For each reference conditional menu in the fee strip, a common entry fee h
expands its no-sale area from D0 to D0+Ch+h^2/2. The positive right and top
traces each decrease by h. The exact revenue variation is consequently

\[
\Delta R_{\rm fee}=(1-3D_0)\varepsilon
 -\frac32C\varepsilon^2-\frac12\varepsilon^3.
\]

Below y=c the menu is the E-plus lottery, D0=(1+lambda)/3 with
lambda=alpha(c+L/4). All coefficients are polynomials in the opponent's
high report x. Their exact integrated contribution is

\[
-92624010033429/125000000000000000000000.
\]

Above y=c, put z=y-c. On the complete rectangle
x in [1741/2500,71/100], z in [0,9/2500], its three cells have fees and
upper x boundaries

| Frozen fee | Upper x boundary |
|---|---|
| 7/2000 (B13.1) | 701/1000-z |
| 7/10000 (B14.1) | 353/500-z |
| 0 | 71/100 |

The first cell starts at 1741/2500 and each later cell starts at the preceding
upper boundary. The prices are A=x+z+f, B=1/2+z+f, C=x+c+z+f and
D0=AB-(A+B-C)^2/2. The source table's normalized-rho denominator is
x+z-501/1000; its ratio lies below 1/8 throughout the strip. The verifier
checks the literal row identities and excludes a later row meeting this
range. Therefore integrating these bivariate polynomials between the
affine x limits covers every tariff region, with boundaries retained in
the mechanism but contributing zero revenue measure.

The three upper-strip contributions are respectively

\[
3161434941/25000000000000000000,\quad
15610239/62500000000000000,\quad
838578339/5000000000000000000.
\]

Adding both halves gives the exact full bidder-1 revenue change

\[
\Delta_1=-24631898853429/125000000000000000000000.
\]

This calculation includes retained buyers' higher payments and the entire
revenue of dropped buyers. It is not a virtual-surplus computation at
selected report profiles. Adding Delta1 to Delta2 yields the expression
at the start of this note.

## 3. Rational logarithm certification and replay

For each positive rational r set z=(r-1)/(r+1). The replay uses 40 terms of

\[
\log r=2\sum_{j=0}^{39}\frac{z^{2j+1}}{2j+1}+E,
\qquad
|E|\le\frac{2|z|^{81}}{81(1-z^2)}.
\]

Every operation and both error endpoints are rational. Signed coefficients
are propagated outward; the final displayed enclosure is rounded outward
as integers divided by 10^45. The narrow enclosure exceeds the separate
mechanism proof's rational lower bound.

`python -B -X utf8 V4_6/verifier/price_joint_revenue.py` replays the stored
certificate without writes. The retained table identities, polynomial
decompositions, cell integration and logarithm bounds pass exactly. The
entry-fee and lottery-cut formulas are also subject to independent polygon
and envelope audits in the V4.6 audit notes. A matched unrestricted auction
upper bound remains unresolved.
