"""Read-only exact replay; no discovery or certificate-writing commands."""
from pathlib import Path
import subprocess,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
COMMANDS=(
    ('functional_kernel.py',),('functional_jump.py',),('functional_star.py',),
    ('structural_reserve_candidate.py',),('structural_reserve_candidate.py','--cap'),
    ('structural_variation_audit.py',),('structural_ic_trace.py',),
    ('residual_high_screening.py',),('residual_wing_screening.py',),
    ('refined_candidate.py',),('refined_revenue.py',),
    ('refined_revenue_audit.py',),('refined_structure_audit.py',),('branch_summary.py',),
)
def run(path,*args):
    subprocess.run([sys.executable,'-B','-X','utf8',str(path),*args],check=True,cwd=ROOT)
for command in COMMANDS:
    print('RUN',' '.join(command),flush=True)
    run(ROOT/'verifier'/command[0],*command[1:])
print('RUN preserved V4.6.1 mathematics and older provenance',flush=True)
run(ROOT.parent/'V4_6_1_lower_bound/verifier/run_all.py')
print('RUN V4.6.1 preservation',flush=True)
run(ROOT/'verifier/preserve_baseline.py')
print(f'V4_6_1_1_EXACT_REPLAY_PASS mathematical_replays={len(COMMANDS)} plus 12 preserved V4.6.1 replays',flush=True)
