"""Bounded implementation checks, distinct from the all-real DSIC proof."""
import sys
if sys.flags.optimize:raise RuntimeError('Run without optimized Python mode')
from fractions import Fraction as F
from itertools import product
import mechanism as m

nodes=(F(),m.TAU/2,m.TAU,F(1))
profiles=list(product(nodes,repeat=4))
knots=(m.seed.c,m.seed.u,m.seed.d,m.seed.d+m.seed.jump,m.seed.A,m.seed.T)
for x in knots:
    for shift in (-F(1,1000000),F(),F(1,1000000)):
        t=m.TAU+(1-m.TAU)*(x+shift)
        for i in range(4):
            v=[F(3,4),F(1,3),F(4,5),F(1,10)];v[i]=t;profiles.append(tuple(v))
for v in profiles:
    truth=m.mechanism(v)
    for i in (0,1):
        for report in ((F(),F()),(m.TAU,m.TAU),(F(1),F(1))):
            alt=list(v);alt[2*i:2*i+2]=report
            got=m.mechanism(alt)
            utility=sum((v[2*i+j]*got['allocations'][i][j] for j in (0,1)),F())-got['payments'][i]
            assert truth['utilities'][i]>=utility
center=tuple(map(F,['1577/2000','123/200','3/5','4/5']))
for signs in product((-1,1),repeat=4):
    v=tuple(x+F(sign,10000) for x,sign in zip(center,signs))
    assert m.mechanism(v)['allocations']==((F(1),F()),(F(),F(1)))
print('RESERVE_IMPLEMENTATION_CHECK_PASS',len(profiles),'profiles',6*len(profiles),'deviations',16,'witness vertices')
