"""Self-contained degree-4 stream and chart-competitor construction."""
from __future__ import annotations

import itertools
from fractions import Fraction as Q

import dual_polynomials as dp


def basis_exponents():
    result = []
    for exponent in itertools.product(range(5), repeat=4):
        if sum(exponent) > 4:
            continue
        swapped = (exponent[1], exponent[0], exponent[3], exponent[2])
        if exponent < swapped:
            result.append((exponent, swapped))
    return result


def stream_components(theta, basis):
    x, y = dp.variable(0), dp.variable(1)
    boundary = dp.multiply(dp.multiply(x, dp.add(dp.ONE, dp.scale(x, -1))),
                           dp.multiply(y, dp.add(dp.ONE, dp.scale(y, -1))))
    antisymmetric = {}
    for coefficient, (exponent, swapped) in zip(theta, basis):
        difference = dp.add(dp.monomial(exponent), dp.scale(dp.monomial(swapped), -1))
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
        dp.scale(dp.add(dp.scale(dp.multiply(s1, s1), 3), dp.scale(dp.ONE, -1)), Q(1, 2)),
        dp.multiply(first_ray_coordinate, s2),
    )
    bidder_two_base = dp.multiply(
        dp.scale(dp.add(dp.scale(dp.multiply(s2, s2), 3), dp.scale(dp.ONE, -1)), Q(1, 2)),
        dp.multiply(second_ray_coordinate, s1),
    )
    return (dp.add(bidder_one_base, dp.multiply(bidder_one_correction, jacobian)),
            dp.add(bidder_two_base, dp.multiply(bidder_two_correction, jacobian)))
