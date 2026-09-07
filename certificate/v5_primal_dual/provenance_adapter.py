"""Portable identity comparison for unchanged mathematical source functions.

Only documented provenance path separators and the unique external stream
manifest path are normalized. No inequality, arithmetic result, hash, count,
or mechanism claim is relaxed. The two audit functions require write=True to
return their full result without their nonportable final equality; they run
only in the disposable runtime tree, and their certificate bytes are restored.
"""
from pathlib import Path, PurePosixPath, PureWindowsPath
from hashlib import sha256
import importlib.util
import contextlib
import io
import json
import math
import sys

STREAM = 'research/closed/two-bidder-two-item-dsic-certificates/certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound/manifest.json'

def require(condition,message):
    if not condition:
        raise RuntimeError(message)

def normalized(record,field,manifest):
    out = dict(record)
    table = {}
    external = 0
    for key,digest in out[field].items():
        path = '/'.join(part for part in key.replace('\\','/').split('/') if part)
        if PureWindowsPath(key).is_absolute() or PurePosixPath(key).is_absolute():
            require(manifest is not None and path.endswith('/'+STREAM),'unexpected absolute provenance path '+key)
            require(digest==sha256(manifest.read_bytes()).hexdigest(),'external manifest identity differs')
            path = '@archive/'+STREAM
            external += 1
        require(path not in table,'provenance normalization collision')
        table[path] = digest
    require(external==(1 if manifest is not None else 0),'unexpected external provenance count')
    out[field] = table
    return out

def load(path):
    spec = importlib.util.spec_from_file_location('portable_'+path.stem,path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    require(sys.flags.optimize==0 and len(sys.argv)==3,'Run without optimization: adapter AUCTION KIND')
    auction = Path(sys.argv[1]).resolve()
    kind = sys.argv[2]
    require(auction.name=='two_bidder_two_item_full_dsic_exact_auction','unexpected runtime layout')
    if kind in ('fresh_structure','fresh_upper','fresh_face_cubature'):
        folder,stem,receipt={
            'fresh_structure':('primal_structure','fresh_structure_check','fresh_structure_receipt'),
            'fresh_upper':('upper','independent_upper_checks','independent_upper_checks'),
            'fresh_face_cubature':('replay_revenue','independent_face_cubature','independent_face_cubature'),
        }[kind]
        root=auction/'V5_archive_audit'/folder
        path=root/(receipt+'.json')
        before=path.read_bytes();expected=json.loads(before)
        module=load(root/(stem+'.py'))
        if kind=='fresh_structure':
            actual=module.calculate()
        else:
            output=io.StringIO()
            try:
                with contextlib.redirect_stdout(output):
                    module.main()
                actual=json.loads(path.read_text(encoding='utf-8')) if kind=='fresh_face_cubature' else json.loads(output.getvalue())
            finally:
                if path.read_bytes()!=before:
                    path.write_bytes(before)
        if kind=='fresh_face_cubature':
            for data in (expected,actual):
                elapsed=data.pop('elapsed_seconds')
                require(isinstance(elapsed,(int,float)) and math.isfinite(elapsed) and elapsed>=0,'invalid execution duration')
                source=data['original_archive_upper_source']
                normalized_path='/'.join(part for part in source.replace('\\','/').split('/') if part)
                require(normalized_path.endswith('/V4_6_2_upper/certificate/upper_ledger.json'),'unexpected fresh face provenance')
                data['original_archive_upper_source']='V4_6_2_upper/certificate/upper_ledger.json'
        require(expected==actual,'fresh audit result differs: '+kind)
        require(path.read_bytes()==before,'fresh audit receipt not restored')
        print('PORTABLE_FRESH_INDEPENDENT_AUDIT_PASS',kind,flush=True)
        return
    if kind=='numerical_remainder':
        root = auction/'V4_6_3_slack_atlas'
        path = root/'certificate/numerical_remainder.json'
        expected = json.loads(path.read_text(encoding='utf-8'))
        require(expected['settings']['depth_B']==20 and expected['settings']['depth_D']==20 and expected['settings']['depth_averaged']==26,'unexpected numerical depths')
        module = load(root/'verifier/numerical_remainder.py')
        actual = module.calculate(depth_b=20,depth_d=20,depth_avg=26)
        require(normalized(expected,'dependencies',None)==normalized(actual,'dependencies',None),'numerical certificate differs beyond path separators')
        print('PORTABLE_NUMERICAL_REMAINDER_DEPTH_20_20_26_PASS',flush=True)
        return
    require(kind in ('upper_splice_audit','upper_bb_audit'),'unknown provenance adapter')
    root = auction/'V5_gap_closure'
    path = root/'discovery'/(kind+'.json')
    before = path.read_bytes()
    expected = json.loads(before)
    module = load(root/'discovery'/(kind+'.py'))
    try:
        actual = module.run(True)
        require(json.loads(path.read_text(encoding='utf-8'))==actual,'generated audit output differs')
        manifest = auction.parents[2]/STREAM
        require(normalized(expected,'sources',manifest)==normalized(actual,'sources',manifest),'audit differs beyond documented provenance paths')
    finally:
        path.write_bytes(before)
    require(path.read_bytes()==before,'staged audit certificate not restored')
    print('PORTABLE_PROVENANCE_COMPARISON_PASS',kind,flush=True)

if __name__=='__main__':
    main()
