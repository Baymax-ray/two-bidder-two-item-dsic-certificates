"""Exact targeted kink sign and actual-capacity reverse-direction witness."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
sys.path.insert(0, str(Path(__file__).resolve().parent))
import residual_lottery as r


def verify():
    checks = []
    witness = None
    for t in (F(7, 10), F(3, 4), F(4, 5)):
        delta, beta = r.menu_parameters(t)
        B, p = r.d+delta, t+beta*r.c
        Y = r.c+delta/(1-beta)
        assert 2*beta*(Y-r.c) == 3*t-2
        for portion in (F(1, 4), F(1, 2), F(3, 4)):
            y0 = r.c+portion*(Y-r.c)
            h, W = Y-y0, 1-p+beta*Y
            incumbent = y0*(W*h-beta*h*h/2)
            entrants = p*h*h/2
            bundle_loss = -Y*W*h
            predicted = -beta*(y0-r.c)*(Y-y0)**2/2
            assert incumbent+entrants+bundle_loss == predicted < 0
            margin = r.q-beta*(r.q+delta)
            assert margin > 0
            admissible_eps = min((1-beta)/4, margin/(4*(B-y0)))
            assert beta+admissible_eps < 1
            assert margin-admissible_eps*(B-y0) > 0
            shifted_Y = ((1-beta)*Y-admissible_eps*y0)/(1-beta-admissible_eps)
            assert Y < shifted_Y < B
            reverse_eps = beta/4
            eta = min((t-r.A)/2, reverse_eps*(y0-r.c)/2)
            x, y = t-eta, r.c
            rho = (r.b-t)/2
            baseline = r.old.candidate((t, rho, x, y))
            assert baseline['masks'][0] == 1
            assert baseline['payments'][0] == x
            assert not r.in_region((x, y))
            current = r.mechanism((t, rho, x, y))
            assert current['allocations'][0] == (F(1), F(0))
            old_max = max(x*a[0]+y*a[1]-price for a, price, label in r.menu((t, rho)))
            reverse_utility = x+(beta-reverse_eps)*y-(p-reverse_eps*y0)
            assert old_max == 0 < reverse_utility
            checks.append(dict(t=str(t), anchor=str(y0), derivative=str(predicted),
                               feasible_higher_epsilon=str(admissible_eps)))
            if witness is None:
                witness = dict(profile=list(map(str, (t, rho, x, y))),
                               old_bidder1_mask=baseline['masks'][0],
                               old_bidder1_payment=str(x),
                               added_allocation=['1', str(beta-reverse_eps)],
                               added_payment=str(p-reverse_eps*y0),
                               added_utility=str(reverse_utility),
                               old_bidder2_utility=str(old_max))
    data = dict(status='RESIDUAL_SECOND_LOTTERY_EXACT_PASS',
                scope='strict negative first variation for one anchored higher-slope family; opposite kink violates actual capacity; no full inner optimality claim',
                sign_formula='-beta*(y0-c)*(Y-y0)^2/2', checks=checks,
                actual_capacity_witness=witness)
    path = r.ROOT/'certificate'/'residual_second_lottery.json'
    if '--write' in sys.argv:
        path.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    else:
        assert json.loads(path.read_text(encoding='utf-8')) == data
    print(data['status'])
    print('exact_sign_and_actual_hole_cases', len(checks))
    return data


if __name__ == '__main__':
    verify()
