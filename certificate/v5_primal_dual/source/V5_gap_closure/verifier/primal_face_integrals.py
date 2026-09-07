"""Exact polynomial integration of source faces for global reserve rebasing.

Only one-dimensional parameter intervals around algebraic branch crossings
are enclosed. Resolved two-dimensional opponent regions integrate exactly.
"""
from fractions import Fraction as F
from pathlib import Path
from math import comb
from hashlib import sha256
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
A=F(2,3);d=F(1,2);c=F(157,500);q=d-c;u=F(3421,10000);sig=F(4,5)
a=A+q*q/2;b=a+c;s=a+d;T=1-F(2,3)*c;U=F(5,3)-2*c;H=1-q;jump=sig*(u-c);J=u+q
bh=F(861928812542301,10**15);round_error=F(1,10**12)
assert (4-3*bh)**2>2 and (4-3*(bh+F(1,10**15)))**2<2

def P(v):return {(0,0):F(v)} if v else {}
tt={(1,0):F(1)};rr={(0,1):F(1)}
def add(*pp):
    out={}
    for p in pp:
        for k,v in p.items():out[k]=out.get(k,F())+v
    return {k:v for k,v in out.items() if v}
def sc(p,v):return {k:x*v for k,x in p.items() if x*v}
def mul(p,z):
    out={}
    for (i,j),v in p.items():
      for (k,l),w in z.items():out[i+k,j+l]=out.get((i+k,j+l),F())+v*w
    return {k:v for k,v in out.items() if v}
def pw(p,n):
    out=P(1)
    for _ in range(n):out=mul(out,p)
    return out
def val(p,t,r=F()):return sum((v*t**i*r**j for (i,j),v in p.items()),F())
def choose(ps,t,r,which=max):return which(ps,key=lambda p:val(p,t,r))
def sub(p,z):return add(p,sc(z,-1))
def integral(p,lo,hi):
    assert all(j==0 for i,j in p)
    return sum((v*(hi**(i+1)-lo**(i+1))/(i+1) for (i,j),v in p.items()),F())
def vertical(p,L,R):
    out={}
    for (i,j),v in p.items():out=add(out,mul({(i,0):v/F(j+1)},sub(pw(R,j+1),pw(L,j+1))))
    return out
def bound(p,lo,hi):
    mid=(lo+hi)/2;half=(hi-lo)/2;co={}
    for (i,j),v in p.items():
        assert j==0
        for n in range(i+1):co[n]=co.get(n,F())+v*comb(i,n)*mid**(i-n)
    rad=sum((abs(v)*half**n for n,v in co.items() if n),F());return co.get(0,F())-rad,co.get(0,F())+rad
def K(k):return add(P(F(5,6)),sc(pw(k,2),F(3,4)))
def kinv(t):
    if t<=d+jump:return P(c)
    if t<J:return sc(sub(tt,P(q+sig*u)),1/(1-sig))
    return sub(tt,P(q))
def delta():return sc(mul(sub(P(T),tt),sub(P(U),tt)),F(9,16))

def moment(PP,BB,CC):
    one=P(1);k=sub(CC,BB);ell=sub(CC,PP);discount=sub(add(PP,BB),CC)
    scarce=mul(sub(one,PP),ell);safe=mul(sub(one,BB),k)
    bundle=sub(mul(sub(one,k),sub(one,ell)),sc(pw(discount,2),F(1,2)))
    rev=add(mul(PP,scarce),mul(BB,safe),mul(CC,bundle))
    number=add(P(2),sc(CC,-2),pw(CC,2),mul(add(PP,BB),sub(one,CC)))
    return rev,number

def menu(t,r):
    z=add(tt,rr);g=sc(sub(P(u),rr),sig) if c<r<u else P(0)
    extraN=P(0);extraR=P(0)
    if t<=A and t+r<=b:
        if t<=d:
            PP=BB=P(A);CC=choose([P(bh),z],t,r);name='Qfree'
        else:
            k=kinv(t);CC=choose([K(k),z],t,r);PP=P(A);BB=choose([P(A),sub(CC,k)],t,r,min);name='Qcon'
    elif A<t<T and r<c:
        de=delta();alpha=sub(sc(tt,3),P(2));PP=tt;BB=add(P(d),de);CC=add(tt,P(c),de)
        extraN=sc(mul(alpha,de),F(1,4));extraR=sc(mul(pw(alpha,2),de),F(1,8));name='E'
    else:
        hh=choose([P(0),sub(tt,P(a)),sub(z,P(b))],t,r)
        PP=add(hh,choose([P(a),sub(P(s),rr)],t,r,min))
        BB=add(hh,choose([P(a),sub(P(s),tt)],t,r,min),g)
        CC=add(hh,P(b),g);name='base'
    PP=choose([PP,P(1)],t,r,min);BB=choose([BB,P(1)],t,r,min)
    pp,bb,cc=val(PP,t,r),val(BB,t,r),val(CC,t,r)
    assert 0<=pp<=1 and 0<=bb<=1 and max(pp,bb)<=cc<=pp+bb
    rev,num=moment(PP,BB,CC)
    G=add(mul(PP,sub(P(1),PP)),mul(BB,sub(P(1),BB)))
    S=sub(P(2),add(PP,BB))
    return add(num,extraN),G,S,add(rev,extraR),BB,name

def cuts(t):
    out=[P(0),tt,P(c),P(u),P(d),P(H),sub(P(b),tt),sub(P(1+c),tt)]
    if t<=A:
        if t<=d:out.append(sub(P(bh),tt))
        else:
            k=kinv(t);out +=[sub(K(k),tt),sub(add(P(A),k),tt)]
    unique={tuple(sorted(p.items())):p for p in out}
    return sorted(unique.values(),key=lambda p:val(p,t))

def two_dimensional():
    nodes=sorted({F(),d,d+jump,J,A,a,T,H,F(1)})
    stack=list(zip(nodes[:-1],nodes[1:]));acc=[F(),F(),F()];lost=F();resolved=[];uncertain=[]
    while stack:
        lo,hi=stack.pop();mid=(lo+hi)/2;cs=cuts(mid)
        good=all(bound(sub(y,x),lo,hi)[0]>=0 for x,y in zip(cs[:-1],cs[1:]))
        if not good:
            if hi-lo>F(1,2**25):stack +=[(lo,mid),(mid,hi)];continue
            area=(hi*hi-lo*lo)/2;lost+=area;uncertain.append([str(lo),str(hi)]);continue
        row=[F(),F(),F()];pieces=0
        for L,R in zip(cs[:-1],cs[1:]):
            rm=(val(L,mid)+val(R,mid))/2
            if not 0<rm<mid:continue
            nn,gg,ss,rev,bb,name=menu(mid,rm);area=integral(sub(R,L),lo,hi)
            assert area>=0
            for j,pol in enumerate((nn,gg,ss)):
                value=integral(vertical(pol,L,R),lo,hi)
                assert 0<=value<=(F(2),F(1,2),F(2))[j]*area
                row[j]+=value
            pieces+=1
        acc=[x+y for x,y in zip(acc,row)];resolved.append([str(lo),str(hi),pieces])
    assert lost<F(1,100000)
    return acc,lost,resolved,uncertain

def one_dimensional():
    nodes=[F(),d,d+jump,J,A,T,F(1)];Rfull=Nfull=Rcross=Ncross=F()
    for lo,hi in zip(nodes[:-1],nodes[1:]):
        mid=(lo+hi)/2;num,gg,ss,rev,bb,name=menu(mid,F())
        assert all(j==0 for p in (num,rev,bb) for i,j in p)
        Rfull+=integral(rev,lo,hi);Nfull+=integral(num,lo,hi)
        Rcross+=2*integral(mul(bb,sub(P(1),bb)),lo,hi)
        Ncross+=2*integral(sub(P(1),bb),lo,hi)
    RS,NS=moment(P(A),P(A),P(bh))
    return dict(Rfull=Rfull,Nfull=Nfull,Rcross=Rcross,Ncross=Ncross,RSJA=val(RS,0),NSJA=val(NS,0))

def calculate():
    mom,lost,resolved,uncertain=two_dimensional();one=one_dimensional()
    # Uniform utility perturbation from rationalizing B0 bounds every total
    # source-face revenue by10*(B0-bh), allocation by8*(B0-bh).
    e=round_error
    en=dict(N4=[4*mom[0]-e,4*(mom[0]+2*lost)+e],
        R3=[one['Rfull']+mom[1]-e,one['Rfull']+mom[1]+lost/2+e],
        N3=[one['Nfull']+mom[2]-e,one['Nfull']+mom[2]+2*lost+e])
    for name in ('Rcross','Ncross','RSJA','NSJA'):en[name]=[one[name]-e,one[name]+e]
    en.update(Rsame=[F(31,81)]*2,Nsame=[F(5,9)]*2,Rone=[F(2,9)]*2,N_one=[F(1,3)]*2)
    old=ROOT.parent/'V4_6_1_1_lower_bound/certificate/refined_revenue.json';data=json.loads(old.read_text())
    en['R4']=list(map(F,data['revenue_interval']))
    return dict(status='EXACT_SOURCE_FACE_MOMENTS_PASS',moment_enclosures={k:list(map(str,v)) for k,v in en.items()},
        display_enclosures={k:list(map(float,v)) for k,v in en.items()},rational_B0=str(bh),uniform_face_rounding_error=str(e),
        unresolved_ordered_opponent_area=str(lost),resolved_t_intervals=resolved,unresolved_t_intervals=uncertain,
        polynomial_regions='Source menu branches; exact vertical polynomial integration with certified cut ordering. Only algebraic crossing strips use range bounds.',
        source_revenue_certificate_sha256=sha256(old.read_bytes()).hexdigest(),
        source_primal_sha256=sha256((ROOT.parent/'V4_6_1_1_lower_bound/verifier/refined_candidate.py').read_bytes()).hexdigest())

if __name__=='__main__':
    out=calculate();path=ROOT/'certificate/primal_face_integrals.json'
    if '--write' in sys.argv:path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text())==out
    print(out['status']);print(json.dumps(out['display_enclosures'],indent=2));print('resolved',len(out['resolved_t_intervals']),'uncertain',len(out['unresolved_t_intervals']))
