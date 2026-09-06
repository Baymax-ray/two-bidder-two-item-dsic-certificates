"""Exact identities and architecture obstructions for V4.5 capacity supports.

The measure/envelope proof is in research_log/dual_capacity_support.md.
This replay checks its rational constants, continuous-cell inequalities,
polynomial integrals, and actual frozen-menu boundary representatives.
It does not certify common dual optimality or a new auction upper bound.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / 'V4_02' / 'verifier'))
import split_cost_candidate as old
sys.path.insert(0, str(ROOT / 'verifier'))
import residual_lottery as new

A = F(2, 3)
a, b, s = F(159, 250), F(91, 100), F(142, 125)
c, d, q = b-a, s-a, s-b
K = A-q
L = b-q
Z = F(5, 6)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(p, r):
    return tuple((p[j] if j < len(p) else F()) +
                 (r[j] if j < len(r) else F())
                 for j in range(max(len(p), len(r))))


def mul(p, r):
    out = [F()] * (len(p)+len(r)-1)
    for j, x in enumerate(p):
        for k, y in enumerate(r):
            out[j+k] += x*y
    return tuple(out)


def value(p, x):
    ans = F()
    for coefficient in reversed(p):
        ans = ans*x+coefficient
    return ans


def integral(p, lo, hi):
    return sum((coefficient*(hi**(j+1)-lo**(j+1))/F(j+1)
                for j, coefficient in enumerate(p)), F())


def menu(k):
    C = F(5, 6)+F(3, 4)*k*k
    return C-k, C


def ell(k, x):
    B, C = menu(k)
    return B if x <= k else C-x


def f(k, x):
    return 3*ell(k, x)-2 if x <= A else F(1)


def tail(k, x):
    B, C = menu(k)
    if x <= k:
        return (2-3*B)*x
    if x <= A:
        return 1-A+(3*C-2)*(A-x)-F(3, 2)*(A*A-x*x)
    return 1-x


def density(k, x, y, z=Z):
    H = max(F(), (y-z)/(1-z))
    pi1 = 3*max(F(), x-A)
    if y >= z:
        pi1 += tail(k, x)/(1-z)
    pi2 = (3*max(F(), y-ell(k, x)) if x <= A else F())+f(k, x)*H
    return pi1, pi2


def calculate():
    require(old.CANDIDATE_SPLIT == s, 'actual split-cost baseline')
    require(c == F(137, 500) and d == F(1, 2) and q == F(113, 500),
            'actual residual constants')
    cutoff = old.v3.cutoff
    require(cutoff == F(1058587, 1362000) < Z, 'joined tariff has returned to base')
    require(Z+c > 1 and Z > A and s-Z < a, 'whole-band base chamber')
    require(c < K < A and menu(c)[0] < A, 'parameter chamber and maximal ell bound')
    require(F(3, 2)*K-1 < 0, 'B(k) decreases throughout interval')

    # Exact symbolic coefficients: a(k)=2-3B(k), with B=5/6+3k^2/4-k.
    ak = (-F(1, 2), F(3), -F(9, 4))
    require(value(ak, c) > 0 and 3-F(9, 2)*K > 0,
            'a(k) positive and increasing on the whole parameter interval')
    mass_poly = mul(mul((L, -F(1)), (F(), F(), F(1))), ak)
    mass = integral(mass_poly, c, K)
    # Independent displayed antiderivative, not the polynomial integrator.
    def primitive(k):
        return -L*k**3/6+(3*L/4+F(1, 8))*k**4-(9*L/20+F(3, 5))*k**5+F(3, 8)*k**6
    require(mass == primitive(K)-primitive(c) == F(11884909837073, 6075000000000000),
            'exact total consumed charge on the old opponent-null faces')
    h = integral(mul((L, -F(1)), ak), c, K)
    require(h == F(39635863, 2700000000), 'conditional band charge coefficient')

    # This rational box is entirely in the actual scarce-item top hole.
    def primitive_a(k):
        return -k/2+F(3, 2)*k*k-F(3, 4)*k*k*k
    witness_mass = F(1, 10)*F(3, 200)*(primitive_a(F(14, 25)-q)-primitive_a(F(11, 20)-q))
    require(witness_mass == F(730317, 200000000000) > 0, 'strict singular-face witness')

    # Nonnegativity is analytic: above z, the left density is the convex
    # combination (1-H)*3(y-ell)+H*(3y-2); below z it is the old density.
    # The following checks explicitly cover all affine junctions at rational k.
    cell_checks = 0
    for k in (c, (c+K)/2, K):
        B, C = menu(k)
        require(A*C-A*A/2-k*k/2 == F(1, 3), 'equal-area identity')
        require(tail(k, 0) == tail(k, 1) == 0, 'tail endpoints')
        require(tail(k, k) == 1-A+(3*C-2)*(A-k)-F(3, 2)*(A*A-k*k),
                'tail continuity at k')
        for x in (F(), k/2, k, (k+A)/2, A, (A+1)/2, F(1)):
            ys = (F(), B, Z, (1+Z)/2, F(1))
            for y in ys:
                p1, p2 = density(k, x, y)
                require(p1 >= 0 and p2 >= 0, 'band price nonnegativity representative')
                if x <= A and y >= Z:
                    H = (y-Z)/(1-Z)
                    require(p2 == (1-H)*3*(y-ell(k, x))+H*(3*y-2),
                            'exact nonnegative convex combination')
                cell_checks += 1

    boundary_checks = 0
    for t in (d+F(1, 1000), F(11, 20), a, A):
        k = t-q
        for rho in (F(), (b-t)/2, b-t):
            for x in (F(), c, (c+k)/2, k, (k+A)/2, F(1)):
                for y in (Z, F(9, 10), F(1)):
                    require(all(extra == 0 for extra in old.increments((x, y))),
                            'actual frozen increment vanishes in band')
                    row = old.candidate((t, rho, x, y))
                    require(row['masks'][0] == (1 if x < k else 0),
                            'actual complete residual and zero-utility tie')
                    boundary_checks += 1

    # Thin-band rejection: empty bidder 1's menu on this opponent rectangle.
    epsilon = F(1, 1000)
    xlo, xhi = F(1, 5), F(1, 4)
    charge = h*(xhi*xhi-xlo*xlo)/2
    lost_revenue_upper = 2*(xhi-xlo)*epsilon
    rejection_gap = charge-lost_revenue_upper
    require(xlo*h/epsilon > 2 and rejection_gap > 0, 'thin-band strict Lagrangian improvement')

    # The reverse lottery splice preserves tightness of all three Q supports.
    require(A < new.T < Z, 'new opponent splice does not reach the price band')
    diff = new.DELTA-new.DELTA_OLD
    require(diff(A) == F(2641, 4000000) > 0 and diff.c[2] > 0 and
            diff.c[1]+2*diff.c[2]*A > 0, 'new safe-item threshold exceeds old threshold throughout E')
    reverse_splice_checks = 0
    for t in (F(7, 10), F(3, 4), F(4, 5)):
        before_delta = max(F(), new.DELTA_OLD(t))
        after_delta = new.DELTA(t)
        w_safe = d+(before_delta+after_delta)/2
        for rho in (F(), b-t):
            require(rho < c <= w_safe-q, 'freed capacity misses the moving junction')
            for profile in ((F(), w_safe, t, rho), (w_safe, F(), rho, t)):
                old_row, new_row = old.candidate(profile), new.mechanism(profile)
                require(old_row['masks'][0] != 0 and new_row['allocations'][0] == (F(), F()),
                        'reverse splice frees the Q scarce item')
                require(density(w_safe-q, rho, t)[0] == 0,
                        'repaired Q scarce density vanishes at the freed reports')
                reverse_splice_checks += 1

    # Additional exact band-transfer identity for a nontrivial convex utility
    # u=x^2+y^2+xy. This is a regression, not the universal envelope proof.
    for k in (c, (c+K)/2, K):
        B, C = menu(k)
        fp = (2-3*B,)
        left_moment = fp[0]*k*k/2
        middle_poly = (1-A+(3*C-2)*A-F(3, 2)*A*A, -(3*C-2), F(3, 2))
        intF = left_moment+integral(middle_poly, k, A)+integral((1, -1), A, 1)
        intxf = integral((F(), 3*B-2), 0, k)+integral((F(), 3*C-2, -3), k, A)+integral((F(), F(1)), A, 1)
        require(intF == intxf, 'integration by parts in the band transfer')
        require(left_moment == tail(k, k)*k+integral((F(), 3*B-2), 0, k),
                'targeted transfer requires the positive junction measure')

    input_path = ROOT.parent / 'V4_02' / 'verifier' / 'split_cost_candidate.py'
    return {
        'scope': 'Exact conditional capacity supports and quantified rejection of two common-support architectures; no matching auction upper certificate.',
        'baseline_split_cost': str(s),
        'baseline_evaluator_sha256': hashlib.sha256(input_path.read_bytes()).hexdigest(),
        'broad_band_lower_edge': str(Z),
        'frozen_joined_base_cutoff': str(cutoff),
        'parameter_k_interval': [str(c), str(K)],
        'singular_support_common_Lagrangian_gap_lower_bound': str(mass),
        'singular_witness_box_mass': str(witness_mass),
        'conditional_band_charge_coefficient_H': str(h),
        'thin_band_width': str(epsilon),
        'thin_band_opponent_x_interval': [str(xlo), str(xhi)],
        'thin_band_consumed_charge': str(charge),
        'thin_band_lost_revenue_upper': str(lost_revenue_upper),
        'thin_band_common_Lagrangian_gap_lower_bound': str(rejection_gap),
        'rational_density_junction_regressions': cell_checks,
        'actual_menu_boundary_regressions': boundary_checks,
        'reverse_lottery_splice_Q_support_regressions': reverse_splice_checks,
        'targeted_support_junction_measure': 'F(k) H(y) delta_{x=k}(dx) dy, H(y)=6(y-5/6)_+',
        'lottery_complementarity': 'Every tight nonnegative capacity measure must assign zero item-2 measure to the genuine lottery region when capacity=1 and allocation beta is strictly between 0 and 1.',
    }


if __name__ == '__main__':
    data = calculate()
    target = ROOT / 'certificate' / 'dual_support.json'
    if '--write' in sys.argv:
        target.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    else:
        require(json.loads(target.read_text(encoding='utf-8')) == data, 'exact certificate replay')
    print('V4_5_DUAL_CAPACITY_SUPPORT_EXACT_PASS')
    print('old singular support common gap >=', data['singular_support_common_Lagrangian_gap_lower_bound'])
    print('thin-band support common gap >=', data['thin_band_common_Lagrangian_gap_lower_bound'])
    print('scope:', data['scope'])
