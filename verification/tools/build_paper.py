from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import tempfile,subprocess,shutil,json,sys
R=Path(__file__).resolve().parents[2]
label=sys.argv[1] if len(sys.argv)>1 else 'pre_review'
L=R/'verification/generated'/('build_'+label);L.mkdir(exist_ok=True,parents=True)
sources=list((R/'manuscript').glob('*.tex'))+[R/'manuscript/references.bib']
hashes={p.name:sha256(p.read_bytes()).hexdigest() for p in sources}
engine=Path('C:/Users/FangJ/TinyTeX/bin/windows')
with tempfile.TemporaryDirectory(prefix='paper-',dir='C:/tmp') as td:
 b=Path(td).resolve()
 assert b.parent==Path('C:/tmp').resolve() and b.name.startswith('paper-')
 for p in sources:shutil.copy2(p,b/p.name)
 latex=[str(engine/'pdflatex.exe'),'-interaction=nonstopmode','-halt-on-error','-file-line-error','manuscript.tex']
 commands=[latex,[str(engine/'bibtex.exe'),'manuscript'],latex,latex,latex]
 for i,cmd in enumerate(commands):
  q=subprocess.run(cmd,cwd=b,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (L/f'pass{i+1}.log').write_bytes(q.stdout)
  if q.returncode:print(q.stdout.decode(errors='replace')[-6000:]);raise SystemExit(q.returncode)
 for name in ['manuscript.pdf','manuscript.log','manuscript.bbl']:shutil.copy2(b/name,L/name)
 assert hashes=={p.name:sha256(p.read_bytes()).hexdigest() for p in sources}
 shutil.copy2(b/'manuscript.pdf',R/'manuscript/manuscript.pdf')
log=(L/'manuscript.log').read_text(errors='replace')
record=dict(status='PDF_BUILD_PASS',timestamp_utc=datetime.now(timezone.utc).isoformat(),
            source_sha256=hashes,pdf_sha256=sha256((L/'manuscript.pdf').read_bytes()).hexdigest(),
            engine=str(engine/'pdflatex.exe'),passes=len(commands),
            warnings=[line for line in log.splitlines() if any(k in line for k in ['Overfull','Underfull','Warning','Output written'])])
(L/'receipt.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(record['status']);print('\n'.join(record['warnings']))
