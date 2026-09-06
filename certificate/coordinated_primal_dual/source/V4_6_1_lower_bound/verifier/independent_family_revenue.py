"""Independent exact continuum integration of the rebuilt symmetric family.

No other project calculator is imported. The common-base contribution is
integrated from menu-cell polynomials over rational opponent polygons.
Full-Q and H replacements use direct menu differences, with exact algebraic
endpoint evaluation. Mathematical feasibility is certified separately.
"""
from fractions import Fraction as F
from math import factorial,isqrt
from pathlib import Path
import json,sys
if not __debug__ or sys.flags.optimize: raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]

def C(v): return {(0,0):F(v)} if v else {}
X,Y={(1,0):F(1)},{(0,1):F(1)}
ONE=C(1)
def add(*ps):
    out={}
    for p in ps:
        for k,v in p.items(): out[k]=out.get(k,F())+v
    return {k:v for k,v in out.items() if v}
def scale(p,z): return {k:v*z for k,v in p.items() if v*z}
def sub(p,r): return add(p,scale(r,-1))
def mul(*ps):
    out=ONE
    for p in ps:
        new={}
        for (i,j),v in out.items():
            for (k,l),w in p.items(): new[(i+k,j+l)]=new.get((i+k,j+l),F())+v*w
        out={k:v for k,v in new.items() if v}
    return out
def power(p,n): return mul(*([p]*n))
def value(p,x,y=F()): return sum((v*x**i*y**j for (i,j),v in p.items()),F())
def G(p,r,s):
    return add(mul(p,sub(ONE,p),sub(s,p)),mul(r,sub(ONE,r),sub(s,r)),
               mul(s,sub(mul(add(ONE,r,scale(s,-1)),add(ONE,p,scale(s,-1))),scale(power(add(p,r,scale(s,-1)),2),F(1,2)))))
def clip(poly,plane):
    out=[]
    for first,last in zip(poly,poly[1:]+poly[:1]):
        u,v=value(plane,*first),value(plane,*last)
        if u>=0:out.append(first)
        if u*v<0:
            z=u/(u-v);out.append(tuple(a+z*(b-a) for a,b in zip(first,last)))
    return out

def polygon_integral(poly,p):
    result=F()
    for j in range(1,len(poly)-1):
        v0,v1,v2=poly[0],poly[j],poly[j+1]
        det=abs((v1[0]-v0[0])*(v2[1]-v0[1])-(v1[1]-v0[1])*(v2[0]-v0[0]))
        if not det:continue
        tx=add(C(v0[0]),scale(X,v1[0]-v0[0]),scale(Y,v2[0]-v0[0]))
        ty=add(C(v0[1]),scale(X,v1[1]-v0[1]),scale(Y,v2[1]-v0[1]))
        expanded={}
        for (h,k),coef in p.items(): expanded=add(expanded,scale(mul(power(tx,h),power(ty,k)),coef))
        result+=det*sum((z*F(factorial(h)*factorial(k),factorial(h+k+2)) for (h,k),z in expanded.items()),F())
    return result

def base_revenue(a,c):
    b,s=a+c,a+F(1,2)
    pivots=(C(0),sub(X,C(a)),sub(add(X,Y),C(b)))
    answer=area=F();records=[]
    for pivot_id,H in enumerate(pivots):
      for tx in (0,1):
       for ry in (0,1):
        poly=[(F(),F()),(F(1),F()),(F(1),F(1))]
        planes=[sub(H,h) for h in pivots]
        planes += [sub(X,C(F(1,2))) if tx else sub(C(F(1,2)),X),sub(Y,C(F(1,2))) if ry else sub(C(F(1,2)),Y)]
        for plane in planes:poly=clip(poly,plane)
        ph=add(H,sub(C(s),Y) if ry else C(a))
        pl=add(H,sub(C(s),X) if tx else C(a));pc=add(H,C(b));k=sub(pc,pl)
        for case in range(3):
            cell=poly[:]
            for plane in ([sub(ONE,ph)] if case==0 else [sub(ph,ONE),sub(ONE,pl)] if case==1 else [sub(pl,ONE)]): cell=clip(cell,plane)
            mass=polygon_integral(cell,ONE)
            if not mass:continue
            if case==0: revenue=G(ph,pl,pc)
            elif case==1: revenue=add(mul(pl,k,sub(ONE,pl)),mul(pc,add(mul(sub(ONE,k),sub(ONE,pl)),scale(power(sub(ONE,k),2),F(1,2)))))
            else: revenue=scale(mul(pc,power(sub(C(2),pc),2)),F(1,2))
            term=polygon_integral(cell,revenue)
            answer+=term;area+=mass
            records.append(dict(pivot=pivot_id,high_split=tx,low_split=ry,price_case=case,area=str(mass),integral=str(term),vertices=[[str(v) for v in point] for point in cell]))
    assert area==F(1,2)
    return 4*answer,records

def primitive(p):
    assert all(j==0 for i,j in p)
    return {(i+1,0):v/F(i+1) for (i,j),v in p.items()}
def pmul(u,v,d): return (u[0]*v[0]+d*u[1]*v[1],u[0]*v[1]+u[1]*v[0])
def peval(p,x,d):
    out=(F(),F())
    for i in range(max((i for i,j in p),default=0),-1,-1):
        out=pmul(out,x,d);out=(out[0]+p.get((i,0),F()),out[1])
    return out
def integrate(p,lo,hi,d=F(2)):
    z=primitive(p);u,v=peval(z,lo,d),peval(z,hi,d)
    return v[0]-u[0],v[1]-u[1]
def rat_integral(p,lo,hi): return integrate(p,(lo,F()),(hi,F()))[0]
def bound(coeffs,radicands,digits=50):
    lo=hi=coeffs[0];n=10**digits
    for c,d in zip(coeffs[1:],radicands):
        z=isqrt((d.numerator*n*n)//d.denominator)
        assert z*z*d.denominator<d.numerator*n*n<(z+1)**2*d.denominator
        a,b=F(z,n),F(z+1,n)
        lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
    return lo,hi

def calculate(a=F(2,3),c=F(47,150)):
    A,d=F(2,3),F(1,2);b,q=a+c,F(1,2)-c
    assert d<a<=A and F(1,6)<q and c<F(1,3)
    k=sub(X,C(q));C0=add(C(F(5,6)),scale(power(k,2),F(3,4)))
    Ri=G(C(A),sub(C0,k),C0)
    t1sq=F(4,3)*c-F(2,9)
    assert (a-q)**2>t1sq
    D=F(4,3)*(b-F(5,6))
    assert (d-q)**2<D<(a-q)**2
    base,records=base_revenue(a,c)
    Bz=G(C(a),sub(C(a+d),X),C(b));Bs=G(X,C(d),add(X,C(c)))
    high=4*rat_integral(mul(sub(C(b),X),sub(Ri,Bz)),d,a)
    high+=4*c*rat_integral(sub(Ri,Bs),a,A)
    T,U=F(1)-F(2,3)*c,F(5,3)-2*c
    delta=scale(mul(sub(C(T),X),sub(C(U),X)),F(9,16))
    lottery=4*c*rat_integral(power(delta,2),A,T)
    b0=(F(4,3),F(-1,3));areaF=(F(1,12),F(1,9));RF=(F(4,9),F(2,27))
    areaL=F(1,4)-F(1,2)*(1-b)**2
    menu0=value(G(C(a),C(a),C(b)),0)
    ig=integrate(mul(sub(ONE,X),G(C(A),C(A),X)),b0,(b,F()))
    ff=pmul(areaF,RF,F(2))
    low=(2*(ff[0]+ig[0]-areaL*menu0),2*(ff[1]+ig[1]))
    cut=integrate(scale(power(sub(C(b),C0),3),-F(4,3)),(d,F()),(q,F(1)),D)
    upper=2*rat_integral(mul(sub(ONE,X),sub(G(C(A),C(A),X),G(sub(X,C(c)),sub(X,C(c)),X))),b,A+c)
    coeffs=(base+high+lottery+low[0]+cut[0],low[1],cut[1])
    full=(coeffs[0]+upper,coeffs[1],coeffs[2])
    interval=bound(coeffs,(F(2),D));intervalH=bound(full,(F(2),D))
    assert upper>=0
    return dict(parameters=dict(a=str(a),b=str(b),c=str(c),q=str(q),split=str(a+d)),base=str(base),base_cells=records,
      high_correction=str(high),lottery_correction=str(lottery),low_pair=list(map(str,low)),capacity_cut_pair=list(map(str,cut)),
      upper_low_square_gain=str(upper),field_basis=['1','sqrt(2)','sqrt('+str(D)+')'],
      full_Q_coefficients=list(map(str,coeffs)),with_H_coefficients=list(map(str,full)),
      full_Q_interval=list(map(str,interval)),with_H_interval=list(map(str,intervalH)),
      scope='independent exact revenue of explicitly defined menu family; feasibility proved separately')

def main():
    data=calculate()
    path=ROOT/'certificate'/'independent_family_revenue.json'
    if '--write' in sys.argv:path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text(encoding='utf-8'))==data
    print('INDEPENDENT_FAMILY_CONTINUUM_REVENUE_PASS')
    print('full_Q_display',float(F(data['full_Q_interval'][0])))
    print('with_H_display',float(F(data['with_H_interval'][0])))
    print('base_cells',len(data['base_cells']))
if __name__=='__main__':main()
