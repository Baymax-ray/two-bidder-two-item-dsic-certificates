"""Exact screening identity and frozen-candidate wing residual replay.

The proof covers all continuous randomized DSIC/IR competitors. The finite
menus below independently check its continuous integral identity; actual
profile checks only replay the frozen implementation. Default is read-only.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from residual_high_screening import clip,moments,cells,value,support


def certificate_integral(menu,k,p):
    revenue=priced=first_strip_mass=F()
    for (a1,a2,payment),poly in zip(menu,cells(menu)):
        revenue+=payment*moments(poly)[0]
        strip=clip(poly,F(-1),F(),k)
        first_strip_mass+=a1*moments(strip)[0]
        gp=clip(clip(poly,F(1),F(),-k),F(1),F(1),-k-p)
        ar,mx,my=moments(gp)
        priced+=a1*(3*mx-ar)/2+a2*(3*my-ar)/2
        hp=clip(strip,F(),F(1),-p)
        ar,mx,my=moments(hp)
        priced+=a2*((3*k+1)*my-(k+1)*ar)/(2*k)
    return revenue,priced,first_strip_mass


def theorem_checks():
    pairs=((F(407,500),F(5281,10000)),(F(4,5),F(11,20)),
           (F(3,4),F(3,5)),(F(2,3),F(2,3)),
           (F(7,10),F(4,5)),(F(2,5),F(1)),(F(1),F(1)))
    tests=positive_slacks=0
    allocations=((F(1,3),F(1)),(F(1),F(2,3)),(F(1,5),F(2,5)),
                 (F(4,5),F(1,4)),(F(1),F(1)))
    for k,p in pairs:
        assert F(1,3)<=k<=1 and F()<p<=1 and k+p>=F(4,3)
        assert (3*k+1)*p>=k+1
        candidate=[(F(),F(),F()),(F(),F(1),p),(F(1),F(1),k+p)]
        revenue,mass,strip=certificate_integral(candidate,k,p)
        assert revenue==mass==value(k,p) and strip==0
        menus=[candidate,[(F(),F(),F()),(F(),F(1),p)],
               [(F(),F(),F()),(F(1),F(1),k+1+F(1,20))]]
        for safe_tax in (F(),F(1,100),F(1,20)):
            for fee in (F(),F(1,100),F(1,20)):
                # The safe option dominates first-positive lotteries at x<k.
                rows=[(a1,a2,max(support(a1,a2,k,p),a1*k+a2*(p+safe_tax))+fee)
                      for a1,a2 in allocations]
                menus.append([(F(),F(),F()),(F(),F(1),p+safe_tax)]+rows)
        for original in menus:
            for u0 in (F(),F(1,17)):
                menu=[(a1,a2,payment-u0) for a1,a2,payment in original]
                assert all(payment+u0>=support(a1,a2,k,p)
                           for a1,a2,payment in menu)
                revenue,priced,firstmass=certificate_integral(menu,k,p)
                assert firstmass==0
                assert revenue+u0==priced,(k,p,menu,revenue,priced)
                assert priced<=mass
                positive_slacks+=revenue<mass
                tests+=1
    return dict(continuous_menu_identity_checks=tests,strict_gap_examples=positive_slacks,
                parameter_pairs=[[str(k),str(p)] for k,p in pairs])


def load_candidate():
    path=ROOT/'verifier/refined_candidate.py'
    spec=importlib.util.spec_from_file_location('residual_frozen_refined_candidate',path)
    candidate=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(candidate)
    return candidate,path


def actual_checks():
    candidate,path=load_candidate()
    a,c,q,u=candidate.a,candidate.c,candidate.q,candidate.u
    lower=1-q;z0=1+u;tiny=F(1,100000)
    assert c==F(157,500) and u==F(3421,10000)
    assert candidate.b+candidate.jump<z0
    assert a+candidate.jump<lower and u+q<lower
    assert z0>=F(4,3) and u<=2*c
    margin=(4-3*q)*(u+q)-(2-q)
    assert margin==F(18601,5000000)>0
    area=2*q*(1-q-u)
    assert area==F(438867,2500000)
    cases=strip_cases=hole_cases=left_cases=0
    opponents=set()
    for t in (lower,F(21,25),F(9,10),F(99,100),F(1)):
        for rho in (u,z0-t,(z0-t+t)/2,F(1,2),lower,t):
            if 0<=rho<=t and t+rho>=z0:
                opponents.add((t,rho))
    for fixed in sorted(opponents):
        t,rho=fixed;z=t+rho;p=min(rho+q,F(1));k=z-p
        assert k>=F(1,3) and (3*k+1)*p>=k+1
        points={(F(),F()),(F(1),F(1)),(k,p),(k/2,p/2),
                (k/2,(1+p)/2),(F(),p/2),(F(),p-tiny),
                (F(1),p/2),((k+1)/2,(z-(k+1)/2)/2)}
        for r in (c,c+candidate.nu,u,candidate.d,candidate.A,a,candidate.T):
            for delta in (-tiny,F(),tiny):
                if 0<=r+delta<=1:
                    points.update(((F(),r+delta),(F(1),r+delta),
                                   (r+delta,F()),(r+delta,F(1)),
                                   (r+delta,p/2),(k/2,r+delta)))
        for delta in (-tiny,F(),tiny):
            if 0<=k+delta<=1:
                points.update(((k+delta,p/2),(k+delta,(p+1)/2)))
        for own in sorted(points):
            if not all(0<=v<=1 for v in own):
                continue
            expected=max(F(),own[1]-p,sum(own)-z)
            for reversed_items in (False,True):
                v=own[::-1] if reversed_items else own
                w=fixed[::-1] if reversed_items else fixed
                first=1 if reversed_items else 0
                second=1-first
                for profile,bidder in ((v+w,0),(w+v,1)):
                    result=candidate.mechanism(profile)
                    assert result['utilities'][bidder]==expected
                    other=result['allocations'][1-bidder]
                    if own[0]<k:
                        assert other[first]==1,(fixed,own,result)
                        strip_cases+=1
                    if all(0<x<1 for x in own) and own[1]<p and sum(own)<z:
                        assert other[first]==1,(fixed,own,result)
                        hole_cases+=1
                    if own[0]==0 and own[1]<p:
                        assert other==(1,1),(fixed,own,result)
                        left_cases+=1
                    cases+=1
    return dict(source=str(path.relative_to(ROOT)).replace('\\','/'),
                source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                fixed_opponent_checks=len(opponents),complete_menu_profile_checks=cases,
                first_item_strip_checks=strip_cases,first_item_hole_checks=hole_cases,
                left_edge_bundle_checks=left_cases,wing_area=str(area),
                density_margin=str(margin),
                scope='Frozen refined candidate; both bidder labels and both item orientations; bounded implementation checks support the separate all-real proof')


def verify():
    data=dict(status='RESIDUAL_WING_SCREENING_EXACT_PASS',theorem=theorem_checks(),
              actual_residual=actual_checks(),
              identity='R+u0=integral_G(((3x-1)a1+(3y-1)a2)/2)+integral_H((((3k+1)y-k-1)/(2k))a2)',
              scope='Full randomized conditional optimum for each bidder on the actual wing residual; no lower-bound increment or unrestricted auction upper claimed',
              proof='research_log/residual_wing_screening.md')
    path=ROOT/'certificate/residual_wing_screening.json'
    if '--write' in sys.argv:
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads(path.read_text(encoding='utf-8'))==data
    print(data['status'])
    print('continuous_identity_checks',data['theorem']['continuous_menu_identity_checks'])
    print('actual_profiles',data['actual_residual']['complete_menu_profile_checks'])
    print('wing_area',data['actual_residual']['wing_area'])
    return data


if __name__=='__main__':
    verify()
