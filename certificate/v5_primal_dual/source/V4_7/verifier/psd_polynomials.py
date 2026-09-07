"""Exact chart polynomials and regional menu margins for PSD discovery/replay."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util,json
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('v462_sparse_algebra',ROOT.parent/'V4_6_2_upper/verifier/sparse_cycle.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
spec=importlib.util.spec_from_file_location('v4611_psd_candidate',ROOT.parent/'V4_6_1_1_lower_bound/verifier/refined_candidate.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)

def correction():
    data=json.loads((p.ARCH/'manifest.json').read_text(encoding='utf-8'))
    anti={}
    for e,co in zip(data['basis_order'],data['theta']):
        e=tuple(e);f=(e[1],e[0],e[3],e[2]);anti=p.add(anti,{e:F(co),f:-F(co)})
    x,y,z,w=[p.var(j) for j in range(4)]
    s=p.mul(x,p.add(p.ONE,p.scale(x,-1)),y,p.add(p.ONE,p.scale(y,-1)),anti)
    return p.der(s,1),p.scale(p.der(s,0),-1)

CORR=correction()
def fields(ownmax,oppmax):
    vs=[p.var(j) for j in range(4)]
    m2=p.mul(vs[ownmax],vs[ownmax]);n2=p.mul(vs[oppmax+2],vs[oppmax+2]);D=p.scale(p.mul(m2,n2),2)
    out=[]
    for j in (0,1):
        first=p.add(p.mul(p.add(p.scale(m2,3),p.scale(p.ONE,-1)),vs[j],n2),p.mul(D,CORR[j]))
        second=p.add(p.mul(p.add(p.scale(n2,3),p.scale(p.ONE,-1)),vs[j+2],m2),p.mul(D,p.swap_bidders(CORR[j])))
        out.append((first,second))
    return out,D

def differences(A,B,W):
    """Each old/new comparison is centered a + epsilon*b; winner chosen exactly."""
    d=tuple(x-y for x,y in zip(A,B));result=[];wins=[]
    for C,sg in ((A,1),(B,-1)):
        fs,D=fields(int(C[1]>C[0]),int(W[1]>W[0]));center=C+W
        CD=p.centered(D,center);local=[]
        for j,(one,two) in enumerate(fs):
            opts=[{},p.centered(one,center),p.centered(two,center)]
            win=max(range(3),key=lambda k:opts[k].get(p.ZERO,F()))
            assert sum(opts[k].get(p.ZERO,F())==opts[win].get(p.ZERO,F()) for k in range(3))==1
            local.append(win)
            for rival in range(3):
                if rival==win:continue
                a=p.add(opts[win],p.scale(opts[rival],-1))
                b=p.scale(CD,sg*d[j]*(int(win==1)-int(rival==1)))
                result.append((a,b))
        wins.append(local)
    return result,wins

def geometric_margins(A,B,W,h,reg):
    out=[]
    for C in (A,B):
        out += [C[j]-h[j] for j in (0,1)]+[1-C[j]-h[j] for j in (0,1)]
        out += [abs(C[0]-C[1])-h[0]-h[1],max(C)-h[C.index(max(C))]-F(43,100)]
    out += [W[j]-h[j+2] for j in (0,1)]+[1-W[j]-h[j+2] for j in (0,1)]
    out += [abs(W[0]-W[1])-h[2]-h[3],max(W)-h[2+W.index(max(W))]-F(43,100)]
    if reg=='Q/Q':
        for C,hh in ((A,h[:2]),(B,h[:2]),(W,h[2:])):
            out += [c.A-C[j]-hh[j] for j in (0,1)]+[c.b-sum(C)-sum(hh)]
    else:
        # Convex base subregions: sum>b and both coordinates>c, OR a fixed
        # coordinate>T. Choose whichever sufficient description has margin.
        for C,hh in ((A,h[:2]),(B,h[:2]),(W,h[2:])):
            out.append(max(min(sum(C)-sum(hh)-c.b,min(C[j]-hh[j]-c.c for j in (0,1))),max(C[j]-hh[j]-c.T for j in (0,1))))
    return out

def empty_menu_margins(A,B,W,h,reg):
    lo=tuple(W[j]-h[j+2] for j in (0,1));hi=tuple(W[j]+h[j+2] for j in (0,1));prices=None
    if reg=='Q/Q':
        tl,th=max(lo),max(hi)
        if th<=c.d:
            assert F(1417,1000)**2>2
            prices=(c.A,c.A,F(861,1000)) # sqrt(2)<1.417 gives B0>.861
        elif tl>=c.d:
            kl,kh=c.inverse(tl),c.inverse(th)
            K=lambda k:F(5,6)+F(3,4)*k*k
            safe=min(c.A,K(kh)-kh);scarce=c.A
            prices=(scarce,safe,K(kl)) if W[0]>W[1] else (safe,scarce,K(kl))
        else:return [-F(1)]*6
    else:
        H=max(F(),lo[0]-c.a,lo[1]-c.a,sum(lo)-c.b)
        prices=(H+min(c.a,c.s-hi[1]),H+min(c.a,c.s-hi[0]),H+c.b)
    out=[]
    for C in (A,B):
        upper=tuple(C[j]+h[j] for j in (0,1))
        out += [prices[j]-upper[j] for j in (0,1)]+[prices[2]-sum(upper)]
    return out

def high_item_menu_margins(A,B,W,h,reg):
    """Base opponent first coordinate high, second low: prices (w1,d,w1+c)."""
    assert reg=='base/base'
    lo=tuple(W[j]-h[j+2] for j in (0,1));hi=tuple(W[j]+h[j+2] for j in (0,1))
    out=[lo[0]-c.T,c.c-hi[1],c.d-c.c]
    for C in (A,B):
        # Strict high single beats empty and bundle; safe single negative.
        out += [C[0]-h[0]-hi[0],c.c-C[1]-h[1],c.d-C[1]-h[1],C[0]-h[0]-c.T]
    return out

def exact_winner_margins(diffs,h,eps):
    return [p.bound(p.add(a,p.scale(b,t)),h)[0] for a,b in diffs for t in (F(),eps)]
