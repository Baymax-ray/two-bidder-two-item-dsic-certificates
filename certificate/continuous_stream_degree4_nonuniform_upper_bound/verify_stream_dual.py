#!/usr/bin/env python3
"""Read-only exact verifier for the degree-four nonuniform stream certificate."""
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
    representatives = [tuple(value) for value in manifest["basis_order"]]
    assert representatives == [pair[0] for pair in basis]
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
        antisymmetric = dp.add(antisymmetric, dp.scale(difference, coefficient))
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
            work[: degree - level + 1] + work[1 : degree - level + 2]
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
        child_results = [
            primitive(a, errors[0], b, errors[1], d, errors[2])
            for a, b, d, errors in children
        ]
        candidate = (sum(result[1] for result in child_results), axis,
                     children, child_results)
        if best is None or candidate[:2] < best[:2]:
            best = candidate
    return best


def recurse(first, fe, second, se, difference, de, remaining, level,
            base_depth, minimum_savings, statistics):
    statistics["nodes"] += 1
    statistics["maximum_error_seen"] = max(
        statistics["maximum_error_seen"], fe, se, de
    )
    fixed, bound = primitive(first, fe, second, se, difference, de)
    maximum_depth = base_depth + 1
    if fixed:
        weight = 1 << (maximum_depth - level)
        statistics["fixed"] += 1
        statistics["coverage_units"] += weight
        return bound * weight
    if remaining == 0:
        statistics["leaves"] += 1
        statistics["coverage_units"] += 2
        best = best_children(first, fe, second, se, difference, de)
        savings = 2 * bound - best[0]
        if savings >= minimum_savings:
            statistics["refined_leaves"] += 1
            statistics["refined_fixed_children"] += sum(
                result[0] for result in best[3]
            )
            statistics["refined_unresolved_children"] += sum(
                not result[0] for result in best[3]
            )
            statistics["savings_units"] += savings
            return best[0]
        statistics["retained_leaves"] += 1
        return 2 * bound
    if remaining <= 4:
        children = best_children(first, fe, second, se, difference, de)[2]
    else:
        axis = choose_variation_axis(first, second, difference)
        children = split_all(first, fe, second, se, difference, de, axis)
    return sum(
        recurse(a, errors[0], b, errors[1], d, errors[2], remaining - 1,
                level + 1, base_depth, minimum_savings, statistics)
        for a, b, d, errors in children
    )


def main():
    manifest, theta, basis = load_manifest()
    certificate = manifest["certificate"]
    expected = manifest["expected"]
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
    control_shapes = []
    for first_chart in range(2):
        for second_chart in range(2):
            first_poly, second_poly = competitors(
                theta, basis, first_chart, second_chart
            )
            difference_poly = dp.add(first_poly, dp.scale(second_poly, -1))
            controls = tuple(
                fixed_controls(polynomial, scale)
                for polynomial in (first_poly, second_poly, difference_poly)
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
            accumulator += recurse(
                controls[0], 1, controls[1], 1, controls[2], 1,
                base_depth, 0, base_depth, minimum_savings, statistics,
            )

    assert statistics["coverage_units"] == 4 * (1 << maximum_depth)
    symmetry_factor = int(certificate["item_symmetry_factor"])
    upper = Q(symmetry_factor * accumulator, scale * (1 << maximum_depth))
    actual = (
        maximum_initial_control,
        maximum_axis_degree,
        accumulator,
        str(upper),
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
    target = Q(expected["comparison_target"])
    assert upper.numerator * target.denominator < (
        target.numerator * upper.denominator
    )
    strict_margin = target - upper
    assert str(strict_margin) == expected["strict_margin"]
    lower = Q(expected["certified_primal_lower_bound"])
    remaining_gap = upper - lower
    assert str(remaining_gap) == expected["remaining_exact_gap"]
    assert 2 * maximum_initial_control < INT64_MAX
    assert symmetry_factor * accumulator < INT64_MAX

    report = {
        "status": "PASS",
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
        "maximum_error_seen": statistics["maximum_error_seen"],
        "nodes": statistics["nodes"],
        "coverage_units": statistics["coverage_units"],
        "expected_coverage_units": 4 * (1 << maximum_depth),
        "accumulator": str(accumulator),
        "upper_fraction": str(upper),
        "comparison_target": str(target),
        "strict_margin": str(strict_margin),
        "base_fixed_winner_or_zero_boxes": statistics["fixed"],
        "base_unresolved_leaves": statistics["leaves"],
        "refined_leaves": statistics["refined_leaves"],
        "retained_leaves": statistics["retained_leaves"],
        "refined_fixed_children": statistics["refined_fixed_children"],
        "refined_unresolved_children": statistics["refined_unresolved_children"],
        "savings_units": str(statistics["savings_units"]),
        "certified_primal_lower_bound": str(lower),
        "remaining_exact_gap": str(remaining_gap),
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

