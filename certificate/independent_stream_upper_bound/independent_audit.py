#!/usr/bin/env python3
"""Independent audit; only mathematical input is candidate_degree4_exact.json."""
from __future__ import annotations

import argparse, itertools, json, math, platform
from fractions import Fraction as Q
from pathlib import Path
import numpy as np

if not __debug__:
    raise RuntimeError("optimized mode is rejected because it removes audit assertions")

HERE = Path(__file__).resolve().parent
SCALE, BASE_DEPTH, FINAL_DEPTH = 10**9, 20, 21
EXPECTED_ACCUMULATOR = 930318295428931
EXPECTED_STATS = {
    "base_fixed": 235487, "base_unresolved": 277676,
    "base_refined": 233184, "base_held": 44492,
    "adaptive_splits": 233184,
    "adaptive_axis_counts": [58611, 58729, 57689, 58155],
    "adaptive_terminal_kinds": {
        "unresolved": 363695, "zero": 46361, "second": 28166, "first": 28146},
    "gain_units": 1308296197325}
EXPECTED_CHARTS = {
    "00": {"unresolved": 40608, "refined": 40510, "gain_units": 390596434610},
    "01": {"unresolved": 59853, "refined": 52869, "gain_units": 295250818800},
    "10": {"unresolved": 59848, "refined": 52876, "gain_units": 295305721446},
    "11": {"unresolved": 117367, "refined": 86929, "gain_units": 327143222469}}
TARGET = Q(372431922023109, 419430400000000)
I64_LIMIT = 2**63 - 1
ZERO = (0, 0, 0, 0)
ONE = {ZERO: Q(1)}


def p_add(a, b):
    out = dict(a)
    for e, c in b.items(): out[e] = out.get(e, Q(0)) + c
    return {e: c for e, c in out.items() if c}


def p_scale(a, k): return {e: k*c for e, c in a.items() if k*c}


def p_mul(a, b):
    out = {}
    for e, c in a.items():
        for f, d in b.items():
            g = tuple(e[j]+f[j] for j in range(4))
            out[g] = out.get(g, Q(0)) + c*d
    return {e: c for e, c in out.items() if c}


def p_derivative(a, axis):
    out = {}
    for e, c in a.items():
        if e[axis]:
            f = list(e); f[axis] -= 1
            out[tuple(f)] = c*e[axis]
    return out


def p_variable(axis):
    e = [0]*4; e[axis] = 1
    return {tuple(e): Q(1)}


def p_compose(poly, substitutions):
    out = {}
    for e, c in poly.items():
        term = ONE
        for axis, power in enumerate(e):
            for _ in range(power): term = p_mul(term, substitutions[axis])
        out = p_add(out, p_scale(term, c))
    return out


def reconstruct_basis():
    out = []
    for e in itertools.product(range(5), repeat=4):
        if sum(e) <= 4:
            f = (e[1], e[0], e[3], e[2])
            if e < f: out.append((e, f))
    return out


def load_candidate(path):
    raw = json.loads(path.read_text(encoding="utf-8"))
    basis = reconstruct_basis()
    assert raw["degree"] == 4 and len(basis) == 32
    assert raw["basis_order"] == [list(pair[0]) for pair in basis]
    assert raw["swap_rule"] == "(e0,e1,e2,e3)->(e1,e0,e3,e2)"
    theta = [Q(x) for x in raw["theta"]]
    assert len(theta) == 32
    assert max(x.denominator for x in theta) <= raw["maximum_denominator"]
    return theta, basis


def stream_component(theta, basis):
    x, y = p_variable(0), p_variable(1)
    boundary = p_mul(p_mul(x, p_add(ONE, p_scale(x, -1))),
                     p_mul(y, p_add(ONE, p_scale(y, -1))))
    anti = {}
    for c, (e, f) in zip(theta, basis):
        anti = p_add(anti, p_scale(p_add({e: Q(1)}, {f: Q(-1)}), c))
    return p_derivative(p_mul(boundary, anti), 1)


def chart_polynomials(theta, basis, c1, c2):
    correction = stream_component(theta, basis)
    s1, t1, s2, t2 = map(p_variable, range(4))
    xy1 = (s1, p_mul(s1, t1)) if c1 == 0 else (p_mul(s1, t1), s1)
    xy2 = (s2, p_mul(s2, t2)) if c2 == 0 else (p_mul(s2, t2), s2)
    subs = [*xy1, *xy2]
    jac = p_mul(s1, s2)
    corr1 = p_compose(correction, subs)
    corr2 = p_compose(correction, [subs[2], subs[3], subs[0], subs[1]])
    ray1, ray2 = (ONE if c1 == 0 else t1), (ONE if c2 == 0 else t2)
    base1 = p_mul(p_scale(p_add(p_scale(p_mul(s1, s1), 3), p_scale(ONE, -1)), Q(1,2)),
                  p_mul(ray1, s2))
    base2 = p_mul(p_scale(p_add(p_scale(p_mul(s2, s2), 3), p_scale(ONE, -1)), Q(1,2)),
                  p_mul(ray2, s1))
    first = p_add(base1, p_mul(corr1, jac))
    second = p_add(base2, p_mul(corr2, jac))
    return first, second, p_add(first, p_scale(second, -1))


def bernstein(poly):
    degrees = tuple(max((e[j] for e in poly), default=0) for j in range(4))
    out = np.empty(tuple(d+1 for d in degrees), dtype=object)
    for index in np.ndindex(out.shape):
        value = Q(0)
        for e, c in poly.items():
            if all(e[j] <= index[j] for j in range(4)):
                term = c
                for j in range(4):
                    term *= Q(math.comb(index[j], e[j]), math.comb(degrees[j], e[j]))
                value += term
        out[index] = value
    return out


def floor_controls(exact):
    out = np.empty(exact.shape, dtype=np.int64)
    for index in np.ndindex(exact.shape):
        x = exact[index]
        m = (x.numerator*SCALE)//x.denominator
        assert -I64_LIMIT <= m <= I64_LIMIT
        out[index] = m
    return out


def split_fixed(controls, axis):
    degree = controls.shape[axis]-1
    work = np.moveaxis(controls, axis, 0).copy()
    left, right = np.empty_like(work), np.empty_like(work)
    left[0], right[degree] = work[0], work[degree]
    for level in range(1, degree+1):
        work[:degree-level+1] = (work[:degree-level+1]+work[1:degree-level+2])//2
        left[level], right[degree-level] = work[0], work[degree-level]
    return np.moveaxis(left, 0, axis), np.moveaxis(right, 0, axis), degree


def split_exact(controls, axis):
    degree = controls.shape[axis]-1
    work = np.moveaxis(controls, axis, 0).copy()
    left, right = np.empty_like(work), np.empty_like(work)
    left[0], right[degree] = work[0], work[degree]
    for level in range(1, degree+1):
        work[:degree-level+1] = (work[:degree-level+1]+work[1:degree-level+2])/2
        left[level], right[degree-level] = work[0], work[degree-level]
    return np.moveaxis(left, 0, axis), np.moveaxis(right, 0, axis)


def ceil_mean(a, error):
    total = sum(map(int, a.flat))
    return -((-total)//a.size)+error


def primitive(a, ae, b, be, d, de):
    amin, amax, bmin, bmax = int(a.min()), int(a.max()), int(b.min()), int(b.max())
    dmin, dmax = int(d.min()), int(d.max())
    if amin-ae >= 0 and dmin-de >= 0: return True, ceil_mean(a, ae), "first"
    if bmin-be >= 0 and dmax+de <= 0: return True, ceil_mean(b, be), "second"
    if amax+ae <= 0 and bmax+be <= 0: return True, 0, "zero"
    return False, max(0, amax+ae, bmax+be), "unresolved"


def choose_axis(a, b, d):
    scores = []
    for axis in range(4):
        score = max(int(np.max(np.abs(np.diff(x, axis=axis)))) if x.shape[axis] > 1 else 0
                    for x in (a, b, d))
        scores.append(score)
    return max(range(4), key=lambda axis: scores[axis])


def split_triple(a, ae, b, be, d, de, axis):
    al, ar, ad = split_fixed(a, axis)
    bl, br, bd = split_fixed(b, axis)
    dl, dr, dd = split_fixed(d, axis)
    errors = (ae+ad, be+bd, de+dd)
    return (al, bl, dl, errors), (ar, br, dr, errors)


def child_score(children):
    return sum(primitive(x, e[0], y, e[1], z, e[2])[1]
               for x, y, z, e in children)


def audit_exact_node(fixed, errors, exact, counts):
    for m, error, q in zip(fixed, errors, exact):
        assert m.shape == q.shape
        for index in np.ndindex(m.shape):
            discrepancy = q[index]*SCALE-int(m[index])
            assert -error <= discrepancy <= error
            counts["control_enclosures"] += 1
    packed = (fixed[0], errors[0], fixed[1], errors[1], fixed[2], errors[2])
    is_fixed, charge, kind = primitive(*packed)
    first, second, difference = exact
    if kind == "first":
        assert min(first.flat) >= 0 and min(difference.flat) >= 0
        assert Q(charge, SCALE) >= sum(first.flat, Q(0))/first.size
    elif kind == "second":
        assert min(second.flat) >= 0 and max(difference.flat) <= 0
        assert Q(charge, SCALE) >= sum(second.flat, Q(0))/second.size
    elif kind == "zero":
        assert max(first.flat) <= 0 and max(second.flat) <= 0 and charge == 0
    else:
        assert not is_fixed
        assert Q(charge, SCALE) >= max(Q(0), max(first.flat), max(second.flat))
    counts["charge_checks"] += 1


def run_shallow(candidate):
    theta, basis = load_candidate(candidate)
    base_depth, final_depth = 5, 6
    counts = {"control_enclosures": 0, "charge_checks": 0, "terminal_boxes": 0}
    coverage = accumulator = 0
    for c1 in range(2):
        for c2 in range(2):
            polys = chart_polynomials(theta, basis, c1, c2)
            exact_roots = tuple(bernstein(poly) for poly in polys)
            fixed_roots = tuple(floor_controls(x) for x in exact_roots)

            def recurse(fixed, errors, exact, remaining, level):
                nonlocal coverage
                audit_exact_node(fixed, errors, exact, counts)
                packed = (fixed[0], errors[0], fixed[1], errors[1], fixed[2], errors[2])
                is_fixed, bound, _ = primitive(*packed)
                if is_fixed:
                    weight = 1 << (final_depth-level)
                    coverage += weight; counts["terminal_boxes"] += 1
                    return bound*weight
                if remaining == 0:
                    best, best_axis, best_children = bound << 1, None, None
                    for axis in range(4):
                        children = split_triple(*packed, axis)
                        score = child_score(children)
                        if score < best: best, best_axis, best_children = score, axis, children
                    coverage += 2
                    if best_axis is None:
                        counts["terminal_boxes"] += 1
                    else:
                        exact_children = [split_exact(x, best_axis) for x in exact]
                        for side, child in enumerate(best_children):
                            audit_exact_node(child[:3], child[3],
                                             tuple(pair[side] for pair in exact_children), counts)
                        counts["terminal_boxes"] += 2
                    return best
                candidates = []
                for axis in range(4):
                    children = split_triple(*packed, axis)
                    candidates.append((child_score(children), axis, children))
                _, axis, children = min(candidates, key=lambda item: (item[0], item[1]))
                exact_children = [split_exact(x, axis) for x in exact]
                return sum(recurse(child[:3], child[3],
                                   tuple(pair[side] for pair in exact_children),
                                   remaining-1, level+1)
                           for side, child in enumerate(children))

            accumulator += recurse(fixed_roots, (1,1,1), exact_roots, base_depth, 0)
    expected_coverage = 4*(1 << final_depth)
    assert coverage == expected_coverage
    report = {"status": "PASS", "mode": "shallow_paired_fraction",
              "base_depth": base_depth, "adaptive_extra_depth": 1,
              "scale": SCALE, "basis_dimension": len(basis),
              "coverage_units": coverage, "expected_coverage_units": expected_coverage,
              "accumulator": str(accumulator), **counts}
    print(json.dumps(report, indent=2))


def run_full(candidate):
    theta, basis = load_candidate(candidate)
    stats = {"base_fixed": 0, "base_unresolved": 0, "base_refined": 0,
             "base_held": 0, "adaptive_splits": 0,
             "adaptive_axis_counts": [0,0,0,0], "adaptive_terminal_kinds": {},
             "gain_units": 0}
    charts = {f"{a}{b}": {"unresolved": 0, "refined": 0, "gain_units": 0}
              for a in range(2) for b in range(2)}
    accumulator = coverage = maximum_initial = maximum_degree = 0
    for c1 in range(2):
        for c2 in range(2):
            exact = tuple(bernstein(poly) for poly in chart_polynomials(theta, basis, c1, c2))
            roots = tuple(floor_controls(x) for x in exact)
            maximum_initial = max(maximum_initial,
                                  *(abs(int(v)) for x in roots for v in (x.min(), x.max())))
            maximum_degree = max(maximum_degree, *(n-1 for x in roots for n in x.shape))
            chart = charts[f"{c1}{c2}"]

            def recurse(a, ae, b, be, d, de, remaining, level):
                nonlocal coverage
                packed = (a,ae,b,be,d,de)
                is_fixed, bound, _ = primitive(*packed)
                if is_fixed:
                    stats["base_fixed"] += 1
                    weight = 1 << (FINAL_DEPTH-level); coverage += weight
                    return bound*weight
                if remaining == 0:
                    stats["base_unresolved"] += 1; chart["unresolved"] += 1
                    baseline = bound << 1
                    best, best_axis, best_children = baseline, None, None
                    for axis in range(4):
                        children = split_triple(*packed, axis)
                        score = child_score(children)
                        if score < best: best, best_axis, best_children = score, axis, children
                    gain = baseline-best
                    stats["gain_units"] += gain; chart["gain_units"] += gain; coverage += 2
                    if best_axis is None:
                        stats["base_held"] += 1
                    else:
                        stats["base_refined"] += 1; stats["adaptive_splits"] += 1
                        stats["adaptive_axis_counts"][best_axis] += 1; chart["refined"] += 1
                        for child in best_children:
                            _, _, kind = primitive(child[0], child[3][0], child[1], child[3][1],
                                                   child[2], child[3][2])
                            terminal = stats["adaptive_terminal_kinds"]
                            terminal[kind] = terminal.get(kind, 0)+1
                    return best
                if remaining <= 4:
                    candidates = []
                    for axis in range(4):
                        children = split_triple(*packed, axis)
                        candidates.append((child_score(children), axis, children))
                    _, axis, children = min(candidates, key=lambda item: (item[0], item[1]))
                else:
                    axis = choose_axis(a,b,d); children = split_triple(*packed, axis)
                return sum(recurse(child[0], child[3][0], child[1], child[3][1],
                                   child[2], child[3][2], remaining-1, level+1)
                           for child in children)

            accumulator += recurse(roots[0],1,roots[1],1,roots[2],1,BASE_DEPTH,0)
    expected_coverage = 4*(1 << FINAL_DEPTH)
    assert coverage == expected_coverage
    assert accumulator == EXPECTED_ACCUMULATOR
    assert stats == EXPECTED_STATS, (stats, EXPECTED_STATS)
    assert charts == EXPECTED_CHARTS, (charts, EXPECTED_CHARTS)
    assert maximum_initial == 1475346733 and maximum_degree == 8
    maximum_error = 1+maximum_degree*FINAL_DEPTH
    maximum_stored = maximum_initial+maximum_degree*FINAL_DEPTH
    maximum_pair_sum = 2*maximum_stored
    maximum_box_numerator = (maximum_initial+maximum_error)*(1 << FINAL_DEPTH)
    assert maximum_pair_sum < I64_LIMIT and maximum_box_numerator < I64_LIMIT
    assert accumulator < I64_LIMIT
    upper = Q(2*accumulator, SCALE*(1 << FINAL_DEPTH))
    assert upper == Q(930318295428931, 1048576000000000) and upper < TARGET
    report = {"status": "PASS", "mode": "full_independent_replay",
              "python": platform.python_version(), "numpy": np.__version__,
              "basis_dimension": len(basis), "base_depth": BASE_DEPTH,
              "adaptive_extra_depth": 1, "common_final_depth": FINAL_DEPTH,
              "scale": SCALE, "maximum_initial_absolute_control": maximum_initial,
              "maximum_axis_degree": maximum_degree,
              "maximum_propagated_error_units": maximum_error,
              "maximum_stored_absolute_control_bound": maximum_stored,
              "maximum_int64_pair_sum_bound": maximum_pair_sum,
              "maximum_single_box_common_depth_numerator_bound": maximum_box_numerator,
              "signed_int64_limit": I64_LIMIT,
              "coverage_units": coverage, "expected_coverage_units": expected_coverage,
              "accumulator": str(accumulator), "upper_fraction": str(upper),
              "comparison_target": str(TARGET), "strict_margin": str(TARGET-upper),
              "statistics": stats, "chart_decomposition": charts}
    print(json.dumps(report, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("shallow", "full"))
    parser.add_argument("--candidate", type=Path, default=HERE/"candidate_degree4_exact.json")
    args = parser.parse_args()
    (run_shallow if args.mode == "shallow" else run_full)(args.candidate)


if __name__ == "__main__": main()
