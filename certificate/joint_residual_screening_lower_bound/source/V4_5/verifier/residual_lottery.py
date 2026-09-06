"""Exact V4.5 actual-residual lottery splice and rational revenue gain.

The continuum proof is research_log/residual_lottery_extension.md.
Default execution replays the certificate without writes; --write creates it.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent/'V4_02'/'verifier'))
import split_cost_candidate as old

P = old.v3.P
X = P((0, 1))
A, b, c = F(2, 3), old.B, old.base.C
d, q, q_old = F(1, 2), F(113, 500), F(227, 1000)
T, U = (2+2*q)/3, (2+6*q)/3
DELTA0 = P(F(1, 2)-c+F(3, 4)*q*q)-F(3, 2)*q*X
DELTA = DELTA0+F(1, 16)*(3*X-2)**2
DELTA_OLD = P(F(1, 2)-c+F(3, 4)*q_old*q_old)-F(3, 2)*q_old*X
OLD_CUTOFF = (F(1, 2)-c+F(3, 4)*q_old*q_old)/(F(3, 2)*q_old)


def in_region(opponent):
    t = max(opponent)
    return A < t < T and sum(opponent) <= b


def menu_parameters(t):
    t = F(t)
    assert A <= t <= T
    delta = DELTA(t)
    beta = (3*t-2)/(3*t-2+2*delta)
    assert delta >= 0 and 0 <= beta <= 1
    assert beta*(q+delta) <= q
    return delta, beta


def menu(opponent):
    """Aligned allocations are rotated back into the physical item order."""
    opponent = tuple(map(F, opponent))
    t = max(opponent)
    delta, beta = menu_parameters(t)
    rows = [((F(0), F(0)), F(0), 'empty'),
            ((F(0), F(1)), d+delta, 'low'),
            ((F(1), F(0)), t, 'high'),
            ((F(1), F(1)), t+c+delta, 'bundle'),
            ((F(1), beta), t+beta*c, 'lottery')]
    if opponent[0] < opponent[1]:
        rows = [(tuple(reversed(a)), p, label) for a, p, label in rows]
    return rows


def asymmetric_mechanism(profile):
    """Complete auction; bidder 1 is exactly V4.02, including its ties."""
    profile = tuple(map(F, profile))
    assert len(profile) == 4 and all(0 <= x <= 1 for x in profile)
    before = old.candidate(profile)
    allocations = tuple(tuple(F(bool(mask & (1 << j))) for j in range(2))
                        for mask in before['masks'])
    result = dict(profile=profile, allocations=allocations,
                  payments=before['payments'], utilities=before['utilities'],
                  branch='retained_V4_02', selected=None)
    if not in_region(profile[:2]):
        return result
    rows = menu(profile[:2])
    values = [sum(x*a for x, a in zip(profile[2:], row[0]))-row[1] for row in rows]
    best = max(values)
    selected = next(i for i, value in enumerate(values) if value == best)
    allocation, payment, label = rows[selected]
    assert all(allocations[0][j]+allocation[j] <= 1 for j in range(2))
    assert payment >= 0 and best >= 0
    result.update(allocations=(allocations[0], allocation),
                  payments=(before['payments'][0], payment),
                  utilities=(before['utilities'][0], best),
                  branch='residual_lottery', selected=label, menu=rows)
    return result


def mechanism(profile):
    """Both independently optimal-in-family conditional splices, all ties."""
    profile = tuple(map(F, profile))
    result = asymmetric_mechanism(profile)
    if not in_region(profile[2:]):
        return result
    rows = menu(profile[2:])
    values = [sum(x*a for x, a in zip(profile[:2], row[0]))-row[1] for row in rows]
    best = max(values)
    selected = next(i for i, value in enumerate(values) if value == best)
    allocation, payment, label = rows[selected]
    assert all(allocation[j]+result['allocations'][1][j] <= 1 for j in range(2))
    result.update(allocations=(allocation, result['allocations'][1]),
                  payments=(payment, result['payments'][1]),
                  utilities=(best, result['utilities'][1]),
                  bidder1_branch='residual_lottery', bidder1_selected=label)
    return result


def revenue_data():
    poly1 = (DELTA-DELTA_OLD)**2+F(1, 8)*DELTA_OLD*(3*X-2)**2
    poly2 = DELTA**2
    G = old.v3.revenue
    new4 = G(X, d+DELTA, X+c+DELTA)
    old4a = G(X, d+DELTA_OLD, X+c+DELTA_OLD)
    old4b = G(X, P(d), X+c)
    lottery_gain = F(1, 8)*DELTA*(3*X-2)**2
    assert (new4-old4a+lottery_gain-poly1).zero()
    assert (new4-old4b+lottery_gain-poly2).zero()
    integrand1, integrand2 = 2*(b-X)*poly1, 2*(b-X)*poly2
    gain1 = integrand1.integral(A, OLD_CUTOFF)
    gain2 = integrand2.integral(OLD_CUTOFF, T)
    assert gain1 > 0 and gain2 > 0
    return dict(gain=str(2*(gain1+gain2)), asymmetric_gain=str(gain1+gain2),
                gain_before_old_cutoff=str(gain1),
                gain_after_old_cutoff=str(gain2),
                integrand_before=[str(x) for x in integrand1.c],
                integrand_after=[str(x) for x in integrand2.c])


def verify():
    assert old.CANDIDATE_SPLIT-old.A == d and old.CANDIDATE_SPLIT-b == q
    assert c+q == d
    assert (DELTA-F(9, 16)*(T-X)*(U-X)).zero()
    assert A < OLD_CUTOFF < T < b < 1 < U
    assert DELTA(T) == 0 and menu_parameters(A)[1] == 0
    assert menu_parameters(T)[1] == 1
    # After multiplication by 2*(1-beta)^2 the separate polynomial degrees
    # are at most (2,3,2) in (t,delta,beta). Three by four by three distinct
    # rational nodes therefore certify the identity, not sampled type IC.
    identity_checks = 0
    for t, delta, beta in product((F(67, 100), F(7, 10), F(3, 4)),
                                 (F(1, 100), F(1, 50), F(3, 100), F(1, 25)),
                                 (F(1, 5), F(2, 5), F(3, 5))):
        z = delta/(1-beta)
        new = (t+beta*c)*((1-t)*z+beta*z*z/2)
        preceding = t*(1-t)*delta+(t+c+delta)*((1-t)*(z-delta)+(z-delta)**2/2)
        closed = delta**2/2*((3*t-2)*beta/(1-beta)-delta*(beta/(1-beta))**2)
        assert new-preceding == closed
        identity_checks += 1
    boundary_checks = 0
    for t in (F(67, 100), F(7, 10), OLD_CUTOFF, F(4, 5)):
        delta, beta = menu_parameters(t)
        B, H = d+delta, c+delta
        Y = c+delta/(1-beta)
        k = t-q
        assert c <= H < Y <= B < 1
        assert t-beta*(Y-c) >= k
        for rho in (F(0), (b-t)/2, b-t):
            for y in (F(0), c, H, Y, d, B, F(1)):
                x_candidates = (F(0), k, t, F(1), t+c-y,
                                t-beta*(y-c), t-beta*(y-c)-F(1, 100000),
                                t-beta*(y-c)+F(1, 100000))
                for x in x_candidates:
                    if 0 <= x <= 1:
                        for profile in ((t, rho, x, y), (rho, t, y, x)):
                            mechanism(profile)
                            boundary_checks += 1
    for t in (A, T):
        for rho in (F(0), b-t):
            for x, y in ((F(0), F(0)), (F(1), F(1)), (t, c)):
                result = mechanism((t, rho, x, y))
                assert result['branch'] == 'retained_V4_02'
                boundary_checks += 1
    witness = (F(7, 10), F(1, 10), F(18, 25), F(29, 100))
    row = mechanism(witness)
    assert row['selected'] == 'lottery'
    assert 0 < row['allocations'][1][1] < 1
    baseline = old.candidate(witness)
    assert baseline['masks'] == (0, 1)
    symmetric_checks = 0
    # Both changed opponent fibers, same and opposite high coordinates,
    # including equal high coordinates and zero-utility choices.
    for t, tau in product((F(67, 100), F(7, 10), F(4, 5)), repeat=2):
        for rho, eta in product((F(0), b-t), (F(0), b-tau)):
            for profile in ((t, rho, tau, eta), (t, rho, eta, tau),
                            (rho, t, tau, eta), (rho, t, eta, tau)):
                mechanism(profile)
                symmetric_checks += 1
    # Reverse splice against bidder 2's inherited solved-Q override.
    for t in (F(67, 100), F(7, 10), F(4, 5)):
        delta, beta = menu_parameters(t)
        for y in (d+delta, d+delta+F(1, 10000), F(3, 5), A):
            for x in (F(0), b-y):
                for rho in (F(0), b-t):
                    for profile in ((x, y, t, rho), (y, x, rho, t)):
                        mechanism(profile)
                        symmetric_checks += 1
    data = dict(status='RESIDUAL_LOTTERY_EXACT_PASS',
                scope='complete pointwise feasible randomized DSIC/IR lower improvement; no full inner optimality claim',
                parameters=dict(a=str(old.A), b=str(b), c=str(c), d=str(d),
                                q=str(q), q_old=str(q_old),
                                region_low=str(A), region_high=str(T),
                                factor_second_root=str(U), old_cutoff=str(OLD_CUTOFF)),
                revenue=revenue_data(), identity_checks=identity_checks,
                pointwise_boundary_checks=boundary_checks,
                symmetric_boundary_checks=symmetric_checks,
                witness=dict(profile=list(map(str, witness)),
                             old_masks=list(baseline['masks']),
                             new_allocation=[[str(a) for a in v] for v in row['allocations']],
                             new_payment=str(row['payments'][1]),
                             new_utility=str(row['utilities'][1])),
                full_class_upper='unresolved outside inherited Q; no upper bound improvement claimed')
    path = ROOT/'certificate'/'residual_lottery.json'
    if '--write' in sys.argv:
        path.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    else:
        assert json.loads(path.read_text(encoding='utf-8')) == data
    print(data['status'])
    print('exact_total_gain', data['revenue']['gain'])
    print('pointwise_boundary_checks', boundary_checks)
    print('witness', data['witness'])
    return data


if __name__ == '__main__':
    verify()
