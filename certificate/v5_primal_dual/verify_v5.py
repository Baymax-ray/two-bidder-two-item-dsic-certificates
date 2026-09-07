"""Read-only archive replay of the selected V5 mathematical dependency closure.

Package and archive files remain byte-identical. Original source functions run
in a disposable original-layout tree; two audit outputs are temporarily
regenerated there only to normalize their absolute provenance comparisons.
"""
from pathlib import Path, PureWindowsPath
from hashlib import sha256
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

PKG=Path(__file__).resolve().parent
PREFIX='output/output/two_bidder_two_item_full_dsic_exact_auction'

def require(condition,message):
    if not condition:
        raise RuntimeError(message)

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def safe(root,name):
    path=Path(name)
    windows=PureWindowsPath(name)
    require(name and not windows.drive and not windows.root
            and not path.is_absolute() and '..' not in path.parts,
            'unsafe relative path '+name)
    root=root.resolve()
    candidate=(root/path).resolve()
    require(candidate!=root and candidate.is_relative_to(root),
            'path escapes root '+name)
    return candidate


def child_environment():
    environment={key:value for key,value in os.environ.items()
                 if not key.upper().startswith('PYTHON')}
    # Legacy grandchildren also omit user-site imports.
    environment['PYTHONNOUSERSITE']='1'
    return environment


def runtime_identity():
    code='''import sys,json,numpy,fractions,hashlib,decimal
modules={name:getattr(module, '__file__', None)
         for name,module in [('numpy',numpy),('fractions',fractions),
                             ('json',json),('hashlib',hashlib),('decimal',decimal)]}
modules.update({name:module.__file__ for name,module in sys.modules.items()
                if name.endswith('_multiarray_umath') and hasattr(module,'__file__')})
print(json.dumps(dict(python=sys.version,executable=sys.executable,
 prefix=sys.prefix,numpy=numpy.__version__,modules=modules,
 ignore_environment=sys.flags.ignore_environment,
 no_user_site=sys.flags.no_user_site,optimize=sys.flags.optimize)))'''
    process=subprocess.run([sys.executable,'-E','-s','-B','-X','utf8','-c',code],
                           cwd=PKG,env=child_environment(),stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,text=True,encoding='utf-8')
    require(process.returncode==0,'runtime probe failed\n'+process.stdout)
    result=json.loads(process.stdout)
    require(result['ignore_environment'] and result['no_user_site']
            and result['optimize']==0,'runtime isolation flags differ')
    return result

def inputs(archive):
    manifest=read(PKG/'manifest.json')
    actual={p.relative_to(PKG).as_posix() for p in PKG.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=PKG/'manifest.json'}
    require(actual==set(manifest['package_files']),'package inventory differs')
    for name,digest in manifest['package_files'].items():
        require(sha256(safe(PKG,name).read_bytes()).hexdigest()==digest,'package identity differs: '+name)
    own=read(PKG/'source_bindings.json')['files'];deps=read(PKG/'dependencies.json')
    require({row['path'] for row in own}=={name for name in actual if name.startswith('source/')},'source inventory differs')
    for row in own:
        require(sha256(safe(PKG,row['path']).read_bytes()).hexdigest()==row['sha256'],'source identity differs')
    for row in deps:
        require(sha256(safe(archive,row['path']).read_bytes()).hexdigest()==row['sha256'],'archive dependency differs: '+row['path'])
    phase=read(PKG/'source/V5_gap_closure/certificate/phase_ledger.json')
    require(manifest['lower_enclosure']==phase['new_revenue']['decimal_enclosure'],'manifest lower differs')
    require(manifest['upper']==phase['new_exact_upper'] and manifest['upper_enclosure']==phase['new_upper']['decimal_enclosure'],'manifest upper differs')
    require(manifest['gap_enclosure']==phase['remaining_gap']['decimal_enclosure'] and manifest['guarantee']=='0.993382','manifest gap/guarantee differs')
    return own,deps,manifest

def call(command,label,cwd):
    start=time.monotonic()
    print('REPLAY_START',label,flush=True)
    process=subprocess.run([sys.executable,'-E','-s','-B','-X','utf8',*command],cwd=cwd,env=child_environment(),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
    require(process.returncode==0,'FAILED '+label+'\n'+process.stdout)
    print('REPLAY_PASS',label,'seconds',round(time.monotonic()-start,3),flush=True)
    return {'entrypoint':label,'exit_code':process.returncode,'elapsed_seconds':round(time.monotonic()-start,3),'output':process.stdout}

def main():
    require(sys.version_info>=(3,10) and sys.flags.optimize==0,'Python >=3.10 without optimization required')
    parser=argparse.ArgumentParser()
    parser.add_argument('--archive-root',type=Path,default=PKG.parents[1])
    parser.add_argument('--temp-root',type=Path)
    args=parser.parse_args()
    archive=args.archive_root.resolve()
    own,deps,manifest=inputs(archive)
    runtime=runtime_identity()
    print('RUNTIME_IDENTITY',json.dumps(runtime),flush=True)
    print('COMPONENT_SCOPE intermediate component at tau=1/100; final lower: ../reserve_parameter/verify_reserve.py',flush=True)
    records=[]
    temp_parent=(args.temp_root or Path(tempfile.gettempdir())).resolve()
    require(temp_parent.is_dir(),'temporary root does not exist')
    with tempfile.TemporaryDirectory(prefix='v5-',dir=temp_parent) as directory:
        stage=Path(directory).resolve()
        require(stage.parent==temp_parent and stage.name.startswith('v5-'),'unexpected temporary directory')
        auction=stage/PREFIX
        staged={}
        for row in deps:
            target=safe(stage,row['stage']);target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(safe(archive,row['path']),target);staged[target]=row['sha256']
        for row in own:
            target=safe(auction,row['origin']);target.parent.mkdir(parents=True,exist_ok=True)
            require(target not in staged,'duplicate staged source')
            shutil.copy2(safe(PKG,row['path']),target);staged[target]=row['sha256']
        for path,digest in staged.items():
            require(sha256(path.read_bytes()).hexdigest()==digest,'staging changed source bytes')
            if path.suffix=='.py':
                compile(path.read_text(encoding='utf-8'),str(path),'exec')
        for entry in manifest['entrypoints']:
            if entry['kind']=='source':
                script=safe(auction,entry['path'])
                command=[str(script)]
            else:
                command=[str(PKG/'provenance_adapter.py'),str(auction),entry['adapter']]
            records.append(call(command,entry['label'],auction))
        records.append(call([str(PKG/'portable_assembly.py'),str(auction)],'portable exact assembly',auction))
        for path,digest in staged.items():
            require(sha256(path.read_bytes()).hexdigest()==digest,'replay changed staged source: '+str(path.relative_to(stage)))
    inputs(archive)
    print('V5_PORTABLE_CERTIFICATE_PASS',len(records)-1,'mathematical replays plus exact assembly',flush=True)
    print('INTERMEDIATE_LOWER_ENCLOSURE_TAU_1_100',*manifest['lower_enclosure'])
    print('UPPER_EXACT',manifest['upper'])
    print('GUARANTEE_GT_99_3382_PERCENT_PASS OPTIMUM_OPEN')
    print(json.dumps({'status':'V5_PORTABLE_CERTIFICATE_PASS','source_files':len(own),'archive_dependencies':len(deps),'mathematical_replays':len(records)-1,'exact_assembly':True,'runtime':runtime,'records':records,'workspace_preservation_replayed':False},ensure_ascii=False),flush=True)

if __name__=='__main__':
    main()
