"""Selected V4.6.1.1 mechanism: reserve change, jump exchange, and Q cap.

Exact rational-report implementation. The displayed formulas and the
independent structural proof specify every real report, including ties.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json,random,sys,importlib.util
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V3/verifier'))
import joined_threshold as qd
A=F(2,3);d=F(1,2);c=F(157,500)
nu=(1-2*c)**2/8;a=A+nu;b=a+c;s=a+d;q=d-c
slope=F(4,5);u=F(3421,10000);jump=slope*(u-c)
T=1-F(2,3)*c;U=F(5,3)-2*c
B0=qd.Quad(F(4,3),-F(1,3),2)
MASKS=((0,0),(1,0),(0,1),(1,1))

def g(x):return slope*(u-x) if c<=x<=u else F()
def h(x):return x+q+g(x)
def inverse(t):
    if t<=d:return t-q
    if t<=d+jump:return c
    if t<u+q:return (t-q-slope*u)/(1-slope)
    return t-q

def menu(opponent):
    x,y=map(F,opponent);t=max(x,y);rho=min(x,y);z=x+y
    if t<=A and z<=b:
        if t<=d:
            C=max(B0,qd.asquad(z))
            return tuple((qd.asquad(p),tuple(map(F,v)),tag) for p,v,tag in
                ((0,(0,0),'empty'),(A,(1,0),'item1'),(A,(0,1),'item2'),(C,(1,1),'bundle'))),'Q_free'
        k=inverse(t);C=max(F(5,6)+F(3,4)*k*k,z,k+h(rho));B=min(A,C-k)
        hi=0 if x>y else 1;scarce=tuple(F(j==hi) for j in (0,1));safe=tuple(1-z for z in scarce)
        rows=((0,(F(),F()),'empty'),(B,safe,'safe'),(A,scarce,'scarce'),(C,(F(1),F(1)),'bundle'))
        return tuple((qd.asquad(p),v,tag) for p,v,tag in rows),'Q_capped' if C-k>A else 'Q_constrained'
    if A<t<T and rho<c:
        hi=0 if x>y else 1;scarce=tuple(F(j==hi) for j in (0,1));safe=tuple(1-z for z in scarce)
        delta=F(9,16)*(T-t)*(U-t);alpha=3*t-2;beta=alpha/(alpha+2*delta)
        lot=tuple(F(1) if j==hi else beta for j in (0,1))
        rows=((0,(F(),F()),'empty'),(d+delta,safe,'safe'),(t,scarce,'scarce'),
              (t+c+delta,(F(1),F(1)),'bundle'),(t+beta*c,lot,'lottery'))
        return tuple((qd.asquad(p),v,tag) for p,v,tag in rows),'E'
    H=max(0,x-a,y-a,z-b)
    prices=[F(),H+min(a,s-y),H+min(a,s-x),H+b]
    fee=g(rho)
    if fee:
        prices[1 if x<y else 2]+=fee;prices[3]+=fee
    return tuple((qd.asquad(p),tuple(map(F,v)),f'base_{j}') for j,(p,v) in enumerate(zip(prices,MASKS))),'base_fee' if fee else 'base'

def mechanism(profile):
    own=tuple(map(F,profile));assert len(own)==4 and all(0<=x<=1 for x in own)
    types=(own[:2],own[2:]);menus=[];argmax=[];utilities=[];branches=[]
    for i in (0,1):
        rows,branch=menu(types[1-i]);values=[sum((v*x for v,x in zip(types[i],alloc)),F())-p for p,alloc,tag in rows]
        utility=max(values);choices=[j for j,v in enumerate(values) if v==utility] if utility!=0 else [0]
        menus.append(rows);argmax.append(choices);utilities.append(utility);branches.append(branch)
    pair=next(((i,j) for i,j in product(*argmax) if all(menus[0][i][1][k]+menus[1][j][1][k]<=1 for k in (0,1))),None)
    assert pair is not None,('no feasible pair of maximizing options',own,branches,argmax)
    selected=[menus[i][pair[i]] for i in (0,1)]
    return dict(profile=own,allocations=tuple(row[1] for row in selected),payments=tuple(row[0] for row in selected),
        utilities=tuple(utilities),branches=tuple(branches),selected=tuple(row[2] for row in selected),menus=tuple(menus))

def verify():
    assert a==F(1025947,1500000) and b==F(1496947,1500000)
    assert d<A<a<T<1 and c<c+nu<u<d and b<1 and 0<q<c
    assert jump==F(281,12500) and 1-slope==F(1,5)
    m=c+nu;B=lambda x:F(5,6)+F(3,4)*x*x-x
    slack=B(A-q)-m-q-g(m)
    assert slack==F(37,5000000)>0
    assert B(A-q)>d and B(c)<A
    assert F(5,6)+F(3,4)*u*u<b and B(c)>d+jump
    assert slope>F(3,2)*(b-m-q)
    for x in (c,(c+u)/2,u,F(2,5)):
        assert inverse(h(x))==x
    for t in (d+F(1,100000),d+jump/2,d+jump):assert inverse(t)==c
    # Interior witness: old split becomes a bundle, with strict choices.
    sys.path.insert(0,str(ROOT.parent/'V4_6_1_lower_bound/verifier'))
    spec=importlib.util.spec_from_file_location('preserved_v461_exchange',ROOT.parent/'V4_6_1_lower_bound/verifier/functional_exchange.py')
    previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)
    witness=(F(103,200),F(1,10),F(63,200),F(99,100))
    old=previous.mechanism(witness);new=mechanism(witness)
    assert old['allocations']==((F(1),F()),(F(),F(1)))
    assert new['allocations']==((F(),F()),(F(1),F(1)))
    # Each box remains within the same strict allocation branches.
    radius=F(1,100000)
    t0,r0,x0,y0=witness
    assert d<t0-radius<t0+radius<d+jump
    assert c<x0-radius<x0+radius<previous.L
    assert x0+radius+previous.q<t0-radius
    assert h(x0-radius)>t0+radius
    assert previous.hinv(t0-radius)>x0+radius
    assert y0-radius>A and r0+radius<min(c,previous.c)
    assert t0+r0+2*radius<B0
    for signs in product((-1,1),repeat=4):
        point=tuple(x+sg*radius for x,sg in zip(witness,signs))
        assert previous.mechanism(point)['allocations']==old['allocations']
        assert mechanism(point)['allocations']==new['allocations']
    rng=random.Random(4611);count=0
    for _ in range(1500):
        mechanism(tuple(F(rng.randrange(10001),10000) for _ in range(4)));count+=1
    nodes=(F(),c,c+nu,u,d,A,a,T,F(1))
    for profile in product(nodes,repeat=4):mechanism(profile);count+=1
    for t in (d,d+F(1,100000),d+jump,d+jump+F(1,100000),h(m),u+q,A,a,T):
        for rho in (F(1,10),c,m,u,b-t):
            if not 0<=rho<=t:continue
            k=inverse(t)
            for x in (c,k,A,a,F(1)):
                for y in (c,d,A,F(1)):
                    mechanism((t,rho,x,y));count+=1
    out=dict(status='REFINED_POINTWISE_CANDIDATE_PASS',parameters={key:str(val) for key,val in
        dict(a=a,A=A,b=b,c=c,d=d,q=q,s=s,T=T,U=U,slope=slope,endpoint=u,jump=jump,nu=nu).items()},
        bounded_profile_checks=count,extra_floor_uniform_slack=str(slack),
        witness=list(map(str,witness)),old_witness_allocations=[[str(x) for x in row] for row in old['allocations']],
        new_witness_allocations=[[str(x) for x in row] for row in new['allocations']],
        witness_box_corner_checks=16,tie_rule='empty at zero; lexicographically first feasible full-menu maximizing pair',
        scope='Finite implementation replay; all-real proof and exact revenue verified separately')
    path=ROOT/'certificate/refined_candidate.json'
    if '--write' in sys.argv:path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text(encoding='utf-8'))==out
    print(out['status']);print('profile_checks',count);print('uniform_floor_slack',slack)
    return out
if __name__=='__main__':
    if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
    verify()
