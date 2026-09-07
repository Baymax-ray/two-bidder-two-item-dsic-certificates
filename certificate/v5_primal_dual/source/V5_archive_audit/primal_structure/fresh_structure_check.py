"""Fresh bounded V5 structural checks; no project imports or source writes.

The universal DSIC and zero-item arguments are in AUDIT.md. This script checks
their rational constants, the complete affine BB witness, and symbolic face
weights. It does not replay inherited global feasibility or integrate revenue.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError("Run with python -B -X utf8, without optimization.")


def calculate():
    A, d, c = F(2, 3), F(1, 2), F(157, 500)
    q = d-c
    a = A+q*q/2
    b = a+c
    T, U = 1-F(2, 3)*c, F(5, 3)-2*c
    kmax = A-q
    delta_A = F(9, 16)*(T-A)*(U-A)
    # For c <= k <= kmax < 2/3, K(k)-k decreases, so this is
    # a uniform lower bound for the constrained-Q safe singleton price.
    q_safe_floor = F(5, 6)+F(3, 4)*kmax*kmax-kmax
    q_bundle_safe_upgrade = F(5, 6)+F(3, 4)*c*c-A
    e_scarce_floor = A-q-delta_A
    assert 0<c<kmax<d<A<T<U
    assert q_safe_floor>d>0
    assert q_bundle_safe_upgrade>0 and e_scarce_floor>0
    assert F(4, 3)-A>0 and (4-3*A)**2>2  # B0 > A.
    assert b-a==c and q>0

    tau, radius = F(1, 100), F(1, 10000)
    scale = 1-tau
    center = tuple(map(F, ("1577/2000", "123/200", "3/5", "4/5")))
    # These uniform bounds prove that the same affine high-sum, fee-free
    # base chart applies at every point of the entire box, old and new.
    chart_margins = {
        "transformed_above_half": min(center)-radius-(tau+scale/2),
        "transformed_high_sum": min(sum(center[:2]),sum(center[2:]))-2*radius-(2*tau+scale*b),
        "old_fee_inactive": min(center)-radius-F(3421,10000),
    }
    assert all(x>0 for x in chart_margins.values())

    def utility_rows(profile, bidder, surcharge):
        x,y = profile[2*bidder:2*bidder+2]
        w,z = profile[2*(1-bidder):2*(1-bidder)+2]
        return (F(), x-w-surcharge, y-z-surcharge, x+y-w-z)

    margins = {"old": [], "new": []}
    for signs in product((-1,1), repeat=4):
        profile = tuple(v+sign*radius for v,sign in zip(center,signs))
        for name,surcharge,selections in (("old",q,(3,0)),("new",scale*q,(1,2))):
            for bidder,selected in enumerate(selections):
                values = utility_rows(profile,bidder,surcharge)
                differences = [values[selected]-value for index,value in enumerate(values) if index!=selected]
                assert all(value>0 for value in differences)
                margins[name].extend(differences)
    assert len(margins["old"])+len(margins["new"]) == 192

    # Coefficients of t^k (1-t)^(4-k), obtained separately for every
    # zero-coordinate subset. Their sum must be the constant polynomial 1.
    total_weight = [0]*5
    faces = []
    for k in range(5):
        for zero in combinations(range(4),k):
            faces.append(zero)
            for j in range(5-k):
                total_weight[k+j] += (-1)**j*comb(4-k,j)
    assert len(faces)==16 and total_weight==[1,0,0,0,0]
    two_zero = [set(face) for face in faces if len(face)==2]
    same_bidder = [face for face in two_zero if {z//2 for z in face} in ({0},{1})]
    same_item = [face for face in two_zero if {z%2 for z in face} in ({0},{1})]
    cross = [face for face in two_zero if face not in same_bidder+same_item]
    assert tuple(map(len,(same_bidder,same_item,cross))) == (2,2,2)
    # In t^k(1-t)^(5-k) R_k + t^(k+1)(1-t)^(4-k) N_k,
    # the derivative at zero is -5 R_0 + R_1 + N_0. Here R_1=4R3.
    derivative = {}
    for family,extra,degree in (("R",0,5),("N",1,4)):
        for k in range(5):
            power = k+extra
            coeff = (-1)**(1-power)*comb(degree-k,1-power) if power<=1 else 0
            if coeff:
                derivative[f"{family}_group_{k}"] = coeff
    assert derivative == {"R_group_0":-5,"R_group_1":1,"N_group_0":1}
    return {
        "status":"FRESH_BOUNDED_PRIMAL_STRUCTURE_PASS",
        "project_imports":False,
        "q_safe_price_floor":str(q_safe_floor),
        "q_bundle_safe_upgrade_floor":str(q_bundle_safe_upgrade),
        "e_zero_scarce_coordinate_exclusion_margin":str(e_scarce_floor),
        "delta_A":str(delta_A),
        "bb_chart_margins":{key:str(value) for key,value in chart_margins.items()},
        "bb_old_minimum_margin":str(min(margins["old"])),
        "bb_new_minimum_margin":str(min(margins["new"])),
        "bb_exact_affine_comparisons":192,
        "bb_box_volume":str((2*radius)**4),
        "face_count":len(faces),
        "two_zero_face_classes":[2,2,2],
        "face_weights_sum_polynomial":total_weight,
        "revenue_derivative_coefficients":derivative,
        "scope":"Rational constants, affine whole-box witness, and symbolic mixture weights; universal proof in AUDIT.md; no source mechanism or face integration replay.",
    }


if __name__ == "__main__":
    output = calculate()
    text = json.dumps(output,indent=2)+"\n"
    if "--write" in sys.argv:
        Path(__file__).with_name("fresh_structure_receipt.json").write_text(text,encoding="utf-8")
    print(text,end="")
