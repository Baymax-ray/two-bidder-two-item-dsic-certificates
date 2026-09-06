"""Independent all-real structure audit with exact exceptional-report replay.

Menus, generalized inverse and ties are reconstructed without importing the
new candidate. Source comparison is performed only after reconstruction.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O')
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V3/verifier'))
import joined_threshold as old
A,d,c,eta,u=F(2,3),F(1,2),F(157,500),F(4,5),F(3421,10000)
q=d-c;nu=(1-2*c)**2/8;a=A+nu;b=a+c;s=a+d;T=1-2*c/3;U=F(5,3)-2*c
B0=old.Quad(F(4,3),-F(1,3),2)
ZERO=(F(),F());UNITS=((F(1),F()),(F(),F(1)))

def fee(x):return eta*(u-x) if c<=x<=u else F()
def h(x):return x+q+fee(x)
def inverse(t):
    if t<=d:return t-q
    if t<=h(c):return c
    if t<h(u):return (t-q-eta*u)/(1-eta)
    return t-q

def kind(w):
    t,rho=max(w),min(w)
    if t<=A and sum(w)<=b:return 'Q_free' if t<=d else 'Q_constrained'
    if A<t<T and rho<c:return 'E'
    return 'base'

def menu(w):
    t,rho=max(w),min(w);hi=0 if w[0]>w[1] else 1;lo=1-hi;mode=kind(w)
    if mode=='Q_free':
        prices=(0,A,A,max(B0,old.asquad(sum(w))))
        return [(ZERO,old.asquad(prices[0])),(UNITS[0],old.asquad(prices[1])),(UNITS[1],old.asquad(prices[2])),((F(1),F(1)),old.asquad(prices[3]))]
    if mode=='Q_constrained':
        k=inverse(t);C=max(F(5,6)+F(3,4)*k*k,sum(w),k+h(rho));B=min(A,C-k)
        return [(ZERO,old.asquad(0)),(UNITS[lo],old.asquad(B)),(UNITS[hi],old.asquad(A)),((F(1),F(1)),old.asquad(C))]
    if mode=='E':
        delta=F(9,16)*(T-t)*(U-t);alpha=3*t-2;beta=alpha/(alpha+2*delta)
        lottery=list(UNITS[hi]);lottery[lo]=beta
        return [(ZERO,old.asquad(0)),(UNITS[lo],old.asquad(d+delta)),(UNITS[hi],old.asquad(t)),((F(1),F(1)),old.asquad(t+c+delta)),(tuple(lottery),old.asquad(t+beta*c))]
    pivot=max(F(),w[0]-a,w[1]-a,sum(w)-b)
    ps=[F(),pivot+min(a,s-w[1]),pivot+min(a,s-w[0]),pivot+b]
    ps[1<<lo]+=fee(rho);ps[3]+=fee(rho)
    return [(ZERO,old.asquad(ps[0])),(UNITS[0],old.asquad(ps[1])),(UNITS[1],old.asquad(ps[2])),((F(1),F(1)),old.asquad(ps[3]))]

def argmax(v,w):
    rows=menu(w);values=[sum((x*y for x,y in zip(v,z)),F())-p for z,p in rows];maximum=max(values)
    assert maximum>=0
    return [rows[0]] if maximum==0 else [r for r,z in zip(rows,values) if z==maximum]

def compatible(left,right):return all(left[0][j]+right[0][j]<=1 for j in (0,1))

def polynomial_add(*ps):
    result={}
    for p in ps:
      for i,v in p.items():result[i]=result.get(i,F())+v
    return {i:v for i,v in result.items() if v}
def scale(p,z):return {i:v*z for i,v in p.items() if v*z}
def multiply(p,r):
    result={}
    for i,v in p.items():
      for j,w in r.items():result[i+j]=result.get(i+j,F())+v*w
    return {i:v for i,v in result.items() if v}

def calculate(compare_source=True):
    K=A-q;rho_star=b-A;B=lambda x:F(5,6)+F(3,4)*x*x-x
    slack=B(K)-h(rho_star)
    assert (a,b,q)==(F(1025947,1500000),F(1496947,1500000),F(93,500))
    assert d<a and b<1 and 0<q<c<rho_star<u<K<d<A<T<1
    assert d<h(c)<h(u)<A and h(c)==F(6531,12500) and h(u)==F(5281,10000)
    assert slack==F(37,5000000)>0 and eta-F(3,2)*K==F(79,1000)>0
    assert B(c)-d-fee(c)==F(212401,3000000)>0
    assert F(3,2)*c-1+eta>0 and d<B(K)<=B(c)<A
    assert F(5,6)+F(3,4)*c*c>B0
    # Exact polynomial identity behind the generic E full-inner support.
    X={1:F(1)};Q=lambda z:{0:F(z)}
    delta=scale(multiply(polynomial_add(Q(T),scale(X,-1)),polynomial_add(Q(U),scale(X,-1))),F(9,16))
    C=polynomial_add(X,Q(c),delta);j=polynomial_add(Q(1),scale(X,-F(1,2)));k=polynomial_add(X,Q(-q))
    mean=polynomial_add(scale(C,3*A),scale(j,-3*A),scale(multiply(j,j),F(3,2)),scale(multiply(k,k),-F(3,2)),Q(-1))
    assert not mean and q*(1-F(3,2)*q)>0
    assert nu==q*q/2 and nu==2*(F(3,4)*q*q)/3
    eps=F(1,1000000)
    for t in (d,d+eps,(d+h(c))/2,h(c),h(c)+eps,(h(c)+h(u))/2,h(u),h(u)+eps,A):
        kk=inverse(t)
        assert h(kk)>=t
        if t>d:assert h(kk-eps)<t
    types={(F(),F()),(F(1),F(1)),(A,c),(A,b-A),(d,b-d),(d,F()),(c,d),(h(c),c),(h(u),u),
       (h(c),rho_star),(A,c-eps),(a,c-eps),((A+T)/2,F(1,10)),((A+T)/2,c-eps),((A+T)/2,c),
       (T,c/2),(F(1),c),(F(1),u),(F(1),c-eps),(F(1),d),(F(9,10),F(4,5)),(F(7,10),F(2,5)),
       (F(3,5),d),(d,d),(u,u),(c,c)}
    for v in list(types):types.add(tuple(reversed(v)))
    types=sorted(types);cache={(v,w):argmax(v,w) for v,w in product(types,repeat=2)}
    counts={};ties=0
    for v,w in product(types,repeat=2):
        left,right=cache[v,w],cache[w,v]
        assert any(compatible(x,y) for x,y in product(left,right)),(v,w,left,right)
        key='/'.join(sorted((kind(v).split('_')[0],kind(w).split('_')[0])))
        counts[key]=counts.get(key,0)+1;ties+=int(len(left)*len(right)>1)
    traces={'Q_top':0,'Q_anchor':0,'E_top':0,'E_rectangle':0,'E_vacant_face':0};capped=0
    for t in (d+eps,(d+h(c))/2,h(c),h(c)+eps,h(u),A):
      kk=inverse(t)
      for rho in (F(),c,rho_star,b-t):
        if not 0<=rho<=t:continue
        w=(t,rho);C=max(F(5,6)+F(3,4)*kk*kk,sum(w));assert C>=kk+h(rho)
        if C-kk>A:
            assert C==sum(w)>B0;capped+=1
        for x in (kk/2,kk-eps):
            assert all(z[0][0]==1 for z in argmax(w,(x,F(1))));traces['Q_top']+=1
        if C>F(5,6)+F(3,4)*kk*kk:
            for v in ((F(1,4),F()),(d,(C-d)/2),(d,C-d-eps)):
                assert all(z[0]==(1,1) for z in argmax(w,v));traces['Q_anchor']+=1
    for t in ((A+a)/2,a,(a+T)/2):
      w=(t,c/2);kk=t-q
      for x in (c-eps,c,c+eps,u,kk-eps):
        assert x<kk and all(z[0][0]==1 for z in argmax(w,(x,F(1))));traces['E_top']+=1
      for x in ((2*A+t)/3,(A+2*t)/3):
        for y in (c/3,c-eps):
            assert all(z[0][0]==1 for z in argmax(w,(x,y)));traces['E_rectangle']+=1
    t=(A+a)/2;x=(A+t)/2
    assert all(z[0][0]==0 for z in argmax((t,c/2),(x,c)));traces['E_vacant_face']+=1
    source_menus=source_profiles=0
    if compare_source:
      sys.path.insert(0,str(ROOT/'verifier'))
      import refined_candidate as actual
      for w in types:
        source=actual.menu(w);source=source[0] if isinstance(source,tuple) and len(source)==2 and isinstance(source[1],str) else source
        reconstructed=menu(w)
        assert len(source)==len(reconstructed)
        for alloc,price in reconstructed:
          assert any(alloc==row[1] and price==row[0] for row in source),(w,source,reconstructed)
        source_menus+=1
      for idx,v in enumerate(types):
       for shift in (0,1,7,19):
        w=types[(idx+shift)%len(types)];row=actual.mechanism(v+w)
        for ii,(vv,ww) in enumerate(((v,w),(w,v))):
          assert any(row['allocations'][ii]==z and row['payments'][ii]==price for z,price in argmax(vv,ww))
        assert all(sum(row['allocations'][ii][jj] for ii in (0,1))<=1 for jj in (0,1));source_profiles+=1
    return dict(status='REFINED_STRUCTURE_FULL_CONTINUUM_AUDIT_PASS',
      scope='Complete all-real joint feasibility and full randomized conditional Q/E optimality for this exact candidate; no global capacity supergradient or auction optimum',
      extra_floor_slack=str(slack),inverse_plateau=[str(d),str(h(c))],inverse_affine_image=[str(h(c)),str(h(u))],
      support_endpoint_price=str(h(u)),reserve_allowance=str(nu),
      independent_menu_types=len(types),independent_profile_cases=len(types)**2,region_pair_counts=counts,positive_tie_profiles=ties,
      occupied_trace_cases=traces,capped_conditional_cases=capped,source_menu_comparisons=source_menus,source_profile_comparisons=source_profiles,
      proof='research_log/refined_structure_audit.md',
      important_distinction='E junction allocation is forced by DSIC and open-rectangle capacity, even where literal junction residual is positive')

if __name__=='__main__':
    data=calculate('--independent-only' not in sys.argv)
    if '--independent-only' not in sys.argv:
      target=ROOT/'certificate/refined_structure_audit.json'
      if '--write' in sys.argv:target.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
      else:assert json.loads(target.read_text(encoding='utf-8'))==data
    print(data['status']);print('profiles',data['independent_profile_cases']);print('source_profiles',data['source_profile_comparisons'])
