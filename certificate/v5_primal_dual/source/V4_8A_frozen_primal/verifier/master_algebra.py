"""Rational continuous endpoint-box data for the coupled stress master."""
from pathlib import Path
from fractions import Fraction as F
from math import prod
import importlib.util,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V4_7/verifier'))
import psd_polynomials as e
spec=importlib.util.spec_from_file_location('atlas_classifier_master',ROOT.parent/'V4_6_3_slack_atlas/verifier/independent_menu_classifier.py')
classifier=importlib.util.module_from_spec(spec);spec.loader.exec_module(classifier)

def old_boxes():
    p=json.loads((ROOT.parent/'V4_7/certificate/psd_local_certificate.json').read_text())
    out=[(tuple(map(F,s['center'])),tuple(map(F,s['halfwidths']))) for w in p['witnesses'] for s in w['selected_symmetry_orbits']]
    p=json.loads((ROOT.parent/'V4_6_2_upper/certificate/sparse_cycle.json').read_text())
    out +=[(tuple(map(F,x)),tuple(map(F,p['halfwidths']))) for x in p['orbit_centers']]
    swap=lambda z:(z[1],z[0],z[3],z[2])
    assert {(swap(C),swap(h)) for C,h in out}==set(out)
    return out

def compatible(C,h):
    if not all(0<x-z<x+z<1 for x,z in zip(C,h)):return False
    for j in (0,2):
        if C[j]-h[j]<=C[j+1]+h[j+1] or C[j]-h[j]<=F(43,100):return False
    return all(any(abs(x-y)>a+b for x,y,a,b in zip(C,D,h,g)) for D,g in old_boxes())

def classify(C,h):
    return classifier.classify(tuple((x-z,x+z) for x,z in zip(C,h)),(0,0))

def fast_center(poly,center):
    # Successive univariate Horner translations; no binomial expansion.
    for axis,x in enumerate(center):
        groups={}
        for key,value in poly.items():
            base=list(key);n=base[axis];base[axis]=0;base=tuple(base)
            groups.setdefault(base,{})[n]=value
        result={}
        for base,co in groups.items():
            n=max(co);arr=[co[n]]
            for k in range(n-1,-1,-1):
                shifted=[F()]*(len(arr)+1)
                for j,v in enumerate(arr):shifted[j]+=x*v;shifted[j+1]+=v
                shifted[0]+=co.get(k,F());arr=shifted
            for j,v in enumerate(arr):
                if v:key=list(base);key[axis]=j;result[tuple(key)]=v
        poly=result
    return poly

FIELDS,D=e.fields(0,0)
WEIGHTS={}
def fast_bound(poly,h):
    weights=WEIGHTS.setdefault(tuple(h),{})
    radius=F()
    for power,coef in poly.items():
        if power==e.p.ZERO:continue
        if power not in weights:weights[power]=prod(x**n for x,n in zip(h,power))
        radius+=abs(coef)*weights[power]
    mid=poly.get(e.p.ZERO,F())
    return mid-radius,mid+radius

def gaps(C,h):
    dhi=2*(C[0]+h[0])**2*(C[2]+h[2])**2
    pp=[[{},fast_center(a,C),fast_center(b,C)] for a,b in FIELDS]
    ans=[]
    for opts in pp:
        lo1,hi1=fast_bound(opts[1],h);lo2,hi2=fast_bound(opts[2],h)
        lod,hid=fast_bound(e.p.add(opts[1],e.p.scale(opts[2],-1)),h)
        ans.append([max(F(),lo1,lo2)/dhi,max(F(),-hi1,-hid)/dhi,max(F(),-hi2,lod)/dhi])
    return ans

def record(C,h):
    if not compatible(C,h):return None
    cl=classify(C,h)
    if not cl['constant_allocation'] or cl['region']!=('base','base'):return None
    aa=tuple(tuple(lo for lo,hi in side) for side in cl['allocation'])
    if any(sum(a[j] for a in aa)!=1 for j in (0,1)):return None
    return dict(center=list(map(str,C)),halfwidths=list(map(str,h)),allocation=[[str(x) for x in side] for side in aa],region='BB_full',
        gaps=[[str(x) for x in row] for row in gaps(C,h)],volume=str(prod(2*x for x in h)))

def aggregate(cells,columns,amplitudes):
    delta=[[[F() for _ in range(3)] for _ in (0,1)] for c in cells]
    for col,lam in zip(columns,amplitudes):
        a,b,i=col['A'],col['B'],col['bidder'];d=tuple(map(F,col['shift']))
        for j in (0,1):delta[a][j][i+1]+=lam*d[j];delta[b][j][i+1]-=lam*d[j]
    theta=[];upper=F()
    for c,dd in zip(cells,delta):
        tt=[max(dd[j][k]-F(c['gaps'][j][k]) for k in range(3)) for j in (0,1)]
        upper+=F(c['volume'])*sum(tt,F());theta.append(tt)
    return delta,theta,upper
