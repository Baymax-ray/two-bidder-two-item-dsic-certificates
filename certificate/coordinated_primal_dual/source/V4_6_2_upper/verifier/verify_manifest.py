"""Read-only branch manifest and full stable-file inventory verification."""
from pathlib import Path
import importlib.util,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
trial=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('upper_manifest',trial.parent/'verifier/verify_manifest.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
checker.verify(trial)
