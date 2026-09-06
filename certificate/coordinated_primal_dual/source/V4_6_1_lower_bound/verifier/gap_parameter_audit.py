"""Independent exact menu-interaction audit of the final rebuilt parameters.

This reconstructs the conditional menus independently, then compares the final
candidate implementation against those independently computed menus.
Finite regressions augment research_log/gap_parameter_audit.md; they do not
certify the continuum by themselves. Normal execution is read-only.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError("Run without -O.")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V4_6'/'verifier'))
import outer_bundle_exchange as inherited
v3 = inherited.v3
A,c,d = F(2,3),F(47,150),F(1,2)
a,b,s,q = A,A+c,A+d,d-c
T,U = 1-2*c/3,F(5,3)-2*c
B0 = inherited.B0
ZERO = (F(),F())


def kind(v):
    t,rho=max(v),min(v)
    if t<=A and sum(v)<=b:
        return 'Q'
    if A<t<T and rho<c:
        return 'Eplus'
    return 'base'


def lottery(t):
    delta=F(9,16)*(T-t)*(U-t)
    alpha=3*t-2
    beta=alpha/(alpha+2*delta)
    length=delta+alpha/2
    return delta,beta,length


def menu(opponent):
    x,y=opponent
    mode=kind(opponent)
    t,rho=max(opponent),min(opponent)
    high=0 if x>y else 1
    low=1-high
    units=((F(1),F()),(F(),F(1)))
    if mode=='Q':
        if t<=d:
            prices=(v3.Quad(),v3.asquad(A),v3.asquad(A),max(B0,v3.asquad(sum(opponent))))
        else:
            k=t-q;C=max(F(5,6)+F(3,4)*k*k,sum(opponent))
            z=[F(),F(),F(),C];z[1<<high]=A;z[1<<low]=C-k
            prices=tuple(map(v3.asquad,z))
        return [(ZERO,prices[0]),(units[0],prices[1]),(units[1],prices[2]),((F(1),F(1)),prices[3])]
    if mode=='Eplus':
        delta,beta,length=lottery(t)
        lot=[F(),F()];lot[high]=F(1);lot[low]=beta
        return [(ZERO,v3.Quad()),(units[low],v3.asquad(d+delta)),
                (units[high],v3.asquad(t)),((F(1),F(1)),v3.asquad(t+c+delta)),
                (tuple(lot),v3.asquad(t+beta*c))]
    H=max(F(),x-A,y-A,x+y-b)
    prices=(F(),H+min(A,s-y),H+min(A,s-x),H+b)
    return [(ZERO,v3.asquad(prices[0])),(units[0],v3.asquad(prices[1])),
            (units[1],v3.asquad(prices[2])),((F(1),F(1)),v3.asquad(prices[3]))]


def maximizers(own,opponent):
    rows=menu(opponent)
    values=[sum((x*y for x,y in zip(own,allocation)),F())-price for allocation,price in rows]
    best=max(values)
    assert best>=0
    if best==0:
        return [(ZERO,v3.Quad())]
    return [row for row,value in zip(rows,values) if value==best]


def feasible(left,right):
    return all(left[0][j]+right[0][j]<=1 for j in (0,1))


def calculate():
    assert (a,b,s,q,T,U)==(F(2,3),F(49,50),F(7,6),F(14,75),F(178,225),F(26,25))
    assert 0<q<c<d<A<T<1
    delta_A=F(9,16)*(T-A)*(U-A)
    assert d<d+delta_A<A
    assert A-q>c
    # delta decreases and Y increases on the entire [A,T] interval.
    assert F(9,16)*(2*T-T-U)<0
    assert F(9,16)*(2*A-T-U)+F(3,2)>0
    assert c+(3*T-2)/2==d
    assert 1-T/2>d
    assert 0<b-A<d and B0<b<F(4,3)
    assert F(1,3)-F(3,2)*(F(4,3)-b)**2>0
    # Parameter substitution in the full randomized Eplus certificate is an
    # exact polynomial identity, not an assumption that old numerical values persist.
    add,mul,scale,Q,X=inherited.add,inherited.mul,inherited.scale,inherited.Q,inherited.X
    delta=scale(mul(add(Q(T),scale(X,-1)),add(Q(U),scale(X,-1))),F(9,16))
    CC=add(X,Q(c),delta);JJ=add(Q(1),scale(X,F(-1,2)));KK=add(X,Q(-q))
    mean_f=add(scale(CC,3*A),scale(JJ,-3*A),scale(mul(JJ,JJ),F(3,2)),
               scale(mul(KK,KK),F(-3,2)),Q(-1))
    assert all(coefficient==0 for coefficient in mean_f.values())
    sink_lower=q*(1-F(3,2)*q)
    assert sink_lower>0
    tiny=F(1,100000)
    points={(F(),F()),(F(1),F(1)),(A,c),(c,A),(A,A),(d,d),
            (d,b-d),(b-d,d),(F(7,10),c),(F(7,10),c-tiny),
            (T,c/2),(T-tiny,c/2),(A,c-tiny),(A+tiny,c-tiny),
            (A+tiny,c),(F(1),c),(c,F(1))}
    for t in (d,d+tiny,F(3,5),A,A+tiny,F(7,10),(A+T)/2,T-tiny,T):
        for rho in (F(),c/2,c-tiny,c,c+tiny):
            points.add((t,rho));points.add((rho,t))
        if t<=A:
            for total in (b-tiny,b,b+tiny):
                rho=total-t
                if 0<=rho<=1:
                    points.add((t,rho));points.add((rho,t))
    for t in (F(7,10),(A+T)/2,T-tiny):
        delta,beta,length=lottery(t)
        Y=c+length
        for y in (c,c+length/2,Y,d):
            x=t-beta*(y-c)
            for shift in (-tiny,F(),tiny):
                if 0<=x+shift<=1:
                    points.add((x+shift,y));points.add((y,x+shift))
    points=sorted(points)
    counts={};profiles=0;joint_ties=0
    for own,opponent in product(points,repeat=2):
        key='/'.join(sorted((kind(own),kind(opponent))))
        left,right=maximizers(own,opponent),maximizers(opponent,own)
        compatible=[(a,b) for a in left for b in right if feasible(a,b)]
        assert compatible,(own,opponent,left,right)
        # Only base/base or Q/Q needs coordinated positive-tie selection.
        if key not in ('Q/Q','base/base'):
            assert len(compatible)==len(left)*len(right),(own,opponent,key)
        if len(left)*len(right)>1:
            joint_ties+=1
        counts[key]=counts.get(key,0)+1
        profiles+=1
    # Direct source comparison is separate from the independent reconstruction.
    sys.path.insert(0,str(ROOT/'verifier'))
    import parameter_candidate as actual
    source_menu_cases=0
    for opponent in points:
        candidate_rows,branch=actual.menu(opponent)
        reconstructed=menu(opponent)
        assert len(candidate_rows)==len(reconstructed)
        for allocation,price in reconstructed:
            assert any(allocation==aa and price==pp for pp,aa,tag in candidate_rows)
        source_menu_cases+=1
    source_profile_cases=0
    for i,own in enumerate(points):
        for shift in (0,1,17,37,97):
            opponent=points[(i+shift)%len(points)]
            row=actual.mechanism(own+opponent)
            for bidder,(v,w) in enumerate(((own,opponent),(opponent,own))):
                assert any(row['allocations'][bidder]==aa and row['payments'][bidder]==pp
                           for aa,pp in maximizers(v,w))
            assert all(row['allocations'][0][j]+row['allocations'][1][j]<=1 for j in (0,1))
            source_profile_cases+=1
    trace_cases=0
    # Actual selected sets: every menu maximizer must occupy the priced item.
    for t,rho in ((F(7,10),F(1,10)),((A+T)/2,c-tiny),(A+tiny,F())):
        fixed=t,rho;k=t-q
        for own in ((k/2,F(1)),(k-tiny,F(1)),((A+t)/2,c)):
            choices=maximizers(fixed,own)
            assert all(row[0][0]==1 for row in choices)
            trace_cases+=1
    for t in (d+tiny,F(3,5),A):
        k=t-q;fixed=t,F()
        for own in ((k/2,F(1)),(k-tiny,F(1))):
            assert all(row[0][0]==1 for row in maximizers(fixed,own))
            trace_cases+=1
    return dict(status='GAP_REBUILT_INTERACTION_AUDIT_EXACT_PASS',
                parameters={name:str(value) for name,value in dict(a=a,b=b,c=c,s=s,q=q,T=T,U=U).items()},
                independently_reconstructed_menu_types=len(points),profile_cases=profiles,
                cases_by_region_pair=counts,positive_argmax_tie_profiles=joint_ties,
                occupied_top_and_junction_cases=trace_cases,
                independent_candidate_menu_comparisons=source_menu_cases,
                independent_candidate_profile_comparisons=source_profile_cases,
                E_certificate_mean_f_polynomial='identically zero',
                E_certificate_uniform_sink_lower=str(sink_lower),
                scope='Exact named-profile and menu-interaction audit only; all-real proof is in the linked note',
                proof='research_log/gap_parameter_audit.md')


def verify():
    data=calculate()
    path=ROOT/'certificate/gap_parameter_audit.json'
    if '--write' in sys.argv:
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads(path.read_text(encoding='utf-8'))==data
    print(data['status'])
    print('profiles',data['profile_cases'])
    print('types',data['independently_reconstructed_menu_types'])
    print('ties',data['positive_argmax_tie_profiles'])
    return data

if __name__=='__main__':
    verify()
