"""A complete joint deformation from the corner-price obstruction.

The exact all-real proof is research_log/price_joint_reallocation.md.
The exact positive lower increment is conservative; it is not the exact
revenue increment. Normal replay is read-only; --write saves its certificate.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'verifier'))
import outer_bundle_reoptimized as baseline

old = baseline.previous.strip.previous
c, q = old.c, old.q
EPS = F(9, 10000)
J0, J1, RHO = F(7, 10), F(71, 100), F(1, 5)


def bidder_two_cut(opponent):
    t, rho = opponent
    return J0 <= t <= J1 and 0 <= rho <= RHO


def bidder_one_fee(opponent):
    x, y = opponent
    return J0-4*EPS <= x <= J1 and c-2*EPS <= y <= c+4*EPS


def mechanism(profile):
    """One fixed physical orientation, with explicit boundary and tie rules."""
    profile = tuple(map(F, profile))
    row = dict(baseline.mechanism(profile))
    allocations = list(row['allocations'])
    payments, utilities = list(row['payments']), list(row['utilities'])
    fee, cut = bidder_one_fee(profile[2:]), bidder_two_cut(profile[:2])
    if fee and allocations[0] != (0, 0):
        if utilities[0] <= EPS:
            allocations[0], payments[0], utilities[0] = (F(), F()), F(), F()
        else:
            payments[0] += EPS
            utilities[0] -= EPS
    selected = None
    if cut:
        menu = old.menu(profile[:2])
        menu = [(a, p-EPS if name == 'lottery' else p, name)
                for a, p, name in menu]
        values = [sum((x*z for x, z in zip(profile[2:], a)), F())-p
                  for a, p, name in menu]
        best = max(values)
        index = next(j for j, value in enumerate(values) if value == best)
        allocations[1], payments[1], selected = menu[index]
        utilities[1] = best
    assert all(allocations[0][j]+allocations[1][j] <= 1 for j in (0, 1))
    assert all(u >= 0 for u in utilities)
    row.update(allocations=tuple(allocations), payments=tuple(payments),
               utilities=tuple(utilities), price_entry_fee=fee,
               price_lottery_cut=cut, price_selected=selected)
    return row


def exact_conditional_gain(t):
    delta, beta = old.menu_parameters(t)
    alpha, length = 3*t-2, delta+(3*t-2)/2
    return (EPS*alpha*length/4-EPS**2*alpha/(4*beta*(1-beta))
            -EPS**3/(2*beta*(1-beta)**2))


def calculate():
    lo_delta, lo_beta = old.menu_parameters(J0)
    hi_delta, hi_beta = old.menu_parameters(J1)
    alpha0, alpha1 = 3*J0-2, 3*J1-2
    length0, length1 = lo_delta+alpha0/2, hi_delta+alpha1/2
    assert F(3, 5) < lo_beta < hi_beta < F(3, 4)
    assert lo_delta < alpha0/3 and alpha1 < 6*hi_delta
    assert F(9, 8)*J1-F(3, 4)-F(3, 2)*q < 0  # delta decreases
    assert F(9, 8)*J0+F(3, 4)-F(3, 2)*q > 0  # L increases
    assert c-2*EPS > 0 and c+length1+4*EPS < F(1, 2)
    assert c+length1+4*EPS < F(1, 2)+hi_delta
    assert 1-J1/2-4*EPS > F(1, 2)  # cut never meets reverse free splice
    assert J1+RHO <= old.b and RHO < c
    hmin = alpha0*length0/4
    assert hmin == F(1213, 625000)
    warea = (J1-J0)*RHO
    sarea = 6*EPS*(J1-J0+4*EPS)
    # Exact payment-cut identity gives uniform coefficients using
    # beta >= 3/5, 1-beta >= 1/4, and alpha <= 13/100.
    lower_second = warea*(EPS*hmin-F(13,60)*EPS**2-F(40,3)*EPS**3)
    # Entry-fee identity: Delta R=(1-3 area D0)e-3Ce^2/2-e^3/2.
    # Below c, all rows are Eplus with lambda<1/25 and C<101/100.
    assert alpha1*(c+length1/4) < F(1,25)
    assert J1+c+hi_delta < F(101,100)
    assert J0-4*EPS > F(2,3)
    # Above c, literal B13.1, B14.1, and zero-fee cells have lambda<=0.
    # lambda increases in x and along each affine upper x(z) boundary.
    lam_bounds = []
    for x, fee in ((F(39,40)-c-4*EPS,F(7,2000)),
                   (F(49,50)-c-4*EPS,F(7,10000)), (J1,F())):
        z = 4*EPS
        ap,bp,cp = x+z+fee,F(1,2)+z+fee,x+c+z+fee
        lam = 3*(ap*bp-(ap+bp-cp)**2/2)-1
        assert lam < 0 and cp < 1
        lam_bounds.append(lam)
    upper_fee_loss = (J1-J0+4*EPS)*(F(2,25)*EPS**2+F(903,100)*EPS**3+3*EPS**4)
    lower_total = lower_second-upper_fee_loss
    assert lower_total == F(26902077489,12500000000000000000) > 0
    # Named corners include all new/opponent entry ties. They supplement,
    # rather than replace, the all-real argument in the proof.
    count = 0
    for t, rho in product((J0, (J0+J1)/2, J1), (F(), RHO)):
        delta, beta = old.menu_parameters(t)
        yy = (c-2*EPS, c-EPS/beta, c, c+4*EPS,
              c+delta/(1-beta)+EPS/(1-beta), F(1))
        for y in yy:
            xx = (J0-4*EPS, J1, t-EPS, t, t+EPS,
                  t-beta*(y-c)-EPS, t-beta*(y-c), F(1))
            for x in xx:
                if 0 <= x <= 1 and 0 <= y <= 1:
                    mechanism((t, rho, x, y))
                    count += 1
        assert exact_conditional_gain(t) >= EPS*hmin-F(13,60)*EPS**2-F(40,3)*EPS**3
    # Reports outside the cut still use a complete entry-fee menu.
    for t, rho in ((F(), F()), (F(1), F(1)), (F(3, 5), F(1, 2))):
        for x, y in product((J0-4*EPS, J0, J1), (c-2*EPS, c, c+4*EPS)):
            mechanism((t, rho, x, y))
            count += 1
    witness = (J0, F(1, 10), J0-EPS/2, c)
    before, after = baseline.mechanism(witness), mechanism(witness)
    assert before['allocations'] == ((1, 0), (0, 0))
    assert after['allocations'][0] == (0, 0)
    assert after['allocations'][1] == (1, lo_beta)
    assert after['price_selected'] == 'lottery'
    # The companion price_joint_revenue.py evaluates the fully specified
    # payment integral exactly. This replay supplies an independent strict
    # rational lower increment.
    return dict(status='PRICE_JOINT_REALLOCATION_EXACT_PASS',
                scope='complete pointwise feasible DSIC/IR joint improvement; conservative exact gain bound',
                epsilon=str(EPS), cut_rectangle=list(map(str,(J0,J1,F(),RHO))),
                fee_rectangle=list(map(str,(J0-4*EPS,J1,c-2*EPS,c+4*EPS))),
                conditional_derivative_minimum=str(hmin),
                second_bidder_gain_lower=str(lower_second),
                first_bidder_loss_upper=str(upper_fee_loss),
                above_strip_lambda_maxima=list(map(str,lam_bounds)),
                total_gain_lower=str(lower_total), boundary_replays=count,
                witness=dict(profile=list(map(str,witness)),
                             old_allocations=[[str(x) for x in a] for a in before['allocations']],
                             new_allocations=[[str(x) for x in a] for a in after['allocations']],
                             new_payment=str(after['payments'][1])),
                exact_revenue_increment='exact rational-plus-log increment in price_joint_revenue.json',
                upper_certificate='reference predecessor is strictly suboptimal; final trial unrestricted optimality unresolved')


if __name__ == '__main__':
    data = calculate()
    path = ROOT/'certificate'/'price_joint_reallocation.json'
    if '--write' in sys.argv:
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads(path.read_text(encoding='utf-8')) == data
    print(data['status'])
    print('strict_joint_gain_lower', data['total_gain_lower'])
    print('boundary_replays', data['boundary_replays'])
