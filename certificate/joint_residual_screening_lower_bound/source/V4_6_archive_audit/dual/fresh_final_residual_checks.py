"""Fresh exact checks of final V4.6 conditional coverage, without source writes.

Finite regressions supplement the all-real audit; they are not its proof.
Default execution compares stored JSON without writing; --write regenerates
only this audit folder's JSON result.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError("Assertions must be enabled")
sys.dont_write_bytecode = True
SOURCE = Path(__file__).resolve().parents[2]/"V4_6"
sys.path.insert(0,str(SOURCE/"verifier"))
import price_joint_reallocation as final

A,q,c = F(2,3),F(113,500),F(137,500)
eps = F(9,10000)
left,right = F(7,10)-4*eps,F(71,100)+eps
counts = {"retained_Eplus_fibers":0,"Eplus_occupied_traces":0,
          "Eplus_candidate_report_choices":0,"Q_occupied_traces":0}


def orient(own,rotated):
    return tuple(reversed(own)) if rotated else tuple(own)


def call(bidder,opponent,own):
    profile = own+opponent if bidder == 0 else opponent+own
    return final.mechanism(profile)


for t in (F(667,1000),left-F(1,10**6),left,F(7,10),F(71,100),
          right,right+F(1,10**6),F(3,4),F(816,1000)):
    alpha = 3*t-2
    delta = q+3*q*q/4-3*q*t/2+alpha*alpha/16
    beta = alpha/(alpha+2*delta)
    b,cc,yy = F(1,2)+delta,t+c+delta,c+delta+alpha/2
    menu = [((F(),F()),F()),((F(),F(1)),b),((F(1),F()),t),
            ((F(1),F(1)),cc),((F(1),beta),t+beta*c)]
    for rho in (F(),F(1,5),F(1,4),c-F(1,10**6)):
        for rotated in (False,True):
            opponent = orient((t,rho),rotated)
            for bidder in (0,1):
                if bidder == 0 and final.bidder_one_fee(opponent):
                    continue
                if bidder == 1 and left <= t <= right:
                    continue
                counts["retained_Eplus_fibers"] += 1
                high = 1 if rotated else 0
                for own in ((F(),F(1)),(c,F(1)),(t-q-F(1,10**6),F(1)),
                            ((2*A+t)/3,c),((A+2*t)/3,c)):
                    row = call(bidder,opponent,orient(own,rotated))
                    assert row["allocations"][1-bidder][high] == 1
                    counts["Eplus_occupied_traces"] += 1
                for own in ((A,F(1)),(t,c),(F(1,2),F(9,10)),(F(1),(c+yy)/2)):
                    values = [sum((x*a for x,a in zip(own,allocation)),F())-p
                              for allocation,p in menu]
                    selected = values.index(max(values))
                    row = call(bidder,opponent,orient(own,rotated))
                    assert row["allocations"][bidder] == orient(menu[selected][0],rotated)
                    assert row["payments"][bidder] == menu[selected][1]
                    counts["Eplus_candidate_report_choices"] += 1

for t,z in ((F(1,2),F(87,100)),(F(1,2),F(91,100)),
            (F(51,100),F(9,10)),(F(54,100),F(91,100))):
    for rotated in (False,True):
        opponent = orient((t,z-t),rotated)
        high,low = (1,0) if rotated else (0,1)
        for own,priced in (((F(1,4),F()),high),((F(1,2),F()),high),
                           ((F(1,2),(z-F(1,2))/2),low),
                           ((F(1,2),z-F(1,2)-F(1,10**6)),low)):
            row = call(1,opponent,orient(own,rotated))
            assert row["allocations"][0][priced] == 1
            counts["Q_occupied_traces"] += 1
        if t > F(1,2):
            for own in ((F(),F(1)),((t-q)/2,F(1)),(t-q-F(1,10**6),F(1))):
                row = call(1,opponent,orient(own,rotated))
                assert row["allocations"][0][high] == 1
                counts["Q_occupied_traces"] += 1

data = dict(status="FRESH_FINAL_RESIDUAL_COVERAGE_REGRESSIONS_PASS",counts=counts,
            scope="Exact boundary regressions against final source mechanism; not exhaustive continuum proof")
destination = Path(__file__).with_suffix(".json")
if '--write' in sys.argv:
    destination.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
else:
    assert json.loads(destination.read_text(encoding="utf-8")) == data
print(data["status"])
print(json.dumps(counts))
