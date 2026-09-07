"""Read-only portable replay of the active lower and unrestricted upper.

Frozen sources are materialized in an isolated original-layout temporary tree.
No original workspace or search/discovery script is used. All script outputs
are compared to frozen certificates by their own entrypoints, then source
identities and independent endpoint reconciliation are checked again.
"""
from pathlib import Path, PureWindowsPath
from fractions import Fraction as F
from hashlib import sha256
import json,subprocess,sys,tempfile,shutil
PKG=Path(__file__).resolve().parent
ARCH=PKG.parents[1]
AUDIT='V4_6_1_1_V4_6_2_archive_audit'
def require(c,m):
    if not c:raise RuntimeError(m)
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def bound(root,name):
    rel=Path(name);windows=PureWindowsPath(name)
    require(name and not windows.drive and not windows.root
            and not rel.is_absolute() and '..' not in rel.parts,'unsafe path '+name)
    root=root.resolve();result=(root/rel).resolve()
    require(result!=root and result.is_relative_to(root),'path escapes root '+name)
    return result
def inputs():
    own=read(PKG/'source_bindings.json')['files'];deps=read(PKG/'dependencies.json')
    require({e['path'] for e in own}=={p.relative_to(PKG).as_posix() for p in (PKG/'source').rglob('*') if p.is_file() and '__pycache__' not in p.parts},'source inventory differs')
    for e in own:require(sha256(bound(PKG,e['path']).read_bytes()).hexdigest()==e['sha256'],'source identity '+e['path'])
    for e in deps:require(sha256(bound(ARCH,e['path']).read_bytes()).hexdigest()==e['sha256'],'dependency identity '+e['path'])
    return own,deps
def endpoint():
    m=read(PKG/'manifest.json');lo=read(PKG/'source/V4_6_1_1_lower_bound/certificate/branch_summary.json');up=read(PKG/'source/V4_6_2_upper/certificate/upper_ledger.json')
    third=read(PKG/'source'/AUDIT/'lower_revenue/third_revenue_and_pairing.json')
    require(m['revenue_coefficients']==lo['exact_revenue_coefficients']==third['coefficients'],'coefficient disagreement')
    require(m['revenue_basis']==lo['field_basis']==third['basis'],'basis disagreement')
    require(m['upper']==up['final_upper'],'upper disagreement')
    U=F(m['upper']);require(U==F(m['upper_anchor'])-F(m['conditional_subtraction'])-F(m['cycle_subtraction']),'upper formula')
    require(m['lower_enclosure']==third['revenue'] and m['gap_enclosure']==third['gap'] and m['ratio_enclosure']==third['ratio_lower_over_upper'] and m['upper_enclosure']==third['new_upper'],'independent enclosure mismatch')
    L=F(m['lower_enclosure'][0]);require(U-L<F(1,100),'gap threshold');require(L/U>F(m['guarantee']),'ratio threshold')
    print('EXACT_LOWER_COEFFICIENTS',*m['revenue_coefficients'])
    print('LOWER_ENCLOSURE',*m['lower_enclosure']);print('UPPER_EXACT',m['upper']);print('GAP_ENCLOSURE',*m['gap_enclosure'])
    print('STRICT_GAP_LT_1_100_PASS GUARANTEE_GT_99_2684_PERCENT_PASS')
def main():
    require(sys.version_info>=(3,10) and sys.flags.optimize==0,'Python >=3.10 without optimization required')
    own,deps=inputs();commands=read(PKG/'entrypoints.json')
    with tempfile.TemporaryDirectory(prefix='dsic-pair-') as tmp:
        stage=Path(tmp);auction=stage/'output/output/two_bidder_two_item_full_dsic_exact_auction'
        for e in deps:
            dst=bound(stage,e['stage']);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(bound(ARCH,e['path']),dst)
        for e in own:
            dst=bound(auction,e['origin']);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(bound(PKG,e['path']),dst)
        for c in commands:
            script=bound(auction,c[0]);result=subprocess.run([sys.executable,'-B','-X','utf8',str(script),*c[1:]],cwd=script.parent,text=True,encoding='utf-8',errors='replace',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            require(result.returncode==0,'FAILED '+str(c)+'\n'+result.stdout)
            print('PASS',' '.join(c),flush=True)
        for e in own:require(sha256(bound(auction,e['origin']).read_bytes()).hexdigest()==e['sha256'],'replay changed staged source '+e['origin'])
    inputs();endpoint();print('COORDINATED_PRIMAL_DUAL_CERTIFICATE_PASS',len(commands),'entrypoints')
if __name__=='__main__':main()
