"""Exact polynomial construction for the continuous stream-dual certificate."""

from __future__ import annotations

import itertools
from fractions import Fraction as Q


ONE = {(0, 0, 0, 0): Q(1)}


def add(a, b):
    result = dict(a)
    for exponent, coefficient in b.items():
        result[exponent] = result.get(exponent, Q(0)) + coefficient
    return {exponent: coefficient for exponent, coefficient in result.items()
            if coefficient}


def scale(a, coefficient):
    return {exponent: coefficient * value for exponent, value in a.items()
            if coefficient * value}


def multiply(a, b):
    result = {}
    for exponent, coefficient in a.items():
        for other_exponent, other_coefficient in b.items():
            product_exponent = tuple(exponent[j] + other_exponent[j]
                                     for j in range(4))
            result[product_exponent] = (
                result.get(product_exponent, Q(0))
                + coefficient * other_coefficient
            )
    return {exponent: coefficient for exponent, coefficient in result.items()
            if coefficient}


def derivative(a, coordinate):
    result = {}
    for exponent, coefficient in a.items():
        if exponent[coordinate]:
            reduced = list(exponent)
            reduced[coordinate] -= 1
            result[tuple(reduced)] = coefficient * exponent[coordinate]
    return result


def variable(coordinate):
    exponent = [0] * 4
    exponent[coordinate] = 1
    return {tuple(exponent): Q(1)}


def monomial(exponent):
    return {exponent: Q(1)}


def basis_exponents():
    result = []
    for exponent in itertools.product(range(4), repeat=4):
        if sum(exponent) > 3:
            continue
        swapped = (exponent[1], exponent[0], exponent[3], exponent[2])
        if exponent < swapped:
            result.append((exponent, swapped))
    return result


def compose(polynomial, substitutions):
    result = {}
    for exponent, coefficient in polynomial.items():
        term = ONE
        for coordinate, power in enumerate(exponent):
            for _ in range(power):
                term = multiply(term, substitutions[coordinate])
        result = add(result, scale(term, coefficient))
    return result


def stream_components(theta):
    x, y = variable(0), variable(1)
    boundary = multiply(
        multiply(x, add(ONE, scale(x, -1))),
        multiply(y, add(ONE, scale(y, -1))),
    )
    antisymmetric_polynomial = {}
    for coefficient, (exponent, swapped) in zip(theta, basis_exponents()):
        difference = add(monomial(exponent), scale(monomial(swapped), -1))
        antisymmetric_polynomial = add(
            antisymmetric_polynomial, scale(difference, coefficient)
        )
    stream = multiply(boundary, antisymmetric_polynomial)
    return derivative(stream, 1), scale(derivative(stream, 0), -1)


def chart_substitutions(first_chart, second_chart):
    s1, t1, s2, t2 = map(variable, range(4))
    first = (s1, multiply(s1, t1)) if first_chart == 0 else (
        multiply(s1, t1), s1
    )
    second = (s2, multiply(s2, t2)) if second_chart == 0 else (
        multiply(s2, t2), s2
    )
    return [*first, *second]


def item_one_competitors(theta, first_chart, second_chart):
    correction_one, _ = stream_components(theta)
    substitutions = chart_substitutions(first_chart, second_chart)
    s1, t1, s2, t2 = map(variable, range(4))
    jacobian = multiply(s1, s2)

    bidder_one_correction = compose(correction_one, substitutions)
    bidder_two_correction = compose(
        correction_one,
        [substitutions[2], substitutions[3],
         substitutions[0], substitutions[1]],
    )

    first_ray_coordinate = ONE if first_chart == 0 else t1
    second_ray_coordinate = ONE if second_chart == 0 else t2
    bidder_one_base = multiply(
        scale(add(scale(multiply(s1, s1), 3), scale(ONE, -1)), Q(1, 2)),
        multiply(first_ray_coordinate, s2),
    )
    bidder_two_base = multiply(
        scale(add(scale(multiply(s2, s2), 3), scale(ONE, -1)), Q(1, 2)),
        multiply(second_ray_coordinate, s1),
    )
    return (
        add(bidder_one_base, multiply(bidder_one_correction, jacobian)),
        add(bidder_two_base, multiply(bidder_two_correction, jacobian)),
    )
