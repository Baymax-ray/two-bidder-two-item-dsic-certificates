#!/usr/bin/env python3
"""Non-importing exact replay of the degree-four nonuniform certificate."""
from __future__ import annotations

import itertools
import json
import math
import platform
from fractions import Fraction as Q
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ZERO = (0, 0, 0, 0)
ONE = {ZERO: Q(1)}
INT64_MAX = 2**63 - 1


def padd(left, right):
    result = dict(left)
    for exponent, coefficient in right.items():
        result[exponent] = result.get(exponent, Q(0)) + coefficient
        if not result[exponent]:
            del result[exponent]
    return result


def pscale(polynomial, scalar):
    return {exponent: scalar * coefficient
            for exponent, coefficient in polynomial.items()
            if scalar * coefficient}


def pmultiply(left, right):
    result = {}
    for exponent, coefficient in left.items():
        for other, other_coefficient in right.items():
            product = tuple(exponent[j] + other[j] for j in range(4))
            result[product] = (
                result.get(product, Q(0)) + coefficient * other_coefficient
            )
    return {exponent: coefficient for exponent, coefficient in result.items()
            if coefficient}


def pderivative(polynomial, axis):
    result = {}
    for exponent, coefficient in polynomial.items():
        if exponent[axis]:
            reduced = list(exponent)
            reduced[axis] -= 1
            result[tuple(reduced)] = coefficient * exponent[axis]
    return result


def variable(axis):
    exponent = [0, 0, 0, 0]
    exponent[axis] = 1
    return {tuple(exponent): Q(1)}


def pcompose(polynomial, substitutions):
    result = {}
    for exponent, coefficient in polynomial.items():
        term = ONE
        for axis, power in enumerate(exponent):
            for _ in range(power):
                term = pmultiply(term, substitutions[axis])
        result = padd(result, pscale(term, coefficient))
    return result


def basis_pairs(degree):
    result = []
    for exponent in itertools.product(range(degree + 1), repeat=4):
        if sum(exponent) > degree:
            continue
        swapped = (exponent[1], exponent[0], exponent[3], exponent[2])
        if exponent < swapped:
            result.append((exponent, swapped))
    return result


def correction_item_one(theta, basis):
    x, y = variable(0), variable(1)
    boundary = pmultiply(
        pmultiply(x, padd(ONE, pscale(x, -1))),
        pmultiply(y, padd(ONE, pscale(y, -1))),
    )
    antisymmetric = {}
    for coefficient, (exponent, swapped) in zip(theta, basis):
        antisymmetric = padd(
            antisymmetric, {exponent: coefficient, swapped: -coefficient}
        )
    return pderivative(pmultiply(boundary, antisymmetric), 1)


def chart_competitors(theta, basis, first_chart, second_chart):
    correction = correction_item_one(theta, basis)
    s1, t1, s2, t2 = (variable(j) for j in range(4))
    first = (s1, pmultiply(s1, t1)) if first_chart == 0 else (
        pmultiply(s1, t1), s1
    )
    second = (s2, pmultiply(s2, t2)) if second_chart == 0 else (
        pmultiply(s2, t2), s2
    )
    substitutions = [*first, *second]
    jacobian = pmultiply(s1, s2)
    bidder_one_correction = pcompose(correction, substitutions)
    bidder_two_correction = pcompose(
        correction,
        [substitutions[2], substitutions[3], substitutions[0], substitutions[1]],
    )
    first_direction = ONE if first_chart == 0 else t1
    second_direction = ONE if second_chart == 0 else t2
    bidder_one_base = pmultiply(
        pscale(padd(pscale(pmultiply(s1, s1), 3), pscale(ONE, -1)), Q(1, 2)),
        pmultiply(first_direction, s2),
    )
    bidder_two_base = pmultiply(
        pscale(padd(pscale(pmultiply(s2, s2), 3), pscale(ONE, -1)), Q(1, 2)),
        pmultiply(second_direction, s1),
    )
    return (
        padd(bidder_one_base, pmultiply(bidder_one_correction, jacobian)),
        padd(bidder_two_base, pmultiply(bidder_two_correction, jacobian)),
    )


def exact_bernstein(polynomial):
    degrees = tuple(
        max((exponent[j] for exponent in polynomial), default=0)
        for j in range(4)
    )
    shape = tuple(degree + 1 for degree in degrees)
    controls = []
    for index in itertools.product(*(range(size) for size in shape)):
        value = Q(0)
        for exponent, coefficient in polynomial.items():
            if all(exponent[j] <= index[j] for j in range(4)):
                term = coefficient
                for j in range(4):
                    term *= Q(
                        math.comb(index[j], exponent[j]),
                        math.comb(degrees[j], exponent[j]),
                    )
                value += term
        controls.append(value)
    return shape, controls


def floor_controls(polynomial, scale):
    shape, exact = exact_bernstein(polynomial)
    fixed = [(value.numerator * scale) // value.denominator for value in exact]
    assert all(Q(integer) <= scale * value < Q(integer + 1)
               for integer, value in zip(fixed, exact))
    assert max(map(abs, fixed), default=0) <= INT64_MAX
    return np.asarray(fixed, dtype=np.int64).reshape(shape)


def split_array(array, axis):
    degree = array.shape[axis] - 1
    moved = np.moveaxis(array, axis, 0)
    work = moved.copy()
    left = np.empty_like(moved)
    right = np.empty_like(moved)
    left[0] = work[0]
    right[degree] = work[degree]
    for stage in range(1, degree + 1):
        assert int(np.max(np.abs(work))) <= INT64_MAX // 2
        work[: degree - stage + 1] = (
            work[: degree - stage + 1] + work[1 : degree - stage + 2]
        ) // 2
        left[stage] = work[0]
        right[degree - stage] = work[degree - stage]
    return np.moveaxis(left, 0, axis), np.moveaxis(right, 0, axis), degree


def ceil_mean(array, error):
    total = sum(map(int, array.flat))
    return -((-total) // array.size) + error


def box_bound(arrays, errors):
    first, second, difference = arrays
    fe, se, de = errors
    fmin, fmax = int(first.min()), int(first.max())
    smin, smax = int(second.min()), int(second.max())
    dmin, dmax = int(difference.min()), int(difference.max())
    if fmin - fe >= 0 and dmin - de >= 0:
        return True, ceil_mean(first, fe)
    if smin - se >= 0 and dmax + de <= 0:
        return True, ceil_mean(second, se)
    if fmax + fe <= 0 and smax + se <= 0:
        return True, 0
    return False, max(0, fmax + fe, smax + se)


def split_box(arrays, errors, axis):
    pairs = []
    new_errors = []
    for array, error in zip(arrays, errors):
        left, right, degree = split_array(array, axis)
        pairs.append((left, right))
        new_errors.append(error + degree)
    child_errors = tuple(new_errors)
    return (
        (tuple(pair[0] for pair in pairs), child_errors),
        (tuple(pair[1] for pair in pairs), child_errors),
    )


def variation_axis(arrays):
    scores = []
    for axis in range(4):
        score = 0
        for array in arrays:
            if array.shape[axis] > 1:
                score = max(
                    score, int(np.max(np.abs(np.diff(array, axis=axis))))
                )
        scores.append(score)
    return max(range(4), key=lambda axis: scores[axis])


def best_split(arrays, errors):
    candidates = []
    for axis in range(4):
        children = split_box(arrays, errors, axis)
        child_results = tuple(box_bound(*child) for child in children)
        score = sum(result[1] for result in child_results)
        candidates.append((score, axis, children, child_results))
    return min(candidates, key=lambda candidate: candidate[:2])


def load_manifest():
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    degree = int(manifest["degree"])
    basis = basis_pairs(degree)
    assert degree == 4 and len(basis) == 32
    assert [pair[0] for pair in basis] == [
        tuple(exponent) for exponent in manifest["basis_order"]
    ]
    theta = tuple(Q(value) for value in manifest["theta"])
    assert tuple(str(value) for value in theta) == tuple(manifest["theta"])
    return manifest, theta, basis


def replay(manifest, theta, basis):
    certificate = manifest["certificate"]
    scale = int(certificate["fixed_point_scale"])
    base_depth = int(certificate["base_depth"])
    maximum_depth = int(certificate["maximum_depth"])
    minimum_savings = int(certificate["adaptive_min_savings_units"])
    assert maximum_depth == base_depth + 1
    statistics = {
        "nodes": 0,
        "fixed": 0,
        "leaves": 0,
        "refined_leaves": 0,
        "retained_leaves": 0,
        "refined_fixed_children": 0,
        "refined_unresolved_children": 0,
        "savings_units": 0,
        "coverage_units": 0,
        "maximum_error_seen": 0,
    }
    accumulator = 0
    maximum_initial_control = 0
    maximum_axis_degree = 0
    chart_reports = []
    for first_chart in range(2):
        for second_chart in range(2):
            first, second = chart_competitors(
                theta, basis, first_chart, second_chart
            )
            difference = padd(first, pscale(second, -1))
            arrays = tuple(
                floor_controls(polynomial, scale)
                for polynomial in (first, second, difference)
            )
            maximum_initial_control = max(
                maximum_initial_control,
                *(abs(int(value)) for array in arrays
                  for value in (array.min(), array.max())),
            )
            maximum_axis_degree = max(
                maximum_axis_degree,
                *(size - 1 for array in arrays for size in array.shape),
            )
            chart_accumulator = 0
            chart_fixed = chart_leaves = 0
            stack = [(arrays, (1, 1, 1), 0)]
            while stack:
                current, errors, level = stack.pop()
                statistics["nodes"] += 1
                statistics["maximum_error_seen"] = max(
                    statistics["maximum_error_seen"], *errors
                )
                fixed, bound = box_bound(current, errors)
                if fixed:
                    weight = 1 << (maximum_depth - level)
                    contribution = bound * weight
                    accumulator += contribution
                    chart_accumulator += contribution
                    statistics["fixed"] += 1
                    chart_fixed += 1
                    statistics["coverage_units"] += weight
                    continue
                if level == base_depth:
                    statistics["leaves"] += 1
                    chart_leaves += 1
                    statistics["coverage_units"] += 2
                    best = best_split(current, errors)
                    savings = 2 * bound - best[0]
                    if savings >= minimum_savings:
                        contribution = best[0]
                        statistics["refined_leaves"] += 1
                        statistics["refined_fixed_children"] += sum(
                            result[0] for result in best[3]
                        )
                        statistics["refined_unresolved_children"] += sum(
                            not result[0] for result in best[3]
                        )
                        statistics["savings_units"] += savings
                    else:
                        contribution = 2 * bound
                        statistics["retained_leaves"] += 1
                    accumulator += contribution
                    chart_accumulator += contribution
                    continue
                remaining = base_depth - level
                if remaining <= 4:
                    children = best_split(current, errors)[2]
                else:
                    children = split_box(current, errors, variation_axis(current))
                stack.append((children[1][0], children[1][1], level + 1))
                stack.append((children[0][0], children[0][1], level + 1))
            chart_reports.append({
                "charts": [first_chart, second_chart],
                "accumulator": str(chart_accumulator),
                "fixed": chart_fixed,
                "base_leaves": chart_leaves,
                "control_shapes": [list(array.shape) for array in arrays],
            })
    symmetry_factor = int(certificate["item_symmetry_factor"])
    upper = Q(symmetry_factor * accumulator, scale * (1 << maximum_depth))
    return {
        "accumulator": accumulator,
        "upper": upper,
        "maximum_initial_control": maximum_initial_control,
        "maximum_axis_degree": maximum_axis_degree,
        "statistics": statistics,
        "chart_reports": chart_reports,
    }


def main():
    manifest, theta, basis = load_manifest()
    result = replay(manifest, theta, basis)
    expected = manifest["expected"]
    statistics = result["statistics"]
    actual = (
        result["maximum_initial_control"],
        result["maximum_axis_degree"],
        result["accumulator"],
        str(result["upper"]),
        statistics["fixed"],
        statistics["leaves"],
        statistics["refined_leaves"],
        statistics["retained_leaves"],
        statistics["refined_fixed_children"],
        statistics["refined_unresolved_children"],
        statistics["savings_units"],
    )
    claimed = (
        int(expected["maximum_initial_absolute_control"]),
        int(expected["maximum_axis_degree"]),
        int(expected["accumulator"]),
        expected["upper_bound"],
        int(expected["base_fixed_winner_or_zero_boxes"]),
        int(expected["base_unresolved_leaves"]),
        int(expected["refined_leaves"]),
        int(expected["retained_leaves"]),
        int(expected["refined_fixed_children"]),
        int(expected["refined_unresolved_children"]),
        int(expected["savings_units"]),
    )
    assert actual == claimed, (actual, claimed)
    maximum_depth = int(manifest["certificate"]["maximum_depth"])
    expected_coverage = 4 * (1 << maximum_depth)
    assert statistics["coverage_units"] == expected_coverage
    target = Q(expected["comparison_target"])
    upper = result["upper"]
    assert upper.numerator * target.denominator < (
        target.numerator * upper.denominator
    )
    margin = target - upper
    assert str(margin) == expected["strict_margin"]
    lower = Q(expected["certified_primal_lower_bound"])
    gap = upper - lower
    assert str(gap) == expected["remaining_exact_gap"]
    assert 2 * result["maximum_initial_control"] < INT64_MAX
    assert 2 * result["accumulator"] < INT64_MAX
    report = {
        "status": "PASS",
        "implementation": "non_importing_iterative_replay",
        "python": platform.python_version(),
        "numpy": np.__version__,
        "basis_dimension": len(basis),
        "accumulator": str(result["accumulator"]),
        "upper_fraction": str(upper),
        "comparison_target": str(target),
        "strict_margin": str(margin),
        "fixed": statistics["fixed"],
        "base_leaves": statistics["leaves"],
        "refined_leaves": statistics["refined_leaves"],
        "retained_leaves": statistics["retained_leaves"],
        "refined_fixed_children": statistics["refined_fixed_children"],
        "refined_unresolved_children": statistics["refined_unresolved_children"],
        "savings_units": str(statistics["savings_units"]),
        "nodes": statistics["nodes"],
        "coverage_units": statistics["coverage_units"],
        "expected_coverage_units": expected_coverage,
        "maximum_error_seen": statistics["maximum_error_seen"],
        "remaining_exact_gap": str(gap),
        "chart_reports": result["chart_reports"],
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

