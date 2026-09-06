"""Exact extension of V4.5 lotteries to the actual free-low-item strip.

Normal execution checks the stored certificate without writes. --write creates
the certificate. The pointwise continuum proof is outer_lottery_strip.md.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent/'V4_5'/'verifier'))
import residual_lottery as previous
import independent_lottery as independent

a, b, c, d, A, T = F(159,250), F(91,100), F(137,500), F(1,2), F(2,3), F(613,750)


def in_extended_region(opponent):
    """The rho=c face is explicitly retained, because old bundle ties exist."""
    t, rho = max(opponent), min(opponent)
    return A < t < T and rho < c


def in_added_region(opponent):
    t, rho = max(opponent), min(opponent)
    return A < t < T and b-t < rho < c


def mechanism(profile):
    """A complete two-sided extension; all unmentioned reports use V4.5."""
    profile = tuple(map(F, profile))
    assert len(profile) == 4 and all(0 <= x <= 1 for x in profile)
    before = previous.mechanism(profile)
    allocations = list(before['allocations'])
    payments, utilities = list(before['payments']), list(before['utilities'])
    selected = [None, None]
    for i in (0, 1):
        own, opponent = profile[2*i:2*i+2], profile[2*(1-i):2*(1-i)+2]
        if not in_added_region(opponent):
            continue
        rows = previous.menu(opponent)
        values = [sum((x*z for x,z in zip(own,row[0])), F())-row[1] for row in rows]
        best = max(values)
        chosen = next(j for j,value in enumerate(values) if value == best)
        allocations[i], payments[i], selected[i] = rows[chosen]
        utilities[i] = best
        assert payments[i] >= 0 and best >= 0
    assert all(allocations[0][j]+allocations[1][j] <= 1 for j in (0,1))
    return dict(profile=profile, allocations=tuple(allocations),
                payments=tuple(payments), utilities=tuple(utilities),
                outer_selected=tuple(selected))


def exact_gain():
    x = previous.X
    g1 = (previous.DELTA-previous.DELTA_OLD)**2 + F(1,8)*previous.DELTA_OLD*(3*x-2)**2
    g2 = previous.DELTA**2
    p1, p2 = 4*(x-a)*g1, 4*(x-a)*g2
    cutoff = previous.OLD_CUTOFF
    gain1, gain2 = p1.integral(A,cutoff), p2.integral(cutoff,T)
    assert gain1 > 0 and gain2 > 0
    # Independently assembled dictionary polynomials, with no P integration.
    ds = independent.scale(independent.mul({0:T,1:F(-1)},
                                          {0:previous.U,1:F(-1)}), F(9,16))
    do = {0:F(1,2)-c+F(3,4)*previous.q_old**2, 1:-F(3,2)*previous.q_old}
    dif = independent.add(ds, independent.scale(do,-1))
    squared = independent.mul({0:F(-2),1:F(3)}, {0:F(-2),1:F(3)})
    gg1 = independent.add(independent.mul(dif,dif),
                          independent.scale(independent.mul(do,squared), F(1,8)))
    gg2 = independent.mul(ds,ds)
    weight = {0:-4*a,1:F(4)}
    replay = independent.integral(independent.mul(weight,gg1), A, cutoff)
    replay += independent.integral(independent.mul(weight,gg2), cutoff,T)
    assert replay == gain1+gain2
    before = independent.reconstruct()
    lo, hi = map(F, before['revenue_interval'])
    return dict(exact_gain=str(replay), gain_before_old_cutoff=str(gain1),
                gain_after_old_cutoff=str(gain2),
                integrand_before=[str(z) for z in p1.c],
                integrand_after=[str(z) for z in p2.c],
                added_opponent_area=str((T-a)**2-(A-a)**2),
                extended_opponent_area=str(2*c*(T-A)),
                revenue_interval=[str(lo+replay),str(hi+replay)],
                multiplier_scope='both bidders and both item orientations; added rho width t-a',
                independent_replay='dictionary polynomial integration agrees exactly')


def verify():
    assert d > c and A > a and T < b and T-A > 0
    checks = 0
    eps = F(1,100000)
    for t in (F(7,10), F(3,4), F(4,5)):
        delta,beta = previous.menu_parameters(t)
        cutoff_y = c+delta/(1-beta)
        for rho in (b-t, (b-t+c)/2, c-eps, c):
            for y in (F(0), c, c+delta, cutoff_y, d+delta, F(1)):
                x_nodes = (F(0),t-previous.q,t,F(1),
                           t-beta*(y-c),t-beta*(y-c)-eps,
                           t-beta*(y-c)+eps)
                for x in x_nodes:
                    if not 0 <= x <= 1:
                        continue
                    for profile in ((t,rho,x,y),(rho,t,y,x)):
                        row = mechanism(profile)
                        if rho == c:
                            assert row['outer_selected'][1] is None
                        checks += 1
    simultaneous = 0
    for t,tau in product((F(7,10),F(3,4),F(4,5)),repeat=2):
        for rho,eta in product(((b-t+c)/2,c-eps), ((b-tau+c)/2,c-eps)):
            for p in ((t,rho,tau,eta),(t,rho,eta,tau),
                      (rho,t,tau,eta),(rho,t,eta,tau)):
                mechanism(p)
                simultaneous += 1
    reverse_q = 0
    for t in (F(7,10),F(3,4),F(4,5)):
        delta,beta = previous.menu_parameters(t)
        for rho in ((b-t+c)/2,c-eps):
            for y in (d+delta,d+delta+eps,F(3,5),A):
                for x in (F(0),b-y):
                    for p in ((x,y,t,rho),(y,x,rho,t)):
                        mechanism(p)
                        reverse_q += 1
    for t in (A,T):
        for rho in ((b-t+c)/2,c):
            row = mechanism((t,rho,F(3,4),F(3,10)))
            assert row['outer_selected'][1] is None
            checks += 1
    # Exact occupied traces used by the separate full-inner certificate.
    # Opposing reports on these traces never enter Eplus or the root free
    # splice. The all-real price identities are proved in the research note.
    occupied_traces = 0
    for t in (F(7,10),F(3,4),F(4,5)):
        for rho in (F(0),(b-t+c)/2,c-eps):
            k = t-previous.q
            for x in ((A+t)/2,(3*A+t)/4,(A+3*t)/4):
                for profile,i in (((t,rho,x,c),0),((x,c,t,rho),1)):
                    assert mechanism(profile)['allocations'][i][0] == 1
                    occupied_traces += 1
            for x in (F(0),c/2,c,(c+k)/2,k-eps):
                for profile,i in (((t,rho,x,F(1)),0),((x,F(1),t,rho),1)):
                    assert mechanism(profile)['allocations'][i][0] == 1
                    occupied_traces += 1
    witness = (F(7,10),F(1,4),F(18,25),F(29,100))
    before, after = previous.mechanism(witness), mechanism(witness)
    assert before['allocations'][1] == (1,0)
    assert after['outer_selected'][1] == 'lottery'
    assert 0 < after['allocations'][1][1] < 1
    data = dict(status='OUTER_LOTTERY_STRIP_EXACT_PASS',
                scope='complete DSIC/IR feasible lower improvement; full inner optimum certified separately in inner_lottery_certificate',
                constants=dict(a=str(a),b=str(b),c=str(c),d=str(d),A=str(A),T=str(T)),
                revenue=exact_gain(), boundary_checks=checks,
                simultaneous_splice_checks=simultaneous, reverse_Q_checks=reverse_q,
                occupied_capacity_trace_checks=occupied_traces,
                witness=dict(profile=list(map(str,witness)),
                             old_allocation=[[str(z) for z in v] for v in before['allocations']],
                             new_allocation=[[str(z) for z in v] for v in after['allocations']],
                             new_payment=str(after['payments'][1])),
                closed_face_policy='retain V4.5 on rho=c and t in {2/3,T}',
                continuum_proof='research_log/outer_lottery_strip.md')
    path = ROOT/'certificate'/'outer_lottery_strip.json'
    if '--write' in sys.argv:
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads(path.read_text(encoding='utf-8')) == data
    print(data['status'])
    print('exact_gain',data['revenue']['exact_gain'])
    print('gain_decimal_for_display',float(F(data['revenue']['exact_gain'])))
    print('checks',checks+simultaneous+reverse_q+occupied_traces)
    return data


if __name__ == '__main__':
    verify()
