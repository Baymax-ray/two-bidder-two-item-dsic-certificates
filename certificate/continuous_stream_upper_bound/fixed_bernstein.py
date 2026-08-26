"""Self-contained exact-to-fixed Bernstein arithmetic."""
from __future__ import annotations

import math
from fractions import Fraction as Q

import numpy as np


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def bernstein_exact(polynomial):
    degrees = tuple(max((e[j] for e in polynomial), default=0) for j in range(4))
    shape = tuple(d + 1 for d in degrees)
    controls = np.empty(shape, dtype=object)
    for index in np.ndindex(shape):
        coefficient = Q(0)
        for exponent, monomial_coefficient in polynomial.items():
            if all(exponent[j] <= index[j] for j in range(4)):
                contribution = monomial_coefficient
                for j in range(4):
                    contribution *= Q(math.comb(index[j], exponent[j]),
                                      math.comb(degrees[j], exponent[j]))
                coefficient += contribution
        controls[index] = coefficient
    return controls


def fixed_controls(polynomial, scale):
    exact = bernstein_exact(polynomial)
    controls = np.empty(exact.shape, dtype=np.int64)
    info = np.iinfo(np.int64)
    for index in np.ndindex(exact.shape):
        value = exact[index]
        fixed = (value.numerator * scale) // value.denominator
        require(info.min <= fixed <= info.max,
                f"fixed control outside int64 at {index}: {fixed}")
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
        work[:degree - level + 1] = (
            work[:degree - level + 1] + work[1:degree - level + 2]
        ) // 2
        left[level] = work[0]
        right[degree - level] = work[degree - level]
    return np.moveaxis(left, 0, axis), np.moveaxis(right, 0, axis), degree


def mean_upper_integer(controls, error):
    total = sum(map(int, controls.flat))
    return -((-total) // controls.size) + error


def choose_axis(first, second, difference):
    scores = []
    for axis in range(4):
        score = 0
        for controls in (first, second, difference):
            if controls.shape[axis] > 1:
                variation = int(np.max(np.abs(np.diff(controls, axis=axis))))
                score = max(score, variation)
        scores.append(score)
    return int(np.argmax(scores))
