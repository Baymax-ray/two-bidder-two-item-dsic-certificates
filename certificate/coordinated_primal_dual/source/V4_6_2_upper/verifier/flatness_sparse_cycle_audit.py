"""Independent sparse-cycle numerator and symmetry audit; always read-only."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path
import importlib.util
import json
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sparse_cycle_primary',ROOT/'verifier/sparse_cycle.py')
primary=importlib.util.module_from_spec(spec)
spec.loader.exec_module(primary)
ZERO=(0,0,0,0)

def collect(terms):
    out={}
    for e,c in terms:out[e]=out.get(e,F())+c
    return {e:c for e,c in out.items() if c}

def shifted_power(e,offset):return tuple(a+b for a,b in zip(e,offset))

def independent_numerators():
    m=json.loads((primary.ARCH/'manifest.json').read_text(encoding='utf-8'))
    boundary=[((1,1,0,0),1),((2,1,0,0),-1),((1,2,0,0),-1),((2,2,0,0),1)]
    stream=[]
    for raw,coef in zip(m['basis_order'],m['theta']):
        e=tuple(raw); f=(e[1],e[0],e[3],e[2]); q=F(coef)
        for a,sign in boundary:
            stream.extend([(shifted_power(e,a),q*sign),(shifted_power(f,a),-q*sign)])
    correction=[]
    for coordinate,sign in ((1,1),(0,-1)):
        terms=[]
        for e,c in stream:
            if not e[coordinate]:continue
            d=list(e);d[coordinate]-=1
            terms.append((tuple(d),sign*e[coordinate]*c))
        correction.append(collect(terms))
    Dpower=(0,2,2,0)
    fields=[]
    for j in range(2):
        e=[0,0,2,0];e[j]+=1
        high=e.copy();high[1]+=2
        one=[(tuple(high),F(3)),(tuple(e),F(-1))]
        one.extend((shifted_power(a,Dpower),2*b) for a,b in correction[j].items())
        e=[0,2,0,0];e[j+2]+=1
        high=e.copy();high[2]+=2
        two=[(tuple(high),F(3)),(tuple(e),F(-1))]
        two.extend((shifted_power((a[2],a[3],a[0],a[1]),Dpower),2*b) for a,b in correction[j].items())
        fields.append((collect(one),collect(two)))
    return fields,{Dpower:F(2)},correction

def shift_one_coordinate(p,j,center):
    terms=[]
    for e,c in p.items():
        for k in range(e[j]+1):
            a=list(e);a[j]=k
            terms.append((tuple(a),c*comb(e[j],k)*center**(e[j]-k)))
    return collect(terms)

def center_sequential(p,center):
    for j,x in enumerate(center):p=shift_one_coordinate(p,j,x)
    return p

def value(p,x):
    return sum((c*product_value(e,x) for e,c in p.items()),F())

def product_value(e,x):
    p=F(1)
    for n,a in zip(e,x):p*=a**n
    return p

def audit():
    independent,D,correction=independent_numerators()
    fields,original_D,_=primary.polynomials()
    assert independent==fields and D==original_D
    # Item symmetry follows directly from the two differentiated stream components.
    swapped={(e[1],e[0],e[3],e[2]):c for e,c in correction[0].items()}
    assert swapped==correction[1]
    A=(F(2,5),F(39,40));B=(F(7,20),F(23,40));W=(F(3,5),F(1,5))
    h=F(3,200);epsilon=F(1,20);d=tuple(a-b for a,b in zip(A,B))
    certificate=json.loads((ROOT/'certificate/sparse_cycle.json').read_text(encoding='utf-8'))
    rows=certificate['certified_winner_margins']
    assert len(rows)==16
    min_lower=None
    for center,sgn,winners in ((A+W,1,(2,1)),(B+W,-1,(1,1))):
        assert center[1]-h>center[0]+h and center[2]-h>center[3]+h
        assert value(D,center)>0
        for j in range(2):
            p1,p2=fields[j]
            for label in ('original','shifted'):
                if label=='shifted':
                    p1=collect(list(fields[j][0].items())+[(e,c*sgn*epsilon*d[j]) for e,c in D.items()])
                selected,rival=(p1,p2) if winners[j]==1 else (p2,p1)
                for relation,poly in (('positive',selected),('beats_rival',collect(list(selected.items())+[(e,-c) for e,c in rival.items()]))):
                    centered=center_sequential(poly,center)
                    assert centered==primary.centered(poly,center)
                    radius=sum((abs(c)*h**sum(e) for e,c in centered.items() if e!=ZERO),F())
                    lo=centered.get(ZERO,F())-radius
                    hi=centered.get(ZERO,F())+radius
                    assert lo>0
                    row=next(x for x in rows if x['center']==list(map(str,center)) and x['item']==j+1 and x['field']==label and x['relation']==relation)
                    assert F(row['lower'])==lo and F(row['upper'])==hi
                    min_lower=lo if min_lower is None else min(min_lower,lo)
                    for signs in product((-1,1),repeat=4):
                        point=tuple(a+s*h for a,s in zip(center,signs))
                        actual=value(poly,point)
                        assert lo<=actual<=hi
    # Four group elements, each with two full-profile rectangles.
    def item_swap(p):return (p[1],p[0],p[3],p[2])
    def bidder_swap(p):return (p[2],p[3],p[0],p[1])
    boxes=[]
    for bswap,iswap in product((False,True),repeat=2):
        for own in (A,B):
            p=own+W
            if iswap:p=item_swap(p)
            if bswap:p=bidder_swap(p)
            boxes.append(p)
    for a,b in combinations(boxes,2):
        assert any(abs(x-y)>2*h for x,y in zip(a,b))
    # Every support profile has both bidders outside the conditional-splice square.
    for p in boxes:
        assert max(p[:2])-h>F(43,100)
        assert max(p[2:])-h>F(43,100)
    volume=(2*h)**4
    aa,ab=(F(),F(1)),(F(1),F(1))
    slope=sum((z*(x-y) for z,x,y in zip(d,aa,ab)),F())
    gain=-epsilon*volume*slope
    assert slope==-F(1,20) and gain==F(81,40000000000)
    assert 4*gain==F(81,10000000000)
    assert F(certificate['exact_strict_upper_reduction']) in (gain,4*gain)
    print('SPARSE_CYCLE_INDEPENDENT_AUDIT_PASS')
    print('rational numerator reconstructions: 4')
    print('strict whole-box comparisons: 16; independent endpoint checks: 256')
    print('disjoint rectangle pairs: 28')
    print('minimum numerator margin:',float(min_lower))
    print('single cycle reduction:',gain)
    print('four-orbit reduction:',4*gain)

if __name__=='__main__':audit()
