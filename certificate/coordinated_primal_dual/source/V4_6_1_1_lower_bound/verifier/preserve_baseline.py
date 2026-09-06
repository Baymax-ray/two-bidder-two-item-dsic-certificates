"""Read-only verification of the frozen V4.6.1 branch and saved manifest."""
from hashlib import sha256
from pathlib import Path
import importlib.util,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
PREVIOUS=ROOT.parent/'V4_6_1_lower_bound'
saved=ROOT/'certificate/pre_V4_6_1_1_SHA256SUMS'
assert saved.read_bytes()==(PREVIOUS/'SHA256SUMS').read_bytes(),'V4.6.1 manifest changed'
spec=importlib.util.spec_from_file_location('baseline_manifest_checker',ROOT.parent/'verifier/verify_manifest.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
count=0
for line in saved.read_text(encoding='utf-8').splitlines():
    digest,name=line.split('  ',1)
    checker.validate_path(name)
    assert sha256((PREVIOUS/name).read_bytes()).hexdigest()==digest,'V4.6.1 identity changed: '+name
    count+=1
assert count==52
checker.verify(PREVIOUS)
print('V4_6_1_1_BASELINE_PRESERVATION_PASS',count,'unchanged V4.6.1 files and unchanged manifest')
print('Outer navigation, outer manifest and concurrent branches are not managed here.')
