"""Exact discovery integrals for varying a above the conditional singleton A.
Feasibility must be established separately before accepting a candidate.
"""
from fractions import Fraction as F
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V4_6_1_lower_bound/verifier'))
import parameter_revenue as p
import independent_family_revenue as ind
A=F(2,3);d=F(1,2)

def revenue(a,c):
    b,s,q=a+c,a+d,d-c;T,U=1-2*c/3,F(5,3)-2*c
    assert A<=a<T and b<1
    X,I,P=p.X,p.I,p.P
    base=ind.base_revenue(a,c)[0]
    k=X-q;C0=P(F(5,6))+F(3,4)*k*k
    Ri=P(F(59,108))+F(1,4)*k*k-k**3+F(9,16)*k**4
    dl=F(9,16)*(T-X)*(U-X)
    qhigh=I(4*p.ratint((b-X)*(Ri-p.G(P(a),P(s)-X,P(b))),d,A))
    r2=p.square(2);B0=(I(4)-r2)/3;RF=I(F(4,9))+F(2,27)*r2
    qlow=2*(F(1,4)-(1-b)**2/2)*(RF-p.G(a,a,b))
    exchange=2*p.integral((1-X)*p.G(P(A),P(A),X),B0,b)-2*RF*p.integral(1-X,B0,b)
    rb=4*(b-F(5,6))/3;upper=q+p.square(rb)
    assert d<upper.lo<upper.hi<A
    cost=-F(4,3)*p.integral((b-C0)**3,d,upper)
    ect=I(4*c*p.ratint(p.G(X,P(d),X+c)-p.G(P(a),P(s)-X,P(b)),A,a))
    elot=I(4*c*p.ratint(dl*dl,A,T))
    return I(base)+qhigh+qlow+exchange+cost+ect+elot

if __name__=='__main__':
    c=F(47,150);base=revenue(A,c)
    for eps in (F(),F(1,100000),F(1,10000),F(1,1000),F(1,200),F(1,100)):
        r=revenue(A+eps,c)
        print('a',A+eps,'R',[float(r.lo),float(r.hi)],'difference',float((r-base).lo))
