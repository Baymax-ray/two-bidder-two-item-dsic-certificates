"""Complete affine jump/plateau mechanism; exact rational reports and ties."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json,random,sys
import functional_kernel as K
sys.path.insert(0,str(K.ROOT.parent/'V4_6_1_lower_bound'/'verifier'))
import parameter_candidate as base
ROOT=Path(__file__).resolve().parents[1]
c,q,A,b=K.c,K.q,K.A,K.b
END,SLOPE=K.END,K.SLOPE
G=F(23,1000)

def g(x):return SLOPE*(END-x) if c<=x<=END else F()
def h(x):return x+q+g(x)
def hinv(t):
    if t<=c+q:return t-q
    if t<=c+q+G:return c
    if t<END+q:return (t-q-SLOPE*END)/(1-SLOPE)
    return t-q

def menu(opponent):
    x,y=tuple(opponent);t=max(x,y);rho=min(x,y);zz=x+y
    rows,branch=base.menu(opponent)
    if branch=='Q_constrained':
        k=hinv(t);C=max(F(5,6)+F(3,4)*k*k,zz,k+h(rho));B=C-k
        assert C==max(F(5,6)+F(3,4)*k*k,zz)
        hi=0 if x>y else 1;scarce=tuple(F(j==hi) for j in (0,1));safe=tuple(1-j for j in scarce)
        return ((base.v3.asquad(0),(F(0),F(0)),'empty'),(base.v3.asquad(B),safe,'safe'),(base.v3.asquad(A),scarce,'scarce'),(base.v3.asquad(C),(F(1),F(1)),'bundle')),'Q_plateau' if t<=c+q+G else 'Q_exchange'
    if branch=='base' and g(rho)>0:
        low=0 if x<y else 1;safe=tuple(F(j==low) for j in (0,1));fee=g(rho)
        rows=tuple((p+(fee if alloc==safe or alloc==(1,1) else 0),alloc,tag) for p,alloc,tag in rows)
        return rows,'base_exchange'
    return rows,branch

def select(profile,menu_function=menu):
    profile=tuple(map(F,profile));assert len(profile)==4 and all(0<=z<=1 for z in profile)
    own=(profile[:2],profile[2:]);menus=[];branches=[];argmax=[];utilities=[]
    for i in (0,1):
        rows,branch=menu_function(own[1-i]);vals=[sum((v*z for v,z in zip(own[i],alloc)),F())-p for p,alloc,tag in rows]
        u=max(vals);choices=[j for j,val in enumerate(vals) if val==u]
        if u==0:choices=[0]
        menus.append(rows);branches.append(branch);argmax.append(choices);utilities.append(u)
    pair=next(((i,j) for i,j in product(*argmax) if all(menus[0][i][1][k]+menus[1][j][1][k]<=1 for k in (0,1))),None)
    assert pair is not None,('joint feasible maximizer missing',profile,branches,argmax)
    selected=[menus[i][pair[i]] for i in (0,1)]
    return {'profile':profile,'allocations':tuple(row[1] for row in selected),'payments':tuple(row[0] for row in selected),'utilities':tuple(utilities),'branches':tuple(branches),'selected':tuple(row[2] for row in selected),'menus':tuple(menus)}
def mechanism(profile):return select(profile)

def verify():
    checks=0;rng=random.Random(46111)
    for _ in range(2500):mechanism(tuple(F(rng.randrange(1001),1000) for j in range(4)));checks+=1
    nodes=(c-F(1,10000),c,c+F(1,10000),END,F(1,2),A,F(1))
    for p in product(nodes,repeat=4):mechanism(p);checks+=1
    for t in (F(1,2),F(1,2)+G/2,F(1,2)+G,F(1,2)+G+F(1,10000),END+q,A):
        for rho in (F(0),c-F(1,10000),c,c+F(1,10000),END,b-t):
            if not 0<=rho<=t:continue
            k=hinv(t)
            for x in (k-F(1,10000),k,k+F(1,10000),A,F(1)):
                for y in (F(0),c,F(1,2),F(1)):
                    for p in ((t,rho,x,y),(x,y,t,rho),(rho,t,y,x)):
                        mechanism(p);checks+=1
    witness=(F(103,200),F(1,10),c+F(1,1000),F(1))
    import functional_exchange as previous
    old,new=previous.mechanism(witness),mechanism(witness)
    assert old['allocations']==((1,0),(0,1)) and new['allocations']==((0,0),(1,1))
    # The closed c face is essential: the base safe price includes g(c).
    face=(F(103,200),F(1,10),c,F(1))
    r=mechanism(face);assert r['allocations'][0]==(0,0)
    data={'status':'FUNCTIONAL_JUMP_POINTWISE_PASS','scope':'All-real mechanism specified in functional_jump.md; rational regression is additional evidence',
      'bounded_profile_checks':checks,'support':[str(c),str(END)],'jump_height':str(G),'plateau_t_interval':[str(F(1,2)),str(F(1,2)+G)],
      'slope_of_h_after_jump':'1/4','tie_rule':'empty at zero; lexicographically first jointly feasible complete-menu argmax pair',
      'closed_c_face':'base safe and bundle fees include g(c)>0',
      'strict_transfer_witness':{'profile':list(map(str,witness)),'old_allocation':[[str(x) for x in a] for a in old['allocations']],'new_allocation':[[str(x) for x in a] for a in new['allocations']]}}
    path=ROOT/'certificate/functional_jump.json'
    if '--write' in sys.argv:path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text(encoding='utf-8'))==data
    print(data['status']);print('checks',checks);return data
if __name__=='__main__':
    if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O')
    verify()
