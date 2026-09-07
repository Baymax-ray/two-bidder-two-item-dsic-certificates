"""Independent PSD numerator audit and exact first-event zero/tie plateaus.

Only source data and the frozen witness parameters are shared with primary.
Polynomial construction, sequential centering and first-event tests are separate.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product,combinations
from math import comb
from hashlib import sha256
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
ARCH=ROOT.parents[3]/'research/closed/two-bidder-two-item-dsic-certificates/certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound'
ZERO=(0,0,0,0)

def collect(terms):
    out={}
    for e,c in terms:out[e]=out.get(e,F())+c
    return {e:c for e,c in out.items() if c}
def plus(*ps):return collect((e,c) for p in ps for e,c in p.items())
def times(p,c):return {e:v*c for e,v in p.items() if v*c}
def multiply(p,q):
    return collect((tuple(a+b for a,b in zip(e,f)),c*d) for e,c in p.items() for f,d in q.items())
def offset(e,f):return tuple(a+b for a,b in zip(e,f))
def centered(p,c):
    for j,x in enumerate(c):
        terms=[]
        for e,v in p.items():
            for k in range(e[j]+1):
                f=list(e);f[j]=k
                terms.append((tuple(f),v*comb(e[j],k)*x**(e[j]-k)))
        p=collect(terms)
    return p
def bound(p,h):
    radius=F()
    for e,c in p.items():
        if e==ZERO:continue
        v=abs(c)
        for n,x in zip(e,h):v*=x**n
        radius+=v
    return p.get(ZERO,F())-radius,p.get(ZERO,F())+radius
def value(p,z):
    out=F()
    for e,c in p.items():
        for n,x in zip(e,z):c*=x**n
        out+=c
    return out

def corrections():
    data=json.loads((ARCH/'manifest.json').read_text(encoding='utf-8'))
    stream=[]
    boundary=(((1,1,0,0),1),((2,1,0,0),-1),((1,2,0,0),-1),((2,2,0,0),1))
    for raw,co in zip(data['basis_order'],data['theta']):
        e=tuple(raw);f=(e[1],e[0],e[3],e[2]);co=F(co)
        for a,s in boundary:stream.extend(((offset(e,a),s*co),(offset(f,a),-s*co)))
    out=[]
    for j,sg in ((1,1),(0,-1)):
        terms=[]
        for e,c in stream:
            if e[j]:
                f=list(e);f[j]-=1;terms.append((tuple(f),sg*e[j]*c))
        out.append(collect(terms))
    assert {(e[1],e[0],e[3],e[2]):c for e,c in out[0].items()}==out[1]
    return out

def fields(c,correction):
    m=int(c[1]>c[0]);n=2+int(c[3]>c[2])
    dp=[0]*4;dp[m]+=2;dp[n]+=2;dp=tuple(dp)
    out=[]
    for j in (0,1):
        row=[]
        for bidder in (0,1):
            other=n if bidder==0 else m;own=m if bidder==0 else n
            e=[0]*4;e[other]+=2;e[j+2*bidder]+=1;high=e.copy();high[own]+=2
            terms=[(tuple(high),F(3)),(tuple(e),-F(1))]
            for f,co in correction[j].items():
                if bidder:f=(f[2],f[3],f[0],f[1])
                terms.append((offset(f,dp),2*co))
            row.append(collect(terms))
        out.append(row)
    return out,{dp:F(2)}

def candidate_box_checks(A,B,W,h,region):
    # Independent all-real affine-cell proof, not corner enumeration.
    aa=F(2,3);cc=F(157,500);dd=F(1,2);bb=aa+(dd-cc)**2/2+cc;tt=1-2*cc/3
    if region=='Q/Q':
        assert max(W[j]+h[j+2] for j in (0,1))<dd
        assert sum(W)+h[2]+h[3]<F(861,1000)
        assert F(1417,1000)**2>2 and (4-F(1417,1000))/3==F(861,1000)
        for C in (A,B):
            assert all(C[j]+h[j]<aa for j in (0,1))
            assert sum(C)+h[0]+h[1]<F(861,1000)
        # Opposing type has coordinates<d and sum<B0; every baseline
        # singleton costs>=d and every bundle costs>=B0, hence also empty.
        return [0,0]
    assert region=='base/base'
    assert W[0]-h[2]>tt and W[1]+h[3]<cc
    for C in (A,B):
        assert C[0]-h[0]>max(tt,W[0]+h[2])
        assert C[1]+h[1]<cc
    # Both menus simplify to (opponent_first,d,opponent_first+c).
    # The corrected bidder uniquely chooses item1; opponent uniquely empty.
    return [1,0]

def audit_one(w,correction):
    A,B,W=(tuple(map(F,w[k])) for k in ('A','B','W'))
    h=tuple(map(F,w['halfwidths']));eps=F(w['epsilon']);d=tuple(x-y for x,y in zip(A,B))
    assert d[0]*d[1] and eps>0
    actual=candidate_box_checks(A,B,W,h,w['region'])
    margins=[];events=[];comparisons=[];field_cache=[];denominators=[]
    for side,(C,sign,wins) in enumerate(((A,1,w['winners'][0]),(B,-1,w['winners'][1]))):
        c=C+W
        for block in (0,2):
            assert abs(c[block]-c[block+1])>h[block]+h[block+1]
            assert max(c[block:block+2])-h[block+int(c[block+1]>c[block])]>F(43,100)
        assert all(0<x-z<x+z<1 for x,z in zip(c,h))
        fs,D=fields(c,correction);D=centered(D,c);denominators.append(D)
        field_cache.append([[centered(p,c) for p in row] for row in fs])
        for j,row in enumerate(field_cache[-1]):
            opts=[{},*row];winner=wins[j]
            for rival in range(3):
                if rival==winner:continue
                poly=plus(opts[winner],times(opts[rival],-1))
                rate=sign*d[j]*(int(winner==1)-int(rival==1));slope=times(D,rate)
                for t in (F(),eps):
                    lo,hi=bound(plus(poly,times(slope,t)),h);assert lo>0
                    margins.append(lo)
                label={'endpoint':'A' if side==0 else 'B','item':j+1,'winner':winner,'rival':rival,'rate':str(rate)}
                comparisons.append((poly,slope,label))
                if rate<0:events.append((poly,times(slope,-1),label))
    virtual_slope=sum((d[j]*(int(w['winners'][0][j]==1)-int(w['winners'][1][j]==1)) for j in (0,1)),F())
    assert virtual_slope<0
    volume=F(1)
    for x in h:volume*=2*x
    gain=-eps*volume*virtual_slope
    assert gain==F(w['single_gain'])
    # Independent direct power moments, rather than primary centered even moments.
    integral=F()
    for e,co in correction[1].items():
        for n,x,z in zip(e,B+W,h):co*=((x+z)**(n+1)-(x-z)**(n+1))/(n+1)
        integral+=co
    radial=2*B[1]*h[1]*(3*h[0]-F(1,2)*(1/(B[0]-h[0])-1/(B[0]+h[0])))*4*h[2]*h[3]
    old_capacity=integral+radial
    assert old_capacity==F(w['exact_endpoint_slacks']['old_capacity'])
    assert old_capacity-gain==F(w['exact_endpoint_slacks']['new_capacity'])
    assert events
    ratios=[p[ZERO]/q[ZERO] for p,q,_ in events]
    winner=min(range(len(events)),key=lambda j:ratios[j])
    assert sum(z==ratios[winner] for z in ratios)==1
    ep,eq,label=events[winner]
    cross=[plus(multiply(p,eq),times(multiply(ep,q),-1)) for j,(p,q,_) in enumerate(events) if j!=winner]
    # Find one exact positive-volume first-event chamber, without numerical root fitting.
    for level in range(31):
        small=tuple(x/2**level for x in h)
        if all(bound(p,small)[0]>0 for p in cross):break
    else:raise AssertionError('No strict event chamber certified')
    patch_volume=F(1)
    for x in small:patch_volume*=2*x
    # At every patch corner alpha is the selected rational event; all
    # winner comparisons remain >=0 and the selected one is EXACTLY zero.
    for signs in product((-1,1),repeat=4):
        z=tuple(s*x for s,x in zip(signs,small));alpha=value(ep,z)/value(eq,z)
        assert alpha>=eps
        for p,q,_ in comparisons:assert value(p,z)+alpha*value(q,z)>=0
        assert value(ep,z)-alpha*value(eq,z)==0
        for i,sign in enumerate((1,-1)):
            for j in (0,1):
                n1=value(field_cache[i][j][0],z)+sign*alpha*d[j]*value(denominators[i],z)
                n2=value(field_cache[i][j][1],z)
                assert max(F(),n1,n2)-actual[j]*n1==0
    plateau='zero virtual value' if 0 in (label['winner'],label['rival']) else 'exact cross-bidder virtual tie'
    return {'region':w['region'],'independent_winner_inequalities':len(margins),
            'minimum_margin':str(min(margins)),'actual_corrected_bidder_allocation':actual,
            'actual_opponent_allocation':[0,0],'candidate_Hessian_slack':'0',
            'single_constant_density_gain':str(gain),'independent_old_capacity':str(old_capacity),
            'independent_new_capacity':str(old_capacity-gain),
            'pointwise_capacity_and_virtual_slack_on_paired_event_patches':'0','events':[z[2] for z in events],
            'first_event_center_density':str(ratios[winner]),'uniform_density_lower':str(eps),
            'first_event_patch_halves':list(map(str,small)),'first_event_patch_volume':str(patch_volume),
            'first_event_patch_label':label,'plateau_kind':plateau,
            'plateau_statement':'The minimum event density has this exact zero/tie on the full positive-volume patch; outside it the minimum-event rule remains globally defined on the endpoint boxes.'}

def verify():
    source=ROOT/'certificate/psd_local_certificate.json'
    data=json.loads(source.read_text(encoding='utf-8'));correction=corrections()
    results=[audit_one(w,correction) for w in data['witnesses']]
    boxes=[]
    for w in data['witnesses']:
        h=tuple(map(F,w['halfwidths']));W=tuple(map(F,w['W']))
        for perm in ((0,1,2,3),(1,0,3,2),(2,3,0,1),(3,2,1,0)):
            for name in ('A','B'):
                c=tuple(map(F,w[name]))+W
                boxes.append((tuple(c[j] for j in perm),tuple(h[j] for j in perm)))
    separation_count=0
    for (a,h),(b,k) in combinations(boxes,2):
        assert any(abs(x-y)>z+t for x,y,z,t in zip(a,b,h,k));separation_count+=1
    old=json.loads((ROOT.parent/'V4_6_2_upper/certificate/sparse_cycle.json').read_text())
    old_h=tuple(map(F,old['halfwidths']));old_separations=0
    for a,h in boxes:
        for raw in old['orbit_centers']:
            b=tuple(map(F,raw));assert any(abs(x-y)>z+t for x,y,z,t in zip(a,b,h,old_h));old_separations+=1
    gain=4*sum((F(w['single_gain']) for w in data['witnesses']),F())
    assert gain==F(data['total_delta'])
    record={'status':'INDEPENDENT_PSD_AND_FIRST_EVENT_PASS','witnesses':results,
            'independent_total_constant_gain':str(gain),
            'independent_endpoint_separations':separation_count,
            'independent_old_cycle_separations':old_separations,
            'source_certificate_sha256':sha256(source.read_bytes()).hexdigest(),
            'source_manifest_sha256':sha256((ARCH/'manifest.json').read_bytes()).hexdigest(),
            'scope':'Independent full-box constant-density checks plus all-real minimum-event zero/tie construction. Variable-density envelope gain is bounded below by the same constant-density gain; no extra numerical gain is claimed.'}
    target=ROOT/'certificate/independent_psd_first_event.json'
    if '--write' in sys.argv:target.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(target.read_text(encoding='utf-8'))==record
    print(record['status'])
    for row in results:print(row['region'],row['plateau_kind'],row['first_event_patch_label'],'Hessian_slack',row['candidate_Hessian_slack'])
    return record
if __name__=='__main__':verify()
