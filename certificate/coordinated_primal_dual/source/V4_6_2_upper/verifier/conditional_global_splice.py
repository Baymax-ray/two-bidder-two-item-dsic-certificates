"""Exact reusable-screening splice, certified by continuous virtual-slack integrals."""
from pathlib import Path
from fractions import Fraction as Q
from math import lcm,isqrt
import importlib.util,json,itertools,argparse,sys
if not __debug__: raise RuntimeError('Do not run this exact verifier with -O')
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
OLD=ROOT/'research/closed/two-bidder-two-item-dsic-certificates/certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound'
spec=importlib.util.spec_from_file_location('conditional_dp',OLD/'dual_polynomials.py')
dp=importlib.util.module_from_spec(spec);spec.loader.exec_module(dp)
A=Q(2,3); WMAX=Q(43,100)


def fields():
    m=json.loads((OLD/'manifest.json').read_text(encoding='utf8'))
    basis=[]
    for e in itertools.product(range(5),repeat=4):
        es=(e[1],e[0],e[3],e[2])
        if sum(e)<=4 and e<es: basis.append((e,es))
    assert [list(e) for e,_ in basis]==m['basis_order']
    x,y,z,r=map(dp.variable,range(4))
    P={}
    for th,(e,es) in zip(m['theta'],basis):
        P=dp.add(P,dp.scale(dp.add(dp.monomial(e),dp.scale(dp.monomial(es),-1)),Q(th)))
    boundary=dp.multiply(dp.multiply(x,dp.add(dp.ONE,dp.scale(x,-1))),dp.multiply(y,dp.add(dp.ONE,dp.scale(y,-1))))
    stream=dp.multiply(boundary,P)
    corr=[dp.derivative(stream,1),dp.scale(dp.derivative(stream,0),-1)]
    sub=[x,dp.multiply(x,y),z,r]
    # s*phi in radial chart v=(s,s*t), other report w kept Cartesian.
    b=dp.scale(dp.add(dp.scale(dp.multiply(x,x),3),dp.scale(dp.ONE,-1)),Q(1,2))
    polys=[dp.add(b,dp.multiply(x,dp.compose(corr[0],sub))),dp.add(dp.multiply(y,b),dp.multiply(x,dp.compose(corr[1],sub)))]
    avg=[]
    for poly in polys:
        out={}
        for e,c in poly.items():
            f=c*WMAX**(e[2]+1)*WMAX**(e[3]+1)/((e[2]+1)*(e[3]+1))
            out[e[:2]]=out.get(e[:2],Q(0))+f
        avg.append({e:c for e,c in out.items() if c})
    return avg,m


def independent_boole(avg,manifest):
    """Independent direct differentiation and degree-five rational quadrature."""
    basis=[]
    for e in itertools.product(range(5),repeat=4):
        es=(e[1],e[0],e[3],e[2])
        if sum(e)<=4 and e<es: basis.append((e,es))
    theta=list(map(Q,manifest['theta']))
    def direct(s,t,w1,w2):
        x=s;y=s*t;vals=(x,y,w1,w2)
        p=px=py=Q(0)
        for th,(e,es) in zip(theta,basis):
            for ex,sign in [(e,1),(es,-1)]:
                for axis in [-1,0,1]:
                    if axis>=0 and not ex[axis]: continue
                    term=th*sign*(ex[axis] if axis>=0 else 1)
                    for j,power in enumerate(ex): term*=vals[j]**(power-(j==axis))
                    if axis==-1: p+=term
                    elif axis==0: px+=term
                    else: py+=term
        c1=x*(1-x)*((1-2*y)*p+y*(1-y)*py)
        c2=-y*(1-y)*((1-2*x)*p+x*(1-x)*px)
        return ((3*s*s-1)/2+s*c1,(3*s*s-1)*t/2+s*c2)
    weights=[Q(v,90) for v in [7,32,12,32,7]]
    points=[(Q(1,3),Q(1,5)),(Q(3,5),Q(2,5)),(Q(4,5),Q(7,9))]
    for s,t in points:
        total=[Q(0),Q(0)]
        for i,wi in enumerate(weights):
            for j,wj in enumerate(weights):
                vals=direct(s,t,WMAX*i/4,WMAX*j/4)
                for k in range(2): total[k]+=WMAX**2*wi*wj*vals[k]
        for k in range(2):
            expected=sum(c*s**i*t**j for (i,j),c in avg[k].items())
            assert total[k]==expected
    return {'quadrature':'tensor Boole, exactly integrates opponent-coordinate degree<=4','rational_own_chart_points':[[str(s),str(t)] for s,t in points],'checked_fields':2}


def primitive(poly): return {(i+1,j+1):c/Q((i+1)*(j+1)) for (i,j),c in poly.items()}

def tabulate(primitives,n):
    den=lcm(*(c.denominator for p in primitives for c in p.values()))
    deg=max(sum(e) for p in primitives for e in p)
    integer=[{e:int(c*den)*n**(deg-sum(e)) for e,c in p.items()} for p in primitives]
    # Integer Horner evaluation per outer index; no floating arithmetic.
    tables=[]
    for p in integer:
        imax=max(i for i,j in p); jmax=max(j for i,j in p)
        table=[]
        for ii in range(n+1):
            coeff=[]
            for jj in range(jmax+1):
                val=0
                for i in range(imax,-1,-1): val=val*ii+p.get((i,jj),0)
                coeff.append(val)
            row=[]
            for jj in range(n+1):
                val=0
                for c in reversed(coeff): val=val*jj+c
                row.append(val)
            table.append(row)
        tables.append(table)
    return tables,den*n**deg


def root2_bounds(digits=40):
    scale=10**digits; lo=isqrt(2*scale*scale)
    assert lo*lo<2*scale*scale<(lo+1)*(lo+1)
    return Q(lo,scale),Q(lo+1,scale)

def select_cell(i,j,n,blo,bhi,klo,khi):
    # Chart 0: high s and low s*t. Cells are closed for inclusion tests;
    # boundaries have zero Lebesgue measure and are assigned exactly once.
    s0=Q(i,n);s1=Q(i+1,n);t0=Q(j,n);t1=Q(j+1,n)
    if s1<=A and s1*(1+t1)<=blo: return (0,0)
    if s0>=A and s1*t1<=klo: return (1,0)
    if s0*(1+t0)>=bhi and s0*t0>=khi: return (1,1)
    return None

def independent_cell_regions():
    """Check all selected coarse cells via all menu comparisons at corners."""
    slo,shi=root2_bounds();blo=(4-shi)/3;bhi=(4-slo)/3;klo=blo-A;khi=bhi-A
    assert select_cell(14,3,16,blo,bhi,klo,khi) is None
    assert select_cell(14,0,16,blo,bhi,klo,khi)==(1,0)
    tested=0
    for n in [8,16,32]:
        for i in range(n):
            for j in range(n):
                a=select_cell(i,j,n,blo,bhi,klo,khi)
                if a is None: continue
                idx={(0,0):0,(1,0):1,(1,1):3}[a]
                for si in [i,i+1]:
                    for tj in [j,j+1]:
                        x=Q(si,n);y=x*Q(tj,n)
                        # Utilities represented as rational plus coeff*sqrt2.
                        us=[(Q(0),Q(0)),(x-A,Q(0)),(y-A,Q(0)),(x+y-Q(4,3),Q(1,3))]
                        for q,c in us:
                            dq=us[idx][0]-q;dc=us[idx][1]-c
                            assert dq+dc*(slo if dc>=0 else shi)>=0
                tested+=1
    return {'all_corner_menu_comparisons':tested*16,'coarse_partitions':[8,16,32],'regression':'n16 cell(14,3) crosses low=k and must be omitted, despite sum>b0'}


def score(n,avg):
    s2lo,s2hi=root2_bounds();blo=(4-s2hi)/3;bhi=(4-s2lo)/3;klo=blo-A;khi=bhi-A
    tabs,den=tabulate([primitive(p) for p in avg],n)
    total=0; counts={'empty':0,'single':0,'bundle':0,'boundary_omitted':0,'positive_slack_cells':0}
    by_region={'empty':0,'single':0,'bundle':0}
    for i in range(n):
        for j in range(n):
            a=select_cell(i,j,n,blo,bhi,klo,khi)
            if a is None: counts['boundary_omitted']+=1; continue
            name={(0,0):'empty',(1,0):'single',(1,1):'bundle'}[a]
            counts[name]+=1
            vals=[t[i+1][j+1]-t[i][j+1]-t[i+1][j]+t[i][j] for t in tabs]
            gap=sum(max(0,v)-aa*v for aa,v in zip(a,vals))
            assert gap>=0
            total+=gap; by_region[name]+=gap
            if gap: counts['positive_slack_cells']+=1
    # Both own-item charts. Opponent W is symmetric, so item-swap is exact.
    return {'radial_partition':n,'one_sided_delta':str(Q(2*total,den)),'delta':str(Q(4*total,den)),'decimal_diagnostic':float(Q(4*total,den)),'counts':counts,'by_region':{k:str(Q(4*v,den)) for k,v in by_region.items()}}

def replay(levels=(16,32,64,128,256,512,1024)):
    avg,m=fields()
    independent=independent_boole(avg,m)
    cell_regions=independent_cell_regions()
    # Independent exact primitive differentiation identity.
    for p in avg:
        pp=primitive(p)
        assert {(i-1,j-1):c*i*j for (i,j),c in pp.items()}==p
    rows=[score(n,avg) for n in levels]
    assert all(Q(a['delta'])<=Q(b['delta']) for a,b in zip(rows,rows[1:]))
    s2lo,s2hi=root2_bounds()
    # SJA band support is zero on own W: x<A, y<Z, and ell(x)>=b0-WMAX>WMAX.
    assert WMAX<A and WMAX<Q(3,4) and (4-s2hi)/3>2*WMAX
    old=Q(3715139591287203,4194304000000000)
    for r in rows:
        r['upper_from_inherited_bound']=str(old-Q(r['delta']))
        r['upper_decimal_diagnostic']=float(old-Q(r['delta']))
        bound=(old-Q(r['delta']))*10**12
        r['simple_upper_rational']=str(Q(-(-bound.numerator//bound.denominator),10**12))
    return {'status':'PASS_EXACT_CONTINUOUS_SUPPORT_SPLICE','scope':'unrestricted randomized pointwise DSIC/IR; full continuous report-space upper, not a type grid','assumptions':['flow_sign_43_certificate.json proves inherited phi1<=0 on W=[0,43/100]^2','inherited polynomial stream revenue envelope is exact with u(0) slack','SJA full-capacity support and exact value are inherited continuum theorems'],'old_manifest_theta':m['theta'],'root2_enclosure':[str(x) for x in root2_bounds()],'independent_cell_region_check':cell_regions,'independent_integration_check':independent,'W_area':str(WMAX**2),'bidder_symmetry_factor':2,'support_zero_on_W_overlap':True,'SJA_value':'4/9+2*sqrt(2)/27','averaged_radial_fields':[{','.join(map(str,e)):str(c) for e,c in sorted(p.items())} for p in avg],'sequence':rows,'replay_boundary':'Exact arithmetic replays finite polynomial integral identities and nonnegative cellwise lower bounds; written continuum proofs establish universal screening validity and gap decomposition.'}

if __name__=='__main__':
    pa=argparse.ArgumentParser();pa.add_argument('--write',action='store_true');pa.add_argument('--max-level',type=int,default=1024);args=pa.parse_args()
    levels=tuple(n for n in [16,32,64,128,256,512,1024] if n<=args.max_level)
    result=replay(levels)
    target=HERE.parent/'certificate/conditional_global_splice.json'
    if args.write: target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    else: assert result==json.loads(target.read_text(encoding='utf8'))
    for row in result['sequence']: print(row['radial_partition'],row['delta'],row['upper_decimal_diagnostic'])
    print(result['status'])
