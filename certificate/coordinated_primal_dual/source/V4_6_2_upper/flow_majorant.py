"""Exact coefficientwise Bernstein-majorant integration of a continuous stream dual."""
from fractions import Fraction as Q
from pathlib import Path
import argparse, hashlib, importlib.util, json, sys, time
import numpy as np
if not __debug__: raise RuntimeError('Do not use python -O.')
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[3]/'research/closed/two-bidder-two-item-dsic-certificates/certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound'
sys.path.insert(0,str(BASE))
spec=importlib.util.spec_from_file_location('inherited_stream',BASE/'verify_stream_dual.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
SCALE=10**12

def common_exact(poly, degrees):
    import math
    out=np.empty(tuple(d+1 for d in degrees),dtype=object)
    for ix in np.ndindex(out.shape):
        val=Q(0)
        for ex,c in poly.items():
            if all(e<=j for e,j in zip(ex,ix)):
                z=c
                for e,j,d in zip(ex,ix,degrees): z*=Q(math.comb(j,e),math.comb(d,e))
                val+=z
        out[ix]=val
    return out

def root_controls(first,second):
    deg=tuple(max(max((e[j] for e in p),default=0) for p in (first,second)) for j in range(4))
    roots=[]
    for poly in (first,second):
        ex=common_exact(poly,deg)
        out=np.empty(ex.shape,dtype=np.int64)
        for ix in np.ndindex(ex.shape):
            v=ex[ix];fixed=v.numerator*SCALE//v.denominator
            assert -(2**63-1)<=fixed<=2**63-1
            out[ix]=fixed
        roots.append(out)
    return roots

def majorant(a,ae,b,be):
    # Each array is a lower approximation, exact coefficient is in [a,a+ae].
    # Pointwise max is below the Bernstein polynomial with controls max(0,a+ae,b+be).
    assert a.shape==b.shape and ae>=0 and be>=0
    ma=max(abs(int(a.min())),abs(int(a.max())))
    mb=max(abs(int(b.min())),abs(int(b.max())))
    assert ma+ae<2**63 and mb+be<2**63 and ma+mb<2**63
    upper=np.maximum(np.maximum(a+ae,b+be),0)
    assert int(np.max(np.abs(upper)))*upper.size < 2**63
    val=(int(upper.sum())+upper.size-1)//upper.size
    awin=int(a.min())>=0 and int((a-b).min())>=be
    bwin=int(b.min())>=0 and int((b-a).min())>=ae
    zero=int((a+ae).max())<=0 and int((b+be).max())<=0
    return val, awin or bwin or zero

def split(a,axis):
    return old.split_floor(a,axis)

def axis_select(a,b):
    assert max(abs(int(a.min())),abs(int(a.max())),abs(int(b.min())),abs(int(b.max())))<2**62
    scores=[]
    for j in range(4):
        scores.append(max(int(np.max(np.abs(np.diff(a,axis=j)))),int(np.max(np.abs(np.diff(b,axis=j))))))
    return int(np.argmax(scores))

def certify(depths, amplitude=Q(1)):
    manifest,theta,basis=old.load_manifest()
    theta=[amplitude*t for t in theta]
    depths=sorted(set(depths));assert depths and all(type(d) is int and 0<=d<=30 for d in depths);D=max(depths)
    accum={d:0 for d in depths};cover={d:0 for d in depths}
    stats={'nodes':0,'fixed':0,'leaves':0,'max_error':1}
    start=time.time()
    for c1,c2 in ((0,0),(0,1),(1,0),(1,1)):
        polys=old.competitors(theta,basis,c1,c2)
        a,b=root_controls(*polys)
        assert a.shape==b.shape
        stack=[(a,1,b,1,0)]
        while stack:
            a,ae,b,be,level=stack.pop();stats['nodes']+=1
            stats['max_error']=max(stats['max_error'],ae,be)
            bound,fixed=majorant(a,ae,b,be)
            for d in depths:
                if level==d or (fixed and level<d):
                    accum[d]+=bound*(1<<(d-level));cover[d]+=1<<(d-level)
            if fixed:stats['fixed']+=1;continue
            if level==D:stats['leaves']+=1;continue
            axis=axis_select(a,b)
            al,ar,ad=split(a,axis);bl,br,bd=split(b,axis)
            stack.append((ar,ae+ad,br,be+bd,level+1))
            stack.append((al,ae+ad,bl,be+bd,level+1))
        print('chart',c1,c2,'elapsed',round(time.time()-start,1),'nodes',stats['nodes'],flush=True)
    results=[]
    incumbent=Q(3715139591287203,4194304000000000)
    for d in depths:
        assert cover[d]==4*(1<<d)
        bound=Q(2*accum[d],SCALE*(1<<d))
        incumbent=min(incumbent,bound)
        results.append({'depth':d,'accumulator':str(accum[d]),'coverage':cover[d],
                        'upper_bound':str(bound),'upper_decimal':float(bound),
                        'monotone_incumbent':str(incumbent)})
    return {'status':'EXACT_CONTINUOUS_BOUND_PASS','scale':SCALE,'method':'coefficientwise Bernstein convex majorant',
            'amplitude':str(amplitude),'results':results,'statistics':stats,'seconds':time.time()-start,
            'dependencies':{f:hashlib.sha256((BASE/f).read_bytes()).hexdigest() for f in ('manifest.json','verify_stream_dual.py','dual_polynomials.py')}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--depths',nargs='+',type=int);ap.add_argument('--write',action='store_true');ap.add_argument('--amplitude',default='1');ap.add_argument('--output',default='flow_majorant_certificate.json');args=ap.parse_args()
    saved_path=HERE/args.output
    saved=json.loads(saved_path.read_text(encoding='utf-8')) if saved_path.exists() else None
    depths=args.depths or ([r['depth'] for r in saved['results']] if saved else [12,14,16])
    result=certify(depths,Q(args.amplitude))
    print(json.dumps(result,indent=2))
    if args.write:saved_path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    else:
        assert saved is not None, 'No saved certificate; use --write only for authorized generation.'
        for k,v in result.items():
            if k!='seconds':assert v==saved[k], ('certificate mismatch',k)
        print('SAVED_CERTIFICATE_MATCH_PASS')
