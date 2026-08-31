#!/usr/bin/env python3
"""Independent iterative replay of the two-level nonuniform stream tree.

This file imports neither the certificate verifier nor any research code.  It
reconstructs the sparse polynomials, rational Bernstein roots, directed
fixed-point subdivision, winner tests, two selective levels, and accumulator.
"""

from __future__ import annotations

import itertools
import json
import math
import platform
from fractions import Fraction as Q
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
INT64_MAX = 2**63 - 1
ONE = {(0, 0, 0, 0): Q(1)}


def padd(left, right):
    answer = dict(left)
    for power, coefficient in right.items():
        answer[power] = answer.get(power, Q(0)) + coefficient
    return {power: coefficient for power, coefficient in answer.items()
            if coefficient}


def pscale(polynomial, scalar):
    return {power: scalar * coefficient
            for power, coefficient in polynomial.items()
            if scalar * coefficient}


def pmultiply(left, right):
    answer = {}
    for power, coefficient in left.items():
        for other_power, other_coefficient in right.items():
            product_power = tuple(power[k] + other_power[k] for k in range(4))
            answer[product_power] = (
                answer.get(product_power, Q(0))
                + coefficient * other_coefficient
            )
    return {power: coefficient for power, coefficient in answer.items()
            if coefficient}


def pderivative(polynomial, coordinate):
    answer = {}
    for power, coefficient in polynomial.items():
        if power[coordinate]:
            reduced = list(power)
            reduced[coordinate] -= 1
            answer[tuple(reduced)] = coefficient * power[coordinate]
    return answer


def variable(coordinate):
    power = [0, 0, 0, 0]
    power[coordinate] = 1
    return {tuple(power): Q(1)}


def pcompose(polynomial, substitutions):
    answer = {}
    for power, coefficient in polynomial.items():
        term = ONE
        for coordinate, exponent in enumerate(power):
            for _ in range(exponent):
                term = pmultiply(term, substitutions[coordinate])
        answer = padd(answer, pscale(term, coefficient))
    return answer


def basis_pairs(degree):
    pairs = []
    for power in itertools.product(range(degree + 1), repeat=4):
        if sum(power) <= degree:
            swapped = (power[1], power[0], power[3], power[2])
            if power < swapped:
                pairs.append((power, swapped))
    return pairs


def correction_item_one(theta, basis):
    x, y = variable(0), variable(1)
    boundary = pmultiply(
        pmultiply(x, padd(ONE, pscale(x, -1))),
        pmultiply(y, padd(ONE, pscale(y, -1))),
    )
    antisymmetric = {}
    for coefficient, (power, swapped) in zip(theta, basis):
        monomial = {power: Q(1)}
        swapped_monomial = {swapped: Q(1)}
        antisymmetric = padd(
            antisymmetric,
            pscale(padd(monomial, pscale(swapped_monomial, -1)), coefficient),
        )
    return pderivative(pmultiply(boundary, antisymmetric), 1)


def chart_competitors(theta, basis, first_chart, second_chart):
    correction = correction_item_one(theta, basis)
    s1, t1, s2, t2 = map(variable, range(4))
    first_pair = ((s1, pmultiply(s1, t1)) if first_chart == 0
                  else (pmultiply(s1, t1), s1))
    second_pair = ((s2, pmultiply(s2, t2)) if second_chart == 0
                   else (pmultiply(s2, t2), s2))
    substitutions = [*first_pair, *second_pair]
    jacobian = pmultiply(s1, s2)
    first_correction = pcompose(correction, substitutions)
    second_correction = pcompose(
        correction,
        [substitutions[2], substitutions[3], substitutions[0], substitutions[1]],
    )
    first_ray = ONE if first_chart == 0 else t1
    second_ray = ONE if second_chart == 0 else t2
    first_base = pmultiply(
        pscale(
            padd(pscale(pmultiply(s1, s1), 3), pscale(ONE, -1)),
            Q(1, 2),
        ),
        pmultiply(first_ray, s2),
    )
    second_base = pmultiply(
        pscale(
            padd(pscale(pmultiply(s2, s2), 3), pscale(ONE, -1)),
            Q(1, 2),
        ),
        pmultiply(second_ray, s1),
    )
    return (
        padd(first_base, pmultiply(first_correction, jacobian)),
        padd(second_base, pmultiply(second_correction, jacobian)),
    )


def exact_bernstein(polynomial):
    degrees = tuple(
        max((power[k] for power in polynomial), default=0) for k in range(4)
    )
    shape = tuple(degree + 1 for degree in degrees)
    values = []
    for index in itertools.product(*(range(size) for size in shape)):
        value = Q(0)
        for power, coefficient in polynomial.items():
            if all(power[k] <= index[k] for k in range(4)):
                term = coefficient
                for k in range(4):
                    term *= Q(
                        math.comb(index[k], power[k]),
                        math.comb(degrees[k], power[k]),
                    )
                value += term
        values.append(value)
    return shape, values


def floor_array(polynomial, scale):
    shape, exact = exact_bernstein(polynomial)
    fixed = [(value.numerator * scale) // value.denominator for value in exact]
    assert all(Q(integer) <= scale * value < Q(integer + 1)
               for integer, value in zip(fixed, exact))
    assert max(map(abs, fixed), default=0) <= INT64_MAX
    return np.asarray(fixed, dtype=np.int64).reshape(shape)


def bisect_array(array, axis):
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
            work[: degree - stage + 1]
            + work[1 : degree - stage + 2]
        ) // 2
        left[stage] = work[0]
        right[degree - stage] = work[degree - stage]
    return np.moveaxis(left, 0, axis), np.moveaxis(right, 0, axis), degree


def ceil_average(array, radius):
    total = sum(map(int, array.flat))
    return -((-total) // array.size) + radius


def local_bound(arrays, radii):
    first, second, difference = arrays
    fe, se, de = radii
    fmin, fmax = int(first.min()), int(first.max())
    smin, smax = int(second.min()), int(second.max())
    dmin, dmax = int(difference.min()), int(difference.max())
    if fmin - fe >= 0 and dmin - de >= 0:
        return True, ceil_average(first, fe)
    if smin - se >= 0 and dmax + de <= 0:
        return True, ceil_average(second, se)
    if fmax + fe <= 0 and smax + se <= 0:
        return True, 0
    return False, max(0, fmax + fe, smax + se)


def split_box(arrays, radii, axis):
    pairs = []
    child_radii = []
    for array, radius in zip(arrays, radii):
        left, right, degree = bisect_array(array, axis)
        pairs.append((left, right))
        child_radii.append(radius + degree)
    errors = tuple(child_radii)
    return (
        (tuple(pair[0] for pair in pairs), errors),
        (tuple(pair[1] for pair in pairs), errors),
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


def best_split(arrays, radii):
    candidates = []
    for axis in range(4):
        children = split_box(arrays, radii, axis)
        results = tuple(local_bound(*child) for child in children)
        candidates.append(
            (sum(result[1] for result in results), axis, children, results)
        )
    return min(candidates, key=lambda candidate: candidate[:2])


def blank_statistics():
    return {
        "nodes": 0,
        "fixed_before_base": 0,
        "base_unresolved": 0,
        "base_refined": 0,
        "base_retained": 0,
        "first_level_fixed": 0,
        "first_level_unresolved": 0,
        "first_level_refined": 0,
        "first_level_retained": 0,
        "second_level_fixed": 0,
        "second_level_unresolved": 0,
        "first_savings_units": 0,
        "second_savings_units": 0,
        "coverage_units": 0,
        "maximum_error_seen": 0,
    }


def merge_statistics(total, chart):
    for name in total:
        if name == "maximum_error_seen":
            total[name] = max(total[name], chart[name])
        else:
            total[name] += chart[name]


def traverse_chart(roots, base_depth, first_minimum, second_minimum):
    terminal_depth = base_depth + 2
    statistics = blank_statistics()
    total = 0
    depth22_total = 0
    worklist = [(roots, (1, 1, 1), 0)]
    while worklist:
        arrays, radii, level = worklist.pop()
        statistics["nodes"] += 1
        statistics["maximum_error_seen"] = max(
            statistics["maximum_error_seen"], *radii
        )
        fixed, bound = local_bound(arrays, radii)
        if fixed:
            weight = 1 << (terminal_depth - level)
            total += bound * weight
            depth22_total += bound * (weight // 2)
            statistics["fixed_before_base"] += 1
            statistics["coverage_units"] += weight
            continue
        if level < base_depth:
            remaining = base_depth - level
            children = (
                best_split(arrays, radii)[2]
                if remaining <= 4
                else split_box(arrays, radii, variation_axis(arrays))
            )
            for child in reversed(children):
                worklist.append((child[0], child[1], level + 1))
            continue

        assert level == base_depth
        statistics["base_unresolved"] += 1
        first = best_split(arrays, radii)
        first_savings = 2 * bound - first[0]
        if first_savings < first_minimum:
            total += 4 * bound
            depth22_total += 2 * bound
            statistics["base_retained"] += 1
            statistics["coverage_units"] += 4
            continue

        statistics["base_refined"] += 1
        statistics["first_savings_units"] += first_savings
        depth22_total += first[0]
        for child, result in zip(first[2], first[3]):
            statistics["nodes"] += 1
            child_arrays, child_radii = child
            statistics["maximum_error_seen"] = max(
                statistics["maximum_error_seen"], *child_radii
            )
            fixed_child, child_bound = result
            if fixed_child:
                total += 2 * child_bound
                statistics["first_level_fixed"] += 1
                statistics["coverage_units"] += 2
                continue

            statistics["first_level_unresolved"] += 1
            second = best_split(child_arrays, child_radii)
            second_savings = 2 * child_bound - second[0]
            if second_savings < second_minimum:
                total += 2 * child_bound
                statistics["first_level_retained"] += 1
                statistics["coverage_units"] += 2
                continue

            total += second[0]
            statistics["first_level_refined"] += 1
            statistics["second_savings_units"] += second_savings
            statistics["second_level_fixed"] += sum(
                result[0] for result in second[3]
            )
            statistics["second_level_unresolved"] += sum(
                not result[0] for result in second[3]
            )
            statistics["maximum_error_seen"] = max(
                statistics["maximum_error_seen"],
                *(radius for grandchild in second[2]
                  for radius in grandchild[1]),
            )
            statistics["nodes"] += 2
            statistics["coverage_units"] += 2
    return total, depth22_total, statistics


def load_manifest():
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    degree = int(manifest["degree"])
    basis = basis_pairs(degree)
    theta = tuple(Q(value) for value in manifest["theta"])
    assert degree == 4 and len(theta) == len(basis) == 32
    assert [pair[0] for pair in basis] == [
        tuple(power) for power in manifest["basis_order"]
    ]
    assert tuple(str(value) for value in theta) == tuple(manifest["theta"])
    assert max(value.denominator for value in theta) <= int(
        manifest["maximum_denominator"]
    )
    return manifest, theta, basis


def main():
    manifest, theta, basis = load_manifest()
    certificate = manifest["certificate"]
    expected = manifest["expected"]
    scale = int(certificate["fixed_point_scale"])
    base_depth = int(certificate["base_depth"])
    maximum_depth = int(certificate["maximum_depth"])
    first_minimum = int(certificate["first_level_minimum_savings_units"])
    second_minimum = int(certificate["second_level_minimum_savings_units"])
    assert maximum_depth == base_depth + 2
    assert first_minimum == second_minimum == 1

    accumulator = 0
    active_accumulator = 0
    statistics = blank_statistics()
    maximum_initial_control = 0
    maximum_axis_degree = 0
    shapes = []
    for first_chart in range(2):
        for second_chart in range(2):
            first, second = chart_competitors(
                theta, basis, first_chart, second_chart
            )
            difference = padd(first, pscale(second, -1))
            roots = tuple(
                floor_array(polynomial, scale)
                for polynomial in (first, second, difference)
            )
            shapes.append([list(array.shape) for array in roots])
            maximum_initial_control = max(
                maximum_initial_control,
                *(abs(int(value)) for array in roots
                  for value in (array.min(), array.max())),
            )
            maximum_axis_degree = max(
                maximum_axis_degree,
                *(size - 1 for array in roots for size in array.shape),
            )
            chart_total, chart_active, chart_statistics = traverse_chart(
                roots, base_depth, first_minimum, second_minimum
            )
            accumulator += chart_total
            active_accumulator += chart_active
            merge_statistics(statistics, chart_statistics)

    symmetry = int(certificate["item_symmetry_factor"])
    upper = Q(symmetry * accumulator, scale * (1 << maximum_depth))
    active_upper = Q(
        symmetry * active_accumulator,
        scale * (1 << (maximum_depth - 1)),
    )
    assert maximum_initial_control == int(
        expected["maximum_initial_absolute_control"]
    )
    assert maximum_axis_degree == int(expected["maximum_axis_degree"])
    assert active_accumulator == int(expected["active_depth22_accumulator"])
    assert active_upper == Q(expected["active_depth22_upper_bound"])
    old_statistics = expected["active_depth22_statistics"]
    for name in (
        "fixed_before_base", "base_unresolved", "base_refined",
        "base_retained", "first_level_fixed", "first_level_unresolved",
    ):
        assert statistics[name] == int(old_statistics[name])
    assert statistics["first_savings_units"] == int(
        old_statistics["first_savings_units"]
    )
    expected_coverage = 4 * (1 << maximum_depth)
    assert statistics["coverage_units"] == expected_coverage
    assert 2 * maximum_initial_control < INT64_MAX
    assert symmetry * accumulator < INT64_MAX
    assert upper < active_upper

    lower = Q(expected["certified_primal_lower_bound"])
    rendered_statistics = {
        name: (str(value) if name.endswith("savings_units") else value)
        for name, value in statistics.items()
    }
    report = {
        "status": "UNSEALED_COMPUTATION",
        "python": platform.python_version(),
        "numpy": np.__version__,
        "degree": manifest["degree"],
        "basis_dimension": len(basis),
        "base_depth": base_depth,
        "maximum_depth": maximum_depth,
        "fixed_point_scale": scale,
        "control_shapes": shapes,
        "maximum_initial_absolute_control": maximum_initial_control,
        "maximum_axis_degree": maximum_axis_degree,
        "maximum_error_seen": statistics["maximum_error_seen"],
        "nodes": statistics["nodes"],
        "coverage_units": statistics["coverage_units"],
        "expected_coverage_units": expected_coverage,
        "accumulator": str(accumulator),
        "upper_fraction": str(upper),
        "active_depth22_accumulator": str(active_accumulator),
        "active_depth22_upper_fraction": str(active_upper),
        "strict_improvement": str(active_upper - upper),
        "certified_primal_lower_bound": str(lower),
        "remaining_exact_gap": str(upper - lower),
        "statistics": rendered_statistics,
    }
    promoted = expected["promoted"]
    if expected["status"] == "SEALED":
        assert isinstance(promoted, dict)
        actual = {
            "accumulator": report["accumulator"],
            "upper_fraction": report["upper_fraction"],
            "strict_improvement": report["strict_improvement"],
            "remaining_exact_gap": report["remaining_exact_gap"],
            "maximum_error_seen": report["maximum_error_seen"],
            "nodes": report["nodes"],
            "coverage_units": report["coverage_units"],
            "statistics": report["statistics"],
        }
        assert actual == promoted, (actual, promoted)
        report["status"] = "PASS"
    else:
        assert expected["status"] == "PENDING_INDEPENDENT_REPLAY"
        assert promoted is None
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
