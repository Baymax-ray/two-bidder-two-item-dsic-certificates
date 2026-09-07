"""Exact fixed-seed reserve-family arithmetic. No source calculator imports.

Default execution is read-only. --write records the derived manifest.
The all-real admissibility theorem is in the manuscript, not inferred from
the bounded implementation tests. Frozen face integrations are dependencies.
"""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from itertools import product
from math import comb
import json,sys

if sys.flags.optimize:
    raise RuntimeError('Run without optimized Python mode')
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE=ROOT/'certificate/v5_primal_dual'
BASE_HASH='204fe57d5ed28a67030f571b1254cc25135df2cb083c1f8444a45afdd3cc5fce'
FACE='source/V5_gap_closure/certificate/primal_face_integrals.json'
TAU=F(83,10000)

def envelope(coeff,moments):
    lo=hi=F()
    for name,c in coeff.items():
        a,b=moments[name]
        lo+=c*(a if c>=0 else b)
        hi+=c*(b if c>=0 else a)
    return lo,hi

def evaluate(poly,t):
    return sum((c*t**i for i,c in enumerate(poly)),F())

def derivative(poly,n=1):
    for _ in range(n): poly=[i*c for i,c in enumerate(poly)][1:]
    return poly

def basis(k,m,mult):
    p=[F()]*6
    for j in range(m+1): p[k+j]=F(mult*(-1)**j*comb(m,j))
    return p

def weights():
    out={}
    for prefix,names in [('R',['R4','R3','RSJA','Rsame','Rcross','Rone']),
                         ('N',['N4','N3','NSJA','Nsame','Ncross','N_one'])]:
        for name,k,mult in zip(names,[0,1,2,2,2,3],[1,4,2,2,2,4]):
            out[name]=basis(k+(prefix=='N'),5-k-(prefix=='N'),mult)
    return out

def bernstein(poly,a,b):
    n=len(poly)-1
    local=[sum((poly[j]*comb(j,k)*a**(j-k)*(b-a)**k
                for j in range(k,n+1)),F()) for k in range(n+1)]
    return [sum((local[k]*F(comb(i,k),comb(n,k)) for k in range(i+1)),F())
            for i in range(n+1)]

def decimal(q,digits=30,up=False):
    scale=10**digits
    n=(q.numerator*scale)//q.denominator
    if up and F(n,scale)<q:n+=1
    sign='-' if n<0 else '';n=abs(n)
    return sign+str(n//scale)+'.'+str(n%scale).zfill(digits)

def displayed(bounds,digits=30):
    return [decimal(bounds[0],digits),decimal(bounds[1],digits,True)]

def ownership():
    center=tuple(map(F,['1577/2000','123/200','3/5','4/5']))
    r=F(1,10000);q=F(93,500);s=1-TAU;b=F(1496947,1500000)
    assert min(center)-r>TAU+s/2
    assert min(sum(center[:2]),sum(center[2:]))-2*r>2*TAU+s*b
    assert min(center)-r>F(3421,10000)
    def utilities(v,i,surcharge):
        x,y=v[2*i:2*i+2];w,z=v[2*(1-i):2*(1-i)+2]
        return (F(),x-w-surcharge,y-z-surcharge,x+y-w-z)
    minima=[]
    for scale,chosen in [(F(1),(3,0)),(s,(1,2))]:
        margins=[]
        for signs in product((-1,1),repeat=4):
            v=tuple(x+r*sign for x,sign in zip(center,signs))
            for i in (0,1):
                values=utilities(v,i,scale*q)
                margins.extend(values[chosen[i]]-x for j,x in enumerate(values) if j!=chosen[i])
        minima.append(min(margins))
    assert min(minima)>0
    return dict(center=list(map(str,center)),radius=str(r),volume=str((2*r)**4),
                seed_margin=str(minima[0]),transformed_margin=str(minima[1]),
                seed_allocation=[[1,1],[0,0]],transformed_allocation=[[1,0],[0,1]],
                whole_box_branch_certified=True,affine_vertex_comparisons=192)

def calculate():
    assert sha256((BASE/'manifest.json').read_bytes()).hexdigest()==BASE_HASH
    source=json.loads((BASE/'manifest.json').read_text(encoding='utf-8'))
    face_bytes=(BASE/FACE).read_bytes()
    assert sha256(face_bytes).hexdigest()==source['package_files'][FACE]
    raw=json.loads(face_bytes)
    assert raw['status']=='EXACT_SOURCE_FACE_MOMENTS_PASS'
    moments={k:tuple(map(F,v)) for k,v in raw['moment_enclosures'].items()}
    assert all(a<=b for a,b in moments.values())
    w=weights()
    revenue=envelope({k:evaluate(p,TAU) for k,p in w.items()},moments)
    old=F(1,100)
    gain=envelope({k:evaluate(p,TAU)-evaluate(p,old) for k,p in w.items()},moments)
    slope=envelope({k:evaluate(derivative(p),old) for k,p in w.items()},moments)
    assert gain[0]>F('0.0000021293')
    assert F('-0.002506136')<slope[0]<=slope[1]<F('-0.002504465')
    assert F('0.876514341027')<revenue[0]<=revenue[1]<F('0.876514355425')
    a,b=F('0.008297'),F('0.008299')
    sign_records=[]
    for left,right,order,sign in [(F(),a,1,1),(b,F(1),1,-1),(a,b,2,-1)]:
        coefficients={k:bernstein(derivative(p,order),left,right) for k,p in w.items()}
        bounds=[envelope({k:p[i] for k,p in coefficients.items()},moments)
                for i in range(6-order)]
        assert all(lo>0 if sign>0 else hi<0 for lo,hi in bounds)
        sign_records.append(dict(interval=list(map(str,(left,right))),derivative_order=order,
                                 sign=sign,bernstein_enclosures=[list(map(str,x)) for x in bounds]))
    coeff={k:bernstein(p,a,b) for k,p in w.items()}
    maximum_upper=max(envelope({k:p[i] for k,p in coeff.items()},moments)[1] for i in range(6))
    assert maximum_upper<F('0.87651436')
    upper=F(source['upper'])
    gap=(upper-revenue[1],upper-revenue[0])
    guarantee=F(993384,1000000)
    assert revenue[0]/upper>guarantee
    return dict(status='EXACT_RESERVE_PARAMETER_CERTIFICATE_PASS',tau=str(TAU),
                mechanism='mechanism.py:mechanism',seed_manifest_sha256=BASE_HASH,
                face_sha256=sha256(face_bytes).hexdigest(),
                revenue_enclosure=list(map(str,revenue)),lower_enclosure=displayed(revenue),
                upper=source['upper'],upper_enclosure=source['upper_enclosure'],
                upper_components=source['upper_components'],gap_enclosure=displayed(gap),
                guarantee=str(guarantee),gain_over_one_percent=list(map(str,gain)),
                gain_display=displayed(gain),slope_at_one_percent=list(map(str,slope)),
                slope_display=displayed(slope),unique_family_optimizer_interval=list(map(str,(a,b))),
                family_sign_certificates=sign_records,family_maximum_upper=str(maximum_upper),
                family_maximum_upper_display=decimal(maximum_upper,30,True),
                ownership=ownership(),
                scope='Fixed-seed reserve family only. Unique family optimum is not unrestricted auction optimality. Frozen face integrations and upper certificate are dependencies, not rerun by this entrypoint.')

def main():
    result=calculate()
    path=HERE/'manifest.json'
    if sys.argv[1:]==['--write']:
        path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    else:
        assert not sys.argv[1:],'Unknown arguments'
        assert json.loads(path.read_text(encoding='utf-8'))==result,'Derived reserve manifest differs'
    print(result['status'])
    for k in ['tau','lower_enclosure','gap_enclosure','gain_display','slope_display',
              'family_maximum_upper_display','ownership']:
        print(k,result[k])

if __name__=='__main__':main()
