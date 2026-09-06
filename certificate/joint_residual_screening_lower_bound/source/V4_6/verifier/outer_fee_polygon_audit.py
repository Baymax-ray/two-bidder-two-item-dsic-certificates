"""Independent continuous-cell audit of the selected corner fee/cut formulas.

This is an exact algebra and source-menu audit, not a type-grid optimality
argument. It imports no polynomial coefficient from price_joint_revenue.py.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verifier'))
import outer_bundle_reoptimized as baseline

older = baseline.previous.strip.previous
p = baseline.previous.p
e,c = F(9,10000),F(137,500)
x0,x1 = F(7,10)-4*e,F(71,100)


def rational(value):
    if isinstance(value,baseline.v3.Quad):
        assert value.s == 0
        return value.r
    return F(value)


def actual_menu(opponent):
    """Reconstruct the entire actual bidder-1 menu from its active branch."""
    if baseline.previous.strip.in_extended_region(opponent):
        rows = older.menu(opponent)
        return [(F(a[0]),F(a[1]),rational(price)) for a,price,label in rows], 'Eplus'
    prices = older.old.retained_menu(opponent,older.old.CANDIDATE_THETA)
    rows = [(F(bool(mask&1)),F(bool(mask&2)),rational(price))
            for mask,price in enumerate(prices)]
    _,fee_id = older.old.base.fee_rows(opponent)
    return rows, 'retained_y_equals_c' if opponent[1] == c else (fee_id or 'zero_fee')


def cells(menu):
    answer = []
    for i,(ax,ay,price) in enumerate(menu):
        poly = [(F(),F()),(F(1),F()),(F(1),F(1)),(F(),F(1))]
        for j,(bx,by,cost) in enumerate(menu):
            if i != j:
                poly = p.clip(poly,ax-bx,ay-by,cost-price)
        answer.append(poly)
    return answer


def verify():
    opponent_cases = []
    # The open below-c region uses genuine lotteries. The y=c line uses the
    # explicitly retained four-option menu and is audited separately.
    for x in (x0,F(7,10),F(141,200),x1):
        for y in (c-2*e,c-e,c):
            opponent_cases.append((x,y))
    # Interior and exact first-match boundaries of each literal tariff row.
    for z in (e,2*e,4*e):
        left1,right1 = x0,F(39,40)-c-z
        right2 = F(49,50)-c-z
        for x in (left1,(left1+right1)/2,right1,
                  (right1+right2)/2,right2,(right2+x1)/2,x1):
            opponent_cases.append((x,c+z))
    menu_checks = 0
    details = []
    for opponent in opponent_cases:
        assert x0 <= opponent[0] <= x1 and c-2*e <= opponent[1] <= c+4*e
        menu,branch = actual_menu(opponent)
        before,masses = p.polygon_revenue(menu)
        raised = [(ax,ay,price+e if ax or ay else price) for ax,ay,price in menu]
        after,new_masses = p.polygon_revenue(raised)
        C = next(price for ax,ay,price in menu if ax == ay == 1)
        d0 = masses[0]
        formula = e*(1-3*d0)-F(3,2)*C*e*e-e**3/2
        assert after-before == formula
        assert new_masses[0] == d0+C*e+e*e/2
        if branch in ('B13.1','B14.1','zero_fee'):
            ap = next(price for ax,ay,price in menu if ax == 1 and ay == 0)
            bp = next(price for ax,ay,price in menu if ax == 0 and ay == 1)
            assert d0 == ap*bp-(ap+bp-C)**2/2
            z = opponent[1]-c
            fee = {'B13.1':F(7,2000),'B14.1':F(7,10000),'zero_fee':F()}[branch]
            assert (ap,bp,C) == (opponent[0]+z+fee,F(1,2)+z+fee,opponent[0]+c+z+fee)
        # Check actual full-mechanism choices at strict interior points of
        # every nonempty winning cell, rather than merely trusting prices.
        for option,poly in zip(menu,cells(menu)):
            if not poly or p.area(poly) == 0:
                continue
            own = tuple(sum((v[j] for v in poly),F())/len(poly) for j in (0,1))
            row = baseline.mechanism(own+opponent)
            assert row['allocations'][0] == option[:2]
            assert row['payments'][0] == option[2]
            menu_checks += 1
        details.append(dict(opponent=list(map(str,opponent)),branch=branch,
                            old_no_sale_area=str(d0),bundle_price=str(C),
                            exact_fee_revenue_change=str(after-before)))
    cut_checks = []
    for t in (F(7,10),F(281,400),F(141,200),F(283,400),F(71,100)):
        delta,beta = older.menu_parameters(t)
        alpha,L = 3*t-2,delta+(3*t-2)/2
        menu = [(a[0],a[1],price) for a,price,label in older.menu((t,F(1,10)))]
        lowered = list(menu)
        ax,ay,price = lowered[-1]
        lowered[-1] = ax,ay,price-e
        old_revenue = p.polygon_revenue(menu)[0]
        new_revenue = p.polygon_revenue(lowered)[0]
        exact = e*alpha*L/4-e*e*alpha/(4*beta*(1-beta))-e**3/(2*beta*(1-beta)**2)
        assert new_revenue-old_revenue == exact
        cut_checks.append(dict(t=str(t),exact_payment_cut_gain=str(exact)))
    data = dict(status='OUTER_FEE_POLYGON_AUDIT_EXACT_PASS',epsilon=str(e),
                scope='independent continuous-cell integration and actual baseline-menu audit; no type-grid optimality claim',
                method='rational halfplane clipping and shoelace areas; no primary fee-integral coefficients imported',
                fee_formula='e*(1-3*D0)-3*C*e^2/2-e^3/2',
                no_sale_formula='D0(e)=D0+C*e+e^2/2',
                fee_fibers=len(details),actual_mechanism_cell_checks=menu_checks,
                branches=sorted(set(row['branch'] for row in details)),
                details=details,cut_checks=cut_checks,
                proof='research_log/outer_fee_polygon_audit.md')
    path = ROOT/'certificate'/'outer_fee_polygon_audit.json'
    if '--write' in sys.argv:
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads(path.read_text(encoding='utf-8')) == data
    print(data['status'])
    print('fee_fibers',len(details),'actual_menu_cells',menu_checks,'cut_fibers',len(cut_checks))
    print('branches',data['branches'])
    return data


if __name__ == '__main__':
    verify()
