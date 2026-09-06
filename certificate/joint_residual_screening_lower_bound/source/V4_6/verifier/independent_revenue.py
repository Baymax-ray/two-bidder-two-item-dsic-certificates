"""Independent continuum integration; no project calculator is imported.

All integrals below start from allocation-cell areas. In particular the Q
cost is integrated as a two-variable polynomial over its curved domain,
rather than using the primary Taylor-expansion calculation. The earlier
V4.5 total enclosure is an explicitly identified frozen dependency.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError("Run without -O.")
ROOT = Path(__file__).resolve().parents[1]

def constant(v):
    return {(0,0):F(v)} if v else {}

def add(*polys):
    out = {}
    for p in polys:
        for k,v in p.items():
            out[k] = out.get(k,F())+v
    return {k:v for k,v in out.items() if v}

def scale(p,c):
    return {k:v*c for k,v in p.items() if v*c}

def multiply(*polys):
    out = constant(1)
    for p in polys:
        new = {}
        for (i,j),v in out.items():
            for (h,k),w in p.items():
                key = i+h,j+k
                new[key] = new.get(key,F())+v*w
        out = {k:v for k,v in new.items() if v}
    return out

def power(p,n):
    return multiply(*([p]*n))

def subtract(p,q):
    return add(p,scale(q,-1))

ONE,T,Z = constant(1),{(1,0):F(1)},{(0,1):F(1)}
a,b,c,A,q = F(159,250),F(91,100),F(137,500),F(2,3),F(113,500)

def menu_revenue(p1,p2,p12):
    # Singleton cells and bundle rectangle minus its right triangle.
    s1=multiply(p1,subtract(ONE,p1),subtract(p12,p1))
    s2=multiply(p2,subtract(ONE,p2),subtract(p12,p2))
    rb=multiply(add(ONE,p1,scale(p12,-1)),add(ONE,p2,scale(p12,-1)))
    cut=add(p1,p2,scale(p12,-1))
    return add(s1,s2,multiply(p12,add(rb,scale(power(cut,2),F(-1,2)))))

def at_t(p,x):
    assert all(j==0 for i,j in p)
    return sum((v*x**i for (i,j),v in p.items()),F())

def integrate_z(p,lo,hi):
    out={}
    for (i,j),v in p.items():
        term=multiply({(i,0):v/F(j+1)},subtract(power(hi,j+1),power(lo,j+1)))
        out=add(out,term)
    assert all(j==0 for i,j in out)
    return out

def primitive_t(p):
    assert all(j==0 for i,j in p)
    return {(i+1,0):v/F(i+1) for (i,j),v in p.items()}

def pair_add(x,y):
    return x[0]+y[0],x[1]+y[1]

def pair_mul(x,y,d):
    return x[0]*y[0]+d*x[1]*y[1],x[0]*y[1]+x[1]*y[0]

def pair_eval(p,x,d):
    # Horner evaluation in a quadratic field, distinct from binomial replay.
    assert all(j==0 for i,j in p)
    result=F(),F()
    for i in range(max((i for i,j in p),default=0),-1,-1):
        result=pair_add(pair_mul(result,x,d),(p.get((i,0),F()),F()))
    return result

def integrate_t(p,lo,hi,d=2):
    primitive=primitive_t(p)
    lower,upper=pair_eval(primitive,lo,d),pair_eval(primitive,hi,d)
    return upper[0]-lower[0],upper[1]-lower[1]

def interval(coeffs,digits=55):
    lo=hi=coeffs[0]
    den=10**digits
    for coefficient,d in zip(coeffs[1:],(2,23)):
        n=isqrt(d*den*den)
        assert n*n<d*den*den<(n+1)*(n+1)
        lb,ub=F(n,den),F(n+1,den)
        lo+=coefficient*(lb if coefficient>=0 else ub)
        hi+=coefficient*(ub if coefficient>=0 else lb)
    return lo,hi

def strings(xs):
    return list(map(str,xs))

def calculate():
    b0=(F(4,3),F(-1,3))
    old=at_t(menu_revenue(constant(a),constant(a),constant(b)),0)
    assert old==F(136719583,250000000)
    area=(F(1,12),F(1,9))
    free=pair_mul(area,(F(4,9)-old,F(2,27)),2)
    assert free==(F(1925713777,243000000000),-F(11719583,2250000000))
    # Full added Eplus strip, both bidders and both orientations.
    end=F(613,750)
    other=F(839,750)
    cutoff=F(1058587,1362000)
    delta=scale(multiply(subtract(constant(end),T),subtract(constant(other),T)),F(9,16))
    qold=F(227,1000)
    deltaold=add(constant(F(1,2)-c+F(3,4)*qold*qold),scale(T,-F(3,2)*qold))
    alpha=add(scale(T,3),constant(-2))
    g1=add(power(subtract(delta,deltaold),2),scale(multiply(deltaold,power(alpha,2)),F(1,8)))
    weight=scale(subtract(T,constant(a)),4)
    strip=integrate_t(multiply(weight,g1),(A,F()),(cutoff,F()))[0]
    strip+=integrate_t(multiply(weight,power(delta,2)),(cutoff,F()),(end,F()))[0]
    assert strip==F(305193169586616381246083,101062797120000000000000000000)
    # Bundle exchange: integrate whole menu difference, including all types.
    gain1=integrate_t(multiply(subtract(ONE,T),subtract(menu_revenue(constant(a),constant(a),T),constant(old))),b0,(b,F()))
    area_g=integrate_t(subtract(ONE,T),b0,(b,F()))
    new_free=integrate_t(multiply(subtract(ONE,T),menu_revenue(constant(A),constant(A),T)),b0,(b,F()))
    old_free=pair_mul(area_g,(F(4,9),F(2,27)),2)
    cost_free=(new_free[0]-old_free[0],new_free[1]-old_free[1])
    k=subtract(T,constant(q))
    C=add(constant(F(5,6)),scale(power(k,2),F(3,4)))
    B=subtract(C,k)
    integrand=subtract(menu_revenue(constant(A),B,Z),menu_revenue(constant(A),B,C))
    cost_poly=scale(integrate_z(integrand,C,constant(b)),2)
    cost=integrate_t(cost_poly,(F(1,2),F()),(q,F(1,15)),23)
    bundle=(gain1[0]+cost_free[0]+cost[0],gain1[1]+cost_free[1],cost[1])
    assert bundle==(F(-61265474244901887143940289321,3402000000000000000000000000000),F(155394217,12150000000),-F(12495509,797343750000))
    # A possible coupled safe-price response, kept separate until feasibility
    # and a complete pointwise mechanism are supplied by its own proof.
    coupled_integrand=subtract(menu_revenue(constant(A),subtract(Z,k),Z),menu_revenue(constant(A),B,Z))
    coupled_poly=scale(integrate_z(coupled_integrand,C,constant(b)),2)
    coupled=integrate_t(coupled_poly,(F(1,2),F()),(q,F(1,15)),23)
    baseline=json.loads((ROOT.parent/'V4_5'/'certificate'/'independent_lottery.json').read_text(encoding='utf-8'))
    baseline_interval=tuple(map(F,baseline['revenue_interval']))
    addition=(strip+free[0]+bundle[0],free[1]+bundle[1],bundle[2])
    ilo,ihi=interval(addition)
    total=baseline_interval[0]+ilo,baseline_interval[1]+ihi
    coupled_primary=json.loads((ROOT/'certificate'/'outer_bundle_reoptimized.json').read_text(encoding='utf-8'))
    assert strings(coupled)==coupled_primary['revenue']['extra_gain_pair']
    refined_addition=(addition[0]+coupled[0],addition[1],addition[2]+coupled[1])
    clow,chigh=interval(refined_addition)
    refined_total=baseline_interval[0]+clow,baseline_interval[1]+chigh
    assert refined_total[0]>total[1]
    primary=json.loads((ROOT/'certificate'/'outer_bundle_exchange.json').read_text(encoding='utf-8'))
    assert strings(bundle)==primary['revenue']['gain_coefficients']
    primary_free=json.loads((ROOT/'certificate'/'free_bidder_one.json').read_text(encoding='utf-8'))
    assert strings(free)==primary_free['gain_pair']
    assert interval(bundle)[0]>0 and interval((free[0],free[1],F()))[0]>0
    return dict(scope='independent exact V4.6 increments; V4.5 total is a frozen dependency',
                strip_gain=str(strip),free_gain_pair=strings(free),bundle_gain_coefficients=strings(bundle),
                total_addition_basis=['1','sqrt(2)','sqrt(23)'],total_addition_coefficients=strings(addition),
                reference_revenue_interval=strings(total),
                coupled_safe_price_integral_pair=strings(coupled),
                coupled_field='sqrt(23)',
                refined_addition_coefficients=strings(refined_addition),
                refined_reference_revenue_interval=strings(refined_total),
                coupled_status='independent integral matches outer_bundle_reoptimized; its pointwise proof is separate',
                baseline_dependency='V4_5/certificate/independent_lottery.json',
                exact_total='R_V4.5 + sum(total_addition_coefficients * total_addition_basis)',
                integration='direct allocation-cell polynomial; curved-domain z integral, then quadratic-field Horner primitive')

def verify():
    data=calculate()
    target=ROOT/'certificate'/'independent_revenue.json'
    if '--write' in sys.argv:
        target.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads(target.read_text(encoding='utf-8'))==data
    print('V4_6_INDEPENDENT_CONTINUUM_REVENUE_PASS')
    print('reference_revenue_display',float(F(data['reference_revenue_interval'][0])))
    print('refined_reference_revenue_display',float(F(data['refined_reference_revenue_interval'][0])))
    print('coupled_safe_price_integral_pair',data['coupled_safe_price_integral_pair'])
    return data

if __name__=='__main__':
    verify()
