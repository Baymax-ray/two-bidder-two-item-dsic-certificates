"""Independent interval replay of split-cost revenue changes.

No import of split_cost_revenue or its logarithm/radical evaluator.
Radical moments use integrated alternating binomial bounds. Bundle moments
use polygon area and first moments. Q changes use moving-strip differences.
The base derivative polynomial is an explicit independently audited input.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
import sys

if not __debug__:
    raise RuntimeError('Run without -O')
ROOT=Path(__file__).resolve().parents[1]
a,b,s0=F(159,250),F(91,100),F(1137,1000)
c,d,q=b-a,s0-a,s0-b
A=F(2,3)
theta=-F(1,1000)
s1=s0+theta
K=A+c*c
r0,r1=b*b-K,F(4,3)*c-F(2,9)
cut=(F(1,2)-c+F(3,4)*q*q)/(F(3,2)*q)


def add(p,z):
    out=[F()]*max(len(p),len(z))
    for j,x in enumerate(p):out[j]+=x
    for j,x in enumerate(z):out[j]+=x
    return out


def scale(p,z):return [x*z for x in p]


def mul(p,z):
    out=[F()]*(len(p)+len(z)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(z):out[i+j]+=x*y
    return out


def power(p,n):
    out=[F(1)]
    for _ in range(n):out=mul(out,p)
    return out


def integral(p,lo,hi):
    return sum((x*(hi**(j+1)-lo**(j+1))/F(j+1) for j,x in enumerate(p)),F())


def ia(x,y):return (x[0]+y[0],x[1]+y[1])
def neg(x):return (-x[1],-x[0])
def sub(x,y):return ia(x,neg(y))
def im(x,y):
    z=[xx*yy for xx in x for yy in y]
    return min(z),max(z)
def isc(x,k):return im(x,(F(k),F(k)))
def point(x):return F(x),F(x)


def eval_interval(p,x):
    z=point(0)
    for co in reversed(p):z=ia(im(z,x),point(co))
    return z


def bounded_integral(p,lo,hi):
    primitive=[F()]+[co/F(j+1) for j,co in enumerate(p)]
    return sub(eval_interval(primitive,hi),eval_interval(primitive,lo))


def sqrt_bracket(x,bits=180):
    den=1<<bits
    n=isqrt(x.numerator*den*den//x.denominator)
    out=F(n,den),F(n+1,den)
    assert out[0]*out[0]<=x<=out[1]*out[1]
    return out


def rounded(x,digits=30):
    unit=10**digits
    lo=(x[0]*unit).numerator//(x[0]*unit).denominator
    hi=-((-x[1]*unit).numerator//(-x[1]*unit).denominator)
    return [str(F(lo,unit)),str(F(hi,unit))]


def root_moments():
    k0,k1=sqrt_bracket(r0),sqrt_bracket(r1)
    lo,hi=k0[1],k1[0]
    assert lo<hi and (lo*lo-r0)/b**2>=0
    assert (hi*hi-r0)/b**2<F(7,100)
    z=[-r0/b**2,F(),1/b**2]
    coeff=F(1)
    zp=[F(1)]
    partial=[F()]
    lower=upper=None
    # For 0<=z<.07, sqrt(1+z) is alternating after its linear term,
    # with decreasing term magnitudes. Even/odd truncations enclose it.
    for n in range(28):
        if n:
            coeff*= (F(1,2)-(n-1))/n
            zp=mul(zp,z)
        partial=add(partial,scale(zp,b*coeff))
        if n==26:lower=add(partial,[-b])
        if n==27:upper=add(partial,[-b])
    width_error=2*((k0[1]-k0[0])+(k1[1]-k1[0]))
    out=[]
    for j in (0,1):
        weight=scale(mul([b-q,-F(1)],[F()]*j+[F(1)]),2)
        low=integral(mul(weight,lower),lo,hi)
        high=integral(mul(weight,upper),lo,hi)+width_error
        # True omitted-end integrands are nonnegative and at most 2.
        assert 0<low<high
        out.append((low,high))
    return out,k1


def polygon_moments(vertices):
    twice_area=moment6=F()
    for (x,y),(xx,yy) in zip(vertices,vertices[1:]+vertices[:1]):
        cross=x*yy-xx*y
        twice_area+=cross
        moment6+=(x+xx)*cross
    if twice_area<0:twice_area,moment6=-twice_area,-moment6
    return twice_area/2,moment6/6


def moments():
    (rr0,rr1),k1=root_moments()
    all0,all1,Q0,Q1=rr0,rr1,rr0,rr1
    k=[-q,F(1)]
    C=add([F(5,6)],scale(power(k,2),F(3,4)))
    threshold=ia(k1,point(q))
    # Joined geometry is derived from the frozen branch menus.
    beta=add(C,[-b])
    for j in (0,1):
        poly=scale(mul(mul([b,-F(1)],power(k,j)),beta),2)
        value=bounded_integral(poly,threshold,point(a))
        if j==0:all0,Q0=ia(all0,value),ia(Q0,value)
        else:all1,Q1=ia(all1,value),ia(Q1,value)
    beta=add(C,[-c,-F(1)])
    for j in (0,1):
        plain=mul(power(k,j),beta)
        av=integral(scale(plain,2*c),a,A)
        qv=integral(scale(mul([b,-F(1)],plain),2),a,A)
        if j==0:all0,Q0=ia(all0,point(av)),ia(Q0,point(qv))
        else:all1,Q1=ia(all1,point(av)),ia(Q1,point(qv))
    beta=[F(1,2)-c+F(3,4)*q*q,-F(3,2)*q]
    all0=ia(all0,point(integral(scale(beta,2*c),A,cut)))
    all1=ia(all1,point(integral(scale(mul(k,beta),2*c),A,cut)))
    data=json.loads((ROOT.parent/'V3/certificate/baseline_mechanism.json').read_text(encoding='utf-8'))
    assert len(data['bundle_rows'])==41
    bm0=bm1=F()
    for row in data['bundle_rows']:
        sl,sh=map(F,row['sum_interval'])
        el,eh=map(F,row['normalized_rho_interval'])
        fee=F(row['fee'])
        vertices=[]
        for sigma,eta in ((sl,el),(sh,el),(sh,eh),(sl,eh)):
            rho=c+eta*(sigma-c-d)
            t=sigma-rho
            vertices.append((t,rho))
            assert rho<d-F(1,1000) and t>d+F(1,1000)
            # All relevant inequalities are affine on this polygon.
            oldA,oldB,oldC=sigma-c+fee,rho+q+fee,sigma+fee
            for delta in (-F(1,1000),F(1,1000)):
                newB=oldB+delta
                assert 0<oldA<1 and 0<newB<1
                assert max(oldA,newB)<oldC<oldA+newB
        area,first_t=polygon_moments(vertices)
        assert area>0
        bm0+=2*fee*area
        bm1+=2*fee*(first_t-q*area)
    all0,all1=ia(all0,point(bm0)),ia(all1,point(bm1))
    return dict(all0=all0,all1=all1,Q0=Q0,Q1=Q1,
                root0=rr0,root1=rr1,bundle0=point(bm0),bundle1=point(bm1))


def delta_G_B(B,C,delta):
    # Each argument is a polynomial in the opposing high coordinate.
    first=mul(mul(delta,add(C,scale(B,-1))),add([F(2)],scale(B,-3)))
    second=mul(power(delta,2),add(add(scale(B,3),[-F(1)]),scale(C,-F(3,2))))
    return add(add(first,second),power(delta,3))


def Q_changes():
    d1=s1-a
    assert d1<d<a<A
    weight=[2*b,-F(2)]
    # Newly constrained strip replaces the former constant (a,a,b) menu.
    strip=integral(mul(weight,delta_G_B([a],[b],[d1,-F(1)])),d1,d)
    zpart=integral(mul(weight,delta_G_B([s0,-F(1)],[b],[theta])),d,a)
    spart=integral(mul(weight,delta_G_B([d],[c,F(1)],[theta])),a,A)
    delta_base=strip+zpart+spart
    def value_poly(qq):
        k=[-qq,F(1)]
        return add(add([F(59,108)],scale(power(k,2),F(1,4))),
                   add(scale(power(k,3),-1),scale(power(k,4),F(9,16))))
    oldv,newv=value_poly(q),value_poly(q+theta)
    strip_area=integral(weight,d1,d)
    delta_inner_r=integral(mul(weight,add(newv,[-F(4,9)])),d1,d)
    delta_inner_r+=integral(mul(weight,add(newv,scale(oldv,-1))),d,A)
    delta_inner_s=-F(2,27)*strip_area
    return delta_base,(delta_inner_r,delta_inner_s)


def evaluate():
    primary=json.loads((ROOT/'certificate/split_cost_revenue.json').read_text(encoding='utf-8'))
    mm=moments()
    for key,value in mm.items():
        expected=tuple(map(F,primary['moment_intervals'][key]))
        assert expected[0]<=value[0]<=value[1]<=expected[1],key
    delta_bq,delta_iq=Q_changes()
    assert delta_bq==F(primary['base_Q_delta'])
    oldpair,newpair=(list(map(F,primary[key])) for key in ('inner_Q_old_pair','inner_Q_new_pair'))
    assert delta_iq==tuple(y-x for x,y in zip(oldpair,newpair))
    # Explicit shared mathematical dependency; independently checked by the
    # separate base-revenue audit, not established by this moment verifier.
    base_derivative=[F(39760023849,3906250000),-F(48411347,1953125),
                     F(221343,10000),-F(216,25),F(5,4)]
    assert list(map(F,primary['base_derivative_polynomial']))==base_derivative
    delta_base=2*integral(base_derivative,s0,s1)
    assert delta_base==F(primary['base_total_delta'])
    fee=ia(isc(sub(isc(mm['all1'],2),mm['Q1']),-3*theta),
           isc(sub(isc(mm['all0'],2),mm['Q0']),F(3,2)*theta*theta))
    iq=ia(point(delta_iq[0]),isc(sqrt_bracket(F(2)),delta_iq[1]))
    gain=ia(point(delta_base-delta_bq),ia(fee,iq))
    expected=tuple(map(F,primary['gain_rational_interval']))
    assert 0<expected[0]<=gain[0]<=gain[1]<=expected[1]
    prev=json.loads((ROOT.parent/'V3_1/certificate/independent_revenue.json').read_text(encoding='utf-8'))
    revenue=ia(tuple(map(F,prev['independent_total_revenue_interval'])),gain)
    return {
        'status':'INDEPENDENT_SPLIT_REVENUE_PASS',
        'scope':'Independent moments and moving-strip revenue differences; feasible-mechanism proof and base derivative have separate audits',
        'method':'Alternating binomial degrees 26/27; dyadic sqrt brackets; polygon area/first moment; moving-strip finite differences',
        'no_primary_revenue_module_import':True,
        'binomial_even_lower_order':26,'binomial_odd_upper_order':27,
        'sqrt_bracket_bits':180,'bundle_polygons':41,
        'moment_intervals':{key:rounded(value) for key,value in mm.items()},
        'base_Q_change':str(delta_bq),'inner_Q_change_pair':list(map(str,delta_iq)),
        'trusted_base_derivative_polynomial':list(map(str,base_derivative)),
        'base_total_change':str(delta_base),'fee_change_interval':rounded(fee),
        'inner_change_interval':rounded(iq),'gain_rational_interval':rounded(gain,24),
        'total_revenue_interval':rounded(revenue,24),
        'prior_revenue_source':'V3_1/certificate/independent_revenue.json',
        'not_claimed':['Full unrestricted optimality','Independent regeneration of frozen V3.1 revenue','A proof of the base derivative polynomial in this script']
    }


if __name__=='__main__':
    data=evaluate()
    target=ROOT/'certificate/independent_split_revenue.json'
    if '--write' in sys.argv:target.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(target.read_text(encoding='utf-8'))==data
    print(data['status'])
    print('gain',data['gain_rational_interval'])
    print('revenue',data['total_revenue_interval'])
