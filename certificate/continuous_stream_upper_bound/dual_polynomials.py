"""Self-contained exact sparse-polynomial primitives for the certificate."""
from __future__ import annotations

from fractions import Fraction as Q

ONE = {(0, 0, 0, 0): Q(1)}


def add(a, b):
    result = dict(a)
    for exponent, coefficient in b.items():
        result[exponent] = result.get(exponent, Q(0)) + coefficient
    return {e: c for e, c in result.items() if c}


def scale(a, coefficient):
    return {e: coefficient * c for e, c in a.items() if coefficient * c}


def multiply(a, b):
    result = {}
    for e, c in a.items():
        for f, d in b.items():
            ef = tuple(e[j] + f[j] for j in range(4))
            result[ef] = result.get(ef, Q(0)) + c * d
    return {e: c for e, c in result.items() if c}


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


def compose(polynomial, substitutions):
    result = {}
    for exponent, coefficient in polynomial.items():
        term = ONE
        for coordinate, power in enumerate(exponent):
            for _ in range(power):
                term = multiply(term, substitutions[coordinate])
        result = add(result, scale(term, coefficient))
    return result


def chart_substitutions(first_chart, second_chart):
    s1, t1, s2, t2 = map(variable, range(4))
    first = (s1, multiply(s1, t1)) if first_chart == 0 else (multiply(s1, t1), s1)
    second = (s2, multiply(s2, t2)) if second_chart == 0 else (multiply(s2, t2), s2)
    return [*first, *second]
