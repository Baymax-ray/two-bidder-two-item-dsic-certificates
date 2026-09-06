"""Exact polynomial checks for the lottery-support redistribution."""
from fractions import Fraction as Q
from pathlib import Path
import json,sys
if not __debug__:raise RuntimeError('Run without -O')
def add(a,b):
 c=[Q(0)]*max(len(a),len(b))
 for i,v in enumerate(a):c[i]+=v
 for i,v in enumerate(b):c[i]+=v
 return c
def scale(a,b):return [v*b for v in a]
def mul(a,b):
 c=[Q(0)]*(len(a)+len(b)-1)
 for i,v in enumerate(a):
  for j,w in enumerate(b):c[i+j]+=v*w
 return c
def integral(p,a,b):return sum(c*(b**(i+1)-a**(i+1))/(i+1) for i,c in enumerate(p))
def replay():
 q=Q(113,500);c=Q(137,500);A=Q(2,3);T=Q(613,750)
 alpha=[Q(-2),Q(3)]
 delta=add([q+3*q*q/4,-3*q/2],scale(mul(alpha,alpha),Q(1,16)))
 L=add(delta,scale(alpha,Q(1,2)))
 m=scale(mul(alpha,L),Q(1,4));lam=add(scale(alpha,c),m)
 assert lam==mul(alpha,add([c],scale(L,Q(1,4))))
 assert add(scale([-q,Q(1)],3),scale(alpha,-1))==[2-3*q,Q(0)]
 sink_bound=q*(2-Q(7,2)*q)
 assert sink_bound>0 and 2-3*q>0
 J=(Q(3,4),Q(4,5))
 old_mass=2*c*integral(mul(lam,[Q(0),Q(1)]),*J)
 new_mass=2*c*integral(mul(m,[Q(0),Q(1)]),*J)
 assert old_mass>new_mass>0
 assert old_mass-new_mass==2*c*c*integral(mul(alpha,[Q(0),Q(1)]),*J)
 return {'status':'EXACT_LOTTERY_SUPPORT_REDISTRIBUTION_IDENTITIES_PASS','parameters':{'q':str(q),'c':str(c),'A':str(A),'T':str(T)},'corner_multiplier_polynomial':[str(x) for x in m],'bulk_sink_coefficient':str(2-3*q),'corner_sink_margin_lower':str(sink_bound),'stable_t_interval':[str(x) for x in J],'original_null_consumed_mass':str(old_mass),'remaining_null_consumed_mass':str(new_mass),'remaining_mass_decimal_diagnostic':float(new_mass),'scope':'Universal support and gap proved in written continuum derivation. Exact replay verifies polynomial identities and positive bounds, not all-real convexity by enumeration. No new numerical upper subtraction uses this lottery support.'}
if __name__=='__main__':
 r=replay();p=Path(__file__).resolve().parents[1]/'certificate/conditional_lottery_redistribution.json'
 if '--write' in sys.argv:p.write_text(json.dumps(r,indent=2)+'\n',encoding='utf8')
 else:assert r==json.loads(p.read_text(encoding='utf8'))
 print(json.dumps(r,indent=2))
