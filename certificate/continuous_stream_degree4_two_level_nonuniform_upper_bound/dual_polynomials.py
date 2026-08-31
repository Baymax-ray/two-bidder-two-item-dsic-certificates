"""Exact sparse-polynomial operations for the two-level stream certificate."""

from __future__ import annotations

from fractions import Fraction as Q


ONE = {(0, 0, 0, 0): Q(1)}


def add(left, right):
    result = dict(left)
    for exponent, coefficient in right.items():
        result[exponent] = result.get(exponent, Q(0)) + coefficient
    return {key: value for key, value in result.items() if value}


def scale(polynomial, scalar):
    return {key: scalar * value for key, value in polynomial.items()
            if scalar * value}


def multiply(left, right):
    result = {}
    for exponent, coefficient in left.items():
        for other_exponent, other_coefficient in right.items():
            product = tuple(exponent[j] + other_exponent[j] for j in range(4))
            result[product] = (
                result.get(product, Q(0)) + coefficient * other_coefficient
            )
    return {key: value for key, value in result.items() if value}


def derivative(polynomial, axis):
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


def monomial(exponent):
    return {tuple(exponent): Q(1)}


def compose(polynomial, substitutions):
    result = {}
    for exponent, coefficient in polynomial.items():
        term = ONE
        for axis, power in enumerate(exponent):
            for _ in range(power):
                term = multiply(term, substitutions[axis])
        result = add(result, scale(term, coefficient))
    return result


def chart_substitutions(first_chart, second_chart):
    s1, t1, s2, t2 = map(variable, range(4))
    first = ((s1, multiply(s1, t1)) if first_chart == 0
             else (multiply(s1, t1), s1))
    second = ((s2, multiply(s2, t2)) if second_chart == 0
              else (multiply(s2, t2), s2))
    return [*first, *second]
