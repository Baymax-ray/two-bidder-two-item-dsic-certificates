"""Independent complete continuum revenue audit of the refined capped candidate.

Uses Green boundary integration and direct conditional-menu areas. Does not
import or call constant_kernel or refined_candidate as a revenue calculator.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V4_6_1_lower_bound'/'verifier'))
import parameter_revenue as algebra
P,X,BP,TT,RR=algebra.P,algebra.X,algebra.BP,algebra.TT,algebra.RR
A=F(2,3);c=F(157,500);d=F(1,2);q=d-c
a=F(1025947,1500000);b=a+c;s=a+d
m=b-A;u=F(3421,10000);slope=F(4,5);jump=slope*(u-c)
T=1-2*c/3;U=F(5,3)-2*c
rb=F(4,3)*(b-F(5,6))

def G(A,B,C):
    return A*(1-A)*(C-A)+B*(1-B)*(C-B)+C*((1-C+B)*(1-C+A)-(A+B-C)**2*F(1,2))
def ev(p,x):return sum((co*x**j for j,co in enumerate(P(p).c)),F())
def pint(p,lo,hi):return P(p).integral(F(lo),F(hi))
def pmul(x,y,D):return (x[0]*y[0]+D*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def padd(x,y):return (x[0]+y[0],x[1]+y[1])
def pscale(x,z):return(x[0]*z,x[1]*z)
def field_integral(p,lo,hi,D):
    pp=P((F(),)+tuple(co/F(j+1) for j,co in enumerate(P(p).c)))
    def at(v):
        ans=(F(),F())
        for co in reversed(pp.c):ans=padd(pmul(ans,v,D),(co,F()))
        return ans
    return padd(at(hi),pscale(at(lo),-1))

def base_revenue():
    total=area=F();count=0
    for H,cond in ((BP(0),(a-TT,b-TT-RR)),(TT-a,(TT-a,c-RR)),(TT+RR-b,(TT+RR-b,RR-c))):
        for lt in (True,False):
            for lr in (True,False):
                pa=H+(a if lr else s-RR);pb=H+(a if lt else s-TT);pc=H+b
                for status in range(3):
                    poly=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1))]
                    fs=list(cond)+[d-TT if lt else TT-d,d-RR if lr else RR-d]
                    if status==0:fs.extend((1-pa,1-pb));rev=G(pa,pb,pc)
                    elif status==1:
                        fs.extend((pa-1,1-pb));k=pc-pb
                        rev=pb*k*(1-pb)+pc*((1-k)*(1-pb)+(1-k)**2/2)
                    else:fs.extend((pa-1,pb-1));rev=pc*(2-pc)**2/2
                    for f in fs:
                        if poly:poly=algebra.clip(poly,f)
                    ar=algebra.pintegral(1,poly)
                    assert ar>=0
                    if ar:area+=ar;total+=algebra.pintegral(rev,poly);count+=1
    assert area==F(1,2)
    return 4*total,count

def root_inverse(t):
    if t<=d:return t-q
    if t<=d+jump:return c
    if t<u+q:return (t-q-slope*u)/(1-slope)
    return t-q

def menu_area(rows):
    ans=F()
    for aa,p in rows:
        poly=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]
        for bb,pp in rows:
            if poly:poly=algebra.clip(poly,(aa[0]-bb[0])*TT+(aa[1]-bb[1])*RR+pp-p)
        ans+=p*algebra.pintegral(1,poly)
    return ans

def area_checks():
    checks=0
    for t in (F(503,1000),F(51,100),d+jump,F(53,100),F(3,5),A):
        for r in (c,m,u,b-t):
            if not 0<=r<=min(t,b-t):continue
            k=root_inverse(t);cc0=F(5,6)+F(3,4)*k*k
            hh=r+q+(slope*(u-r) if c<=r<=u else 0)
            C=max(cc0,t+r,k+hh);assert C==max(cc0,t+r)
            B=min(A,C-k)
            rows=(((0,0),F(0)),((1,0),A),((0,1),B),((1,1),C))
            actual=menu_area(rows);assert actual==G(A,B,C)
            Ri=F(59,108)+k*k/4-k**3+F(9,16)*k**4
            hhcap=max(F(),C-k-A)
            assert actual==Ri-(C-cc0)**2+F(3,2)*k*hhcap*hhcap+hhcap**3/2
            checks+=1
    for t in ((A+a)/2,a,F(7,10),T-F(1,1000)):
        dl=F(9,16)*(T-t)*(U-t);beta=(3*t-2)/(3*t-2+2*dl)
        rows=(((0,0),F()),((0,1),d+dl),((1,0),t),((1,1),t+c+dl),((1,beta),t+beta*c))
        assert menu_area(rows)==G(t,d,t+c)+dl*dl;checks+=1
    for r in (c,(c+m)/2,m,(m+u)/2,u):
        gg=slope*(u-r)
        for t in (A,(A+b-r)/2,b-r,1+c-r,F(1)):
            if not t>=r or (t<=A and t+r<=b):continue
            H=max(F(),t-a,t+r-b)
            pa=H+a;pb=H+s-t;pc=H+b
            old=menu_area((((0,0),F()),((1,0),pa),((0,1),pb),((1,1),pc)))
            new=menu_area((((0,0),F()),((1,0),pa),((0,1),pb+gg),((1,1),pc+gg)))
            if pa<=1:gamma=1-2*pc+2*pa+F(3,2)*(pc-pb)**2-F(3,2)*pa*pa
            else:gamma=F(3,2)-2*pc+F(3,2)*(pc-pb)**2
            assert new-old==gamma*gg-gg*gg;checks+=1
    return checks

def calculate():
    assert a==A+(1-2*c)**2/8 and c<m<u<d<A<a<T<1
    assert m==F(165649,500000) and jump==F(281,12500)
    # C>=k+h(rho) is redundant; its smallest sufficient slack is at rho=m.
    ka=A-q;Bka=F(5,6)+F(3,4)*ka*ka-ka
    slack=Bka-(m+q+slope*(u-m))
    assert slack==F(37,5000000)>0 and slope-F(3,2)*ka>0
    assert ev(P(F(5,6))+F(3,4)*X*X,u)<b
    assert rb==F(246947,1125000) and u*u<rb<ka*ka
    base,cells=base_revenue()
    C0=P(F(5,6))+F(3,4)*X*X
    Ri=P(F(59,108))+F(1,4)*X*X-X**3+F(9,16)*X**4
    Z=G(P(a),P(s)-X,P(b));Bs=G(X,P(d),X+c)
    J=F(1,2)*X*(m-X)**3+F(1,8)*(m-X)**4
    gx=slope*(u-X);hx=X+q+gx;hp=1-slope
    ic=ev(Ri,c);dc=b-ev(C0,c)
    plateau=ic*((b-d)*jump-jump*jump/2)-jump*dc**3/3+jump*ev(J,c)
    curve=hp*pint((b-hx)*Ri-(b-C0)**3*F(1,3),c,u)+hp*pint(J,c,m)
    unchanged=pint((b-q-X)*Ri,u,ka)
    tail=pscale(field_integral((b-C0)**3,(u,F()),(F(),F(1)),rb),-F(1,3))
    baseQ=pint((b-X)*Z,d,A)
    qfinal=padd((4*(plateau+curve+unchanged-baseQ),F()),pscale(tail,4))
    # Independently integrate the complete clean capped menu for comparison.
    qclean=padd((4*(pint((b-q-X)*Ri,c,ka)+pint(J,c,m)-baseQ),F()),pscale(field_integral((b-C0)**3,(c,F()),(F(),F(1)),rb),-F(4,3)))
    rf=(F(4,9),F(2,27));b0=(F(4,3),-F(1,3));areaL=F(1,4)-(1-b)**2/2
    qlow=pscale(padd(rf,(-G(a,a,b),F())),2*areaL)
    qlow=padd(qlow,pscale(field_integral((1-X)*G(P(A),P(A),X),b0,(b,F()),2),2))
    qlow=padd(qlow,pscale(pmul(rf,field_integral(1-X,b0,(b,F()),2),2),-2))
    dl=F(9,16)*(T-X)*(U-X)
    elot=4*c*pint(dl*dl,A,T)
    ebase=4*c*pint(Bs-Z,A,a)
    # Ordinary bundle-pivot base region, integrated directly in low report x.
    th=1+c-X;ll=b-X
    j1=(1-a)*(1-2*c+F(3,2)*q*q-F(3,2)*(X-c)**2-F(3,2)*(q+X-c)*(th+ll))
    j2=F(3,2)*(1-th)-(1-th*th)-2*X*(1-th)+F(1,2)*((1-q)**3-(th-q)**3)
    base_main=4*pint(gx*(j1+j2)-gx*gx*(1-b+X),c,u)
    # Additional zero-pivot rows exist because a>A.
    zint=(1-2*c-F(3,2)*a*a)*(m-X)+F(1,2)*((b-X-q)**3-(A-q)**3)
    base_extra=4*pint(gx*zint-gx*gx*(m-X),c,m)
    final=(base+qfinal[0]+qlow[0]+elot+ebase+base_main+base_extra,qlow[1],qfinal[1])
    clean=(base+qclean[0]+qlow[0]+elot+ebase,qlow[1],qclean[1])
    assert final[1:]==clean[1:]
    gain=final[0]-clean[0]
    expected=F(12679344561540434503009375151,1575000000000000000000000000000000)
    assert gain==expected
    rv=algebra.I(final[0])+final[1]*algebra.tools.sqrt_interval(2,60)+final[2]*algebra.tools.sqrt_interval(rb,60)
    rc=algebra.I(clean[0])+clean[1]*algebra.tools.sqrt_interval(2,60)+clean[2]*algebra.tools.sqrt_interval(rb,60)
    qcap=4*(jump*ev(J,c)+hp*pint(J,c,m))
    qcap_clean=4*pint(J,c,m)
    data={'status':'REFINED_CONTINUOUS_REVENUE_AUDIT_PASS','scope':'Independent direct integration of all continuous conditional menus, including capped safe price, jump plateau, and a>A strips; not an unrestricted upper bound',
      'parameters':{k:str(v) for k,v in dict(a=a,b=b,c=c,s=s,q=q,A=A,d=d,m=m,u=u,slope=slope,jump=jump).items()},
      'base_exact':str(base),'base_positive_area_cells':cells,'base_ordered_area':'1/2','conditional_polygon_checks':area_checks(),
      'extra_capacity_max_slack':str(slack),'radicand':str(rb),
      'exact_revenue_coefficients_basis_1_sqrt2_sqrt_radicand':list(map(str,final)),
      'exact_clean_coefficients_same_basis':list(map(str,clean)),
      'exact_gain_over_clean':str(gain),'revenue_interval':algebra.tools.rounded_interval(rv,30),'clean_revenue_interval':algebra.tools.rounded_interval(rc,30),
      'audit_components':{k:str(v) for k,v in dict(Q_jump_plateau_single_ordered=plateau,Q_slope_single_ordered=curve,Q_unchanged_Ri_single_ordered=unchanged,E_lottery=elot,E_missing_base_correction=ebase,base_functional_main=base_main,base_missing_strip=base_extra,Q_cap_total=qcap,Q_cap_clean=qcap_clean,Q_cap_gain=qcap-qcap_clean).items()},
      'independence':'No constant_kernel/refined_candidate calculator imported; base Green polygon integration and direct Q t/rho decomposition, including inverse plateau.',
      'proof':'research_log/refined_revenue_audit.md'}
    path=ROOT/'certificate/refined_revenue_audit.json'
    if '--write' in sys.argv:path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text(encoding='utf-8'))==data
    print(data['status']);print('revenue',data['revenue_interval']);print('gain',gain,float(gain));print('menu_area_checks',data['conditional_polygon_checks']);return data
if __name__=='__main__':
    if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O')
    calculate()
