"""Read-only exact replay; --skip-deep explicitly omits both full tree runs."""
from pathlib import Path
import argparse,subprocess,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--skip-deep',action='store_true');args=parser.parse_args()
def run(path,*extra):
    print('REPLAY',str(path),*extra,flush=True)
    subprocess.run([sys.executable,'-B','-X','utf8',str(path),*extra],check=True)
if args.skip_deep:
    print('DEEP_INTEGRATIONS_SKIPPED_THIS_INVOCATION',flush=True)
else:
    run(root/'flow_majorant.py')
    run(root/'verifier/independent_majorant.py')
run(root.parent/'V3_1/verifier/constrained_screening_verify.py')
run(root.parent/'V4_5/verifier/dual_support_verify.py')
run(root/'flow_sign.py')
run(root/'flow_sign.py','--cap','43/100','--output','flow_sign_43_certificate.json')
run(root/'flow_half_counterexample.py')
for name in ('conditional_global_splice.py','independent_conditional_splice.py',
             'conditional_lottery_redistribution.py','flatness_constraints.py',
             'sparse_cycle.py','flatness_sparse_cycle_audit.py',
             'remaining_lottery_slack.py','upper_ledger.py',
             'current_bound_comparison.py','current_lower_flatness.py','preserve_previous.py'):
    run(root/'verifier'/name)
print('V4_6_2_NONDEEP_EXACT_REPLAYS_PASS' if args.skip_deep else 'V4_6_2_ALL_EXACT_REPLAYS_PASS')
print('UNRESTRICTED_OPTIMUM_AND_EQUALITY_MECHANISM_REMAIN_OPEN')
