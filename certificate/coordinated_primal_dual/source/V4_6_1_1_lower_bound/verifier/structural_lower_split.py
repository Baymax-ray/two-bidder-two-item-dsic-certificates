"""Exact complete menu integrals for coordinated split lowering."""
from fractions import Fraction as F
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verifier'))
import structural_split as out
p=out.p;A=F(2,3)

def revenue(a,c,d):
    b,s,q=a+c,a+d,d-c;cE=F(1,2)-q;T,U=1-2*cE/3,F(5,3)-2*cE
    assert a>=F(1,2) and b<=2*d<=1 and c<d and A<T
    X,P,I=p.X,p.P,p.I
    outside=out.outer_base(a,c,d,T)
    k=X-q;C0=P(F(5,6))+F(3,4)*k*k
    Ri=P(F(59,108))+F(1,4)*k*k-k**3+F(9,16)*k**4
    r2=p.square(2);B0=(I(4)-r2)/3;RF=I(F(4,9))+F(2,27)*r2
    qlow=2*(d*d-(2*d-b)**2/2)*RF
    exchange=2*p.integral((2*d-X)*p.G(P(A),P(A),X),B0,b)-2*RF*p.integral(2*d-X,B0,b)
    qhigh=I(4*p.ratint((b-X)*Ri,d,A))
    rb=4*(b-F(5,6))/3;upper=q+p.square(rb)
    assert d<upper.lo<upper.hi<A
    cost=-F(4,3)*p.integral((b-C0)**3,d,upper)
    dl=F(9,16)*(T-X)*(U-X)
    e=I(4*c*p.ratint(p.G(X,P(F(1,2)),X+cE)+dl*dl,A,T))
    return I(outside)+qlow+exchange+qhigh+cost+e

if __name__=='__main__':
    a,c=A,F(47,150)
    for d in (F(1,2),F(4999,10000),F(499,1000),F(99,200),F(49,100)):
      r=revenue(a,c,d)
      print('d',d,'R',p.tools.rounded_interval(r,30),'float',float(r.lo))
