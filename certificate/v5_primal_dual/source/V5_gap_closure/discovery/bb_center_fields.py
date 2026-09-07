from pathlib import Path
from fractions import Fraction as F
import json,sys,importlib.util,time
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('field',ROOT.parent/'V4_7/verifier/psd_polynomials.py')
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
spec=importlib.util.spec_from_file_location('master',ROOT.parent/'V4_8A_frozen_primal/verifier/master_algebra.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
centers=[tuple(map(F,['23/40','3/5','91/100','13/40'])),tuple(map(F,['29/40','23/40','91/100','13/40']))]
halfs=list(map(F,['3/40','3/20','9/100','13/40']))
out=[]
for ci,C in enumerate(centers):
    row=[]
    for p in [f.CORR[0],f.CORR[1],f.p.swap_bidders(f.CORR[0]),f.p.swap_bidders(f.CORR[1])]:
        co=m.fast_center(p,C)
        co={e:c*__import__('math').prod(h**n for h,n in zip(halfs,e)) for e,c in co.items()}
        row.append([[list(e),str(c)] for e,c in sorted(co.items())])
    out.append(row)
(ROOT/'discovery/bb_centered_fields.json').write_text(json.dumps(dict(centers=[[str(v) for v in c] for c in centers],halfwidths=list(map(str,halfs)),corrections=out),indent=2)+'\n')
print('8 normalized exact correction polynomials saved',sum(len(p) for row in out for p in row))
