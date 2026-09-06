"""Independent rational polygon integration for the V4.5 lottery candidate.

No discovery or candidate modules are imported. Whole continuous winning cells
are clipped and integrated; the finite parameter checks are algebra checks,
not a proof of pointwise feasibility or unrestricted optimality.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O')
ROOT = Path(__file__).resolve().parents[1]
c, q, qo, b = F(137,500), F(113,500), F(227,1000), F(91,100)
T, U = F(613,750), F(839,750)
old_cut = (F(1,2)-c+F(3,4)*qo*qo)/(F(3,2)*qo)


def clip(poly, aa, bb, cc):
    """Closed halfplane aa*x+bb*y+cc >= 0."""
    result = []
    for start, end in zip(poly, poly[1:]+poly[:1]):
        fs, fe = aa*start[0]+bb*start[1]+cc, aa*end[0]+bb*end[1]+cc
        if fs >= 0:
            result.append(start)
        if (fs < 0 < fe) or (fe < 0 < fs):
            ratio = fs/(fs-fe)
            result.append(tuple(start[j]+ratio*(end[j]-start[j]) for j in (0,1)))
    return result


def area(poly):
    return abs(sum((x*y2-y*x2 for (x,y),(x2,y2) in
                    zip(poly,poly[1:]+poly[:1])),F()))/2


def polygon_revenue(menu):
    answer, masses = F(), []
    for i, (ax,ay,p) in enumerate(menu):
        poly = [(F(),F()),(F(1),F()),(F(1),F(1)),(F(),F(1))]
        for j,(bx,by,z) in enumerate(menu):
            if i != j:
                poly = clip(poly,ax-bx,ay-by,z-p)
        mass = area(poly)
        answer += p*mass
        masses.append(mass)
    assert sum(masses) == 1
    return answer, masses


def menu(t,delta,beta=None):
    result = [(F(),F(),F()),(F(1),F(),t),
              (F(),F(1),F(1,2)+delta),(F(1),F(1),t+c+delta)]
    if beta is not None:
        result.append((F(1),beta,t+beta*c))
    return result


# Dictionary polynomials; no inherited polynomial package.
def add(*items):
    ans = {}
    for item in items:
        for j,v in item.items():
            ans[j] = ans.get(j,F())+v
    return {j:v for j,v in ans.items() if v}


def scale(poly,value):
    return {j:v*value for j,v in poly.items() if v*value}


def mul(p,r):
    ans = {}
    for i,a in p.items():
        for j,v in r.items():
            ans[i+j] = ans.get(i+j,F())+a*v
    return {j:v for j,v in ans.items() if v}


def value(poly,x):
    return sum((v*x**j for j,v in poly.items()),F())


def integral(poly,lo,hi):
    return sum((v*(hi**(j+1)-lo**(j+1))/(j+1) for j,v in poly.items()),F())


def reconstruct():
    delta_star = scale(mul({0:T,1:F(-1)},{0:U,1:F(-1)}),F(9,16))
    delta_old = {0:F(1,2)-c+F(3,4)*qo*qo,1:-F(3,2)*qo}
    aa = scale(mul({0:F(-2),1:F(3)},{0:F(-2),1:F(3)}),F(1,8))
    difference = add(delta_star,scale(delta_old,-1))
    gain_left = add(mul(difference,difference),mul(delta_old,aa))
    gain_right = mul(delta_star,delta_star)
    weight = {0:2*b,1:F(-2)}
    total = integral(mul(weight,gain_left),F(2,3),old_cut)
    total += integral(mul(weight,gain_right),old_cut,T)
    assert total > 0
    checks = []
    samples = [F(7,10),F(3,4),old_cut,F(4,5),(old_cut+T)/2]
    for t in samples:
        ds = value(delta_star,t)
        do = max(F(),value(delta_old,t))
        beta = (3*t-2)/(3*t-2+2*ds)
        z = beta/(1-beta)
        assert F(2,3)<t<T and 0<beta<1 and 0<ds
        assert z*ds < q
        # The winning lottery strip stays below the actual residual kink y=d.
        assert c+ds/(1-beta)<F(1,2)
        prior, _ = polygon_revenue(menu(t,do))
        raised, _ = polygon_revenue(menu(t,ds))
        final, masses = polygon_revenue(menu(t,ds,beta))
        fixed_gain = ds*ds*((3*t-2)*z-ds*z*z)/2
        assert final-raised == fixed_gain
        expected = value(gain_left if t<=old_cut else gain_right,t)
        assert final-prior == expected
        checks.append({'t':str(t),'delta':str(ds),'beta':str(beta),
                       'lottery_cell_area':str(masses[-1]),
                       'conditional_gain':str(final-prior)})
    # A bounded-degree identity is checked using exact continuous cells at
    # independent rational t nodes; there is no finite type LP here.
    for j in range(1,10):
        t = F(2,3)+(old_cut-F(2,3))*F(j,10)
        ds = value(delta_star,t)
        do = value(delta_old,t)
        beta = (3*t-2)/(3*t-2+2*ds)
        assert polygon_revenue(menu(t,ds,beta))[0]-polygon_revenue(menu(t,do))[0] == value(gain_left,t)
    data = json.loads((ROOT.parent/'V4_02/certificate/split_cost_revenue.json').read_text(encoding='utf-8'))
    lo,hi = map(F,data['revenue_rational_interval'])
    return {'scope':'independent exact continuous-cell revenue audit; no full inner or auction optimality claim',
            'method':'rational halfplane clipping, shoelace areas, dictionary-polynomial integration',
            'band_end':str(T),'factorization_other_root':str(U),'old_cutoff':str(old_cut),
            'gain_polynomial_before_old_cutoff':{str(k):str(v) for k,v in sorted(gain_left.items())},
            'gain_polynomial_after_old_cutoff':{str(k):str(v) for k,v in sorted(gain_right.items())},
            'one_sided_exact_gain':str(total),
            'exact_gain':str(2*total),'revenue_interval':[str(lo+2*total),str(hi+2*total)],
            'gain_multiplier_scope':'both conditional menu changes; simultaneous feasibility proved separately',
            'polygon_cases':checks,'additional_rational_parameter_checks':9,
            'baseline_interval_dependency':'V4_02/certificate/split_cost_revenue.json'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args = parser.parse_args()
    result = reconstruct()
    path = ROOT/'certificate/independent_lottery.json'
    if args.write:
        path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    else:
        assert result == json.loads(path.read_text(encoding='utf-8'))
    print('INDEPENDENT_LOTTERY_EXACT_PASS')
    print('exact_gain',result['exact_gain'])
    print('gain_decimal_for_display',float(F(result['exact_gain'])))
    print('revenue_decimal_for_display',float(F(result['revenue_interval'][0])))


if __name__=='__main__':
    main()
