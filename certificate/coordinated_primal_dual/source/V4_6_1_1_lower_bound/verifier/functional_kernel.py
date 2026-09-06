"""Exact coupled opportunity-cost kernel and its admissible pointwise optimizer."""
from fractions import Fraction as F
from pathlib import Path
from math import comb
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V4_6_1_lower_bound'/'verifier'))
import parameter_revenue as old
P,X,I=old.P,old.X,old.I
a,c,b,d,q,A=old.a,old.c,old.b,old.d,old.q,old.A
C0=P(F(5,6))+F(3,4)*X*X
RI=P(F(59,108))+F(1,4)*X*X-X**3+F(9,16)*X**4
RP=F(1,2)*X-3*X*X+F(9,4)*X**3
th=1+c-X;ll=b-X
J1=(1-a)*(1-2*c+F(3,2)*q*q-F(3,2)*(X-c)**2-F(3,2)*(q+X-c)*(th+ll))
J2=F(3,2)*(1-th)-(1-th*th)-2*X*(1-th)+F(1,2)*((1-q)**3-(th-q)**3)
AA=4*(-(b-X-q)*RP-F(3,2)*X*(b-C0)**2+J1+J2)
BB=4*(1-b+X)-2*RP
SS=P(F(5,6))+F(3,4)*(b-X-q)**2-(b-X-q)-X-q
END=F(43,125);V=F(69,200);SLOPE=F(3,4)
GG=SLOPE*(END-X)

def ev(p,x):return sum((co*x**j for j,co in enumerate(P(p).c)),F())
def derivative(p):return P(tuple(F(i)*co for i,co in enumerate(P(p).c))[1:])
def bernstein(p,l,r):
    p=P(p);n=len(p.c)-1;power=[F() for _ in range(n+1)]
    for j,co in enumerate(p.c):
        for k in range(j+1):power[k]+=co*comb(j,k)*l**(j-k)*(r-l)**k
    return [sum((power[j]*F(comb(i,j),comb(n,j)) for j in range(i+1)),F()) for i in range(n+1)]
def kappa_bracket(steps=120):
    lo,hi=c,V
    assert ev(AA,lo)>0>ev(AA,hi)
    for _ in range(steps):
        mid=(lo+hi)/2
        if ev(AA,mid)>0:lo=mid
        else:hi=mid
    return lo,hi

def calculate():
    assert AA.c==tuple(map(F,['315889/1687500','227/3750','69/25','-791/50','9','-27/8']))
    assert BB.c==tuple(map(F,['2/25','3','6','-9/2']))
    assert SS.c==tuple(map(F,['9761/30000','-119/100','3/4']))
    signs={name:bernstein(poly,c,V) for name,poly in {
      'B_positive':BB,'S_positive':SS,'A_strictly_decreasing':-derivative(AA),
      'pointwise_optimum_below_slack':2*BB*SS-AA,
      'pointwise_h_strictly_increasing':2*BB*BB+derivative(AA)*BB-AA*derivative(BB)}.items()}
    assert all(min(vals)>0 for vals in signs.values())
    assert min(bernstein(SS-GG,c,END))==F(47,15000)>0
    assert ev(GG,c)==F(23,1000)
    assert ev(C0,V)<b and ev(C0,c)>V+q+ev(SS,c)
    gain=(AA*GG-BB*GG*GG).integral(c,END)
    assert gain==F(2982529415201233,369140625000000000000)
    prior_gain=F(68161978301,216000000000000000)
    assert gain-prior_gain>F(77,10000000)
    kap=kappa_bracket();assert END<kap[0]<kap[1]<F(172083,500000)
    err=AA-2*BB*GG;Bmin=min(signs['B_positive']);Bmax=max(signs['B_positive'])
    norm=(err*err).integral(c,END)
    gap_lo=norm/(4*Bmax)
    gap_hi=norm/(4*Bmin)+(F(172083,500000)-END)*ev(AA,END)**2/(4*Bmin)
    assert 0<gap_lo<gap_hi<F(535,10**12)
    coeff=(F(482935538268336599,574087500000000000)+gain,F(31,1215),-F(170368,664453125))
    rv=I(coeff[0])+coeff[1]*old.square(2)+coeff[2]*old.square(11)
    data={'status':'FUNCTIONAL_KERNEL_EXACT_PASS','scope':'Complete coupled revenue functional; g-star optimizes this explicitly sufficient capacity family only',
      'A_coefficients':list(map(str,AA.c)),'B_coefficients':list(map(str,BB.c)),'slack_coefficients':list(map(str,SS.c)),
      'bernstein_positive_coefficients':{name:list(map(str,vals)) for name,vals in signs.items()},
      'affine_jump':{'support':[str(c),str(END)],'slope':str(SLOPE),'jump_height':str(ev(GG,c)),'slack_minimum':'47/15000','exact_gain_over_clean':str(gain),'exact_gain_over_V4_6_1':str(gain-prior_gain)},
      'affine_revenue_coefficients_basis_1_sqrt2_sqrt11':list(map(str,coeff)),
      'affine_revenue_interval':old.tools.rounded_interval(rv,28),
      'kappa_unique_root_bracket':list(map(str,kap)),
      'gstar_definition':'A(x)/(2B(x)) on closed [c,kappa], zero elsewhere, right jump at c',
      'gstar_exact_revenue_increment':'integral_c^kappa A(x)^2/(4B(x)) dx',
      'gstar_minus_affine_interval':list(map(str,(gap_lo,gap_hi))),
      'not_claimed':['full auction optimum','optimality outside the explicitly sufficient h family']}
    path=ROOT/'certificate/functional_kernel.json'
    if '--write' in sys.argv:path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text(encoding='utf-8'))==data
    print(data['status']);print('affine_gain',float(gain));print('affine_revenue',data['affine_revenue_interval']);print('star_advantage_bounds',[float(gap_lo),float(gap_hi)])
    return data
if __name__=='__main__':
    if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O')
    calculate()
