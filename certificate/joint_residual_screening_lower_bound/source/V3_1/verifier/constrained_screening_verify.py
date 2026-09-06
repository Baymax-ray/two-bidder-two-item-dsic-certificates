"""Exact replay of the unrestricted constrained-screening certificate.

The general pointwise DSIC/measure proof is in constrained_screening.md.
Default mode is read-only; --write explicitly generates the certificate.
"""

import argparse
from fractions import Fraction as Q
import json
from pathlib import Path

if not __debug__:
    raise RuntimeError("Run without -O: this exact replay uses assertions.")


def parameters(k):
    A = Q(2, 3)
    C = Q(5, 6) + Q(3, 4) * k * k
    return A, C - k, C


def menu_value(A, B, C):
    return A * (1 - A) * (C - A) + B * (1 - B) * (C - B) + C * ((1 - C + B) * (1 - C + A) - (A + B - C) ** 2 / 2)


def polynomial_value(k):
    return Q(59, 108) + k * k / 4 - k ** 3 + Q(9, 16) * k ** 4


def tail(x, k):
    A, B, C = parameters(k)
    if x <= k:
        return (2 - 3 * B) * x
    if x <= A:
        return 1 - A + (3 * C - 2) * (A - x) - Q(3, 2) * (A * A - x * x)
    return 1 - x


def pairing(k):
    A, B, C = parameters(k)
    volume1 = Q(3, 2) * (1 - A) ** 2
    const = 1 - A + (3 * C - 2) * A - Q(3, 2) * A * A
    edge = const * (A - k) + (2 - 3 * C) * (A * A - k * k) / 2 + (A ** 3 - k ** 3) / 2
    edge += (1 - A) ** 2 / 2
    volume2 = Q(3, 2) * k * (1 - B) ** 2 + ((1 - C + A) ** 3 - (1 - B) ** 3) / 2
    return volume1, edge, volume2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    k = Q(283, 1000)
    A, B, C = parameters(k)

    # Parameter interval contains all d<t<=a: k ranges from c to a-q.
    c, upper = Q(137, 500), Q(409, 1000)
    assert 0 < c < k < upper < Q(2, 3)
    # B'=3k/2-1<0 on this interval, so this endpoint suffices.
    assert Q(3, 2) * upper < 1
    assert 0 < parameters(upper)[1] <= parameters(c)[1] < Q(2, 3)
    assert parameters(c)[2] > Q(2, 3)
    assert parameters(c)[1] < 1

    # Algebraic identity replay: every expression has degree <=6 in k.
    # Seven distinct exact nodes therefore prove each displayed identity.
    nodes = [Q(n, 100) for n in range(28, 35)]
    for node in nodes:
        a, b, cc = parameters(node)
        area0 = a * cc - a * a / 2 - node * node / 2
        assert area0 == Q(1, 3)
        assert 1 - a == Q(1, 3)
        assert a - area0 == Q(1, 3)
        assert menu_value(a, b, cc) == polynomial_value(node)
        assert sum(pairing(node)) == polynomial_value(node)
        assert tail(Q(0), node) == tail(Q(1), node) == 0
        assert tail(node, node) == (2 - 3 * b) * node
        mid_at_k = 1 - a + (3 * cc - 2) * (a - node) - Q(3, 2) * (a * a - node * node)
        assert mid_at_k == tail(node, node)
        assert tail(a, node) == 1 - a
        derivative = node / 2 - 3 * node * node + Q(9, 4) * node ** 3
        assert derivative == -tail(node, node)

    # Complete cell definitions certify menu dominance algebraically.
    # Item 1: x>=A and y<=C-A; item 2: y>=B and x<=k;
    # bundle: x>=k, y>=C-A, x+y>=C; empty: all three values<=0.
    assert C - B == k
    assert C - A > 0
    assert A + B - C == A - k > 0
    assert B >= C - A
    assert A > k
    # The strict discount makes the unused opposite singleton dominated.
    assert A - k > 0
    # Boundary priority item2 -> item1 -> bundle allocates no item1 at x=k.
    for y in (Q(0), B, Q(1)):
        values = (Q(0), k - A, y - B, k + y - C)
        selected = next(i for i in (0, 2, 1, 3) if values[i] == max(values))
        assert selected in (0, 2)

    # Actual V3 top-edge prices at w=(.51,.01), checked symbolically on
    # the two affine x chambers rather than sampled to infer the chamber.
    t, rho, d, q = Q(51, 100), Q(1, 100), Q(501, 1000), Q(227, 1000)
    assert t - q == k
    assert t > d
    assert d == c + q
    assert t - d == k - c > 0
    assert t - (k + q) == 0
    assert rho < d and t + rho < Q(91, 100)

    expected = Q(236416913460803, 432000000000000)
    assert polynomial_value(k) == expected
    masses = pairing(k)
    result = {
        "status": "PASS",
        "scope": "Exact polynomial replay for full randomized inner optimum and global capacity support; not a two-bidder optimum certificate",
        "k": str(k),
        "prices": {"item1": str(A), "item2": str(B), "bundle": str(C)},
        "exact_inner_revenue": str(expected),
        "value_polynomial_coefficients": ["59/108", "0", "1/4", "-1", "9/16"],
        "candidate_capacity_pairing": str(sum(masses)),
        "pairing_parts": {"item1_volume": str(masses[0]), "item1_top_edge": str(masses[1]), "item2_volume": str(masses[2])},
        "F_at_k": str(tail(k, k)),
        "value_derivative": str(-tail(k, k)),
        "three_partition_areas": ["1/3", "1/3", "1/3"],
        "polynomial_identity_degree_bound": 6,
        "exact_interpolation_nodes": [str(z) for z in nodes],
        "gap_identity": "<pi,r>-R=<pi,r-a>+3 integral_D0 u",
        "not_claimed": ["Outer bidder optimality against these prices", "Full two-bidder optimal revenue", "Formal machine verification of the measure proof"],
    }
    target = Path(__file__).resolve().parents[1] / "certificate" / "constrained_screening.json"
    if args.write:
        target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    else:
        assert json.loads(target.read_text(encoding="utf-8")) == result
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
