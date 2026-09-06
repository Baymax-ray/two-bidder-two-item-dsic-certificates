"""Independent symbolic integration and exact allocation-cell audit."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import conditional_global_splice as primary
ROOT=HERE.parent

def add(*ps):
    q={}
    for p in ps:
        for e,c in p.items():q[e]=q.get(e,F())+c
    return {e:c for e,c in q.items() if c}
def scale(p,z):return {e:c*z for e,c in p.items() if c*z}
def mul(*ps):
    q={(0,0):F(1)}
    for p in ps:
        r={}
        for e,c in q.items():
            for f,d in p.items():
                k=e[0]+f[0],e[1]+f[1];r[k]=r.get(k,F())+c*d
        q={e:c for e,c in r.items() if c}
    return q

ONE={(0,0):F(1)};S={(1,0):F(1)};Y={(1,1):F(1)}

def symbolic_boole(manifest):
    bases=[tuple(e) for e in manifest['basis_order']]
    coeff=list(map(F,manifest['theta']))
    h=F(43,100); weights=[F(i,90) for i in (7,32,12,32,7)]
    accumulated=[{},{}]
    for i,j in product(range(5),repeat=2):
        opp=(h*i/4,h*j/4)
        derivatives=[{},{},{}]
        for e,theta in zip(bases,coeff):
            for powers,sign in ((e,1),((e[1],e[0],e[3],e[2]),-1)):
                factor=theta*sign*opp[0]**powers[2]*opp[1]**powers[3]
                for n,axis in enumerate((-1,0,1)):
                    if axis>=0 and not powers[axis]:continue
                    degree=(powers[0]+powers[1]-(axis>=0),powers[1]-(axis==1))
                    value=factor*(powers[axis] if axis>=0 else 1)
                    derivatives[n]=add(derivatives[n],{degree:value})
        pp,px,py=derivatives
        corr1=mul(S,add(ONE,scale(S,-1)),add(mul(add(ONE,scale(Y,-2)),pp),mul(Y,add(ONE,scale(Y,-1)),py)))
        corr2=scale(mul(Y,add(ONE,scale(Y,-1)),add(mul(add(ONE,scale(S,-2)),pp),mul(S,add(ONE,scale(S,-1)),px))),-1)
        base=add(scale(mul(S,S),F(3,2)),scale(ONE,-F(1,2)))
        vals=(add(base,mul(S,corr1)),add(mul({(0,1):F(1)},base),mul(S,corr2)))
        for k in range(2):accumulated[k]=add(accumulated[k],scale(vals[k],h*h*weights[i]*weights[j]))
    return accumulated

def sign_pair(r,s):
    if s==0:return (r>0)-(r<0)
    if r>=0 and s>=0:return 1
    if r<=0 and s<=0:return -1
    z=r*r-2*s*s
    return ((r>0)-(r<0))*((z>0)-(z<0))

def corner_check(s,t,a):
    values=[(F(),F()),(s-F(2,3),F()),(s*t-F(2,3),F()),(s+s*t-F(4,3),F(1,3))]
    index={(0,0):0,(1,0):1,(1,1):3}[a]
    selected=values[index]
    return all(sign_pair(selected[0]-v[0],selected[1]-v[1])>=0 for v in values)

def integrate(poly,i,j,n):
    return sum((v*(F(i+1,n)**(a+1)-F(i,n)**(a+1))*(F(j+1,n)**(b+1)-F(j,n)**(b+1))/((a+1)*(b+1)) for (a,b),v in poly.items()),F())

def verify():
    averaged,manifest=primary.fields()
    independent=symbolic_boole(manifest)
    assert independent==averaged
    slo,shi=primary.root2_bounds()
    blo,bhi=(4-shi)/3,(4-slo)/3;klo,khi=blo-F(2,3),bhi-F(2,3)
    checks=0
    for n in (8,16,32,64):
        for i,j in product(range(n),repeat=2):
            a=primary.select_cell(i,j,n,blo,bhi,klo,khi)
            if a is None:continue
            for ii,jj in product((i,i+1),(j,j+1)):
                assert corner_check(F(ii,n),F(jj,n),a),(n,i,j,a,ii,jj)
                checks+=1
    # Old OR test misclassified this cell although it crosses the bundle
    # upgrade threshold. Both required bundle inequalities are necessary.
    assert primary.select_cell(14,3,16,blo,bhi,klo,khi) is None
    assert not corner_check(F(14,16),F(3,16),(1,1))
    assert corner_check(F(15,16),F(4,16),(1,1))
    # Primitive integer tabulation is compared with direct monomial
    # rectangle integrals, independently at several nonuniform positions.
    integral_checks=0
    for n in (16,32,64):
        tables,den=primary.tabulate([primary.primitive(p) for p in averaged],n)
        for i,j in ((0,0),(n//3,n//5),(n-2,n//4),(n-1,n-1),(n//2,n//2)):
            for k in range(2):
                t=tables[k]
                value=F(t[i+1][j+1]-t[i][j+1]-t[i+1][j]+t[i][j],den)
                assert value==integrate(independent[k],i,j,n)
                integral_checks+=1
    data=dict(status='INDEPENDENT_CONDITIONAL_SPLICE_PASS',
        symbolic_integration='all coefficients match direct analytic derivatives plus tensor Boole integration',
        field_monomial_counts=[len(p) for p in independent],
        exact_cell_corner_comparisons=checks,exact_independent_cell_integrals=integral_checks,
        rejected_crossing_cell=dict(n=16,i=14,j=3),
        scope='independent full polynomial identity and boundary classification audits; main verifier reconstructs 1024 integral partition')
    path=ROOT/'certificate/independent_conditional_splice.json'
    if '--write' in sys.argv:path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text(encoding='utf-8'))==data
    print(data['status']);print('cell_corner_comparisons',checks)
    return data
if __name__=='__main__':verify()
