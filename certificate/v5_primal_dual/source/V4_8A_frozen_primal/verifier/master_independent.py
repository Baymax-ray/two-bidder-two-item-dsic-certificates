"""Independent numerator, affine-cell, overlap, and epigraph verification."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from math import prod
import importlib.util,json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('independent_v47_master',ROOT.parent/'V4_7/verifier/independent_psd_first_event.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
c=F(157,500);q=F(1,2)-c;u=F(3421,10000)
def gg(x):return F(4,5)*(u-x) if c<=x<=u else F()
def price_values(lo,hi):
    nodes=[lo,hi]+[x for x in (c,u,F(1,2)) if lo<=x<=hi]
    vals=[(max(c,x)+gg(x),min(q,max(F(),x-c))) for x in nodes]
    if lo<c<=hi:vals.append((c,F()))
    return vals

def affine(C,h,alloc):
    margins=[]
    for i in (0,1):
        x,y,t,rho=C[2*i],C[2*i+1],C[2*(1-i)],C[2*(1-i)+1]
        hx,hy,ht,hr=h[2*i],h[2*i+1],h[2*(1-i)],h[2*(1-i)+1]
        assert x-hx>1-q and t-ht>1-q
        vals=price_values(rho-hr,rho+hr);fs=[z[0] for z in vals];ps=[z[1] for z in vals]
        if alloc[i]==['0','0']:
            m=[t-ht+min(ps)-x-hx,t-ht+min(fs)-x-hx-y-hy]
        else:
            assert alloc[i]==['1','1'];m=[x-hx+y-hy-t-ht-max(fs),y-hy-max(f-b for f,b in vals)]
        assert min(m)>=0;(margins.extend(m))
    return margins

def run():
    path=ROOT/'certificate/master_certificate.json';data=json.loads(path.read_text(encoding='utf-8'));cells=data['cells'];cols=data['columns'];lam=list(map(F,data['amplitudes']))
    correction=p.corrections();checkg=[];menus=[]
    source_paths={'source_stream_manifest_sha256':p.ARCH/'manifest.json',
        'frozen_primal_sha256':ROOT.parent/'V4_6_1_1_lower_bound/verifier/refined_candidate.py',
        'reserved_V47_certificate_sha256':ROOT.parent/'V4_7/certificate/psd_local_certificate.json',
        'reserved_V462_cycle_sha256':ROOT.parent/'V4_6_2_upper/certificate/sparse_cycle.json'}
    assert all(sha256(path.read_bytes()).hexdigest()==data[key] for key,path in source_paths.items())
    old=json.loads(source_paths['reserved_V47_certificate_sha256'].read_text())
    reserved=[(tuple(map(F,z['center'])),tuple(map(F,z['halfwidths']))) for w in old['witnesses'] for z in w['selected_symmetry_orbits']]
    old=json.loads(source_paths['reserved_V462_cycle_sha256'].read_text())
    reserved +=[(tuple(map(F,z)),tuple(map(F,old['halfwidths']))) for z in old['orbit_centers']]
    assert {((C[1],C[0],C[3],C[2]),(h[1],h[0],h[3],h[2])) for C,h in reserved}==set(reserved)
    for cell in cells:
        C=tuple(map(F,cell['center']));h=tuple(map(F,cell['halfwidths']));menus+=affine(C,h,cell['allocation'])
        assert all(z>0 for z in h) and all(0<x-z<x+z<1 for x,z in zip(C,h))
        assert str(prod(2*z for z in h))==cell['volume']
        assert all(C[j]-h[j]>C[j+1]+h[j+1] and C[j]-h[j]>F(43,100) for j in (0,2))
        assert all(any(abs(x-y)>v+w for x,y,v,w in zip(C,D,h,g)) for D,g in reserved)
        fs,D=p.fields(C,correction);dhi=2*(C[0]+h[0])**2*(C[2]+h[2])**2;L=[]
        for row in fs:
            opts=[{},p.centered(row[0],C),p.centered(row[1],C)];rr=[]
            for k in range(3):
                bounds=[p.bound(p.plus(opts[l],p.times(opts[k],-1)),h)[0] for l in range(3) if l!=k]
                rr.append(max(F(),max(bounds)/dhi))
            L.append(rr)
        assert [[str(x) for x in row] for row in L]==cell['gaps'];checkg.append(L)
    for ca,cb in combinations(cells,2):
        A=list(map(F,ca['center']));B=list(map(F,cb['center']));h=list(map(F,ca['halfwidths']));g=list(map(F,cb['halfwidths']))
        assert any(abs(x-y)>=v+w for x,y,v,w in zip(A,B,h,g))
    dd=[[[F(),F(),F()] for _ in (0,1)] for _ in cells]
    for col,z in zip(cols,lam):
        assert z>0;i=col['bidder'];ia,ib=col['A'],col['B'];ca,cb=cells[ia],cells[ib]
        assert ca['allocation'][i]==cb['allocation'][i] and ca['halfwidths']==cb['halfwidths']
        A=tuple(map(F,ca['center']));B=tuple(map(F,cb['center']));assert A[2*(1-i):2*(1-i)+2]==B[2*(1-i):2*(1-i)+2]
        d=[A[2*i+j]-B[2*i+j] for j in (0,1)];assert list(map(F,col['shift']))==d
        for j in (0,1):dd[ia][j][i+1]+=z*d[j];dd[ib][j][i+1]-=z*d[j]
    total=F();theta=[]
    for c,L,D in zip(cells,checkg,dd):
        row=[max(D[j][k]-L[j][k] for k in range(3)) for j in (0,1)];theta.append(row);total+=F(c['volume'])*sum(row,F())
    assert total<0 and str(-2*total)==data['exact_total_gain_lower']
    assert [[str(x) for x in row] for row in theta]==data['theta']
    out=dict(status='INDEPENDENT_COUPLED_MASTER_PASS',certificate_sha256=sha256(path.read_bytes()).hexdigest(),exact_total_gain_lower=str(-2*total),
        independent_cell_gap_reconstructions=len(cells),independent_affine_menu_inequalities=len(menus),independent_joint_epigraph_cells=2*len(cells),
        scope='separate stream reconstruction and sequential centering; separate BB macro-menu proof; exact aggregate epigraph evaluation')
    target=ROOT/'certificate/master_independent.json'
    if '--write' in sys.argv:target.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(target.read_text())==out
    print(out['status']);print('gain',out['exact_total_gain_lower'])
if __name__=='__main__':run()
