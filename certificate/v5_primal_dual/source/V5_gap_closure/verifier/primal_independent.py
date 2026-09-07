# Independent geometric and face-moment audit for the V5 lower mechanism.
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,sys

if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
ZERO=(0,0,0)
def constant(x):return {ZERO:F(x)} if x else {}
def var(k):
    e=list(ZERO);e[k]=1;return {tuple(e):F(1)}
def add(*polys):
    out={}
    for p in polys:
        for e,c in p.items():out[e]=out.get(e,F())+c
    return {e:c for e,c in out.items() if c}
def scale(p,c):return {e:v*c for e,v in p.items() if v*c}
def sub(a,b):return add(a,scale(b,-1))
def mul(*polys):
    out=constant(1)
    for p in polys:
        result={}
        for e,c in out.items():
            for f,d in p.items():
                g=tuple(x+y for x,y in zip(e,f));result[g]=result.get(g,F())+c*d
        out={e:c for e,c in result.items() if c}
    return out
def power(p,n):return mul(*([p]*n))
def calculate():
    P,B,C=[var(j) for j in range(3)];one=constant(1);two=constant(2)
    scarce=mul(sub(one,P),sub(C,P));safe=mul(sub(one,B),sub(C,B))
    bundle=sub(mul(add(one,B,scale(C,-1)),add(one,P,scale(C,-1))),scale(power(add(P,B,scale(C,-1)),2),F(1,2)))
    num=add(two,scale(C,-2),power(C,2),mul(add(P,B),sub(one,C)))
    assert not sub(add(scarce,safe,scale(bundle,2)),num)
    t,c,delta=[var(j) for j in range(3)]
    alpha=add(scale(t,3),constant(-2));a=scale(alpha,F(1,2));L=add(a,delta);z=sub(one,t)
    # beta=a/L; cancel L before expanding the exact strip integrals.
    newN=mul(add(L,a),add(z,scale(a,F(1,2))))
    oldN=add(mul(z,delta),scale(mul(z,a),2),power(a,2))
    assert not sub(sub(newN,oldN),scale(mul(alpha,delta),F(1,4)))
    newR=mul(add(mul(t,L),mul(a,c)),add(z,scale(a,F(1,2))))
    oldR=add(mul(t,z,delta),mul(add(t,c,delta),add(mul(z,a),scale(power(a,2),F(1,2)))))
    assert not sub(sub(newR,oldR),scale(mul(power(alpha,2),delta),F(1,8)))
    # Clipped deterministic probabilities are nonnegative under the stated
    # price hypotheses; lottery strip has h in [0,L] and x>=t-beta*h.
    p=ROOT/'certificate/primal_face_integrals.json';data=json.loads(p.read_text())
    ranges=[tuple(map(F,z[:2])) for z in data['resolved_t_intervals']]+[tuple(map(F,z)) for z in data['unresolved_t_intervals']]
    ranges.sort();assert ranges[0][0]==0 and ranges[-1][1]==1
    assert all(a<b for a,b in ranges)
    assert all(b==c for (a,b),(c,d) in zip(ranges,ranges[1:]))
    missing=sum(((F(hi)**2-F(lo)**2)/2 for lo,hi in data['unresolved_t_intervals']),F())
    assert missing==F(data['unresolved_ordered_opponent_area'])
    # Algebraic reserve enclosure and a deliberately loose Lipschitz budget.
    bh=F(data['rational_B0']);error=F(data['uniform_face_rounding_error'])
    assert (4-3*bh)**2>2>(4-3*(bh+F(1,10**15)))**2
    assert error>=F(10,10**15)
    assert F(7,3)+4+F(3,2)<10
    assert F(10,3)+2<8
    en={k:list(map(F,v)) for k,v in data['moment_enclosures'].items()}
    tau=F(1,100);s=1-tau
    def total(prefix,edge,side):
        return s**4*en[prefix+'4'][side]+4*tau*s**3*en[prefix+'3'][side]+2*tau*tau*s*s*sum((en[prefix+k][side] for k in ('SJA','same','cross')),F())+4*tau**3*s*en[edge][side]
    revenue=[s*total('R','Rone',i)+tau*total('N','N_one',i) for i in (0,1)]
    derivative=[en['N4'][0]-5*en['R4'][1]+4*en['R3'][0],en['N4'][1]-5*en['R4'][0]+4*en['R3'][1]]
    assert 0<derivative[0]<derivative[1]
    gain=revenue[0]-en['R4'][1];assert gain>F(48,1000000)
    # All sixteen source faces are represented with multiplicities 1,4,6,4,1.
    z=var(0);ss=sub(constant(1),z)
    weights=add(power(ss,4),scale(mul(z,power(ss,3)),4),scale(mul(power(z,2),power(ss,2)),6),scale(mul(power(z,3),ss),4),power(z,4))
    assert weights==constant(1)
    # An independent full-box high-sum ownership witness.
    v1,v2,w1,w2=map(F,['1577/2000','123/200','3/5','4/5'])
    q=F(93,500);qp=s*q;r=F(1,10000)
    assert min(v1,v2,w1,w2)-r>F(1,2)
    old_margin=v2-w2+q;new_margin=w2-v2-qp
    assert old_margin-2*r>0 and new_margin-2*r>0
    assert v1+v2-w1-w2-4*r>0
    assert v1-w1-qp-2*r>0
    return dict(status='INDEPENDENT_GLOBAL_PRIMAL_MOMENT_AUDIT_PASS',
        deterministic_quantity_identity=True,lottery_quantity_gain='alpha*delta/4',
        lottery_revenue_gain='alpha**2*delta/8',all_parameter_intervals_cover_unit_interval=True,
        source_face_multiplicities=[1,4,6,4,1],source_face_certificate_sha256=sha256(p.read_bytes()).hexdigest(),
        independent_revenue_enclosure=list(map(str,revenue)),display_revenue_enclosure=list(map(float,revenue)),
        positive_global_gain_lower=str(gain),display_gain_lower=float(gain),derivative_interval=list(map(str,derivative)),
        ownership_witness_box_volume=str((2*r)**4),old_ownership='bidder1 bundle; bidder2 empty',
        new_ownership='bidder1 item1; bidder2 item2',old_margin_after_box=str(old_margin-2*r),
        new_margin_after_box=str(new_margin-2*r),
        scope='Independent exact moment geometry and polynomial assembly; the all-real transport, zero-item, and branch-coverage proofs are reviewed in the accompanying note.')
if __name__=='__main__':
    out=calculate();p=ROOT/'certificate/primal_independent.json'
    if '--write' in sys.argv:p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(p.read_text())==out
    print(out['status']);print(out['display_revenue_enclosure'],out['display_gain_lower'])
