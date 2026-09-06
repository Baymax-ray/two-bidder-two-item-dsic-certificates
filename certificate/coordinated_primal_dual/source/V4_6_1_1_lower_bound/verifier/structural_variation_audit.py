"""Exact finite route comparisons; not derivative or global optimality tests."""
from fractions import Fraction as F
from pathlib import Path
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O')
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verifier'))
import structural_reserve as reserve
import structural_split as split
import structural_lower_split as lower

def verify():
    A,c=F(2,3),F(47,150);clean=reserve.revenue(A,c);p=reserve.p
    above=[]
    for eps in (F(1,10000),F(1,1000),F(1,100),F(98,5625)):
        r=reserve.revenue(A+eps,c);diff=r-clean;assert diff.lo>0
        above.append(dict(a=str(A+eps),revenue_interval=p.tools.rounded_interval(r,30),gain_over_clean_interval=p.tools.rounded_interval(diff,30)))
    old=split.outer_base(A,c,F(1,2));up=[]
    for d in (F(5001,10000),F(501,1000),F(51,100)):
        diff=split.outer_base(A,c,d)-old;assert diff<0
        up.append(dict(base_d=str(d),exact_gain=str(diff)))
    down=[]
    assert max(lower.revenue(A,c,F(1,2)).lo,clean.lo)<min(lower.revenue(A,c,F(1,2)).hi,clean.hi)
    for d in (F(4999,10000),F(499,1000),F(49,100)):
        r=lower.revenue(A,c,d);diff=r-clean;assert diff.hi<0
        down.append(dict(coordinated_d=str(d),revenue_interval=p.tools.rounded_interval(r,30),gain_over_clean_interval=p.tools.rounded_interval(diff,30)))
    data=dict(status='STRUCTURAL_VARIATION_EXACT_ROUTE_AUDIT_PASS',
      reserve_above_A=above,base_only_split_increase=up,coordinated_split_decrease=down,
      scope='Exact continuous revenue comparisons for specified complete paths; no universal sign, stationarity, or unrestricted optimizer claim',
      proof='research_log/structural_compatibility.md',
      warning='Alternative paths are not additive; the accepted capped reserve mechanism is separately specified and verified')
    target=ROOT/'certificate/structural_variation_audit.json'
    if '--write' in sys.argv:target.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(target.read_text(encoding='utf-8'))==data
    print(data['status']);return data
if __name__=='__main__':verify()
