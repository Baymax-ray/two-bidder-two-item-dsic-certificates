"""Exact report witness: inherited stream sign cannot extend to h=1/2."""
import itertools,json
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
import flow_majorant as fm

def prove():
    _,theta,basis=fm.old.load_manifest();dp=fm.old.dp
    curl,_=fm.old.stream_components(theta,basis)
    assert all(e[0]>=1 for e in curl)
    divided={(e[0]-1,)+e[1:]:c for e,c in curl.items()}
    z,t,v0,v1=[dp.variable(i) for i in range(4)]
    s=dp.scale(z,Q(1,2));ss=dp.multiply(s,s)
    corr=dp.compose(divided,[s,dp.multiply(s,t),v0,v1])
    poly=dp.add(dp.add(dp.scale(ss,3),dp.scale(dp.ONE,-1)),dp.scale(dp.multiply(ss,corr),2))
    a=fm.old.fixed_controls(poly,fm.SCALE)
    stack=[(a,1,0,[(Q(0),Q(1))]*4)]
    while stack:
        a,e,depth,box=stack.pop()
        if int(a.max())+e<=0:continue
        for ix in itertools.product(*[(0,n-1) for n in a.shape]):
            if int(a[ix])>0:
                point=[box[j][int(ix[j]>0)] for j in range(4)]
                exact=Q(0)
                for ex,c in poly.items():
                    value=c
                    for q,n in zip(point,ex):value*=q**n
                    exact+=value
                assert exact>=Q(int(a[ix]),fm.SCALE)>Q(1,40)
                own=[point[0]/2,point[0]*point[1]/2]
                phi=exact/(2*own[0])
                return {'status':'EXACT_POSITIVE_VIRTUAL_WITNESS_PASS','own_report':list(map(str,own)),
                        'opponent_report':list(map(str,point[2:])), 'normalized_value':str(exact),
                        'virtual_value':str(phi),'normalized_lower_bound':'1/40',
                        'consequence':'The same inherited virtual value is positive on a relative neighborhood; the blanket nonpositive claim on [0,1/2]^2 is false.'}
        assert depth<10
        assert max(abs(int(a.min())),abs(int(a.max())))<2**62
        axis=int(np.argmax([int(np.max(np.abs(np.diff(a,axis=j)))) if a.shape[j]>1 else 0 for j in range(4)]))
        left,right,d=fm.old.split_floor(a,axis);mid=sum(box[axis])/2
        lb=box.copy();rb=box.copy();lb[axis]=(box[axis][0],mid);rb[axis]=(mid,box[axis][1])
        stack.append((right,e+d,depth+1,rb));stack.append((left,e+d,depth+1,lb))
    raise AssertionError('No positive witness')
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();result=prove()
    path=Path(__file__).parent/'flow_half_counterexample.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    else:assert result==json.loads(path.read_text())
    print(json.dumps(result,indent=2))
