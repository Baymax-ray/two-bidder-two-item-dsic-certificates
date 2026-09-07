from pathlib import Path
from PIL import Image, ImageDraw
from pypdf import PdfReader
from hashlib import sha256
import subprocess,sys,json
A=Path(__file__).resolve().parents[1]/'generated'
label=sys.argv[1] if len(sys.argv)>1 else 'pre_review'
B=A/('build_'+label)
R=B/'render';R.mkdir(exist_ok=True)
poppler=Path('C:/Users/FangJ/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin')
subprocess.run([str(poppler/'pdftoppm.exe'),'-r','80','-png',str(B/'manuscript.pdf'),str(R/'page')],check=True)
pages=sorted(R.glob('page-*.png'))
sheet=Image.new('RGB',(6*175,((len(pages)+5)//6)*266),'#dddddd')
draw=ImageDraw.Draw(sheet)
for i,path in enumerate(pages):
 im=Image.open(path);im.thumbnail((165,240))
 x=(i%6)*175+5;y=(i//6)*266+21
 sheet.paste(im,(x,y));draw.text((x,y-16),f'Page {i+1}',fill='black')
sheet.save(R/'contact_all_pages.png')
pdf=PdfReader(str(B/'manuscript.pdf'))
texts=[page.extract_text() or '' for page in pdf.pages]
report=dict(page_count=len(pdf.pages),render_count=len(pages),pdf_sha256=sha256((B/'manuscript.pdf').read_bytes()).hexdigest(),
 new_section_pages=[i+1 for i,t in enumerate(texts) if any(w in t for w in ['Global reserve','global reserve','support splice','Shared-endpoint','translated IC','translated-IC','common capacity price'])],
 zero_text_pages=[i+1 for i,t in enumerate(texts) if not t.strip()],
 reference_pages=[i+1 for i,t in enumerate(texts) if 'References' in t])
assert len(pdf.pages)==len(pages) and not report['zero_text_pages']
(B/'extracted.txt').write_text('\n\f\n'.join(texts),encoding='utf-8')
(B/'render_receipt.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
