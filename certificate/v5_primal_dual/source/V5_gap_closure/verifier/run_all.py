"""Read-only V5 accepted proof replay; --record writes only its receipt."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import os
import subprocess
import sys
import time

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O.')

ROOT = Path(__file__).resolve().parents[1]
AUCTION = ROOT.parent
ENTRIES = [
    'verifier/global_duality.py',
    'verifier/bb_global.py',
    'verifier/primal_face_integrals.py',
    'verifier/primal_global.py',
    'verifier/primal_independent.py',
    'verifier/phase_ledger.py',
    'discovery/upper_splice_audit.py',
    'discovery/upper_bb_audit.py',
]

def preserve():
    base = Path(chr(92)*2+'?'+chr(92)+str(AUCTION)) if os.name == 'nt' else AUCTION
    lines = (ROOT/'certificate/baseline_SHA256SUMS').read_text().splitlines()
    for line in lines:
        digest, rel = line.split('  ', 1)
        assert rel != 'CURRENT_PHASE.md' and not rel.startswith('V5_gap_closure/')
        assert sha256((base/rel).read_bytes()).hexdigest() == digest, rel
    assert len(lines) == 4278
    return len(lines)

def snapshot():
    return {
        p.relative_to(ROOT).as_posix(): sha256(p.read_bytes()).hexdigest()
        for p in sorted(ROOT.rglob('*'))
        if p.is_file() and '__pycache__' not in p.parts
        and p.suffix != '.pyc'
        and p.relative_to(ROOT).as_posix() not in ('SHA256SUMS', 'certificate/replay_receipt.json')
    }

def call(rel, optimized=False):
    cmd = [sys.executable, '-B', '-X', 'utf8']
    if optimized:
        cmd.append('-O')
    cmd.append(str(ROOT/rel))
    start = time.monotonic()
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    output = result.stdout + result.stderr
    if optimized:
        assert result.returncode != 0 and 'Run without -O.' in output, (rel, output)
    else:
        assert result.returncode == 0, (rel, output)
    record = dict(entry=rel, optimized=optimized, status='PASS',
                  exit_code=result.returncode,
                  elapsed_seconds=round(time.monotonic()-start, 3),
                  output=output)
    print(('GUARD ' if optimized else 'REPLAY ') + rel + ': PASS', flush=True)
    return record

def main():
    assert sys.argv[1:] in ([], ['--record']), 'Only --record is accepted.'
    import numpy
    before = snapshot()
    count = preserve()
    pyfiles = list(ROOT.rglob('*.py'))
    for p in pyfiles:
        compile(p.read_text(encoding='utf-8'), str(p), 'exec')
    normal = [call(rel) for rel in ENTRIES]
    guards = [call(rel, True) for rel in ENTRIES + ['verifier/run_all.py']]
    assert snapshot() == before, 'Replay modified phase inputs.'
    assert preserve() == count
    receipt = dict(
        status='V5_ACCEPTED_GLOBAL_GAP_REDUCTION_REPLAY_PASS',
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        python=sys.version, numpy=numpy.__version__,
        normal_replays=normal, optimized_rejection_checks=guards,
        compiled_python_files=len(pyfiles), preserved_predecessor_files=count,
        source_hashes=before,
        acceptance_scope='All new accepted certificates and independent audits; inherited proofs and large historical integral certificates remain explicit hash-checked dependencies.',
        excluded='Unaccepted QQ curl and all other floating discovery gains.',
        unrestricted_optimum='OPEN')
    if '--record' in sys.argv:
        (ROOT/'certificate/replay_receipt.json').write_text(
            json.dumps(receipt, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(receipt['status'])
    print(f'{len(normal)} normal replays; {len(guards)} optimization guards; {len(pyfiles)} compiled files; {count} preserved predecessors.')

if __name__ == '__main__':
    main()
