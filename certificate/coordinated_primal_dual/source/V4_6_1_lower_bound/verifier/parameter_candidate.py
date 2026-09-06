"""Complete exact rational-report evaluator for the rebuilt symmetric family.

The formulas also specify all real reports; their pointwise mathematical
feasibility proof is parameter_rebuilt_family.md and the independent audit.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json,random,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V3'/'verifier'))
import joined_threshold as v3
A=F(2,3);a=A;c=F(47,150);b=A+c;s=F(7,6);d=F(1,2);q=d-c
T=1-2*c/3;U=F(5,3)-2*c
B0=v3.Quad(F(4,3),-F(1,3),2)
MASKS=((0,0),(1,0),(0,1),(1,1))

def menu(opponent):
    x,y=tuple(opponent);t=max(x,y);rho=min(x,y);z=x+y
    if t<=A and z<=b:
        if t<=d:
            C=max(B0,v3.asquad(z));return tuple((v3.asquad(p),v,tag) for p,v,tag in ((0,(0,0),'empty'),(A,(1,0),'item1'),(A,(0,1),'item2'),(C,(1,1),'bundle'))),'Q_free'
        k=t-q;C=max(F(5,6)+F(3,4)*k*k,z);B=C-k
        hi=0 if x>y else 1
        scarce=tuple(F(j==hi) for j in (0,1));safe=tuple(1-j for j in scarce)
        return ((v3.asquad(0),(F(0),F(0)),'empty'),(v3.asquad(B),safe,'safe'),(v3.asquad(A),scarce,'scarce'),(v3.asquad(C),(F(1),F(1)),'bundle')),'Q_constrained'
    if A<t<T and rho<c:
        hi=0 if x>y else 1
        scarce=tuple(F(j==hi) for j in (0,1));safe=tuple(1-j for j in scarce)
        dl=F(9,16)*(T-t)*(U-t);alpha=3*t-2;beta=alpha/(alpha+2*dl)
        lot=tuple(F(1) if j==hi else beta for j in (0,1))
        return ((v3.asquad(0),(F(0),F(0)),'empty'),(v3.asquad(d+dl),safe,'safe'),(v3.asquad(t),scarce,'scarce'),(v3.asquad(t+c+dl),(F(1),F(1)),'bundle'),(v3.asquad(t+beta*c),lot,'lottery')),'E_lottery'
    H=max(0,x-a,y-a,x+y-b)
    ps=(0,H+min(a,s-y),H+min(a,s-x),H+b)
    return tuple((v3.asquad(p),tuple(map(F,v)),f'base_{j}') for j,(p,v) in enumerate(zip(ps,MASKS))),'base'

def mechanism(profile):
    profile=tuple(map(F,profile));assert len(profile)==4 and all(0<=z<=1 for z in profile)
    own=(profile[:2],profile[2:]);menus=[];branches=[];argmax=[];utilities=[]
    for i in (0,1):
        rows,branch=menu(own[1-i]);vals=[sum((v*z for v,z in zip(own[i],alloc)),F())-p for p,alloc,tag in rows]
        u=max(vals);choices=[j for j,val in enumerate(vals) if val==u]
        if u==0:choices=[0]
        menus.append(rows);branches.append(branch);argmax.append(choices);utilities.append(u)
    pair=None
    for i,j in product(*argmax):
        if all(menus[0][i][1][k]+menus[1][j][1][k]<=1 for k in (0,1)):
            pair=(i,j);break
    assert pair is not None,('pointwise feasible maximizer missing',profile,branches,argmax)
    selected=[menus[i][pair[i]] for i in (0,1)]
    return {'profile':profile,'allocations':tuple(row[1] for row in selected),'payments':tuple(row[0] for row in selected),'utilities':tuple(utilities),'branches':tuple(branches),'selected':tuple(row[2] for row in selected),'menus':tuple(menus)}

def verify():
    # Structural interval inequalities used by the all-real proof.
    k0,k1=c,A-q
    assert 0<q<c<d<A<T<1 and b==A+c<1
    assert F(5,6)+F(3,4)*k1*k1-k1>d
    assert k1<A and F(5,6)+F(3,4)*c*c > B0
    assert F(5,6)+F(3,4)*k1*k1>=A+c
    checks=0
    rng=random.Random(461)
    for _ in range(2500):
        mechanism(tuple(F(rng.randrange(1001),1000) for j in range(4)));checks+=1
    nodes=(F(0),c,d,A,T,F(1))
    for profile in product(nodes,repeat=4):
        mechanism(profile);checks+=1
    # Q sum faces, diagonal ties, E corner line and lottery indifference.
    eps=F(1,1000000)
    for t in (d,d+eps,F(3,5),A,A+eps,F(7,10),T-eps,T):
        for rho in (F(0),c-eps,c,c+eps,b-t):
            if not 0<=rho<=t:continue
            op=(t,rho)
            for xx in (c,t-q,A,t,F(1)):
                for yy in (F(0),c,d,b-xx,F(1)):
                    if 0<=xx<=1 and 0<=yy<=1:
                        for prof in ((t,rho,xx,yy),(xx,yy,t,rho),(rho,t,yy,xx)):
                            mechanism(prof);checks+=1
    data={'status':'PARAMETER_CANDIDATE_POINTWISE_REPLAY_PASS','bounded_profile_checks':checks,
      'all_real_proof':'research_log/parameter_rebuilt_family.md; independent gap-agent audit',
      'tie_rule':'empty at zero utility; otherwise lexicographically first jointly feasible pair among full menu argmax rows',
      'menu_structures':['affine base','symmetric full-Q screening with bundle competition','five-option E lottery'],
      'removed_from_definition':['inherited fee boxes','square-root joined branch','F/G wrappers','corner corrections'],
      'parameters':{name:str(value) for name,value in dict(a=a,b=b,c=c,s=s,d=d,q=q,A=A,T=T,U=U).items()}}
    path=ROOT/'certificate/parameter_candidate.json'
    if '--write' in sys.argv:path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text(encoding='utf-8'))==data
    print(data['status']);print('checks',checks)
    return data
if __name__=='__main__':
    if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O')
    verify()
