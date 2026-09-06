"""Read-only preservation of 992 live files and one archived navigation identity."""
from hashlib import sha256
from pathlib import Path
import sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
trial=Path(__file__).resolve().parents[1];root=trial.parent
saved=trial/'certificate/pre_V4_6_1_SHA256SUMS'
count=0
live_count=0
navigation_same=None
for line in saved.read_text(encoding='utf-8').splitlines():
    digest,name=line.split('  ',1)
    if name.startswith('/') or ':' in name or '..' in Path(name).parts:raise RuntimeError('unsafe saved path')
    if name=='CURRENT_PHASE.md':
        target=trial/'certificate/pre_V4_6_1_CURRENT_PHASE.md'
        navigation_same=sha256((root/name).read_bytes()).hexdigest()==digest
    else:
        target=root/name
        live_count+=1
    assert sha256(target.read_bytes()).hexdigest()==digest,'prior identity changed: '+name
    count+=1
assert count==993 and live_count==992 and navigation_same is not None
outer_same=saved.read_bytes()==(root/'SHA256SUMS').read_bytes()
print('V4_6_1_BASELINE_PRESERVATION_PASS',live_count,'unchanged live identities + 1 matching archived navigation identity')
print('live_navigation_matches_start_snapshot',navigation_same,'(not written or managed by this branch)')
print('outer_manifest_matches_start_snapshot',outer_same,'(not written or managed by this branch)')
print('Pre-existing unlisted audit/upper-branch files are outside this preservation claim.')
