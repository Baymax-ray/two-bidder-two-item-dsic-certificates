"""V3.1 exact constrained-fiber improvement over the frozen V4 baseline.

The continuum proof and inner certificate are separate written theorems.
This evaluator uses exact quadratic comparisons for rational reports.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

if not __debug__:
    raise RuntimeError('Run without -O')
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / 'V4/verifier'))
import free_capacity_fibers as free
v3 = free.v3
P, T, I = v3.P, v3.T, v3.I


def require(test, message):
    if not test:
        raise RuntimeError(message)


def in_changed_region(w):
    t, rho = max(w), min(w)
    return v3.d < t and (t-v3.q)**2 < v3.r1 and 0 <= rho < v3.b-t


def in_solved_region(w):
    return min(w) >= 0 and max(w) <= F(2,3) and sum(w) <= v3.b


def mechanism(profile):
    profile = tuple(map(F, profile))
    original = free.mechanism(profile)
    w, z = profile[:2], profile[2:]
    if not in_solved_region(w):
        return original
    t = max(w)
    if t <= v3.d:
        require(original['masks'][0] == 0, 'closed full-capacity fiber')
        prices, priority = free.SJA_PRICES, (0,1,2,3)
        branch = 'closed_full_capacity_optimum'
    else:
        k = t - v3.q
        high_mask = 1 if w[0] > w[1] else 2
        low_mask = 3 - high_mask
        C = F(5,6) + F(3,4)*k*k
        prices = [v3.Quad()]*4
        prices[high_mask], prices[low_mask], prices[3] = map(v3.asquad, (F(2,3), C-k, C))
        priority = (0,low_mask,high_mask,3)
        branch = 'constrained_inner_optimum'
    utilities = [v3.base.value(z, mask)-prices[mask] for mask in range(4)]
    maximum = max(utilities)
    # Empty at zero utility; otherwise favor the safe low-coordinate item
    # at the binding high-value=k bundle/item2 tie.
    selected = next(mask for mask in priority if utilities[mask] == maximum)
    require(original['masks'][0] & selected == 0, 'pointwise capacity')
    changed = dict(original)
    changed['masks'] = (original['masks'][0], selected)
    changed['payments'] = (original['payments'][0], prices[selected])
    changed['utilities'] = (original['utilities'][0], maximum)
    changed['menus'] = (original['menus'][0], tuple(prices))
    changed['branches'] = (original['branches'][0], branch)
    return changed


def revenue_enclosure():
    k = T-v3.q
    C = P(F(5,6))+F(3,4)*k*k
    new = (P(F(2,3)), C-k, C)
    old = (P(v3.a), P(v3.b)-k, P(v3.b))
    integrand = 2*(v3.b-T)*(v3.revenue(*new)-v3.revenue(*old))
    k0, k1 = v3.sqrt_interval(v3.r0), v3.sqrt_interval(v3.r1)
    C1 = v3.c+F(2,3)
    Jdiff = (k1*(2*v3.r1+5*v3.K)*C1-k0*(2*v3.r0+5*v3.K)*v3.b)*F(1,8)
    Jdiff = Jdiff+F(3,8)*v3.K*v3.K*v3.log_interval((k1+C1)/(k0+v3.b))
    root_polynomial = (v3.h-T)*(-F(3,2)*v3.b*(T*T+v3.K)+F(1,2)*v3.b**3)
    old_root_gain = 4*(v3.h*Jdiff-F(C1**5-v3.b**5,5)
                      +v3.integrate_interval(root_polynomial,k0,k1))
    gain = v3.integrate_interval(integrand, v3.d, k1+v3.q)-old_root_gain/F(2)
    return gain, integrand


def certificate():
    require(v3.d < F(2,3) and v3.a < F(2,3), 'strict chamber order')
    # The conditional strict-gain decomposition is verified independently
    # in the inner dual replay; here verify its parameter signs globally.
    require(v3.c**2 < v3.r0 < v3.r1 < (v3.a-v3.q)**2, 'all branch intervals')
    require(v3.b > F(2,3) > v3.a and v3.r1 < F(4,9), 'positive gain factors')
    # Polynomial identity, not a type grid: separate degrees are at most
    # (3,2,4) in (A0,C0,k). Four by three by five distinct rational nodes
    # therefore certify the identity on all real arguments.
    def G(A,B,C):
        return A*(1-A)*(C-A)+B*(1-B)*(C-B)+C*((1-C+B)*(1-C+A)-(A+B-C)**2/2)
    identity_checks = 0
    for A0 in (F(1,2),F(11,20),F(3,5),F(16,25)):
        delta = F(2,3)-A0
        for C0 in (F(9,10),F(19,20),F(1)):
            for kk in (F(7,25),F(29,100),F(3,10),F(31,100),F(8,25)):
                optimal_C = F(5,6)+F(3,4)*kk*kk
                lhs = G(F(2,3),optimal_C-kk,optimal_C)-G(A0,C0-kk,C0)
                rhs = (C0-optimal_C)**2+F(3,2)*(C0-F(2,3))*delta**2+delta**3
                require(lhs == rhs, 'global strict-gain polynomial identity')
                identity_checks += 1
    witness = (F(51,100), F(1,100), F(3,10), F(3,5))
    old, new = free.mechanism(witness), mechanism(witness)
    require(old['masks'] == (0,0) and new['masks'] == (0,3), 'strict base-containment escape')
    require(v3.base.mechanism(witness)['base_masks'] == (0,0), 'shared base empty')
    k = witness[0]-v3.q
    tie = witness[:2]+(k,F(1))
    tied = mechanism(tie)
    require(tied['masks'] == (0,2), 'binding top-edge tie assigns safe item only')
    occupied = witness[:2]+(k-F(1,1000),F(1))
    require(mechanism(occupied)['masks'] == (1,2), 'actual nonfree capacity respected')
    examples = [witness, tie, occupied, (0,0,0,0), (v3.d,F(1,100),1,1),
                (F(1,100), F(51,100), F(3,5),F(3,10)),
                (F(3,5),F(1,100),F(2,3),F(1,5)), (1,1,1,1)]
    for profile in examples:
        before, after = free.mechanism(profile), mechanism(profile)
        require(after['masks'][0] == before['masks'][0], 'bidder1 unchanged')
        require(after['payments'][0] == before['payments'][0], 'bidder1 payment unchanged')
        if not in_solved_region(profile[:2]):
            require(after == before, 'complete outside continuation')
    gain, polynomial = revenue_enclosure()
    require(gain.lo > F(2153805511902915,10**20), 'strict exact integrated improvement')
    baseline = json.loads((ROOT.parent/'V4/certificate/combined_revenue.json').read_text(encoding='utf-8'))
    lower = I(*map(F,baseline['revenue_rational_interval']))
    total = lower+gain
    upper = I(F(3715139591287203,4194304000000000))
    solved_area = v3.d*v3.d-(2*v3.d-v3.b)**2/2 + 2*(v3.b*(F(2,3)-v3.d)-(F(4,9)-v3.d*v3.d)/2)
    require(solved_area == F(63871,180000), 'exact closed solved polygon area')
    kpoly = T-v3.q
    value_poly = P(F(59,108))+F(1,4)*kpoly*kpoly-kpoly*kpoly*kpoly+F(9,16)*kpoly*kpoly*kpoly*kpoly
    constrained_value = v3.integrate_interval(2*(v3.b-T)*value_poly,v3.d,F(2,3))
    require(constrained_value.lo == constrained_value.hi, 'rational constrained value')
    free_area = F(246769,1000000)
    local_value = (constrained_value.lo+free_area*F(4,9), free_area*F(2,27))
    require(local_value == (F(3270005919999123155413,19440000000000000000000),
                           F(246769,13500000)), 'exact fully optimized regional inner value')
    return {
        'scope': 'complete feasible mechanism; full randomized inner optimum on the certified opponent region only',
        'exact_gain': '2*integral_d^t1 (b-t)*(G(2/3,C(t)-k,C(t))-G(a,b-k,b))dt - G_root_V3/2',
        'exact_revenue': 'R_V3_1 = R_free_V4 + exact_gain; finite algebraic/logarithmic expression',
        'integrand_coefficients': list(map(str,polynomial.c)),
        'gain_rational_interval': v3.rounded_interval(gain,24),
        'revenue_rational_interval': v3.rounded_interval(total,24),
        'gap_rational_interval': v3.rounded_interval(upper-total,24),
        'solved_opponent_region_area': str(solved_area),
        'exact_bidder2_value_on_solved_region': free.encode_pair(local_value),
        'positive_measure_changed_region': 'd<t<t1, 0<=rho<b-t; either orientation',
        'solved_region': 'closed Q={max(w1,w2)<=2/3, w1+w2<=b}; all its fibers and boundaries optimized',
        'witness': list(map(str,witness)), 'old_masks': list(old['masks']), 'new_masks': list(new['masks']),
        'binding_tie_profile': list(map(str,tie)), 'binding_tie_masks': list(tied['masks']),
        'rational_report_smoke_checks': len(examples),
        'conditional_gain_identity': {'separate_degree_bounds': [3,2,4],
                                      'exact_interpolation_checks': identity_checks},
        'not_claimed': ['full inner optimum on every opponent report', 'outer bidder optimality',
                        'matching unrestricted two-bidder upper certificate'],
    }


if __name__ == '__main__':
    data = certificate()
    path = ROOT/'certificate/constrained_candidate.json'
    if '--write' in sys.argv:
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:
        require(json.loads(path.read_text(encoding='utf-8'))==data,'exact saved replay')
    print('CONSTRAINED_CANDIDATE_PASS')
    for key in ('gain_rational_interval','revenue_rational_interval','gap_rational_interval'):
        print(key,data[key])
