"""Exact replay of a coupled continuous-box stress master solution.

The nonlinear virtual maximum may change winner. Each cell epigraph is a
proved continuous upper on that change, not a discrete objective proxy.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verifier'))
import master_algebra as a

def compact(raw):
    ids=sorted({c[k] for c in raw['columns'] for k in ('A','B')});renumber={x:j for j,x in enumerate(ids)}
    cols=[dict(c,A=renumber[c['A']],B=renumber[c['B']]) for c in raw['columns']]
    return dict(cells=[raw['cells'][i] for i in ids],columns=cols,amplitudes=raw['amplitudes'])

def calculate(raw):
    data=compact(raw);cells=data['cells'];cols=data['columns'];lam=list(map(F,data['amplitudes']))
    assert len(cols)==len(lam) and all(x>0 for x in lam)
    replay=[]
    for c in cells:
        C=tuple(map(F,c['center']));h=tuple(map(F,c['halfwidths']));r=a.record(C,h);assert r==c
        replay.append(r)
    separations=[]
    for j,k in combinations(range(len(cells)),2):
        c,d=cells[j],cells[k];C=list(map(F,c['center']));D=list(map(F,d['center']));h=list(map(F,c['halfwidths']));g=list(map(F,d['halfwidths']))
        sep=[n for n in range(4) if abs(C[n]-D[n])>=h[n]+g[n]];assert sep,(j,k)
        separations.append([j,k,sep[0]])
    degree=[0]*len(cells);kinds={'continuous_PSD':0,'axis_IC_kernel':0}
    for c in cols:
        x,y,i=c['A'],c['B'],c['bidder'];assert i in (0,1) and x!=y
        cx,cy=cells[x],cells[y];X=list(map(F,cx['center']));Y=list(map(F,cy['center']));h=list(map(F,cx['halfwidths']));g=list(map(F,cy['halfwidths']))
        assert h==g and X[2*(1-i):2*(1-i)+2]==Y[2*(1-i):2*(1-i)+2]
        assert cx['allocation'][i]==cy['allocation'][i]
        d=[X[2*i+j]-Y[2*i+j] for j in (0,1)];assert list(map(F,c['shift']))==d and any(d)
        degree[x]+=1;degree[y]+=1;kinds['continuous_PSD' if all(d) else 'axis_IC_kernel']+=1
    dd,tt,up=a.aggregate(cells,cols,lam);assert up<0
    # Simultaneous item exchange creates a disjoint second physical chart.
    assert {(p[1],p[0],p[3],p[2]):v for p,v in a.e.CORR[0].items()}==a.e.CORR[1]
    for c in cells:
        C=list(map(F,c['center']));h=list(map(F,c['halfwidths']))
        assert all(C[j]-h[j]>C[j+1]+h[j+1] for j in (0,2))
    for row in tt:assert len(row)==2
    return dict(status='COUPLED_COMPLEMENTARY_CONTINUOUS_MASTER_PASS',**data,
        exact_base_chart_change_upper=str(up),exact_base_chart_gain_lower=str(-up),item_symmetry_copies=2,
        exact_total_gain_lower=str(-2*up),theta=[[str(x) for x in row] for row in tt],
        aggregate_shifts=[[[str(x) for x in row] for row in side] for side in dd],
        overlapping_endpoint_cells=sum(n>1 for n in degree),max_active_columns_at_one_endpoint=max(degree),column_representations=kinds,
        base_chart_endpoint_separations=separations,incumbent_added_weighted_IC='0',incumbent_added_Hessian_slack='0',
        capacity_slack_change='0 on full-allocation endpoint cells',
        virtual_mismatch_decrease='at least exact_total_gain_lower; exact additional numerical enclosure kept separate',
        source_stream_manifest_sha256=sha256((a.e.p.ARCH/'manifest.json').read_bytes()).hexdigest(),
        frozen_primal_sha256=sha256((ROOT.parent/'V4_6_1_1_lower_bound/verifier/refined_candidate.py').read_bytes()).hexdigest(),
        reserved_V47_certificate_sha256=sha256((ROOT.parent/'V4_7/certificate/psd_local_certificate.json').read_bytes()).hexdigest(),
        reserved_V462_cycle_sha256=sha256((ROOT.parent/'V4_6_2_upper/certificate/sparse_cycle.json').read_bytes()).hexdigest(),
        scope='unrestricted randomized pointwise DSIC/IR upper decrease; finite master optimality is not global mechanism optimality')

if __name__=='__main__':
    path=ROOT/'certificate/master_certificate.json'
    raw=json.loads((ROOT/'certificate/master_candidate.json' if '--write' in sys.argv else path).read_text(encoding='utf-8'))
    out=calculate(raw)
    if '--write' in sys.argv:path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:assert out==raw
    print(out['status']);print('gain',out['exact_total_gain_lower']);print('display',float(F(out['exact_total_gain_lower'])));print('active_columns',len(out['columns']),'overlap_cells',out['overlapping_endpoint_cells'])
