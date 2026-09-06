"""Exact nonpositivity of bidder1 stream values on a low report square."""
import json
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
import flow_majorant as fm

def prove(cap=Q(2,5)):
    assert 0<cap<=1
    manifest,theta,basis=fm.old.load_manifest();dp=fm.old.dp
    curl,_=fm.old.stream_components(theta,basis)
    assert all(e[0]>=1 for e in curl)
    divided={(e[0]-1,)+e[1:]:c for e,c in curl.items()}
    s,z,v0,v1=[dp.variable(i) for i in range(4)]
    scaled_s=dp.scale(s,cap);ss=dp.multiply(scaled_s,scaled_s)
    records=[]
    for chart in (0,1):
        st=dp.multiply(scaled_s,z)
        own=(scaled_s,st) if chart==0 else (st,scaled_s)
        corr=dp.compose(divided,[own[0],own[1],v0,v1])
        poly=dp.add(dp.add(dp.scale(ss,3),dp.scale(dp.ONE,-1)),dp.scale(dp.multiply(ss,corr),2))
        a=fm.old.fixed_controls(poly,fm.SCALE)
        stack=[(a,1,0)];coverage=Q(0);nodes=0;leaves=0;maximum=-10**40;depthmax=0
        while stack:
            a,e,depth=stack.pop();nodes+=1
            if int(a.max())+e<=0:
                coverage+=Q(1,2**depth);leaves+=1;maximum=max(maximum,int(a.max())+e);depthmax=max(depthmax,depth);continue
            import itertools
            corners=[a[ix] for ix in itertools.product(*[(0,n-1) for n in a.shape])]
            assert max(corners)<=0, ('positive actual corner',chart,depth,int(max(corners)))
            assert depth<24,('sign not established',chart,depth,int(a.max())+e)
            assert max(abs(int(a.min())),abs(int(a.max())))<2**62
            axis=int(np.argmax([int(np.max(np.abs(np.diff(a,axis=j)))) if a.shape[j]>1 else 0 for j in range(4)]))
            l,r,d=fm.old.split_floor(a,axis)
            stack.append((r,e+d,depth+1));stack.append((l,e+d,depth+1))
        assert coverage==1
        records.append({'chart':chart,'nodes':nodes,'leaves':leaves,'max_depth':depthmax,'max_upper_control':maximum,'coverage':str(coverage)})
    return {'status':'EXACT_STREAM_SIGN_PASS','w_square':['0',str(cap)],'opponent_square':['0','1'],'scale':fm.SCALE,'records':records,'statement':'Both bidder1 virtual values are nonpositive whenever max(w)<=h, for all opponent reports, by own-chart proof and simultaneous item symmetry.'}
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--cap',default='2/5');ap.add_argument('--output',default='flow_sign_certificate.json');args=ap.parse_args();r=prove(Q(args.cap));print(json.dumps(r,indent=2))
    p=Path(__file__).parent/args.output
    if args.write:p.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    else:assert r==json.loads(p.read_text())
