"""Read-only exact replay of V4.6.1 lower-bound mathematics and provenance.

Floating discovery programs are deliberately excluded. The branch manifest
is checked separately, so replay logs can be saved before sealing it.
"""
from pathlib import Path
import subprocess,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=(
    'parameter_candidate.py','parameter_revenue.py',
    'independent_family_revenue.py','gap_low_square.py',
    'sym_rescreen.py','sym_full_q_mirror.py',
    'gap_parameter_audit.py','sym_parameter_q_audit.py',
    'functional_exchange.py','independent_functional.py',
    'functional_gap_audit.py','branch_summary.py',
)
for script in SCRIPTS:
    print('RUN',script,flush=True)
    subprocess.run([sys.executable,'-B','-X','utf8',str(ROOT/'verifier'/script)],check=True,cwd=ROOT)
print('RUN predecessor identities',flush=True)
subprocess.run([sys.executable,'-B','-X','utf8',str(ROOT/'verifier/preserve_baseline.py')],check=True,cwd=ROOT)
print('RUN V4.6 manifest',flush=True)
subprocess.run([sys.executable,'-B','-X','utf8',str(ROOT.parent/'V4_6/verifier/verify_manifest.py')],check=True,cwd=ROOT)
print(f'V4_6_1_EXACT_REPLAY_PASS mathematical_replays={len(SCRIPTS)}',flush=True)
