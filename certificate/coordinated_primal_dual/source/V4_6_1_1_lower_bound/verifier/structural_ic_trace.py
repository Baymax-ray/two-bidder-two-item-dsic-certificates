"""Exact actual-capacity witnesses for the incentive-derived E junction."""
from fractions import Fraction as F
from pathlib import Path
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O')
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verifier'))
import structural_reserve_candidate as m

def verify():
    counts={'rectangle':0,'top':0};vacant=[]
    for t in ((m.A+m.a)/2,m.a,(m.a+m.T)/2):
      for rho in (F(),m.c/2,m.c-F(1,10000)):
        w=(t,rho)
        for x in ((2*m.A+t)/3,(m.A+2*t)/3):
          for y in (m.c/3,2*m.c/3,m.c-F(1,10000)):
            row=m.capped_mechanism((x,y)+w)
            assert row['allocations'][1][0]==1;counts['rectangle']+=1
        for x in (m.c/2,(t-m.q)/2,t-m.q-F(1,10000)):
          row=m.capped_mechanism((x,F(1))+w)
          assert row['allocations'][1][0]==1;counts['top']+=1
    t=(m.A+m.a)/2;x=(m.A+t)/2;w=(t,F(1,10))
    row=m.capped_mechanism((x,m.c)+w)
    assert row['allocations'][1][0]==0
    data=dict(status='STRUCTURAL_IC_DERIVED_E_TRACE_PASS',
       scope='Full E inner certificate repaired through DSIC-derived horizontal trace; not a global capacity supergradient',
       actual_capacity_examples=counts,
       vacant_literal_junction=dict(profile=list(map(str,(x,m.c)+w)),opponent_allocation=list(map(str,row['allocations'][1]))),
       all_real_proof='research_log/structural_compatibility.md Section 10',
       conclusion='Capped identity-h reserve candidate has full randomized conditional certificates on Q and E for both bidders')
    target=ROOT/'certificate/structural_ic_trace.json'
    if '--write' in sys.argv:target.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(target.read_text(encoding='utf-8'))==data
    print(data['status']);return data
if __name__=='__main__':verify()
