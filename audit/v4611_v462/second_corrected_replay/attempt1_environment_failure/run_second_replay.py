"""Author-side second corrected replay; only this audit directory is written."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
from math import isqrt
from datetime import datetime, timezone
import json
import os
import platform
import subprocess
import sys
import time
import uuid


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
PKG = ROOT / 'research/closed/two-bidder-two-item-dsic-certificates/certificate/coordinated_primal_dual'
ARCH = PKG.parents[1]


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def snapshot(label):
    result = {p.relative_to(PKG).as_posix(): digest(p)
              for p in sorted(PKG.rglob('*')) if p.is_file()}
    save(label + '_sha256.json', result)
    (OUT / (label + '_SHA256SUMS')).write_text(
        ''.join(h + '  ' + p + '\n' for p, h in result.items()), encoding='utf-8')
    return result


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def independent_reconciliation():
    m = read(PKG / 'manifest.json')
    lower = read(PKG / 'source/V4_6_1_1_lower_bound/certificate/branch_summary.json')
    upper = read(PKG / 'source/V4_6_2_upper/certificate/upper_ledger.json')
    third = read(PKG / 'source/V4_6_1_1_V4_6_2_archive_audit/lower_revenue/third_revenue_and_pairing.json')
    assert m['revenue_coefficients'] == lower['exact_revenue_coefficients'] == third['coefficients']
    assert m['revenue_basis'] == lower['field_basis'] == third['basis'] == ['1', 'sqrt(2)', 'sqrt(493894)']
    u = Fraction(m['upper'])
    assert u == Fraction(upper['final_upper'])
    assert u == Fraction(m['upper_anchor']) - Fraction(m['conditional_subtraction']) - Fraction(m['cycle_subtraction'])
    scale = 10 ** 60
    intervals = [(Fraction(1), Fraction(1))]
    for radicand in (2, 493894):
        n = isqrt(radicand * scale * scale)
        assert n * n <= radicand * scale * scale < (n + 1) * (n + 1)
        intervals.append((Fraction(n, scale), Fraction(n + 1, scale)))
    lo = hi = Fraction(0)
    for coefficient, (a, b) in zip(m['revenue_coefficients'], intervals):
        c = Fraction(coefficient)
        lo += c * (a if c >= 0 else b)
        hi += c * (b if c >= 0 else a)
    assert lo < hi
    exact = {'lower_enclosure': (lo, hi), 'upper_enclosure': (u, u),
             'gap_enclosure': (u - hi, u - lo), 'ratio_enclosure': (lo / u, hi / u)}
    for field, (a, b) in exact.items():
        assert Fraction(m[field][0]) <= a <= b <= Fraction(m[field][1]), field
    for field, third_field in [('lower_enclosure', 'revenue'), ('upper_enclosure', 'new_upper'),
                               ('gap_enclosure', 'gap'), ('ratio_enclosure', 'ratio_lower_over_upper')]:
        assert m[field] == third[third_field]
    assert u - lo < Fraction(1, 100)
    assert lo / u > Fraction(m['guarantee'])
    return {'status': 'PASS', 'method': 'Exact Fraction arithmetic; independently bounded radicals by integer-square-root intervals at 60 decimal places.',
            'revenue_basis': m['revenue_basis'], 'revenue_coefficients': m['revenue_coefficients'],
            'upper_exact': m['upper'], 'lower_enclosure': m['lower_enclosure'],
            'upper_enclosure': m['upper_enclosure'], 'gap_enclosure': m['gap_enclosure'],
            'ratio_enclosure': m['ratio_enclosure'], 'strict_gap_lt_1_100': True,
            'strict_ratio_gt_992684_over_1000000': True,
            'independent_lower_rational_bounds': [str(lo), str(hi)]}


def binding_check():
    own = read(PKG / 'source_bindings.json')['files']
    deps = read(PKG / 'dependencies.json')
    assert {e['path'] for e in own} == {p.relative_to(PKG).as_posix() for p in (PKG / 'source').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    for entry in own:
        assert digest(PKG / entry['path']) == entry['sha256'], entry['path']
    for entry in deps:
        assert digest(ARCH / entry['path']) == entry['sha256'], entry['path']
    return {'status': 'PASS', 'bound_source_files': len(own), 'dependency_files': len(deps)}


def main():
    assert sys.flags.optimize == 0
    started = datetime.now(timezone.utc).isoformat()
    tmp = OUT / ('temp_root_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '_' + uuid.uuid4().hex[:8])
    tmp.mkdir()
    extended_tmp = '\\\\?\\' + str(tmp) if os.name == 'nt' else str(tmp)
    env = os.environ.copy()
    env.update({'TEMP': extended_tmp, 'TMP': extended_tmp, 'PYTHONDONTWRITEBYTECODE': '1'})
    command = [sys.executable, '-B', '-X', 'utf8', str(PKG / 'verify_coordinated.py')]
    before = snapshot('before')
    environment = {'started_utc': started, 'python_executable': sys.executable,
                   'python_version': sys.version, 'python_optimize': sys.flags.optimize,
                   'platform': platform.platform(), 'command': command, 'cwd': str(PKG),
                   'process_TEMP': extended_tmp, 'process_TMP': extended_tmp,
                   'temporary_root': str(tmp), 'global_environment_modified': False,
                   'package': str(PKG), 'package_file_count': len(before),
                   'runner_sha256': digest(Path(__file__)),
                   'wrapper_sha256_before': before['verify_coordinated.py']}
    save('environment.json', environment)
    save('run_status.json', {'status': 'RUNNING', 'started_utc': started, 'command': command})
    print('SECOND_CORRECTED_REPLAY_STARTED', started, 'files', len(before), flush=True)
    timer = time.perf_counter()
    with (OUT / 'stdout.txt').open('w', encoding='utf-8') as stdout, (OUT / 'stderr.txt').open('w', encoding='utf-8') as stderr:
        result = subprocess.run(command, cwd=PKG, env=env, stdout=stdout, stderr=stderr)
    elapsed = time.perf_counter() - timer
    finished = datetime.now(timezone.utc).isoformat()
    after = snapshot('after')
    changed = [p for p in sorted(set(before) | set(after)) if before.get(p) != after.get(p)]
    stdout = (OUT / 'stdout.txt').read_text(encoding='utf-8')
    stderr = (OUT / 'stderr.txt').read_text(encoding='utf-8')
    entrypoints = read(PKG / 'entrypoints.json')
    expected = ['PASS ' + ' '.join(c) for c in entrypoints]
    actual = [line for line in stdout.splitlines() if line.startswith('PASS ')]
    marker = 'COORDINATED_PRIMAL_DUAL_CERTIFICATE_PASS 46 entrypoints'
    errors = []
    try:
        bindings = binding_check()
    except Exception as error:
        bindings = {'status': 'FAIL', 'error': repr(error)}
        errors.append('Final source/dependency binding check failed: ' + repr(error))
    try:
        endpoints = independent_reconciliation()
    except Exception as error:
        endpoints = {'status': 'FAIL', 'error': repr(error)}
        errors.append('Independent endpoint reconciliation failed: ' + repr(error))
    passed = (result.returncode == 0 and not changed and len(entrypoints) == 46 and actual == expected
              and marker in stdout.splitlines() and bindings['status'] == 'PASS' and endpoints['status'] == 'PASS')
    report = {'status': 'PASS' if passed else 'FAIL', 'role': 'Author-side validation; not an independent reviewer report.',
              'scope': 'Second fresh corrected full portable replay in a distinct temporary root, followed by source identity and exact endpoint reconciliation.',
              'started_utc': started, 'finished_utc': finished, 'elapsed_seconds': elapsed,
              'exit_code': result.returncode, 'command': command, 'temporary_root': str(tmp),
              'package_file_count_before': len(before), 'package_file_count_after': len(after),
              'all_package_files_unchanged': not changed, 'changed_paths': changed,
              'expected_entrypoint_count': len(entrypoints), 'passed_entrypoint_count': len(actual),
              'entrypoint_sequence_matches': actual == expected, 'final_marker_expected': marker,
              'final_marker_observed': marker in stdout.splitlines(),
              'stderr_empty': not stderr.strip(), 'final_source_identity': bindings,
              'wrapper_sha256_before': before.get('verify_coordinated.py'),
              'wrapper_sha256_after': after.get('verify_coordinated.py'),
              'manifest_sha256_before': before.get('manifest.json'),
              'manifest_sha256_after': after.get('manifest.json'),
              'endpoint_reconciliation': endpoints,
              'stdout_sha256': digest(OUT / 'stdout.txt'), 'stderr_sha256': digest(OUT / 'stderr.txt'),
              'errors': errors,
              'limitations': 'Validation establishes this finite frozen certificate replay and stated endpoint bracket; it does not establish optimality, convergence, or hypotheses beyond those of the certificate.'}
    save('validation_report.json', report)
    save('run_status.json', {'status': report['status'], 'finished_utc': finished, 'exit_code': result.returncode, 'elapsed_seconds': elapsed})
    lines = ['# Second corrected portable replay', '',
             'Author-side validation; this is not an independent reviewer report.', '',
             '**Result: ' + report['status'] + '**', '',
             '- Exit code: ' + str(result.returncode) + '.',
             '- Elapsed: ' + format(elapsed, '.3f') + ' seconds.',
             '- Completed entrypoints: ' + str(len(actual)) + '/' + str(len(entrypoints)) + '; expected sequence matches: ' + str(actual == expected) + '.',
             '- Final marker observed: ' + str(report['final_marker_observed']) + ' (`' + marker + '`).',
             '- Package source identity: ' + str(len(before)) + ' files before / ' + str(len(after)) + ' after; unchanged: ' + str(not changed) + '.',
             '- Final bound source/dependency identities: ' + bindings['status'] + '.',
             '- Independent exact endpoint reconciliation: ' + endpoints['status'] + '.',
             '- Separate stdout and stderr are retained; stderr empty: ' + str(report['stderr_empty']) + '.',
             '- UTC interval: ' + started + ' to ' + finished + '.',
             '- Distinct temporary root: `' + str(tmp) + '`.',
             '- Process-specific TEMP/TMP used Windows extended paths; the global environment was unchanged.', '',
             '## Endpoint reconciliation', '']
    if endpoints['status'] == 'PASS':
        for field in ('lower_enclosure', 'upper_enclosure', 'gap_enclosure', 'ratio_enclosure'):
            lines.append('- ' + field + ': [' + ', '.join(endpoints[field]) + '].')
        lines.extend(['- Strict gap < 1/100 and ratio > 992684/1000000: PASS.',
                      '- The radical bounds were recomputed with integer square roots and exact rational arithmetic at 60 decimal places.'])
    lines.extend(['', '## Source identity', '',
                  '- Wrapper SHA-256 before and after: `' + str(report['wrapper_sha256_before']) + '` / `' + str(report['wrapper_sha256_after']) + '`.',
                  '- Manifest SHA-256 before and after: `' + str(report['manifest_sha256_before']) + '` / `' + str(report['manifest_sha256_after']) + '`.',
                  '- Full inventories: `before_sha256.json`, `after_sha256.json`, `before_SHA256SUMS`, `after_SHA256SUMS`.',
                  '- Run evidence: `environment.json`, `stdout.txt`, `stderr.txt`, `validation_report.json`.', '', report['limitations'], ''])
    if errors or changed:
        lines.extend(['Errors: ' + repr(errors), 'Changed paths: ' + repr(changed), ''])
    (OUT / 'validation_report.md').write_text('\n'.join(lines), encoding='utf-8')
    print('SECOND_CORRECTED_REPLAY_' + report['status'], 'exit', result.returncode, 'entrypoints', len(actual), 'seconds', elapsed, flush=True)
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
