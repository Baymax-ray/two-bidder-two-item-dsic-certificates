"""Independent polynomial replay of the complete functional revenue change.

The base derivatives are reconstructed from menu-cell revenue formulas,
not imported from the primary functional calculator. Q is integrated after
the monotone change of variable, including its Jacobian. Fractions only.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys
import independent_family_revenue as p
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
C,X,Y,ONE=p.C,p.X,p.Y,p.ONE
add,sub,mul,scale,power=p.add,p.sub,p.mul,p.scale,p.power

def derivative(z):return {(i-1,j):i*v for (i,j),v in z.items() if i}

def integrate_x(z,lo,hi):
    result={}
    for (i,j),v in z.items():
        result=add(result,scale(mul(power(Y,j),sub(power(hi,i+1),power(lo,i+1))),v/F(i+1)))
    assert all(i==0 for i,j in result)
    return {(j,0):v for (i,j),v in result.items()}

def direct_base_variation(revenue,P,B,S):
    zero=revenue(P,B,S)
    plus=revenue(P,add(B,ONE),add(S,ONE))
    minus=revenue(P,sub(B,ONE),sub(S,ONE))
    first=scale(sub(plus,minus),F(1,2))
    second=scale(sub(add(plus,minus),scale(zero,2)),F(1,2))
    assert second==C(-1)
    # The formulas have degree at most three in a common price shift.
    # This fourth evaluation independently rules out a cubic term.
    assert revenue(P,add(B,C(2)),add(S,C(2)))==add(zero,scale(first,2),scale(second,4))
    return first

def high_price_revenue(P,B,S):
    k=sub(S,B)
    return add(mul(B,k,sub(ONE,B)),mul(S,add(mul(sub(ONE,k),sub(ONE,B)),scale(power(sub(ONE,k),2),F(1,2)))))

def calculate():
    b,c,q=F(49,50),F(47,150),F(14,75)
    L,M,U=F(8,25),F(33,100),F(17,50)
    epsilon=F(1,1000)
    C0=add(C(F(5,6)),scale(power(X,2),F(3,4)))
    I=p.G(C(F(2,3)),sub(C0,X),C0)
    assert I==add(C(F(59,108)),scale(power(X,2),F(1,4)),scale(power(X,3),-1),scale(power(X,4),F(9,16)))
    Q1=Q2=F()
    # Direct expansion of ((b-h) I - (b-C0)^3/3) h'.
    J=sub(mul(sub(C(b-q),X),I),scale(power(sub(C(b),C0),3),F(1,3)))
    pieces=[(L,M,scale(sub(X,C(L)),1/(M-L))),
            (M,U,scale(sub(C(U),X),1/(U-M)))]
    for lo,hi,phi in pieces:
        first=sub(mul(J,derivative(phi)),mul(phi,I))
        second=scale(mul(phi,I,derivative(phi)),-1)
        Q1+=4*p.rat_integral(first,lo,hi)
        Q2+=4*p.rat_integral(second,lo,hi)
    P,B,S=sub(add(X,Y),C(c)),add(Y,C(q)),add(X,Y)
    gamma_low=direct_base_variation(p.G,P,B,S)
    gamma_high=direct_base_variation(high_price_revenue,P,B,S)
    # Conditional high-report domains: b-r <= t <= 1+c-r <= 1.
    gamma=add(integrate_x(gamma_low,sub(C(b),Y),sub(C(1+c),Y)),
              integrate_x(gamma_high,sub(C(1+c),Y),ONE))
    B1=B2=F()
    for lo,hi,phi in pieces:
        B1+=4*p.rat_integral(mul(phi,gamma),lo,hi)
        B2-=4*p.rat_integral(mul(power(phi,2),add(C(1-b),X)),lo,hi)
    components=dict(Q_linear=str(Q1),base_linear=str(B1),Q_quadratic=str(Q2),base_quadratic=str(B2))
    first,second=Q1+B1,Q2+B2
    gain=epsilon*first+epsilon**2*second
    assert first+2*epsilon*second>0 and gain>0
    primary=json.loads((ROOT/'certificate/functional_exchange.json').read_text(encoding='utf-8'))
    assert components==primary['coefficient_components']
    assert first==F(primary['linear_coefficient'])
    assert second==F(primary['quadratic_coefficient'])
    assert gain==F(primary['exact_gain'])
    clean=p.calculate()['full_Q_coefficients']
    final=(F(clean[0])+gain,F(clean[1]),F(clean[2])*F(2,15))
    assert final==tuple(map(F,primary['radical_coefficients_basis_1_sqrt2_sqrt11']))
    return dict(status='INDEPENDENT_FUNCTIONAL_REVENUE_PASS',
      coefficient_components=components,linear_coefficient=str(first),quadratic_coefficient=str(second),
      exact_gain=str(gain),final_coefficients=list(map(str,final)),
      proof_scope='Exact continuum revenue identity; pointwise mechanism validity is proved and audited separately',
      independence='Primary functional calculator not imported; direct Q Jacobian expansion and base menu price-shift reconstruction')

def main():
    data=calculate();target=ROOT/'certificate/independent_functional.json'
    if '--write' in sys.argv:target.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(target.read_text(encoding='utf-8'))==data
    print(data['status']);print('gain',data['exact_gain'])
if __name__=='__main__':main()
