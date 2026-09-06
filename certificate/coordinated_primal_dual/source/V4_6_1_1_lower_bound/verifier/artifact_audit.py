"""Read-only JSON, Markdown target and display-formula packaging checks."""
from pathlib import Path
import json,re,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
json_count=0;markdown_count=0;link_count=0
for path in sorted(ROOT.rglob('*.json')):
    json.loads(path.read_text(encoding='utf-8'));json_count+=1
for path in sorted(ROOT.rglob('*.md')):
    text=path.read_text(encoding='utf-8');markdown_count+=1
    assert not any(ord(char)<32 and char not in '\n\r\t' for char in text),path
    assert text.count('\\[')==text.count('\\]'),('display delimiters',path)
    assert text.count('\\(')==text.count('\\)'),('inline delimiters',path)
    for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',text):
        target=target.strip('<>').split('#',1)[0]
        if not target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target):continue
        assert (path.parent/target).is_file(),('missing Markdown target',path,target)
        link_count+=1
print('V4_6_1_1_ARTIFACT_AUDIT_PASS',f'json={json_count}',f'markdown={markdown_count}',f'local_links={link_count}')
print('Python',sys.version.split()[0]);print('This checks packaging, not mathematical truth.')
