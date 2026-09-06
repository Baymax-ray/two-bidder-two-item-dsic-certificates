"""Exact positive gap on an untouched V4.6 lottery box for the final dual."""
from fractions import Fraction as F
from pathlib import Path
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));import sparse_cycle as p
ROOT=HERE.parent

def verify():
    data=json.loads((p.ARCH/'manifest.json').read_text(encoding='utf-8'))
    anti={}
    for ee,cc in zip(data['basis_order'],data['theta']):
        e=tuple(ee);c=F(cc);es=e[1],e[0],e[3],e[2]
        anti=p.add(anti,{e:c,es:-c})
    x,y,z,w=[p.var(j) for j in range(4)]
    stream=p.mul(x,p.add(p.ONE,p.scale(x,-1)),y,p.add(p.ONE,p.scale(y,-1)),anti)
    second=p.swap_bidders(p.scale(p.der(stream,0),-1))
    x2,z2=p.mul(x,x),p.mul(z,z)
    D=p.scale(p.mul(x2,z2),2)
    numerator=p.add(p.mul(p.add(p.scale(z2,3),p.scale(p.ONE,-1)),w,x2),p.mul(D,second))
    center=(F(151,200),F(3,40),F(9,10),F(13,40));half=(F(1,10000),)*4
    lo,hi=p.bound(p.centered(numerator,center),half)
    assert lo>0 or hi<0,(float(lo),float(hi))
    absolute=lo if lo>0 else -hi
    denominator_upper=2*(center[0]+half[0])**2*(center[2]+half[2])**2
    phi_lower=absolute/denominator_upper
    larger=((F(3,4),F(19,25)),(F(1,20),F(1,10)),(F(17,20),F(19,20)),(F(3,10),F(7,20)))
    for z,h,(a,b) in zip(center,half,larger):assert a<z-h<z+h<b
    assert max(center[:2])-half[0]>F(43,100) and max(center[2:])-half[2]>F(43,100)
    cycles=json.loads((ROOT/'certificate/sparse_cycle.json').read_text(encoding='utf-8'))
    c_half=tuple(map(F,cycles['halfwidths']))
    for cc in cycles['orbit_centers']:
        other=tuple(map(F,cc))
        assert any(abs(z-v)>h+k for z,v,h,k in zip(center,other,half,c_half))
    # The all-real V4.6 lottery-box proof gives bidder1 empty, bidder2
    # allocation(1,beta), and 4/5<beta<19/20. Therefore capacity+virtual
    # slack on the safe item is at least |phi_22|/20, whichever its sign.
    volume=F(1)
    for h in half:volume*=2*h
    gap=phi_lower*volume/20
    result=dict(status='POSITIVE_UNTOUCHED_LOTTERY_GAP_PASS',
       center=list(map(str,center)),halfwidths=list(map(str,half)),
       virtual_numerator_interval=list(map(str,(lo,hi))),virtual_absolute_lower=str(phi_lower),
       box_volume=str(volume),exact_capacity_plus_virtual_slack_lower=str(gap),
       sign='positive' if lo>0 else 'negative',
       candidate_dependency='V4.6 all-real lottery box in flatness_constraints.json and flatness_global_equality.md',
       scope='final common density is unchanged stream on this box; strict gap of this dual versus V4.6, not candidate suboptimality')
    target=ROOT/'certificate/remaining_lottery_slack.json'
    if '--write' in sys.argv:target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(target.read_text(encoding='utf-8'))==result
    print(result['status']);print('phi_absolute_lower_display',float(phi_lower));print('certified_gap_positive',gap>0)
    return result
if __name__=='__main__':verify()
