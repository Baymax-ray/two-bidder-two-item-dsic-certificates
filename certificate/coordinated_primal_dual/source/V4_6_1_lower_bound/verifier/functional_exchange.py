"""Exact feasible positive functional exchange and scoped negative direction.

All-real proofs are in research_log/functional_exchange.md. No optimizer or
floating quadrature is used in this replay.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json,random,sys
import parameter_candidate as base
import parameter_revenue as calc
ROOT=Path(__file__).resolve().parents[1]
A,c,b,d,q=base.A,base.c,base.b,base.d,base.q
L,M,U=F(8,25),F(33,100),F(17,50)
EPS=F(1,1000)

def phi(x):
    if L<x<=M:return (x-L)/(M-L)
    if M<x<U:return (U-x)/(U-M)
    return F()
def h(x,epsilon=EPS):return x+q+epsilon*phi(x)
def hinv(t,epsilon=EPS):
    if t<=L+q or t>=U+q:return t-q
    if t<=M+q+epsilon:return (t-q+epsilon*L/(M-L))/(1+epsilon/(M-L))
    return (t-q-epsilon*U/(U-M))/(1-epsilon/(U-M))
def menu(opponent,epsilon=EPS):
    x,y=tuple(opponent);t=max(x,y);rho=min(x,y);zz=x+y
    rows,branch=base.menu(opponent)
    if branch=='Q_constrained':
        k=hinv(t,epsilon);C=max(F(5,6)+F(3,4)*k*k,zz,k+h(rho,epsilon));B=C-k
        hi=0 if x>y else 1
        scarce=tuple(F(j==hi) for j in (0,1));safe=tuple(1-j for j in scarce)
        return ((base.v3.asquad(0),(F(0),F(0)),'empty'),(base.v3.asquad(B),safe,'safe'),(base.v3.asquad(A),scarce,'scarce'),(base.v3.asquad(C),(F(1),F(1)),'bundle')),'Q_functional'
    if branch=='base' and phi(rho)>0:
        low=0 if x<y else 1;safe=tuple(F(j==low) for j in (0,1));fee=epsilon*phi(rho)
        rows=tuple((p+(fee if alloc==safe or alloc==(1,1) else 0),alloc,tag) for p,alloc,tag in rows)
        return rows,'base_functional'
    return rows,branch

def mechanism(profile,epsilon=EPS):
    profile=tuple(map(F,profile));assert len(profile)==4 and all(0<=z<=1 for z in profile);assert 0<=epsilon<=EPS
    own=(profile[:2],profile[2:]);menus=[];branches=[];argmax=[];utilities=[]
    for i in (0,1):
        rows,branch=menu(own[1-i],epsilon);vals=[sum((v*z for v,z in zip(own[i],alloc)),F())-p for p,alloc,tag in rows]
        u=max(vals);choices=[j for j,val in enumerate(vals) if val==u]
        if u==0:choices=[0]
        menus.append(rows);branches.append(branch);argmax.append(choices);utilities.append(u)
    pair=next(((i,j) for i,j in product(*argmax) if all(menus[0][i][1][k]+menus[1][j][1][k]<=1 for k in (0,1))),None)
    assert pair is not None,('functional feasible maximizer missing',profile,branches,argmax)
    selected=[menus[i][pair[i]] for i in (0,1)]
    return {'profile':profile,'allocations':tuple(row[1] for row in selected),'payments':tuple(row[0] for row in selected),'utilities':tuple(utilities),'branches':tuple(branches),'selected':tuple(row[2] for row in selected),'menus':tuple(menus)}

def variation_coefficients(lo,mid,hi):
    P,X,TT,RR=calc.P,calc.X,calc.TT,calc.RR
    C0=P(F(5,6))+F(3,4)*X*X;Rp=X*F(1,2)-3*X*X+F(9,4)*X**3
    dq=qb=bb=db=F()
    pq=-Rp*(b-q-X)-F(3,2)*X*(b-C0)**2
    gp=1-2*c+F(3,2)*(TT-q)**2-F(3,2)*(TT+RR-c)**2
    gh=F(3,2)-2*(TT+RR)+F(3,2)*(TT-q)**2
    for ll,hh,ph,phb in ((lo,mid,(X-lo)*F(1,mid-lo),(RR-lo)/(mid-lo)),(mid,hi,(hi-X)*F(1,hi-mid),(hi-RR)/(hi-mid))):
        dq+=4*calc.ratint(pq*ph,ll,hh);qb+=2*calc.ratint(ph*ph*Rp,ll,hh);bb-=4*calc.ratint(ph*ph*(1-b+X),ll,hh)
        p1=[(b-ll,ll),(1+c-ll,ll),(1+c-hh,hh),(b-hh,hh)]
        p2=[(1+c-ll,ll),(F(1),ll),(F(1),hh),(1+c-hh,hh)]
        db+=4*(calc.pintegral(phb*gp,p1)+calc.pintegral(phb*gh,p2))
    return dq,db,qb,bb

def verify():
    assert c<L<M<U<d and U-L==F(1,50)
    assert 1-EPS/(U-M)==F(9,10)>0
    kk=b-U-q;slack=F(5,6)+F(3,4)*kk*kk-kk-U-q
    assert slack==F(14,1875)>EPS
    assert F(5,6)+F(3,4)*U*U<b
    assert F(5,6)+F(3,4)*L*L>U+q
    for x in (F(0),c,L,(L+M)/2,M,(M+U)/2,U,F(1)):
        assert hinv(h(x))==x
    dq,db,qb,bb=variation_coefficients(L,M,U)
    D,H=dq+db,qb+bb
    assert D==F(70410824789,216000000000000)>0
    assert H==-F(31233979,3000000000)<0
    gain=D*EPS+H*EPS*EPS
    assert gain==F(68161978301,216000000000000000)>0
    assert D+2*H*EPS>0
    # The old higher tent has additional nonpositive Q max-constraint costs.
    ndq,ndb,_,_=variation_coefficients(F(17,50),F(9,25),F(19,50))
    nbound=ndq+ndb
    assert ndq==F(218153451,62500000000)
    assert ndb==-F(728239,168750000)
    assert nbound==-F(1392246823,1687500000000)<0
    checks=0;rng=random.Random(46171)
    for _ in range(3000):
        p=tuple(F(rng.randrange(1001),1000) for j in range(4));mechanism(p);checks+=1
    nodes=(c,L,M,U,d,A,F(1))
    for p in product(nodes,repeat=4):mechanism(p);checks+=1
    for t in (L+q,M+q,M+q+EPS,U+q,F(3,5),A):
        for rho in (L,M,U,b-t):
            if not 0<=rho<=t:continue
            k=hinv(t)
            for x in (k-F(1,100000),k,k+F(1,100000),A,F(1)):
                for y in (L,M,U,d,F(1)):
                    for p in ((t,rho,x,y),(x,y,t,rho),(rho,t,y,x)):
                        mechanism(p);checks+=1
    coeff=(F(482935538268336599,574087500000000000)+gain,F(31,1215),-F(170368,664453125))
    revenue=calc.I(coeff[0])+coeff[1]*calc.square(2)+coeff[2]*calc.square(11)
    data={'status':'FUNCTIONAL_EXCHANGE_EXACT_PASS','scope':'Complete positive functional candidate plus rejection of one different positive tent; no unrestricted optimality',
      'support':[str(L),str(M),str(U)],'epsilon':str(EPS),'slopes':[str(1+EPS/(M-L)),str(1-EPS/(U-M))],
      'capacity_repricing_slack':str(slack),'linear_coefficient':str(D),'quadratic_coefficient':str(H),'exact_gain':str(gain),
      'coefficient_components':{key:str(v) for key,v in dict(Q_linear=dq,base_linear=db,Q_quadratic=qb,base_quadratic=bb).items()},
      'exact_gain_decimal_display':float(gain),'radical_coefficients_basis_1_sqrt2_sqrt11':list(map(str,coeff)),
      'revenue_interval':calc.tools.rounded_interval(revenue,28),'pointwise_profile_checks':checks,
      'negative_tent':{'support':['17/50','9/25','19/50'],'right_derivative_upper_bound':str(nbound),'claim':'This positive tent is locally unprofitable; this does not rule out other h directions.'},
      'proof':'research_log/functional_exchange.md'}
    path=ROOT/'certificate/functional_exchange.json'
    if '--write' in sys.argv:path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text(encoding='utf-8'))==data
    print(data['status']);print('gain',gain,float(gain));print('revenue',[float(F(v)) for v in data['revenue_interval']]);print('checks',checks)
    return data
if __name__=='__main__':
    if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O')
    verify()
