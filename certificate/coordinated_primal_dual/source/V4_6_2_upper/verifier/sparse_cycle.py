"""Exact continuum long-range two-box IC cycle, no type-grid constraints.

Discovery chose rational centers. This replay independently reconstructs
all virtual polynomials and proves strict winner margins on entire boxes.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
from math import comb
from hashlib import sha256
import json,sys
if not __debug__ or sys.flags.optimize: raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
ARCH=ROOT.parents[3]/'research/closed/two-bidder-two-item-dsic-certificates/certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound'
ZERO=(0,0,0,0)
ONE={ZERO:F(1)}

def add(*ps):
    q={}
    for p in ps:
        for e,c in p.items():q[e]=q.get(e,F())+c
    return {e:c for e,c in q.items() if c}

def scale(p,c):return {e:v*c for e,v in p.items() if v*c}
def mul(*ps):
    q=ONE
    for p in ps:
        r={}
        for e,c in q.items():
            for f,d in p.items():
                g=tuple(a+b for a,b in zip(e,f));r[g]=r.get(g,F())+c*d
        q={e:c for e,c in r.items() if c}
    return q

def var(j):
    e=list(ZERO);e[j]=1
    return {tuple(e):F(1)}

def der(p,j):
    out={}
    for e,c in p.items():
        if e[j]:
            f=list(e);f[j]-=1;out[tuple(f)]=c*e[j]
    return out

def swap_bidders(p):return {(e[2],e[3],e[0],e[1]):c for e,c in p.items()}

def centered(p,center):
    out={}
    for e,c in p.items():
        for f in product(*(range(n+1) for n in e)):
            v=c
            for n,k,x in zip(e,f,center):v*=comb(n,k)*x**(n-k)
            out[f]=out.get(f,F())+v
    return {e:c for e,c in out.items() if c}

def bound(p,halfwidths):
    center=p.get(ZERO,F());radius=F()
    for e,c in p.items():
        if e==ZERO:continue
        term=abs(c)
        for n,h in zip(e,halfwidths):term*=h**n
        radius+=term
    return center-radius,center+radius

def polynomials():
    data=json.loads((ARCH/'manifest.json').read_text(encoding='utf-8'))
    exponents=[tuple(e) for e in data['basis_order']]
    theta=list(map(F,data['theta']))
    assert len(theta)==len(exponents)==32
    anti={}
    for e,c in zip(exponents,theta):
        f=(e[1],e[0],e[3],e[2])
        assert e<f
        anti=add(anti,{e:c,f:-c})
    x,y,z,w=[var(j) for j in range(4)]
    stream=mul(x,add(ONE,scale(x,-1)),y,add(ONE,scale(y,-1)),anti)
    correction=(der(stream,1),scale(der(stream,0),-1))
    assert not add(der(correction[0],0),der(correction[1],1))
    item_swap={(e[1],e[0],e[3],e[2]):v for e,v in correction[0].items()}
    assert item_swap==correction[1]
    # Both source boxes have own second coordinate maximal; opponent first
    # coordinate maximal. D=2*y^2*z^2 is strictly positive on both boxes.
    y2,z2=mul(y,y),mul(z,z)
    denominator=scale(mul(y2,z2),2)
    fields=[]
    for j in range(2):
        p1=add(mul(add(scale(y2,3),scale(ONE,-1)),(x,y)[j],z2),mul(denominator,correction[j]))
        p2=add(mul(add(scale(z2,3),scale(ONE,-1)),(z,w)[j],y2),mul(denominator,swap_bidders(correction[j])))
        fields.append((p1,p2))
    return fields,denominator,data

def calculate():
    fields,D,source=polynomials()
    A=(F(2,5),F(39,40));B=(F(7,20),F(23,40));W=(F(3,5),F(1,5))
    shift=tuple(a-b for a,b in zip(A,B))
    assert shift==(F(1,20),F(2,5))
    # Winner arrays use 1 for bidder1, 2 for bidder2, 0 for unsold.
    winners=((2,1),(1,1))
    epsilon=F(1,20)
    half=(F(3,200),)*4
    checks=[]
    for center,sign,win in ((A+W,1,winners[0]),(B+W,-1,winners[1])):
        assert center[1]-half[1]>center[0]+half[0]>0
        assert center[2]-half[2]>center[3]+half[3]>0
        assert all(0<z-h<z+h<1 for z,h in zip(center,half))
        for j in range(2):
            p1,p2=fields[j]
            shifted=add(p1,scale(D,sign*epsilon*shift[j]))
            for label,first in (('original',p1),('shifted',shifted)):
                selected=first if win[j]==1 else p2
                rival=p2 if win[j]==1 else first
                for relation,p in (('positive',selected),('beats_rival',add(selected,scale(rival,-1)))):
                    lo,hi=bound(centered(p,center),half)
                    checks.append(dict(center=list(map(str,center)),item=j+1,field=label,relation=relation,lower=str(lo),upper=str(hi)))
                    assert lo>0,(center,j,label,relation,float(lo))
    volume=(2*half[0])*(2*half[1])*(2*half[2])*(2*half[3])
    aa,ab=(F(),F(1)),(F(1),F(1))
    slope=sum((d*(x-y) for d,x,y in zip(shift,aa,ab)),F())
    assert slope==-F(1,20)
    gain=-epsilon*volume*slope
    assert gain==F(81,40000000000)
    permutations=((0,1,2,3),(1,0,3,2),(2,3,0,1),(3,2,1,0))
    orbit_centers=[tuple(center[j] for j in permutation) for permutation in permutations for center in (A+W,B+W)]
    separations=[]
    for i in range(8):
        for j in range(i+1,8):
            axes=[k for k in range(4) if abs(orbit_centers[i][k]-orbit_centers[j][k])>2*half[k]]
            assert axes
            separations.append([i,j,axes[0]])
    for center in orbit_centers:
        assert max(center[:2])-half[0]>F(43,100)
        assert max(center[2:])-half[2]>F(43,100)
    aggregate=4*gain
    assert aggregate==F(81,10000000000)
    return dict(status='SPARSE_LONG_RANGE_CONTINUUM_CYCLE_PASS',
        center_A=list(map(str,A)),center_B=list(map(str,B)),opponent_center=list(map(str,W)),
        halfwidths=list(map(str,half)),cycle_density=str(epsilon),shift=list(map(str,shift)),
        allocation_A=['0','1'],allocation_B=['1','1'],
        old_and_new_winners=[list(w) for w in winners],
        single_orientation_reduction=str(gain),exact_strict_upper_reduction=str(aggregate),
        orbit_centers=[list(map(str,c)) for c in orbit_centers],pairwise_separations=separations,
        certified_density_sequence=['1/80','1/40','1/20'],
        exact_reduction_sequence=[str(aggregate/4),str(aggregate/2),str(aggregate)],
        certified_winner_margins=checks,
        source_manifest_sha256=sha256((ARCH/'manifest.json').read_bytes()).hexdigest(),
        source='continuous_stream_degree4_two_level_nonuniform_upper_bound',
        scope='nonnegative translated two-way IC flow; exact decrease of full continuous virtual envelope',
        old_upper='3715139591287203/4194304000000000',
        new_upper_from_inherited=str(F(3715139591287203,4194304000000000)-aggregate),
        independent_scope='rational centered-Taylor absolute bounds on full report boxes; no grid feasibility')

if __name__=='__main__':
    data=calculate()
    target=ROOT/'certificate/sparse_cycle.json'
    if '--write' in sys.argv:target.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(target.read_text(encoding='utf-8'))==data
    print(data['status']);print('exact_upper_reduction',data['exact_strict_upper_reduction'])
