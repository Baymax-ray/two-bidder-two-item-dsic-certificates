"""Fresh exact face audit: scalar menus, Bernstein branch proofs, rational cubature.

No V5 or predecessor calculator is imported. Accepted t strips are only a
subdivision proposal; all ordering and menu-selection predicates are certified
again on each complete curved cell. Cubature is exact for a proved degree bound.
"""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
from hashlib import sha256
import json
import sys
import time

assert __debug__ and not sys.flags.optimize
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
V5=BASE/'V5_gap_closure'
A=F(2,3); d=F(1,2); c=F(157,500); q=d-c; u=F(3421,10000); sig=F(4,5)
a=A+q*q/2; b=a+c; s0=a+d; T=1-F(2,3)*c; U=F(5,3)-2*c
H=1-q; jump=sig*(u-c); J=u+q; bh=F(861928812542301,10**15)
predicate_count=0
cell_count=0

def const(v):
    return lambda t,r: F(v)

def certified_sign(fn,lo,hi,L,R,nonnegative=True):
    """Every tested fn is affine in r and quadratic in t at most.
    Substitution of a quadratic boundary stays quadratic. Its three exact
    Bernstein coefficients bound it on the whole interval, not just samples.
    """
    global predicate_count
    for boundary in (L,R):
        vals=[fn(t,boundary(t))*(1 if nonnegative else -1) for t in (lo,(lo+hi)/2,hi)]
        controls=[vals[0],2*vals[1]-(vals[0]+vals[2])/2,vals[2]]
        assert min(controls)>=0, ('branch/order sign', str(lo),str(hi),list(map(str,controls)))
        predicate_count+=1

def make_menu(lo,hi,L,R):
    tm=(lo+hi)/2; rm=(L(tm)+R(tm))/2
    def check(fn,positive=True):
        certified_sign(fn,lo,hi,L,R,positive)
    def test(fn):
        yes=fn(tm,rm)>=0
        check(fn,yes)
        return yes
    def pick(functions,maximum=True):
        index=(max if maximum else min)(range(len(functions)),key=lambda i:functions[i](tm,rm))
        chosen=functions[index]
        for other in functions:
            check(lambda t,r,f=chosen,g=other:f(t,r)-g(t,r),maximum)
        return chosen
    # Freeze branches only after proving their predicates on the entire cell.
    small_t=test(lambda t,r:A-t)
    low_sum=test(lambda t,r:b-t-r) if small_t else False
    is_e=False
    if small_t and low_sum:
        P=const(A)
        if test(lambda t,r:d-t):
            B=const(A); C=pick([const(bh),lambda t,r:t+r])
        else:
            if test(lambda t,r:d+jump-t):
                k=const(c)
            elif test(lambda t,r:J-t):
                k=lambda t,r:(t-q-sig*u)/(1-sig)
            else:
                k=lambda t,r:t-q
            C=pick([lambda t,r:F(5,6)+F(3,4)*k(t,r)**2,lambda t,r:t+r])
            B=pick([const(A),lambda t,r:C(t,r)-k(t,r)],False)
    else:
        above_a=test(lambda t,r:t-A)
        below_t=test(lambda t,r:T-t)
        below_c=test(lambda t,r:c-r)
        if above_a and below_t and below_c:
            is_e=True
            de=lambda t,r:F(9,16)*(T-t)*(U-t)
            P=lambda t,r:t
            B=lambda t,r:d+de(t,r)
            C=lambda t,r:t+c+de(t,r)
        else:
            hc=pick([const(0),lambda t,r:t-a,lambda t,r:t+r-b])
            pbase=pick([const(a),lambda t,r:s0-r],False)
            bbase=pick([const(a),lambda t,r:s0-t],False)
            above_c=test(lambda t,r:r-c)
            below_u=test(lambda t,r:u-r)
            fee=(lambda t,r:sig*(u-r)) if above_c and below_u else const(0)
            P=lambda t,r:hc(t,r)+pbase(t,r)
            B=lambda t,r:hc(t,r)+bbase(t,r)+fee(t,r)
            C=lambda t,r:hc(t,r)+b+fee(t,r)
    P=pick([P,const(1)],False); B=pick([B,const(1)],False)
    for predicate in (P,B,lambda t,r:1-P(t,r),lambda t,r:1-B(t,r),
                      lambda t,r:C(t,r)-P(t,r),lambda t,r:C(t,r)-B(t,r),
                      lambda t,r:P(t,r)+B(t,r)-C(t,r)):
        check(predicate)
    def moments(t,r):
        pp,bb,cc=P(t,r),B(t,r),C(t,r)
        scarce=(1-pp)*(cc-pp); safe=(1-bb)*(cc-bb)
        bundle=(1-cc+bb)*(1-cc+pp)-(pp+bb-cc)**2/2
        rev=pp*scarce+bb*safe+cc*bundle
        number=scarce+safe+2*bundle
        if is_e:
            delta=F(9,16)*(T-t)*(U-t); halfalpha=(3*t-2)/2
            width=delta+halfalpha; z=1-t
            # Integrate lottery and displaced deterministic regions directly;
            # cancel beta=a/width before evaluation, including zero-width ends.
            newN=(width+halfalpha)*(z+halfalpha/2)
            oldN=z*delta+2*z*halfalpha+halfalpha**2
            newR=(t*width+halfalpha*c)*(z+halfalpha/2)
            oldR=t*z*delta+(t+c+delta)*(z*halfalpha+halfalpha**2/2)
            assert newN-oldN==(3*t-2)*delta/4
            assert newR-oldR==(3*t-2)**2*delta/8
            number+=newN-oldN; rev+=newR-oldR
        return number,pp*(1-pp)+bb*(1-bb),2-pp-bb,rev,bb
    return moments

def cut_curves(mid):
    curves=[lambda t:F(0),lambda t:t,lambda t:c,lambda t:u,lambda t:d,
            lambda t:H,lambda t:b-t,lambda t:1+c-t]
    if mid<=A:
        if mid<=d:
            curves.append(lambda t:bh-t)
        else:
            if mid<=d+jump:k=lambda t:c
            elif mid<J:k=lambda t:(t-q-sig*u)/(1-sig)
            else:k=lambda t:t-q
            curves.extend([lambda t:F(5,6)+F(3,4)*k(t)**2-t,lambda t:A+k(t)-t])
    unique={tuple(fn(t) for t in (F(0),F(1,2),F(1))):fn for fn in curves}
    return sorted(unique.values(),key=lambda fn:fn(mid))

def rule(degree):
    """Integrate rational Lagrange basis on [0,1]; prove all monomial moments."""
    nodes=[F(i,degree) for i in range(degree+1)];weights=[]
    for i,x in enumerate(nodes):
        poly=[F(1)]
        for j,y in enumerate(nodes):
            if i==j:continue
            nxt=[F(0)]*(len(poly)+1)
            for k,z in enumerate(poly):
                nxt[k]-=z*y/(x-y);nxt[k+1]+=z/(x-y)
            poly=nxt
        weights.append(sum((z/(k+1) for k,z in enumerate(poly)),F(0)))
    for k in range(degree+1):
        assert sum((w*x**k for w,x in zip(weights,nodes)),F(0))==F(1,k+1)
    return list(zip(nodes,weights))

X=rule(8); Y=rule(2)

def rectangle_moments(lo,hi,L,R,menu):
    # P,B,C after r=L(t)+(R(t)-L(t))*y: t-degree<=2, y-degree<=1.
    # N,G,S times Jacobian: t-degree<=6, y-degree<=2. Degree8/2 suffices.
    result=[F(0)]*3
    for x,wx in X:
        t=lo+(hi-lo)*x; left=L(t); width=R(t)-left
        for y,wy in Y:
            vals=menu(t,left+width*y)
            for k in range(3):result[k]+=wx*wy*(hi-lo)*width*vals[k]
    return result

def line_moments():
    nodes=[F(0),d,d+jump,J,A,T,F(1)]
    sums=[F(0)]*4
    for lo,hi in zip(nodes,nodes[1:]):
        menu=make_menu(lo,hi,lambda t:F(0),lambda t:F(0))
        for x,w in X:
            t=lo+(hi-lo)*x; nn,gg,ss,rev,bb=menu(t,F(0))
            for j,value in enumerate([rev,nn,2*bb*(1-bb),2*(1-bb)]):
                sums[j]+=(hi-lo)*w*value
    return dict(zip(['Rfull','Nfull','Rcross','Ncross'],sums))

def decimal(q,up=False,places=30):
    q=F(q);scale=10**places
    integer=-((-q*scale).numerator//(-q*scale).denominator) if up else (q*scale).numerator//(q*scale).denominator
    sign='-' if integer<0 else '';whole,frac=divmod(abs(integer),scale)
    return f'{sign}{whole}.{frac:0{places}d}'

def interval_output(pair):
    return dict(exact=list(map(str,pair)),decimal=[decimal(pair[0]),decimal(pair[1],True)])

def main():
    global cell_count
    started=time.monotonic()
    face_path=V5/'certificate/primal_face_integrals.json'
    faces=json.loads(face_path.read_text())
    ranges=[tuple(map(F,row[:2])) for row in faces['resolved_t_intervals']]
    missing=[tuple(map(F,row)) for row in faces['unresolved_t_intervals']]
    cover=sorted(ranges+missing)
    assert cover[0][0]==0 and cover[-1][1]==1
    assert all(lo<hi for lo,hi in cover)
    assert all(x[1]==y[0] for x,y in zip(cover,cover[1:]))
    total=[F(0)]*3
    for index,(lo,hi) in enumerate(ranges):
        mid=(lo+hi)/2;cuts=cut_curves(mid);pieces=0
        for left,right in zip(cuts,cuts[1:]):
            certified_sign(lambda t,r:left(t)-right(t),lo,hi,left,right,False)
            if not 0<(left(mid)+right(mid))/2<mid:continue
            menu=make_menu(lo,hi,left,right)
            part=rectangle_moments(lo,hi,left,right,menu)
            total=[x+y for x,y in zip(total,part)];pieces+=1;cell_count+=1
        assert pieces==faces['resolved_t_intervals'][index][2]
        if (index+1)%50==0:print('independent strips',index+1,flush=True)
    area=sum(((hi*hi-lo*lo)/2 for lo,hi in missing),F(0))
    assert str(area)==faces['unresolved_ordered_opponent_area']
    one=line_moments();error=F(1,10**12)
    assert bh>0 and 4-3*(bh+F(1,10**15))>0
    assert (4-3*bh)**2>2>(4-3*(bh+F(1,10**15)))**2
    assert error>=F(10,10**15) and error>=F(8,10**15)
    rebuilt={'N4':[4*total[0]-error,4*total[0]+8*area+error],
             'R3':[one['Rfull']+total[1]-error,one['Rfull']+total[1]+area/2+error],
             'N3':[one['Nfull']+total[2]-error,one['Nfull']+total[2]+2*area+error]}
    for key in ('Rcross','Ncross'):rebuilt[key]=[one[key]-error,one[key]+error]
    sja=make_menu(F(0),F(0),lambda t:F(0),lambda t:F(0))(F(0),F(0))
    rebuilt['RSJA']=[sja[3]-error,sja[3]+error]
    rebuilt['NSJA']=[sja[0]-error,sja[0]+error]
    rebuilt.update(Rsame=[F(31,81)]*2,Nsame=[F(5,9)]*2,Rone=[F(2,9)]*2,N_one=[F(1,3)]*2)
    claimed={k:list(map(F,v)) for k,v in faces['moment_enclosures'].items()}
    for key,pair in rebuilt.items():assert pair==claimed[key],key
    # Independent integer-square-root brackets for the inherited radical R4.
    old=json.loads((BASE/'V4_8B_support_redesign/certificate/phase_ledger.json').read_text())
    co=list(map(F,old['preserved_lower_coefficients']));scale=10**70
    radicals=[]
    for rad in (2,493894):
        n=isqrt(rad*scale*scale);assert n*n<=rad*scale*scale<(n+1)*(n+1)
        radicals.append([F(n,scale),F(n+1,scale)])
    r4=[co[0]+sum((coeff*box[0 if coeff>=0 else 1] for coeff,box in zip(co[1:],radicals)),F(0)),
        co[0]+sum((coeff*box[1 if coeff>=0 else 0] for coeff,box in zip(co[1:],radicals)),F(0))]
    assert claimed['R4'][0]<=r4[0]<=r4[1]<=claimed['R4'][1]
    rebuilt['R4']=claimed['R4']
    tau=F(1,100);s=1-tau
    output=[]
    for side in (0,1):
        acc=F(0)
        for mask in range(16):
            zero=[i for i in range(4) if mask&(1<<i)];k=len(zero)
            if k==0:rk,nk='R4','N4'
            elif k==1:rk,nk='R3','N3'
            elif k==2:
                z0,z1=zero
                suffix='SJA' if z0//2==z1//2 else 'same' if z0%2==z1%2 else 'cross'
                rk,nk='R'+suffix,'N'+suffix
            elif k==3:rk,nk='Rone','N_one'
            else:continue
            acc+=tau**k*s**(4-k)*(s*rebuilt[rk][side]+tau*rebuilt[nk][side])
        output.append(acc)
    ledger=json.loads((V5/'certificate/phase_ledger.json').read_text())
    assert output==[F(ledger['new_revenue'][k]) for k in ('lower','upper')]
    derivative=[rebuilt['N4'][0]+4*rebuilt['R3'][0]-5*r4[1],rebuilt['N4'][1]+4*rebuilt['R3'][1]-5*r4[0]]
    assert derivative[0]>0 and output[0]-r4[1]>F(3,62500)
    upper_old=F(old['preserved_exact_upper'])
    event=json.loads((BASE/'V4_8A_frozen_primal/certificate/first_event_gain.json').read_text())
    splice=json.loads((V5/'certificate/global_duality.json').read_text())
    bb=json.loads((V5/'certificate/bb_global.json').read_text())
    upper=upper_old+F(event['gain_interval'][0])-F(splice['global_gain_lower'])-F(bb['exact_upper_decrease'])
    assert upper==F(ledger['new_exact_upper'])
    gap=[upper-output[1],upper-output[0]]
    old_gap=[upper_old-rebuilt['R4'][1],upper_old-rebuilt['R4'][0]]
    reduction=[old_gap[0]-gap[1],old_gap[1]-gap[0]]
    percent=[100*reduction[0]/old_gap[1],100*reduction[1]/old_gap[0]]
    assert percent==[F(ledger['gap_reduction_percent'][k]) for k in ('lower','upper')]
    # A sharper correlated ratio enclosure, using the exact radical old R4.
    correlated=[100*(1-gap[1]/(upper_old-r4[1])),100*(1-gap[0]/(upper_old-r4[0]))]
    archived_path=BASE/'V4_6_2_upper/certificate/upper_ledger.json'
    archived=json.loads(archived_path.read_text())
    archived_upper=F(archived['final_upper'])
    archived_gap=[archived_upper-r4[1],archived_upper-r4[0]]
    archived_percent=[100*(1-gap[1]/archived_gap[0]),100*(1-gap[0]/archived_gap[1])]
    for key,pair in {'remaining_gap':gap,'old_gap':old_gap,'gap_reduction':reduction,
                     'net_upper_decrease':[upper_old-upper]*2,
                     'primal_gain':[output[0]-rebuilt['R4'][1],output[1]-rebuilt['R4'][0]]}.items():
        assert pair==[F(ledger[key][side]) for side in ('lower','upper')],key
        assert [decimal(pair[0]),decimal(pair[1],True)]==ledger[key]['decimal_enclosure'],key
    guarantee=F(496691,500000)
    assert output[0]/upper>guarantee
    result=dict(status='INDEPENDENT_RATIONAL_FACE_CUBATURE_AND_LEDGER_PASS',
        elapsed_seconds=time.monotonic()-started,resolved_strips=len(ranges),unresolved_strips=len(missing),
        complete_polynomial_cells=cell_count,whole_cell_Bernstein_predicate_checks=predicate_count,
        quadrature='Exact rational Lagrange cubature, degree8 in normalized t and degree2 in normalized rho. Actual N/G/S degree<=6/2; 1D revenue degree<=6.',
        same_moment_enclosures=True,new_revenue=interval_output(output),new_upper=interval_output([upper,upper]),
        remaining_gap=interval_output(gap),old_radical_revenue=interval_output(r4),
        source_percent_V48B=interval_output(percent),correlated_percent_V48B=interval_output(correlated),
        revenue_over_certified_upper_percent=interval_output([100*output[0]/upper,100*output[1]/upper]),
        guaranteed_fraction_of_unrestricted_OPT=str(guarantee),guaranteed_percent='99.3382',
        strict_gain=interval_output([output[0]-r4[1],output[1]-r4[0]]),positive_derivative=interval_output(derivative),
        unresolved_ordered_area=str(area),rounding_allowance=str(error),
        original_archive_baseline='V4.6.1.1 exact radical lower paired with V4.6.2 exact upper; not the older lower in V4.6.2 upper_ledger.',
        original_archive_upper_source=str(archived_path),original_archive_upper=str(archived_upper),
        original_archive_gap=interval_output(archived_gap),percent_reduction_original_archive_pair=interval_output(archived_percent),
        shared_dependencies=['Source menu branch formulas and written proof of Q exchange redundancy and face symmetries.',
        'Inherited exact R4 radical coefficients and source revenue theorem; independent sqrt bracketing is arithmetic only.',
        'Accepted t subdivision reused as proposed partition, all cell order/branch predicates recertified.',
        'Inherited global upper endpoint and accepted upper gains are assembled independently, not reproved by this script.',
        'Uniform B0 perturbation bound uses the written utility integration-by-parts argument.'],
        source_face_sha256=sha256(face_path.read_bytes()).hexdigest())
    (HERE/'independent_face_cubature.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
