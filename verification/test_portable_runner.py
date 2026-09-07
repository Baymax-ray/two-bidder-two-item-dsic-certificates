"""Regression checks for portable path containment and Python import policy."""
from pathlib import Path, PureWindowsPath
from fractions import Fraction as F
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('portable_runner',ROOT/'certificate/v5_primal_dual/verify_v5.py')
runner=importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

class PortableRunnerTests(unittest.TestCase):
    def test_inside_path(self):
        root=ROOT/'certificate/v5_primal_dual'
        self.assertEqual(runner.safe(root,'source/V5_gap_closure/certificate/primal_global.json'),
                         (root/'source/V5_gap_closure/certificate/primal_global.json').resolve())

    def test_windows_anchored_and_escaping_names(self):
        # Both Windows cases passed the former is_absolute plus '..' test.
        for name in ('C:foo', r'\foo'):
            old=PureWindowsPath(name)
            self.assertFalse(old.is_absolute())
            self.assertNotIn('..',old.parts)
        for name in ('C:foo',r'C:\foo',r'\foo',r'\\server\share\foo',
                     '/foo','../foo','inside/../../foo','','.'):
            with self.subTest(name=name):
                with self.assertRaises(RuntimeError):
                    runner.safe(ROOT,name)

    def test_clean_import_environment(self):
        with tempfile.TemporaryDirectory(prefix='dsic-import-') as directory:
            shadow=Path(directory).resolve()
            self.assertTrue(shadow.name.startswith('dsic-import-'))
            for name in ('numpy','fractions'):
                (shadow/(name+'.py')).write_text("raise RuntimeError('INJECTED_MODULE')\n",encoding='utf-8')
            with patch.dict(os.environ,{'PYTHONPATH':str(shadow),
                                        'PYTHONHOME':str(shadow/'invalid'),
                                        'PYTHONUSERBASE':str(shadow)}):
                identity=runner.runtime_identity()
            self.assertEqual(identity['optimize'],0)
            self.assertTrue(identity['ignore_environment'] and identity['no_user_site'])
            self.assertEqual(Path(identity['executable']).resolve(),Path(sys.executable).resolve())
            for origin in identity['modules'].values():
                if origin:
                    self.assertFalse(Path(origin).resolve().is_relative_to(shadow))

    def test_optimized_entrypoints_reject_before_replay(self):
        paths=('certificate/v5_primal_dual/verify_v5.py',
               'certificate/reserve_parameter/verify_reserve.py',
               'certificate/reserve_parameter/mechanism.py',
               'certificate/reserve_parameter/check_implementation.py',
               'verification/reproduce_all.py')
        for name in paths:
            with self.subTest(name=name):
                result=subprocess.run([sys.executable,'-E','-s','-B','-O',str(ROOT/name)],
                    cwd=ROOT,env=runner.child_environment(),stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
                self.assertNotEqual(result.returncode,0)
                self.assertIn('optimiz',result.stdout.lower())

    def test_retained_zero_value_margins(self):
        # Exact inequalities retained from the former author revision check.
        A,d,c=F(2,3),F(1,2),F(157,500)
        q=d-c;T=1-2*c/3;U=F(5,3)-2*c;k=A-q
        K=lambda t:F(5,6)+3*t*t/4
        delta=9*(T-A)*(U-A)/16
        self.assertLess(c,k)
        self.assertLess(k,F(2,3))
        self.assertEqual(K(k)-k,F(525947,10**6))
        self.assertEqual(K(c)-A,F(721841,3000000))
        self.assertEqual(A-q-delta,F(1364159,3000000))
        self.assertGreater(A-d-delta,0)
        self.assertGreater(U,T)
        self.assertGreater(T,A)

if __name__=='__main__':
    if sys.flags.optimize:
        raise RuntimeError('Run without optimized Python mode')
    unittest.main()
