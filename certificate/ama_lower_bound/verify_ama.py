#!/usr/bin/env python3
"""Fail-closed exact verifier for a rational affine-maximizer lower bound.

The verifier trusts only the three rational parameters and claimed totals in
manifest.json.  It reconstructs the mechanism's polyhedral partition from the
score formulas below.  Every calculation uses fractions.Fraction.

For each full-dimensional refined cell it:
  1. enumerates every feasible intersection of four independent inequalities;
  2. reconstructs the exact facets, two-faces, and edges from those vertices;
  3. applies the canonical barycentric subdivision (all chains
     vertex < edge < two-face < facet < polytope); and
  4. integrates the cell's affine payment sum exactly over the resulting
     rational 4-simplices.

The barycentric-subdivision theorem for convex polytopes makes the simplices a
partition.  Thus no floating-point convex-hull oracle or optimizer summary is
part of the trusted path.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations, permutations
import json
from pathlib import Path
import sys


Form = tuple[tuple[Q, Q, Q, Q], Q]
Point = tuple[Q, Q, Q, Q]


def parse_q(text: str) -> Q:
    return Q(text)


def form(coeff=(0, 0, 0, 0), constant=0) -> Form:
    return tuple(Q(x) for x in coeff), Q(constant)


def form_add(*forms: Form) -> Form:
    return (
        tuple(sum((f[0][j] for f in forms), Q(0)) for j in range(4)),
        sum((f[1] for f in forms), Q(0)),
    )


def form_neg(f: Form) -> Form:
    return tuple(-x for x in f[0]), -f[1]


def form_sub(f: Form, g: Form) -> Form:
    return form_add(f, form_neg(g))


def form_value(f: Form, point: Point) -> Q:
    return sum((f[0][j] * point[j] for j in range(4)), f[1])


def matrix_rank(rows: list[list[Q]]) -> int:
    if not rows:
        return 0
    a = [row[:] for row in rows]
    m, n = len(a), len(a[0])
    rank = 0
    for col in range(n):
        pivot = next((r for r in range(rank, m) if a[r][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        p = a[rank][col]
        a[rank] = [x / p for x in a[rank]]
        for r in range(m):
            if r != rank and a[r][col]:
                q = a[r][col]
                a[r] = [a[r][k] - q * a[rank][k] for k in range(n)]
        rank += 1
        if rank == m:
            break
    return rank


_inverse_cache: dict[tuple[tuple[Q, ...], ...], tuple[tuple[Q, ...], ...] | None] = {}


def inverse4(rows: tuple[tuple[Q, ...], ...]):
    cached = _inverse_cache.get(rows, "missing")
    if cached != "missing":
        return cached
    a = [list(rows[r]) + [Q(int(r == c)) for c in range(4)] for r in range(4)]
    for col in range(4):
        pivot = next((r for r in range(col, 4) if a[r][col]), None)
        if pivot is None:
            _inverse_cache[rows] = None
            return None
        a[col], a[pivot] = a[pivot], a[col]
        p = a[col][col]
        a[col] = [x / p for x in a[col]]
        for r in range(4):
            if r != col and a[r][col]:
                q = a[r][col]
                a[r] = [a[r][k] - q * a[col][k] for k in range(8)]
    inv = tuple(tuple(a[r][4 + c] for c in range(4)) for r in range(4))
    _inverse_cache[rows] = inv
    return inv


def exact_vertices(inequalities: list[Form]) -> list[Point]:
    """Enumerate all vertices of the bounded H-polytope a.x+c >= 0."""
    vertices: set[Point] = set()
    for ids in combinations(range(len(inequalities)), 4):
        rows = tuple(inequalities[i][0] for i in ids)
        inv = inverse4(rows)
        if inv is None:
            continue
        constants = tuple(inequalities[i][1] for i in ids)
        point = tuple(
            -sum((inv[r][k] * constants[k] for k in range(4)), Q(0))
            for r in range(4)
        )
        if all(form_value(f, point) >= 0 for f in inequalities):
            vertices.add(point)
    return sorted(vertices)


def affine_dimension(vertex_ids: frozenset[int], vertices: list[Point]) -> int:
    if not vertex_ids:
        return -1
    ids = sorted(vertex_ids)
    if len(ids) == 1:
        return 0
    base = vertices[ids[0]]
    rows = [[vertices[i][j] - base[j] for j in range(4)] for i in ids[1:]]
    return matrix_rank(rows)


def barycenter(vertex_ids: frozenset[int], vertices: list[Point]) -> Point:
    n = len(vertex_ids)
    assert n
    return tuple(sum((vertices[i][j] for i in vertex_ids), Q(0)) / n for j in range(4))


_perms4 = tuple(
    (p, -1 if sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4)) % 2 else 1)
    for p in permutations(range(4))
)


def determinant4(rows: list[list[Q]]) -> Q:
    total = Q(0)
    for p, sign in _perms4:
        term = Q(sign)
        for r in range(4):
            term *= rows[r][p[r]]
        total += term
    return total


def validate_face_lattice(
    vertices: list[Point],
    inequalities: list[Form],
):
    all_vertices = frozenset(range(len(vertices)))

    facets_set: set[frozenset[int]] = set()
    for inequality in inequalities:
        face = frozenset(i for i, v in enumerate(vertices) if form_value(inequality, v) == 0)
        if affine_dimension(face, vertices) == 3:
            facets_set.add(face)
    facets = sorted(facets_set, key=lambda f: (len(f), tuple(sorted(f))))
    assert len(facets) >= 5, "a bounded 4-polytope needs at least five facets"

    ridges_set: set[frozenset[int]] = set()
    for f1, f2 in combinations(facets, 2):
        face = f1 & f2
        if affine_dimension(face, vertices) == 2:
            ridges_set.add(face)
    ridges = sorted(ridges_set, key=lambda f: (len(f), tuple(sorted(f))))

    ridge_edges: dict[frozenset[int], list[frozenset[int]]] = {}
    edges_set: set[frozenset[int]] = set()
    for ridge in ridges:
        candidates: set[frozenset[int]] = set()
        for facet in facets:
            face = ridge & facet
            if affine_dimension(face, vertices) == 1:
                candidates.add(face)
        edges = sorted(candidates, key=lambda f: tuple(sorted(f)))
        assert len(edges) == len(ridge), "two-face is not a verified polygon"
        degrees = {v: 0 for v in ridge}
        for edge in edges:
            assert len(edge) == 2, "a polytope edge must have exactly two endpoint vertices"
            for v in edge:
                degrees[v] += 1
            edges_set.add(edge)
        assert all(degrees[v] == 2 for v in ridge), "two-face edge graph is not a cycle"
        ridge_edges[ridge] = edges

    edges = sorted(edges_set, key=lambda f: tuple(sorted(f)))
    for ridge in ridges:
        assert sum(ridge <= facet for facet in facets) == 2, "a ridge must meet two facets"

    # Each three-dimensional facet must have a closed Eulerian boundary.
    for facet in facets:
        fv = {v for v in facet}
        fe = [e for e in edges if e <= facet]
        fr = [r for r in ridges if r <= facet]
        assert len(fv) - len(fe) + len(fr) == 2, "facet Euler check failed"
        for edge in fe:
            assert sum(edge <= ridge for ridge in fr) == 2, "facet boundary is not closed"

    assert len(vertices) - len(edges) + len(ridges) - len(facets) == 0, "4-polytope Euler check failed"
    return all_vertices, facets, ridges, ridge_edges


def integrate_cell(inequalities: list[Form], revenue: Form):
    vertices = exact_vertices(inequalities)
    vertex_ids = frozenset(range(len(vertices)))
    if affine_dimension(vertex_ids, vertices) < 4:
        return Q(0), Q(0), 0, len(vertices), (0, 0, 0)

    polytope, facets, ridges, ridge_edges = validate_face_lattice(vertices, inequalities)
    centers: dict[frozenset[int], Point] = {polytope: barycenter(polytope, vertices)}
    for face in facets + ridges:
        centers[face] = barycenter(face, vertices)
    for edges in ridge_edges.values():
        for edge in edges:
            centers[edge] = barycenter(edge, vertices)

    volume = Q(0)
    integral = Q(0)
    simplex_count = 0
    for facet in facets:
        for ridge in ridges:
            if not ridge <= facet:
                continue
            for edge in ridge_edges[ridge]:
                for endpoint in sorted(edge):
                    points = [
                        centers[polytope],
                        centers[facet],
                        centers[ridge],
                        centers[edge],
                        vertices[endpoint],
                    ]
                    rows = [
                        [points[r + 1][j] - points[0][j] for j in range(4)]
                        for r in range(4)
                    ]
                    simplex_volume = abs(determinant4(rows)) / 24
                    assert simplex_volume > 0, "degenerate barycentric simplex"
                    centroid = tuple(sum((p[j] for p in points), Q(0)) / 5 for j in range(4))
                    volume += simplex_volume
                    integral += simplex_volume * form_value(revenue, centroid)
                    simplex_count += 1
    return volume, integral, simplex_count, len(vertices), (len(facets), len(ridges), len(set(e for es in ridge_edges.values() for e in es)))


def build_mechanism(a: Q, b: Q, s: Q):
    # Outcome ids and allocations:
    # 0 none; 1/2 singleton to bidder 1; 3 both to bidder 1;
    # 4/5 singleton to bidder 2; 6 both to bidder 2; 7/8 the two splits.
    scores = [
        form(),
        form((1, 0, 0, 0), -a),
        form((0, 1, 0, 0), -a),
        form((1, 1, 0, 0), -b),
        form((0, 0, 1, 0), -a),
        form((0, 0, 0, 1), -a),
        form((0, 0, 1, 1), -b),
        form((1, 0, 0, 1), -s),
        form((0, 1, 1, 0), -s),
    ]
    costs = [Q(0), a, a, b, a, a, b, s, s]
    value_1 = [
        form(), form((1, 0, 0, 0)), form((0, 1, 0, 0)), form((1, 1, 0, 0)),
        form(), form(), form(), form((1, 0, 0, 0)), form((0, 1, 0, 0)),
    ]
    value_2 = [
        form(), form(), form(), form(), form((0, 0, 1, 0)), form((0, 0, 0, 1)),
        form((0, 0, 1, 1)), form((0, 0, 0, 1)), form((0, 0, 1, 0)),
    ]
    return scores, costs, value_1, value_2


def main() -> int:
    manifest_path = Path(__file__).with_name("manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["scope"] == "primal_lower_bound_only"
    parameters = manifest["parameters"]
    a = parse_q(parameters["single_item_cost_a"])
    b = parse_q(parameters["same_bidder_bundle_cost_b"])
    s = parse_q(parameters["split_allocation_cost_s"])
    assert (a, b, s) == (Q(159, 250), Q(91, 100), Q(1137, 1000))

    scores, costs, value_1, value_2 = build_mechanism(a, b, s)
    h1_ids = (0, 4, 5, 6)
    h2_ids = (0, 1, 2, 3)

    cube: list[Form] = []
    for j in range(4):
        lower = [0, 0, 0, 0]
        lower[j] = 1
        upper = [0, 0, 0, 0]
        upper[j] = -1
        cube.extend((form(lower, 0), form(upper, 1)))

    total_volume = Q(0)
    total_revenue = Q(0)
    full_cells = 0
    total_simplices = 0
    total_vertices = 0
    by_outcome = []

    for outcome in range(9):
        outcome_volume = Q(0)
        outcome_revenue = Q(0)
        outcome_cells = 0
        for h1 in h1_ids:
            for h2 in h2_ids:
                inequalities = cube + [
                    form_sub(scores[outcome], scores[r]) for r in range(9) if r != outcome
                ] + [
                    form_sub(scores[h1], scores[r]) for r in h1_ids if r != h1
                ] + [
                    form_sub(scores[h2], scores[r]) for r in h2_ids if r != h2
                ]
                # Exact duplicate inequalities do not change the cell.
                inequalities = list(dict.fromkeys(inequalities))
                revenue = form_add(
                    scores[h1], scores[h2], form_neg(value_1[outcome]),
                    form_neg(value_2[outcome]), form(constant=2 * costs[outcome]),
                )
                volume, integral, simplices, vertex_count, _ = integrate_cell(inequalities, revenue)
                if volume:
                    full_cells += 1
                    outcome_cells += 1
                    total_simplices += simplices
                    total_vertices += vertex_count
                    total_volume += volume
                    total_revenue += integral
                    outcome_volume += volume
                    outcome_revenue += integral
        by_outcome.append((outcome, outcome_cells, outcome_volume, outcome_revenue))

    expected = manifest["expected"]
    assert total_volume == parse_q(expected["total_cell_volume"]), (
        f"cell partition volume mismatch: {total_volume}"
    )
    assert total_revenue == parse_q(expected["expected_revenue"]), (
        f"revenue mismatch: {total_revenue}"
    )
    assert full_cells == int(expected["full_dimensional_refined_cells"]), (
        f"full-cell count mismatch: {full_cells}"
    )

    print("AMA LOWER-BOUND CERTIFICATE: PASS")
    print(f"parameters: a={a}, b={b}, s={s}")
    print(f"refined full-dimensional cells: {full_cells} / 144")
    print(f"enumerated cell vertices (with repetition across cells): {total_vertices}")
    print(f"exact barycentric 4-simplices: {total_simplices}")
    for outcome, cells, volume, revenue in by_outcome:
        print(f"outcome {outcome}: cells={cells}, volume={volume}, revenue={revenue}")
    print(f"total volume: {total_volume}")
    print(f"exact expected revenue: {total_revenue}")
    print(f"decimal expected revenue: {float(total_revenue):.15f}")
    print("scope: exact feasible/DSIC/ex-post-IR primal lower bound only; no global upper bound")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, ValueError, OSError) as exc:
        print(f"AMA LOWER-BOUND CERTIFICATE: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
