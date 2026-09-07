"""Frozen-field two-sided integration; no active bound or coefficients changed."""
from fractions import Fraction as Q
from pathlib import Path
from math import comb,isqrt
import argparse,hashlib,importlib.util,itertools,json,sys,time
import numpy as np
if not __debug__ or sys.flags.optimize: raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
UP=ROOT.parent/'V4_6_2_upper'
ARCH=ROOT.parents[3]/'research/closed/two-bidder-two-item-dsic-certificates/certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound'
SCALE=10**12;LIMIT=2**63-1;W=Q(43,100);A=Q(2,3)
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
archive=load('remainder_independent_polynomials',ARCH/'independent_replay.py')
sys.path.insert(0,str(ARCH))
old=load('remainder_primary_polynomials',ARCH/'verify_stream_dual.py')
dp=old.dp

def rational_controls(poly,degrees):
    work=np.empty(tuple(d+1 for d in degrees),dtype=object);work.fill(Q())
    for exponent,coefficient in poly.items():work[exponent]=coefficient
    for axis,d in enumerate(degrees):
        source=np.moveaxis(work,axis,0);target=np.empty_like(source)
        for j in range(d+1):
            row=np.empty(source.shape[1:],dtype=object);row.fill(Q())
            for e in range(j+1):row+=source[e]*Q(comb(j,e),comb(d,e))
            target[j]=row
        work=np.moveaxis(target,0,axis)
    return work

def controls(polys):
    ndim=len(next(iter(polys[0])))
    degrees=tuple(max(max(e[j] for e in p) for p in polys) for j in range(ndim))
    arrays=[]
    for p in polys:
        exact=rational_controls(p,degrees)
        vals=[int(v.numerator*SCALE//v.denominator) for v in exact.flat]
        assert max(map(abs,vals))*exact.size<LIMIT
        arrays.append(np.array(vals,dtype=np.int64).reshape(exact.shape))
    return arrays,degrees

def bisect(a,axis):
    m=np.moveaxis(a,axis,0);d=m.shape[0]-1;work=m.copy();left=np.empty_like(m);right=np.empty_like(m)
    left[0]=work[0];right[d]=work[d]
    for level in range(1,d+1):
        assert int(np.max(np.abs(work)))<=LIMIT//2
        work[:d-level+1]=(work[:d-level+1]+work[1:d-level+2])//2
        left[level]=work[0];right[d-level]=work[d-level]
    return np.moveaxis(left,0,axis),np.moveaxis(right,0,axis),d

def pos_bounds(a,e):
    n=a.size;lo=max(0,int(a.sum())//n)
    upper=np.maximum(0,a+e);hi=-(-int(upper.sum())//n)
    fixed=int(a.min())>=0 or int((a+e).max())<=0
    return lo,hi,fixed

def bounds(arrays,errors,mode):
    if mode=='max':
        a,b=arrays;ae,be=errors;n=a.size
        lower=max(0,int(a.sum())//n,int(b.sum())//n)
        upper=np.maximum(0,np.maximum(a+ae,b+be))
        high=-(-int(upper.sum())//n)
        fixed=(int(a.min())>=0 and int((a-b).min())>=be) or (int(b.min())>=0 and int((b-a).min())>=ae) or (int((a+ae).max())<=0 and int((b+be).max())<=0)
        return lower,high,fixed,[True,True]
    rows=[pos_bounds(a,e) for a,e in zip(arrays,errors)]
    return sum(v[0] for v in rows),sum(v[1] for v in rows),all(v[2] for v in rows),[not v[2] for v in rows]

def choose_axis(arrays,active):
    scores=[]
    for axis in range(arrays[0].ndim):
        scores.append(max((int(np.max(np.abs(np.diff(a,axis=axis)))) for a,on in zip(arrays,active) if on and a.shape[axis]>1),default=-1))
    return int(np.argmax(scores))

def tree(polys,depth,mode,chart_tag='',regional_depth=6):
    arrays,degrees=controls(polys);ndim=arrays[0].ndim;unit=1<<depth
    box=tuple((0,unit) for _ in range(ndim));stack=[(arrays,[1]*len(arrays),0,'',box)]
    total=[0,0];coverage=0;stats=dict(nodes=0,fixed=0,terminal=0,max_error=1);regions={};start=time.monotonic()
    while stack:
        arrays,errors,level,path,box=stack.pop();stats['nodes']+=1;stats['max_error']=max(stats['max_error'],*errors)
        lo,hi,fixed,active=bounds(arrays,errors,mode)
        assert 0<=lo<=hi
        if fixed or level==depth:
            weight=1<<(depth-level);coverage+=weight;total[0]+=lo*weight;total[1]+=hi*weight
            stats['fixed' if fixed else 'terminal']+=1
            key=path[:regional_depth]
            if key not in regions:regions[key]=dict(lower_units=0,upper_units=0,coverage_units=0,leaves=0)
            row=regions[key];row['lower_units']+=lo*weight;row['upper_units']+=hi*weight;row['coverage_units']+=weight;row['leaves']+=1
            if level<=regional_depth:row['box_units']=box
        else:
            axis=choose_axis(arrays,active);children=[bisect(a,axis) for a in arrays]
            new_errors=[e+d for e,(_,_,d) in zip(errors,children)]
            midpoint=sum(box[axis])//2
            leftbox=list(box);rightbox=list(box);leftbox[axis]=(box[axis][0],midpoint);rightbox[axis]=(midpoint,box[axis][1])
            if level+1==regional_depth:
                for bit,bb in [('0',leftbox),('1',rightbox)]:
                    regions[path+bit]=dict(lower_units=0,upper_units=0,coverage_units=0,leaves=0,box_units=tuple(bb))
            stack.append(([p[1] for p in children],new_errors,level+1,path+'1',tuple(rightbox)))
            stack.append(([p[0] for p in children],new_errors,level+1,path+'0',tuple(leftbox)))
        if stats['nodes']%100000==0:print('remainder tree',chart_tag,stats['nodes'],'seconds',round(time.monotonic()-start,1),flush=True)
    assert coverage==unit
    assert sum(v['coverage_units'] for v in regions.values())==unit
    assert [sum(v[k] for v in regions.values()) for k in ('lower_units','upper_units')]==total
    for path,row in regions.items():
        row['path']=path;row['box']=[[str(Q(x,unit)) for x in interval] for interval in row.pop('box_units')]
        row['integral']=[str(Q(row['lower_units'],SCALE*unit)),str(Q(row['upper_units'],SCALE*unit))]
    out=dict(tag=chart_tag,depth=depth,mode=mode,degrees=list(degrees),statistics=stats,coverage=coverage,lower=str(Q(total[0],SCALE*unit)),upper=str(Q(total[1],SCALE*unit)),regions=list(regions.values()))
    print('remainder finished',chart_tag,'bounds',float(Q(out['lower'])),float(Q(out['upper'])),'seconds',round(time.monotonic()-start,1),flush=True)
    return out

def full_splice_polynomials(theta,basis):
    corr=old.stream_components(theta,basis);s,t,z,r=map(dp.variable,range(4))
    sub=[s,dp.multiply(s,t),dp.scale(z,W),dp.scale(r,W)]
    base=dp.scale(dp.add(dp.scale(dp.multiply(s,s),3),dp.scale(dp.ONE,-1)),Q(1,2))
    return [dp.add(base,dp.multiply(s,dp.compose(corr[0],sub))),dp.add(dp.multiply(t,base),dp.multiply(s,dp.compose(corr[1],sub)))]

def average(polys):
    result=[]
    for p in polys:
        avg={}
        for e,c in p.items():avg[e[:2]]=avg.get(e[:2],Q())+W*W*c/Q((e[2]+1)*(e[3]+1))
        result.append({e:c for e,c in avg.items() if c})
    return result

def sqrt2_interval():
    scale=10**40;n=isqrt(2*scale*scale);assert n*n<2*scale*scale<(n+1)**2
    return Q(n,scale),Q(n+1,scale)

def interval_data(lo,hi):
    assert lo<=hi
    return dict(lower=str(lo),upper=str(hi),lower_decimal=float(lo),upper_decimal=float(hi))

def calculate(depth_b=20,depth_d=20,depth_avg=24):
    start=time.monotonic();manifest,theta,basis=archive.load_manifest()
    primary=json.loads((UP/'flow_majorant_certificate.json').read_text(encoding='utf-8'))
    splice=json.loads((UP/'certificate/conditional_global_splice.json').read_text(encoding='utf-8'))
    B20=Q(primary['results'][-1]['upper_bound']);Delta=Q(splice['sequence'][-1]['delta'])
    charts=[]
    for i,j in itertools.product((0,1),repeat=2):charts.append(tree(archive.chart_competitors(theta,basis,i,j),depth_b,'max',f'B{i}{j}'))
    blo=2*sum(Q(x['lower']) for x in charts);bhi=2*sum(Q(x['upper']) for x in charts)
    if depth_b in [12,14,16,18,20]:assert bhi==Q(next(r['upper_bound'] for r in primary['results'] if r['depth']==depth_b))
    polys=full_splice_polynomials(theta,basis);avg=average(polys)
    assert [{','.join(map(str,e)):str(c) for e,c in sorted(p.items())} for p in avg]==splice['averaged_radial_fields']
    dtree=tree(polys,depth_d,'positive','D_full')
    atree=tree(avg,depth_avg,'positive','D_averaged')
    sqlo,sqhi=sqrt2_interval();rlo=Q(4,9)+2*sqlo/27;rhi=Q(4,9)+2*sqhi/27
    dlo=4*W*W*Q(dtree['lower'])-2*W*W*rhi;dhi=4*W*W*Q(dtree['upper'])-2*W*W*rlo
    alo=4*Q(atree['lower'])-2*W*W*rhi;ahi=4*Q(atree['upper'])-2*W*W*rlo
    dlo=max(dlo,Delta,alo);alo=max(alo,Delta);assert dlo<=dhi and alo<=ahi
    eblo=max(0,B20-bhi);ebhi=B20-blo
    edlo=dlo-Delta;edhi=dhi-Delta
    out=dict(status='FROZEN_NUMERICAL_REMAINDER_ENCLOSURE_PASS',scope='Frozen amplitude-one field and existing support splice only; no new mechanism, coefficients, dual or active bound',scale=SCALE,
        settings=dict(depth_B=depth_b,depth_D=depth_d,depth_averaged=depth_avg,regional_path_depth=6),
        frozen_B20=str(B20),frozen_Delta1024=str(Delta),B=interval_data(blo,min(B20,bhi)),D=interval_data(dlo,dhi),D_averaged=interval_data(alo,ahi),
        B_error=interval_data(eblo,ebhi),D_error=interval_data(edlo,edhi),
        opponent_averaging_loss=interval_data(max(0,dlo-ahi),dhi-alo),
        own_cell_and_omission_loss=interval_data(max(0,alo-Delta),ahi-Delta),
        total_E=interval_data(eblo+edlo,ebhi+edhi),
        B_charts=charts,D_tree=dtree,averaged_tree=atree,
        dependencies={str(p.relative_to(ROOT.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [UP/'flow_majorant_certificate.json',UP/'certificate/conditional_global_splice.json']},
        archive_dependencies={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ARCH/'manifest.json',ARCH/'independent_replay.py',ARCH/'verify_stream_dual.py',ARCH/'dual_polynomials.py']})
    print('global E',out['total_E'],'elapsed',round(time.monotonic()-start,1),flush=True)
    return out

if __name__=='__main__':
    pa=argparse.ArgumentParser();pa.add_argument('--depth-b',type=int,default=20);pa.add_argument('--depth-d',type=int,default=20);pa.add_argument('--depth-avg',type=int,default=24);pa.add_argument('--output',default='numerical_remainder.json');pa.add_argument('--write',action='store_true');args=pa.parse_args()
    result=calculate(args.depth_b,args.depth_d,args.depth_avg);target=ROOT/'certificate'/args.output
    assert target.resolve().parent==(ROOT/'certificate').resolve()
    if args.write:target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(target.read_text(encoding='utf-8'))==result
    print(result['status'],flush=True)
