"""Exact independent constants and identities for Q-Q/Q-base compatibility."""
from fractions import Fraction as F
from pathlib import Path
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O')
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verifier'))
import parameter_candidate as m

def verify():
    A,c,d,q,b,s=m.A,m.c,m.d,m.q,m.b,m.s;k=A-q
    C0=lambda z:F(5,6)+F(3,4)*z*z
    assert A==m.a and d==s-A==F(1,2) and b==A+c and q==s-b
    assert 0<q<c<k<A and b<1 and b<s and C0(k)<s
    assert C0(k)-k>d and C0(c)>m.B0 and k<F(2,3)
    # The two decisive strict-comparison price gaps reduce identically.
    for t in (d+F(1,1000),F(3,5),A):
        for rho in (F(),(b-t)/2,b-t):
            kt=t-q;C=max(C0(kt),t+rho)
            assert C-A<d and C-kt>d and C>=t+rho
            for x in (kt,kt+F(1,10000),A):
                assert (x+q-t)==(x-kt)
            for z in (F(),kt/2,kt-F(1,10000)):
                row=m.mechanism((t,rho,z,F(1)))
                assert row['allocations'][0][0]==1
    data=dict(status='SYM_PARAMETER_Q_INDEPENDENT_AUDIT_PASS',
      proof='research_log/sym_parameter_q_audit.md',
      audited_scope='all-real Q-Q and Q-base compatibility; conditional support anchors; E interactions separate',
      exact_constants={key:str(value) for key,value in dict(kmax=k,C0max=C0(k),safe_min=C0(k)-k,s=s,b=b).items()})
    p=ROOT/'certificate/sym_parameter_q_audit.json'
    if '--write' in sys.argv:p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(p.read_text(encoding='utf-8'))==data
    print(data['status']);return data
if __name__=='__main__':verify()
