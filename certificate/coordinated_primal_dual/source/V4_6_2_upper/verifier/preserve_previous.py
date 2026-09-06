"""Check predecessor identities and separately verify documented archive drift.

--strict also requires the initially unlisted archive-audit files unchanged.
The ordinary replay never calls a documented changed file preserved.
"""
from pathlib import Path
from hashlib import sha256
import argparse,json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
trial=Path(__file__).resolve().parents[1];root=trial.parent
expected=json.loads((trial/'certificate/predecessor_status.json').read_text(encoding='utf-8'))
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--strict',action='store_true');args=parser.parse_args()
comparison=json.loads((trial/'certificate/predecessor_final_comparison.json').read_text(encoding='utf-8'))
documented={entry['source']:{row['path']:row for row in entry['changes']} for entry in comparison}
seen=set();counts=[]
for filename in ('pre_V4_6_2_SHA256SUMS','preexisting_archive_audit_SHA256SUMS'):
    count=0;changes={}
    for line in (trial/'certificate'/filename).read_text(encoding='utf-8').splitlines():
        digest,relative=line.split('  ',1)
        assert not relative.startswith('/') and ':' not in relative and '..' not in Path(relative).parts
        assert relative not in seen;seen.add(relative)
        actual=trial/'certificate/pre_V4_6_2_CURRENT_PHASE.md' if relative=='CURRENT_PHASE.md' else root/relative
        current=sha256(actual.read_bytes()).hexdigest()
        if current!=digest:
            changes[relative]=(digest,current)
        count+=1
    if filename=='pre_V4_6_2_SHA256SUMS' or args.strict:
        assert not changes,changes
    assert changes=={path:(row['original_sha256'],row['current_sha256'])
                     for path,row in documented[filename].items()},changes
    print('PREDECESSOR_COMPARISON',filename,'unchanged',count-len(changes),
          'documented_changed',len(changes))
    counts.append(count)
assert counts==[expected['listed_prior_identities'],expected['preexisting_unlisted_archive_audit_files']]
print('LISTED_993_PREDECESSORS_PRESERVED_ARCHIVE_DRIFT_SEPARATELY_RECORDED')
