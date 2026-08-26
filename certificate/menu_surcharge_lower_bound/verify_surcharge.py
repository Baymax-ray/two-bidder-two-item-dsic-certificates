#!/usr/bin/env python3
"""Exact verifier for the opponent-dependent common entry surcharge."""

from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


def clean(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def add(p, q):
    n = max(len(p), len(q))
    return clean(
        [
            (p[k] if k < len(p) else F(0))
            + (q[k] if k < len(q) else F(0))
            for k in range(n)
        ]
    )


def neg(p):
    return tuple(-x for x in p)


def sub(p, q):
    return add(p, neg(q))


def scale(p, c):
    return clean([c * x for x in p])


def mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return clean(out)


def square(p):
    return mul(p, p)


def evaluate(p, t):
    total = F(0)
    for coefficient in reversed(p):
        total = total * t + coefficient
    return total


def integrate(p, lo, hi):
    return sum(
        coefficient * (hi ** (k + 1) - lo ** (k + 1)) / F(k + 1)
        for k, coefficient in enumerate(p)
    )


ONE = (F(1),)
T = (F(0), F(1))


def menu_revenue(A, B, C):
    """Exact polynomial r(A,B,C) for an active subadditive four-option menu."""
    item_1 = mul(mul(A, sub(ONE, A)), sub(C, A))
    item_2 = mul(mul(B, sub(ONE, B)), sub(C, B))
    rectangle = mul(add(sub(ONE, C), B), add(sub(ONE, C), A))
    triangle = scale(square(sub(add(A, B), C)), F(1, 2))
    bundle = mul(C, sub(rectangle, triangle))
    return add(add(item_1, item_2), bundle)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest().upper()


def verify_base_dependency(manifest):
    dependency = manifest["base_certificate"]
    base_dir = (
        Path(__file__).resolve().parent / dependency["directory"]
    ).resolve()
    expected = (
        ("manifest.json", dependency["manifest_sha256"]),
        ("verify_ama.py", dependency["verifier_sha256"]),
        ("verification_output.txt", dependency["output_sha256"]),
    )
    for name, digest in expected:
        path = base_dir / name
        assert path.is_file(), f"missing base dependency: {path}"
        assert file_sha256(path) == digest, f"base dependency hash mismatch: {name}"
    return json.loads((base_dir / "manifest.json").read_text(encoding="utf-8"))


def main():
    manifest = json.loads(
        Path(__file__).with_name("manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["scope"] == "primal_lower_bound_only"
    base_manifest = verify_base_dependency(manifest)

    base_parameters = base_manifest["parameters"]
    a = F(base_parameters["single_item_cost_a"])
    b = F(base_parameters["same_bidder_bundle_cost_b"])
    s = F(base_parameters["split_allocation_cost_s"])

    surcharge = manifest["surcharge"]
    e = F(surcharge["amount"])
    rectangle = surcharge["canonical_rectangle"]
    free_lo, free_hi = map(F, rectangle["free_coordinate_interval"])
    lo, hi = map(F, rectangle["varying_coordinate_interval"])
    free_length = free_hi - free_lo
    rectangle_count = int(surcharge["transposed_rectangle_count"])
    bidder_count = int(surcharge["symmetric_bidder_count"])
    assert rectangle_count == 2
    assert bidder_count == 2

    # On the first rectangle q=(rho,t), H=0 and the active base menu is
    # A=s-t, B=a, C=b. The transposed rectangle has the symmetric formula.
    assert hi < a
    assert free_hi < a
    assert free_hi + hi < b
    assert s - lo < a
    assert a <= s - free_hi

    A = sub((s,), T)
    B = (a,)
    C = (b,)
    A_e = add(A, (e,))
    B_e = add(B, (e,))
    C_e = add(C, (e,))

    for t in (lo, hi):
        for prices in (
            (evaluate(A, t), evaluate(B, t), evaluate(C, t)),
            (evaluate(A_e, t), evaluate(B_e, t), evaluate(C_e, t)),
        ):
            pa, pb, pc = prices
            assert F(0) <= pa <= pc <= F(1)
            assert F(0) <= pb <= pc
            assert pc <= pa + pb

    delta = sub(menu_revenue(A_e, B_e, C_e), menu_revenue(A, B, C))
    expected = manifest["expected"]
    expected_delta = tuple(
        map(F, expected["delta_coefficients_low_to_high"])
    )
    assert delta == expected_delta

    delta_lo = evaluate(delta, lo)
    delta_hi = evaluate(delta, hi)
    derivative_lo = delta[1] + 2 * delta[2] * lo
    assert delta_lo == F(expected["delta_at_varying_lo"])
    assert delta_hi == F(expected["delta_at_varying_hi"])
    assert derivative_lo > 0

    one_strip_integral = integrate(delta, lo, hi)
    assert one_strip_integral == F(expected["one_strip_integral"])

    # Two transposed rectangles and two symmetric bidders.
    gain = rectangle_count * bidder_count * free_length * one_strip_integral
    assert gain == F(expected["total_revenue_gain"])

    base_revenue = F(base_manifest["expected"]["expected_revenue"])
    assert base_revenue == F(manifest["base_certificate"]["expected_revenue"])
    final_revenue = base_revenue + gain
    assert final_revenue == F(expected["final_expected_revenue"])

    print("MENU-SURCHARGE LOWER-BOUND CERTIFICATE: PASS")
    print("manifest obligations: PASS")
    print("base certificate hashes: PASS")
    print(f"parameters: a={a}, b={b}, s={s}, e={e}")
    print(f"surcharge t-interval: [{lo}, {hi}]")
    print(
        "delta(t) coefficients low-to-high: "
        + ", ".join(str(c) for c in delta)
    )
    print(f"delta(lo): {delta_lo}")
    print(f"delta(hi): {delta_hi}")
    print(f"one-strip exact integral: {one_strip_integral}")
    print(f"total exact surcharge gain: {gain}")
    print(f"base exact revenue: {base_revenue}")
    print(f"final exact revenue: {final_revenue}")
    print(f"decimal final revenue: {float(final_revenue):.15f}")
    print("scope: exact feasible/DSIC/ex-post-IR primal lower bound only; no global upper bound")


if __name__ == "__main__":
    main()
