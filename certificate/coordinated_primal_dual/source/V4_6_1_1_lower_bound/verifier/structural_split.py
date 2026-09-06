"""Exact outer-base split variation, retaining complete Q/E screening menus."""
from fractions import Fraction as F
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'V4_6_1_lower_bound/verifier'))
import parameter_revenue as p
A=F(2,3)

def outer_base(a,c,d,T_override=None):
    b,s,T=a+c,a+d,(1-2*c/3 if T_override is None else T_override);P,X,Y=p.BP,p.TT,p.RR
    total=area=F()
    outer=((A-X,X+Y-b),(X-A,T-X,Y-c),(X-T,))
    for H,cond in ((P(0),(a-X,b-X-Y)),(X-a,(X-a,c-Y)),(X+Y-b,(X+Y-b,Y-c))):
      for tx in (True,False):
       for ry in (True,False):
        pa=H+(a if ry else s-Y);pb=H+(a if tx else s-X);pc=H+b
        for case in range(3):
          fs=list(cond)+[d-X if tx else X-d,d-Y if ry else Y-d]
          if case==0:fs += [1-pa,1-pb];rev=p.G(pa,pb,pc)
          elif case==1:
            fs += [pa-1,1-pb];k=pc-pb
            rev=pb*k*(1-pb)+pc*((1-k)*(1-pb)+(1-k)**2/2)
          else:fs += [pb-1,pa-1];rev=pc*(2-pc)**2/2
          for region in outer:
            poly=[(F(),F()),(F(1),F()),(F(1),F(1))]
            for plane in fs+list(region):
              if poly:poly=p.clip(poly,plane)
            ar=p.pintegral(1,poly)
            if ar:area+=ar;total+=p.pintegral(rev,poly)
    expected=F(1,2)-(A*A-(2*A-b)**2/2)/2-c*(T-A)
    assert area==expected
    return 4*total

if __name__=='__main__':
    a,c=A,F(47,150);old=outer_base(a,c,F(1,2))
    for dd in (F(1,2),F(5001,10000),F(501,1000),F(51,100),F(11,20)):
      diff=outer_base(a,c,dd)-old
      print('d',dd,'delta',diff,'float',float(diff))
