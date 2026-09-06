"""Exact revenue coordinates with the reserve on either side of A.

Uses the preserved independent polynomial integration kernel. The all-real
mechanism proof is separate. Unlike the earlier discovery family, Q ends
at sum=b on every high-report fiber, including t>a.
"""
from pathlib import Path
from fractions import Fraction as F
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V4_6_1_lower_bound/verifier'))
import independent_family_revenue as p
C,X,Y,ONE=p.C,p.X,p.Y,p.ONE
add,sub,mul,scale,power=p.add,p.sub,p.mul,p.scale,p.power
A,d=F(2,3),F(1,2)

def derivative(z):return {(i-1,j):i*v for (i,j),v in z.items() if i}

def integrate_x(z,lo,hi):
    out={}
    for (i,j),v in z.items():
        out=add(out,scale(mul(power(Y,j),sub(power(hi,i+1),power(lo,i+1))),v/F(i+1)))
    assert all(i==0 for i,j in out)
    return {(j,0):v for (i,j),v in out.items()}

def clean(a,c,cap=True):
    assert d<a and F(3,10)<=c<F(1,3)
    b,s,q=a+c,a+d,d-c
    assert b<1 and b>A
    k=sub(X,C(q));C0=add(C(F(5,6)),scale(power(k,2),F(3,4)))
    I=p.G(C(A),sub(C0,k),C0)
    Z=p.G(C(a),sub(C(s),X),C(b))
    S=p.G(X,C(d),add(X,C(c)))
    base,cells=p.base_revenue(a,c)
    high=4*p.rat_integral(mul(sub(C(b),X),sub(I,Z)),d,min(a,A))
    if a<A:high+=4*p.rat_integral(mul(sub(C(b),X),sub(I,S)),a,A)
    T,U=1-F(2,3)*c,F(5,3)-2*c
    delta=scale(mul(sub(C(T),X),sub(C(U),X)),F(9,16))
    lottery=4*c*p.rat_integral(power(delta,2),A,T)
    if a>A:
        assert a<T
        lottery+=4*c*p.rat_integral(sub(S,Z),A,a)
    b0=(F(4,3),-F(1,3));areaF=(F(1,12),F(1,9));RF=(F(4,9),F(2,27))
    areaL=F(1,4)-(1-b)**2/2
    ff=p.pmul(areaF,RF,F(2))
    integ=p.integrate(mul(sub(ONE,X),p.G(C(A),C(A),X)),b0,(b,F()))
    low=(2*(ff[0]+integ[0]-areaL*p.value(p.G(C(a),C(a),C(b)),0)),2*(ff[1]+integ[1]))
    D=F(4,3)*(b-F(5,6))
    assert c*c<D<(A-q)**2
    cut=p.integrate(scale(power(sub(C(b),C0),3),-F(4,3)),(d,F()),(q,F(1)),D)
    clipping=F()
    if cap and a>A:
        W=sub(C(c+a-A),X)
        J=add(scale(mul(X,power(W,3)),F(1,2)),scale(power(W,4),F(1,8)))
        clipping=4*p.rat_integral(J,c,c+a-A)
    coeff=(base+high+lottery+low[0]+cut[0]+clipping,low[1],cut[1])
    return dict(a=a,c=c,b=b,q=q,D=D,coefficients=coeff,
        interval=p.bound(coeff,(F(2),D)),base=base,base_cells=cells,
        high=high,lottery=lottery,low=low,cut=cut,clipping=clipping)

def functional_polynomials(a,c):
    assert d<a
    b,q=a+c,d-c
    C0=add(C(F(5,6)),scale(power(X,2),F(3,4)))
    I=p.G(C(A),sub(C0,X),C0);Ip=derivative(I)
    # Direct base revenue derivatives, with high singleton unchanged.
    P,B,S=sub(add(X,Y),C(c)),add(Y,C(q)),add(X,Y)
    def high_price(P,B,S):
        k=sub(S,B)
        return add(mul(B,k,sub(ONE,B)),mul(S,add(mul(sub(ONE,k),sub(ONE,B)),scale(power(sub(ONE,k),2),F(1,2)))))
    gammas=[]
    for R in (p.G,high_price):
        zero=R(P,B,S);plus=R(P,add(B,ONE),add(S,ONE));minus=R(P,sub(B,ONE),sub(S,ONE))
        gamma=scale(sub(plus,minus),F(1,2))
        assert scale(sub(add(plus,minus),scale(zero,2)),F(1,2))==C(-1)
        assert R(P,add(B,C(2)),add(S,C(2)))==add(zero,scale(gamma,2),C(-4))
        gammas.append(gamma)
    inner=add(integrate_x(gammas[0],sub(C(b),Y),sub(C(1+c),Y)),
              integrate_x(gammas[1],sub(C(1+c),Y),ONE))
    linear=scale(add(scale(mul(sub(C(b-q),X),Ip),-1),
        scale(mul(X,power(sub(C(b),C0),2)),-F(3,2)),inner),4)
    quadratic=sub(scale(add(C(1-b),X),4),scale(Ip,2))
    return linear,quadratic

def affine_gain(a,c,slope,endpoint):
    linear,quadratic=functional_polynomials(a,c)
    g=scale(sub(C(endpoint),X),slope)
    gain=p.rat_integral(sub(mul(linear,g),mul(quadratic,power(g,2))),c,endpoint)
    if a>A:
        b,q=a+c,d-c;m=c+a-A
        assert m<endpoint
        P,B,S=C(a),sub(C(a+d),X),C(b)
        plus=p.G(P,add(B,ONE),add(S,ONE));minus=p.G(P,sub(B,ONE),sub(S,ONE))
        gamma=scale(sub(plus,minus),F(1,2))
        inner=integrate_x(gamma,C(A),sub(C(b),Y))
        W=sub(C(m),X)
        extra_linear=add(scale(inner,4),scale(mul(X,power(W,2)),6))
        extra_quadratic=scale(W,4)
        gain+=p.rat_integral(sub(mul(extra_linear,g),mul(extra_quadratic,power(g,2))),c,m)
    return gain

def affine_hypotheses(a,c,slope,endpoint):
    q=d-c;b=a+c;m=c+max(a-A,F())
    if not d<a or not F(3,10)<=c<F(1,3) or not b<1:return False
    if a-A>(1-2*c)**2/8 or not c<endpoint<d or not 0<slope<1:return False
    if not m<endpoint:return False
    # On the left segment the bound is affine. On the right, the
    # convex quadratic minus g is minimized at its vertex or an endpoint.
    B0=lambda k:F(5,6)+F(3,4)*k*k-k
    g=lambda x:slope*(endpoint-x)
    if a>A:
        if min(B0(A-q)-x-q-g(x) for x in (c,m))<0:return False
    lo=max(c,m);vertex=b-q-F(2,3)*slope
    nodes=[lo,endpoint]+([vertex] if lo<vertex<endpoint else [])
    if min(B0(b-x-q)-x-q-g(x) for x in nodes)<0:return False
    # Q/base low-y compatibility, and the affected C0<b integration cell.
    low_nodes=[c,endpoint];low_vertex=F(2,3)*(1-slope)
    if c<low_vertex<endpoint:low_nodes.append(low_vertex)
    if min(B0(x)-d-g(x) for x in low_nodes)<0:return False
    if F(5,6)+F(3,4)*endpoint*endpoint>=b:return False
    return True

def display(data,gain=F()):return float(data['interval'][0]+gain)
