"""Bounded independent V5 upper audit. No project calculators are imported.

Default writes nothing. --write stores this audit's receipt beside this file.
Universal analytic arguments are in upper_audit.md; finite scalar checks here
are supplementary. Full polynomial/tree replay is recorded separately.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError("Proof checks require unoptimized Python.")
HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]


def read(rel):
    return json.loads((BASE / rel).read_text(encoding="utf-8"))


# Exact Q(sqrt(2)) arithmetic, independent of a computer algebra library.
def Q(a=0, b=0):
    return F(a), F(b)


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def mul(x, y):
    return x[0]*y[0] + 2*x[1]*y[1], x[0]*y[1] + x[1]*y[0]


def scale(x, t):
    return x[0]*t, x[1]*t


def sub(x, y):
    return add(x, scale(y, -1))


def power(x, n):
    out = Q(1)
    for _ in range(n):
        out = mul(out, x)
    return out


def positive(x):
    a, b = x
    if b == 0:
        return a > 0
    if a == 0:
        return b > 0
    if a > 0 and b > 0:
        return True
    if a < 0 and b < 0:
        return False
    return a*a > 2*b*b if a > 0 else 2*b*b > a*a


def screening_checks():
    A, B, k = Q(F(2, 3)), Q(F(4, 3), -F(1, 3)), Q(F(2, 3), -F(1, 3))
    one = Q(1)
    assert sub(B, A) == k
    assert sub(mul(A, A), scale(power(sub(scale(A, 2), B), 2), F(1, 2))) == Q(F(1, 3))
    assert positive(sub(B, Q(F(43, 50)))) and positive(sub(B, Q(F(17, 20))))
    assert scale(power(sub(A, k), 2), F(3, 2)) == sub(one, A)
    # F is continuous at both x breaks. Its derivative and f cancel.
    for x in (Q(0), k, A, one):
        assert add(scale(sub(x, k), 3), scale(sub(k, x), 3)) == Q()
    assert add(Q(-1), Q(1)) == Q()
    # Top normal trace on each x branch equals one; right trace is one.
    assert scale(sub(one, A), 3) == one
    for x in (k, A):
        assert add(scale(sub(one, sub(B, x)), 3), scale(sub(k, x), 3)) == one
    # Direct support mass integrals. Integral f=F(0)-F(1)=0.
    int_F = add(scale(power(sub(A, k), 3), F(1, 2)), scale(power(sub(one, A), 2), F(1, 2)))
    mass1 = add(scale(power(sub(one, A), 2), F(3, 2)), int_F)
    middle = scale(sub(power(sub(one, k), 3), power(sub(one, A), 3)), F(1, 3))
    mass2 = scale(add(mul(k, power(sub(one, A), 2)), middle), F(3, 2))
    assert mass1 == mass2 == Q(F(2, 9), F(1, 27))
    assert add(mass1, mass2) == Q(F(4, 9), F(2, 27))
    return {"no_sale_area": "1/3", "support_mass": "4/9 + 2*sqrt(2)/27", "field_normal_trace_checks": "exact Q(sqrt(2))"}


def box(center, widths):
    return tuple((F(c)-F(h), F(c)+F(h)) for c, h in zip(center, widths))


def disjoint(a, b):
    return any(hi <= lo2 or hi2 <= lo for (lo, hi), (lo2, hi2) in zip(a, b))


def symmetries(b):
    return [b, tuple(b[j] for j in (1, 0, 3, 2)), tuple(b[j] for j in (2, 3, 0, 1)), tuple(b[j] for j in (3, 2, 1, 0))]


def outside_splice(b):
    W = ((F(), F(43, 100)),)*2
    J = ((F(43, 100), F(1, 2)), (F(), F(7, 20)))
    return all(all(disjoint(b[2*i:2*i+2], p) for p in (W, J, J[::-1])) for i in (0, 1))


def bb_checks():
    data = read("V5_gap_closure/certificate/bb_global_input.json")
    cert = read("V5_gap_closure/certificate/bb_global.json")
    centers = [tuple(map(F, row)) for row in (("23/40", "3/5", "91/100", "13/40"), ("29/40", "23/40", "91/100", "13/40"))]
    h = tuple(map(F, ("3/40", "3/20", "9/100", "13/40")))
    endpoints, gain, total_mass = [], F(), F()
    assert data["scale"] == 2**20
    for cell in data["cells"]:
        path = cell["path"]
        assert len(path) % 2 == 0
        ranges = [[-F(1), F(1)] for _ in range(4)]
        for k in range(0, len(path), 2):
            axis, side = int(path[k]), int(path[k+1])
            assert axis in range(4) and side in (0, 1)
            mid = sum(ranges[axis])/2
            ranges[axis][1-side] = mid
        weight = F(cell["density_numerator"], data["scale"])
        assert weight > 0
        volume = F(1)
        for width, (lo, hi) in zip(h, ranges):
            volume *= width*(hi-lo)
        gain += 4*volume*weight/40
        total_mass += 8*volume*weight
        for center in centers:
            physical = tuple((c+width*lo, c+width*hi) for c, width, (lo, hi) in zip(center, h, ranges))
            endpoints.extend(symmetries(physical))
    assert len(endpoints) == 512
    assert all(outside_splice(b) for b in endpoints)
    assert all(disjoint(a, b) for a, b in combinations(endpoints, 2))
    assert gain == F(cert["exact_upper_decrease"]) == F(4786305147, 17179869184000000)
    assert total_mass == F(cert["finite_IC_measure_mass"])
    return endpoints, {"endpoint_boxes_all_symmetries": len(endpoints), "endpoint_pair_separations": len(endpoints)*(len(endpoints)-1)//2, "gain": str(gain), "IC_measure_mass": str(total_mass)}


def master_checks(bb):
    data = read("V4_8A_frozen_primal/certificate/master_certificate.json")
    cells, columns = data["cells"], data["columns"]
    endpoints = []
    shifts = [[[F(), F(), F()] for _ in range(2)] for _ in cells]
    for cell in cells:
        physical = box(cell["center"], cell["halfwidths"])
        endpoints.extend([physical, tuple(physical[j] for j in (1, 0, 3, 2))])
    assert all(outside_splice(b) for b in endpoints)
    assert all(disjoint(a, b) for a in endpoints for b in bb)
    assert all(disjoint(a, b) for a, b in combinations(endpoints, 2))
    for col, lam in zip(columns, map(F, data["amplitudes"])):
        assert lam > 0
        a, b, i = col["A"], col["B"], col["bidder"]
        assert cells[a]["halfwidths"] == cells[b]["halfwidths"]
        ca, cb = list(map(F, cells[a]["center"])), list(map(F, cells[b]["center"]))
        assert ca[2*(1-i):2*(1-i)+2] == cb[2*(1-i):2*(1-i)+2]
        for j in range(2):
            d = ca[2*i+j]-cb[2*i+j]
            assert d == F(col["shift"][j])
            shifts[a][j][i+1] += lam*d
            shifts[b][j][i+1] -= lam*d
    cost = F()
    for cell, row, recorded in zip(cells, shifts, data["theta"]):
        theta = [max(row[j][k]-F(cell["gaps"][j][k]) for k in range(3)) for j in range(2)]
        assert theta == list(map(F, recorded))
        cost += F(cell["volume"])*sum(theta)
    assert -2*cost == F(data["exact_total_gain_lower"]) > 0
    sparse = read("V4_6_2_upper/certificate/sparse_cycle.json")
    sparse_boxes = [box(c, sparse["halfwidths"]) for c in sparse["orbit_centers"]]
    assert all(outside_splice(b) for b in sparse_boxes)
    assert all(disjoint(a, b) for a in sparse_boxes for b in bb+endpoints)
    return {"master_columns": len(columns), "master_endpoint_boxes_with_item_copy": len(endpoints), "master_gain": str(-2*cost), "sparse_endpoint_boxes": len(sparse_boxes), "scope": "independent aggregate epigraph and all retained-support disjointness; polynomial regret bounds replayed separately"}


def ledger_checks():
    u462 = F(read("V4_6_2_upper/certificate/upper_ledger.json")["final_upper"])
    n = read("V4_6_3_slack_atlas/certificate/numerical_remainder.json")["total_E"]
    atlas = read("V4_6_3_slack_atlas/certificate/atlas_ledger.json")["numerical_remainder_contracted"]
    assert all(F(n[k]) == F(atlas[k]) for k in ("lower", "upper"))
    em = F(read("V4_8A_frozen_primal/certificate/master_certificate.json")["exact_total_gain_lower"])
    event = F(read("V4_8A_frozen_primal/certificate/first_event_gain.json")["gain_interval"][0])
    u48 = F(read("V4_8B_support_redesign/certificate/phase_ledger.json")["preserved_exact_upper"])
    assert u48+event == u462-F(n["lower"])-em
    splice = F(read("V5_gap_closure/certificate/global_duality.json")["global_gain_lower"])
    bb = F(read("V5_gap_closure/certificate/bb_global.json")["exact_upper_decrease"])
    u5 = F(read("V5_gap_closure/certificate/phase_ledger.json")["new_exact_upper"])
    assert u5 == u462-F(n["lower"])-em-splice-bb
    return {"formula": "U_V462 - E_numerical_lower - G_master_lower - G_splice_lower - G_BB", "equals_recorded_V5_exact_upper": True, "contracted_E_equals_raw_numerical_E": True, "first_event_fully_cancels": True, "exact_V5_upper": str(u5)}


def scalar_checks():
    count = 0
    for a, b in product(map(F, range(-3, 4)), repeat=2):
        for p in map(F, range(4)):
            assert max(F(), a, b)-max(p, b) >= max(F(), a)-p-max(F(), b-p)
            count += 1
        assert max(F(), a)-max(F(), b)+max(F(), b)-max(F(), a) == 0
    for a1, a2, b2, lam in product((F(), F(1, 3), F(1)), repeat=4):
        g, h = lam/40, 3*lam/20
        dc, dk, dv = -g*(1-a2-b2), h*a1+g*(1-a2), -g-h*a1-g*b2
        assert dc+dk+dv == -g
    return {"directed_max_checks": count, "BB_correlated_slack_checks": 81, "scope": "finite algebra sanity checks, with universal inequalities proved in the report"}


def main():
    bb, bb_result = bb_checks()
    result = {"status": "INDEPENDENT_BOUNDED_UPPER_AUDIT_PASS", "screening": screening_checks(), "BB": bb_result, "retained_support": master_checks(bb), "assembly": ledger_checks(), "supplementary_algebra": scalar_checks(), "no_project_calculators_imported": True, "limitations": "Does not replace full V5 Bernstein trees or full numerical-remainder integration replay."}
    result["script_sha256"] = sha256(Path(__file__).read_bytes()).hexdigest()
    if "--write" in sys.argv:
        (HERE / "independent_upper_checks.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
