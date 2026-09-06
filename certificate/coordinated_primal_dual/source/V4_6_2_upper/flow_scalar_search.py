"""Discovery: optimize a fixed-partition continuous Bernstein majorant in stream amplitude."""
from pathlib import Path
import json,time
from fractions import Fraction as Q
import numpy as np
import flow_majorant as fm

LO=1.;HI=1.03;DEPTH=18

def splitf(a,axis):
    degree=a.shape[axis]-1
    m=np.moveaxis(a,axis,0);w=m.copy();l=np.empty_like(m);r=np.empty_like(m)
    l[0]=w[0];r[degree]=w[degree]
    for lev in range(1,degree+1):
        w[:degree-lev+1]=(w[:degree-lev+1]+w[1:degree-lev+2])/2
        l[lev]=w[0];r[degree-lev]=w[degree-lev]
    return np.moveaxis(l,0,axis),np.moveaxis(r,0,axis)

def run():
    manifest,theta,basis=fm.old.load_manifest();events=[];slope=0.;value=0.;start=time.time();leaves=0
    for c1,c2 in ((0,0),(0,1),(1,0),(1,1)):
        af,bf=fm.root_controls(*fm.old.competitors(theta,basis,c1,c2))
        # Degree elevation differs for zero stream; explicitly reconstruct on full dimensions.
        deg=tuple(x-1 for x in af.shape)
        p0=fm.old.competitors([Q(0)]*len(theta),basis,c1,c2)
        a0=np.array(fm.common_exact(p0[0],deg),dtype=float);b0=np.array(fm.common_exact(p0[1],deg),dtype=float)
        da=af/fm.SCALE-a0;db=bf/fm.SCALE-b0
        stack=[(a0,da,b0,db,0)]
        while stack:
            a,da,b,db,depth=stack.pop()
            al=a+LO*da;ah=a+HI*da;bl=b+LO*db;bh=b+HI*db
            fixed=(np.min(al)>=0 and np.min(ah)>=0 and np.min(al-bl)>=0 and np.min(ah-bh)>=0) or (np.min(bl)>=0 and np.min(bh)>=0 and np.min(bl-al)>=0 and np.min(bh-ah)>=0) or (np.max(al)<=0 and np.max(ah)<=0 and np.max(bl)<=0 and np.max(bh)<=0)
            if depth==DEPTH or fixed:
                leaves+=1;weight=2.**(-depth)/a.size
                winner=np.argmax(np.stack([np.zeros_like(a),al,bl]),axis=0)
                slope+=weight*np.sum(np.where(winner==1,da,np.where(winner==2,db,0)))
                value+=weight*np.maximum(np.maximum(al,bl),0).sum()
                for aa,dd,othera,otherd,kind in ((a,da,b,db,0),(b,db,a,da,0),(a-b,da-db,a,da,1)):
                    valid=np.abs(dd)>1e-16
                    t=np.zeros_like(dd);np.divide(-aa,dd,out=t,where=valid)
                    valid&=(t>LO)&(t<HI)
                    oth=othera+t*otherd
                    valid&=(oth<=0) if kind==0 else (oth>=0)
                    if np.any(valid):events.append((t[valid].ravel(),(np.abs(dd[valid])*weight).ravel()))
                continue
            scores=[max(np.max(np.abs(np.diff(a+da,axis=j))),np.max(np.abs(np.diff(b+db,axis=j)))) for j in range(4)]
            axis=int(np.argmax(scores));sp=[splitf(v,axis) for v in (a,da,b,db)]
            stack.append(tuple(v[1] for v in sp)+(depth+1,));stack.append(tuple(v[0] for v in sp)+(depth+1,))
        print('chart',c1,c2,'leaves',leaves,'secs',time.time()-start,flush=True)
    ts=np.concatenate([x[0] for x in events]);ws=np.concatenate([x[1] for x in events]);order=np.argsort(ts);ts=ts[order];ws=ws[order]
    cumulative=slope+np.cumsum(ws);ix=int(np.searchsorted(cumulative,0))
    opt=LO if slope>=0 else (HI if ix>=len(ts) else ts[ix]);candidate=Q(float(opt)).limit_denominator(1000000)
    chosen=ts<opt;vopt=value+slope*(opt-LO)+np.sum(ws[chosen]*(opt-ts[chosen]))
    result={'status':'NUMERICAL_DISCOVERY_ONLY','objective':'fixed-partition continuous Bernstein majorant, not a type-grid LP','depth':DEPTH,'amplitude_interval':[LO,HI],'optimum_amplitude':opt,'rational_trial_amplitude':str(candidate),'objective_value_times_item_symmetry':float(2*vopt),'initial_slope':float(slope),'events':len(ts),'leaves':leaves}
    print(json.dumps(result,indent=2));(Path(__file__).parent/'flow_scalar_discovery.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':run()
