"""Full independent depth-20 continuous-majorant replay.

Uses only the archive's independent polynomial and de Casteljau routines;
never imports flow_majorant.py or the archive's verify_stream_dual.py.
Normal operation is read-only. --write regenerates this independent record.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import comb
from hashlib import sha256
import importlib.util
import itertools
import json
import sys
import time
import numpy as np
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
ARCH=ROOT.parents[3]/'research/closed/two-bidder-two-item-dsic-certificates/certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound'
spec=importlib.util.spec_from_file_location('archive_independent_majorant',ARCH/'independent_replay.py')
archive=importlib.util.module_from_spec(spec)
spec.loader.exec_module(archive)
SCALE=10**12
LIMIT=2**63-1
DEPTHS=(12,14,16,18,20)

def rational_controls(poly,degree):
    """Separable power-to-Bernstein transform on a common degree tensor."""
    shape=tuple(d+1 for d in degree)
    work=np.empty(shape,dtype=object)
    work.fill(Q())
    for exponent,coefficient in poly.items():work[exponent]=coefficient
    for axis,d in enumerate(degree):
        old=np.moveaxis(work,axis,0)
        new=np.empty_like(old)
        for row in range(d+1):
            total=np.empty(old.shape[1:],dtype=object)
            total.fill(Q())
            for power in range(row+1):
                total=total+old[power]*Q(comb(row,power),comb(d,power))
            new[row]=total
        work=np.moveaxis(new,0,axis)
    return work

def initial_arrays(first,second):
    degree=tuple(max(max((e[j] for e in p),default=0) for p in (first,second)) for j in range(4))
    arrays=[]
    for poly in (first,second):
        exact=rational_controls(poly,degree)
        lower=[]
        for coefficient in exact.flat:
            k=(SCALE*coefficient.numerator)//coefficient.denominator
            assert Q(k)<=SCALE*coefficient<Q(k+1)
            assert abs(k)<=LIMIT
            lower.append(k)
        arrays.append(np.array(lower,dtype=np.int64).reshape(exact.shape))
    return arrays,degree

def integrate_majorant(first,second,err_first,err_second):
    max_first=max(abs(int(first.min())),abs(int(first.max())))
    max_second=max(abs(int(second.min())),abs(int(second.max())))
    assert max_first+err_first<=LIMIT and max_second+err_second<=LIMIT
    assert max_first+max_second<=LIMIT
    coefficients=np.maximum(0,np.maximum(first+err_first,second+err_second))
    assert int(coefficients.max())*coefficients.size<=LIMIT
    integral_units=-((-int(np.sum(coefficients)))//coefficients.size)
    a_wins=int(first.min())>=0 and int(np.min(first-second))>=err_second
    b_wins=int(second.min())>=0 and int(np.min(second-first))>=err_first
    none_wins=int(np.max(first+err_first))<=0 and int(np.max(second+err_second))<=0
    return integral_units,bool(a_wins or b_wins or none_wins)

def choose_axis(first,second):
    assert max(abs(int(first.min())),abs(int(first.max())),abs(int(second.min())),abs(int(second.max())))<2**62
    best_axis,best_score=0,-1
    for axis in range(4):
        score=max(int(np.max(np.abs(np.diff(first,axis=axis)))),int(np.max(np.abs(np.diff(second,axis=axis)))))
        if score>best_score:best_axis,best_score=axis,score
    return best_axis

def elementary_checks():
    # Separable conversion reproduces t^2 in degree 3 and products exactly.
    poly={(2,1,0,0):Q(7,5),(0,0,0,0):Q(-1,3)}
    degree=(3,2,1,1)
    controls=rational_controls(poly,degree)
    for index in itertools.product(*(range(d+1) for d in degree)):
        expected=-Q(1,3)+Q(7,5)*Q(comb(index[0],2),comb(3,2))*Q(index[1],2)
        assert controls[index]==expected
    # Both signs occur, and a positive error is carried one-sidedly.
    a=np.array([-9,7,15],dtype=np.int64)
    b=np.array([2,-3,11],dtype=np.int64)
    val,fixed=integrate_majorant(a,b,2,4)
    assert val==11 and not fixed

def calculate():
    elementary_checks()
    target=ROOT/'flow_majorant_certificate.json'
    primary_bytes=target.read_bytes()
    primary=json.loads(primary_bytes)
    assert primary['amplitude']=='1' and primary['scale']==SCALE
    assert tuple(row['depth'] for row in primary['results'])==DEPTHS
    manifest,theta,basis=archive.load_manifest()
    accum={d:0 for d in DEPTHS}
    cover={d:0 for d in DEPTHS}
    stats={'nodes':0,'fixed':0,'leaves':0,'max_error':1}
    chart_records=[]
    start=time.monotonic()
    last_progress=start
    for c1,c2 in itertools.product((0,1),repeat=2):
        polynomials=archive.chart_competitors(theta,basis,c1,c2)
        (first,second),degree=initial_arrays(*polynomials)
        print('independent chart start',c1,c2,'common degrees',degree,flush=True)
        stack=[(first,second,1,1,0)]
        local_nodes=0
        while stack:
            first,second,err_first,err_second,level=stack.pop()
            stats['nodes']+=1;local_nodes+=1
            stats['max_error']=max(stats['max_error'],err_first,err_second)
            value,stop=integrate_majorant(first,second,err_first,err_second)
            for depth in DEPTHS:
                if level==depth or (stop and level<depth):
                    units=2**(depth-level)
                    accum[depth]+=value*units
                    cover[depth]+=units
            if stop:
                stats['fixed']+=1
            elif level==DEPTHS[-1]:
                stats['leaves']+=1
            else:
                axis=choose_axis(first,second)
                left_a,right_a,degree_a=archive.bisect_array(first,axis)
                left_b,right_b,degree_b=archive.bisect_array(second,axis)
                stack.append((right_a,right_b,err_first+degree_a,err_second+degree_b,level+1))
                stack.append((left_a,left_b,err_first+degree_a,err_second+degree_b,level+1))
            if stats['nodes']%50000==0 and time.monotonic()-last_progress>=20:
                print('independent progress nodes',stats['nodes'],'elapsed',round(time.monotonic()-start,1),flush=True)
                last_progress=time.monotonic()
        chart_records.append({'chart':[c1,c2],'common_degree':list(degree),'nodes':local_nodes})
        print('independent chart complete',c1,c2,'nodes',stats['nodes'],'elapsed',round(time.monotonic()-start,1),flush=True)
    results=[]
    for depth,saved in zip(DEPTHS,primary['results']):
        assert cover[depth]==4*2**depth==saved['coverage']
        assert accum[depth]==int(saved['accumulator'])
        bound=Q(2*accum[depth],SCALE*2**depth)
        assert bound==Q(saved['upper_bound'])
        results.append({'depth':depth,'accumulator':str(accum[depth]),'coverage':cover[depth],'upper_bound':str(bound)})
    assert stats==primary['statistics']
    assert target.read_bytes()==primary_bytes,'Primary certificate changed during independent replay.'
    assert all(Q(a['upper_bound'])>Q(b['upper_bound']) for a,b in zip(results,results[1:]))
    return {
        'status':'FULL_DEPTH20_INDEPENDENT_MAJORANT_REPLAY_PASS',
        'arithmetic':'Exact Fraction root controls, one-sided int64 subdivision with overflow checks, Python integer accumulation',
        'scale':SCALE,'amplitude':'1','results':results,'statistics':stats,'charts':chart_records,
        'dependencies':{name:sha256((ARCH/name).read_bytes()).hexdigest() for name in ('manifest.json','independent_replay.py')},
        'primary_certificate_sha256':sha256(primary_bytes).hexdigest(),
        'import_boundary':'Imports neither flow_majorant.py nor archive verify_stream_dual.py; uses archive independent polynomial builder and midpoint subdivision only.',
        'scope':'Full replay of all four continuous chart trees through depth 20; compares every saved accumulator, coverage, and tree statistic.'
    }

if __name__=='__main__':
    out=calculate()
    record=ROOT/'certificate/independent_majorant.json'
    if '--write' in sys.argv:
        record.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads(record.read_text(encoding='utf-8'))==out
    print(out['status'],flush=True)
    print('depth20 upper',out['results'][-1]['upper_bound'],flush=True)
