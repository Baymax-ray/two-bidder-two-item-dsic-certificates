"""Read-only portable exact lower replay, source identity and strict bracket."""
from pathlib import Path, PureWindowsPath
from hashlib import sha256
from fractions import Fraction as F
import json
import subprocess
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parent

def bound(root,name):
    rel=Path(name);windows=PureWindowsPath(name)
    if not name or windows.drive or windows.root or rel.is_absolute() or '..' in rel.parts:
        raise RuntimeError('Unsafe source path '+name)
    root=root.resolve();result=(root/rel).resolve()
    if result==root or not result.is_relative_to(root):
        raise RuntimeError('Source path escapes root '+name)
    return result

def main():
    records=json.loads((ROOT/'source_bindings.json').read_text(encoding='utf-8'))['files']
    expected=set()
    for row in records:
        rel=row['path']
        if sha256(bound(ROOT,rel).read_bytes()).hexdigest()!=row['sha256']:
            raise RuntimeError('Changed source '+rel)
        expected.add(rel)
    actual={p.relative_to(ROOT).as_posix() for p in (ROOT/'source').rglob('*')
            if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    if actual!=expected:
        raise RuntimeError('Incomplete source inventory')
    print('SOURCE_BINDINGS_PASS',len(records),flush=True)
    names=json.loads((ROOT/'entrypoints.json').read_text(encoding='utf-8'))
    names+=['V4_6_archive_audit/primal/check_primal.py',
            'V4_6_archive_audit/dual/fresh_exact_dual_checks.py',
            'V4_6_archive_audit/dual/fresh_final_residual_checks.py',
            'V4_6_archive_audit/revenue/fresh_exact_gap.py']
    for name in names:
        path=bound(ROOT/'source',name)
        result=subprocess.run([sys.executable,'-B','-X','utf8',str(path)],cwd=path.parent,
                              text=True,encoding='utf-8',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(name+' failed\n'+result.stdout)
        print('PASS',name,flush=True)
    data=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    cert=json.loads((ROOT/'source/V4_6_archive_audit/revenue/fresh_exact_gap.json').read_text(encoding='utf-8'))
    if (data['algebraic_coefficients']!=cert['algebraic_coefficients']
            or data['algebraic_basis']!=['1','sqrt(2)','sqrt(23)']
            or data['joint_rational']!=cert['joint_rational']
            or {row['ratio']:row['coefficient'] for row in data['joint_logs']}!=cert['joint_logs']
            or len(data['joint_logs'])!=len(cert['joint_logs'])):
        raise RuntimeError('Exact revenue expression manifest mismatch')
    lo,hi=map(F,data['revenue_enclosure'])
    fresh_lo,fresh_hi=map(F,cert['revenue_decimal_enclosure'])
    display_lo,display_hi=map(F,data['revenue_decimal_enclosure'])
    if not (lo<=fresh_lo<=fresh_hi<=hi and display_lo<lo<=hi<display_hi
            and F(data['lower_floor'])==display_lo and hi<F(data['upper'])
            and data['upper']==cert['upper']):
        raise RuntimeError('Revenue enclosure manifest mismatch')
    if data['strict_gap']!=cert['strict_certificate']:
        raise RuntimeError('Gap manifest mismatch')
    lower,upper=F(data['lower_floor']),F(data['upper'])
    if not (0<upper-lower<F(1,100) and lower/upper>F(988779,1000000)):
        raise RuntimeError('Claimed bracket/guarantee failed')
    print('JOINT_RESIDUAL_SCREENING_CERTIFICATE_PASS lower_floor='+str(lower)+' upper='+str(upper))
    print('STRICT_GAP_LT_1_100_PASS',F(1,100)-(upper-lower))
    print('REVENUE_GUARANTEE_GT_98_8779_PERCENT_PASS')
    print('UNRESTRICTED_OPTIMUM_REMAINS_OPEN')

if __name__=='__main__':
    main()
