#!/usr/bin/env python3
"""Manifest-driven exact verifier for the two-level nonuniform stream bound."""

from __future__ import annotations

import itertools
import json
import math
import platform
from fractions import Fraction as Q
from pathlib import Path

import numpy as np

import dual_polynomials as dp


HERE = Path(__file__).resolve().parent
INT64_MAX = 2**63 - 1


def basis_exponents(degree):
    result = []
    for exponent in itertools.product(range(degree + 1), repeat=4):
        if sum(exponent) > degree:
            continue
        swapped = (exponent[1], exponent[0], exponent[3], exponent[2])
        if exponent < swapped:
            result.append((exponent, swapped))
    return result


def load_manifest():
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    degree = int(manifest["degree"])
    assert degree == 4
    basis = basis_exponents(degree)
    assert [tuple(value) for value in manifest["basis_order"]] == [
        pair[0] for pair in basis
    ]
    theta = [Q(value) for value in manifest["theta"]]
    assert len(theta) == len(basis) == 32
    assert [str(value) for value in theta] == manifest["theta"]
    assert max(value.denominator for value in theta) <= int(
        manifest["maximum_denominator"]
    )
    return manifest, theta, basis


def stream_components(theta, basis):
    x, y = dp.variable(0), dp.variable(1)
    boundary = dp.multiply(
        dp.multiply(x, dp.add(dp.ONE, dp.scale(x, -1))),
        dp.multiply(y, dp.add(dp.ONE, dp.scale(y, -1))),
    )
    antisymmetric = {}
    for coefficient, (exponent, swapped) in zip(theta, basis):
        difference = dp.add(
            dp.monomial(exponent), dp.scale(dp.monomial(swapped), -1)
        )
        antisymmetric = dp.add(
            antisymmetric, dp.scale(difference, coefficient)
        )
    stream = dp.multiply(boundary, antisymmetric)
    return dp.derivative(stream, 1), dp.scale(dp.derivative(stream, 0), -1)


def competitors(theta, basis, first_chart, second_chart):
    correction_one, _ = stream_components(theta, basis)
    substitutions = dp.chart_substitutions(first_chart, second_chart)
    s1, t1, s2, t2 = map(dp.variable, range(4))
    jacobian = dp.multiply(s1, s2)
    bidder_one_correction = dp.compose(correction_one, substitutions)
    bidder_two_correction = dp.compose(
        correction_one,
        [substitutions[2], substitutions[3], substitutions[0], substitutions[1]],
    )
    first_ray_coordinate = dp.ONE if first_chart == 0 else t1
    second_ray_coordinate = dp.ONE if second_chart == 0 else t2
    bidder_one_base = dp.multiply(
        dp.scale(
            dp.add(dp.scale(dp.multiply(s1, s1), 3), dp.scale(dp.ONE, -1)),
            Q(1, 2),
        ),
        dp.multiply(first_ray_coordinate, s2),
    )
    bidder_two_base = dp.multiply(
        dp.scale(
            dp.add(dp.scale(dp.multiply(s2, s2), 3), dp.scale(dp.ONE, -1)),
            Q(1, 2),
        ),
        dp.multiply(second_ray_coordinate, s1),
    )
    return (
        dp.add(bidder_one_base, dp.multiply(bidder_one_correction, jacobian)),
        dp.add(bidder_two_base, dp.multiply(bidder_two_correction, jacobian)),
    )


def bernstein_exact(polynomial):
    degrees = tuple(
        max((exponent[j] for exponent in polynomial), default=0)
        for j in range(4)
    )
    shape = tuple(degree + 1 for degree in degrees)
    controls = np.empty(shape, dtype=object)
    for index in np.ndindex(shape):
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
        controls[index] = value
    return controls


def fixed_controls(polynomial, scale):
    exact = bernstein_exact(polynomial)
    controls = np.empty(exact.shape, dtype=np.int64)
    for index in np.ndindex(exact.shape):
        value = exact[index]
        fixed = (value.numerator * scale) // value.denominator
        assert -INT64_MAX <= fixed <= INT64_MAX
        controls[index] = fixed
    return controls


def split_floor(controls, axis):
    degree = controls.shape[axis] - 1
    moved = np.moveaxis(controls, axis, 0)
    work = moved.copy()
    left = np.empty_like(moved)
    right = np.empty_like(moved)
    left[0] = work[0]
    right[degree] = work[degree]
    for level in range(1, degree + 1):
        assert int(np.max(np.abs(work))) <= INT64_MAX // 2
        work[: degree - level + 1] = (
            work[: degree - level + 1]
            + work[1 : degree - level + 2]
        ) // 2
        left[level] = work[0]
        right[degree - level] = work[degree - level]
    return np.moveaxis(left, 0, axis), np.moveaxis(right, 0, axis), degree


def mean_upper_integer(controls, error):
    total = sum(map(int, controls.flat))
    return -((-total) // controls.size) + error


def primitive(first, fe, second, se, difference, de):
    fmin, fmax = int(first.min()), int(first.max())
    smin, smax = int(second.min()), int(second.max())
    dmin, dmax = int(difference.min()), int(difference.max())
    if fmin - fe >= 0 and dmin - de >= 0:
        return True, mean_upper_integer(first, fe)
    if smin - se >= 0 and dmax + de <= 0:
        return True, mean_upper_integer(second, se)
    if fmax + fe <= 0 and smax + se <= 0:
        return True, 0
    return False, max(0, fmax + fe, smax + se)


def split_all(first, fe, second, se, difference, de, axis):
    fl, fr, fd = split_floor(first, axis)
    sl, sr, sd = split_floor(second, axis)
    dl, dr, dd = split_floor(difference, axis)
    errors = (fe + fd, se + sd, de + dd)
    return (fl, sl, dl, errors), (fr, sr, dr, errors)


def choose_variation_axis(first, second, difference):
    scores = []
    for axis in range(4):
        score = 0
        for controls in (first, second, difference):
            if controls.shape[axis] > 1:
                score = max(
                    score, int(np.max(np.abs(np.diff(controls, axis=axis))))
                )
        scores.append(score)
    return int(np.argmax(scores))


def best_children(first, fe, second, se, difference, de):
    best = None
    for axis in range(4):
        children = split_all(first, fe, second, se, difference, de, axis)
        child_results = tuple(
            primitive(a, errors[0], b, errors[1], d, errors[2])
            for a, b, d, errors in children
        )
        candidate = (
            sum(result[1] for result in child_results),
            axis,
            children,
            child_results,
        )
        if best is None or candidate[:2] < best[:2]:
            best = candidate
    return best


def empty_statistics():
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


def add_statistics(total, part):
    for key, value in part.items():
        if key == "maximum_error_seen":
            total[key] = max(total[key], value)
        else:
            total[key] += value


def process_chart(roots, base_depth, first_minimum, second_minimum):
    maximum_depth = base_depth + 2
    statistics = empty_statistics()
    accumulator = 0
    active_accumulator = 0
    stack = [(roots[0], 1, roots[1], 1, roots[2], 1, 0)]
    while stack:
        first, fe, second, se, difference, de, level = stack.pop()
        statistics["nodes"] += 1
        statistics["maximum_error_seen"] = max(
            statistics["maximum_error_seen"], fe, se, de
        )
        fixed, bound = primitive(first, fe, second, se, difference, de)
        if fixed:
            weight = 1 << (maximum_depth - level)
            accumulator += bound * weight
            active_accumulator += bound * (weight // 2)
            statistics["fixed_before_base"] += 1
            statistics["coverage_units"] += weight
            continue
        if level < base_depth:
            remaining = base_depth - level
            if remaining <= 4:
                children = best_children(
                    first, fe, second, se, difference, de
                )[2]
            else:
                axis = choose_variation_axis(first, second, difference)
                children = split_all(
                    first, fe, second, se, difference, de, axis
                )
            for a, b, d, errors in reversed(children):
                stack.append(
                    (a, errors[0], b, errors[1], d, errors[2], level + 1)
                )
            continue

        assert level == base_depth
        statistics["base_unresolved"] += 1
        first_split = best_children(first, fe, second, se, difference, de)
        first_savings = 2 * bound - first_split[0]
        if first_savings < first_minimum:
            accumulator += 4 * bound
            active_accumulator += 2 * bound
            statistics["base_retained"] += 1
            statistics["coverage_units"] += 4
            continue

        statistics["base_refined"] += 1
        statistics["first_savings_units"] += first_savings
        active_accumulator += first_split[0]
        for child, child_result in zip(first_split[2], first_split[3]):
            child_fixed, child_bound = child_result
            statistics["nodes"] += 1
            a, b, d, errors = child
            statistics["maximum_error_seen"] = max(
                statistics["maximum_error_seen"], *errors
            )
            if child_fixed:
                accumulator += 2 * child_bound
                statistics["first_level_fixed"] += 1
                statistics["coverage_units"] += 2
                continue

            statistics["first_level_unresolved"] += 1
            second_split = best_children(
                a, errors[0], b, errors[1], d, errors[2]
            )
            second_savings = 2 * child_bound - second_split[0]
            if second_savings < second_minimum:
                accumulator += 2 * child_bound
                statistics["first_level_retained"] += 1
                statistics["coverage_units"] += 2
                continue

            accumulator += second_split[0]
            statistics["first_level_refined"] += 1
            statistics["second_savings_units"] += second_savings
            statistics["second_level_fixed"] += sum(
                result[0] for result in second_split[3]
            )
            statistics["second_level_unresolved"] += sum(
                not result[0] for result in second_split[3]
            )
            statistics["maximum_error_seen"] = max(
                statistics["maximum_error_seen"],
                *(error for split_child in second_split[2]
                  for error in split_child[3]),
            )
            statistics["nodes"] += 2
            statistics["coverage_units"] += 2
    return accumulator, active_accumulator, statistics


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

    total_accumulator = 0
    total_active_accumulator = 0
    total_statistics = empty_statistics()
    maximum_initial_control = 0
    maximum_axis_degree = 0
    control_shapes = []
    for first_chart in range(2):
        for second_chart in range(2):
            first, second = competitors(
                theta, basis, first_chart, second_chart
            )
            difference = dp.add(first, dp.scale(second, -1))
            controls = tuple(
                fixed_controls(polynomial, scale)
                for polynomial in (first, second, difference)
            )
            control_shapes.append([list(array.shape) for array in controls])
            maximum_initial_control = max(
                maximum_initial_control,
                *(abs(int(value)) for array in controls
                  for value in (array.min(), array.max())),
            )
            maximum_axis_degree = max(
                maximum_axis_degree,
                *(size - 1 for array in controls for size in array.shape),
            )
            accumulator, active_accumulator, statistics = process_chart(
                controls, base_depth, first_minimum, second_minimum
            )
            total_accumulator += accumulator
            total_active_accumulator += active_accumulator
            add_statistics(total_statistics, statistics)

    symmetry_factor = int(certificate["item_symmetry_factor"])
    upper = Q(
        symmetry_factor * total_accumulator,
        scale * (1 << maximum_depth),
    )
    active_upper = Q(
        symmetry_factor * total_active_accumulator,
        scale * (1 << (maximum_depth - 1)),
    )
    claimed_active_accumulator = int(expected["active_depth22_accumulator"])
    claimed_active_upper = Q(expected["active_depth22_upper_bound"])
    assert total_active_accumulator == claimed_active_accumulator
    assert active_upper == claimed_active_upper
    active_statistics = expected["active_depth22_statistics"]
    assert total_statistics["fixed_before_base"] == int(
        active_statistics["fixed_before_base"]
    )
    assert total_statistics["base_unresolved"] == int(
        active_statistics["base_unresolved"]
    )
    assert total_statistics["base_refined"] == int(
        active_statistics["base_refined"]
    )
    assert total_statistics["base_retained"] == int(
        active_statistics["base_retained"]
    )
    assert total_statistics["first_level_fixed"] == int(
        active_statistics["first_level_fixed"]
    )
    assert total_statistics["first_level_unresolved"] == int(
        active_statistics["first_level_unresolved"]
    )
    assert total_statistics["first_savings_units"] == int(
        active_statistics["first_savings_units"]
    )
    assert maximum_initial_control == int(
        expected["maximum_initial_absolute_control"]
    )
    assert maximum_axis_degree == int(expected["maximum_axis_degree"])
    assert total_statistics["coverage_units"] == 4 * (1 << maximum_depth)
    assert 2 * maximum_initial_control < INT64_MAX
    assert symmetry_factor * total_accumulator < INT64_MAX
    assert upper < active_upper

    lower = Q(expected["certified_primal_lower_bound"])
    report = {
        "status": "UNSEALED_COMPUTATION",
        "python": platform.python_version(),
        "numpy": np.__version__,
        "degree": manifest["degree"],
        "basis_dimension": len(basis),
        "base_depth": base_depth,
        "maximum_depth": maximum_depth,
        "fixed_point_scale": scale,
        "control_shapes": control_shapes,
        "maximum_initial_absolute_control": maximum_initial_control,
        "maximum_axis_degree": maximum_axis_degree,
        "maximum_error_seen": total_statistics["maximum_error_seen"],
        "nodes": total_statistics["nodes"],
        "coverage_units": total_statistics["coverage_units"],
        "expected_coverage_units": 4 * (1 << maximum_depth),
        "accumulator": str(total_accumulator),
        "upper_fraction": str(upper),
        "active_depth22_accumulator": str(total_active_accumulator),
        "active_depth22_upper_fraction": str(active_upper),
        "strict_improvement": str(active_upper - upper),
        "certified_primal_lower_bound": str(lower),
        "remaining_exact_gap": str(upper - lower),
        "statistics": {
            key: (str(value) if key.endswith("savings_units") else value)
            for key, value in total_statistics.items()
        },
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
