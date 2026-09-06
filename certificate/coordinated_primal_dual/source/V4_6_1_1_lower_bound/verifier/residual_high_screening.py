"""Exact all-randomized screening identity and actual high-base residual audit.

Continuous polygon/line integration checks the analytic identity for diverse
complete competing menus. Actual profiles are bounded implementation checks.
Normal replay is read-only. --write saves this phase certificate only.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError("Run without -O.")
ROOT=Path(__file__).resolve().parents[1]
SQUARE=[(F(),F()),(F(1),F()),(F(1),F(1)),(F(),F(1))]


def clip(poly,ax,ay,const):
    out=[]
    for left,right in zip(poly,poly[1:]+poly[:1]):
        fl=ax*left[0]+ay*left[1]+const
        fr=ax*right[0]+ay*right[1]+const
        if fl>=0:
            out.append(left)
        if (fl<0<fr) or (fr<0<fl):
            t=fl/(fl-fr)
            out.append(tuple(left[j]+t*(right[j]-left[j]) for j in (0,1)))
    return out


def moments(poly):
    area=mx=my=F()
    for left,right in zip(poly,poly[1:]+poly[:1]):
        det=left[0]*right[1]-left[1]*right[0]
        area+=det/2
        mx+=(left[0]+right[0])*det/6
        my+=(left[1]+right[1])*det/6
    assert area>=0
    return area,mx,my


def cells(menu):
    result=[]
    for i,(ax,ay,payment) in enumerate(menu):
        poly=SQUARE[:]
        for j,(bx,by,other) in enumerate(menu):
            if i==j:
                continue
            if (ax,ay,payment)==(bx,by,other) and j<i:
                poly=[]
                break
            poly=clip(poly,ax-bx,ay-by,other-payment)
        result.append(poly)
    assert sum((moments(poly)[0] for poly in result),F())==1
    return result


def line_weight(menu,k,p):
    affine=[(ay,ax*k-payment) for ax,ay,payment in menu]
    knots={p,F(1)}
    for a,b in affine:
        for c,d in affine:
            if a!=c:
                y=(d-b)/(a-c)
                if p<y<1:
                    knots.add(y)
    knots=sorted(knots)
    total=F()
    for lo,hi in zip(knots,knots[1:]):
        mid=(lo+hi)/2
        values=[a*mid+b for a,b in affine]
        index=values.index(max(values))
        total+=menu[index][1]*(hi-lo-(hi*hi-lo*lo)/2)
    return (3*k-1)*total/2


def certificate_integral(menu,k,p):
    z=k+p
    payment_revenue=volume=F()
    for (a1,a2,payment),poly in zip(menu,cells(menu)):
        area= moments(poly)[0]
        payment_revenue+=payment*area
        gp=clip(clip(poly,F(1),F(),-k),F(1),F(1),-z)
        ar,mx,my=moments(gp)
        volume+=a1*(3*mx-ar)/2+a2*(3*my-ar)/2
        hp=clip(clip(poly,F(-1),F(),k),F(),F(1),-p)
        ar,mx,my=moments(hp)
        volume+=a2*(3*my-2*ar)
    return payment_revenue,volume+line_weight(menu,k,p)


def value(k,p):
    z=k+p
    return p*k*(1-p)+z*((1-k)*(1-p)+(1-k)**2/2)


def support(a1,a2,k,p):
    z=k+p
    return max(a1+a2*(z-1),a1*k+a2*p)


def theorem_checks():
    pairs=((F(2,3),F(2,3)),(F(16,25),F(18,25)),(F(7,10),F(4,5)),
           (F(61,75),F(61,75)),(F(3,4),F(1)),(F(1),F(3,4)),(F(1),F(1)))
    tests=0;positive_slacks=0
    for k,p in pairs:
        assert F(1,3)<=k<=1 and F(2,3)<=p<=1 and k+p>=F(4,3)
        z=k+p
        candidate=[(F(),F(),F()),(F(),F(1),p),(F(1),F(1),z)]
        revenue,mass=certificate_integral(candidate,k,p)
        assert revenue==mass==value(k,p)
        allocations=((F(1,3),F(1)),(F(1),F(2,3)),(F(1,5),F(2,5)),
                     (F(4,5),F(1,4)),(F(1),F(1)))
        menus=[candidate,
               [(F(),F(),F()),(F(),F(1),p)],
               [(F(),F(),F()),(F(1),F(1),z+F(1,20))],
               [(F(),F(),F()),(F(),F(1),p+F(1,25)),(F(1),F(1),z+F(1,50))]]
        for fee in (F(),F(1,100),F(1,20)):
            menus.append([(F(),F(),F())]+[(a1,a2,support(a1,a2,k,p)+fee) for a1,a2 in allocations])
        for original in menus:
            for u0 in (F(),F(1,17)):
                menu=[(a1,a2,price-u0) for a1,a2,price in original]
                assert all(price+u0>=support(a1,a2,k,p) for a1,a2,price in menu)
                revenue,priced=certificate_integral(menu,k,p)
                assert revenue+u0==priced,(k,p,menu,revenue,priced)
                assert priced<=mass
                positive_slacks+=revenue<mass
                tests+=1
    return dict(continuous_menu_identity_checks=tests,strict_gap_examples=positive_slacks,
                parameter_pairs=[[str(k),str(p)] for k,p in pairs])


def load_preserved_candidate():
    path=ROOT.parent/'V4_6_1_lower_bound/verifier/functional_exchange.py'
    sys.path.insert(0,str(path.parent))
    spec=importlib.util.spec_from_file_location('residual_preserved_functional_candidate',path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module,path


def actual_checks():
    candidate,path=load_preserved_candidate()
    c,q,u=F(47,150),F(14,75),F(17,50)
    lower=1-q;z0=1+u;tiny=F(1,100000)
    no_sale=menu_cases=0
    for t in (lower,F(21,25),F(9,10),F(1)):
        for rho in (F(1,2),z0-t,F(7,10),lower,t):
            if not F(1,2)<=rho<=t or t+rho<z0:
                continue
            fixed=(t,rho);z=t+rho;p=min(rho+q,F(1));k=z-p
            points={(F(),F()),(F(1),F(1)),(k,p),(k/2,p/2),
                    (F(1),p/2),((k+1)/2,(z-(k+1)/2)/2)}
            for r in (candidate.L,candidate.M,candidate.U):
                points.add((F(1)-tiny,r));points.add((r,F(1)-tiny))
            for shift in (-tiny,F(),tiny):
                if 0<=k+shift<=1:
                    points.add((k+shift,(p+1)/2))
            for own in points:
                if not all(0<=v<=1 for v in own):
                    continue
                expected=max(F(),own[1]-p,sum(own)-z)
                for profile,bidder in ((own+fixed,0),(fixed+own,1)):
                    row=candidate.mechanism(profile)
                    assert row['utilities'][bidder]==expected
                    if all(0<v<1 for v in own) and own[1]<p and sum(own)<z:
                        assert row['allocations'][1-bidder]==(1,1),(fixed,own,row)
                        no_sale+=1
                    menu_cases+=1
    # Closed high-region edge can retain a free normal boundary marginal.
    fixed=(lower,lower);own=(F(1),candidate.M)
    edge=candidate.mechanism(own+fixed)
    assert edge['allocations']==((0,0),(0,1))
    assert sum(own)<sum(fixed)
    area=F(1,4)-c*c-(u-c)**2
    A=F(2,3);T=1-2*c/3
    covered=A*A-(A-c)**2/2+2*c*(T-A)+area
    assert area==F(34,225) and covered==F(82501,135000)
    return dict(source=str(path.relative_to(ROOT.parent)).replace('\\','/'),
                source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                complete_menu_profile_checks=menu_cases,strict_interior_bundle_cases=no_sale,
                boundary_exception=dict(profile=list(map(str,own+fixed)),
                                        allocations=[[str(x) for x in v] for v in edge['allocations']],
                                        meaning='Normal marginal may be free on the own-report edge; the theorem uses only no-sale interior'),
                high_region_area=str(area),total_certified_opponent_area=str(covered),
                broader_endpoint_43_over_125_area=str(F(1,4)-c*c-(F(43,125)-c)**2),
                actual_scope='Preserved V4.6.1 final functional mechanism; newer mechanisms require separate applicability verification')


def verify():
    data=dict(status='RESIDUAL_HIGH_SCREENING_EXACT_PASS',
              theorem=theorem_checks(),actual_residual=actual_checks(),
              identity='R+u0=integral_G(((3x-1)a1+(3y-1)a2)/2)+integral_H((3y-2)a2)+(3k-1)/2*integral_p^1((1-y)a2(k,y))',
              scope='Full randomized conditional optimum under an actual no-sale-interior capacity hole; no revenue gain or global auction upper claimed',
              proof='research_log/residual_high_screening.md')
    path=ROOT/'certificate/residual_high_screening.json'
    if '--write' in sys.argv:
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads(path.read_text(encoding='utf-8'))==data
    print(data['status'])
    print('continuous_identity_checks',data['theorem']['continuous_menu_identity_checks'])
    print('actual_profiles',data['actual_residual']['complete_menu_profile_checks'])
    print('high_region_area',data['actual_residual']['high_region_area'])
    return data

if __name__=='__main__':
    verify()
