"""Independent pointwise and conditional-support audit of the positive tent.

Uses affine knot interpolation for h and its inverse and reconstructs menus
independently of functional_exchange. Finite tests augment the all-real note.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError("Run without -O.")
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verifier'))
import gap_parameter_audit as clean
import importlib.util
sys.path.insert(0,str(ROOT/'verifier'))
_spec=importlib.util.spec_from_file_location('functional_candidate_audit_target',ROOT/'verifier/functional_exchange.py')
actual=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(actual)
A,c,b,d,q=clean.A,clean.c,clean.b,clean.d,clean.q
L,M,U=F(8,25),F(33,100),F(17,50)
EPS=F(1,1000)
ZERO=clean.ZERO


def interpolate(x,x0,x1,y0,y1):
    return y0+(x-x0)*(y1-y0)/(x1-x0)


def graph(epsilon):
    return ((L,L+q),(M,M+q+epsilon),(U,U+q))


def forward(x,epsilon):
    knots=graph(epsilon)
    if x<=L or x>=U:
        return x+q
    left,right=(knots[0],knots[1]) if x<=M else (knots[1],knots[2])
    return interpolate(x,left[0],right[0],left[1],right[1])


def inverse(t,epsilon):
    knots=graph(epsilon)
    if t<=knots[0][1] or t>=knots[-1][1]:
        return t-q
    left,right=(knots[0],knots[1]) if t<=knots[1][1] else (knots[1],knots[2])
    return interpolate(t,left[1],right[1],left[0],right[0])


def rows(opponent,epsilon):
    x,y=opponent;t,rho=max(opponent),min(opponent)
    branch=clean.kind(opponent)
    if branch=='Q' and t>d:
        k=inverse(t,epsilon)
        C=max(F(5,6)+F(3,4)*k*k,sum(opponent),k+forward(rho,epsilon))
        high=0 if x>y else 1
        prices=[F(),F(),F(),C]
        prices[1<<high]=A;prices[1<<(1-high)]=C-k
        return [(tuple(F(bool(mask&(1<<j))) for j in (0,1)),clean.v3.asquad(price))
                for mask,price in enumerate(prices)]
    out=clean.menu(opponent)
    if branch=='base' and L<rho<U:
        low=0 if x<y else 1
        safe=tuple(F(j==low) for j in (0,1))
        fee=forward(rho,epsilon)-rho-q
        out=[(allocation,price+(fee if allocation in (safe,(1,1)) else 0))
             for allocation,price in out]
    return out


def choices(own,menu):
    values=[sum((x*y for x,y in zip(own,allocation)),F())-price for allocation,price in menu]
    best=max(values)
    assert best>=0
    if best==0:
        return [(ZERO,clean.v3.Quad())]
    return [row for row,value in zip(menu,values) if value==best]


def verify():
    tiny=F(1,100000)
    assert c<L<M<U<d and U+q<A
    assert F(1)-EPS/(U-M)==F(9,10)>0
    kk=b-U-q
    slack=F(5,6)+F(3,4)*kk*kk-kk-U-q
    assert slack==F(14,1875)>EPS
    assert L+q-c>0 # strict discounted-base inequality P-(C-B)>0
    statistics=[]
    for epsilon in (F(),EPS/2,EPS):
        points={(F(),F()),(F(1),F(1)),(A,c),(c,A),(d,d),
                (clean.T,c),(c,clean.T),(A+tiny,c),(A,c+tiny)}
        for x in (F(),c,L,L+tiny,(L+M)/2,M,(M+U)/2,U-tiny,U,F(1)):
            assert inverse(forward(x,epsilon),epsilon)==x
            assert forward(x,epsilon)==actual.h(x,epsilon)
        ts=(d,d+tiny,L+q,M+q,M+q+epsilon,U+q,F(3,5),A,F(7,10),clean.T)
        for t in ts:
            for rho in (F(),c,L,M,U,b-t):
                if 0<=rho<=t:
                    points.add((t,rho));points.add((rho,t))
            if d<t<=A:
                k=inverse(t,epsilon)
                for x in (k-tiny,k,k+tiny):
                    points.add((x,F(1)));points.add((F(1),x))
        for r in (L,L+tiny,M,U-tiny,U):
            t=(b-r+1)/2
            P=t+r-c;B=r+q;C=t+r;fee=forward(r,epsilon)-r-q
            assert C-B<P
            for own in ((C-B-tiny,B+fee/2),(P+tiny,c-tiny),
                        (C-B+tiny,B+fee+tiny)):
                points.add(own);points.add(tuple(reversed(own)))
            points.add((t,r));points.add((r,t))
        points=sorted(points)
        menus={op:rows(op,epsilon) for op in points}
        source_menu_cases=0
        for opponent in points:
            published,branch=actual.menu(opponent,epsilon)
            reconstructed=menus[opponent]
            assert len(published)==len(reconstructed)
            for allocation,price in reconstructed:
                assert any(allocation==aa and price==pp for pp,aa,tag in published)
            source_menu_cases+=1
        profiles=ties=0;counts={}
        for own,opponent in product(points,repeat=2):
            left,right=choices(own,menus[opponent]),choices(opponent,menus[own])
            assert any(clean.feasible(a,z) for a in left for z in right),(epsilon,own,opponent,left,right)
            key='/'.join(sorted((clean.kind(own),clean.kind(opponent))))
            counts[key]=counts.get(key,0)+1
            ties+=len(left)*len(right)>1
            profiles+=1
        source_profiles=0
        for i,own in enumerate(points):
            for shift in (1,37,97):
                opponent=points[(i+shift)%len(points)]
                result=actual.mechanism(own+opponent,epsilon)
                for bidder,(v,w) in enumerate(((own,opponent),(opponent,own))):
                    assert any(result['allocations'][bidder]==aa and result['payments'][bidder]==pp
                               for aa,pp in choices(v,menus[w]))
                assert all(result['allocations'][0][j]+result['allocations'][1][j]<=1 for j in (0,1))
                source_profiles+=1
        trace_cases=0
        for t in (d+tiny,L+q,M+q+epsilon,U+q,F(3,5),A):
            k=inverse(t,epsilon)
            fixed=(t,F())
            for x in (k/2,k-tiny):
                selected=choices(fixed,rows((x,F(1)),epsilon))
                assert all(row[0][0]==1 for row in selected)
                trace_cases+=1
        for t in (A+tiny,F(7,10),clean.T-tiny):
            fixed=(t,c-tiny);k=t-q
            for report in ((L,F(1)),(M,F(1)),(U,F(1)),(k-tiny,F(1)),((A+t)/2,c)):
                selected=choices(fixed,rows(report,epsilon))
                assert all(row[0][0]==1 for row in selected)
                trace_cases+=1
        for t in (L+q,M+q+epsilon,U+q):
            k=inverse(t,epsilon);C0=F(5,6)+F(3,4)*k*k;z=(C0+b)/2
            fixed=(t,z-t)
            assert clean.kind(fixed)=='Q' and max(fixed)==t and z>C0
            for report in ((F(1,4),F()),(d,(z-d)/2),(d,z-d-tiny)):
                selected=choices(fixed,rows(report,epsilon))
                assert all(row[0]==(1,1) for row in selected)
                trace_cases+=1
        statistics.append(dict(epsilon=str(epsilon),independent_types=len(points),
                               independent_profile_pairs=profiles,region_pair_counts=counts,
                               positive_argmax_tie_profiles=ties,
                               source_menu_comparisons=source_menu_cases,
                               source_profile_comparisons=source_profiles,
                               occupied_top_junction_anchor_cases=trace_cases))
    data=dict(status='FUNCTIONAL_GAP_AUDIT_EXACT_PASS',
              uniform_extra_floor_slack=str(slack),epsilon_statistics=statistics,
              total_profile_pairs=sum(z['independent_profile_pairs'] for z in statistics),
              scope='Pointwise implementation audit; all-real feasibility and full conditional Q/E certificate extension in note',
              full_conditional_gap_map='Both bidders: zero unrestricted conditional gap on all Q and Eplus for actual functional residual',
              excluded_claims=['optimal outer allocation','optimal h','unrestricted auction optimum'],
              proof='research_log/functional_gap_audit.md')
    path=ROOT/'certificate/functional_gap_audit.json'
    if '--write' in sys.argv:
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads(path.read_text(encoding='utf-8'))==data
    print(data['status'])
    print('independent_profile_pairs',data['total_profile_pairs'])
    print('occupied_trace_cases',sum(z['occupied_top_junction_anchor_cases'] for z in statistics))
    return data

if __name__=='__main__':
    verify()
